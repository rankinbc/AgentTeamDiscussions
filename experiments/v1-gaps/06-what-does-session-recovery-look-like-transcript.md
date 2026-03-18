# Transcript: What does session recovery look like?

*Generated: 2026-03-18 04:02*

## Round: PROPOSE

### The Cognitive Architect (creativity engine designer)

# Session Recovery: The Filesystem Is the Checkpoint

## Decisions

### D1: Progress Is Derived, Not Recorded

No progress file. No `state.json`. No cursor.

The orchestrator scans the session folder on startup: count the completed design docs (`q{n}_design.md`). The next question number is `max(n) + 1`. Done.

A dedicated progress marker is a second source of truth that can disagree with the actual artifacts. If the process crashes after writing the design doc but before updating a progress file, you have a lie on disk. If it crashes after the progress file but before the design doc, you have a different lie. The filesystem inventory cannot disagree with itself.

### D2: Incomplete Question Detection

A question is **complete** when three files exist: `q{n}_design.md`, `q{n}_transcript.md`, and the ledger contains a `### Q{n}` block. If a design doc exists but the ledger entry is missing, the question is **partial** -- the synthesizer crashed mid-extraction.

Recovery action for partial: re-run synthesis only, feeding the existing transcript. Do not re-run the discussion rounds. Agent contributions are preserved; only the distillation step replays.

### D3: Morning Brief Reports Incomplete Sessions

The Morning Brief includes a status line:

```
Session Status: INCOMPLETE (5/10 questions finished, Q6 partial — synthesis replay needed)
```

If all questions completed: `COMPLETE`. If interrupted cleanly between questions: `INCOMPLETE (5/10)`. If mid-question: `INCOMPLETE (5/10, Q6 partial)`.

No euphemisms. The brief tells you exactly where it stopped and whether replaying requires human intervention.

### D4: No Rollback Machinery

There is no undo. If a design doc is malformed, the user deletes it and reruns. Simplicity over sophistication.

### The Flow Orchestrator (mechanical flow designer)

## Decisions

### D1: Progress Marker is the Ledger Itself

No separate checkpoint file. The decisions ledger already accumulates one block per completed question. Count the blocks — that's your progress. Question is complete when its ledger block exists. If the ledger has 4 blocks, you resume at question 5.

A dedicated checkpoint file would duplicate information the ledger already contains. Eliminate it.

### D2: Partial State is Discarded on Resume

If the process crashes mid-question (during rounds or synthesis), any partial files for that question — incomplete transcript, draft design doc — are orphaned. On restart, the orchestrator counts ledger blocks, identifies the next unanswered question, and runs it from scratch.

No attempt to recover partial round output. The rounds are cheap (three `claude -p` calls plus synthesis). Reconstructing partial state is expensive in complexity and fragile in practice. Rerun the question.

### D3: Resume is a Startup Behavior, Not a Separate Command

The orchestrator always checks for an existing session folder on launch. If one exists with a partial question set, it prompts: "Session has 4/10 questions completed. Resume? [Y/n]". Same entry point, same command.

### D4: Morning Brief Reports Completion State

If the session is incomplete, the Morning Brief states: "Session incomplete: 4 of 10 questions answered. Last completed: Q4 (topic tag). Run orchestrator to resume." No partial analysis of unanswered questions. No speculation.

### D5: The Design Doc From the Last Completed Question Chains Forward Normally

Resume loads the ledger and Q4's design doc as prior context — identical to what Q5 would have received had the process not crashed. No special recovery context needed.

## Open Questions

- None introduced. This resolves cleanly from existing structure.

## Round: CRITIQUE

### The Systems Pragmatist (infrastructure realist)

# Critique: Two Proposals, Same Instinct, One Real Disagreement

Both proposals converge on the right principle: derive state from artifacts, not metadata files. Good. But they diverge on one critical failure mode, and neither acknowledges it clearly enough.

## The Disagreement That Matters: Partial State

Cognitive Architect says: detect partial questions, replay synthesis only. Flow Orchestrator says: discard partial state, rerun the full question.

**Flow Orchestrator is right.** Here's why:

Replaying synthesis assumes the transcript is complete and well-formed. But a crash during round 3 produces a transcript with two agent contributions, not three. The synthesizer now operates on incomplete input and produces a design doc missing an entire perspective. That design doc chains forward as context for Q6. The error compounds silently.

Detecting *which* partial state is recoverable requires inspecting transcript contents — counting agent blocks, validating structure. That's parsing your own output to determine correctness. Exactly the kind of operation that looks correct in the happy path and fails silently in production.

**Rerun the question. Three CLI calls cost seconds. Debugging a half-synthesized design doc costs the session.**

## Filesystem-as-Checkpoint: One Caveat

