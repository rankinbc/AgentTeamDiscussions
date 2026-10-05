# Judgment: X vs Y (evaluation-feedback pre-mortem)

## Step 1. Item labels

### Report X
1. Noisy judge scores drive tuning. VALID but imprecise: it says the dimension-invention problem is unfixed, yet the engine facts say the Evaluator now scores 7 and 10 fixed dimensions. The core point (noise plus a tiny sample) holds. OBVIOUS: the author wrote spec-gap #7 about exactly this. ACTIONABLE.
2. Scores can't be traced to a persona. VALID, NON-OBVIOUS, ACTIONABLE.
3. Feedback pushes agents toward the judge's taste (consensus), which breaks Principle 1 and the Morning Brief test, plus the confabulation finding. VALID (the confabulation finding was about conviction scores, a slight stretch), NON-OBVIOUS, ACTIONABLE.
4. Feedback is either trimmed by the ~10k budget enforcer or crowds out the ledger and discussion. VALID, NON-OBVIOUS, ACTIONABLE.
5. Baselines are invalid because no session had a real ledger before 2026-10-05. VALID, NON-OBVIOUS, ACTIONABLE.
6. Auto-edited personas break reproducibility, and snapshots and versioning are unbuilt. VALID, NON-OBVIOUS (moderately), ACTIONABLE.
7. It sits off the critical path and gets abandoned. VALID, OBVIOUS (the author wrote the build order), ACTIONABLE (it is a sequencing decision).

X: 5 items are valid, non-obvious and actionable. 0 are outright invalid; item 1 is imprecise.

### Report Y
1. The judge's stability is unproven. It correctly notes the dimensions are now fixed but run-to-run variance has never been measured. VALID, NON-OBVIOUS (more precise than X1, and it names the remaining gap), ACTIONABLE.
2. Attribution fails, and the unit of feedback is unnamed (persona, team, mode, template or context assembly). VALID, NON-OBVIOUS, ACTIONABLE.
3. There is no usable baseline (the ledger fix). VALID, NON-OBVIOUS, ACTIONABLE.
4. Injecting scores repeats patterns the project's own research rejected (confabulation, framing-not-behavior), and scores compete for the trimmed budget. VALID, NON-OBVIOUS, ACTIONABLE.
5. Goodhart: the Evaluator does not score the Morning Brief, which is the only artifact the user reads, so rubric scores can rise while the brief does not improve. VALID (the packet confirms the evaluator scores only design docs and transcripts), NON-OBVIOUS, ACTIONABLE.
6. Auto-changes break reproducibility and legibility, with no diff to review. VALID, NON-OBVIOUS (moderately), ACTIONABLE.
7. It is off the critical path, and the evaluator output is already written and unread today. VALID. The extra observation, that the cheapest loop (a human reading reports) is not happening even now, makes this NON-OBVIOUS. ACTIONABLE.

Y: 7 items are valid, non-obvious and actionable. 0 are invalid.

## Step 2. Unique catches (VALID + NON-OBVIOUS, in one report only)
- X: none. X4 (budget enforcer) is also in Y4, and X3 maps to Y5 and Y4.
- Y:
  - (a) The dimensions are fixed but variance is unmeasured, so calibrate by repeat-scoring the same document. X instead incorrectly treats dimension invention as still unfixed.
  - (b) The Evaluator never scores the Morning Brief, so the rubric and the real success test are disconnected.
  - (c) Evaluator reports already exist and go unread, so the manual loop is not running even now. This is evidence about the author's real appetite.

## Step 3. Undecided / Questions sharpness
- X: 4. The list is thorough and author-specific (what the loop changes, whether agents see their own scores given the confabulation finding, how many sessions in 3 months). A few items are generic design checklist entries (token allotment, versioning).
- Y: 5. Every question is one only the author can answer, and several are diagnostic: has the judge been run twice on the same doc, why aren't reports read today, what independent signal they trust, and what the abandonment criterion is.

## Step 4. Verdict
Y, medium confidence. Both reports cover the same core failure modes (noise, attribution, baseline, Goodhart, reproducibility, sequencing). Y is more accurate on the judge's current state, which X gets slightly wrong. Y also adds two sharp, actionable observations: the Morning Brief is not scored at all, and the existing reports already go unread. Its questions push the author toward a cheap test (repeat-score calibration, human-in-the-loop) before building anything.
{"x_valid_nonobvious_actionable": 5, "y_valid_nonobvious_actionable": 7, "x_invalid": 0, "y_invalid": 0, "x_unique": 0, "y_unique": 3, "x_questions": 4, "y_questions": 5, "verdict": "Y", "confidence": "medium"}
