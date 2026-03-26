"""Agent and team loading from the data directory."""

from pathlib import Path

import yaml

from agentteam.types import AgentConfig, JobType, TeamConfig

_SYSTEM_DIR = Path(__file__).resolve().parent.parent.parent
_DATA_DIR = _SYSTEM_DIR / "data"
_AGENTS_DIR = _DATA_DIR / "discussionAgents"
_TEAMS_DIR = _DATA_DIR / "teams"


def load_agent(config_path: str) -> AgentConfig:
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Agent config not found: {config_path}")
    with open(path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)
    raw.pop("_meta", None)  # backward compat with old YAML files
    raw.pop("meta", None)
    return AgentConfig(**raw)


def load_agent_by_key(agent_key: str, agents_dir: Path = None) -> AgentConfig:
    search_dir = agents_dir or _AGENTS_DIR
    if not search_dir.exists():
        raise FileNotFoundError(f"Agents directory not found: {search_dir}")
    exact = search_dir / f"{agent_key}.yaml"
    if exact.exists():
        return load_agent(str(exact))
    for f in search_dir.glob(f"*__{agent_key}.yaml"):
        return load_agent(str(f))
    raise FileNotFoundError(f"No agent file found for key '{agent_key}' in {search_dir}")


def load_team_by_name(team_name: str, teams_dir: Path = None, agents_dir: Path = None) -> TeamConfig:
    t_dir = teams_dir or _TEAMS_DIR
    a_dir = agents_dir or _AGENTS_DIR
    team_path = t_dir / f"{team_name}.yaml"
    if not team_path.exists():
        raise FileNotFoundError(f"Team config not found: {team_path}")
    with open(team_path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)
    agents = {}
    for entry in raw.get("agents", []):
        agent_key = entry["agent_key"]
        agent_file = entry.get("file")
        if agent_file:
            agents[agent_key] = load_agent(str(a_dir / agent_file))
        else:
            agents[agent_key] = load_agent_by_key(agent_key, a_dir)
    return TeamConfig(agents=agents)


def load_team(config_path: str) -> TeamConfig:
    path = Path(config_path)
    team_dir = path.parent
    if not path.exists():
        raise FileNotFoundError(f"Team config not found: {config_path}")
    with open(path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)
    if "agents" not in raw:
        raise KeyError(f"Team config missing 'agents' key: {config_path}")
    if isinstance(raw["agents"], list):
        agents = {}
        for entry in raw["agents"]:
            agent_key = entry["agent_key"]
            agent_file = entry.get("file")
            if agent_file:
                agent_path = team_dir / agent_file
                if not agent_path.exists():
                    agent_path = _AGENTS_DIR / agent_file
                if not agent_path.exists():
                    raise FileNotFoundError(
                        f"Agent file '{agent_file}' not found in team dir ({team_dir}) "
                        f"or agents dir ({_AGENTS_DIR})"
                    )
                agents[agent_key] = load_agent(str(agent_path))
            else:
                agents[agent_key] = load_agent_by_key(agent_key)
        return TeamConfig(agents=agents)
    else:
        return TeamConfig(agents={k: AgentConfig(**v) for k, v in raw["agents"].items()})


def resolve_agent(team: TeamConfig, identifier: str) -> tuple[str, AgentConfig]:
    if identifier in team.agents:
        return identifier, team.agents[identifier]
    lower_id = identifier.lower()
    for key, agent in team.agents.items():
        if key.lower() == lower_id or agent.name.lower() == lower_id:
            return key, agent
    for key, agent in team.agents.items():
        if hasattr(agent, "id") and agent.id == identifier:
            return key, agent
    available = ", ".join(f"{k} ({a.name})" for k, a in team.agents.items())
    raise KeyError(f"Agent not found: '{identifier}'. Available: {available}")


def list_teams(teams_dir: Path = None) -> list[dict]:
    t_dir = teams_dir or _TEAMS_DIR
    if not t_dir.exists():
        return []
    teams = []
    for f in sorted(t_dir.glob("*.yaml")):
        with open(f, "r", encoding="utf-8") as fh:
            raw = yaml.safe_load(fh)
        teams.append({"name": raw.get("name", f.stem), "file": f.name, "agent_count": len(raw.get("agents", []))})
    return teams


def list_agents(agents_dir: Path = None) -> list[dict]:
    a_dir = agents_dir or _AGENTS_DIR
    if not a_dir.exists():
        return []
    agents = []
    for f in sorted(a_dir.glob("*.yaml")):
        with open(f, "r", encoding="utf-8") as fh:
            raw = yaml.safe_load(fh)
        agents.append({"id": raw.get("id", ""), "name": raw.get("name", f.stem), "key": f.stem.split("__")[-1] if "__" in f.stem else f.stem, "file": f.name})
    return agents


_JOB_TO_ROUND: dict[str, str] = {
    "propose": "propose",
    "ideate": "propose",    # idea generators participate in the proposal round
    "critique": "critique",
    "evaluate": "evaluate",
    "simplify": "evaluate", # simplifiers join the evaluation round
}


def assign_rounds_from_job_types(team: TeamConfig) -> dict[str, list[str]]:
    """Derive discussion round groups from each agent's output.job type.

    Returns {"propose": [...], "critique": [...], "evaluate": [...]} with all
    three keys always present (empty list if no agents have that job).

    JobType.IDEATE maps to "propose" (idea generators participate in proposal round).
    JobType.SIMPLIFY maps to "evaluate".

    Raises:
        ValueError: If no agents qualify for the "propose" round (discussion
            cannot start without at least one proposer).
    """
    groups: dict[str, list[str]] = {"propose": [], "critique": [], "evaluate": []}
    for key, agent in team.agents.items():
        round_name = _JOB_TO_ROUND.get(agent.output.job.value, "propose")
        groups[round_name].append(key)
    if not groups["propose"]:
        raise ValueError(
            "Team has no agents with job=propose or job=ideate. "
            "At least one proposer is required to run a discussion."
        )
    return groups
