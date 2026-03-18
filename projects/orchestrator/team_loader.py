"""YAML team config loading and agent resolution."""

from pathlib import Path

import yaml

from .models import AgentConfig, TeamConfig


def load_team(config_path: str) -> TeamConfig:
    """Load team config from a YAML file.

    Args:
        config_path: Path to the YAML team config file.

    Returns:
        TeamConfig with all agents parsed.

    Raises:
        FileNotFoundError: If the config file doesn't exist.
        KeyError: If the YAML is missing the 'agents' key.
    """
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Team config not found: {config_path}")

    with open(path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    if "agents" not in raw:
        raise KeyError(f"Team config missing 'agents' key: {config_path}")

    agents = {}
    for key, agent_data in raw["agents"].items():
        agents[key] = AgentConfig(**agent_data)

    return TeamConfig(agents=agents)


def resolve_agent(team: TeamConfig, identifier: str) -> tuple[str, AgentConfig]:
    """Look up an agent by YAML key or display name.

    Args:
        team: Loaded TeamConfig.
        identifier: Either the YAML key (e.g. 'cognitive_architect') or
            the display name (e.g. 'The Cognitive Architect').

    Returns:
        Tuple of (agent_key, AgentConfig).

    Raises:
        KeyError: If no agent matches the identifier.
    """
    # Try exact key match first
    if identifier in team.agents:
        return identifier, team.agents[identifier]

    # Try case-insensitive key match
    lower_id = identifier.lower()
    for key, agent in team.agents.items():
        if key.lower() == lower_id:
            return key, agent

    # Try display name match (case-insensitive)
    for key, agent in team.agents.items():
        if agent.name.lower() == lower_id:
            return key, agent

    available = ", ".join(
        f"{k} ({a.name})" for k, a in team.agents.items()
    )
    raise KeyError(
        f"Agent not found: '{identifier}'. Available: {available}"
    )
