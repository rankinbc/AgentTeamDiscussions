### The Cognitive Architect (creativity engine designer)

The beta system's 6000-char truncation is treating the symptom. The disease is using the wrong artifact as context.

**The Morning Brief already solves this problem. We're not using it.**

The rolling synthesis architecture produces a brief after every question — compressed, structured, cumulative. By Q8, `brief.md` contains exactly what Q8 needs: all decided decisions, all live open questions, the sharpest outstanding objections, and the recommended focus. That's the context. Not seven design docs.

**My proposal:** Prior design docs are never fed to subsequent discussion rounds. The input contract for propose/critique/evaluate is:

```
current_question + morning_brief (current state)
```

That's it. The brief is the accumulator. It was *designed* to be the accumulator. Feeding raw design docs alongside it is double-counting — you're passing both the compressed form and the uncompressed source, and the model will weight whichever is most recent and verbose (the raw docs).

The design doc's job is archival and human review. The brief's job is forward context. These are different artifacts with different consumers. Stop conflating them.

**This also resolves a residual open question:** "Does the design doc chain forward as context?" Yes — *through the brief*, not directly. The extraction step captures what matters. What the brief omits is by design: low-signal deliberation that shouldn't pollute later questions.

**The implementation consequence:** Remove the design doc concatenation from the discussion input. The brief is already on disk. Pass it. The 6000-char truncation logic becomes unnecessary complexity — delete it.

### The Flow Orchestrator (mechanical flow designer)

Agreed. The Cognitive Architect's framing is correct, and it simplifies the state machine.

**The operational sequence is now:**

```
Propose input:  current_question + brief.md (or empty on Q1)
Critique input: current_question + brief.md + propose_output
Evaluate input: current_question + brief.md + propose_output + critique_output
```

The brief is bounded by design — hard word budgets, four sections, pruned on every write. It cannot grow unboundedly. The truncation problem was always about feeding the wrong artifact; removing design docs from discussion input removes the problem entirely. The 6000-char truncation logic is now dead code — delete it.

**What this closes:**

The "prior design docs chain forward as context" decision is not contradicted — the mechanism is *through the brief*, not direct concatenation. The brief is the forward-chain. Design docs are archival only.

**Q1 edge case is already handled:** `brief.md` doesn't exist on Q1. Input is just `current_question`. The `## What Got Built` omission decision covers the synthesis side. The discussion side just runs with no prior context — which is correct.

**One sequencing note to make explicit:** Step 5 (design doc write) still consumes truncated evaluate output + extracted fields. That input contract is unchanged. The change is strictly to discussion round inputs (steps 1–3). These are orthogonal writes to different artifacts with different consumers. Don't conflate the fix.

**Flag:** The existing "prior design docs chain forward" decision in the agreed list needs a clarifying amendment: *through the brief, not directly into discussion rounds.* Otherwise a future implementer will reintroduce the concatenation.


<!-- complete -->
