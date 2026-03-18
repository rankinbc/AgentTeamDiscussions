# What's in the Discussion and DiscussionRound state?

*Generated: 2026-03-17 22:40 | Question 3 | 156s | Mode: counter*

## Decisions

1. **Discussion state carries five persistent fields; DiscussionRound state carries four scoped fields.** All proposals converged on the same core primitives. Derived values (tension, momentum, surfaced ideas) are computed at assembly time, never stored as state. The Pragmatist's snapshot-diff approach is the consensus mechanism -- it avoids write conflicts, avoids unbounded event logs, and provides both net deltas (for agents) and itemized breakdowns (for debugging) from the same data.

2. **Discussion state (persists across the entire conversation):**

   | Field | Type | Updated by | Influences |
   |---|---|---|---|
   | `phase` | enum (brainstorm, refine, specify, review) | Orchestrator, when phase transition criteria are met | Layer 2 task prompt -- controls diverge/converge instructions and phase-specific behavioral constraints |
   | `round_number` | int | Orchestrator, incremented on each round reset | Layer 2 task prompt display; serves as the baseline for snapshot delta computation |
   | `committed_decisions` | list[Decision] | Orchestrator, when both teams ratify an outcome | Appears in every agent's Layer 0 save file as settled ground truth -- agents do not re-litigate committed decisions |
   | `artifact_refs` | list[ArtifactRef] | Orchestrator, when a phase produces a spec, PRD, or architecture doc | Layer 2 can reference "draft spec v2 exists" without inlining the artifact into agent context |
   | `idea_registry` | map{id -> IdeaRecord} | Agents (propose new ideas), BackgroundAgents (plant synthesized ideas), archival sweep (remove ideas below threshold) | Canonical source of what ideas exist and who holds them at what magnitude -- every other process reads from and writes to this directly |

   **What is not here:** No `tension_map` (computed from stance divergence at assembly time). No `active_ideas` separate from the registry. No event log as a required V1 field -- an optional append-only backing store may be added for auditability but is not load-bearing for agent context or round mechanics.

3. **DiscussionRound state (scoped to one round, discarded on reset):**

   | Field | Type | Updated by | Influences |
   |---|---|---|---|
   | `turn_count` | int | Orchestrator, incremented per turn | Determines when the round ends; not visible in agent context |
   | `speaker_queue` | list[agent_id] | Orchestrator, determined at round-open | Controls who speaks next -- scheduling only, invisible to agents |
   | `magnitude_snapshots` | map{agent_id -> snapshot of their idea/stance magnitudes} | Orchestrator, captured at round-open from `idea_registry` | Diffed against `idea_registry` at round-close to yield per-agent magnitude deltas for between-round processing |
   | `random_events` | list[Event] | Event system, rolled pre-round before agents receive context | Injected into targeted agents' Layer 1 as factual notifications ("something shifted"); the event system decides which agents are affected |

   **What is not here:** No `momentum` field (computable from snapshot diffs -- ideas with large positive deltas within a single round are rising). No `surfaced_ideas` set (zero momentum already signals an unmentioned idea). No `round_events` append-only log (snapshots provide the same diff information without unbounded growth).

4. **Magnitude deltas are net in agent context, itemized only in storage.** When between-round processes modify the same idea -- say intra-team talk shifts Idea X by +2.1 and a BackgroundAgent shifts it by -0.8 -- the agent sees "+1.3 on Idea X" in their Layer 1 compressed externals. The persona handles interpretation of what that shift means. Itemized breakdowns (which process contributed what) exist in the snapshot diff log for debugging and session review but never enter the 9k round-open context budget.

5. **No explicit agenda field exists anywhere in state.** Agents self-select what to open with based on their save file's magnitude rankings. The phase constrains how agents engage (brainstorm says "diverge freely," review says "evaluate against criteria") but not what topics they raise. Structure emerges from magnitudes, not orchestrator curation.

6. **The idea_registry is the single source of truth for magnitudes, not a cache or projection.** Every process that changes an idea's magnitude writes directly to the registry: agent proposals, BackgroundAgent interventions, between-round intra-team talk, archival sweeps. There is no event log that the registry is derived from. The registry is ground truth. This is a deliberate V1 simplification -- event sourcing is architecturally cleaner but adds schema design, projection code, and log pruning concerns that are not justified until the system proves the core mechanics work.

7. **The interaction between round state and persistent state follows a defined lifecycle:**
   - **Round-open:** Orchestrator snapshots each agent's magnitudes from `idea_registry` into `magnitude_snapshots`. Random events are rolled and stored. Agents receive assembled context (Layers 0-2).
   - **Mid-round:** Agents converse. The running transcript is the context. No state fields are updated mid-turn -- magnitude changes from conversation are extracted at round-close, not live.
   - **Round-close:** Orchestrator diffs `magnitude_snapshots` against current `idea_registry` to compute what shifted during the round. This diff feeds into between-round processing.
   - **Between-round:** Thinking routines (reflect, research, strategize) and intra-team talk run. These processes read the round's diff and write magnitude changes directly to `idea_registry`. BackgroundAgents analyze patterns (e.g., high round delta but low overall magnitude = rising star) and intervene. Archival sweep runs per-agent with persona-dependent thresholds.
   - **Next round-open:** New snapshots are taken. The cycle repeats. The previous round's `DiscussionRound` state is discarded.

## Open Questions

- **Save file serialization format.** The save file contains ideas with magnitudes, stances with magnitudes, committed decisions, and a 3-5 sentence personal recap. The format (JSON, YAML, structured markdown) affects token efficiency when injected into Layer 0 and parseability by the curator. JSON is most compact; YAML is most readable in session review; structured markdown is most natural for LLM consumption. This needs a decision before implementation.
- **Archival threshold interaction with idea_registry.** When a stubborn agent's persona-dependent threshold keeps a low-magnitude idea alive that a flexible agent would have dropped, the idea exists in `idea_registry` with different per-agent magnitudes. The archival sweep must be per-agent -- an idea can be archived for Agent A (magnitude fell below their threshold) while remaining active for Agent B (whose stubbornness keeps the threshold lower). The registry needs to track per-agent magnitude, not a single global magnitude. The IdeaRecord structure must account for this.
- **Event log as optional V1 backing store.** Multiple participants noted that an append-only event log is valuable for debugging and session review ("what happened to Idea X over 15 rounds?") but agreed it should not be load-bearing for agent context. The question is whether to build it in V1 as a write-only audit trail or defer entirely. Building it is cheap (just append); not building it means reconstructing history from snapshots, which is lossy.
- **Random event system specifics.** The `random_events` field exists in round state but the event system's mechanics are undefined: what is the probability distribution, what kinds of events exist, how many agents can be affected per round, and can events contradict each other? This needs its own design pass.