"""Tests for agentteam.agents.drift and drift integration in orchestrator."""

from unittest.mock import AsyncMock, patch

import pytest

from agentteam.agents.drift import build_drift_reminder, detect_drift
from agentteam.conversation.orchestrator import build_agent_payload, run_round
from agentteam.types import AgentConfig, PersonalityConfig, PositionConfig, TeamConfig


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def make_positioned_agent(
    role: str = "systems architect",
    drives: list[str] | None = None,
    pushback_on: list[str] | None = None,
) -> AgentConfig:
    """AgentConfig with a non-empty position (drives + pushback_on)."""
    return AgentConfig(
        name="Architect",
        description="A test agent with a position.",
        position=PositionConfig(
            role=role,
            drives=drives or ["data-driven decisions", "cost efficiency", "maintainability"],
            pushback_on=pushback_on or ["premature optimization", "scope creep", "over-engineering"],
        ),
    )


def make_team_with_positioned_agent(agent_key: str = "agent1") -> TeamConfig:
    return TeamConfig(agents={agent_key: make_positioned_agent()})


SAMPLE_QUESTION = {"number": 1, "title": "How should auth work?", "body": "Describe the auth flow."}


# ---------------------------------------------------------------------------
# TestDetectDrift
# ---------------------------------------------------------------------------


class TestDetectDrift:
    def test_no_drift_empty_response(self):
        agent = make_positioned_agent()
        assert detect_drift("", agent) is False

    def test_no_drift_no_identity_anchors(self, minimal_agent):
        """Agent with no drives/pushback — can't detect drift."""
        # minimal_agent has default PositionConfig (empty drives + pushback_on)
        assert detect_drift("I agree with everything that was said.", minimal_agent) is False

    def test_detects_agreement_without_drive_keywords(self):
        agent = make_positioned_agent()
        response = "I agree. That approach sounds reasonable."
        assert detect_drift(response, agent) is True

    def test_no_drift_agreement_with_drive_keywords(self):
        """Agreement + drive keyword present → agent is speaking in character."""
        agent = make_positioned_agent()
        # "data-driven" contains "data" (len > 3) → anchor word present
        response = "I agree that data-driven decisions are the right call here."
        assert detect_drift(response, agent) is False

    def test_detects_capitulation_phrase(self):
        agent = make_positioned_agent()
        response = "Perhaps you're right, we should reconsider the entire approach."
        assert detect_drift(response, agent) is True

    def test_detects_i_withdraw_phrase(self):
        agent = make_positioned_agent()
        response = "I withdraw my previous objection about the database schema."
        assert detect_drift(response, agent) is True

    def test_no_drift_response_with_pushback_keywords(self):
        """Response mentions pushback_on keywords → agent staying in character."""
        agent = make_positioned_agent()
        # "premature" (len > 3) is an anchor word from pushback_on
        response = "We should avoid premature optimization here. Let's focus on correctness first."
        assert detect_drift(response, agent) is False

    def test_case_insensitive(self):
        agent = make_positioned_agent()
        response = "I AGREE completely. Great approach!"
        assert detect_drift(response, agent) is True

    def test_no_drift_when_all_position_words_too_short(self):
        """Position words all ≤3 chars → anchor_words empty → return False (no-anchor case)."""
        agent = AgentConfig(
            name="Short",
            description="Agent with only short position words.",
            position=PositionConfig(
                role="tester",
                drives=["API", "UX", "QA"],
                pushback_on=["FUD", "BS", "PR"],
            ),
        )
        assert detect_drift("I agree completely.", agent) is False

    def test_capitulation_suppressed_when_anchor_words_present(self):
        """Capitulation phrase + anchor keyword → AC5 applies → drift NOT detected."""
        agent = make_positioned_agent()
        # "premature" is an anchor word from pushback_on; capitulation phrase present
        response = "I'll concede that premature optimization is the real risk here."
        assert detect_drift(response, agent) is False

    def test_capitulation_detected_when_no_anchor_words(self):
        """Capitulation phrase + no anchor keywords → drift detected."""
        agent = make_positioned_agent()
        response = "I'll concede the point entirely."
        assert detect_drift(response, agent) is True


# ---------------------------------------------------------------------------
# TestBuildDriftReminder
# ---------------------------------------------------------------------------


