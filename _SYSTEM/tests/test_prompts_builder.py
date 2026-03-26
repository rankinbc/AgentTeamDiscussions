"""Tests for agentteam.prompts.builder."""
import pytest

from agentteam.prompts.builder import (
    build_context_lens,
    build_perspective_reminder,
    build_system_prompt,
    filter_prior_rounds,
)
from agentteam.types import (
    AgentConfig,
    AntiSlopConfig,
    Brevity,
    CognitiveStyle,
    PersonalityConfig,
    PositionConfig,
    VoiceConfig,
)


# ---------------------------------------------------------------------------
# build_system_prompt
# ---------------------------------------------------------------------------

class TestBuildSystemPrompt:
    def test_returns_non_empty_string(self, minimal_agent):
        prompt = build_system_prompt(minimal_agent)
        assert isinstance(prompt, str)
        assert len(prompt) > 0

    def test_includes_agent_name(self, minimal_agent):
        prompt = build_system_prompt(minimal_agent)
        assert "Test Agent" in prompt

    def test_includes_description(self, minimal_agent):
        prompt = build_system_prompt(minimal_agent)
        assert "test agent" in prompt.lower()

    def test_includes_vocabulary_hints(self, rich_agent):
        prompt = build_system_prompt(rich_agent)
        assert "trade-off" in prompt

    def test_anti_patterns_listed(self, rich_agent):
        """Anti-patterns should appear in the voice section."""
        prompt = build_system_prompt(rich_agent)
        assert "I think" in prompt

    def test_devils_advocate_rule_included(self, rich_agent):
        prompt = build_system_prompt(rich_agent)
        assert "DEVIL" in prompt

    def test_agreement_tax_rule_included(self, rich_agent):
        prompt = build_system_prompt(rich_agent)
        assert "AGREEMENT TAX" in prompt

    def test_different_agents_produce_different_prompts(self, minimal_agent, rich_agent):
        assert build_system_prompt(minimal_agent) != build_system_prompt(rich_agent)

    def test_concise_brevity_mentioned(self, rich_agent):
        prompt = build_system_prompt(rich_agent)
        assert "300 words" in prompt  # concise brevity threshold

    def test_high_assertiveness_described(self):
        agent = AgentConfig(
            name="Assertive",
            description="High assertiveness agent.",
            personality=PersonalityConfig(assertiveness=0.95),
        )
        prompt = build_system_prompt(agent)
        assert "extremely assertive" in prompt

    def test_low_assertiveness_described(self):
        agent = AgentConfig(
            name="Gentle",
            description="Low assertiveness agent.",
            personality=PersonalityConfig(assertiveness=0.1),
        )
        prompt = build_system_prompt(agent)
        assert "strongly" in prompt and "reserved" in prompt

    def test_custom_role_included(self):
        agent = AgentConfig(
            name="Moderator",
            description="Runs discussions.",
            position=PositionConfig(role="facilitator"),
        )
        prompt = build_system_prompt(agent)
        assert "Facilitator" in prompt

    def test_no_antislop_section_when_all_disabled(self):
        agent = AgentConfig(
            name="Plain",
            description="No anti-slop rules.",
            anti_slop=AntiSlopConfig(
                agreement_tax=False,
                perspective_enforcement=False,
                devils_advocate_duty=False,
                uncomfortable_idea_quota=0,
                domain_pivot_trigger=False,
            ),
        )
        prompt = build_system_prompt(agent)
        assert "Anti-Slop" not in prompt


# ---------------------------------------------------------------------------
# build_perspective_reminder
# ---------------------------------------------------------------------------

class TestBuildPerspectiveReminder:
    def test_returns_non_empty_string(self, minimal_agent):
        reminder = build_perspective_reminder(minimal_agent)
        assert isinstance(reminder, str)
        assert len(reminder) > 0

    def test_includes_agent_name(self, minimal_agent):
        assert "Test Agent" in build_perspective_reminder(minimal_agent)

    def test_includes_cognitive_style(self, minimal_agent):
        reminder = build_perspective_reminder(minimal_agent)
        assert "analytical" in reminder

    def test_is_short(self, minimal_agent):
        """Perspective reminder should be a single bracketed line."""
        reminder = build_perspective_reminder(minimal_agent)
        assert reminder.startswith("[")
        assert reminder.endswith("]")


# ---------------------------------------------------------------------------
# build_context_lens
# ---------------------------------------------------------------------------

class TestBuildContextLens:
    def test_returns_empty_string_for_minimal_agent(self, minimal_agent):
        """Minimal agent has no drives, pushbacks, or domain affinities."""
        assert build_context_lens(minimal_agent) == ""

    def test_includes_drives_when_present(self):
        agent = AgentConfig(
            name="Focused",
            description="Has drives.",
            position=PositionConfig(drives=["user impact", "simplicity", "clarity"]),
        )
        lens = build_context_lens(agent)
        assert "user impact" in lens

    def test_includes_pushback_when_present(self):
        agent = AgentConfig(
            name="Critic",
            description="Pushes back.",
            position=PositionConfig(pushback_on=["over-engineering", "premature abstraction", "vague requirements"]),
        )
        lens = build_context_lens(agent)
        assert "over-engineering" in lens

    def test_high_receptivity_message_included(self):
        agent = AgentConfig(
            name="Open",
            description="Receptive.",
            personality=PersonalityConfig(idea_receptivity=0.9),
            position=PositionConfig(drives=["ideas", "novelty", "exploration"]),
        )
        lens = build_context_lens(agent)
        assert "Build on" in lens or "Pay close attention" in lens


# ---------------------------------------------------------------------------
# filter_prior_rounds
# ---------------------------------------------------------------------------

class TestFilterPriorRounds:
    def test_empty_string_returned_unchanged(self, minimal_agent):
        assert filter_prior_rounds("", minimal_agent) == ""

    def test_short_text_returned_unchanged(self, minimal_agent):
        text = "Short prior context."
        assert filter_prior_rounds(text, minimal_agent) == text

    def test_high_receptivity_and_patience_returns_original(self):
        agent = AgentConfig(
            name="Patient",
            description="Patient agent.",
            personality=PersonalityConfig(idea_receptivity=0.8, patience=0.8),
        )
        text = "x" * 5000
        assert filter_prior_rounds(text, agent) == text

    def test_low_patience_truncates_long_text(self):
        agent = AgentConfig(
            name="Impatient",
            description="Impatient agent.",
            personality=PersonalityConfig(idea_receptivity=0.5, patience=0.1),
        )
        long_text = "[Agent]: " + "context " * 500  # ~4500 chars
        result = filter_prior_rounds(long_text, agent)
        assert len(result) < len(long_text)
        assert "truncated" in result.lower()
