# Pre-mortem subject: How should phase transitions be triggered?

The V2 roadmap plans a Phase System (Brainstorm -> Refine -> Specify -> Review). Open question: should transitions be time-based, convergence-based, round-count based, or something else?

## Current engine facts (as of 2026-10-05, verified against the code)

- C# .NET 8 engine shells out to `claude -p` for every agent turn; one system prompt per persona, built from YAML.
- A session runs a list of questions. Each question runs fixed rounds from a mode (e.g. propose -> critique -> evaluate),
  agents speak sequentially within a round, then one synthesis call writes a design doc.
- Between rounds, agents only see earlier rounds' "## Position Summary" blocks (3 sentences each); within a round they
  see earlier speakers in full.
- Context per turn: persona reminder, focus lens, role overlay, brief context, decided items + decisions ledger,
  headings of the previous design doc, open questions carried from earlier docs, discussion so far, the question.
  A budget enforcer trims unprotected sections when a payload exceeds ~10k tokens.
- The decisions ledger (DECIDED / CONTESTED / OPEN lines per question) chains forward to later questions.
  Until 2026-10-05 the synthesis template was never rendered, so no session before then produced a real ledger.
- An Evaluator exists: after a session it scores design docs (7 dimensions) and transcripts (10 dimensions) 1-10 via an
  LLM judge and writes a report. Nothing reads those scores back; persona YAML is static and edited by hand.
- There is no phase system, no moderator input channel, no research engine, and no live/rolling synthesis in the
  running code. Templates for rolling synthesis exist but are unused.
- One developer, solo project. Sessions are run occasionally, not in production. 17 sessions exist on disk.


---

# Source document: docs/v2/ROADMAP.md

# V2 Roadmap

## Confirmed V2 Features (from PRD Growth Section)

These are the features explicitly scoped as post-MVP growth:

1. **Phase System** — Brainstorm → Refine → Specify → Review with automatic transitions
2. **Moderator Input** — Live steering via HTTP during discussions
3. **Dynamic Turn Ordering** — Rebuttal priority / urgency meter
4. **Key Takeaway Mechanism** — Convergence detection and voting
5. **Evaluation Engine** — Rubric scoring against design doc quality dimensions
6. **Multiple Output Artifact Types** — PRD, architecture doc, user stories
7. **Research Engine** — External data gathering during discussions

## Critical Path (from Agent Panel Analysis)

Recommended build order based on dependency analysis and user value:

1. **Blind Proposals** (1-2 days) — Suppress prior context in propose phase. Highest immediate user value.
2. **Manifest Versioning** (0.5 day) — Co-deliver with blind proposals for schema evolution.
3. **Phase System** (2-3 days) — Metadata labeling, phase-specific prompt injection, transition logic. Foundational infrastructure for most V2 features.
4. **Key Takeaways** (1 day) — Extraction at phase boundaries.
5. **Stale Detection** (2 days) — Compare outputs across phase boundaries for repetition signals.
6. **Anti-Sycophancy Detection** (2 days) — Measure blind vs revealed position drift (measurement only).
7. **BIT System** (parallel track) — Personality dimensions, measurable independently.

Key insight: Start with blind proposals (changes what user reads immediately) rather than phases (invisible infrastructure). Phases enable blind proposals to be cleaner, but blind proposals work without phases.

## Vision (Post-V2)

- **Team Configuration Layer** — Multi-team with spokesperson/internal deliberation
- **MCP Message Broker** — Cross-team communication channel
- **Full Magnitude System** — Ideas/stances tracking and BackgroundAgents
- **Intra-team Deliberation** — Between rounds
- **Context Management** — Prior sessions, RAG, research findings
- **Web UI** — Session monitoring and artifact browsing
- **Agent Library** — Sharable team configurations

## Idea Index

| Idea | Summary | Scope |
|------|---------|-------|
| [entity-model.md](ideas/entity-model.md) | Magnitude-based ideas/stances, BackgroundAgents, complex entity persistence | Vision |
| [orchestrator-event-cadence.md](ideas/orchestrator-event-cadence.md) | Per-turn convergence detection and event-driven orchestration | V2 |
| [key-takeaway-mechanism.md](ideas/key-takeaway-mechanism.md) | Convergence voting system for extracting key insights | V2 |
| [rebuttal-priority.md](ideas/rebuttal-priority.md) | Dynamic turn ordering based on conversation content | V2 |
| [moderator-input.md](ideas/moderator-input.md) | Live steering via HTTP during discussions | V2 |
| [phase-dynamics.md](ideas/phase-dynamics.md) | Per-phase personality weighting in creativity engine | V2 |
| [session-platform.md](ideas/session-platform.md) | Agent library, session-as-package, management layer | Vision |
| [research-scope-controls.md](ideas/research-scope-controls.md) | 4-layer research cost control for external data gathering | V2 |
| [agent-behavior-philosophy.md](ideas/agent-behavior-philosophy.md) | Ego simulation, behavioral prescription mechanisms | V2 |
| [implementation-gaps.md](ideas/implementation-gaps.md) | V2+ gaps identified during spec review | V2 |
| [team-configuration.md](ideas/team-configuration.md) | Multi-team YAML surface with spokesperson/deliberation | Vision |
| [mcp-message-broker.md](ideas/mcp-message-broker.md) | Cross-team communication backbone via MCP | Vision |
| [research-engine.md](ideas/research-engine.md) | External knowledge gathering during discussions | V2 |
| [agent-identity-and-resolution.md](ideas/agent-identity-and-resolution.md) | GUID-based agent identity, multi-source resolution, session snapshots | V2 |

