# What's in the Discussion and DiscussionRound state?

*Generated: 2026-03-17 23:29 | Question 3 | 152s | Mode: angles*

## Decisions

### D1: Store Inputs, Compute Outputs

Fields that are pure functions of other stored fields are methods, not persisted state. `momentum` (ratio of magnitude changes to total magnitude), `tension_scores` (calculated from opposing stance magnitudes), and `drift_from_agenda` (gap between `round_agenda` and `heat_map`) are computed when needed and discarded. Storing derived values creates cache invalidation bugs and staleness. The curator calls these as utility functions at assembly time.

### D2: Discussion State Serves Three Consumers

Discussion state is not a general-purpose record. Every field earns persistence by serving at least one of three consumers:
- **Curator** -- assembling the Situation block for agent prompts
- **BackgroundAgents** -- choosing intervention targets
- **Orchestrator** -- making mechanical sequencing and phase decisions

If a field cannot be traced to a specific consumer's decision or prompt fragment, it does not belong in state.

### D3: Stalled Topics Replace Unresolved Tensions

`stalled_topics` (topic ID + rounds without magnitude movement) is concrete and actionable. BackgroundAgents can target stalled topics without interpretation. A topic evicts from the list when its magnitude moves beyond a threshold OR a decision commits on that topic. Cap at 5 entries, oldest-out, to bound growth.

### D4: Active Topics and Group Direction Vector Are Pipeline Outputs, Not State

Both `active_topics` (aggregate magnitudes per topic) and `group_direction_vector` (mean stance magnitude per topic, per D7) are recalculated at every round boundary from agent states. They exist as pipeline step outputs available to downstream consumers during boundary processing. They are not persisted between boundaries because they would be immediately overwritten.

### D5: Drift Is Computed, Never Stored

The gap between what agents were supposed to discuss (`round_agenda`) and what they actually discussed (`heat_map`) is the drift signal. The curator computes this by comparing the two fields at assembly time. Storing a `drift_from_agenda` float collapses a rich structural comparison into a single number that obscures whether agents wandered to something productive or just lost focus.

### D6: Token Budget Survives at Scale

After 15 rounds with 6 agents: `committed_decisions` at ~50 tokens each (8 decisions = 400 tokens), `stalled_topics` capped at 5 (~100 tokens), `phase` + `round_count` (~50 tokens). Total Discussion state serializes under 600 tokens. The curator consumes this plus agent save files (~3k for 6 agents) plus DiscussionRound state (~300 tokens), totaling ~4k tokens input, well within the curator's context window. Discussion state never competes with the agent's Situation block because the curator mediates -- agents never see raw state.

---

## Discussion State

Persists across rounds. Owned by the orchestrator. Mutated only at round boundaries.

### `phase`

- **Type:** Enum (brainstorm, refine, specify, review)
- **Updated by:** Phase transition engine, evaluated at each round boundary
- **Consumers:** Orchestrator selects the task prompt template. Curator frames urgency and constraints. Phase gates what kinds of moves agents can make (e.g., agents cannot commit decisions during brainstorm).
- **Lifecycle:** Set at discussion start, transitions forward only.

### `committed_decisions`

- **Type:** Append-only list. Each entry: `{decision_text, confidence: float, round_committed: int, contributing_agents: list}`
- **Updated by:** Orchestrator when consensus is detected (configurable threshold on stance magnitude convergence)
- **Consumers:** Curator marks resolved items so agents stop relitigating. Stalled topic eviction checks against this list.
- **Lifecycle:** Append-only. Never pruned. Decisions are the product of the discussion. Growth is bounded by the discussion producing outcomes.

### `stalled_topics`

- **Type:** List of `{topic_id, rounds_without_movement: int}`
- **Updated by:** Orchestrator at each round boundary, diffing topic magnitudes across the current and previous round
- **Consumers:** BackgroundAgents use this as their primary targeting list for interventions (planting ideas, bumping magnitudes). Curator may surface persistent stalls to create urgency.
- **Lifecycle:** A topic enters when its aggregate magnitude changes less than a configurable threshold across a round boundary. A topic evicts when: (a) its magnitude moves beyond the threshold, (b) a decision commits on that topic, or (c) a BackgroundAgent intervenes on it (one round grace period to see if intervention took effect). Capped at 5 entries. When a sixth would be added, the oldest evicts.

### `round_count`

- **Type:** Integer
- **Updated by:** Orchestrator, incremented at each round boundary
- **Consumers:** Curator adjusts urgency framing as rounds accumulate. Phase transition engine uses round count as pressure input. Thinking routine selection may vary by round (e.g., Research is more valuable early, Strategize later).
- **Lifecycle:** Monotonically increasing. Resets only if discussion resets.

---

## Computed at Round Boundary (Not Persisted)

These are produced by pipeline steps and consumed during the same boundary processing. They exist as in-memory values passed between pipeline stages.

### `active_topics`

- **Type:** Map of `{topic_id -> aggregate_magnitude: float}`
- **Computed by:** Aggregating all agents' idea and stance magnitudes per topic after pipeline steps 1-4 complete
- **Consumers:** Curator uses for Situation block assembly. Feeds `group_direction_vector` calculation. Stalled topic detection diffs this against previous round's values.
- **Not persisted because:** Fully derivable from agent states, which are persisted. Recalculated every boundary.

### `group_direction_vector`

