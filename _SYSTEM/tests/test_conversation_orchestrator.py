"""Unit tests for agentteam/conversation/orchestrator.py.

Uses mocked run_claude_async — no real Claude calls.
"""

from unittest.mock import AsyncMock, call, patch

import pytest

from agentteam.conversation.orchestrator import build_agent_payload, compute_speaking_order, run_round
from agentteam.types import AgentConfig, PersonalityConfig, PositionConfig, TeamConfig

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

SAMPLE_QUESTION = {"number": 1, "title": "How should auth work?", "body": "Describe the auth flow."}


def make_team(specs: dict[str, dict]) -> TeamConfig:
    """Build a minimal TeamConfig for tests from a dict of {key: overrides}."""
    agents: dict[str, AgentConfig] = {}
    for key, overrides in specs.items():
        personality = PersonalityConfig(**overrides.get("personality", {}))
        position = PositionConfig(**overrides.get("position", {}))
        agents[key] = AgentConfig(
            name=overrides.get("name", key),
            description=overrides.get("description", f"Test agent {key}"),
            personality=personality,
            position=position,
        )
    return TeamConfig(agents=agents)


def make_system_prompts(team: TeamConfig) -> dict[str, str]:
    return {key: f"system prompt for {key}" for key in team.agents}


# ---------------------------------------------------------------------------
# TestComputeSpeakingOrder
# ---------------------------------------------------------------------------

class TestComputeSpeakingOrder:
    def test_returns_all_agents(self):
        team = make_team({
            "alpha": {"personality": {"assertiveness": 0.5}},
            "beta": {"personality": {"assertiveness": 0.3}},
            "gamma": {"personality": {"assertiveness": 0.8}},
        })
        result = compute_speaking_order(["alpha", "beta", "gamma"], team)
        assert sorted(result) == ["alpha", "beta", "gamma"]

    def test_returns_correct_length(self):
        team = make_team({
            "a": {"personality": {"assertiveness": 0.5}},
            "b": {"personality": {"assertiveness": 0.5}},
        })
        result = compute_speaking_order(["a", "b"], team)
        assert len(result) == 2

    def test_high_assertiveness_first(self):
        """High-assertiveness agent should appear before low-assertiveness across multiple runs."""
        team = make_team({
            "high": {"personality": {"assertiveness": 1.0, "stubbornness": 1.0}},
            "low": {"personality": {"assertiveness": 0.0, "stubbornness": 0.0}},
        })
        # Run 10 times to account for jitter — the gap is large enough to be stable
        wins = sum(
            1
            for _ in range(10)
            if compute_speaking_order(["high", "low"], team)[0] == "high"
        )
        assert wins >= 8  # expect high to win at least 8 of 10

    def test_single_agent(self):
        team = make_team({"solo": {}})
        result = compute_speaking_order(["solo"], team)
        assert result == ["solo"]


# ---------------------------------------------------------------------------
# TestBuildAgentPayload
# ---------------------------------------------------------------------------

class TestBuildAgentPayload:
    def setup_method(self):
        self.team = make_team({"agent1": {"name": "Agent One"}})
        self.question = SAMPLE_QUESTION

    def test_contains_question_title(self):
        payload = build_agent_payload("agent1", self.team, self.question, "", "", "", "")
        assert "How should auth work?" in payload

    def test_contains_question_body(self):
        payload = build_agent_payload("agent1", self.team, self.question, "", "", "", "")
        assert "Describe the auth flow." in payload

    def test_contains_decisions_when_provided(self):
        payload = build_agent_payload(
            "agent1", self.team, self.question,
            decisions="Use JWT tokens.",
            prior_rounds="", prior_specs="", open_questions="",
        )
        assert "JWT tokens" in payload
        assert "What's Already Decided" in payload

    def test_omits_decisions_when_empty(self):
        payload = build_agent_payload(
            "agent1", self.team, self.question,
            decisions="", prior_rounds="", prior_specs="", open_questions="",
        )
        assert "What's Already Decided" not in payload

    def test_first_speaker_prompt(self):
        """When this_round_so_far is empty, payload says 'speaking first'."""
        payload = build_agent_payload(
            "agent1", self.team, self.question, "", "", "", "",
            this_round_so_far="",
        )
        assert "speaking first" in payload.lower()

    def test_subsequent_speaker_prompt(self):
        """When this_round_so_far has content, payload says 'already spoken'."""
        payload = build_agent_payload(
            "agent1", self.team, self.question, "", "", "", "",
            this_round_so_far="[Other Agent]\nSome prior response.\n\n",
        )
        assert "already spoken" in payload.lower()

    def test_contains_prior_rounds(self):
        payload = build_agent_payload(
            "agent1", self.team, self.question, "",
            prior_rounds="[PROPOSE - Agent Two]\nProposal text here.\n\n",
            prior_specs="", open_questions="",
        )
        # Prior rounds appear in Discussion So Far section
        assert "Discussion So Far" in payload

    def test_contains_prior_specs(self):
        payload = build_agent_payload(
            "agent1", self.team, self.question, "", "",
            prior_specs="## Previous design doc", open_questions="",
        )
        assert "Prior Design Docs" in payload
        assert "Previous design doc" in payload

    def test_contains_round_instruction(self):
        payload = build_agent_payload(
            "agent1", self.team, self.question, "", "", "", "",
            round_instruction="Counter-propose the previous idea.",
        )
        assert "Counter-propose the previous idea." in payload

    def test_omits_prior_specs_when_empty(self):
        payload = build_agent_payload(
            "agent1", self.team, self.question, "", "", prior_specs="", open_questions="",
        )
        assert "Prior Design Docs" not in payload


