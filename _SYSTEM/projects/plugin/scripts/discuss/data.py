"""Load personas, teams, modes, overlays and display names from the repo.

Nothing is copied into the plugin: the source of truth stays where the C#
engine reads it. Paths resolve relative to the plugin root, which sits at
_SYSTEM/projects/plugin next to the engine.
"""

import os
from dataclasses import dataclass, field
from pathlib import Path

import yaml

PLUGIN_ROOT = Path(__file__).resolve().parents[2]
ENGINE_DIR = Path(os.environ.get("ATD_ENGINE_DIR", PLUGIN_ROOT.parent / "engine"))
SHARED_DATA_DIR = Path(os.environ.get("ATD_DATA_DIR", PLUGIN_ROOT.parents[1] / "data"))

AGENTS_DIR = SHARED_DATA_DIR / "discussionAgents"
ENGINE_TEAMS_DIR = ENGINE_DIR / "data" / "teams"
SHARED_TEAMS_DIR = SHARED_DATA_DIR / "teams"
CONFIG_DIR = ENGINE_DIR / "config"
TEMPLATES_DIR = ENGINE_DIR / "templates" / "prompts"
SESSIONS_DIR = ENGINE_DIR / "output" / "sessions"
INPUT_DIR = ENGINE_DIR / "input"

COGNITIVE_STYLES = {"analytical", "lateral", "systematic", "intuitive", "divergent"}
EMOTIONAL_BASELINES = {"optimistic", "skeptical", "curious", "cautious", "neutral", "enthusiastic"}
BREVITIES = {"concise", "normal", "thorough"}
LEVELS = {"requirements", "design", "implementation"}
JOBS = {"propose", "critique", "evaluate", "simplify", "ideate"}


@dataclass
class Personality:
    assertiveness: float = 0.5
    creativity_temp: float = 0.5
    risk_tolerance: float = 0.5
    attention_span: float = 0.5
    stubbornness: float = 0.5
    idea_receptivity: float = 0.5
    bluntness: float = 0.5
    patience: float = 0.5
    cognitive_style: str = "analytical"
    emotional_baseline: str = "neutral"
    domain_affinities: list = field(default_factory=list)


@dataclass
class Position:
    role: str = "participant"
    intensity: float = 0.5
    drives: list = field(default_factory=list)
    pushback_on: list = field(default_factory=list)
    # allergies is deliberately not loaded: AgentLoader.ParsePositionConfig ignores it.


@dataclass
class Technique:
    primary: str = "none"
    style_description: str = ""
    behaviors: list = field(default_factory=list)


@dataclass
class AntiSlop:
    agreement_tax: bool = True
    perspective_enforcement: bool = True
    devils_advocate_duty: bool = False
    uncomfortable_idea_quota: int = 0
    domain_pivot_trigger: bool = False


@dataclass
class Voice:
    tone: str = "professional"
    brevity: str = "normal"
    vocabulary_hints: list = field(default_factory=list)
    anti_patterns: list = field(default_factory=list)


@dataclass
class Output:
    operating_level: str = "requirements"
    job: str = "propose"


@dataclass
class Agent:
    key: str
    team: str
    name: str
    description: str
    personality: Personality
    position: Position
    technique: Technique
    anti_slop: AntiSlop
    voice: Voice
    output: Output


def _enum(raw, key, default, allowed):
    value = str(raw.get(key, default)).lower()
    return value if value in allowed else default


def _num(raw, key, default):
    try:
        return float(raw.get(key, default))
    except (TypeError, ValueError):
        return default


def _strs(raw, key):
    value = raw.get(key)
    return [str(x) for x in value] if isinstance(value, list) else []


def parse_agent(raw: dict, key: str, team: str) -> Agent:
    """Mirror AgentLoader.ParseAgentConfig, including its defaults."""
    p = raw.get("personality") or {}
    pos = raw.get("position") or {}
    tech = raw.get("technique") or {}
    anti = raw.get("anti_slop") or {}
    voice = raw.get("voice") or {}
    out = raw.get("output") or {}
    return Agent(
        key=key,
        team=team,
        name=str(raw.get("name", key)),
        description=str(raw.get("description", "")),
        personality=Personality(
            assertiveness=_num(p, "assertiveness", 0.5),
            creativity_temp=_num(p, "creativity_temp", 0.5),
            risk_tolerance=_num(p, "risk_tolerance", 0.5),
            attention_span=_num(p, "attention_span", 0.5),
            stubbornness=_num(p, "stubbornness", 0.5),
            idea_receptivity=_num(p, "idea_receptivity", 0.5),
            bluntness=_num(p, "bluntness", 0.5),
            patience=_num(p, "patience", 0.5),
            cognitive_style=_enum(p, "cognitive_style", "analytical", COGNITIVE_STYLES),
            emotional_baseline=_enum(p, "emotional_baseline", "neutral", EMOTIONAL_BASELINES),
            domain_affinities=_strs(p, "domain_affinities"),
        ),
        position=Position(
            role=str(pos.get("role", "participant")),
            intensity=_num(pos, "intensity", 0.5),
            drives=_strs(pos, "drives"),
            pushback_on=_strs(pos, "pushback_on"),
        ),
        technique=Technique(
            primary=str(tech.get("primary", "none")),
            style_description=str(tech.get("style_description", "")),
            behaviors=_strs(tech, "behaviors"),
        ),
        anti_slop=AntiSlop(
            agreement_tax=bool(anti.get("agreement_tax", True)),
            perspective_enforcement=bool(anti.get("perspective_enforcement", True)),
            devils_advocate_duty=bool(anti.get("devils_advocate_duty", False)),
            uncomfortable_idea_quota=int(anti.get("uncomfortable_idea_quota", 0) or 0),
            domain_pivot_trigger=bool(anti.get("domain_pivot_trigger", False)),
        ),
        voice=Voice(
            tone=str(voice.get("tone", "professional")),
            brevity=_enum(voice, "brevity", "normal", BREVITIES),
            vocabulary_hints=_strs(voice, "vocabulary_hints"),
            anti_patterns=_strs(voice, "anti_patterns"),
        ),
        output=Output(
            operating_level=_enum(out, "operating_level", "requirements", LEVELS),
            job=_enum(out, "job", "propose", JOBS),
        ),
    )


