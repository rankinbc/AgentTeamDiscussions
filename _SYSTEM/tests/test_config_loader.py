"""Tests for agentteam.config.loader.ConfigLoader."""
import pytest
from pathlib import Path

from agentteam.config.loader import ConfigLoader


@pytest.fixture
def loader(minimal_config_dir, minimal_template_dir) -> ConfigLoader:
    """A ConfigLoader pointed at the minimal test config/template dirs."""
    return ConfigLoader(config_dir=minimal_config_dir, template_dir=minimal_template_dir)


# ---------------------------------------------------------------------------
# defaults
# ---------------------------------------------------------------------------

class TestDefaults:
    def test_returns_dict(self, loader):
        assert isinstance(loader.defaults(), dict)

    def test_contains_timeouts(self, loader):
        assert "timeouts" in loader.defaults()

    def test_result_is_cached(self, loader):
        assert loader.defaults() is loader.defaults()


# ---------------------------------------------------------------------------
# timeout / truncation accessors
# ---------------------------------------------------------------------------

class TestTimeoutAccessor:
    def test_known_timeout_name(self, loader):
        assert loader.timeout("discussion") == 120

    def test_unknown_name_falls_back_to_default(self, loader):
        assert loader.timeout("nonexistent_key") == 60

    def test_truncation_known_key(self, loader):
        assert loader.truncation("short") == 2000

    def test_truncation_unknown_falls_back(self, loader):
        assert loader.truncation("unknown_key") == 6000


# ---------------------------------------------------------------------------
# display name / color accessors
# ---------------------------------------------------------------------------

class TestDisplayNames:
    def test_known_agent_returns_display_name(self, loader):
        assert loader.display_name("alpha") == "Agent Alpha"

    def test_unknown_agent_returns_key(self, loader):
        assert loader.display_name("unknown_agent") == "unknown_agent"

    def test_display_names_returns_full_dict(self, loader):
        names = loader.display_names()
        assert names["alpha"] == "Agent Alpha"
        assert names["beta"] == "Agent Beta"

    def test_agent_color_known(self, loader):
        assert loader.agent_color("alpha") == "#ff0000"

    def test_agent_color_unknown_returns_fallback(self, loader):
        assert loader.agent_color("unknown") == "#94a3b8"

    def test_agent_colors_returns_dict(self, loader):
        colors = loader.agent_colors()
        assert isinstance(colors, dict)

    def test_agent_colors_ansi_returns_list(self, loader):
        assert isinstance(loader.agent_colors_ansi(), list)


# ---------------------------------------------------------------------------
# experiment modes / role overlays
# ---------------------------------------------------------------------------

class TestExperimentModes:
    def test_returns_dict(self, loader):
        assert isinstance(loader.experiment_modes(), dict)

    def test_default_mode_present(self, loader):
        assert "default" in loader.experiment_modes()


class TestRoleOverlays:
    def test_role_overlays_returns_dict(self, loader):
        assert isinstance(loader.role_overlays(), dict)

    def test_overlay_instruction_known_role(self, loader):
        assert "Propose" in loader.overlay_instruction("proposer")

    def test_overlay_instruction_unknown_role_returns_empty(self, loader):
        assert loader.overlay_instruction("nonexistent_role") == ""

    def test_counter_propose_instruction_nonempty(self, loader):
        assert loader.counter_propose_instruction() != ""


# ---------------------------------------------------------------------------
# template rendering
# ---------------------------------------------------------------------------

class TestTemplateRendering:
    def test_render_prompt_substitutes_variable(self, loader):
        result = loader.render_prompt("test_prompt.md.j2", topic="round anatomy")
        assert result == "Topic: round anatomy"

    def test_load_prompt_raw_returns_unrendered_template(self, loader):
        raw = loader.load_prompt_raw("test_prompt.md.j2")
        assert "{{ topic }}" in raw

    def test_load_html_template(self, loader):
        html = loader.load_html_template("test.html")
        assert "<h1>" in html


# ---------------------------------------------------------------------------
# Two independent loaders do not share cache
# ---------------------------------------------------------------------------

class TestCacheIsolation:
    def test_two_loaders_have_independent_caches(self, minimal_config_dir, minimal_template_dir):
        loader_a = ConfigLoader(config_dir=minimal_config_dir, template_dir=minimal_template_dir)
        loader_b = ConfigLoader(config_dir=minimal_config_dir, template_dir=minimal_template_dir)
        # Mutating one cache should not affect the other
        loader_a._cache["yaml:custom"] = "value_a"
        assert "yaml:custom" not in loader_b._cache
