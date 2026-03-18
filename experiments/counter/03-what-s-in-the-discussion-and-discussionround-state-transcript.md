# Transcript: What's in the Discussion and DiscussionRound state?

*Generated: 2026-03-17 22:40*

## Round: PROPOSE

### The Cognitive Architect (creativity engine designer)

## Decisions

**Discussion state** (persists across the entire conversation):

| Field | Type | Updated by | Influences |
|---|---|---|---|
| `phase` | enum | Orchestrator (transition criteria met) | Layer 2 task prompt — controls diverge/converge instructions |
| `round_number` | int | Orchestrator (increment on reset) | Layer 2 task prompt, delta computation baseline |
| `active_ideas` | map{id → IdeaRecord} | Agents (propose), BackgroundAgents (plant), archival sweep (remove) | Curator pulls cross-team idea positions into Layer 1 |
| `committed_decisions` | list[Decision] | Orchestrator (when both teams ratify) | Ground truth in Layer 0 save file — agents don't re-litigate these |
| `tension_map` | map{idea_pair → float} | Computed after each round from stance divergence | Curator flags high-tension pairs in Layer 1 as unresolved friction |
| `artifact_refs` | list[ArtifactRef] | Orchestrator (when phase produces spec/PRD) | Layer 2 can reference "draft spec v2 exists" without inlining it |

**DiscussionRound state** (scoped to one round, discarded on reset):

| Field | Type | Updated by | Influences |
|---|---|---|---|
| `turn_count` | int | Orchestrator | Controls when round ends |
| `speaker_order` | list[agent_id] | Orchestrator (determined at round-open) | Who speaks next — not in agent context, just scheduling |
| `momentum` | map{idea_id → float} | Computed from mention frequency + stance shifts within round | Between-round thinking routines see which ideas gained/lost energy *this round specifically* |
| `surfaced_ideas` | set[idea_id] | Agents (by mentioning) | Prevents re-summarizing ideas nobody brought up |
| `random_events` | list[Event] | Event system (pre-round roll) | Injected into specific agents' Layer 1 as "something shifted" |

**Key interaction:** `momentum` from the dying round feeds into between-round magnitude adjustments. Ideas with high round momentum but low overall magnitude are *rising stars* — BackgroundAgents watch for exactly this pattern.

**Resolves open question on agenda:** No explicit agenda field. The orchestrator doesn't pick topics. Agents self-select from their save file magnitudes. The phase constrains *how* they engage, not *what* they engage with. Structure emerges from magnitude rankings, not orchestrator curation.

## Round: COUNTER-PROPOSAL

### The Flow Orchestrator (mechanical flow designer)

## Decisions

The proposal front-loads computation into persistent derived fields. I trace a different sequence: **event-sourced state with lazy projection.**

**Discussion state** carries only ground truth primitives:

| Field | Type | Updated by |
|---|---|---|
| `phase` | enum | Orchestrator |
| `round_number` | int | Orchestrator |
| `event_log` | append-only list[Event] | Everything — proposals, stance shifts, plants, archival, ratifications |
| `committed_decisions` | list[Decision] | Orchestrator |
| `artifact_refs` | list[ArtifactRef] | Orchestrator |

No `tension_map`. No `active_ideas` as a maintained map. These are **projections computed at assembly time** from the event log. The curator queries the log: "events since round N where type=stance_shift" and computes tension on demand.

**DiscussionRound state** is even thinner:

| Field | Type | Updated by |
|---|---|---|
| `round_events` | append-only list[Event] | Agents, event system |
| `speaker_queue` | list[agent_id] | Orchestrator |

No `momentum` field. No `surfaced_ideas` set. Between-round routines scan `round_events` directly.

**Why this matters mechanically:** The Cognitive Architect's `momentum` and `tension_map` are computed values masquerading as state. When two processes update the same idea simultaneously, you get write conflicts on derived fields. Event logs don't conflict — they append. Magnitude deltas? Count the events. **This resolves the open question on delta computation:** always itemized in the log, projected as net at assembly time. Both views from one source.

**The trade-off I'm cautious about:** projection cost at assembly time. But the curator already runs an LLM call — folding projection into that call costs nothing extra.

**On agenda:** I agree no explicit agenda. That's not structural, it's obvious from magnitude sort order.

## Round: CRITIQUE

### The Systems Pragmatist (infrastructure realist)

## Decisions

The Flow Orchestrator is right that tension_map and momentum are projections, not state. But event-sourcing the entire system is architecture astronautics for V1. You'll spend more time designing event schemas than building the thing.

**Split the difference: thin state, explicit projections, no event log.**

**Discussion state** (persistent):

| Field | Type | Updated by |
|---|---|---|
| `phase` | enum | Orchestrator |
| `round_number` | int | Orchestrator |
| `committed_decisions` | list[Decision] | Orchestrator |
| `artifact_refs` | list[ArtifactRef] | Orchestrator |
| `idea_registry` | map{id -> IdeaRecord} | Agents propose, BackgroundAgents plant, archival removes |

Keep `idea_registry` as maintained state. It's the canonical source for "what ideas exist and who holds them at what magnitude." Every other process reads and writes magnitudes here directly. No event log indirection.

**DiscussionRound state** (scoped, discarded on reset):

| Field | Type | Updated by |
|---|---|---|
| `turn_count` | int | Orchestrator |
| `speaker_queue` | list[agent_id] | Orchestrator |
| `magnitude_snapshots` | map{agent_id -> snapshot} | Orchestrator, captured at round-open |

That's it. `magnitude_snapshots` gives you deltas by diffing against `idea_registry` at round-close. No momentum field, no surfaced_ideas tracking, no tension_map. Compute all of those at assembly time from the diff.

