"""Tests for AntiSlopConfig and VoiceConfig Pydantic schema validation."""

import pytest
from pydantic import ValidationError

from agentteam.types import (
    AgentConfig,
    AntiSlopConfig,
    Brevity,
    VoiceConfig,
)

_VALID_ANTI_PATTERNS = [f"slop phrase {i}" for i in range(8)]
_VALID_ANTI_PATTERNS_12 = [f"slop phrase {i}" for i in range(12)]


# ---------------------------------------------------------------------------
# TestAntiSlopConfig
# ---------------------------------------------------------------------------

class TestAntiSlopConfig:
    def test_defaults_match_spec(self):
        a = AntiSlopConfig()
        assert a.agreement_tax is True
        assert a.perspective_enforcement is True
        assert a.devils_advocate_duty is False
        assert a.uncomfortable_idea_quota == 0
        assert a.domain_pivot_trigger is False

    def test_agreement_tax_can_be_disabled(self):
        a = AntiSlopConfig(agreement_tax=False)
        assert a.agreement_tax is False

    def test_devils_advocate_can_be_enabled(self):
        a = AntiSlopConfig(devils_advocate_duty=True)
        assert a.devils_advocate_duty is True

    def test_uncomfortable_idea_quota_min_boundary(self):
        a = AntiSlopConfig(uncomfortable_idea_quota=0)
        assert a.uncomfortable_idea_quota == 0

    def test_uncomfortable_idea_quota_max_boundary(self):
        a = AntiSlopConfig(uncomfortable_idea_quota=5)
        assert a.uncomfortable_idea_quota == 5

    def test_uncomfortable_idea_quota_above_max_raises(self):
        with pytest.raises(ValidationError):
            AntiSlopConfig(uncomfortable_idea_quota=6)

    def test_uncomfortable_idea_quota_negative_raises(self):
        with pytest.raises(ValidationError):
            AntiSlopConfig(uncomfortable_idea_quota=-1)

    def test_full_construction_all_fields(self):
        a = AntiSlopConfig(
            agreement_tax=True,
            perspective_enforcement=False,
            devils_advocate_duty=True,
            uncomfortable_idea_quota=3,
            domain_pivot_trigger=True,
        )
        assert a.perspective_enforcement is False
        assert a.uncomfortable_idea_quota == 3
        assert a.domain_pivot_trigger is True


# ---------------------------------------------------------------------------
# TestVoiceConfig
# ---------------------------------------------------------------------------

class TestVoiceConfig:
    def test_anti_patterns_too_few(self):
        with pytest.raises(ValidationError):
            VoiceConfig(anti_patterns=["a", "b", "c", "d", "e", "f", "g"])  # 7

    def test_anti_patterns_too_many(self):
        phrases = [f"phrase {i}" for i in range(13)]
        with pytest.raises(ValidationError):
            VoiceConfig(anti_patterns=phrases)  # 13

    def test_anti_patterns_valid_eight(self):
        v = VoiceConfig(anti_patterns=_VALID_ANTI_PATTERNS)
        assert len(v.anti_patterns) == 8

    def test_anti_patterns_valid_twelve(self):
        v = VoiceConfig(anti_patterns=_VALID_ANTI_PATTERNS_12)
        assert len(v.anti_patterns) == 12

    def test_anti_patterns_boundary_nine(self):
        phrases = [f"p{i}" for i in range(9)]
        v = VoiceConfig(anti_patterns=phrases)
        assert len(v.anti_patterns) == 9

    def test_default_empty_anti_patterns_valid(self):
        # Empty default via default_factory must NOT fail min_length (Pydantic v2 validate_default=False)
        v = VoiceConfig()
        assert v.anti_patterns == []

    def test_explicit_empty_list_raises(self):
        # Explicitly passing [] is validated (unlike the default); must fail min_length=8
        with pytest.raises(ValidationError):
            VoiceConfig(anti_patterns=[])

    def test_brevity_enum_default(self):
        v = VoiceConfig()
        assert v.brevity == Brevity.NORMAL

    def test_brevity_concise(self):
        v = VoiceConfig(brevity=Brevity.CONCISE)
        assert v.brevity == Brevity.CONCISE

    def test_tone_and_vocabulary_hints_accessible_alongside_anti_patterns(self):
        v = VoiceConfig(
            tone="blunt",
            brevity=Brevity.CONCISE,
            vocabulary_hints=["trade-off", "constraint"],
            anti_patterns=_VALID_ANTI_PATTERNS,
        )
        assert v.tone == "blunt"
        assert "trade-off" in v.vocabulary_hints
        assert len(v.anti_patterns) == 8


# ---------------------------------------------------------------------------
# TestVoiceAndAntiSlopTogether
# ---------------------------------------------------------------------------

class TestVoiceAndAntiSlopTogether:
    def test_full_agent_with_voice_and_antislop(self):
        a = AgentConfig(
            name="Full Agent",
            description="Agent with voice and anti-slop configured.",
            voice=VoiceConfig(
                tone="blunt",
                brevity=Brevity.CONCISE,
                vocabulary_hints=["trade-off"],
                anti_patterns=_VALID_ANTI_PATTERNS,
            ),
            anti_slop=AntiSlopConfig(
                agreement_tax=True,
                devils_advocate_duty=True,
                uncomfortable_idea_quota=2,
            ),
        )
        assert len(a.voice.anti_patterns) == 8
        assert a.anti_slop.uncomfortable_idea_quota == 2
        assert a.anti_slop.agreement_tax is True

    def test_invalid_quota_in_agent_raises_with_field_name(self):
        with pytest.raises(ValidationError) as exc_info:
            AgentConfig(
                name="Agent",
                description="desc",
                anti_slop=AntiSlopConfig(uncomfortable_idea_quota=99),
            )
        assert "uncomfortable_idea_quota" in str(exc_info.value).lower()
