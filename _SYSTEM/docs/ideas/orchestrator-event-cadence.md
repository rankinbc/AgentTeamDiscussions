# Orchestrator Event Cadence

*Findings from live agent conversation (2026-03-25) + design direction from Brian*

## Context

The orchestrator drives conversations by building context, managing turn order, and routing messages. Prior to this spec, the orchestrator did very little beyond basic turn management -- agents talked, challenges were detected via string matching, and urgency scores drove speaking order. There was no framework for when the orchestrator should intervene, what it should track, or what post-session artifacts it should produce.

A 25-turn conversation with the beta agents (7 agents) debated the full event architecture. The core design principle that emerged: every orchestrator action must answer "what prompt changes as a result?" Actions that cannot answer that are cut.

---

## Design Principle: Fire-or-Hold

From restaurant expediting: an action fires only when its output would change the next prompt sent to an agent. Convergence detection on a schedule is a thermometer nobody reads. Convergence detection gated on "would I inject a disruption prompt right now?" is a thermostat.

This principle killed multiple candidate actions (see What Was Explicitly Killed).

---

## The Cadence Table

### Per-Turn Actions (every agent message)

#### Pattern-Match Capture

**Trigger:** Every agent message, immediately after response is received.
**Cost:** Zero LLM calls. No model-based inference at this cadence.
**Consumes:** The agent's response, including the structured `---signals---` footer.
**Produces:** Append-only writes to three structures (see below).

#### Three-Tier Detection Hierarchy

**This is a structural requirement, not an implementation detail.** Detection uses three tiers in strict priority order. Each tier has a specific job and activates only when the tier above it fails or does not apply.

**Tier 1 -- Footer fields (primary).** The agent's `---signals---` footer is the authoritative source for all detection. Each footer field maps to a specific detection job:

| Footer Field | Detection Job |
|-------------|--------------|
| `stance` | Concession detection (stance = "agreeing" after prior "challenging" = concession event) and position change detection (any stance shift from prior turn) |
| `changed` | Captures the shift text -- what actually moved in the discussion. Written to concession log verbatim. |
| `key_claim` | Position tracking -- the claim text is the position being defended. Tracked as agent-key + claim-text pair. |
| `propose_takeaway` | Convergence signal (not a detection job -- a state mutation event) |
| `challenge_takeaway` | Challenge signal (state mutation event) |
| `reference_takeaway` | Staleness clock reset (state mutation event) |

Footer fields are parsed first. If all fields are present and valid, regex does not run. This is the expected path for 90%+ of turns.

**Tier 2 -- Keyword regex (fallback).** Activates only when footer fields are missing or malformed (the do-verify failure case from the footer reliability policy). Regex runs on the agent's prose response to extract what the footer should have contained.

Concession detection patterns:
- Explicit concession: "you're right," "I'll concede," "I was wrong," "I hadn't considered," "fair point," "I'll give you that," "I stand corrected"
- Position reversal: "[Agent Name], that's correct" preceded by prior disagreement with that agent
- Qualified concession: "partially right," "right about X but wrong about Y," "concede on this point"

Position change patterns:
- New position: "the answer is," "the right approach is," "what we need is"
- Abandonment: "I'm dropping," "not worth defending," "I've made my case on this"
- Shift: "I've changed my mind," "reconsidering," "updating my position"

Estimated coverage: ~80% of concessions, ~70% of position changes. Missed signals degrade quality (slightly stale counters) but do not corrupt state.

**Tier 3 -- Graph traversal (dropped threads only).** Detects ideas that were raised but never followed up. This is a graph operation, not a text operation -- it reads the position tracker history and identifies claims that appeared once and were never referenced, challenged, or conceded in subsequent turns.

Graph traversal does not detect concessions or position changes. It exclusively serves the dropped-thread list. It runs per-turn but is computationally cheap: a scan of the position tracker entries from the last N turns, checking for unreferenced claims.

