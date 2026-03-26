"""Tests for agentteam.prompts.identity -- Jinja2-rendered identity layer."""

from pathlib import Path

import pytest

from agentteam.prompts.identity import build_identity_layer
from agentteam.types import AgentConfig, PersonalityConfig, PositionConfig, TechniqueConfig


# ---------------------------------------------------------------------------
# TestBuildIdentityLayer
# ---------------------------------------------------------------------------


class TestBuildIdentityLayer:
    def test_name_in_output(self, minimal_agent):
        result = build_identity_layer(minimal_agent)
        assert "Test Agent" in result

    def test_description_in_output(self, minimal_agent):
        result = build_identity_layer(minimal_agent)
        assert "test agent" in result.lower()

    def test_drives_in_output(self):
        agent = AgentConfig(
            name="Focused",
            description="Has drives.",
            position=PositionConfig(drives=["user impact", "simplicity", "clarity"]),
        )
        result = build_identity_layer(agent)
        assert "user impact" in result
        assert "simplicity" in result
        assert "clarity" in result

    def test_pushback_in_output(self):
        agent = AgentConfig(
            name="Critic",
            description="Has pushback.",
            position=PositionConfig(
                pushback_on=["over-engineering", "premature abstraction", "vague requirements"]
            ),
        )
        result = build_identity_layer(agent)
        assert "over-engineering" in result
        assert "premature abstraction" in result

    def test_trait_band_extremely_high(self):
        agent = AgentConfig(
            name="A",
            description="High assertiveness.",
            personality=PersonalityConfig(assertiveness=0.95),
        )
        result = build_identity_layer(agent)
        assert "extremely assertive" in result

    def test_trait_band_quite_high(self):
        agent = AgentConfig(
            name="A",
            description="Quite high assertiveness.",
            personality=PersonalityConfig(assertiveness=0.7),
        )
        result = build_identity_layer(agent)
        assert "quite assertive" in result

    def test_trait_band_balanced(self):
        agent = AgentConfig(
            name="A",
            description="Balanced assertiveness.",
            personality=PersonalityConfig(assertiveness=0.5),
        )
        result = build_identity_layer(agent)
        assert "balance" in result
        assert "reserved" in result
        assert "assertive" in result

    def test_trait_band_lean_low(self):
        agent = AgentConfig(
            name="A",
            description="Lean low assertiveness.",
            personality=PersonalityConfig(assertiveness=0.3),
        )
        result = build_identity_layer(agent)
        assert "lean toward" in result
        assert "reserved" in result

    def test_trait_band_strongly_low(self):
        agent = AgentConfig(
            name="A",
            description="Strongly low assertiveness.",
            personality=PersonalityConfig(assertiveness=0.1),
        )
        result = build_identity_layer(agent)
        assert "strongly" in result
        assert "reserved" in result

    def test_technique_name_in_output(self):
        agent = AgentConfig(
            name="Thinker",
            description="Uses a technique.",
            technique=TechniqueConfig(
                primary="first_principles",
                style_description="Break every assumption down to its roots.",
                behaviors=[
                    "Question every assumption",
                    "Rebuild from scratch",
                    "List axioms explicitly",
                    "Avoid analogies",
                    "Derive conclusions step by step",
                ],
            ),
        )
        result = build_identity_layer(agent)
        assert "First Principles" in result

    def test_style_description_in_output(self):
        agent = AgentConfig(
            name="Thinker",
            description="Uses a technique.",
            technique=TechniqueConfig(
                primary="first_principles",
                style_description="Break every assumption down to its roots.",
                behaviors=[
                    "Question every assumption",
                    "Rebuild from scratch",
                    "List axioms explicitly",
                    "Avoid analogies",
                    "Derive conclusions step by step",
                ],
            ),
        )
        result = build_identity_layer(agent)
        assert "Break every assumption down to its roots." in result

    def test_behaviors_in_output(self):
        agent = AgentConfig(
            name="Thinker",
            description="Uses a technique.",
            technique=TechniqueConfig(
                primary="analysis",
                behaviors=[
                    "Be rigorous",
                    "Cite evidence",
                    "State assumptions explicitly",
                    "Quantify uncertainty",
                    "Flag logical leaps",
                ],
            ),
        )
        result = build_identity_layer(agent)
        assert "Be rigorous" in result
        assert "Cite evidence" in result

    def test_domain_affinities_in_output(self):
        agent = AgentConfig(
            name="Expert",
            description="Has domain affinities.",
            personality=PersonalityConfig(domain_affinities=["economics", "game theory"]),
        )
        result = build_identity_layer(agent)
        assert "economics" in result
        assert "game theory" in result

    def test_role_section_header(self):
        agent = AgentConfig(
            name="Mod",
            description="Facilitator.",
            position=PositionConfig(role="facilitator"),
        )
        result = build_identity_layer(agent)
        assert "## Your Role: Facilitator" in result

    def test_personality_section_header(self, minimal_agent):
        result = build_identity_layer(minimal_agent)
        assert "## Your Personality" in result

    def test_technique_section_header(self, minimal_agent):
        result = build_identity_layer(minimal_agent)
        assert "## Your Thinking Technique:" in result

    def test_no_drives_section_when_empty(self, minimal_agent):
        result = build_identity_layer(minimal_agent)
        assert "What drives you:" not in result

    def test_no_pushback_section_when_empty(self, minimal_agent):
        result = build_identity_layer(minimal_agent)
        assert "You actively push back on:" not in result

    def test_high_intensity_line(self):
        agent = AgentConfig(
            name="A",
            description="High intensity.",
            position=PositionConfig(intensity=0.9),
        )
        result = build_identity_layer(agent)
        assert "force and passion" in result

    def test_mid_intensity_line(self):
        agent = AgentConfig(
            name="A",
            description="Mid intensity.",
            position=PositionConfig(intensity=0.5),
        )
        result = build_identity_layer(agent)
        assert "conviction" in result

    def test_low_intensity_line(self):
        agent = AgentConfig(
            name="A",
            description="Low intensity.",
            position=PositionConfig(intensity=0.2),
        )
        result = build_identity_layer(agent)
        assert "measured restraint" in result

    # Boundary-exact tests for _describe_trait thresholds
    def test_trait_boundary_exactly_0_8(self):
        agent = AgentConfig(
            name="A",
            description="Exactly 0.8 assertiveness.",
            personality=PersonalityConfig(assertiveness=0.8),
        )
        assert "extremely assertive" in build_identity_layer(agent)

    def test_trait_boundary_exactly_0_6(self):
        agent = AgentConfig(
            name="A",
            description="Exactly 0.6 assertiveness.",
            personality=PersonalityConfig(assertiveness=0.6),
        )
        assert "quite assertive" in build_identity_layer(agent)

    def test_trait_boundary_exactly_0_4(self):
        agent = AgentConfig(
            name="A",
            description="Exactly 0.4 assertiveness.",
            personality=PersonalityConfig(assertiveness=0.4),
        )
        assert "balance" in build_identity_layer(agent)

    def test_trait_boundary_exactly_0_2(self):
        agent = AgentConfig(
            name="A",
            description="Exactly 0.2 assertiveness.",
            personality=PersonalityConfig(assertiveness=0.2),
        )
        assert "lean toward" in build_identity_layer(agent)

    # Boundary-exact tests for _intensity_line thresholds
    def test_intensity_boundary_exactly_0_7(self):
        agent = AgentConfig(
            name="A",
            description="Exactly 0.7 intensity.",
            position=PositionConfig(intensity=0.7),
        )
        assert "force and passion" in build_identity_layer(agent)

    def test_intensity_boundary_exactly_0_4(self):
        agent = AgentConfig(
            name="A",
            description="Exactly 0.4 intensity.",
            position=PositionConfig(intensity=0.4),
        )
        assert "conviction" in build_identity_layer(agent)


# ---------------------------------------------------------------------------
# TestIdentityJinja2Rendering
# ---------------------------------------------------------------------------


class TestIdentityJinja2Rendering:
    def test_returns_non_empty_string(self, minimal_agent):
        result = build_identity_layer(minimal_agent)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_template_file_exists(self):
        from agentteam.prompts.identity import _TEMPLATES_DIR
        template_path = _TEMPLATES_DIR / "identity.j2"
        assert template_path.exists(), f"Template not found: {template_path}"

    def test_idempotent(self, minimal_agent):
        assert build_identity_layer(minimal_agent) == build_identity_layer(minimal_agent)

    def test_different_agents_produce_different_output(self, minimal_agent, rich_agent):
        assert build_identity_layer(minimal_agent) != build_identity_layer(rich_agent)

    def test_no_raw_jinja_tags_in_output(self, minimal_agent):
        result = build_identity_layer(minimal_agent)
        assert "{{" not in result
        assert "{%" not in result

    def test_rich_agent_output(self, rich_agent):
        result = build_identity_layer(rich_agent)
        assert "Critic" in result
        assert "sharp analytical critic" in result.lower()
