"""Rerun the 22 timed-out design question calls with higher timeout."""

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


# The 22 that timed out
FAILED = [
    ("1", "cognitive_architect"),
    ("2", "cognitive_architect"), ("2", "product_oracle"), ("2", "systems_pragmatist"),
    ("3", "product_oracle"), ("3", "systems_pragmatist"),
    ("4", "cognitive_architect"), ("4", "product_oracle"), ("4", "systems_pragmatist"),
    ("5", "cognitive_architect"), ("5", "product_oracle"), ("5", "systems_pragmatist"),
    ("6", "product_oracle"), ("6", "systems_pragmatist"),
    ("7", "product_oracle"), ("7", "systems_pragmatist"),
    ("8", "cognitive_architect"),
    ("9", "cognitive_architect"), ("9", "product_oracle"), ("9", "systems_pragmatist"),
    ("10", "cognitive_architect"), ("10", "systems_pragmatist"),
]


async def ask_agent(agent_key, agent, system_prompt, question_id, title, prompt):
    reminder = build_perspective_reminder(agent)
    payload = f"{reminder}\n\n{prompt}"

    print(f"  Starting: Q{question_id} x {agent.name}", flush=True)
    start = time.time()
    response = await run_claude_async(system_prompt, payload, timeout=360)
    elapsed = time.time() - start
    timed_out = "[Claude CLI timed out" in response
    status = "TIMEOUT" if timed_out else "OK"
    print(f"  {status}:     Q{question_id} x {agent.name} ({elapsed:.0f}s)", flush=True)

    return {
        "question_id": question_id,
        "title": title,
        "agent_key": agent_key,
        "agent_name": agent.name,
        "agent_role": agent.position.role,
        "response": response,
        "elapsed": elapsed,
    }


async def main():
    team = load_team(str(Path(__file__).parent / "config" / "teams" / "beta-agents.yaml"))

    questions_path = Path(__file__).parent / "config" / "design-questions.yaml"
    with open(questions_path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    questions = raw["questions"]
    q_by_id = {}
    for q_key, q_data in questions.items():
        q_id = q_key.split("_")[0]
        q_by_id[q_id] = q_data

    system_prompts = {key: build_system_prompt(agent) for key, agent in team.agents.items()}

    tasks = []
    for q_id, agent_key in FAILED:
        q_data = q_by_id[q_id]
        agent = team.agents[agent_key]
        tasks.append(
            ask_agent(agent_key, agent, system_prompts[agent_key],
                      q_id, q_data["title"], q_data["prompt"])
        )

    print(f"\nRetrying {len(tasks)} timed-out calls with 360s timeout, 4 concurrent...\n", flush=True)
    start_all = time.time()

    semaphore = asyncio.Semaphore(4)

    async def throttled(coro):
        async with semaphore:
            return await coro

    results = await asyncio.gather(*[throttled(t) for t in tasks])
    total_time = time.time() - start_all

    succeeded = sum(1 for r in results if "[Claude CLI timed out" not in r["response"])
    print(f"\nDone in {total_time:.0f}s. Succeeded: {succeeded}/{len(results)}\n", flush=True)

    # Organize by question
    by_question = {}
    for r in results:
        qid = r["question_id"]
        if qid not in by_question:
            by_question[qid] = {"title": r["title"], "responses": []}
        by_question[qid]["responses"].append(r)

    # Write supplement file
    output_dir = Path(__file__).parent / "output"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    output_path = output_dir / f"design_questions_retry_{timestamp}.md"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# AgentTeamDiscussions: Design Question Responses (Retry)\n\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"Total time: {total_time:.0f}s across {len(results)} calls\n")
        f.write(f"Succeeded: {succeeded}/{len(results)}\n\n")
        f.write("---\n\n")

        for qid in sorted(by_question.keys(), key=lambda x: int(x)):
            q = by_question[qid]
            f.write(f"# Question {qid}: {q['title']}\n\n")

            for resp in sorted(q["responses"], key=lambda r: r["agent_key"]):
                f.write(f"## {resp['agent_name']} ({resp['agent_role']})\n\n")
                f.write(resp["response"])
                f.write(f"\n\n*({resp['elapsed']:.0f}s)*\n\n")
                f.write("---\n\n")

    print(f"Output saved to: {output_path}")


if __name__ == "__main__":
    asyncio.run(main())
