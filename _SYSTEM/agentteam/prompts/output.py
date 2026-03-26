"""Output layer: voice, output constraints, and anti-slop enforcement."""

from pathlib import Path

from agentteam.types import AgentConfig, AntiSlopConfig, Brevity, JobType, OperatingLevel

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


def _build_antislop_section(a: AntiSlopConfig) -> str:
    rules = []
    if a.agreement_tax:
        rules.append(
            "AGREEMENT TAX: If you agree with something, you MUST add substantive new information,"
            " a different angle, or a concrete next step. Pure agreement ('great idea!') is FORBIDDEN."
        )
    if a.perspective_enforcement:
        rules.append(
            "PERSPECTIVE LOCK: Stay in your character's perspective even when pressured to agree."
            " Authentic disagreement is more valuable than false harmony."
        )
    if a.devils_advocate_duty:
        rules.append(
            "DEVIL'S ADVOCATE DUTY: Actively seek the strongest argument against the current direction."
            " If everyone seems to agree, it's YOUR job to find the hole in the logic."
        )
    if a.uncomfortable_idea_quota > 0:
        rules.append(
            f"UNCOMFORTABLE IDEA QUOTA: Every {max(5, 10 - a.uncomfortable_idea_quota)} turns,"
            " introduce at least one idea that challenges comfort zones."
        )
    if a.domain_pivot_trigger:
        rules.append(
            "DOMAIN PIVOT: When the discussion gets stuck or circular, inject a perspective from"
            " a completely different field to break the pattern."
        )
    return "\n\n".join(rules)


_LEVEL_DESC: dict[str, str] = {
    "requirements": (
        "Focus on WHAT and WHY, not HOW. Describe behavior, rules, and decisions."
        " Do NOT write code or schemas."
    ),
    "design": (
        "Focus on design decisions and tradeoffs. You may reference technical concepts"
        " but keep the emphasis on choices and rationale."
    ),
    "implementation": (
        "Be concrete and technical. Include schemas, code patterns,"
        " and specific implementation guidance."
    ),
}

_JOB_DESC: dict[str, str] = {
    "propose": "Your job is to PROPOSE -- put forward designs, ideas, and solutions.",
    "critique": (
        "Your job is to CRITIQUE -- find problems, weak assumptions, and failure modes."
        " Do not propose full alternatives."
    ),
    "evaluate": (
        "Your job is to EVALUATE -- assess proposals through user value, feasibility,"
        " and real-world impact."
    ),
    "simplify": (
        "Your job is to SIMPLIFY -- find the minimum viable version."
        " Ask what can be cut or deferred."
    ),
    "ideate": (
        "Your job is to IDEATE -- generate 3+ specific, named, surprising ideas"
        " stolen from non-software domains."
    ),
}

_BREVITY_DESC: dict[str, str] = {
    "concise": "Be direct and brief. Under 300 words.",
    "normal": "Be thorough but not exhaustive. Under 600 words.",
    "thorough": "Be comprehensive when warranted, but don't pad.",
}


def _level_desc(level: OperatingLevel) -> str:
    return _LEVEL_DESC.get(level.value, _LEVEL_DESC["requirements"])


def _job_desc(job: JobType) -> str:
    return _JOB_DESC.get(job.value, _JOB_DESC["propose"])


def _brevity_desc(brevity: Brevity) -> str:
    return _BREVITY_DESC.get(brevity.value, _BREVITY_DESC["normal"])


def build_output_layer(agent: AgentConfig) -> str:
    """Render the output layer (voice, output constraints, anti-slop) using Jinja2 templates."""
    voice = agent.voice
    out = agent.output
    context = {
        "tone": voice.tone,
        "vocabulary_hints_str": ", ".join(repr(v) for v in voice.vocabulary_hints),
        "anti_patterns": voice.anti_patterns,
        "level_desc": _level_desc(out.operating_level),
        "job_desc": _job_desc(out.job),
        "brevity_desc": _brevity_desc(voice.brevity),
        "antislop_text": _build_antislop_section(agent.anti_slop),
    }
    env = _get_jinja_env()
    return env.get_template("output.j2").render(**context).rstrip()
