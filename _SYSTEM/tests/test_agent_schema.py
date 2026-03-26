"""Tests for AgentConfig Pydantic schema validation."""

import pytest
from pydantic import ValidationError

from agentteam.types import (
    AgentConfig,
    PersonalityConfig,
    PositionConfig,
    TechniqueConfig,
)

_VALID_DRIVES = ["drive one", "drive two", "drive three"]
_VALID_PUSHBACK = ["pushback one", "pushback two", "pushback three"]
_VALID_BEHAVIORS = ["behavior one", "behavior two", "behavior three", "behavior four", "behavior five"]


# ---------------------------------------------------------------------------
# TestPersonalityConfig
# ---------------------------------------------------------------------------

class TestPersonalityConfig:
    def test_defaults_are_valid(self):
        p = PersonalityConfig()
        assert 0.0 <= p.assertiveness <= 1.0

    def test_assertiveness_out_of_range(self):
        with pytest.raises(ValidationError):
            PersonalityConfig(assertiveness=1.5)

    def test_creativity_temp_negative(self):
        with pytest.raises(ValidationError):
            PersonalityConfig(creativity_temp=-0.1)

    def test_all_eight_dimensions_accessible(self):
        p = PersonalityConfig()
        for attr in (
            "assertiveness", "creativity_temp", "risk_tolerance", "attention_span",
            "stubbornness", "idea_receptivity", "bluntness", "patience",
        ):
            val = getattr(p, attr)
            assert isinstance(val, float), f"{attr} should be a float"

    def test_boundary_values_valid(self):
        p = PersonalityConfig(assertiveness=0.0, creativity_temp=1.0)
        assert p.assertiveness == 0.0
        assert p.creativity_temp == 1.0

    def test_stubbornness_above_one(self):
        with pytest.raises(ValidationError):
            PersonalityConfig(stubbornness=1.001)


# ---------------------------------------------------------------------------
# TestPositionConfig
# ---------------------------------------------------------------------------

class TestPositionConfig:
    def test_drives_too_few(self):
        with pytest.raises(ValidationError):
            PositionConfig(drives=["a", "b"])

    def test_drives_too_many(self):
        with pytest.raises(ValidationError):
            PositionConfig(drives=["a", "b", "c", "d", "e", "f"])

    def test_drives_valid_three(self):
        p = PositionConfig(drives=_VALID_DRIVES)
        assert len(p.drives) == 3

    def test_drives_valid_five(self):
        p = PositionConfig(drives=["a", "b", "c", "d", "e"])
        assert len(p.drives) == 5

    def test_pushback_on_too_few(self):
        with pytest.raises(ValidationError):
            PositionConfig(pushback_on=["a", "b"])

    def test_pushback_on_valid(self):
        p = PositionConfig(pushback_on=["a", "b", "c", "d"])
        assert len(p.pushback_on) == 4

    def test_default_empty_drives_valid(self):
        # Empty default (not explicitly set) must NOT fail min_length
        p = PositionConfig()
        assert p.drives == []

    def test_default_empty_pushback_valid(self):
        p = PositionConfig()
        assert p.pushback_on == []

    def test_intensity_out_of_range(self):
        with pytest.raises(ValidationError):
            PositionConfig(intensity=1.5)

    def test_drives_exactly_four(self):
        p = PositionConfig(drives=["a", "b", "c", "d"])
        assert len(p.drives) == 4


# ---------------------------------------------------------------------------
# TestTechniqueConfig
# ---------------------------------------------------------------------------

class TestTechniqueConfig:
    def test_behaviors_too_few(self):
        with pytest.raises(ValidationError):
            TechniqueConfig(behaviors=["a", "b", "c"])

    def test_behaviors_too_many(self):
        with pytest.raises(ValidationError):
            TechniqueConfig(behaviors=["a", "b", "c", "d", "e", "f", "g", "h", "i"])

    def test_behaviors_valid_five(self):
        t = TechniqueConfig(behaviors=_VALID_BEHAVIORS)
        assert len(t.behaviors) == 5

    def test_behaviors_valid_eight(self):
        behaviors = [f"behavior {i}" for i in range(8)]
        t = TechniqueConfig(behaviors=behaviors)
        assert len(t.behaviors) == 8

    def test_default_empty_behaviors_valid(self):
        # Empty default must NOT fail min_length
        t = TechniqueConfig()
        assert t.behaviors == []


# ---------------------------------------------------------------------------
# TestAgentConfig
# ---------------------------------------------------------------------------

class TestAgentConfig:
    def test_minimal_valid_agent(self):
        a = AgentConfig(name="Test", description="A test agent.")
        assert a.name == "Test"
        assert a.description == "A test agent."
        assert isinstance(a.personality, PersonalityConfig)
        assert isinstance(a.position, PositionConfig)
        assert isinstance(a.technique, TechniqueConfig)

    def test_full_valid_agent(self):
        a = AgentConfig(
            name="Full Agent",
            description="A fully specified agent.",
            position=PositionConfig(
                role="tester",
                drives=_VALID_DRIVES,
                pushback_on=_VALID_PUSHBACK,
                intensity=0.7,
            ),
            technique=TechniqueConfig(
                primary="testing",
                style_description="Tests things.",
                behaviors=_VALID_BEHAVIORS,
            ),
        )
        assert len(a.position.drives) == 3
        assert len(a.technique.behaviors) == 5

    def test_missing_name_raises(self):
        with pytest.raises(ValidationError):
            AgentConfig(description="x")

    def test_missing_description_raises(self):
        with pytest.raises(ValidationError):
            AgentConfig(name="x")

    def test_invalid_position_propagates(self):
        with pytest.raises(ValidationError) as exc_info:
            AgentConfig(
                name="Agent",
                description="desc",
                position=PositionConfig(drives=["only_one"]),
            )
        assert "drives" in str(exc_info.value).lower()
