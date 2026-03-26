"""Single-agent conversation loop."""

import sys
from pathlib import Path

import yaml

from conversation import Conversation
from agentteam.runner.claude import run_claude_sync
from agentteam.types import AgentConfig, TeamConfig


def load_team(config_path: str) -> TeamConfig:
    """Load team config from YAML."""
    with open(config_path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    # Parse each agent
    agents = {}
    for key, agent_data in raw["agents"].items():
        agents[key] = AgentConfig(**agent_data)

    return TeamConfig(agents=agents)


def pick_agent(team: TeamConfig) -> tuple[str, AgentConfig]:
    """Interactive agent selection."""
    print("\nAvailable agents:")
    keys = list(team.agents.keys())
    for i, key in enumerate(keys, 1):
        agent = team.agents[key]
        print(f"  {i}. {agent.name} -- {agent.position.role}")
    print()

    while True:
        choice = input("Pick an agent (number or name): ").strip()
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(keys):
                key = keys[idx]
                return key, team.agents[key]
        elif choice.lower() in team.agents:
            return choice.lower(), team.agents[choice.lower()]
        print("Invalid choice, try again.")


def run_conversation(team: TeamConfig):
    """Main conversation loop."""
    agent_key, agent = pick_agent(team)
    conv = Conversation(agent=agent)

    print(f"\n--- Talking to {agent.name} ({agent.position.role}) ---")
    print("Commands: 'quit', '/switch', '/history', '/debug'\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break

        if not user_input:
            continue

        if user_input.lower() == "quit":
            print("Bye!")
            break

        if user_input == "/switch":
            agent_key, agent = pick_agent(team)
            conv = Conversation(agent=agent)
            print(f"\n--- Switched to {agent.name} ({agent.position.role}) ---\n")
            continue

        if user_input == "/history":
            if not conv.history:
                print("[No history yet]")
            else:
                for msg in conv.history:
                    label = msg.agent_name if msg.role == "assistant" else "You"
                    print(f"[{label}]: {msg.content[:200]}{'...' if len(msg.content) > 200 else ''}")
            print()
            continue

        if user_input == "/debug":
            print("=== System Prompt ===")
            print(conv.system_prompt)
            print("=== End System Prompt ===\n")
            continue

        # Build payload and run
        conv.add_user_message(user_input)

        # Add uncomfortable idea nudge if triggered
        message = user_input
        if conv.should_trigger_uncomfortable_idea():
            message += "\n\n[System: It's time to introduce an uncomfortable or contrarian idea that challenges the current direction.]"

        payload = conv.build_prompt_payload(message)

        print(f"\n{agent.name}: ", end="", flush=True)
        response = run_claude_sync(conv.system_prompt, payload)
        print(response)
        print()

        conv.add_assistant_message(response)


def main():
    config_path = Path(__file__).resolve().parent.parent.parent.parent / "data" / "teams" / "beta-agents.yaml"

    if not config_path.exists():
        print(f"Config not found: {config_path}")
        sys.exit(1)

    team = load_team(str(config_path))
    run_conversation(team)


if __name__ == "__main__":
    main()