## Open Questions (from V1 Spec Gaps Relevant to V2)

- How should phase transitions be triggered? (time-based, convergence-based, round-count?)
- How does the evaluation engine feed back into agent behavior for subsequent sessions?
- What's the boundary between moderator input and phase system auto-transitions?
- How do research engine results integrate into the context assembly pipeline?

---

# Source document: docs/v2/ideas/phase-dynamics.md

# Phase Dynamics -- How the Creativity Engine Changes Per Phase

**Status:** Draft - discovered during PRD creation
**Date:** 2026-03-17

---

## Concept

The creativity engine isn't static. Each Phase activates different personality weightings, bench configurations, communication modes, technique categories, and anti-slop mechanisms. The system shifts from maximum divergence (brainstorm) through progressive convergence (refine, specify) to adversarial validation (review).

---

## Phase Configurations

### Brainstorm Phase

**Goal:** Maximum idea quantity and diversity. Push past obvious ideas into genuinely novel territory.

| Dimension | Setting |
|---|---|
| Communication mode | YES-AND -- build, extend, never critique |
| Active technique categories | creative, wild, theatrical, biomimetic, quantum, cultural |
| Bench priority | High creativity-temperature agents, Connector, Anarchist, Visionary archetypes |
| Anti-slop emphasis | Domain pivot triggers, convergence suppression, uncomfortable idea quota |
| Deliberation profile | Short internal turns, high volume, breadth over depth |
| Phase exit gate | Minimum Idea count (configurable, default 50+), domain diversity threshold |
| Agreement tax | Maximum -- pure agreement costs a turn |
| Muse activity | High -- frequent random stimuli and provocations |
| Devil's advocate duty | Active, rotating every 5 turns |

### Refine Phase

**Goal:** Challenge assumptions, find gaps, stress-test the best ideas from brainstorm. Kill weak ideas. Strengthen strong ones.

| Dimension | Setting |
|---|---|
| Communication mode | CHALLENGE -- poke holes, question assumptions, demand evidence |
| Active technique categories | deep, structured, risk analysis |
| Bench priority | Challenger, Detective, Skeptic archetypes. Customer and Competitor positions amplified. |
| Anti-slop emphasis | Perspective enforcement, novelty scoring (but applied to critiques -- are critiques diverse or all the same?) |
| Deliberation profile | Longer internal turns, depth over breadth, position papers for significant disagreements |
| Phase exit gate | All major Ideas have been challenged and either defended or killed. Disagreement queue below threshold. |
| Agreement tax | Moderate -- agreement is fine if paired with "and here's the remaining risk" |
| Muse activity | Low -- focused analysis, not random stimulation |
| Devil's advocate duty | Not needed -- the Phase itself is adversarial |

### Specify Phase

**Goal:** Pin down requirements and acceptance criteria for surviving ideas. Precision over creativity. The output of this phase should be implementable.

| Dimension | Setting |
|---|---|
| Communication mode | SPECIFY -- define exactly, accept criteria, edge cases, no ambiguity |
| Active technique categories | structured (Decision Tree, Solution Matrix, Morphological Analysis) |
| Bench priority | Systematic cognitive style, Builder position, high attention span agents |
| Anti-slop emphasis | Perspective enforcement (Builder position asking "what exactly happens when...?"), silence as signal for non-relevant agents |
| Deliberation profile | Long internal turns, completeness checks, each Decision logged with full provenance |
| Phase exit gate | All requirements have acceptance criteria. Builder agent confirms specs are implementable. No undefined edge cases. |
| Agreement tax | Low -- agreement on specifications is productive |
| Muse activity | Off -- this is not the time for random stimulation |
| Devil's advocate duty | Off -- replaced by Builder agent's natural "is this buildable?" pressure |

### Review Phase

**Goal:** Adversarial validation. Find every weakness in the specs. The Competitor, Skeptic, and Regulator positions are most active.

| Dimension | Setting |
|---|---|
| Communication mode | ADVERSARIAL -- actively try to break the specs, find contradictions, missing pieces |
| Active technique categories | risk, competitive, deep (Failure Analysis, Chaos Engineering, Pre-mortem) |
| Bench priority | Competitor, Regulator, Skeptic, Support/Ops positions. High stubbornness agents. |
| Anti-slop emphasis | Surprise audits on review quality (are reviewers finding real issues or surface-level nits?) |
| Deliberation profile | Medium internal turns, focused on specific weaknesses |
| Phase exit gate | Spec validation gate passes. All critical issues resolved. Agreement score above threshold. |
| Agreement tax | Maximum for the reviewing agents -- "it's fine" is not acceptable |
| Muse activity | Off |
| Devil's advocate duty | Not needed -- entire Phase is adversarial |

---

## Phase Transition Dynamics

When transitioning between phases:
1. BackgroundAgent (Weaver) generates a Briefing summarizing the outgoing phase
2. AgentMinds get adjusted -- Idea magnitudes recalculated based on phase outcomes
3. Bench rotation happens -- agents appropriate for the new phase come in
4. Communication mode switches (the orchestrator's per-turn prompt changes)
5. Anti-slop mechanism weights adjust
6. Phase-specific technique categories activate

---

# Source document: docs/v2/ideas/orchestrator-event-cadence.md

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