**Per-turn footer failure definition:** A footer is malformed if any do-verify field fails validation. Validation rules:

- `stance`: must be one of the values declared in the Section 7 task directive of context-assembly-template.md. The validator must read this enum list from Section 7 at runtime -- never maintain an independent copy, as independently specified lists will drift.
- `changed`: must be a non-empty string, 150 characters max.
- `key_claim`: must be a non-empty string, 150 characters max.
- `confidence`: must be a number between 0.0 and 1.0.
- `ready_to_advance`: must be `true` or `false`.

Any other value -- error text, null, truncated output, empty string, JSON artifacts -- is unparseable and triggers the Tier 2 regex fallback for that turn.

**System-level compliance threshold:** These are two separate requirements and must not be conflated:

1. The per-turn failure definition above determines whether regex activates on *this turn*.
2. The compliance threshold determines whether regex is load-bearing *system-wide*.

If footer parse failure rate exceeds 15% of turns over a session (measured by the orchestrator), flag a footer-compliance alert in the Morning Brief System Alerts section. Above 15% failure, regex is load-bearing infrastructure and the pattern list needs investment. Below 5% failure, regex is vestigial and could be simplified. Between 5-15%, regex is a healthy fallback operating as designed.

#### Detection Outputs

The three tiers feed the same three append-only structures:

1. **Concession log** -- Detected via `stance` + `changed` footer fields (Tier 1), or linguistic fingerprints (Tier 2). Each entry: agent key, turn number, concession text (from `changed` field or regex-extracted phrase), and detection tier used.

2. **Position tracker** -- Updated via `key_claim` footer field (Tier 1), or keyword patterns (Tier 2). Each entry: agent key, turn number, claim text, stance. Tracked as agent-key + claim-text pairs.

3. **Dropped-thread list** -- Detected via graph traversal of position tracker history (Tier 3 only). Each entry: claim text, proposing agent, turn proposed, turns since last reference.

**Implementation constraint:** Writes are append-only. No re-evaluation, no merging, no scan operations beyond the Tier 3 graph check. This keeps per-turn cost near zero.

#### Counter Increment

**Trigger:** After pattern-match capture completes.
**Cost:** Zero. Integer arithmetic.
**Consumes:** Capture output from current turn.
**Produces:** Updated values for two counters:

1. **Concession rate** -- Rolling window (last N turns, N configurable) of concession events divided by total turns. A rate above zero means positions are still shifting.

2. **Distinct position count** -- Number of unique positions being actively defended. Declining count signals convergence; stable count signals either productive disagreement or stagnation (disambiguated by concession rate).

---

### Periodic Actions (every N turns)

#### Composite Threshold Check

**Trigger:** Automatic after every N turns (N=7 starting value, YAML-configurable).
**Cost:** Zero LLM calls. Comparison of counter values against configured thresholds.
**Consumes:** Concession rate + position count counters.
**Produces:** One of three signals:

| Concession Rate | Position Count | Signal | Action |
|----------------|---------------|--------|--------|
| Below threshold | Stable for M turns | **Stagnation** | Disruption injection |
| Nonzero | Declining | **Convergence** | Phase transition |
| Any | Any (neither threshold crossed for N turns) | **Dead zone** | Timeout injection |

All thresholds are YAML-configurable. Starting values for experimentation:
- Stagnation: concession rate < 10% over last 7 turns AND position count stable for 5 turns
- Convergence: concession rate > 0% AND position count declined by 2+ over last 7 turns
- Dead zone timeout: 7 turns with neither signal firing

#### Disruption Injection (on stagnation signal)

**Trigger:** Composite threshold signals stagnation.
**Cost:** Zero LLM calls. Content is sourced from existing data, not generated.
**Consumes:** Dropped-thread list.
**Produces:** Modified next-agent prompt containing a resurfaced dropped thread.