Both proposals assume atomic file writes. They aren't. A crash mid-write produces a truncated `q5_design.md` that exists but is garbage. The completeness check needs a trivial integrity signal — a trailing marker line (`<!-- complete -->`), checked on resume. Not a progress file. A self-contained validity marker within the artifact itself.

## On the Ledger as Progress Counter

Agreed. The ledger block count is the canonical progress indicator. Adding a checkpoint file is adding a consistency problem.

## Resolution

Discard-and-rerun beats selective replay. Add a completion marker inside artifacts. Everything else aligns.

### The Adversarial Critic (adversarial reviewer)

# Critique: The Interesting Disagreement Is the Only One That Matters

Both proposals agree on the easy stuff: no checkpoint file, derive progress from artifacts, Morning Brief reports status. Fine. That's obvious enough to not need two proposals.

The real divergence: **what happens to a half-finished question?**

**Cognitive Architect** wants surgical recovery — detect that the transcript exists but synthesis failed, replay only synthesis. **Flow Orchestrator** says burn it down and rerun the whole question.

I side with the Orchestrator, and the Architect's own prior work tells us why.

The Architect proposes a three-file completeness check: design doc, transcript, and ledger block. But this creates exactly the multi-source-of-truth problem D1 claims to solve. Now you need three artifacts to agree, and you need logic to diagnose which combination of present/absent files maps to which failure mode. Transcript exists but no design doc? Replay synthesis. Design doc exists but no ledger entry? Replay extraction. Both exist but ledger entry is malformed? Now what?

That's a state machine masquerading as simplicity.

Three `claude -p` calls plus synthesis costs what — two minutes? The complexity budget for partial recovery exceeds the compute budget for rerunning. This isn't a database migration. It's four CLI invocations.

**One genuine gap neither proposal addresses:** what prevents the orchestrator from appending a duplicate ledger block if it reruns a question whose ledger entry already exists? The "append-only, never edit" rule from Q5 means you can't delete the partial entry. You need dedup-on-write or you've corrupted the ledger. Solve that before declaring this clean.

The Orchestrator's proposal is mechanically simpler and has fewer failure modes. Ship that.

## Round: EVALUATE

### The Product Oracle (user advocate)

# Evaluate: The User Wakes Up to a Half-Finished Session

The job here isn't "recover state." The job is: **the user glances at results before coffee and knows exactly what happened and what to do.**

## Verdict: Discard-and-Rerun Wins

Both critics are right, and for the reason that matters most to the user: predictability. If I rerun a question, I get a complete result. If I replay synthesis on a partial transcript, I get a result that *looks* complete but might be missing a perspective. The user can't tell the difference. That's the worst kind of failure -- one that passes visual inspection.

Three CLI calls cost seconds. A subtly degraded design doc costs trust in every doc that follows it.

## The Two Gaps Are Real

**Completion markers.** The Pragmatist's `<!-- complete -->` trailing line is the right weight. Not a schema. Not a checksum. A line that's either there or it isn't. The orchestrator checks for it on resume.

**Ledger dedup.** The Critic caught a real bug. On rerun, the orchestrator must check whether a `### Q{n}` block already exists before appending. If it does, the prior entry is from a crashed run and is potentially incomplete. Since we can't edit the ledger (Q5, D3), the rerun appends a fresh block with a `REPLACES Q{n}` annotation. Agents seeing both resolve in favor of the later entry -- same chronological-wins rule already established.

## What the User Sees

Resume is automatic. Morning Brief is honest. No decisions about what to recover. That's the product.

### The Context Surgeon (context efficiency evaluator)

# Evaluate: Context Budget on This Question Is Nearly Spent

The critics converged. The remaining work is bookkeeping.

## What's Decided

**Discard-and-rerun wins.** Both critics independently rejected surgical replay. The argument is settled: three CLI calls are cheaper than a partial-state diagnostic engine. No further deliberation needed.

**Progress = ledger block count.** Universal agreement. No checkpoint file.

**Morning Brief reports status honestly.** No disagreement on format or content.

## Two Mechanical Details Need Answers

**1. Completion marker.** The Pragmatist's `<!-- complete -->` trailing line solves truncated writes. Costs nothing. The orchestrator checks for it before trusting any artifact. If absent, the file is treated as non-existent. This is a one-line implementation decision, not a design question.

**2. Ledger dedup on rerun.** The Critic caught this. If Q5 crashed after appending a ledger block but before finishing the design doc, rerunning Q5 appends a second block. Solution: before appending, check whether `### Q{n}` already exists in the ledger. If yes, skip the append. This is not editing the ledger — it's a write guard. The append-only rule from Q5 survives intact.

## Open Questions Resolved

None of the three prior open questions (extraction loss rate, supersession clarity, topic tag vocabulary) are addressable by this question's scope. They remain open.

## Context Cost Assessment

This question consumed four proposals and critiques to reach three decisions and two implementation details. The signal-to-token ratio dropped after the first critique. Future questions of this mechanical complexity should skip the second critique round.
