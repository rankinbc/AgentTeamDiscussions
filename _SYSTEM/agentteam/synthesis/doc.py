"""Design doc synthesis — calls Claude to merge round responses into a structured design document."""

from agentteam.runner.claude import run_claude_async
from agentteam.runner.errors import is_error_response

_MIN_SYNTHESIS_LENGTH = 50  # chars — anything shorter is considered a synthesis failure


def build_synthesis_input(
    question: dict,
    round_responses: dict[str, dict[str, str]],
    round_labels: list[str],
    decisions: str = "",
    prior_specs: str = "",
    open_questions: str = "",
) -> str:
    """Assemble round responses into the structured user-message payload for synthesis.

    Args:
        question: Dict with 'title' and 'body' keys.
        round_responses: Maps round_label → {agent_key: response_text}.
        round_labels: Ordered list of round names (e.g. ['propose', 'critique', 'evaluate']).
        decisions: Pre-existing decisions from the brief (optional).
        prior_specs: Design docs from earlier questions in the session (optional).
        open_questions: Unresolved open items from prior design docs (optional).

    Returns:
        Formatted string ready to send as the user message to the synthesis Claude call.
    """
    parts: list[str] = []
    parts.append(f"# Design Question: {question['title']}\n\n## The Question\n\n{question['body']}")

    if decisions:
        parts.append(f"## Prior Decisions (from brief)\n\n{decisions}")

    if prior_specs:
        parts.append(f"## Prior Design Docs\n\n{prior_specs}")

    if open_questions:
        parts.append(
            f"## Unresolved Open Questions from Prior Docs\n\n"
            f"Resolve any of these that this discussion addresses:\n\n{open_questions}"
        )

    for round_name in round_labels:
        responses = round_responses.get(round_name, {})
        label = "COUNTER-PROPOSAL" if round_name == "counter" else round_name.upper()
        section = f"## Round: {label}\n\n"
        for agent_key, response in responses.items():
            section += f"### {agent_key}\n\n{response}\n\n"
        parts.append(section.rstrip())

    parts.append(
        "Synthesize into a single design doc. No code. Focus on behavior and rules.\n\n"
        "IMPORTANT: Output ONLY the design doc. Start with '## Decisions'. "
        "Do not request file permissions, describe what you would write, or add any "
        "meta-commentary before or after the document."
    )

    return "\n\n".join(parts)


async def synthesize(
    question: dict,
    round_responses: dict[str, dict[str, str]],
    round_labels: list[str],
    system_prompt: str,
    timeout: int,
    decisions: str = "",
    prior_specs: str = "",
    open_questions: str = "",
) -> str:
    """Call Claude to synthesize round responses into a design document.

    Args:
        question: Dict with 'title' and 'body' keys.
        round_responses: Maps round_label → {agent_key: response_text}.
        round_labels: Ordered list of round names.
        system_prompt: The synthesis system prompt (identity/instructions for the moderator).
        timeout: Seconds to wait for Claude response.
        decisions: Pre-existing decisions from the brief (optional).
        prior_specs: Prior question design docs for context chaining (optional).
        open_questions: Unresolved open items from prior docs (optional).

    Returns:
        Design document text from Claude.

    Raises:
        RuntimeError: If synthesis output is empty or too short to be useful (< 50 chars).
    """
    synth_input = build_synthesis_input(
        question, round_responses, round_labels, decisions, prior_specs, open_questions
    )
    result = await run_claude_async(system_prompt, synth_input, timeout=timeout)
    if result and is_error_response(result):
        raise RuntimeError(f"Synthesis Claude call failed: {result}")
    if not result or len(result.strip()) < _MIN_SYNTHESIS_LENGTH:
        raise RuntimeError(
            f"Synthesis produced empty/minimal output ({len(result or '')} chars)"
        )
    return result
