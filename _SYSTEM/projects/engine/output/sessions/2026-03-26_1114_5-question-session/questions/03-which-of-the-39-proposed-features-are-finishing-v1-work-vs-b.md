# Which of the 39 proposed features are finishing V1 work vs building genuinely new systems?

*Generated: 2026-03-26 11:29 | Q3 | 195s | Mode: compete*

## Decisions

### D1: Enumerate before classifying

All five agents converged on this: the 39-feature list has not been concretely enumerated with defined boundaries. No classification framework — dependency depth, state-machine topology, cascade risk, user-output scoring, or file-boundary triage — produces value until the list exists with enough precision to estimate against. Classification debates on an unbounded list are premature abstraction.

### D2: Extract V1 features mechanically from the codebase

The V1-vs-new distinction is already encoded in the repository. Stubs, TODOs, partial implementations, and features that touch only existing files without requiring new interfaces constitute V1 completion work. Everything requiring new abstractions, new event types, or new state machines is a new system. This is a grep operation, not a design decision.

### D3: Measurement before mechanism remains the single ordering constraint

The prior decided finding — context accumulation dominates agent identity by Round 2 — already establishes that mechanism features (stigmergic coordination, dynamic context budgeting, adaptive round structures) cannot be evaluated without measurement infrastructure. This is not a new insight but it is the only sequencing dependency that survived critique. Crude proximate signals (token overlap, semantic similarity, prompt-vs-context ratios) are sufficient to start; perfect instrumentation is not required.

### D4: Score features by visible output improvement

Once enumerated, features should be evaluated against a single question: does this change what appears in the Morning Brief or design docs, and can the improvement be measured by reading output? Features that cannot demonstrate visible improvement in session output are not ready to build regardless of their engineering elegance.

### D5: Atomic writes for session.json is the single gating feature

This was already decided as a V1 blocker. It gates every feature that depends on session state surviving crashes. Ship it before anything else.

---

## Design: Feature Classification Process

### Step 1 — Mechanical Enumeration

Scan the codebase for the V1 boundary:

- **Stubs and TODOs** in source files indicate intended-but-unfinished V1 work.
- **Existing interfaces with partial implementations** (e.g., speaking order is iterated but not rotated; ledger appends but does not filter) are V1 completion.
- **Features requiring new interfaces, new file types, or new subprocess interactions** (e.g., token counting in ClaudeRunner, shared artifact stores for stigmergic coordination) are new systems.

Produce a concrete list with one line per feature, a boundary definition (what's in, what's out), and the V1-or-new tag.

### Step 2 — Sequencing

Apply three rules in order:

1. **V1 blockers ship first.** Atomic writes for session.json. Speaking order rotation. Any feature whose absence produces corrupt or misleading output.

2. **Instrumentation ships before mechanisms.** Transcript content auditing, context window consumption tracking, and behavioral distinctiveness metrics are prerequisites for evaluating whether mechanism features work. Instrumentation does not need to be perfect — proximate signals from existing observations (D3's identity decay finding was made by reading transcripts, not by running metrics) are sufficient to unblock mechanism design.

3. **Mechanisms ship with evaluation criteria defined in advance.** No mechanism feature (adaptive rounds, dynamic context budgets, cognitive-strategy migration) enters development without a stated metric and threshold for success. This prevents the failure mode the Critic identified: instrumentation that measures the wrong things producing garbage data that looks authoritative.

### Step 3 — Output-Impact Filter

Within each sequencing tier, prioritize by: does this feature change what the user reads in the Morning Brief or design docs? Features that improve internal engineering quality but produce no visible output change are valid work but lower priority than features the user can evaluate by reading session output.

---

## Rejected Approaches

| Approach | Why Rejected |
|---|---|
| Three-tier dependency depth (wiring / instrumentation / mechanisms) | Adds abstraction without changing what ships when. The valid insight (measurement before mechanism) is already a decided finding. |
| State-machine binary (existing vs. new state machines) | Honest engineering lens but tells you nothing about effort, risk, or user value. A zero-new-state-machine feature can still take weeks. |
| Cascade-risk identification (find the five riskiest features) | Cannot identify cascade risks in an unnumbered list. Same enumeration prerequisite as every other approach. |
| User-output scoring before enumeration | Correct principle applied prematurely. Scoring a list that doesn't exist is the same mistake as sorting an empty array. |

---

## Open Items

- The 39-feature list has not been produced. This design doc defines the process for classifying features but cannot execute it without the enumerated list.
- The circular dependency between instrumentation and mechanism design (you cannot instrument what you cannot define; you cannot define identity metrics without experimental mechanisms) is real but manageable through proximate signals. The boundary between "good enough instrumentation" and "premature mechanism building" will need judgment calls per feature.
- Feature boundary definitions will be contested. "Speaking order rotation" could be one feature (round-robin) or three (random, round-robin, weighted). Boundary precision determines whether 39 is actually 39 or 25 or 60.
<!-- complete -->
