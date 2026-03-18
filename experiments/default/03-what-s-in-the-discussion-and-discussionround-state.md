# What's in the Discussion and DiscussionRound state?

*Generated: 2026-03-17 22:34 | Question 3 | 149s | Mode: default*

I don't have write access to the docs directory, so I'll present the synthesized design document here for you to place. Here's the complete spec:

---

# Discussion and DiscussionRound State

**Status:** Draft
**Source:** Design discussion (Propose/Critique/Evaluate)
**Last Updated:** 2026-03-17

---

## Overview

The system maintains two levels of state that frame every agent interaction. **Discussion** state persists across the entire multi-round conversation. **DiscussionRound** state is created fresh at round-open and destroyed on reset. Together they form the container that all agent-level state (ideas, stances, magnitudes) floats within.

Every field exists to serve one purpose: help agents make better contributions next turn. If a field doesn't change what an agent says, it doesn't belong here.

---

## Discussion State (Persistent)

Lives for the entire discussion session. Survives round resets. Updated incrementally as the conversation progresses.

### Fields

| Field | Type | Updated By | How It Flows Into Agent Context |
|---|---|---|---|
| `phase` | enum: brainstorm, refine, specify, review | Orchestrator, when transition criteria are met | Included in the Situation block. Gates what agents are asked to do -- brainstorm rounds don't ask for spec language, review rounds don't solicit new ideas. |
| `active_decisions` | list of {id, description, status, confidence} | Agents via explicit commit action; orchestrator marks resolved or reopened | Curated into the Situation block. Agents see what's decided, what's open, and what's been reopened. Status lifecycle: proposed -> debated -> committed -> reopened. |
| `unresolved_tensions` | list of {id, parties[], description, magnitude} | Orchestrator extracts from transcript when agents hold opposing stances | Fed to BackgroundAgents for synthesis opportunities. Surfaced to agents in Situation block only if magnitude stays high across multiple turns. Low-magnitude tensions are omitted to save context budget. |
| `artifact_registry` | list of {id, type, version, phase_created} | MCP server logs on artifact creation; orchestrator increments version | Agents see artifact existence and version number, never full content unless explicitly requested. Prevents context bloat from inlining specs. |
| `round_count` | int | Orchestrator increments at round-open | Used in decay calculations (magnitudes drift toward zero over rounds) and phase transition rules (minimum rounds before transition). Not prominently displayed to agents but available. |
| `rejected_ideas` | list of {id, round_rejected, reason_summary} | Orchestrator logs when an idea is explicitly argued down and no agent defends it | Prevents zombie ideas. BackgroundAgents check this list before planting synthesized ideas -- if the room already killed it, don't replant it. Not surfaced to agents directly (they already rejected it), but available to BackgroundAgents and diagnostics. |

### Behavioral Rules

**`phase` transition:** The orchestrator evaluates transition criteria at the end of each round. Criteria are defined in `phases.yaml` and may include: minimum round count, percentage of active decisions committed, artifact production thresholds. Transitions are one-directional in V1 (no reverting from refine to brainstorm).

**`active_decisions` lifecycle:** A decision starts as `proposed` when an agent explicitly frames something as a decision point. It moves to `debated` when multiple agents take stances on it. It becomes `committed` when participating agents converge (stance magnitudes align) or when a supermajority threshold is met. It can be `reopened` if a BackgroundAgent plants contradictory evidence or a new tension emerges that undermines the basis for the decision. Reopening resets its confidence score.

**`rejected_ideas` vs. archived ideas:** These are different. An archived idea fell below an agent's magnitude threshold through decay and neglect -- it faded. A rejected idea was actively argued against and lost. Archived ideas can be replanted by BackgroundAgents. Rejected ideas cannot (without explicit new evidence that wasn't available when the rejection occurred).

---

## DiscussionRound State (Ephemeral)

Created fresh at round-open. Destroyed on round reset. Tracks the dynamics of a single round in progress.

### Fields

