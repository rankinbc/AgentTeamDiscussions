"""Assembles system prompts from agent YAML config."""

from models import AgentConfig, AntiSlopConfig, PersonalityConfig


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
        _describe_trait("idea_receptivity", p.idea_receptivity,
                        "an agenda driver who stays focused on your own ideas and redirects others back to your points",
                        "deeply engaged with others' ideas -- you build on what others say, amplify their best points, and genuinely absorb their perspective before responding"),
        _describe_trait("bluntness", p.bluntness,
                        "diplomatic and tactful -- you soften hard truths and frame criticism constructively",
                        "brutally direct -- you say exactly what you think with zero sugar-coating, and you don't care if it stings. You'd rather be rude and right than polite and vague"),
        _describe_trait("patience", p.patience,
                        "impatient -- you cut off tangents, call out circular arguments, and push to move on when the discussion is spinning its wheels",
                        "patient -- you let discussions breathe, allow tangents that might lead somewhere, and don't rush to conclusions"),
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


PROJECT_CONTEXT = """## Project Context: AgentTeamDiscussions

You are helping design AgentTeamDiscussions -- an autonomous multi-agent discussion
system that converts product ideas into implementation-ready specs overnight without
continuous human involvement. Built for a solo builder who submits an idea at 10 PM
and wakes up to a Morning Brief with prioritized findings, unresolved disagreements,
and draft specs.

Architecture:
- Two separate agent teams, each in their own Claude context window, communicating
  ONLY through an MCP server message broker (never sharing context)
- Python orchestrator spawns stateless `claude -p` CLI processes (Claude Max OAuth)
- Teams are YAML-configurable: each agent has personality traits (8 dimensions on
  0-1 scales), a stakeholder position (Customer, Investor, Builder, Skeptic, etc.),
  and a creativity technique (SCAMPER, Five Whys, Analogical Thinking, etc.)
- 4 discussion phases: Brainstorm (diverge) -> Refine (challenge) -> Specify (pin
  down) -> Review (adversarial validation)
- 10 anti-slop mechanisms prevent LLM consensus drift: agreement tax, convergence
  suppression, devil's advocate duty, novelty scoring, perspective enforcement,
  uncomfortable idea quotas, domain pivots, surprise audits, silence-as-signal,
  post-hoc diversity checks
- 7 BackgroundAgent types operate on full history: Curator, Oracle, Specter
  (circuit breaker), Director (interventions), Weaver (cross-session synthesis),
  TieBreakerGhost, Custom
- File-per-message storage for context efficiency; teams read summaries, pull full
  bodies on demand
- Morning Brief output: tiered (FYI / needs input / needs decision / needs
  tiebreaker), highlights, draft specs, decision log with confidence scores

Key constraints:
- Must survive 8+ hours of autonomous overnight operation on Windows
- Context windows fill up -- need briefing-based resets at phase transitions
- Each claude CLI call is stateless; all history must be reconstructed from files
- This is ideation and requirements scope only -- agents discuss WHAT to build and
  WHY, not HOW to code it
- All thresholds, traits, and mechanisms must be observable and tunable via YAML

What's decided: entity model (21 types), personality dimensions, position types,
phase structure, anti-slop mechanism list, BackgroundAgent types, file-based storage.
What's NOT decided: message contract between teams, agent turn mechanics, orchestrator
state machine, how traits become prompts, how anti-slop is enforced at runtime, phase
transition triggers, context management strategy, AgentMind schema."""


def build_system_prompt(agent: AgentConfig, include_project_context: bool = True) -> str:
    """Assemble the full system prompt from agent config."""
    sections = []

    # Project context (skip for non-software teams)
    if include_project_context:
        sections.append(PROJECT_CONTEXT)

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
        "ideate": (
            "Your job is to IDEATE -- generate a numbered list of 3+ specific, named, "
            "surprising ideas. Each idea gets a bold **Name**, a one-line pitch, and one "
            "concrete mechanism detail. Do NOT describe architectures, pipelines, or system "
            "designs. Do NOT analyze the problem. Only generate novel ideas stolen from "
            "non-software domains (biology, game design, economics, military doctrine, "
            "improv comedy, restaurant logistics). If your idea sounds like something a "
            "software architect would say, delete it and try harder."
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


def build_context_lens(agent: AgentConfig) -> str:
    """Build an agent-specific context lens that tells the agent what to focus on.

    This doesn't filter the raw context -- it adds a framing layer that directs
    the agent's attention to the parts of the context that matter for their role.
    Cheaper and more robust than actually filtering text.
    """
    lines = []

    # What this agent cares about
    if agent.position.drives:
        top_drives = agent.position.drives[:3]
        lines.append("When reading the context below, focus on:")
        for d in top_drives:
            lines.append(f"  - {d}")

    # What this agent should challenge
    if agent.position.pushback_on:
        top_pushback = agent.position.pushback_on[:3]
        lines.append("Flag anything that looks like:")
        for p in top_pushback:
            lines.append(f"  - {p}")

    # Domain lens
    if agent.personality.domain_affinities:
        domains = ", ".join(agent.personality.domain_affinities[:4])
        lines.append(f"Apply your expertise in: {domains}")

    # Receptivity framing
    r = agent.personality.idea_receptivity
    if r >= 0.7:
        lines.append("Pay close attention to what other agents proposed. Build on their best ideas.")
    elif r <= 0.3:
        lines.append("Stay focused on your own perspective. Don't get pulled into other agents' framing.")

    # Patience framing
    p = agent.personality.patience
    if p <= 0.3:
        lines.append("If the discussion is covering old ground, call it out and push forward.")

    if not lines:
        return ""

    return "=== Your Focus for This Context ===\n" + "\n".join(lines) + "\n=== End Focus ===\n"


def filter_prior_rounds(prior_rounds: str, agent: AgentConfig) -> str:
    """Optionally compress prior rounds based on agent's receptivity and patience.

    High-receptivity agents get the full discussion.
    Low-receptivity agents get a compressed version (just agent names + first sentence).
    Low-patience agents get only the most recent round.
    """
    if not prior_rounds:
        return prior_rounds

    r = agent.personality.idea_receptivity
    p = agent.personality.patience

    # High receptivity + high patience: full context
    if r >= 0.5 and p >= 0.5:
        return prior_rounds

    # Low patience: trim to last ~2000 chars (most recent exchanges)
    if p < 0.3 and len(prior_rounds) > 3000:
        # Find a good break point
        trimmed = prior_rounds[-2500:]
        # Find the first complete agent header
        idx = trimmed.find("\n[")
        if idx > 0:
            trimmed = trimmed[idx:]
        return f"[Earlier discussion truncated -- focusing on recent exchanges]\n{trimmed}"

    # Low receptivity: keep full text but it'll be framed by the context lens
    return prior_rounds
