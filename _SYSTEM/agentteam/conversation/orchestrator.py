"""Three-round discussion orchestration for agent teams."""

import random
import time
from typing import Callable

from agentteam.agents.drift import build_drift_reminder, detect_drift
from agentteam.prompts.builder import build_context_lens, build_perspective_reminder, filter_prior_rounds
from agentteam.runner.claude import run_claude_async
from agentteam.runner.errors import is_error_response
from agentteam.types import TeamConfig


def compute_speaking_order(agents: list[str], team: TeamConfig) -> list[str]:
    """Order agents by priority score (assertiveness + intensity + stubbornness) with random jitter.

    Higher score speaks first. Jitter prevents deterministic ordering on every run.
    """
    scored = []
    for key in agents:
        agent = team.agents[key]
        p = agent.personality
        score = (p.assertiveness * 0.5 + agent.position.intensity * 0.3 + p.stubbornness * 0.2)
        score += random.uniform(-0.1, 0.1)
        scored.append((key, score))
    scored.sort(key=lambda x: x[1], reverse=True)
    return [key for key, _ in scored]


def build_agent_payload(
    agent_key: str,
    team: TeamConfig,
    question: dict,
    decisions: str,
    prior_rounds: str,
    prior_specs: str,
    open_questions: str,
    round_instruction: str = "",
    this_round_so_far: str = "",
    previous_response: str = "",
) -> str:
    """Build the full user-message payload for one agent in a round.

    Uses perspective reminder, context lens, and filtered prior rounds from agentteam.prompts.builder.
    No config_loader or AGENT_DISPLAY_NAMES dependencies — pure agentteam library code.
    """
    agent = team.agents[agent_key]
    parts: list[str] = []

    reminder = build_perspective_reminder(agent)
    parts.append(reminder)

    # Drift detection — inject targeted reminder if agent has drifted from their role
    if previous_response and detect_drift(previous_response, agent):
        parts.append(build_drift_reminder(agent))

    context_lens = build_context_lens(agent)
    if context_lens:
        parts.append(context_lens)

    if decisions:
        parts.append(
            f"=== What's Already Decided ===\n{decisions}\n=== End Decisions ==="
        )

    if prior_specs:
        parts.append(
            f"=== Prior Design Docs (reference, don't contradict) ===\n"
            f"{prior_specs}\n=== End Prior Docs ==="
        )

    if open_questions:
        parts.append(
            f"=== Unresolved Open Questions from Prior Docs ===\n{open_questions}\n"
            f"=== End Open Questions ===\n\nIf this question can resolve any of the above, do so."
        )

    filtered = filter_prior_rounds(prior_rounds, agent)
    combined = filtered
    if this_round_so_far:
        combined += f"\n\n--- This round so far ---\n{this_round_so_far}"
    if combined.strip():
        parts.append(
            f"=== Discussion So Far (this question) ===\n{combined}\n=== End Discussion ==="
        )

    parts.append(f"## Question: {question['title']}\n\n{question['body']}")

    if round_instruction:
        parts.append(round_instruction)

    if this_round_so_far:
        parts.append(
            "Other agents have already spoken this round. Respond to their points directly. "
            "Agree, disagree, or build on what they said. 250 words max."
        )
    else:
        parts.append("You are speaking first this round. Set the agenda. 250 words max.")

    return "\n\n".join(parts)


async def run_round(
    agents: list[str],
    system_prompts: dict[str, str],
    team: TeamConfig,
    question: dict,
    decisions: str,
    prior_rounds: str,
    prior_specs: str,
    open_questions: str,
    timeout: int,
    round_instruction: str = "",
    on_agent_start: Callable[[str], None] | None = None,
    on_agent_done: Callable[[str, str, float], None] | None = None,
    previous_responses: dict[str, str] | None = None,
) -> dict[str, str]:
    """Run one round sequentially. Each agent sees all prior speakers in this_round_so_far.

    Callbacks:
      on_agent_start(agent_key: str)
      on_agent_done(agent_key: str, response: str, elapsed: float)
    """
    ordered = compute_speaking_order(agents, team)
    responses: dict[str, str] = {}
    this_round_so_far = ""

    for agent_key in ordered:
        if on_agent_start:
            on_agent_start(agent_key)

        start = time.time()
        payload = build_agent_payload(
            agent_key, team, question, decisions, prior_rounds,
            prior_specs, open_questions, round_instruction, this_round_so_far,
            previous_response=(previous_responses or {}).get(agent_key, ""),
        )
        response = await run_claude_async(system_prompts[agent_key], payload, timeout=timeout)
        elapsed = time.time() - start

        if is_error_response(response):
            raise RuntimeError(f"Claude failed for agent {agent_key!r}: {response}")

        responses[agent_key] = response

        if on_agent_done:
            on_agent_done(agent_key, response, elapsed)

        # Accumulate for the next speaker's context
        agent = team.agents[agent_key]
        this_round_so_far += f"[{agent.name}]\n{response}\n\n"

    return responses