The injection content is a **callback to unfinished business** -- positions raised but never challenged, concessions that were never followed up. The orchestrator already tracks this in the dropped-thread list. The injection is targeted (grounded in session history) rather than generic (random domain pivots or provocative questions).

From improv Harold structure: dead zones don't get random disruption, they get callbacks to earlier material that was dropped without resolution.

#### Timeout Injection (on dead zone signal)

**Trigger:** Neither stagnation nor convergence signal fires for N consecutive turns.
**Cost:** Zero LLM calls.
**Consumes:** Dropped-thread list.
**Produces:** Callback injection fires unconditionally.

This covers the gap between stagnation and convergence -- moderate concession rate, stable position count, discussion just drifting without triggering either threshold. The timeout is the safety net.

---

### Phase Boundary Actions (on convergence signal)

#### Model Synthesis

**Trigger:** Composite threshold signals convergence.
**Cost:** One LLM call. This is the only LLM call in the cadence outside of agent turns.
**Consumes:** Running summary structures only -- NOT full message history. This constraint is locked: synthesis must read bounded input, not raw history that scales with session length.
**Produces:** Two outputs:

1. **Promoted summary** -- Becomes the briefing context for the next phase. Contains: positions held, concessions made, raised-but-unresolved threads.

2. **Morning Brief draft section** -- The same data formatted for human consumption. This is a promotion, not a fresh computation -- the summary structures already contain Morning Brief content because summary structure = Morning Brief input (design axiom).

**Design axiom:** The orchestrator's running summary structures contain exactly what the Morning Brief reports. If the orchestrator is tracking anything not headed for the Morning Brief, it's waste. Synthesis at phase boundaries is a promotion of existing summaries, not a fresh analysis.

---

### Post-Session Actions (after final turn)

#### Morning Brief Export

**Trigger:** Session end (all turns exhausted or moderator stops the session).
**Cost:** Zero additional LLM calls. The Morning Brief is assembled from summary structures already maintained throughout the session.
**Consumes:** Final state of: concession log, position tracker, dropped-thread list, phase synthesis outputs, confirmed takeaways (if Key Takeaway mechanism is implemented).
**Produces:** The Morning Brief -- the single user-facing artifact.

Morning Brief structure:
1. **Contested takeaways** (if takeaway mechanism active) -- sorted by contestation scalar
2. **Positions held at session end** -- which agents held which positions, with concession history
3. **Concessions made** -- the most valuable signal; explicit position changes with what changed the agent's mind
4. **Raised but unresolved** -- the dropped-thread list promoted to a user-facing section. Ideas that got no traction but weren't refuted. This is the "fossil record" the user scans for overlooked insights.
5. **Tombstones** (if takeaway mechanism active) -- rejected ideas with killing arguments
6. **Session metadata** -- turn count, phase transitions, disruption injections fired, stagnation events

**One data structure, two consumers:** The dropped-thread list serves callback injection during the session and the "raised but unresolved" section of the Morning Brief after the session. No duplication, no extra cost.

---

## What Was Explicitly Killed

These candidate actions were evaluated and rejected:

### Context Relevance Scoring
Scoring which prior messages are most relevant to the current thread, per-turn. **Killed because:** requires an LLM call per-turn to evaluate context, producing a signal that would at best slightly improve which messages get compressed vs kept verbatim. The cost (N LLM calls per session) vastly exceeds the marginal improvement over recency-based compression.

### Diversity Audit
Checking whether agent responses are genuinely distinct or converging into sameness. **Killed because:** model-based evaluation required, per-turn cost, and no defined action the orchestrator takes on the output. If diversity degrades, the anti-slop mechanisms in agent prompts are the correct lever, not an orchestrator intervention.

### Quality Gate on Agent Responses
Evaluating whether an agent's response is substantive enough before adding it to history. **Killed because:** LLM evaluating LLM output per-turn is the most expensive possible cadence action. Low-quality responses are better handled by anti-slop prompt engineering than by a meta-evaluator.

