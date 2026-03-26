"""Config and template loader — delegates to agentteam.config.loader.ConfigLoader.

Creates a loader instance pointed at this project's config/ and templates/ dirs.
All module-level names are bound methods of that instance, so callers see no API change.

Usage:
    from config_loader import defaults, display_name, agent_color, render_prompt
    from config_loader import experiment_modes, role_overlays, load_spec_template

    timeout = defaults()["timeouts"]["discussion"]
    name = display_name("cognitive_architect")
    color = agent_color("cognitive_architect")
    prompt = render_prompt("prompts/synthesis.md.j2", question_number=1, topic_tag="turn anatomy")
    modes = experiment_modes()
    spec = load_spec_template("product_spec")
    html = load_html_template("live_conversation.html")
"""

from agentteam.config.loader import ConfigLoader
from pathlib import Path

_ENGINE_DIR = Path(__file__).resolve().parent
_loader = ConfigLoader(
    config_dir=_ENGINE_DIR / "config",
    template_dir=_ENGINE_DIR / "templates",
)

# Bind all public methods as module-level names — callers see no API change.
defaults = _loader.defaults
agent_display_config = _loader.agent_display_config
experiment_modes = _loader.experiment_modes
role_overlays = _loader.role_overlays
display_name = _loader.display_name
display_names = _loader.display_names
agent_color = _loader.agent_color
agent_colors = _loader.agent_colors
agent_colors_ansi = _loader.agent_colors_ansi
overlay_instruction = _loader.overlay_instruction
counter_propose_instruction = _loader.counter_propose_instruction
timeout = _loader.timeout
truncation = _loader.truncation
render_prompt = _loader.render_prompt
load_prompt_raw = _loader.load_prompt_raw
load_spec_template = _loader.load_spec_template
load_html_template = _loader.load_html_template