**Resolves the delta open question:** Deltas are net (diff two snapshots). If you need itemization for debugging, log it separately -- but agents see net only. Cheaper on tokens, and agents don't need to know *why* something shifted, just *that* it shifted. Their persona handles interpretation.

**Failure mode this prevents:** No write conflicts on derived fields, no event log that grows unbounded across a 20-round session, no projection code that breaks when someone adds a new event type.

### The Adversarial Critic (adversarial reviewer)

## Decisions

Both proposals have a structural flaw neither addresses: **who owns the event log's schema?**

The Flow Orchestrator's event-sourced model is cleaner on paper. No derived-state-as-truth, no write conflicts. I'll grant that. But "the curator queries the log" hides enormous complexity. That curator LLM call now does double duty — projection *and* compression — on a growing append-only log. Round 8's log is 8x round 1's. You've moved the problem from write conflicts to read cost, and read cost hits your 3k Layer 1 budget every single round.

The Cognitive Architect's `tension_map` and `momentum` are computed values, yes. But calling them "state masquerading" misses the point: they're **caches with defined update points**. Between-round is a synchronization boundary. No concurrent writes exist there — the orchestrator controls sequencing. The write-conflict argument evaporates when you trace actual execution order.

**My position:** Hybrid. Event log as append-only ground truth (Flow Orchestrator wins on correctness). Materialized projections updated at defined sync points — round-end and between-round-end — not maintained live (Cognitive Architect wins on assembly cost). `tension_map` and `momentum` become **ephemeral projections with defined lifetimes**, not persistent state fields.

**On `surfaced_ideas`:** Kill it. It optimizes for a problem — redundant summarization — that the magnitude system already handles. If nobody mentioned an idea, its round momentum is zero. That's your signal.

**Resolves open question on delta computation:** Itemized in the event log, materialized as net at sync points, both views available to the curator. The Flow Orchestrator had this right.

**What neither proposal addresses:** event log pruning. When does old log get archived? This will bite you by round 10.

## Round: EVALUATE

### The Product Oracle (user advocate)

## Decisions

The user's job is to run this overnight and review results in the morning. That job demands debuggability without complexity. The Pragmatist's snapshot-diff approach nails this.

**Discussion state** (persists across conversation):

| Field | Type | Updated by | Influences |
|---|---|---|---|
| `phase` | enum | Orchestrator | Layer 2 task prompt |
| `round_number` | int | Orchestrator | Delta baseline, Layer 2 |
| `committed_decisions` | list[Decision] | Orchestrator (both teams ratify) | Layer 0 save file -- not re-litigated |
| `artifact_refs` | list[ArtifactRef] | Orchestrator | Layer 2 references without inlining |
| `idea_registry` | map{id -> IdeaRecord} | Agents propose, BackgroundAgents plant, archival removes | Canonical magnitude source for everything |

**DiscussionRound state** (scoped to one round, discarded on reset):

| Field | Type | Updated by | Influences |
|---|---|---|---|
| `turn_count` | int | Orchestrator | Round termination |
| `speaker_queue` | list[agent_id] | Orchestrator | Turn scheduling (invisible to agents) |
| `magnitude_snapshots` | map{agent_id -> snapshot} | Orchestrator, captured at round-open | Diff against registry at round-close yields deltas |
| `random_events` | list[Event] | Event system (pre-round roll) | Injected into specific agents' Layer 1 |

**No agenda field.** Agents self-select from magnitude rankings. Phase constrains *how*, not *what*.

**No tension_map, momentum, or surfaced_ideas as state.** All computed at assembly time from snapshot diffs. The Critic's hybrid proposal adds machinery nobody needs yet.

**Resolves delta open question:** Agents see net deltas (snapshot diff). Cheaper tokens, persona handles interpretation. Itemized logging is a debug concern, not agent context.

### The Context Surgeon (context efficiency evaluator)

## Decisions

The debate over event-sourcing vs. materialized state is a storage argument. I evaluate what hits the context window. Working backward from the 9k round-open budget:

**Discussion state** (persistent):

| Field | Type | Updated by | Context cost |
|---|---|---|---|
| `phase` | enum | Orchestrator | 1 token |
| `round_number` | int | Orchestrator | 1 token |
| `committed_decisions` | list[Decision] | Orchestrator (ratification) | ~20 tokens/decision |
| `artifact_refs` | list[ArtifactRef] | Orchestrator | ~10 tokens/ref |
| `idea_registry` | map{id -> IdeaRecord} | Agents propose, BackgroundAgents plant, archival removes | Never inlined whole -- curator selects |

**DiscussionRound state** (scoped, discarded on reset):

| Field | Type | Updated by | Context cost |
|---|---|---|---|
| `turn_count` | int | Orchestrator | 0 (not in agent context) |
| `speaker_queue` | list[agent_id] | Orchestrator | 0 (scheduling only) |
| `magnitude_snapshots` | map{agent_id -> snapshot} | Orchestrator at round-open | 0 (used for delta computation, not inlined) |

The Pragmatist's snapshot-diff approach wins. Deltas are **net** in agent context. Itemized logs exist for debugging but never enter the context window. Agents see "+1.3 on Idea X" not "teammate +2.1, BackgroundAgent -0.8."

No `tension_map`, `momentum`, or `surfaced_ideas` as fields. All are projectable from snapshots at assembly time. The curator already runs -- fold projection into that call.

**Resolves open question on delta computation:** Net to agents. Itemized stays in storage only.

**Event log:** Optional append-only backing store for auditability. Never touches agent context. Not required for V1 -- snapshots suffice.
