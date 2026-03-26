"""Tests for agentteam.prompts.output — Jinja2-rendered output layer."""

import pytest

from agentteam.prompts.output import build_output_layer
from agentteam.types import (
    AgentConfig,
    AntiSlopConfig,
    Brevity,
    JobType,
    OperatingLevel,
    OutputConfig,
    VoiceConfig,
)


# ---------------------------------------------------------------------------
# TestBuildOutputLayer
# ---------------------------------------------------------------------------


class TestBuildOutputLayer:
    def test_voice_tone_in_output(self, minimal_agent):
        result = build_output_layer(minimal_agent)
        assert "professional" in result

    def test_vocabulary_hints_in_output(self):
        agent = AgentConfig(
            name="Wordsmith",
            description="Has vocabulary hints.",
            voice=VoiceConfig(
                vocabulary_hints=["trade-off", "constraint"],
                anti_patterns=[
                    "I think", "perhaps", "I believe", "in my opinion",
                    "we could", "it seems", "generally", "basically",
                ],
            ),
        )
        result = build_output_layer(agent)
        assert "'trade-off'" in result
        assert "'constraint'" in result
        assert "Phrases that fit your style" in result

    def test_anti_patterns_in_output(self):
        agent = AgentConfig(
            name="Strict",
            description="Has anti-patterns.",
            voice=VoiceConfig(
                anti_patterns=[
                    "I think", "perhaps", "perhaps we should consider", "I believe",
                    "in my opinion", "we could explore", "it seems to me", "generally speaking",
                ],
            ),
        )
        result = build_output_layer(agent)
        assert "NEVER use these phrases:" in result
        assert '"I think"' in result
        assert '"perhaps"' in result

    def test_no_vocabulary_hints_when_empty(self, minimal_agent):
        result = build_output_layer(minimal_agent)
        assert "Phrases that fit your style" not in result

    def test_no_anti_patterns_section_when_empty(self, minimal_agent):
        result = build_output_layer(minimal_agent)
        assert "NEVER use these phrases:" not in result

    def test_brevity_concise(self):
        agent = AgentConfig(
            name="Brief",
            description="Concise agent.",
            voice=VoiceConfig(brevity=Brevity.CONCISE, anti_patterns=[
                "I think", "perhaps", "I believe", "in my opinion",
                "we could", "it seems", "generally", "basically",
            ]),
        )
        result = build_output_layer(agent)
        assert "300 words" in result

    def test_brevity_normal(self, minimal_agent):
        result = build_output_layer(minimal_agent)
        assert "600 words" in result

    def test_brevity_thorough(self):
        agent = AgentConfig(
            name="Thorough",
            description="Thorough agent.",
            voice=VoiceConfig(brevity=Brevity.THOROUGH, anti_patterns=[
                "I think", "perhaps", "I believe", "in my opinion",
                "we could", "it seems", "generally", "basically",
            ]),
        )
        result = build_output_layer(agent)
        assert "300 words" not in result
        assert "600 words" not in result
        assert "comprehensive" in result

    def test_operating_level_requirements(self, minimal_agent):
        result = build_output_layer(minimal_agent)
        assert "WHAT and WHY" in result

    def test_operating_level_design(self):
        agent = AgentConfig(
            name="Designer",
            description="Design-level agent.",
            output=OutputConfig(operating_level=OperatingLevel.DESIGN),
        )
        result = build_output_layer(agent)
        assert "design decisions and tradeoffs" in result

    def test_operating_level_implementation(self):
        agent = AgentConfig(
            name="Implementer",
            description="Implementation-level agent.",
            output=OutputConfig(operating_level=OperatingLevel.IMPLEMENTATION),
        )
        result = build_output_layer(agent)
        assert "concrete and technical" in result

    def test_job_type_propose(self, minimal_agent):
        result = build_output_layer(minimal_agent)
        assert "PROPOSE" in result

    def test_job_type_critique(self):
        agent = AgentConfig(
            name="Critic",
            description="Critique agent.",
            output=OutputConfig(job=JobType.CRITIQUE),
        )
        result = build_output_layer(agent)
        assert "CRITIQUE" in result

    def test_job_type_evaluate(self):
        agent = AgentConfig(
            name="Evaluator",
            description="Evaluate agent.",
            output=OutputConfig(job=JobType.EVALUATE),
        )
        result = build_output_layer(agent)
        assert "EVALUATE" in result

    def test_job_type_simplify(self):
        agent = AgentConfig(
            name="Simplifier",
            description="Simplify agent.",
            output=OutputConfig(job=JobType.SIMPLIFY),
        )
        result = build_output_layer(agent)
        assert "SIMPLIFY" in result

    def test_job_type_ideate(self):
        agent = AgentConfig(
            name="Ideator",
            description="Ideate agent.",
            output=OutputConfig(job=JobType.IDEATE),
        )
        result = build_output_layer(agent)
        assert "IDEATE" in result

    def test_antislop_agreement_tax_included(self, minimal_agent):
        result = build_output_layer(minimal_agent)
        assert "AGREEMENT TAX" in result

    def test_antislop_perspective_enforcement_included(self, minimal_agent):
        result = build_output_layer(minimal_agent)
        assert "PERSPECTIVE LOCK" in result

    def test_antislop_devils_advocate_included(self):
        agent = AgentConfig(
            name="Devil",
            description="Devil's advocate.",
            anti_slop=AntiSlopConfig(devils_advocate_duty=True),
        )
        result = build_output_layer(agent)
        assert "DEVIL'S ADVOCATE DUTY" in result

    def test_antislop_uncomfortable_quota_included(self):
        agent = AgentConfig(
            name="Disruptor",
            description="Quota agent.",
            anti_slop=AntiSlopConfig(uncomfortable_idea_quota=3),
        )
        result = build_output_layer(agent)
        assert "UNCOMFORTABLE IDEA QUOTA" in result

    def test_antislop_uncomfortable_quota_boundary_1(self):
        agent = AgentConfig(
            name="A",
            description="Quota boundary 1.",
            anti_slop=AntiSlopConfig(uncomfortable_idea_quota=1),
        )
        result = build_output_layer(agent)
        assert "Every 9 turns" in result

    def test_antislop_uncomfortable_quota_boundary_5(self):
        agent = AgentConfig(
            name="A",
            description="Quota boundary 5.",
            anti_slop=AntiSlopConfig(uncomfortable_idea_quota=5),
        )
        result = build_output_layer(agent)
        assert "Every 5 turns" in result

    def test_antislop_domain_pivot_included(self):
        agent = AgentConfig(
            name="Pivotter",
            description="Domain pivot agent.",
            anti_slop=AntiSlopConfig(domain_pivot_trigger=True),
        )
        result = build_output_layer(agent)
        assert "DOMAIN PIVOT" in result

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
        result = build_output_layer(agent)
        assert "## Anti-Slop Rules" not in result


# ---------------------------------------------------------------------------
# TestOutputJinja2Rendering
# ---------------------------------------------------------------------------


class TestOutputJinja2Rendering:
    def test_returns_non_empty_string(self, minimal_agent):
        result = build_output_layer(minimal_agent)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_template_file_exists(self):
        from agentteam.prompts.output import _TEMPLATES_DIR

        template_path = _TEMPLATES_DIR / "output.j2"
        assert template_path.exists(), f"Template not found: {template_path}"

    def test_idempotent(self, minimal_agent):
        assert build_output_layer(minimal_agent) == build_output_layer(minimal_agent)

    def test_different_agents_produce_different_output(self, minimal_agent, rich_agent):
        assert build_output_layer(minimal_agent) != build_output_layer(rich_agent)

    def test_no_raw_jinja_tags_in_output(self, minimal_agent):
        result = build_output_layer(minimal_agent)
        assert "{{" not in result
        assert "{%" not in result

    def test_voice_section_header_present(self, minimal_agent):
        result = build_output_layer(minimal_agent)
        assert "## Your Voice" in result

    def test_output_section_header_present(self, minimal_agent):
        result = build_output_layer(minimal_agent)
        assert "## Your Output" in result
