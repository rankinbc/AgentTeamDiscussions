# Rebuttal Priority (Urgency Meter)

*Implementation spec for dynamic turn ordering based on conversation content*

## Problem

Current `compute_speaking_order()` uses a static formula:
```
score = assertiveness * 0.5 + intensity * 0.3 + stubbornness * 0.2 + jitter
```

This produces roughly the same order every turn. The Adversarial Critic almost always speaks first (highest assertiveness + stubbornness). Conversations feel like serial monologues because agents don't react to being challenged -- they just wait their turn.

## Goal

When Agent A challenges Agent B, Agent B should speak next. Two agents "going at it" should emerge naturally. Other agents queue behind until the confrontation cools.

## Design

### Urgency Meter

Each agent has a `urgency` float (starts at 0.0). Every turn:

1. **Passive growth**: All agents gain `+0.1` urgency (listening builds desire to speak)
2. **Challenge spike**: If the most recent message references an agent by name AND contains disagreement language, that agent gets `+0.5` urgency
3. **Post-speak reset**: After speaking, agent's urgency resets to `0.0`
4. **Decay**: Agents who weren't challenged and didn't speak get their urgency capped at `1.0` (prevents runaway accumulation)

### Speaking Order Formula (replaces current)

```
priority = base_score + urgency

where base_score = assertiveness * 0.3 + intensity * 0.2 + stubbornness * 0.1 + jitter(0.05)
```

Note: base_score weights are reduced from current values because urgency should dominate when active. Jitter is also reduced -- urgency provides the real variation now.

### Challenge Detection

Simple keyword + name matching. No LLM call.

```python
def detect_challenges(message_text: str, speaker_key: str, all_agent_keys: list[str],
                      display_names: dict[str, str]) -> list[str]:
    """Return list of agent keys who were challenged in this message."""

    challenged = []
    text_lower = message_text.lower()

    DISAGREEMENT_SIGNALS = [
        "disagree", "wrong", "no,", "but that", "that won't", "that doesn't",
        "i reject", "flawed", "problem with", "issue with", "pushback",
        "not true", "incorrect", "misses", "ignores", "overlooks",
        "too simplistic", "naive", "won't work", "can't work", "fails to",
        "contradicts", "undermines", "you're missing", "that's not",
    ]

    has_disagreement = any(signal in text_lower for signal in DISAGREEMENT_SIGNALS)
    if not has_disagreement:
        return []

    for key in all_agent_keys:
        if key == speaker_key:
            continue
        # Check for name mention (display name or key variants)
        name = display_names.get(key, key)
        # Extract short name: "The Adversarial Critic (adversarial reviewer)" -> "adversarial critic"
        short_name = name.split("(")[0].replace("The ", "").strip().lower()
        # Also check the key itself: "adversarial_critic" -> "adversarial critic"
        key_name = key.replace("_", " ")

        if short_name in text_lower or key_name in text_lower:
            challenged.append(key)

    return challenged
```

### Not Detecting: Implicit Challenges

If an agent says "that approach won't work" without naming who said it, we do NOT try to figure out who they mean. Only explicit name-mentions trigger urgency spikes. This avoids false positives and keeps the system simple.

Future: could track "last agent who spoke about topic X" and infer challenges, but that requires semantic understanding we don't want to pay for.

### State Management

```python
# In run_conversation(), before the turn loop:
urgency = {key: 0.0 for key in agent_keys}

# Each turn:
# 1. Passive growth for all agents
for key in agent_keys:
    urgency[key] = min(urgency[key] + 0.1, 1.0)

# 2. Compute order using urgency
order = compute_speaking_order_with_urgency(agent_keys, team, urgency)

# 3. After each agent speaks:
#    - Reset speaker's urgency
#    - Detect challenges and spike targets
urgency[speaker_key] = 0.0
challenged = detect_challenges(response, speaker_key, agent_keys, AGENT_DISPLAY_NAMES)
for target in challenged:
    urgency[target] = min(urgency[target] + 0.5, 1.5)  # Can exceed 1.0 cap for challenges
```

### Ego Injection (Emotional Rebuttal Framing)

When an agent's urgency was spiked by a challenge, inject emotional framing scaled by their personality traits. The intensity of the ego response is driven by `assertiveness * bluntness`.

