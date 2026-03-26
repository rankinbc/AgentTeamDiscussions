"""Unit tests for agentteam/synthesis/doc.py.

Uses mocked run_claude_async — no real Claude calls.
"""

from unittest.mock import AsyncMock, patch

import pytest

from agentteam.synthesis.doc import _MIN_SYNTHESIS_LENGTH, build_synthesis_input, synthesize

# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------

SAMPLE_QUESTION = {"number": 1, "title": "How should auth work?", "body": "Describe the auth flow."}

SAMPLE_ROUND_RESPONSES = {
    "propose": {"agent_a": "I propose JWT tokens.", "agent_b": "I suggest OAuth2."},
    "critique": {"agent_c": "JWT has expiry issues.", "agent_d": "OAuth2 is complex."},
    "evaluate": {"agent_e": "JWT is better for our use case."},
}

ROUND_LABELS = ["propose", "critique", "evaluate"]

SYNTHESIS_PROMPT = "You are a neutral moderator. Synthesize the discussion into a design doc."

VALID_DESIGN_DOC = (
    "## Decisions\n\nUse JWT tokens for authentication.\n\n"
    "## Exclusions\n\nOAuth2 was considered but rejected as too complex.\n\n"
    "## Blocking Open Items\n\nNone.\n\n"
    "## Non-Blocking Open Items\n\nToken refresh strategy to be determined."
)


# ---------------------------------------------------------------------------
# TestBuildSynthesisInput
# ---------------------------------------------------------------------------

class TestBuildSynthesisInput:
    def test_contains_question_title(self):
        result = build_synthesis_input(SAMPLE_QUESTION, SAMPLE_ROUND_RESPONSES, ROUND_LABELS)
        assert "How should auth work?" in result

    def test_contains_question_body(self):
        result = build_synthesis_input(SAMPLE_QUESTION, SAMPLE_ROUND_RESPONSES, ROUND_LABELS)
        assert "Describe the auth flow." in result

    def test_contains_round_label_propose(self):
        result = build_synthesis_input(SAMPLE_QUESTION, SAMPLE_ROUND_RESPONSES, ROUND_LABELS)
        assert "## Round: PROPOSE" in result

    def test_contains_round_label_critique(self):
        result = build_synthesis_input(SAMPLE_QUESTION, SAMPLE_ROUND_RESPONSES, ROUND_LABELS)
        assert "## Round: CRITIQUE" in result

    def test_contains_round_label_evaluate(self):
        result = build_synthesis_input(SAMPLE_QUESTION, SAMPLE_ROUND_RESPONSES, ROUND_LABELS)
        assert "## Round: EVALUATE" in result

    def test_contains_agent_responses(self):
        result = build_synthesis_input(SAMPLE_QUESTION, SAMPLE_ROUND_RESPONSES, ROUND_LABELS)
        assert "I propose JWT tokens." in result
        assert "JWT has expiry issues." in result
        assert "JWT is better for our use case." in result

    def test_contains_decisions_when_provided(self):
        result = build_synthesis_input(
            SAMPLE_QUESTION, SAMPLE_ROUND_RESPONSES, ROUND_LABELS,
            decisions="Use stateless auth only.",
        )
        assert "Prior Decisions" in result
        assert "Use stateless auth only." in result

    def test_omits_decisions_when_empty(self):
        result = build_synthesis_input(
            SAMPLE_QUESTION, SAMPLE_ROUND_RESPONSES, ROUND_LABELS,
            decisions="",
        )
        assert "Prior Decisions" not in result

    def test_contains_prior_specs_when_provided(self):
        result = build_synthesis_input(
            SAMPLE_QUESTION, SAMPLE_ROUND_RESPONSES, ROUND_LABELS,
            prior_specs="# Previous design doc\n\nSome context.",
        )
        assert "Prior Design Docs" in result
        assert "Previous design doc" in result

    def test_omits_prior_specs_when_empty(self):
        result = build_synthesis_input(
            SAMPLE_QUESTION, SAMPLE_ROUND_RESPONSES, ROUND_LABELS,
            prior_specs="",
        )
        assert "Prior Design Docs" not in result

    def test_round_order_preserved(self):
        """Rounds appear in the order given by round_labels."""
        result = build_synthesis_input(
            SAMPLE_QUESTION, SAMPLE_ROUND_RESPONSES,
            round_labels=["evaluate", "propose"],
        )
        evaluate_pos = result.index("## Round: EVALUATE")
        propose_pos = result.index("## Round: PROPOSE")
        assert evaluate_pos < propose_pos

    def test_ends_with_synthesis_instruction(self):
        result = build_synthesis_input(SAMPLE_QUESTION, SAMPLE_ROUND_RESPONSES, ROUND_LABELS)
        assert "Start with '## Decisions'" in result

    def test_counter_round_label_formatted(self):
        """'counter' round name is formatted as COUNTER-PROPOSAL."""
        responses = {"counter": {"agent_a": "Counter proposal."}}
        result = build_synthesis_input(SAMPLE_QUESTION, responses, ["counter"])
        assert "## Round: COUNTER-PROPOSAL" in result

    def test_missing_round_produces_empty_section(self):
        """If a round_label has no entry in round_responses, the section is still present."""
        result = build_synthesis_input(
            SAMPLE_QUESTION, {}, ["propose"],
        )
        assert "## Round: PROPOSE" in result


