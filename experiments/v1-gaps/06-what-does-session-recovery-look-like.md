# What does session recovery look like?

*Generated: 2026-03-18 04:02 | Question 6 | 107s | Mode: compete*

## Decisions

### D1: Progress Is Derived From Artifacts, Not Recorded in a Checkpoint File

No `state.json`, no progress marker, no cursor file. The orchestrator scans the session folder on startup and counts completed artifacts. The next question number is `max(completed) + 1`.

A dedicated progress file is a second source of truth. If it disagrees with the actual artifacts on disk, one of them is lying. The filesystem inventory cannot disagree with itself.

The decisions ledger serves as the canonical progress indicator. Count the `### Q{n}` blocks -- that is the number of completed questions.

### D2: Incomplete Questions Are Discarded and Rerun From Scratch

If the process crashes mid-question -- during any round or during synthesis -- all partial output for that question is abandoned. On restart, the orchestrator identifies the next unanswered question by ledger block count and runs it fresh: all three discussion rounds plus synthesis.

No attempt to detect whether a transcript is complete. No selective replay of synthesis on a partial transcript. A crash during round 2 produces a transcript missing an entire agent perspective. Replaying synthesis on that input produces a design doc that looks complete but is substantively degraded. The user cannot distinguish a full-perspective doc from a partial-perspective doc by visual inspection. That failure mode is worse than rerunning.

Three `claude -p` calls plus synthesis costs seconds. Diagnosing which partial artifacts are recoverable costs a state machine. The complexity budget for surgical recovery exceeds the compute budget for rerunning.

### D3: Artifacts Include a Completion Marker

Every file the orchestrator writes -- design docs, transcripts, ledger entries -- ends with a trailing marker line: `<!-- complete -->`. On resume, the orchestrator checks for this marker before trusting any artifact. If the marker is absent, the file is treated as non-existent (truncated write from a crash).

This is not a checksum or a schema. It is a single line that is either present or not. A crash mid-write produces a truncated file without the marker. The check is one string comparison.

### D4: Ledger Dedup on Rerun Is a Write Guard, Not an Edit

Before appending a new `### Q{n}` block to the ledger, the orchestrator checks whether a block for that question number already exists. If it does -- meaning a prior run crashed after the ledger append but before completing other artifacts -- the orchestrator skips the append.

This is not editing the ledger. The append-only rule from Q5 (D3) survives. This is a guard that prevents duplicate entries. The existing block, even if from a crashed run, contains the same extracted decisions because synthesis completed (the ledger entry was written). What failed was a downstream step.

If the ledger block exists but the design doc does not (or lacks the completion marker), the orchestrator reruns the full question but only appends to the ledger if no block for that question exists.

### D5: Resume Is Startup Behavior, Not a Separate Command

The orchestrator always checks for an existing session folder on launch. If one exists with fewer completed questions than configured, it prompts: `"Session has 4/10 questions completed. Resume? [Y/n]"`. Same entry point, same command. No separate recovery workflow.

On resume, the orchestrator loads the ledger and the last completed design doc as prior context -- identical to what the next question would have received had the process not crashed. No special recovery context is injected.

### D6: Morning Brief Reports Completion State

If the session is incomplete, the Morning Brief includes:

```
Session Status: INCOMPLETE (5/10 questions finished)
Last completed: Q5 (topic tag)
Run orchestrator to resume.
```

If all questions completed: `Session Status: COMPLETE`.

No partial analysis of unanswered questions. No speculation about what remaining questions might produce. The brief states what happened and what to do next.

### D7: No Rollback Machinery

There is no undo. If a completed design doc is malformed, the user deletes it (and its completion marker disappears), and reruns. The orchestrator sees the missing or incomplete artifact and treats that question as the next to run. Simplicity over sophistication.

## Open Questions

- **Extraction loss rate** (from Q5): What percentage of meaningful constraints survive extraction into the ledger? Remains open. Not addressable by recovery design.
- **Supersession clarity** (from Q5): Whether agents reliably infer that later decisions supersede earlier ones from chronological order alone. Remains open.
- **Topic tag vocabulary** (from Q5): Whether topic tags should be fixed or free-form. Remains open.