```python
def build_ego_injection(agent_key: str, challenger_name: str, team, ego_score: float) -> str:
    """Build ego-scaled emotional framing for a challenged agent."""
    if ego_score >= 0.7:
        # High ego (e.g. Adversarial Critic: 0.9 * 0.95 = 0.855)
        return (
            f"\n[CHALLENGED] {challenger_name} just called your point wrong. "
            f"You are not going to let that slide. Respond directly -- "
            f"prove your point or make them regret the challenge. "
            f"Do not be diplomatic about it.\n"
        )
    elif ego_score >= 0.4:
        # Medium ego (e.g. Cognitive Architect: 0.7 * 0.5 = 0.35... actually low)
        # Better example: Flow Orchestrator: 0.6 * 0.6 = 0.36... also low
        # Systems Pragmatist: 0.8 * 0.7 = 0.56
        return (
            f"\n[CHALLENGED] {challenger_name} pushed back on your point. "
            f"You feel the need to defend it. Address their criticism directly "
            f"before moving on.\n"
        )
    else:
        # Low ego (e.g. Context Surgeon: 0.4 * 0.3 = 0.12)
        return (
            f"\n[CHALLENGED] {challenger_name} disagreed with you. "
            f"Consider their point carefully before responding.\n"
        )
```

For the **challenger** (the one who started the fight), inject a "don't back down" framing scaled by `stubbornness`:

```python
def build_challenger_injection(agent_key: str, target_name: str, team, stubbornness: float) -> str:
    """Tell the challenger not to back down if the target responds."""
    if stubbornness >= 0.7:
        return (
            f"\n[STATUS] You just challenged {target_name} and you meant it. "
            f"If they push back, do not back down. You must not be disrespected "
            f"without responding.\n"
        )
    elif stubbornness >= 0.4:
        return (
            f"\n[STATUS] You raised a concern with {target_name}. "
            f"Stand by your point if they push back.\n"
        )
    else:
        return ""  # Low stubbornness = flexible, no reinforcement needed
```

This produces natural escalation: high-ego agents get combative when challenged, and high-stubbornness challengers don't back down, creating genuine back-and-forth friction. Low-trait agents stay measured, so not every challenge becomes a fight.

### State: Who Challenged Whom

Track challenge relationships so both sides get appropriate injections:

```python
# After detect_challenges():
challenge_map = {}  # {target_key: challenger_key}
# ... and separately:
active_challengers = {}  # {challenger_key: target_key}

# When building an agent's payload:
if agent_key in challenge_map:
    challenger_key = challenge_map[agent_key]
    ego_score = agent.personality.assertiveness * agent.personality.bluntness
    payload += build_ego_injection(agent_key, display_name_of(challenger_key), team, ego_score)

if agent_key in active_challengers:
    target_key = active_challengers[agent_key]
    payload += build_challenger_injection(agent_key, display_name_of(target_key), team, agent.personality.stubbornness)
```

Challenge state clears after the agent speaks (same as urgency reset).

### UI Updates

The urgency meter should be visible in the web UI:

- Add an urgency bar to each agent card in the roster (like existing trait bars, but dynamic)
- Color: dim when low, amber when building, red when spiked
- Show urgency value in the turn counter display alongside speaking order

### What This Changes

- `compute_speaking_order()` in `run_discussion.py` -- add urgency parameter
- `run_conversation()` in `live_conversation.py` -- add urgency state, challenge detection, rebuttal injection
- `ConvHandler` HTML -- add urgency bar to agent cards, update via SSE events
- New SSE event type: `urgency_update` with per-agent urgency values

### What This Doesn't Change

- Agent system prompts (personality, voice, anti-slop)
- Context compression (still last 5 verbatim, older compressed)
- Convergence detection
- Transcript format

## Edge Cases

- **Multiple challenges in one message**: Both targets get spiked. The one with higher total priority speaks first.
- **Self-reference**: Agent mentions their own name -- ignored (speaker_key check).
- **Challenge + agreement**: "Adversarial Critic is wrong about X but right about Y" -- still triggers spike. The agent can sort out the nuance in their response.
- **Rapid back-and-forth monopoly**: Two agents could theoretically trade challenges forever, locking others out. Mitigated by passive growth -- after enough turns, other agents' urgency naturally reaches competitive levels.
- **First turn**: No history, no challenges. Falls back to base_score ordering (same as current behavior).

## Future: Live Evaluator + Minority Pressure

A background evaluator that tracks consensus could inject minority-status framing into the perspective reminder for agents who hold unpopular positions. Example: "Most agents think you're wrong about X. You need to convince them or concede." This would combine the Live Evaluator concept (agent-behavior-mechanisms.md lines 138-145) with ego injection -- agents in the minority get pressure to either fight harder or change their mind, preventing silent dissent from evaporating.

This requires:
- A consensus tracker (what positions have majority support)
- Per-agent position tracking (what each agent has argued for)
- Injection into `build_perspective_reminder()` with the minority framing

Deferred until the base urgency/ego system is validated.

## Success Criteria

1. When Agent A explicitly challenges Agent B by name, Agent B speaks next (or within next 2 speakers)
2. Two-agent confrontations emerge and persist for 2-4 exchanges before others break in
3. Agents who haven't spoken in many turns eventually get a turn via passive growth
4. The UI shows urgency meters that visibly spike and decay