# ---------------------------------------------------------------------------
# TestSynthesize
# ---------------------------------------------------------------------------

class TestSynthesize:
    async def test_returns_string_on_success(self):
        with patch(
            "agentteam.synthesis.doc.run_claude_async",
            new=AsyncMock(return_value=VALID_DESIGN_DOC),
        ):
            result = await synthesize(
                SAMPLE_QUESTION, SAMPLE_ROUND_RESPONSES, ROUND_LABELS,
                system_prompt=SYNTHESIS_PROMPT, timeout=15,
            )
        assert isinstance(result, str)
        assert len(result) >= _MIN_SYNTHESIS_LENGTH

    async def test_raises_on_empty_response(self):
        with patch(
            "agentteam.synthesis.doc.run_claude_async",
            new=AsyncMock(return_value=""),
        ):
            with pytest.raises(RuntimeError, match="empty/minimal"):
                await synthesize(
                    SAMPLE_QUESTION, SAMPLE_ROUND_RESPONSES, ROUND_LABELS,
                    system_prompt=SYNTHESIS_PROMPT, timeout=15,
                )

    async def test_raises_on_short_response(self):
        short = "Too short"  # less than _MIN_SYNTHESIS_LENGTH
        assert len(short) < _MIN_SYNTHESIS_LENGTH
        with patch(
            "agentteam.synthesis.doc.run_claude_async",
            new=AsyncMock(return_value=short),
        ):
            with pytest.raises(RuntimeError):
                await synthesize(
                    SAMPLE_QUESTION, SAMPLE_ROUND_RESPONSES, ROUND_LABELS,
                    system_prompt=SYNTHESIS_PROMPT, timeout=15,
                )

    async def test_passes_system_prompt(self):
        mock_claude = AsyncMock(return_value=VALID_DESIGN_DOC)
        with patch("agentteam.synthesis.doc.run_claude_async", new=mock_claude):
            await synthesize(
                SAMPLE_QUESTION, SAMPLE_ROUND_RESPONSES, ROUND_LABELS,
                system_prompt=SYNTHESIS_PROMPT, timeout=15,
            )
        # system_prompt is the first positional arg to run_claude_async
        args = mock_claude.call_args[0]
        assert args[0] == SYNTHESIS_PROMPT

    async def test_passes_timeout(self):
        mock_claude = AsyncMock(return_value=VALID_DESIGN_DOC)
        with patch("agentteam.synthesis.doc.run_claude_async", new=mock_claude):
            await synthesize(
                SAMPLE_QUESTION, SAMPLE_ROUND_RESPONSES, ROUND_LABELS,
                system_prompt=SYNTHESIS_PROMPT, timeout=42,
            )
        call_kwargs = mock_claude.call_args[1]
        assert call_kwargs.get("timeout") == 42

    async def test_input_contains_synthesis_instruction(self):
        """The assembled input passed to Claude ends with the synthesis directive."""
        captured_inputs: list[str] = []

        async def fake_claude(system_prompt, user_message, timeout):
            captured_inputs.append(user_message)
            return VALID_DESIGN_DOC

        with patch("agentteam.synthesis.doc.run_claude_async", new=fake_claude):
            await synthesize(
                SAMPLE_QUESTION, SAMPLE_ROUND_RESPONSES, ROUND_LABELS,
                system_prompt=SYNTHESIS_PROMPT, timeout=15,
            )

        assert len(captured_inputs) == 1
        assert "Start with '## Decisions'" in captured_inputs[0]

    async def test_raises_on_none_response(self):
        with patch(
            "agentteam.synthesis.doc.run_claude_async",
            new=AsyncMock(return_value=None),
        ):
            with pytest.raises(RuntimeError):
                await synthesize(
                    SAMPLE_QUESTION, SAMPLE_ROUND_RESPONSES, ROUND_LABELS,
                    system_prompt=SYNTHESIS_PROMPT, timeout=15,
                )
