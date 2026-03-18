"""Multi-agent conversation modes: round-robin, panel, debate."""

import asyncio
import sys
from pathlib import Path

from conversation import MultiConversation
from claude_runner import run_claude_sync, run_claude_async
from interact import load_team
from prompt_builder import build_system_prompt


def run_panel(team_config, topic: str):
    """All agents respond independently in parallel to the same prompt."""
    agents = team_config.agents
    multi = MultiConversation(agents=agents)
    multi.add_user_message(topic)

    print(f"\n{'='*60}")
    print(f"PANEL DISCUSSION: {topic}")
    print(f"{'='*60}\n")

    async def gather_responses():
        tasks = {}
        for key, agent in agents.items():
            payload = multi.build_agent_payload(key, f"Topic for discussion: {topic}")
            tasks[key] = run_claude_async(multi.system_prompts[key], payload)

        results = {}
        for key, coro in tasks.items():
            results[key] = await coro
        return results

    responses = asyncio.run(gather_responses())

    for key, response in responses.items():
        agent = agents[key]
        print(f"--- {agent.name} ({agent.position.role}) ---")
        print(response)
        print()
        multi.add_agent_message(key, response)

    return multi


def run_round_robin(team_config, topic: str, rounds: int = 3):
    """Each agent responds in sequence, seeing previous responses."""
    agents = team_config.agents
    multi = MultiConversation(agents=agents)
    multi.add_user_message(topic)

    print(f"\n{'='*60}")
    print(f"ROUND ROBIN: {topic}")
    print(f"{'='*60}\n")

    agent_keys = list(agents.keys())

    for round_num in range(1, rounds + 1):
        print(f"--- Round {round_num} ---\n")
        for key in agent_keys:
            agent = agents[key]
            payload = multi.build_agent_payload(key)

            print(f"{agent.name}: ", end="", flush=True)
            response = run_claude_sync(multi.system_prompts[key], payload)
            print(response)
            print()

            multi.add_agent_message(key, response)
        multi.round_count += 1

    return multi


def run_debate(team_config, topic: str, rounds: int = 3):
    """Agents respond to each other, maintaining positions."""
    agents = team_config.agents
    multi = MultiConversation(agents=agents)

    # Frame as debate
    debate_prompt = (
        f"DEBATE TOPIC: {topic}\n\n"
        f"You are in a structured debate. Take a clear position and defend it. "
        f"Engage directly with other participants' arguments. "
        f"Do NOT converge to consensus -- maintain your perspective and find "
        f"the strongest version of your argument."
    )
    multi.add_user_message(debate_prompt)

    print(f"\n{'='*60}")
    print(f"DEBATE: {topic}")
    print(f"{'='*60}\n")

    agent_keys = list(agents.keys())

    # Opening statements (parallel)
    print("--- Opening Statements ---\n")

    async def opening_statements():
        tasks = {}
        for key in agent_keys:
            payload = multi.build_agent_payload(
                key,
                f"Give your opening position on: {topic}\n"
                f"Be clear, specific, and take a definite stance."
            )
            tasks[key] = run_claude_async(multi.system_prompts[key], payload)

        results = {}
        for key, coro in tasks.items():
            results[key] = await coro
        return results

    opening = asyncio.run(opening_statements())
    for key, response in opening.items():
        agent = agents[key]
        print(f"{agent.name}: {response}\n")
        multi.add_agent_message(key, response)

    # Rounds of debate (sequential so each sees previous)
    for round_num in range(1, rounds + 1):
        print(f"--- Round {round_num} ---\n")
        for key in agent_keys:
            agent = agents[key]
            context = (
                f"Round {round_num} of {rounds}. "
                f"Respond to the other participants' arguments. "
                f"Challenge their weakest points. Strengthen your position."
            )
            payload = multi.build_agent_payload(key, context)

            print(f"{agent.name}: ", end="", flush=True)
            response = run_claude_sync(multi.system_prompts[key], payload)
            print(response)
            print()

            multi.add_agent_message(key, response)
        multi.round_count += 1

    return multi


def interactive_multi(team_config):
    """Interactive multi-agent session with mode selection."""
    print("\nMulti-Agent Modes:")
    print("  1. Panel -- all agents respond independently (parallel)")
    print("  2. Round Robin -- agents respond in sequence, building on each other")
    print("  3. Debate -- agents take positions and argue")
    print()

    while True:
        choice = input("Pick a mode (1-3): ").strip()
        if choice in ("1", "2", "3"):
            break
        print("Invalid choice.")

    topic = input("\nTopic/prompt: ").strip()
    if not topic:
        print("No topic provided.")
        return

    if choice == "1":
        multi = run_panel(team_config, topic)
    elif choice == "2":
        rounds = input("Number of rounds [3]: ").strip()
        rounds = int(rounds) if rounds.isdigit() else 3
        multi = run_round_robin(team_config, topic, rounds)
    else:
        rounds = input("Number of debate rounds [3]: ").strip()
        rounds = int(rounds) if rounds.isdigit() else 3
        multi = run_debate(team_config, topic, rounds)

    # Offer continuation
    print("\nContinue the discussion? Enter a follow-up or 'quit'.")
    while True:
        try:
            follow_up = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if not follow_up or follow_up.lower() == "quit":
            break

        multi.add_user_message(follow_up)

        # Round-robin follow-up
        for key in team_config.agents:
            agent = team_config.agents[key]
            payload = multi.build_agent_payload(key)
            print(f"\n{agent.name}: ", end="", flush=True)
            response = run_claude_sync(multi.system_prompts[key], payload)
            print(response)
            multi.add_agent_message(key, response)

    print("\nDone!")


def main():
    config_path = Path(__file__).parent / "config" / "teams" / "beta-agents.yaml"

    if not config_path.exists():
        print(f"Config not found: {config_path}")
        sys.exit(1)

    team = load_team(str(config_path))
    interactive_multi(team)


if __name__ == "__main__":
    main()
