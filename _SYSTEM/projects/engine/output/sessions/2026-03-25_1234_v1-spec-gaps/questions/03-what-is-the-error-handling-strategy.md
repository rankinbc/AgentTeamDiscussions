# What is the error handling strategy?

*Generated: 2026-03-25 12:42 | Question 3 | 160s | Mode: compete*

## Decisions

1. **Retry taxonomy is two-policy, not one.** Transient failures (timeout, 5xx) use 2 retries with 5-second fixed backoff. Rate limit failures (429) use 2 retries with exponential backoff plus jitter, respecting the `retry-after` header when present. These are two config keys in one block. Uniform retry policy across all call types is rejected; identical handling of rate limits and transient failures risks retry storms that worsen the original condition.

2. **Round-level failure produces a partial transcript and a tombstone design doc.** If any round after propose fails after retries, the session saves whatever transcript exists and writes a tombstone design doc rather than a full design doc. The transcript is evidence and is never discarded. The tombstone contains one sentence identifying the question, the failure type, and a statement that downstream questions lack this context. One sentence is sufficient — the synthesizer reads it, not the user.

3. **Question-level failure (propose fails) produces a tombstone design doc, not a stub file.** When propose fails after retries, the session writes a tombstone design doc explicitly stating the question was not resolved and that the context chain has a known gap at this position. This is not renamed or numbered differently — it occupies the question's slot in the prior-doc chain so subsequent questions receive an explicit signal rather than a silent omission. A separate stub file is not written; the tombstone is the record.

4. **`QUESTION_FAILED` is a terminal state.** It is not recoverable after retries are exhausted. The session loop checks for this state before advancing to the next question. The tombstone is written as part of the transition into this state.

5. **Context chain poisoning is the primary blast radius.** The tombstone design doc is the sole mitigation. Subsequent questions receive it as prior context; the chain is broken but the break is legible. "Skip and continue silently" is rejected. Downstream questions that reason from a named gap produce worse output than downstream questions that reason from no gap, but they do not produce silently corrupted output.

6. **Fragment fallback on combined extraction call failure uses the Cognitive Architect's sentinel, not null fields.** If the combined extraction call fails after retries, write a sentinel fragment with: `question_id` from the session, `decision: "[extraction failed]"`, `needs_your_call`: the question title verbatim, `blocker`: empty string. The question title is the call to action and must not be discarded. `null` fields risk silent omission at synthesis time. Extraction is skipped entirely for a tombstoned question; the sentinel is only for questions where rounds succeeded but extraction failed.

7. **Retry policy for the combined extraction call: 2 retries, 30-second backoff.** This resolves the open question carried from Q2. The policy applies to both outputs of the combined call (fragment and decisions entry). On failure after retries, log with `question_id`, write the sentinel fragment, omit that question's decisions.json entry, and continue.

8. **`partial: true` header flag is not written.** No downstream consumer reads it in V1. A partial design doc is a doc; a tombstone design doc is a tombstone. The distinction is communicated by content, not metadata.

9. **The Morning Brief uses three sections only.** "Not Completed" as a fourth section is rejected. Failed questions surface in "Needs Your Call" with a `(session error)` label. The distinction between intellectual blockers and operational failures is real but does not require a separate section to communicate. The user's reading model stays constant regardless of session health.

10. **If more than half the questions fail, do not produce the Morning Brief.** Write a single-line error file in its place. A Brief assembled from a majority of tombstones and sentinel fragments is not a Brief — it is noise formatted as output. The session never exits without either a `morning_brief.md` or an `error.md`; one or the other is always written.

11. **Synthesis failure with all rounds succeeded falls to the existing decided fallback.** Direct concatenation of fragment fields into three-section framing. No additional handling is required here.

## Resolved Open Questions

- **Retry policy for the combined extraction call:** 2 retries, 30-second backoff. Decided above.
- **Fragment fallback if combined call fails:** Sentinel fragment using question title verbatim in `needs_your_call`. Decided above.

## Open Questions

- **Exact prompt template for the per-question fragment extractor** (carried from Q2, still unresolved).
- **Retry policy for the synthesis call** before falling back to deterministic concatenation (two retries with 30-second backoff recommended but not yet decided).
- **Threshold configuration for the majority-failure abort rule** — whether the "more than half" threshold is hardcoded or a config key.
<!-- complete -->