### Participation Rebalancing
Prompting silent agents to speak. **Killed because:** the urgency system already handles this. Agents who haven't spoken accumulate passive urgency and rise in the speaking order naturally.

### Scheduled Rolling Synthesis
Periodic synthesis on a timer (e.g., every 5 turns). **Killed because:** synthesis on a timer wastes tokens when nothing has changed. Synthesis at phase boundaries is free because you're already paying for the context rewrite. Timer-based synthesis produces summaries of conversations that haven't converged yet, which is noise.

### Topic Drift Detection (standalone)
A separate mechanism to detect when conversation wanders from the original question. **Killed because:** the composite threshold check already detects drift indirectly (stable position count + low concession rate = nothing productive happening, which includes drift). A separate drift detector would require an LLM call to compare current discussion to original topic, and the stagnation injection already solves the problem by resurfacing dropped threads.

---

## Cost Profile

| Cadence | Actions | LLM Calls | Token Cost |
|---------|---------|-----------|------------|
| Per-turn (25 turns) | Pattern capture + counter increment | 0 | ~0 (regex only) |
| Every N turns (~3 checks per session) | Threshold check + possible injection | 0 | ~0 (counter comparison + prompt modification) |
| Phase boundary (~2 per session) | Model synthesis | 2 | ~2K tokens input per synthesis (summary structures only) |
| Post-session (once) | Morning Brief export | 0 | ~0 (assembly from existing structures) |
| **Total overhead** | | **2 LLM calls** | **~4K tokens** |

The entire cadence overhead is 2 LLM calls per session beyond the agent turns themselves. All per-turn and periodic actions are zero-cost.

---

## Open Validation Questions

These are not design blockers. They are tuning parameters that can only be answered by running sessions.

- **Does 80% regex coverage produce meaningful callback injections?** The missed 20% means the dropped-thread list may miss subtle concessions. Only answerable by reading overnight transcripts and checking whether the "raised but unresolved" section of the Morning Brief contains useful items.

- **Is N=7 the right threshold window?** For a 15-turn phase, N=7 means stagnation can't trigger until turn 7 at the earliest, leaving an 8-turn window for intervention. May be too tight. YAML-configurable, tune from first overnight run.

- **Does the composite threshold correctly distinguish stagnation from productive disagreement?** The dead-zone timeout covers the gap between the two signals, but may fire too aggressively on sessions that are genuinely exploring slowly. Monitor timeout injection frequency in early runs.

- **Is position-count decline a reliable convergence signal?** The Cognitive Architect flagged that positions consolidating because agents found something compelling (success) and positions consolidating from exhaustion (failure) look identical to the counter. The concession rate disambiguates in theory -- genuine convergence is preceded by concession events, stagnation is not -- but this ordering assumption needs validation.

---

## Relationship to Existing Specs

- **key-takeaway-mechanism.md** -- Confirmed takeaways feed the Morning Brief as structured input. The cadence table's phase-boundary synthesis should incorporate takeaway state into its promoted summary. Tombstones feed the "raised but unresolved" section.

- **turn-anatomy.md** -- Per-turn pattern capture operates on the agent's raw output after it's received but before the next turn's context is built. The capture results (concession, position change, dropped thread) are available for the next turn's context construction.

- **design-decisions.md** -- The "signals alongside content" pattern applies: capture results are orchestrator-internal signals, not visible to agents. Agents see only the prompt modifications that result from threshold-triggered actions (disruption injection, phase transition briefing).

- **agent-behavior-mechanisms.md** -- The concession detection regex list should be informed by the retraction signals already defined ("I retract: [claim X]"). The position tracker aligns with the agent-assigned claim tags described in that spec.

- **rebuttal-priority.md** -- The urgency system continues to operate independently of the cadence table. Challenge detection (per-turn) feeds urgency; the cadence table's periodic actions do not modify urgency directly.