| Field | Type | Updated By | How It Flows Into Agent Context |
|---|---|---|---|
| `turn_order` | list of agent_ids | Orchestrator sets at round-open (rotation with priority bumps for agents holding high-magnitude unresolved tensions) | Each agent knows the full speaking sequence. Prevents cross-talk and lets agents anticipate who follows them. |
| `turn_count` | int | Orchestrator increments after each agent turn | Caps round length. When turn_count approaches the configured maximum, the orchestrator injects wind-down language into the Task block ("this round is wrapping up -- commit or table"). |
| `heat_map` | dict {topic_id: float} | Orchestrator recalculates after each turn. Aggregation: count of substantive mentions weighted by the mentioning agent's stance/idea magnitude on that topic. | Drives the context curator's token allocation. Hot topics get more detailed summaries in the Situation block; cold topics get one-line references or are omitted entirely. Agents never see the raw heat_map numbers. |
| `surfaced_ideas` | dict {idea_id: int} | Incremented when an agent substantively engages with an idea (not just name-drops it). Orchestrator judges substantiveness by whether the agent took a position or added reasoning. | Weighted count, not binary. A passing mention scores 1. A sustained argument scores higher. The curator uses this to avoid two failure modes: (1) suppressing ideas that were mentioned but never actually discussed, (2) re-introducing ideas that have been thoroughly covered this round. |
| `round_goal` | string | Orchestrator derives from current phase criteria plus gaps identified in Discussion state (e.g., "Three decisions remain open from refine phase -- advance at least one") | Injected into the Task block of every agent's prompt this round. This is the specific question or objective the round should advance. Distinct from phase-level goals. |
| `stalled_turns` | int | Orchestrator increments when a turn produces no magnitude changes across any agent's ideas or stances and no new ideas are introduced. Resets to zero on any magnitude change or new idea. | Not shown to agents. Triggers BackgroundAgent intervention when it crosses a configurable threshold (e.g., 3 consecutive stalled turns). Replaces the proposed `entropy` and `momentum` fields -- it's observable, cheap to compute, and directly actionable. |

### Behavioral Rules

**`heat_map` aggregation:** The formula is `sum(mention_weight * mentioning_agent_magnitude_on_topic)` per topic. A mention by an agent who holds a high-magnitude stance on the topic contributes more heat than a mention by an agent with low engagement. This prevents a single prolific but low-conviction agent from dominating the heat map.

**`surfaced_ideas` and curator interaction:** The curator receives the surfaced_ideas dict and uses it to modulate the Situation block. Ideas with high surfaced counts get compressed summaries ("already discussed extensively this round -- positions are X, Y, Z"). Ideas with surfaced count of 1 get flagged as "raised but not yet discussed." Ideas with surfaced count of 0 are eligible for full introduction if their magnitude warrants it.

**`stalled_turns` thresholds:** Configurable per phase. Brainstorm phase tolerates fewer stalled turns (creative phases should move fast) than review phase (deliberation is expected to slow down). When the threshold is crossed, the orchestrator signals BackgroundAgents to intervene -- plant a new idea, bump a neglected tension's magnitude, or shift a stance to create productive friction.

**Round termination:** A round ends when `turn_count` reaches the configured maximum OR when the orchestrator detects that the `round_goal` has been sufficiently addressed (all agents have spoken to it and positions are clear). Early termination saves token budget.

---

## What Was Cut and Why

| Proposed Field | Verdict | Rationale |
|---|---|---|
| `entropy` (float, magnitude variance across agents) | Cut | Underspecified formula. "Magnitude variance" depends on which magnitudes, what window, how outliers are handled. Untestable -- you can't write a unit test for "does this float feel right." Replaced by `stalled_turns` for the activation-trigger use case. Acceptable as a logged diagnostic for post-session analysis if needed later, but not a state field that drives behavior. |
| `momentum` (float, sentiment direction) | Cut | Requires an LLM call per turn to produce a number that nudges another LLM call (the curator). Paying twice for ambiguity. The curator already reads the transcript -- let it form its own judgment about room direction. |
| `committed_decisions` (flat list) | Replaced by `active_decisions` | Decisions have a lifecycle. A flat list of committed decisions loses the pipeline (proposed/debated/committed/reopened). Agents need to see where to put their energy -- "this is still open" versus "this is settled" versus "this was settled but got reopened." |
| `hot_topics` (ranked list) | Replaced by `heat_map` | Data structures beat summaries. A ranked list loses per-topic granularity. The curator needs to know how hot each topic is relative to others, not just the ordering. |

---

## Interaction Between Levels

The two state levels interact through the round lifecycle:

1. **Round-open:** Discussion state seeds the new DiscussionRound. Phase determines round_goal. Active decisions and unresolved tensions inform turn_order priority. Round state fields initialize to zero/empty.

2. **During round:** DiscussionRound state updates after every turn. heat_map, surfaced_ideas, stalled_turns all change. These influence what the curator puts in each agent's Situation block for their next turn.

3. **Round-close:** DiscussionRound state informs updates to Discussion state. New decisions get added to active_decisions. New tensions get logged. Rejected ideas get recorded. Round_count increments.

4. **Between rounds:** Discussion state is the input to the between-round processes (intra-team talk, BackgroundAgent interventions, thinking routines). DiscussionRound state is discarded. A new DiscussionRound is created at the next round-open with no memory of prior round dynamics -- only what survived into Discussion state and agent save files carries forward.

This separation enforces the design principle that rounds don't continue seamlessly. The reset is real. What matters persists in Discussion state and agent save files. What was ephemeral dies with the round.

---

Want me to save this to `docs/design_specs/` once write permissions are sorted, or do you want to adjust anything first?