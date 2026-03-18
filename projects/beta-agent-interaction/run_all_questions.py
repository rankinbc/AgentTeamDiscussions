"""Run all 10 design questions against each agent in a single call per agent.

Each agent gets their system prompt once and all 10 questions as one payload.
This means: 3 calls total (one per agent), running in parallel.
"""

import asyncio
import sys
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import yaml
from interact import load_team
from prompt_builder import build_system_prompt, build_perspective_reminder
from claude_runner import run_claude_async


def load_questions() -> list[dict]:
    """Load and format all questions from the config."""
    questions_path = Path(__file__).parent / "config" / "design-questions.yaml"
    with open(questions_path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    questions = []
    for q_key, q_data in raw["questions"].items():
        q_id = q_key.split("_")[0]
        questions.append({
            "id": q_id,
            "title": q_data["title"],
            "prompt": q_data["prompt"].strip(),
        })
    return questions


def build_mega_prompt(agent, questions: list[dict]) -> str:
    """Build a single payload containing all 10 questions for one agent."""
    reminder = build_perspective_reminder(agent)

    parts = [
        reminder,
        "",
        "You are being asked 10 design questions about the AgentTeamDiscussions system.",
        "Answer ALL 10 questions in order. For each question:",
        "- Use the heading format: # Question N: [title]",
        "- Give a thorough, concrete answer with schemas, code snippets, and specific",
        "  design decisions where appropriate",
        "- Stay in character throughout -- your perspective and technique should shape",
        "  every answer",
        "- Do NOT refer to other agents or their answers -- you are answering independently",
        "- Be concrete and specific. Propose actual designs, not abstract principles.",
        "",
        "Here are all 10 questions:",
        "",
    ]

    for q in questions:
        parts.append(f"---")
        parts.append(f"")
        parts.append(f"## Question {q['id']}: {q['title']}")
        parts.append(f"")
        parts.append(q["prompt"])
        parts.append(f"")

    parts.append("---")
    parts.append("")
    parts.append("Now answer all 10 questions in order. Begin with Question 1.")

    return "\n".join(parts)


async def run_agent(agent_key, agent, system_prompt, questions):
    """Run all 10 questions against one agent in a single call."""
    payload = build_mega_prompt(agent, questions)

    print(f"  Starting: {agent.name} ({len(payload)} chars payload)", flush=True)
    start = time.time()

    # Long timeout -- these are 10 meaty questions in one response
    response = await run_claude_async(system_prompt, payload, timeout=600)

    elapsed = time.time() - start
    timed_out = "[Claude CLI timed out" in response
    status = "TIMEOUT" if timed_out else f"OK ({len(response)} chars)"
    print(f"  Done:     {agent.name} -- {status} ({elapsed:.0f}s)", flush=True)

    return {
        "agent_key": agent_key,
        "agent_name": agent.name,
        "agent_role": agent.position.role,
        "response": response,
        "elapsed": elapsed,
        "timed_out": timed_out,
    }


async def main():
    team = load_team(str(Path(__file__).parent / "config" / "teams" / "beta-agents.yaml"))
    questions = load_questions()
    system_prompts = {key: build_system_prompt(agent) for key, agent in team.agents.items()}

    print(f"\nLaunching 3 parallel calls (one per agent, all 10 questions each)...\n", flush=True)
    start_all = time.time()

    results = await asyncio.gather(*[
        run_agent(key, agent, system_prompts[key], questions)
        for key, agent in team.agents.items()
    ])

    total_time = time.time() - start_all
    succeeded = sum(1 for r in results if not r["timed_out"])
    print(f"\nAll done in {total_time:.0f}s. Succeeded: {succeeded}/{len(results)}\n", flush=True)

    # Write output
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / f"design_questions_{timestamp}.md"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# AgentTeamDiscussions: Design Question Responses\n\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"Total time: {total_time:.0f}s -- 3 calls (one per agent, all 10 questions)\n")
        f.write(f"Succeeded: {succeeded}/{len(results)}\n\n")
        f.write("---\n\n")

        for r in sorted(results, key=lambda x: x["agent_key"]):
            f.write(f"# {r['agent_name']} ({r['agent_role']})\n\n")
            if r["timed_out"]:
                f.write(f"*[Timed out after 600s]*\n\n")
            else:
                f.write(r["response"])
                f.write(f"\n\n*({r['elapsed']:.0f}s)*\n\n")
            f.write("---\n\n")

    print(f"Output saved to: {output_path}")
    for r in results:
        lines = len(r["response"].split("\n")) if not r["timed_out"] else 0
        print(f"  {r['agent_name']}: {lines} lines, {len(r['response']):,} chars")


if __name__ == "__main__":
    asyncio.run(main())
