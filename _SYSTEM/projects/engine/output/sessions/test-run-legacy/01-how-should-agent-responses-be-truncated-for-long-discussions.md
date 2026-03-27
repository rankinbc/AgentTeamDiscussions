# How should agent responses be truncated for long discussions?

*Generated: 2026-03-25 12:02 | Question 1 | 158s | Mode: compete*

## Decisions

### Context Strategy: Hybrid Deterministic Core with Structured State Overlay

**Core principle:** Each agent receives the minimum information state required for coherent continuation — not a history replay. The target is *current argumentative position*, not *chronological record*.

---

## Agent Context Composition

Each agent receives exactly four components per turn, in this order:

1. **Session Frame** (~200 tokens, never compressed)
   The original question, constraints, and any pre-committed decisions. Static for the life of the session. Always included verbatim.

2. **Own Position Register** (~50 tokens per claim)
   Extracted claims the agent has previously committed to or conceded, in structured form. Not verbatim prose — conclusions only. Example: `"Claimed: sliding windows cause positional drift (round 3)"` / `"Conceded: full history is not viable at scale (round 5)"`. Maintained per-agent by the orchestrator.

3. **Live Dispute State** (variable, capped at 300 tokens)
   Open claims from other agents that remain unresolved — marked with originating agent and round. Closed or conceded items are dropped from this list, not summarized. The orchestrator maintains one shared dispute register; each agent receives only the open items plus any items they personally closed.

4. **Last Turn Verbatim**
   The immediately preceding turn from each agent, in full. One turn only. This is the response surface — what must be addressed next.

Everything older than the above is dropped. No summarization. No sliding window of arbitrary length.

---

## Orchestrator Responsibilities

The orchestrator — not any agent — owns all state management between turns.

**After each full round, the orchestrator:**
- Parses agent responses for explicit claim assertions (new positions stated) and explicit concessions (prior positions withdrawn or qualified)
- Updates the per-agent Position Register
- Updates the shared Live Dispute register (promoting new claims, retiring conceded ones)
- Computes token budget for the next round's context package

**Parsing approach:** Structured agent output is required. Agent prompts must instruct agents to mark claims and concessions using lightweight delimiters (e.g., `[CLAIM: ...]`, `[CONCEDE: ...]`). The orchestrator extracts these deterministically — no LLM inference call, no regex heuristics on free prose. This is a prompt engineering constraint on agents, not an inference problem on the orchestrator.

**Consensus detection is not implemented.** "Settled ground" synthesis is removed from scope. The closed-claims list in the dispute register is the complete record of convergence. A separate consensus-detection pipeline introduces ambiguous classification with no reliable trigger condition.

---

## Ceiling Protocol

Token budget is computed before each round. Three operating modes:

| Budget State | Behavior |
|---|---|
| < 80% capacity | Normal operation — all four context components included |
| 80–94% capacity | Position Register compressed to claim labels only (no round metadata). Last-turn verbatim truncated to 200 tokens if needed. |
| ≥ 95% capacity | Session halted. Orchestrator runs forced synthesis: concatenates all closed claims into a final convergence summary and writes it to the session artifact. No new agent turns are issued. |

The 95% halt is deterministic and unconditional. There is no graceful degradation past this point — a partial synthesis is better than a crashed context.

---

## What Is Explicitly Out of Scope

- **Rolling summarization of prose:** Introduces a per-turn LLM call, fails silently on hallucinated summaries, adds latency. Not implemented.
- **Multi-turn own-voice buffer (3 turns):** One verbatim last turn is sufficient to prevent self-contradiction within the immediate response. Earlier positions are captured in the Position Register as claims, not prose.
- **Settled-ground paragraph:** Redundant with the closed-claims list and requires consensus detection, which is unspecified. Removed.
- **Variable sliding window by "rounds":** Round length is not constant. Any window defined in rounds produces variable token budgets. Fixed-composition context packages are used instead.

---

## Failure Modes Addressed

| Failure | Mechanism |
|---|---|
| Agent re-proposes a previously conceded claim | Own Position Register contains the concession explicitly; agent sees it every turn |
| Agent contradicts its own current position | Last-turn verbatim included; Position Register reflects committed claims |
| Session crashes at context limit with no output | 95% ceiling halt + forced synthesis fires before overflow |
| Circular discussion producing no new positions | Live Dispute register retires closed claims; agents see only open questions |
| Overnight session produces no usable Morning Brief | Ceiling protocol guarantees a convergence artifact even on forced halt |

---

## User-Visible Quality Criteria

The primary measurement target is Morning Brief quality as rated by the human reviewer — not internal coherence metrics. Implementation of this architecture is justified only if it produces observable improvement on:

- Absence of repeated positions across the Brief
- Absence of self-contradictory agent claims within the same document
- Session completion rate on overnight runs (no crashes, no empty output)

Before adding further sophistication (consensus detection, multi-turn buffers, rolling synthesis), run a comparison: does the Brief read as more novel and actionable than a simple recent-window approach? That measurement gates the next investment decision.