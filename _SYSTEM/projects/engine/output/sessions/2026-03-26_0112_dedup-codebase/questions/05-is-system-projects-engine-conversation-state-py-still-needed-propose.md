### The Cognitive Architect (creativity engine designer)

The prior decisions established a pattern worth applying here directly: **diff before deciding**. The `config/teams/` episode showed that "partial overlap" is a label, not a measurement. Partial overlap could mean 90% identical with engine-specific additions worth preserving, or it could mean near-identical files that diverged silently when someone edited one copy and not the other.

Before consolidation strategy, run the diff. That produces three possible findings:

**Finding A — Engine copy is a subset of library.** No unique logic. Delete and redirect. Done.

**Finding B — Engine copy has genuine engine-specific state.** Here the cognitive architecture question becomes real: what state *belongs* at which layer? Library state should be agent-agnostic orchestration primitives — turn history, message types, participant identities. Engine state should be session-lifecycle concerns — round counts, experiment mode, Morning Brief accumulation buffer, live dashboard connection. If the engine copy mixes these, the right move is surgical extraction: promote the genuine library-level primitives upward, leave engine-specific concerns in the engine layer, then delete what's left.

**Finding C — Drift without clear ownership.** Analogous to persona drift in `config/teams/`. Silent degradation with no observable failure signal. The Morning Brief criterion doesn't catch this. Requires human review before any deletion.

The agenda I'm setting: **read both files before this discussion goes further.** Consolidation strategy chosen without the diff is speculation dressed as architecture. Every other question — redirect, delete, keep — is downstream of what the diff actually shows.

Who wants to pull those files?

### The Flow Orchestrator (mechanical flow designer)

The Cognitive Architect is correct on one point: diff first. But the framing stops before the operational sequence, which is where the actual decision complexity lives. Let me trace it.

**Step 1 — Read both files.** Not diff. Read. I need to know what *kind* of state each file holds before a byte diff tells me anything actionable. Diff output on state classes without understanding the state lifecycle is noise.

**Step 2 — Classify by ownership boundary.** Two questions with yes/no answers:
- Does the engine copy hold state that the library's session runner needs to read or write?
- Does the library copy hold state that the engine's discussion rounds need to read or write?

Each "yes" is a coupling point. Coupling points are not consolidation blockers — they're the *ordering constraints* for consolidation.

**Step 3 — Trace callers.** Who imports each file, and at what point in the session lifecycle? A state object instantiated at session start and passed through discussion rounds has a different consolidation path than one constructed fresh per-round.

**Decision tree:**
- Zero coupling points → delete engine copy, redirect imports, single commit.
- Coupling exists, engine state is a strict subset → redirect engine imports to library, delete.
- Coupling exists, divergent state fields → surgical extraction required; engine-specific fields stay, library primitives are the canonical source, engine copy becomes a thin subclass or is dropped entirely with field migration.
- Drift with no clear ownership → hard stop, human review.

I'm not speculating on which branch this lands in. Pull both files. That's the unblocking action.


<!-- complete -->
