# What's in the Discussion and DiscussionRound state?

*Generated: 2026-03-17 23:24 | Question 3 | 133s | Mode: bigsmall*

## Decisions

### D4: Discussion State Fields

**Status:** Agreed

Discussion state persists across all rounds for the lifetime of a discussion. Three fields, each with exactly one writer.

| Field | Type | Writer | Behavior |
|---|---|---|---|
| `phase` | string enum | Orchestrator phase transition engine | Set on discussion creation. Updated when phase transition criteria are met (turn count thresholds, decision count thresholds, or explicit facilitator advancement). The curator uses this to select the prompt template and curation strategy -- brainstorm phase keeps exploratory ideas in context, specify phase favors converged positions, review phase surfaces artifacts for validation. |
| `committed_decisions[]` | array of `{id, statement, confidence, round_committed, participating_agents[]}` | Written when agents reach explicit consensus above a confidence threshold | Injected verbatim into every agent's situation block. Never curated away, never summarized, never dropped by archival threshold. These are ground truth. Once committed, agents cannot relitigate -- the curator treats them as fixed context. Decisions are the primary mechanism by which overnight runs produce forward progress rather than circular debate. |
| `artifact_registry{}` | map of `{artifact_id -> {type, version, round_created, producing_agent, summary}}` | Written during specify and review phases when agents produce specs, PRDs, or architecture docs | Referenced by ID in agent context. Full artifact content is never injected into the situation block. When an agent needs to reference an artifact, the curator includes the summary line; the agent can request full content through a tool call. This keeps artifact-heavy phases from blowing the context budget. |

**What does NOT live here:**

- **Ideas and stances.** These live on agent save files. Each agent owns their ideas with magnitudes and their stances with magnitudes. The curator reads agent save files directly during D1 step 4. Storing a global `active_ideas[]` on Discussion creates two sources of truth -- when an agent's magnitude disagrees with the Discussion-level magnitude, there is no canonical answer. One writer per field means ideas belong to agents.

- **Open tensions.** Tensions are what BackgroundAgents discover by reading agent save files and message history. Pre-computing them into a stored field means maintaining cache invalidation logic (what removes a tension? when is it stale?) that runs unattended at 3am. BackgroundAgents are better at detecting tensions than a rule-based field updater. Let them do their job.

- **Topic heat / momentum.** These are derived metrics computed at point of use. The curator can count mention frequency from message logs when it needs to weight topics. Storing derived state means staleness bugs with no one watching.

- **Drift events.** These fire between rounds (D1 step 2 timing). They are generated transiently, consumed during curation (D1 step 4), then discarded. They do not need persistent storage. If a drift event matters, its effects are already reflected in the agent save files that the curator reads.

---

### D5: DiscussionRound State Fields

**Status:** Agreed

DiscussionRound state is created fresh at round initialization and destroyed on round reset. Three fields.

| Field | Type | Writer | Behavior |
|---|---|---|---|
| `round_number` | integer | Orchestrator, set at initialization | Provides temporal grounding. Injected into the situation block so agents understand pacing ("round 4 of brainstorm -- time pressure is real"). The orchestrator also uses this for phase transition checks that depend on minimum round counts. Agents see this number but do not control it. |
| `message_log[]` | array of `{agent_id, team, content, turn_index}` | Raw append on each cross-team message | This IS the mid-round context per D3. No curation, no threading, no transformation. Messages append and agents see the raw log. Threading and topic grouping are curator presentation concerns applied only at round boundaries, never stored as state. Agenda declarations from the opening prompt are simply the first entries in this log -- they are not duplicated into a separate field. |
| `round_summary` | string | Single LLM call at round close | Generated after the last turn of the round. Feeds directly into each agent's save file as the "what happened last round from your perspective" narrative (personalized per agent by the save-file writer). The curator for the next round uses this as its primary input alongside agent save files. This is the bridge between ephemeral round state and persistent agent memory. |

**What does NOT live here:**

- **Turn count.** The orchestrator tracks this internally to enforce round length limits. It is not state that influences agent context or curation. It is an orchestrator-internal counter, not a field on the DiscussionRound entity.

