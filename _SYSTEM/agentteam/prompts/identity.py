"""Identity layer prompt rendering using Jinja2 templates."""

from pathlib import Path

from agentteam.types import AgentConfig, PersonalityConfig

_TEMPLATES_DIR = Path(__file__).parent / "templates"
_jinja_env = None


def _get_jinja_env():
    global _jinja_env
    if _jinja_env is None:
        from jinja2 import Environment, FileSystemLoader
        _jinja_env = Environment(
            loader=FileSystemLoader(str(_TEMPLATES_DIR)),
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=True,
        )
    return _jinja_env


def _describe_trait(value: float, low_desc: str, high_desc: str) -> str:
    if value >= 0.8:
        return f"You are extremely {high_desc}."
    elif value >= 0.6:
        return f"You are quite {high_desc}."
    elif value >= 0.4:
        return f"You balance {low_desc} and {high_desc} tendencies."
    elif value >= 0.2:
        return f"You lean toward being {low_desc}."
    else:
        return f"You are strongly {low_desc}."


def _personality_lines(p: PersonalityConfig) -> list[str]:
    lines = [
        _describe_trait(
            p.assertiveness,
            "reserved and diplomatic",
            "assertive -- you fight hard for your ideas and don't back down easily",
        ),
        _describe_trait(
            p.creativity_temp,
            "conventional and proven-path",
            "wildly creative -- you reach for novel, unexpected ideas",
        ),
        _describe_trait(
            p.risk_tolerance,
            "risk-averse and safety-focused",
            "risk-tolerant -- you embrace bold bets and untested approaches",
        ),
        f"Your cognitive style is {p.cognitive_style.value}"
        " -- this shapes how you approach every problem.",
        f"Your emotional baseline is {p.emotional_baseline.value}"
        " -- this colors your reactions and framing.",
        _describe_trait(
            p.attention_span,
            "a topic-hopper who jumps between ideas freely",
            "deeply focused -- you drill into one thread exhaustively",
        ),
        _describe_trait(
            p.stubbornness,
            "flexible and quick to update your views",
            "stubborn -- you hold your ground and require strong evidence to change your mind",
        ),
        _describe_trait(
            p.idea_receptivity,
            "an agenda driver who stays focused on your own ideas",
            "deeply engaged with others' ideas"
            " -- you build on what others say and genuinely absorb their perspective",
        ),
        _describe_trait(
            p.bluntness,
            "diplomatic and tactful -- you soften hard truths",
            "brutally direct -- you say exactly what you think with zero sugar-coating",
        ),
        _describe_trait(
            p.patience,
            "impatient -- you cut off tangents and push to move on",
            "patient -- you let discussions breathe and don't rush to conclusions",
        ),
    ]
    if p.domain_affinities:
        lines.append(f"You naturally draw from these domains: {', '.join(p.domain_affinities)}.")
    return lines


def _intensity_line(intensity: float) -> str:
    if intensity >= 0.7:
        return "You express your views with force and passion -- you're not here to play nice."
    elif intensity >= 0.4:
        return "You express your views with conviction but remain open to dialogue."
    else:
        return "You express your views with measured restraint."


def build_identity_layer(agent: AgentConfig) -> str:
    """Render the identity layer for agent system prompt using Jinja2 templates."""
    pos = agent.position
    tech = agent.technique

    context = {
        "name": agent.name,
        "description": agent.description.strip(),
        "role": pos.role.title(),
        "drives": pos.drives,
        "pushback_on": pos.pushback_on,
        "intensity_line": _intensity_line(pos.intensity),
        "personality_text": "\n".join(_personality_lines(agent.personality)),
        "technique_name": tech.primary.replace("_", " ").title(),
        "style_description": tech.style_description.strip() if tech.style_description else "",
        "behaviors": tech.behaviors,
    }

    env = _get_jinja_env()
    return env.get_template("identity.j2").render(**context).rstrip()
