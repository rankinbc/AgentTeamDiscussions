# What is the error handling strategy?

*Generated: 2026-03-25 12:29 | Question 3 | 181s | Mode: compete*

## Decisions

1. **Three failure layers, three policies.** Failures are layer-specific. Round failures (propose/critique/evaluate) are the session's core value and get one retry. Extraction failures degrade gracefully with no retry. Synthesis failures use the existing `brief_fallback.md` path. A single retry policy across all 70+ calls is wrong — the policy must match what each layer is worth.

2. **One retry, no delay, scoped to the failing call only.** The retry budget catches transient API blips, not systemic failure. One retry per round call. If the retry fails, the round is dead. Completed rounds within the same question are not re-run. Three retries with backoff is complexity the hypothesis has no evidence to support in V1.

3. **On round failure (post-retry), the question is skipped. Exact sequence:**
   1. Write tombstone to transcript: `[ROUND FAILED: <round>, Q<n>]` — naming the specific failing round so partial records are interpretable.
   2. Stop. No extraction call. No design doc write. No synthesis call.
   3. Increment question counter. Continue to Q(n+1).

4. **`brief.md` is never touched on question failure.** The tombstone is transcript-only. The brief stays at its last valid state. A direct append to `brief.md` is a third write path that violates the established contract (synthesis overwrites `brief.md` OR writes `brief_fallback.md`). Injecting failure noise into `previous_brief` also displaces substantive decisions from the synthesis context chain. The brief is a forward-looking compression artifact, not a status log.

5. **On question failure, Q(n+1) inherits Q(n-1)'s design doc.** The context chain skips the gap. No placeholder file, no doc synthesis — pass the last successful design doc forward. This is the simplest correct mechanism for preserving context continuity across a failed question.

6. **Synthesis failure after successful rounds is covered by the existing `brief_fallback.md` mechanism.** Rounds succeeded, extraction succeeded, synthesis fails — write `brief_fallback.md`, leave `brief.md` at last valid state, session continues. No new path is needed. This case was already decided; it required only explicit confirmation that the existing fallback applies.

7. **Transcript writes are incremental, per round.** Each round result is written to disk as it completes, not batched at question end or session end. If the session dies mid-question, all completed rounds from all prior questions and the surviving rounds of the current question are already on disk. Nothing is lost on crash.

8. **Session abort after 3 consecutive question failures.** Three consecutive failures is a reliable signal that something systemic is wrong (API outage, misconfiguration, runaway error). Two is too aggressive for transient issues; unbounded is a runaway process. On abort, write a session-level error log with question indices and failure reasons.

9. **All failures are logged to `session.log` with question index and failure reason.** This costs zero tokens in the brief chain and provides the evaluator with a complete failure record. It is not a new mechanism — it is an explicit log write on every failure condition: round failure, extraction failure, synthesis failure, and session abort.

10. **`## What Got Built` is omitted when `previous_brief` is empty.** On the first question, there is no prior state to report. Including the section header with zero content is structural noise and wastes synthesis tokens. The section appears only once at least one question has completed successfully.

---

## Failure Behavior Summary

| Failure | Retry | Brief impact | Transcript | Session continues? |
|---|---|---|---|---|
| Round call fails | 1 retry, no delay | None — brief unchanged | Tombstone: `[ROUND FAILED: <round>, Q<n>]` | Yes — skip to Q(n+1) |
| Extraction fails | None | Degraded synthesis (empty arrays) | Raw evaluate output → `extraction_fallback_<n>.txt` | Yes |
| Synthesis fails | None | `brief_fallback.md` written; `brief.md` unchanged | Logged | Yes |
| 3 consecutive question failures | — | Brief at last valid state | Session abort entry | No — abort |

---

## Open Questions

*None. All open questions from this discussion are resolved.*
<!-- complete -->