def load_agent_file(path: Path) -> Agent:
    """Agent files are named {team}__{agent_key}.yaml."""
    stem = path.stem
    team, _, key = stem.partition("__")
    with open(path, encoding="utf-8") as f:
        raw = yaml.safe_load(f) or {}
    return parse_agent(raw, key or stem, team)


def load_all_agents() -> list:
    return [load_agent_file(p) for p in sorted(AGENTS_DIR.glob("*__*.yaml"))]


@dataclass
class Mode:
    name: str
    description: str
    groups: dict  # ordered round name -> [agent_key]
    agent_roles: dict  # agent_key -> overlay name


@dataclass
class Team:
    name: str
    agents: dict  # agent_key -> Agent
    modes: dict  # mode name -> Mode
    default_mode: str


def team_file(team_name: str) -> Path:
    """Modes live in the engine-local team copy; fall back to the shared copy."""
    for d in (ENGINE_TEAMS_DIR, SHARED_TEAMS_DIR):
        candidate = d / f"{team_name}.yaml"
        if candidate.exists():
            return candidate
    raise FileNotFoundError(f"team not found: {team_name}")


def list_team_names() -> list:
    names = set()
    for d in (ENGINE_TEAMS_DIR, SHARED_TEAMS_DIR):
        if d.exists():
            names.update(p.stem for p in d.glob("*.yaml"))
    return sorted(names)


def load_team(team_name: str) -> Team:
    with open(team_file(team_name), encoding="utf-8") as f:
        raw = yaml.safe_load(f) or {}

    agents = {}
    for entry in raw.get("agents") or []:
        key = entry.get("agent_key")
        file_name = entry.get("file") or f"{team_name}__{key}.yaml"
        path = AGENTS_DIR / file_name
        if not path.exists():
            continue
        agents[key] = load_agent_file(path)

    modes = {}
    for mode_name, m in (raw.get("modes") or {}).items():
        modes[mode_name] = Mode(
            name=mode_name,
            description=str(m.get("description", "")),
            groups={r: list(a or []) for r, a in (m.get("groups") or {}).items()},
            agent_roles=dict(m.get("agent_roles") or {}),
        )
    if not modes:
        # DiscussionEngine falls back to a propose-only round with everyone.
        modes["default"] = Mode("default", "fallback", {"propose": list(agents)}, {})

    default_mode = str(raw.get("default_mode") or next(iter(modes)))
    return Team(team_name, agents, modes, default_mode)


def filter_mode(mode: Mode, active: set) -> Mode:
    """Restrict a mode to the selected agents and drop empty rounds (SessionRunner)."""
    groups = {r: [a for a in agents if a in active] for r, agents in mode.groups.items()}
    groups = {r: a for r, a in groups.items() if a}
    roles = {k: v for k, v in mode.agent_roles.items() if k in active}
    return Mode(mode.name, mode.description, groups, roles)


def _yaml(path: Path) -> dict:
    if not path.exists():
        return {}
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def display_names() -> dict:
    return dict(_yaml(CONFIG_DIR / "agent_display.yaml").get("display_names") or {})


def display_name(key: str) -> str:
    return display_names().get(key, key)


def overlay_instruction(name: str) -> str:
    overlays = _yaml(CONFIG_DIR / "role_overlays.yaml").get("overlays") or {}
    return str((overlays.get(name) or {}).get("instruction", "")).strip()


def counter_propose_instruction() -> str:
    return str(_yaml(CONFIG_DIR / "role_overlays.yaml").get("counter_propose_instruction", "")).strip()


def defaults() -> dict:
    return _yaml(CONFIG_DIR / "defaults.yaml")


def template(name: str) -> str:
    with open(TEMPLATES_DIR / name, encoding="utf-8") as f:
        return f.read().strip()
