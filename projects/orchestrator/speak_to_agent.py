"""Single-shot agent interaction: load config, build prompt, call claude, return response.

Usage as module:
    from orchestrator.speak_to_agent import speak_to_agent
    response = speak_to_agent("cognitive_architect", "What matters most?")

Usage from CLI:
    python -m orchestrator.speak_to_agent cognitive_architect "What matters most?"
"""

import sys
from pathlib import Path

from .claude_runner import run_claude_sync
from .models import AgentConfig
from .prompt_builder import build_system_prompt, build_perspective_reminder
from .team_loader import load_team, resolve_agent


# Default config search paths, relative to this file's location
_THIS_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT = _THIS_DIR.parent  # projects/
_REPO_ROOT = _PROJECT_ROOT.parent  # AgentTeamDiscussions/

_DEFAULT_CONFIG_PATHS = [
    _THIS_DIR / "config" / "teams",                          # orchestrator's own configs (future)
    _PROJECT_ROOT / "beta-agent-interaction" / "config" / "teams",  # existing beta config
]

_DEFAULT_CONFIG_NAME = "beta-agents.yaml"


def _find_team_config(explicit_path: str | None = None) -> str:
    """Resolve team config file path.

    Search order:
    1. Explicit path if provided
    2. config/teams/ under orchestrator package
    3. beta-agent-interaction/config/teams/ (fallback to working config)
    """
    if explicit_path:
        p = Path(explicit_path)
        if p.exists():
            return str(p)
        raise FileNotFoundError(f"Specified team config not found: {explicit_path}")

    for search_dir in _DEFAULT_CONFIG_PATHS:
        candidate = search_dir / _DEFAULT_CONFIG_NAME
        if candidate.exists():
            return str(candidate)

    raise FileNotFoundError(
        f"No team config found. Searched: "
        + ", ".join(str(d / _DEFAULT_CONFIG_NAME) for d in _DEFAULT_CONFIG_PATHS)
    )


def _build_user_message(text: str) -> str:
    """Assemble the user message from situation + task layers.

    Situation layer: Minimal for V1 -- no conversation history, no phase
    tracking. Placeholder structure for future modules to populate.

    Task layer: The user's text with a concrete directive framing.
    """
    parts = []

    # --- Situation layer (V1: minimal) ---
    # Future: conversation summary, phase info, recent messages, artifacts
    # For now, nothing -- pure single-shot.

    # --- Task layer ---
    parts.append(
        f"Respond to this directly. Stay in character and give your honest perspective.\n\n"
        f"{text}"
    )

    return "\n\n".join(parts)


def speak_to_agent(
    agent_id: str,
    text: str,
    team_config: str | None = None,
    timeout: int = 120,
) -> str:
    """Send a single message to an agent and get their response.

    Stateless single-shot: loads agent config, builds 3-layer turn prompt,
    calls claude CLI, returns the raw response. No conversation history.

    Args:
        agent_id: Agent YAML key (e.g. 'cognitive_architect') or display
            name (e.g. 'The Cognitive Architect').
        text: The message to send to the agent.
        team_config: Optional path to team YAML config. If None, searches
            default locations.
        timeout: Claude CLI timeout in seconds.

    Returns:
        The agent's response as a string.
    """
    # Load config and resolve agent
    config_path = _find_team_config(team_config)
    team = load_team(config_path)
    agent_key, agent = resolve_agent(team, agent_id)

    # Identity layer -> system prompt
    system_prompt = build_system_prompt(agent)

    # Situation + Task layers -> user message
    user_message = _build_user_message(text)

    # Call claude
    response = run_claude_sync(
        system_prompt=system_prompt,
        user_message=user_message,
        timeout=timeout,
    )

    return response


def main():
    """CLI entry point."""
    if len(sys.argv) < 3:
        print("Usage: python -m orchestrator.speak_to_agent <agent_id> \"<message>\"")
        print()
        print("  agent_id: YAML key (e.g. cognitive_architect) or display name")
        print("  message:  What to say to the agent")
        print()
        print("Options:")
        print("  --config PATH   Path to team YAML config")
        print("  --timeout N     Timeout in seconds (default: 120)")
        sys.exit(1)

    # Parse args (simple, no argparse needed for this)
    args = sys.argv[1:]
    config_path = None
    timeout = 120

    # Extract flags
    filtered = []
    i = 0
    while i < len(args):
        if args[i] == "--config" and i + 1 < len(args):
            config_path = args[i + 1]
            i += 2
        elif args[i] == "--timeout" and i + 1 < len(args):
            timeout = int(args[i + 1])
            i += 2
        else:
            filtered.append(args[i])
            i += 1

    if len(filtered) < 2:
        print("Error: Need both agent_id and message.")
        sys.exit(1)

    agent_id = filtered[0]
    message = " ".join(filtered[1:])

    try:
        response = speak_to_agent(
            agent_id=agent_id,
            text=message,
            team_config=config_path,
            timeout=timeout,
        )
        print(response)
    except (FileNotFoundError, KeyError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
