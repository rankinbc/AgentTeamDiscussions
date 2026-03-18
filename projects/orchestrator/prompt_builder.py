"""Assembles system prompts from agent YAML config.

Identity layer of the turn: persona, bias, position, personality,
technique, voice, output rules, anti-slop. No project-specific context
here -- that belongs in the Situation layer, injected per-call.
"""

from .models import AgentConfig, AntiSlopConfig, PersonalityConfig


def _describe_trait(name: str, value: float, low_desc: str, high_desc: str) -> str:
    """Convert a 0-1 trait value to natural language."""
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


def _build_personality_section(p: PersonalityConfig) -> str:
    """Translate personality numbers to behavioral descriptions."""
    lines = [
        _describe_trait("assertiveness", p.assertiveness,
                        "reserved and diplomatic", "assertive -- you fight hard for your ideas and don't back down easily"),
        _describe_trait("creativity", p.creativity_temp,
                        "conventional and proven-path", "wildly creative -- you reach for novel, unexpected ideas"),
        _describe_trait("risk", p.risk_tolerance,
                        "risk-averse and safety-focused", "risk-tolerant -- you embrace bold bets and untested approaches"),
        f"Your cognitive style is {p.cognitive_style.value} -- this shapes how you approach every problem.",
        f"Your emotional baseline is {p.emotional_baseline.value} -- this colors your reactions and framing.",
        _describe_trait("focus", p.attention_span,
                        "a topic-hopper who jumps between ideas freely", "deeply focused -- you drill into one thread exhaustively"),
        _describe_trait("stubbornness", p.stubbornness,
                        "flexible and quick to update your views", "stubborn -- you hold your ground and require strong evidence to change your mind"),
    ]
    if p.domain_affinities:
        lines.append(f"You naturally draw from these domains: {', '.join(p.domain_affinities)}.")
    return "\n".join(lines)


def _build_antislop_section(a: AntiSlopConfig) -> str:
    """Build anti-slop rules."""
    rules = []
    if a.agreement_tax:
        rules.append(
            "AGREEMENT TAX: If you agree with something, you MUST add substantive new "
            "information, a different angle, or a concrete next step. Pure agreement "
            "('great idea!', 'I love that') is FORBIDDEN. Agreement without substance "
            "is noise."
        )
    if a.perspective_enforcement:
        rules.append(
            "PERSPECTIVE LOCK: Stay in your character's perspective even when pressured "
            "to agree. If your character would push back, push back. Do not soften your "
            "position to be polite. Authentic disagreement is more valuable than false harmony."
        )
    if a.devils_advocate_duty:
        rules.append(
            "DEVIL'S ADVOCATE DUTY: Actively seek the strongest argument against the "
            "current direction. If everyone seems to agree, it's YOUR job to find the "
            "hole in the logic."
        )
    if a.uncomfortable_idea_quota > 0:
        rules.append(
            f"UNCOMFORTABLE IDEA QUOTA: Every {max(5, 10 - a.uncomfortable_idea_quota)} turns, "
            f"introduce at least one idea that challenges comfort zones -- something "
            f"the group might resist but needs to consider."
        )
    if a.domain_pivot_trigger:
        rules.append(
            "DOMAIN PIVOT: When the discussion gets stuck or circular, inject a "
            "perspective from a completely different field to break the pattern."
        )
    return "\n\n".join(rules)