class TestBuildDriftReminder:
    def test_contains_role(self):
        agent = make_positioned_agent(role="security engineer")
        result = build_drift_reminder(agent)
        assert "security engineer" in result

    def test_contains_drives(self):
        agent = make_positioned_agent(
            drives=["security first", "zero trust model", "least privilege"]
        )
        result = build_drift_reminder(agent)
        assert "security first" in result
        assert "zero trust model" in result
        assert "least privilege" in result

    def test_contains_pushback_on(self):
        agent = make_positioned_agent(
            pushback_on=["implicit trust", "wide permissions", "credential sharing"]
        )
        result = build_drift_reminder(agent)
        assert "implicit trust" in result
        assert "wide permissions" in result

    def test_under_100_words(self):
        """Drift reminder must stay under 100 words (token budget constraint)."""
        agent = make_positioned_agent(
            role="senior systems architect",
            drives=["data-driven decisions", "cost efficiency", "maintainability"],
            pushback_on=["premature optimization", "scope creep", "over-engineering"],
        )
        result = build_drift_reminder(agent)
        assert len(result.split()) < 100

    def test_minimal_agent_uses_fallback_text(self, minimal_agent):
        """When drives/pushback_on are empty, fallback text is used."""
        result = build_drift_reminder(minimal_agent)
        assert "your stated priorities" in result
        assert "overreach and vagueness" in result

    def test_format_matches_ac_spec(self):
        """Result must contain the AC-specified format markers."""
        agent = make_positioned_agent()
        result = build_drift_reminder(agent)
        assert "Remember, you are" in result
        assert "drives are" in result
        assert "Push back on" in result


# ---------------------------------------------------------------------------
# TestBuildAgentPayloadDriftIntegration
# ---------------------------------------------------------------------------


class TestBuildAgentPayloadDriftIntegration:
    def test_drift_reminder_injected_when_drift_detected(self):
        """Agreement phrase without drive keywords triggers drift reminder in payload."""
        team = make_team_with_positioned_agent("agent1")
        # Pure agreement, no identity anchor words
        previous_response = "I agree. That all sounds reasonable to me."
        payload = build_agent_payload(
            "agent1", team, SAMPLE_QUESTION, "", "", "", "",
            previous_response=previous_response,
        )
        assert "DRIFT ALERT" in payload

    def test_no_drift_reminder_when_previous_response_empty(self):
        """Empty previous_response — no drift reminder injected."""
        team = make_team_with_positioned_agent("agent1")
        payload = build_agent_payload(
            "agent1", team, SAMPLE_QUESTION, "", "", "", "",
            previous_response="",
        )
        assert "DRIFT ALERT" not in payload

    def test_no_drift_reminder_when_no_drift(self):
        """Response in character — no drift reminder injected."""
        team = make_team_with_positioned_agent("agent1")
        # Response mentions "efficiency" (4 chars) from "cost efficiency"
        previous_response = (
            "The cost efficiency argument is compelling. "
            "We should prioritize maintainability over speed."
        )
        payload = build_agent_payload(
            "agent1", team, SAMPLE_QUESTION, "", "", "", "",
            previous_response=previous_response,
        )
        assert "DRIFT ALERT" not in payload


# ---------------------------------------------------------------------------
# TestRunRoundDriftIntegration
# ---------------------------------------------------------------------------


class TestRunRoundDriftIntegration:
    def setup_method(self):
        self.team = make_team_with_positioned_agent("agent1")
        self.system_prompts = {"agent1": "system prompt for agent1"}

    async def test_no_crash_when_previous_responses_none(self):
        """run_round with previous_responses=None completes without error."""
        with patch(
            "agentteam.conversation.orchestrator.run_claude_async",
            new=AsyncMock(return_value="mock response"),
        ):
            result = await run_round(
                agents=["agent1"],
                system_prompts=self.system_prompts,
                team=self.team,
                question=SAMPLE_QUESTION,
                decisions="",
                prior_rounds="",
                prior_specs="",
                open_questions="",
                timeout=15,
                previous_responses=None,
            )
        assert "agent1" in result

    async def test_previous_responses_forwarded_to_payload(self):
        """previous_responses dict is passed to build_agent_payload via detect_drift."""
        captured_payloads: list[str] = []

        async def fake_claude(system_prompt, payload, timeout):
            captured_payloads.append(payload)
            return "mock response"

        with patch("agentteam.conversation.orchestrator.run_claude_async", new=fake_claude):
            with patch(
                "agentteam.conversation.orchestrator.compute_speaking_order",
                return_value=["agent1"],
            ):
                await run_round(
                    agents=["agent1"],
                    system_prompts=self.system_prompts,
                    team=self.team,
                    question=SAMPLE_QUESTION,
                    decisions="",
                    prior_rounds="",
                    prior_specs="",
                    open_questions="",
                    timeout=15,
                    # Drifting response: pure agreement, no drive keywords
                    previous_responses={"agent1": "I agree completely. Great point!"},
                )

        assert len(captured_payloads) == 1
        assert "DRIFT ALERT" in captured_payloads[0]
