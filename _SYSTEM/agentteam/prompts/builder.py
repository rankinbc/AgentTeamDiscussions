"""System prompt assembly from agent config."""

from agentteam.types import AgentConfig

from .identity import build_identity_layer
from .output import build_output_layer


def build_system_prompt(agent: AgentConfig) -> str:
    """Assemble the full system prompt from agent config."""
    sections = []
    sections.append(build_identity_layer(agent))
    sections.append(build_output_layer(agent))

    pos = agent.position
    sections.append(
        f"## Remember\n\nYou are {agent.name}. Stay in character. Your role is {pos.role}. "
        f"Your style is {agent.personality.cognitive_style.value}"
        f" and {agent.personality.emotional_baseline.value}. "
        f"Add substance or stay silent."
    )
    return "\n\n".join(sections)


def build_perspective_reminder(agent: AgentConfig) -> str:
    """Short per-turn identity reinforcement to fight context drift."""
    return (
        f"[You are {agent.name} -- {agent.position.role}. "
        f"Style: {agent.personality.cognitive_style.value},"
        f" {agent.personality.emotional_baseline.value}. "
        f"Technique: {agent.technique.primary.replace('_', ' ')}."
        f" Stay in character. Add substance or stay silent.]"
    )


def build_context_lens(agent: AgentConfig) -> str:
    """Agent-specific framing layer directing attention to relevant context."""
    lines = []
    if agent.position.drives:
        lines.append("When reading the context below, focus on:")
        lines.extend(f"  - {d}" for d in agent.position.drives[:3])
    if agent.position.pushback_on:
        lines.append("Flag anything that looks like:")
        lines.extend(f"  - {p}" for p in agent.position.pushback_on[:3])
    if agent.personality.domain_affinities:
        lines.append(
            f"Apply your expertise in: {', '.join(agent.personality.domain_affinities[:4])}"
        )
    if agent.personality.idea_receptivity >= 0.7:
        lines.append("Pay close attention to what other agents proposed. Build on their best ideas.")
    elif agent.personality.idea_receptivity <= 0.3:
        lines.append(
            "Stay focused on your own perspective. Don't get pulled into other agents' framing."
        )
    if agent.personality.patience <= 0.3:
        lines.append("If the discussion is covering old ground, call it out and push forward.")
    if not lines:
        return ""
    return "=== Your Focus for This Context ===\n" + "\n".join(lines) + "\n=== End Focus ===\n"


def filter_prior_rounds(prior_rounds: str, agent: AgentConfig) -> str:
    """Optionally compress prior rounds based on agent receptivity and patience."""
    if not prior_rounds:
        return prior_rounds
    r = agent.personality.idea_receptivity
    p = agent.personality.patience
    if r >= 0.5 and p >= 0.5:
        return prior_rounds
    if p < 0.3 and len(prior_rounds) > 3000:
        trimmed = prior_rounds[-2500:]
        idx = trimmed.find("\n[")
        if idx > 0:
            trimmed = trimmed[idx:]
        return f"[Earlier discussion truncated -- focusing on recent exchanges]\n{trimmed}"
    return prior_rounds
