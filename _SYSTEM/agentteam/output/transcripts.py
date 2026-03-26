"""Per-round transcript formatting and writing."""

from pathlib import Path

from agentteam.types import TeamConfig
from agentteam.utils.io import write_atomic


def format_round_transcript(
    question: dict,
    round_num: int,
    round_name: str,
    responses: dict[str, str],
    team: TeamConfig,
) -> str:
    """Format one round's responses as a readable markdown transcript.

    Args:
        question: Dict with 'title' and 'body' keys.
        round_num: 1-based position of this round in the session.
        round_name: Round name (e.g. 'propose', 'critique', 'counter').
        responses: Maps agent_key → response_text for this round.
        team: TeamConfig used to resolve agent display name and role.

    Returns:
        Formatted markdown string.
    """
    label = "COUNTER-PROPOSAL" if round_name == "counter" else round_name.upper()
    parts: list[str] = [
        f"# Round {round_num}: {label}",
        "",
        f"*Question: {question['title']}*",
        "",
    ]

    for agent_key, response in responses.items():
        if agent_key in team.agents:
            agent = team.agents[agent_key]
            heading = f"## {agent.name} ({agent.position.role})"
        else:
            heading = f"## {agent_key}"
        parts.append(heading)
        parts.append("")
        parts.append(response)
        parts.append("")

    return "\n".join(parts)


def write_round_transcripts(
    question_dir: Path,
    round_responses: dict[str, dict[str, str]],
    round_labels: list[str],
    question: dict,
    team: TeamConfig,
) -> list[Path]:
    """Write per-round transcript files to question_dir.

    Files are named: round-{N}-{round_name}.md, where N is the 1-based
    position in round_labels.

    Args:
        question_dir: Existing per-question output directory.
        round_responses: Maps round_name → {agent_key: response_text}.
        round_labels: Ordered list of round names.
        question: Dict with 'title' and 'body' keys.
        team: TeamConfig for agent display names and roles.

    Returns:
        List of Path objects for each written file.

    Raises:
        ValueError: If question_dir does not exist.
    """
    if not question_dir.exists():
        raise ValueError(f"question_dir does not exist: {question_dir}")

    written: list[Path] = []
    for round_num, round_name in enumerate(round_labels, start=1):
        responses = round_responses.get(round_name, {})
        content = format_round_transcript(question, round_num, round_name, responses, team)
        path = question_dir / f"round-{round_num}-{round_name}.md"
        write_atomic(path, content)
        written.append(path)

    return written