# ---------------------------------------------------------------------------
# TestRunRound
# ---------------------------------------------------------------------------

class TestRunRound:
    def setup_method(self):
        self.team = make_team({
            "alpha": {"name": "Alpha Agent", "personality": {"assertiveness": 0.5}},
            "beta": {"name": "Beta Agent", "personality": {"assertiveness": 0.5}},
        })
        self.system_prompts = make_system_prompts(self.team)

    async def test_returns_all_agents(self):
        with patch(
            "agentteam.conversation.orchestrator.run_claude_async",
            new=AsyncMock(return_value="mock response"),
        ):
            result = await run_round(
                agents=["alpha", "beta"],
                system_prompts=self.system_prompts,
                team=self.team,
                question=SAMPLE_QUESTION,
                decisions="",
                prior_rounds="",
                prior_specs="",
                open_questions="",
                timeout=15,
            )
        assert "alpha" in result
        assert "beta" in result

    async def test_calls_claude_once_per_agent(self):
        mock_claude = AsyncMock(return_value="mock response")
        with patch("agentteam.conversation.orchestrator.run_claude_async", new=mock_claude):
            await run_round(
                agents=["alpha", "beta"],
                system_prompts=self.system_prompts,
                team=self.team,
                question=SAMPLE_QUESTION,
                decisions="",
                prior_rounds="",
                prior_specs="",
                open_questions="",
                timeout=15,
            )
        assert mock_claude.call_count == 2

    async def test_sequential_accumulation(self):
        """Second agent's payload should contain first agent's response."""
        captured_payloads: list[str] = []

        async def fake_claude(system_prompt, payload, timeout):
            captured_payloads.append(payload)
            return "response from agent"

        with patch("agentteam.conversation.orchestrator.run_claude_async", new=fake_claude):
            with patch(
                "agentteam.conversation.orchestrator.compute_speaking_order",
                return_value=["alpha", "beta"],
            ):
                await run_round(
                    agents=["alpha", "beta"],
                    system_prompts=self.system_prompts,
                    team=self.team,
                    question=SAMPLE_QUESTION,
                    decisions="",
                    prior_rounds="",
                    prior_specs="",
                    open_questions="",
                    timeout=15,
                )

        # First agent's payload — no prior speakers
        assert "already spoken" not in captured_payloads[0].lower()
        # Second agent's payload — contains first agent's response
        assert "response from agent" in captured_payloads[1]

    async def test_on_agent_done_called(self):
        done_calls: list[tuple] = []

        def on_done(agent_key: str, response: str, elapsed: float):
            done_calls.append((agent_key, response, elapsed))

        with patch(
            "agentteam.conversation.orchestrator.run_claude_async",
            new=AsyncMock(return_value="mock response"),
        ):
            await run_round(
                agents=["alpha", "beta"],
                system_prompts=self.system_prompts,
                team=self.team,
                question=SAMPLE_QUESTION,
                decisions="",
                prior_rounds="",
                prior_specs="",
                open_questions="",
                timeout=15,
                on_agent_done=on_done,
            )

        assert len(done_calls) == 2
        # Each call has (agent_key, response, elapsed)
        agent_keys = {c[0] for c in done_calls}
        assert agent_keys == {"alpha", "beta"}
        for _, response, elapsed in done_calls:
            assert response == "mock response"
            assert isinstance(elapsed, float)

    async def test_on_agent_start_called(self):
        start_calls: list[str] = []

        with patch(
            "agentteam.conversation.orchestrator.run_claude_async",
            new=AsyncMock(return_value="mock response"),
        ):
            await run_round(
                agents=["alpha", "beta"],
                system_prompts=self.system_prompts,
                team=self.team,
                question=SAMPLE_QUESTION,
                decisions="",
                prior_rounds="",
                prior_specs="",
                open_questions="",
                timeout=15,
                on_agent_start=start_calls.append,
            )

        assert sorted(start_calls) == ["alpha", "beta"]

    async def test_response_stored_per_agent_key(self):
        """Each agent's response is stored by its key in the returned dict."""
        call_count = 0

        async def fake_claude(system_prompt, payload, timeout):
            nonlocal call_count
            call_count += 1
            return f"response_{call_count}"

        with patch("agentteam.conversation.orchestrator.run_claude_async", new=fake_claude):
            result = await run_round(
                agents=["alpha", "beta"],
                system_prompts=self.system_prompts,
                team=self.team,
                question=SAMPLE_QUESTION,
                decisions="",
                prior_rounds="",
                prior_specs="",
                open_questions="",
                timeout=15,
            )

        # Each agent has a response string
        assert all(v.startswith("response_") for v in result.values())
