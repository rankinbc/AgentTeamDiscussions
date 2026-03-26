### The Cognitive Architect (creativity engine designer)

## Error Handling: Triage-First, Never Dark

The core principle: **every call failure produces a artifact, never a void.**

### Retry Policy (resolves open question)
Two retries, exponential backoff: 30s then 90s. After three failures, the call is dead. This applies uniformly to all LLM calls — discussion rounds, extraction, synthesis.

### Round-Level Failure
If critique or evaluate fails (after retries), the session **advances anyway**. The design doc is assembled from whatever rounds completed. A question with only a propose round produces a thin doc — but that doc is still written to disk with a `partial: true` flag in its header. Partial is not nothing.

### Question-Level Failure
If propose fails (nothing to build on), skip to question 7. But write a stub file: `q6_failed.md` containing the question text and failure log. This preserves the chain numbering for prior-doc context assembly — downstream questions see a gap, not a renumbering.

### Fragment Fallback (resolves open question)
If extraction fails, generate a deterministic stub fragment: `question_id` from the session, `decision` = "Discussion did not complete," `needs_your_call` = the question title verbatim, `blocker` = empty. This costs no LLM call and guarantees the Morning Brief has an entry for every question.

### Morning Brief Treatment
Failed questions surface under a fourth section: **"Not Completed"** — separate from "Don't Start Yet." The distinction matters: blockers are intellectual, failures are operational. Don't conflate them.

### Synthesis Failure
Already decided: deterministic fallback from fragments. No additional handling needed.

### The Flow Orchestrator (mechanical flow designer)

## Mostly Agree — One Cut, One Sequence Question

**Retry policy: accept.** 30s/90s backoff, three strikes dead. Uniform across all LLM calls is cleaner than per-call policies. No objection.

**Fragment stub fallback: accept.** Deterministic, zero cost, guarantees brief coverage. This resolves the open question cleanly.

**Cut the fourth Morning Brief section.** "Not Completed" as a distinct section adds complexity to the synthesis prompt, the fallback template, and the user's reading model — for an edge case. Failed questions already need human attention. Put them in "Needs Your Call" with an explicit `(session failure)` label. The user gets the same information, the synthesis prompt stays three sections, and the fallback path doesn't branch. The distinction between intellectual blockers and operational failures is real, but it doesn't require a new section to communicate.

**Cut `partial: true` in the doc header.** Nothing reads it in V1. If no downstream consumer acts on that flag, it's documentation noise. The stub file for a fully-failed question is sufficient; a partial doc is just a doc.

**Sequence question on question-level skip:** when propose fails after retries, what is the exact trigger that advances the session? Is it timeout expiry, exception catch, or explicit failure state? "Skip to question 7" is the right behavior — I just want the state machine to be explicit: `QUESTION_FAILED` is a terminal state for that question, not a recoverable one, and the session loop checks for it before incrementing.

The rest holds.


<!-- complete -->
