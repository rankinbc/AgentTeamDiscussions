"""Reusable helper: ask all 3 agents a question in parallel, return results."""

import asyncio
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from interact import load_team
from prompt_builder import build_system_prompt, build_perspective_reminder
from claude_runner import run_claude_async

_team = None
_system_prompts = None


def _ensure_loaded():
    global _team, _system_prompts
    if _team is None:
        _team = load_team(str(Path(__file__).parent / "config" / "teams" / "beta-agents.yaml"))
        _system_prompts = {key: build_system_prompt(agent) for key, agent in _team.agents.items()}


def ask_panel_sync(question: str, timeout: int = 360, context: str = "") -> dict[str, str]:
    """Ask all 3 agents a question. Returns {agent_key: response}."""
    return asyncio.run(ask_panel(question, timeout, context))


async def ask_panel(question: str, timeout: int = 360, context: str = "") -> dict[str, str]:
    """Async version: ask all 3 agents in parallel."""
    _ensure_loaded()

    async def ask_one(key, agent):
        reminder = build_perspective_reminder(agent)
        payload = f"{reminder}\n\n"
        if context:
            payload += f"=== Additional Context ===\n{context}\n=== End Context ===\n\n"
        payload += question

        response = await run_claude_async(_system_prompts[key], payload, timeout=timeout)
        return key, response

    tasks = [ask_one(key, agent) for key, agent in _team.agents.items()]
    results = await asyncio.gather(*tasks)
    return {key: resp for key, resp in results}


if __name__ == "__main__":
    # Quick test
    question = sys.argv[1] if len(sys.argv) > 1 else "In one sentence, what should we design first?"
    results = ask_panel_sync(question, timeout=60)
    for key, resp in results.items():
        print(f"--- {key} ---")
        print(resp[:300])
        print()