def build_system_prompt(agent: AgentConfig) -> str:
    """Assemble the full system prompt from agent config.

    This is the Identity layer of the turn context model:
    who the agent is, how they think, what they do.
    """
    sections = []

    # Identity
    sections.append(f"# You are {agent.name}\n\n{agent.description.strip()}")

    # Position
    pos = agent.position
    pos_lines = [f"## Your Role: {pos.role.title()}"]
    if pos.drives:
        pos_lines.append("\nWhat drives you:")
        for d in pos.drives:
            pos_lines.append(f"- {d}")
    if pos.pushback_on:
        pos_lines.append("\nYou actively push back on:")
        for p in pos.pushback_on:
            pos_lines.append(f"- {p}")
    intensity_desc = {
        (0.0, 0.4): "You express your views with measured restraint.",
        (0.4, 0.7): "You express your views with conviction but remain open to dialogue.",
        (0.7, 1.01): "You express your views with force and passion -- you're not here to play nice.",
    }
    for (lo, hi), desc in intensity_desc.items():
        if lo <= pos.intensity < hi:
            pos_lines.append(f"\n{desc}")
            break
    sections.append("\n".join(pos_lines))

    # Personality
    sections.append(f"## Your Personality\n\n{_build_personality_section(agent.personality)}")

    # Technique
    tech = agent.technique
    tech_lines = [f"## Your Thinking Technique: {tech.primary.replace('_', ' ').title()}"]
    if tech.style_description:
        tech_lines.append(f"\n{tech.style_description.strip()}")
    if tech.behaviors:
        tech_lines.append("\nBehavioral rules:")
        for b in tech.behaviors:
            tech_lines.append(f"- {b}")
    sections.append("\n".join(tech_lines))

    # Voice
    voice = agent.voice
    voice_lines = [f"## Your Voice\n\nTone: {voice.tone}"]
    if voice.vocabulary_hints:
        voice_lines.append(f"\nPhrases that fit your style: {', '.join(repr(v) for v in voice.vocabulary_hints)}")
    if voice.anti_patterns:
        voice_lines.append("\nNEVER use these phrases (they are generic slop):")
        for ap in voice.anti_patterns:
            voice_lines.append(f'- "{ap}"')
    sections.append("\n".join(voice_lines))

    # Output rules
    out = agent.output
    out_lines = ["## Your Output"]

    level_desc = {
        "requirements": (
            "Focus on WHAT and WHY, not HOW. Describe behavior, rules, and decisions. "
            "Do NOT write code, schemas, class definitions, or pseudocode unless explicitly asked."
        ),
        "design": (
            "Focus on design decisions and tradeoffs. You may reference technical concepts "
            "but keep the emphasis on choices and rationale, not implementation detail."
        ),
        "implementation": (
            "Be concrete and technical. Include schemas, code patterns, and specific "
            "implementation guidance where it clarifies the design."
        ),
    }
    out_lines.append(f"\n{level_desc.get(out.operating_level, level_desc['requirements'])}")

    job_desc = {
        "propose": "Your job is to PROPOSE -- put forward designs, ideas, and solutions.",
        "critique": (
            "Your job is to CRITIQUE -- find problems, weak assumptions, and failure modes "
            "in what others propose. Do not propose full alternative designs. Identify what's "
            "wrong and why, then stop."
        ),
        "evaluate": (
            "Your job is to EVALUATE -- assess proposals through the lens of user value, "
            "feasibility, and real-world impact. Say what works, what doesn't, and what the "
            "user would actually experience. Do not propose full alternative designs."
        ),
        "simplify": (
            "Your job is to SIMPLIFY -- find the minimum viable version of every proposal. "
            "Ask what can be cut, deferred, or made simpler. Push for the smallest thing "
            "that tests the core assumption."
        ),
    }
    out_lines.append(f"\n{job_desc.get(out.job, job_desc['propose'])}")

    brevity_desc = {
        "concise": "Be direct and brief. Aim for the shortest answer that fully addresses the question. Under 300 words unless the question demands more.",
        "normal": "Be thorough but not exhaustive. Cover what matters, skip what doesn't. Aim for under 600 words.",
        "thorough": "Be comprehensive when the topic warrants it, but don't pad.",
    }
    out_lines.append(f"\n{brevity_desc.get(agent.voice.brevity, brevity_desc['normal'])}")

    sections.append("\n".join(out_lines))

    # Anti-slop rules
    antislop = _build_antislop_section(agent.anti_slop)
    if antislop:
        sections.append(f"## Anti-Slop Rules\n\n{antislop}")

    # Per-turn reminder (compact, appended to every prompt)
    sections.append(
        f"## Remember\n\n"
        f"You are {agent.name}. Stay in character. Your role is {pos.role}. "
        f"Your style is {agent.personality.cognitive_style.value} and "
        f"{agent.personality.emotional_baseline.value}. "
        f"Add substance or stay silent."
    )

    return "\n\n".join(sections)


def build_perspective_reminder(agent: AgentConfig) -> str:
    """Short per-turn identity reinforcement to fight context drift."""
    return (
        f"[You are {agent.name} -- {agent.position.role}. "
        f"Style: {agent.personality.cognitive_style.value}, "
        f"{agent.personality.emotional_baseline.value}. "
        f"Technique: {agent.technique.primary.replace('_', ' ')}. "
        f"Stay in character. Add substance or stay silent.]"
    )
