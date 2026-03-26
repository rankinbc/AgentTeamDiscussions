"""Perspective drift detection for agent conversations."""

from agentteam.types import AgentConfig

_AGREEMENT_PHRASES: frozenset[str] = frozenset([
    "i agree", "you're right", "that's correct", "great point",
    "exactly right", "well said", "i concede", "you've convinced me",
    "i was wrong", "you are right",
])

_CAPITULATION_PHRASES: frozenset[str] = frozenset([
    "perhaps you're right", "i'll concede", "i take that back",
    "i withdraw", "you make a good point about", "i'll drop",
    "i abandon", "let's forget my earlier",
])


def _extract_anchor_words(agent: AgentConfig) -> frozenset[str]:
    """Extract content words (len > 3) from drives + pushback_on — identity anchors."""
    words: set[str] = set()
    for item in agent.position.drives + agent.position.pushback_on:
        for word in item.split():
            if len(word) > 3:
                words.add(word.lower().strip(".,;:"))
    return frozenset(words)


def detect_drift(previous_response: str, agent: AgentConfig) -> bool:
    """Detect if an agent has drifted from their assigned role.

    Signals:
    - Signal 1: Agreement phrases without any identity anchor keywords
    - Signal 2: Explicit capitulation phrases (unconditional)

    Returns False when:
    - previous_response is empty
    - Agent has no drives or pushback_on (no anchors to check against)
    - Response contains identity anchor keywords (agent is speaking in character)
    """
    if not previous_response:
        return False

    drives = agent.position.drives
    pushback_on = agent.position.pushback_on

    # No identity anchors — cannot meaningfully detect drift
    if not drives and not pushback_on:
        return False

    lower = previous_response.lower()
    anchor_words = _extract_anchor_words(agent)

    # If all position words are too short to extract (e.g. ["API", "UX"]), treat as no-anchor case
    if not anchor_words:
        return False

    has_anchors = any(word in lower for word in anchor_words)

    # Signal 1: Agreement without identity anchors
    if any(phrase in lower for phrase in _AGREEMENT_PHRASES) and not has_anchors:
        return True

    # Signal 2: Explicit capitulation — suppressed if agent is still anchored in their position
    if any(phrase in lower for phrase in _CAPITULATION_PHRASES) and not has_anchors:
        return True

    return False


def build_drift_reminder(agent: AgentConfig) -> str:
    """Build a targeted perspective reminder for a drifting agent.

    Returns a reminder < 100 words specifying the agent's role, drives,
    and pushback items.
    """
    pos = agent.position
    drives_text = "; ".join(pos.drives) if pos.drives else "your stated priorities"
    pushback_text = "; ".join(pos.pushback_on) if pos.pushback_on else "overreach and vagueness"
    return (
        f"[DRIFT ALERT: Remember, you are {pos.role}. "
        f"Your drives are: {drives_text}. "
        f"Push back on: {pushback_text}.]"
    )
