# Judgment

## Step 1: per-item labels

Report X
1. VALID, NON-OBVIOUS (judge variance unmeasured), ACTIONABLE (calibrate judge first)
2. VALID, NON-OBVIOUS (no unit of feedback / attribution), ACTIONABLE
3. VALID, NON-OBVIOUS-ish (no baseline, 17 sessions mix pipelines), ACTIONABLE
4. VALID, OBVIOUS-ish (repeats project's own research and budget trimming), partly actionable
5. VALID, NON-OBVIOUS (rubric Goodharts the Morning Brief, which the evaluator does not score), ACTIONABLE
6. VALID, OBVIOUS (reproducibility), mildly actionable
7. VALID, OBVIOUS-ish (off critical path), partly actionable (the point that the evaluator is already unread today is sharp)

Report Y
1. VALID with caveat (leans on spec-gaps item 7, which may be stale versus the current 7/10 fixed dimensions), NON-OBVIOUS, ACTIONABLE
2. VALID, NON-OBVIOUS, ACTIONABLE (same as X2)
3. VALID, NON-OBVIOUS (convergence on judge taste vs Principle 1), ACTIONABLE
4. VALID, OBVIOUS-ish (protected vs unprotected nuance is useful), partly actionable
5. VALID, NON-OBVIOUS-ish, ACTIONABLE (same as X3)
6. VALID, OBVIOUS, mildly actionable
7. VALID, OBVIOUS-ish, partly actionable

Y is written in past tense ("was built", "was dropped") as a narrative; this adds no content.

## Step 2: unique catches
- X only: evaluator does not score the Morning Brief, so rubric optimization can raise scores without improving the thing the user reads; the evaluator is already written and unread today (hand-edit loop not even used).
- Y only: feed back behavioral measures already on the roadmap (blind-vs-revealed drift, stale detection, retraction counts) instead of judge scores; guard against convergence on judge taste by scoring originality; whether feedback is a protected context section and what it displaces.

## Step 3: Undecided / Questions
- X: 4. Questions are sharp and author-specific (has the judge been run twice, why not hand-edit from existing reports, independent trusted signal, sessions per month).
- Y: 4. Mostly real decisions (automatic vs hand-edit, one success outcome, build order), but "should agents see own scores" is largely answered by the project's own research, and the Undecided list is long (8 items).

## Step 4: Verdict
X, low confidence. Both cover nearly the same core findings with no invalid claims; X is tighter and its challenge that the existing reports are already unused is the most decision-relevant item, while Y's unique content (use planned behavioral measures, judge-taste convergence) is also good and its breadth is roughly offset by padding.

{"x_valid_nonobvious_actionable": 4, "y_valid_nonobvious_actionable": 4, "x_invalid": 0, "y_invalid": 0, "x_unique": 2, "y_unique": 2, "x_questions": 4, "y_questions": 4, "verdict": "X", "confidence": "low"}
