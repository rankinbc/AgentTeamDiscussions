# What problems will emerge at scale?

*Generated: 2026-03-26 18:54 | Q4 | 229s | Mode: compete*

## Decisions

### 1. The Per-Game Machine-Readable Manifest Is the Immediate Structural Gap

A per-game index file — machine-queryable, maintained alongside the hierarchy — is required before wave 2 of any game. Without it, research agents at scale either load everything (context budget exhausted) or load nothing (blind writes, duplication, contradictory outputs the user must manually untangle). The folder structure is a human-readable index. Human-readable indexes do not support machine traversal. This gap exists from wave 1 and compounds with every subsequent research wave.

The manifest is a single structured file per game that agents query before reading or writing anything. It must answer: what files exist, what systems they cover, and what depth level they represent. Exact schema is deferred but must be agent-queryable without full directory traversal.

### 2. The Cross-Game Schema Layer Is Rejected as Premature

The Architect's proposal is rejected. A shared vocabulary of system archetypes is a valid long-term direction, but it fails on two counts at current scale: (a) schema ownership is unresolved — no decision records who can evolve the schema when a new game's system doesn't fit an existing archetype, and (b) it adds a mandatory shared-context dependency to every agent call, taxing every invocation before a single recurrence pattern has been proven worth that overhead. The approval queue problem the Architect identifies does not justify introducing a second, parallel approval queue for schema evolution.

Cross-game schema is deferred until recurrence patterns are empirically established across at least three games. If the same archetype appears in three independent games with the same structural shape, that earns normalization. It is not anticipated in advance.

### 3. Cascade Invalidation Is a Real Problem and a Deferred One

The Critic's point stands: the CONTRADICTED flag without downstream traversal is incomplete. Marking a claim contradicted leaves all derived INFERRED claims built on it untouched, with no mechanism to locate them. The Pragmatist is correct that markdown files cannot natively implement a dependency graph — provenance tracks origin, not dependency, and these are not the same thing.

However, the prescription of relational infrastructure is rejected for solo-builder scale. The cure costs more in configuration and maintenance overhead than the disease costs in manual reconciliation at 10 games. Cascade invalidation becomes a first-order problem only when a real derived chain gets overturned and the user feels the consequence. Until that happens, the correct posture is: when a claim is marked CONTRADICTED, the file must explicitly list any known downstream files that cite it. This is a manual obligation on the researcher who files the CONTRADICTED flag, not an automated traversal. It is incomplete by design and honest about that incompleteness.

### 4. UNKNOWN Estimate Rot Has a Lightweight Fix

UNKNOWN estimates accumulate across waves with no retirement signal. By wave 4, a file may contain multiple bracketed estimates, some superseded by later findings, none marked inactive. The fix is a `superseded_by` field on each estimate, recording the wave number and file that resolved it. This is metadata, not architecture. Unresolved estimates older than a configurable threshold are flagged stale. These are two fields. No structural change required.

The deeper problem — that downstream researchers treat `[UNKNOWN: est 2-4]` as a known data point and build INFERRED claims on it — is addressed by a provenance propagation rule: any claim derived from an UNKNOWN estimate must carry that origin in its own provenance, regardless of the intermediate tier label. INFERRED claims built on UNKNOWN inputs are tagged `INFERRED ← UNKNOWN`. The displayed tier does not launder the chain.

### 5. Wave-Gate Paralysis Is a UX Problem, Not an Architecture Problem

Managing approval queues across 10 games in simultaneous wave progression is a presentation problem. The fix is a unified dashboard view showing all pending approvals across all games in a single queue, sortable by game and wave. This does not require architectural change to the wave-gated pipeline. The wave gate itself is retained — human approval between waves remains the correct control point. The bottleneck is the absence of a consolidated view, not the existence of approval gates.

### 6. A Shared Conventions Document Is Adopted

Schema drift between games — where "Level 3" means exact formula in one game and rough mechanic in another — is a legitimate scale problem. The fix is a single `conventions.md` in the root of `analysis_games/` defining depth-level semantics that apply across all games. Researchers read it before filing. This document is versioned but not enforced by tooling — enforcement creates coordination overhead that exceeds the cost of the occasional misfiled entry. Drift is corrected at organizer review, not prevented by a schema layer.

### 7. Conflict File Staleness Is Addressed by a Single Field

First-class conflict artifacts are correct. Unresolved conflicts at scale become archaeological debris without resolution pressure. Each conflict file gains a `stale_after` datetime. Conflicts that exceed this threshold surface in the wave approval dashboard as blocked items requiring resolution before the next wave proceeds. This creates resolution pressure without changing the conflict-as-file design.

### 8. What Is Not Decided Here

- The exact schema of the per-game manifest (deferred to implementation)
- The specific threshold for `stale_after` on conflict files (configurable, not fixed here)
- Whether cross-game schema adoption is ever triggered, and by what governance process (deferred until three-game recurrence is observed)
- Tooling for the unified approval dashboard (deferred to implementation)
- How ROM version ambiguity interacts with provenance at scale (open gap, carried forward from Q3)
<!-- complete -->