- **Agenda declarations.** These are the first entries in `message_log[]`. Storing them separately duplicates data and creates ambiguity about which version is canonical if an agent's opening statement is edited or re-curated.

- **Active threads.** Threading is a presentation concern. The message log is flat. If the curator wants to group messages by topic for the next round's situation block, it does so at curation time by reading the log. Thread structure is not persisted.

- **Surfaced disagreements.** Same reasoning as open tensions on Discussion -- derived at point of use by BackgroundAgents reading message history, not pre-computed into state.

- **Momentum map.** Mention frequency within a round is derivable from `message_log[]` at round-end processing time. Computing it on demand during the round-end save-file update avoids maintaining a counter that drifts from the actual log.

---

### D6: State Flow Through the Round Lifecycle

**Status:** Agreed

The six fields interact with the D1 initialization sequence as follows:

**Between rounds (D1 steps 1-4):**

1. **Load save file** -- Agent save files are the primary state carrier between rounds. They contain ideas with magnitudes, stances with magnitudes, committed decisions (mirrored from Discussion), and the personalized narrative from last round's `round_summary`.

2. **Run BackgroundAgents** -- Angels read agent save files and the previous round's `message_log[]` (still available before destruction). They mutate agent save files directly. They also read `committed_decisions[]` from Discussion to avoid contradicting settled ground truth. They do not read or write any DiscussionRound field.

3. **Run intra-team talk** -- Teammates compare ideas from their save files. Magnitude adjustments happen on save files. This step reads `committed_decisions[]` to keep intra-team talk grounded in what's already decided.

4. **Curate context** -- The curator reads: `phase` (to select strategy), `committed_decisions[]` (to inject verbatim), `artifact_registry{}` (to include relevant summaries), agent save files (to rank ideas by magnitude against persona-dependent archival thresholds), and the previous `round_summary` (to provide narrative continuity). Output is the ~8-15k situation block.

5. **Assemble prompt** -- Identity block (~2k, static) + curated situation block + task block (~1-2k). Previous DiscussionRound is now destroyed. New DiscussionRound is created with `round_number` set and empty `message_log[]`.

**During the round (D3 behavior):**

- `message_log[]` grows by raw append. No curation runs. No BackgroundAgents run. No state fields are updated except `message_log[]`.
- `phase` may transition if the orchestrator detects transition criteria are met mid-round (rare but possible).
- `committed_decisions[]` may grow if agents reach explicit consensus during the round.
- `artifact_registry{}` may grow if agents produce artifacts during specify/review phases.

**At round close:**

- `round_summary` is generated from `message_log[]` via a single cheap LLM call.
- Agent save files are updated: reflection pre-pass adjusts magnitudes, `round_summary` is personalized into narrative, new ideas and stances from the round are incorporated.
- Mention frequency is derived from `message_log[]` to apply end-of-round magnitude boosts to heavily-discussed ideas (computed, not stored).
- The DiscussionRound is retained only until the next round's BackgroundAgents have finished reading it (D1 step 2), then destroyed.

---

### D7: Design Invariants

**Status:** Agreed

These rules govern all future additions to Discussion or DiscussionRound state:

1. **One writer per field.** If two subsystems need to update the same data, one of them is wrong about where that data lives. Find the canonical owner.

2. **No derived fields in state.** If a value can be computed from existing fields at point of use, compute it. Storing derived values creates cache invalidation obligations that fail silently in unattended runs.

3. **No duplication of agent save file data.** Ideas, stances, and magnitudes belong to agents. Discussion and DiscussionRound reference agents but do not mirror their internal state.

4. **Every field must have a concrete failure mode if removed.** If removing a field produces no observable behavior change, it should not exist. The test: "What breaks tonight at 3am if this field is missing?"

5. **Ephemeral state stays ephemeral.** If a value is needed in the next round, it must flow through an explicit bridge (the `round_summary` to save-file pathway or a write to Discussion-level state). Implicit survival of round-scoped data across round boundaries is a bug.