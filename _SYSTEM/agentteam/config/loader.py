"""Class-based config and template loader with injectable directories.

Usage — create a loader for a specific config dir:
    from agentteam.config.loader import ConfigLoader
    from pathlib import Path

    loader = ConfigLoader(
        config_dir=Path("my_project/config"),
        template_dir=Path("my_project/templates"),
    )
    timeout = loader.defaults()["timeouts"]["discussion"]
    name = loader.display_name("cognitive_architect")
    html = loader.load_html_template("live_conversation.html")

Default loader (reads _SYSTEM/config/ and _SYSTEM/templates/):
    from agentteam.config.loader import defaults, display_name, render_prompt
"""

from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

# _SYSTEM/ is 3 levels up from this file: agentteam/config/loader.py
_SYSTEM_DIR = Path(__file__).resolve().parent.parent.parent


class ConfigLoader:
    """Loads YAML config and Jinja2 templates from a configurable directory pair."""

    def __init__(self, config_dir: Path, template_dir: Path):
        self._config_dir = config_dir
        self._template_dir = template_dir
        self._cache: dict[str, Any] = {}
        self._jinja_env = None

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _load_yaml(self, filename: str) -> dict:
        key = f"yaml:{filename}"
        if key not in self._cache:
            self._cache[key] = yaml.safe_load(
                (self._config_dir / filename).read_text(encoding="utf-8")
            )
        return self._cache[key]

    def _get_jinja_env(self):
        if self._jinja_env is None:
            from jinja2 import Environment, FileSystemLoader
            self._jinja_env = Environment(
                loader=FileSystemLoader(str(self._template_dir)),
                trim_blocks=True,
                lstrip_blocks=True,
                keep_trailing_newline=True,
            )
        return self._jinja_env

    # ------------------------------------------------------------------
    # Config loaders
    # ------------------------------------------------------------------

    def defaults(self) -> dict:
        """Load defaults.yaml — timeouts, thresholds, magic numbers."""
        return self._load_yaml("defaults.yaml")

    def agent_display_config(self) -> dict:
        """Load agent_display.yaml — display names and colors."""
        return self._load_yaml("agent_display.yaml")

    def experiment_modes(self) -> dict:
        """Load experiment_modes.yaml — discussion mode configurations."""
        raw = self._load_yaml("experiment_modes.yaml")
        return raw["modes"]

    def role_overlays(self) -> dict:
        """Load role_overlays.yaml — per-agent role overlay instructions."""
        return self._load_yaml("role_overlays.yaml")

    # ------------------------------------------------------------------
    # Convenience accessors
    # ------------------------------------------------------------------

    def display_name(self, agent_key: str) -> str:
        return self.agent_display_config()["display_names"].get(agent_key, agent_key)

    def display_names(self) -> dict[str, str]:
        return self.agent_display_config()["display_names"]

    def agent_color(self, agent_key: str) -> str:
        return self.agent_display_config()["colors_hex"].get(agent_key, "#94a3b8")

    def agent_colors(self) -> dict[str, str]:
        return self.agent_display_config()["colors_hex"]

    def agent_colors_ansi(self) -> list[str]:
        return self.agent_display_config()["colors_ansi_cycle"]

    def overlay_instruction(self, role_key: str) -> str:
        overlays = self.role_overlays()["overlays"]
        if role_key in overlays:
            return overlays[role_key]["instruction"]
        return ""

    def counter_propose_instruction(self) -> str:
        return self.role_overlays()["counter_propose_instruction"]

    def timeout(self, name: str) -> int:
        return self.defaults()["timeouts"].get(name, self.defaults()["timeouts"]["default"])

    def truncation(self, name: str) -> int:
        return self.defaults()["truncation"].get(name, 6000)

    # ------------------------------------------------------------------
    # Template rendering
    # ------------------------------------------------------------------

    def render_prompt(self, template_path: str, **kwargs) -> str:
        """Render a Jinja2 template. template_path is relative to template_dir."""
        env = self._get_jinja_env()
        return env.get_template(template_path).render(**kwargs)

    def load_prompt_raw(self, template_path: str) -> str:
        """Load a template as raw text (no rendering)."""
        return (self._template_dir / template_path).read_text(encoding="utf-8")

    def load_spec_template(self, name: str) -> dict:
        """Load a spec template YAML."""
        path = self._config_dir / "spec_templates" / f"{name}.yaml"
        return yaml.safe_load(path.read_text(encoding="utf-8"))

    def load_html_template(self, name: str) -> str:
        """Load an HTML template file."""
        return (self._template_dir / "html" / name).read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Default instance — reads _SYSTEM/config/ and _SYSTEM/templates/
# ---------------------------------------------------------------------------

_default_loader = ConfigLoader(
    config_dir=_SYSTEM_DIR / "config",
    template_dir=_SYSTEM_DIR / "templates",
)


# Module-level convenience functions delegating to the default loader
def defaults() -> dict:
    return _default_loader.defaults()


def agent_display_config() -> dict:
    return _default_loader.agent_display_config()


def experiment_modes() -> dict:
    return _default_loader.experiment_modes()


def role_overlays() -> dict:
    return _default_loader.role_overlays()


def display_name(agent_key: str) -> str:
    return _default_loader.display_name(agent_key)


def display_names() -> dict[str, str]:
    return _default_loader.display_names()


def agent_color(agent_key: str) -> str:
    return _default_loader.agent_color(agent_key)


def agent_colors() -> dict[str, str]:
    return _default_loader.agent_colors()


def agent_colors_ansi() -> list[str]:
    return _default_loader.agent_colors_ansi()


def overlay_instruction(role_key: str) -> str:
    return _default_loader.overlay_instruction(role_key)


def counter_propose_instruction() -> str:
    return _default_loader.counter_propose_instruction()


def timeout(name: str) -> int:
    return _default_loader.timeout(name)


def truncation(name: str) -> int:
    return _default_loader.truncation(name)


def render_prompt(template_path: str, **kwargs) -> str:
    return _default_loader.render_prompt(template_path, **kwargs)


def load_prompt_raw(template_path: str) -> str:
    return _default_loader.load_prompt_raw(template_path)


def load_spec_template(name: str) -> dict:
    return _default_loader.load_spec_template(name)


def load_html_template(name: str) -> str:
    return _default_loader.load_html_template(name)