- **Type:** Map of `{topic_id -> mean_stance_magnitude: float}`
- **Computed by:** Pipeline Step 4 (per D7). Mean of all agents' stance magnitudes per active topic.
- **Consumers:** Curator uses to signal group consensus or divergence. Tension formula (a utility function) uses to identify productive disagreements.
- **Not persisted because:** Cheap to compute, has a clear invalidation point (every boundary), and would be immediately overwritten.

### `momentum`

- **Type:** Float
- **Computed by:** Utility function. Ratio of total magnitude change across all agents and topics to total magnitude. Calculated from the current round's `heat_map` and the magnitude diffs from pipeline processing.
- **Consumers:** Curator uses to signal "we're stalling" or "things are moving fast" in the Situation block.
- **Not persisted because:** Pure function of other stored/computed values.

### `tension_scores`

- **Type:** Map of `{agent_pair -> float}`
- **Computed by:** Utility function. For each pair of agents, the absolute difference between their stance magnitudes on shared topics, summed.
- **Consumers:** Curator highlights productive disagreements in the Situation block to encourage engagement.
- **Not persisted because:** Pure function of agent stance magnitudes.

### `drift_from_agenda`

- **Type:** Structural comparison (not a single float)
- **Computed by:** Curator at assembly time. Compares `round_agenda` (what was surfaced) against `heat_map` (what was actually discussed).
- **Consumers:** Curator decides whether to re-anchor agents toward the agenda or let productive drift ride.
- **Not persisted because:** Requires interpretation, not just calculation. The curator makes a judgment call, not a threshold check.

---

## DiscussionRound State

Created fresh each round. Ephemeral. Discarded after boundary processing extracts what it needs for Discussion state updates.

### `round_number`

- **Type:** Integer
- **Updated by:** Set at round creation from `Discussion.round_count`
- **Consumers:** Logging and debug correlation. Not directly in agent prompts.

### `speaking_order`

- **Type:** Ordered list of agent IDs
- **Updated by:** Magnitude-weighted random draw at pipeline end (D5). Weight equals the agent's highest unresolved item magnitude. Agents with higher conviction open more often without making order deterministic.
- **Consumers:** Orchestrator uses to sequence turn calls mid-round. Not in agent prompts -- agents do not know the speaking order.

### `turns_taken`

- **Type:** Integer
- **Updated by:** Orchestrator, incremented after each agent turn mid-round
- **Consumers:** Orchestrator enforces round length (configurable max turns). Not in agent prompts directly, but the orchestrator may signal "last turn" to the final speaker.

### `heat_map`

- **Type:** Map of `{topic_id -> mention_count: int}`
- **Updated by:** Orchestrator mid-round, parsed from agent responses. Simple keyword/topic matching against the active topics list.
- **Consumers:** Nothing mid-round (per D2 -- mid-round has no curation or state mutation). At the next round boundary: feeds momentum calculation, stalled topic detection, and drift comparison against `round_agenda`.
- **Why it earns persistence:** Genuinely new information accumulated during the round. Not derivable from any pre-round state. Captures what the conversation actually discussed versus what was planned.

### `round_agenda`

- **Type:** List of `{topic_id, priority: int}`
- **Updated by:** Curator output during prompt assembly. Filtered and prioritized from the computed `active_topics` based on staleness, magnitude, and phase.
- **Consumers:** Curator uses to shape what the Situation block emphasizes for each agent. At next boundary, compared against `heat_map` to detect drift.
- **Why it earns persistence:** Records the curator's editorial judgment about what mattered at round start. This is not re-derivable because the curator's LLM call is non-deterministic.

### `state_diffs`

- **Type:** Ordered list of diffs from pipeline steps
- **Updated by:** Each pipeline step appends its diff (D3)
- **Consumers:** Debug and replay only. Never appears in agent prompts. Enables reordering or dropping pipeline steps without corrupting base state.
- **Lifecycle:** Retained for the session's debug log. Not consumed by any runtime process.

---

## Bidirectional Coupling

The bidirectional relationship between state and conversation operates through two specific channels:

**State shapes conversation:** The curator reads Discussion state (especially `stalled_topics` and `committed_decisions`) and computed values (`active_topics`, `group_direction_vector`, `momentum`) to assemble each agent's Situation block. Agents with high-magnitude items on stalled topics get framing that emphasizes urgency. Agents whose stances align with group direction get framing that signals momentum. The curator's editorial choices determine what each agent cares about entering the round.

**Conversation shapes state:** Mid-round responses are parsed into `heat_map`, which is the only new information generated during a round. At the next boundary, `heat_map` feeds stalled topic detection (a topic discussed heavily but without magnitude movement is stalling differently than one ignored entirely), momentum calculation, and drift analysis. The orchestrator also detects consensus events mid-round that append to `committed_decisions`.

No other coupling exists. Mid-round turns do not mutate Discussion state, trigger BackgroundAgents, or invoke the curator. The boundary carries all complexity (D2).

---

## Eviction and Growth Rules

| Structure | Growth Pattern | Eviction Trigger | Cap |
|---|---|---|---|
| `committed_decisions` | Append-only, ~1-2 per round in later phases | Never evicted | None (bounded by discussion producing outcomes) |
| `stalled_topics` | Enters on low-movement detection | Magnitude moves, decision commits, or BackgroundAgent intervenes | 5 entries, oldest-out |
| `heat_map` | Rebuilt each round | Discarded at round end after boundary processing | Bounded by active topic count |
| `round_agenda` | Rebuilt each round | Discarded at round end after boundary processing | Bounded by active topic count |
| `state_diffs` | Appends per pipeline step | Archived to session log | Bounded by pipeline step count (~6 per round) |