# How does prior context get managed as questions accumulate?

*Generated: 2026-03-25 12:49 | Question 5 | 157s | Mode: compete*

## Decisions

1. **Prior design doc chain uses a sliding window of 3, verbatim, tombstones included.** Question N receives the three most recent design docs by slot position as prior context. Earlier docs are archived in the session folder and not passed forward. Tombstones occupy their slot in the chain and are never skipped — the tombstone's one-sentence content explicitly signals the gap to downstream agents. Silently skipping a tombstone and pulling an earlier doc re-introduces the invisible-failure problem already resolved at the session level. Summarization is rejected: it adds a lossy LLM call to every question transition, compounds errors across 10 questions, and solves a problem that does not exist at this scale. The window of 3 was established in Q4 and is not reopened.

2. **Context assembly for question N reads design docs from disk directly; the fragment log feeds synthesis only.** Async fragment extraction means "doc written to disk" and "fragment appended to log" are not atomic events. The fragment log can lag the design doc. Context assembly and synthesis are different consumers with different read targets. Reading the prior-doc window from the fragment log introduces a predictable interleaving failure. Reading docs from disk by slot position is the correct path. These two consumers must not be conflated in the implementation.

3. **Prior doc injection format: labeled header per doc, deterministic, no LLM involvement.** Each doc in the window is prefixed with `## Prior Context: Question {id} — {title or FAILED}`, newline-separated. Raw concatenation of three unlabeled docs causes proposing agents to lose track of which context belongs to which question, producing muddier reasoning, muddier fragments, and a weaker Morning Brief. The labeled header is 10 tokens, survives any per-doc truncation, and is the minimum viable spec for avoiding context corruption. This is not a prompt template detail — it is a context integrity requirement. It is decided here.

4. **Per-doc token cap added to the prior-doc window spec: `prior_doc_max_tokens`, default 500.** A window of 3 docs with no per-doc size cap is a count constraint, not a token budget. Three docs at 800 words each contribute approximately 3,200 tokens to every downstream agent call. This is a different budget line from synthesis input (bounded at ~1,150 tokens by fragment log design), and the two must not be conflated. Each doc in the window is truncated to 500 tokens if it exceeds that limit. Truncation direction is bottom-up: rationale is dropped before conclusions. The labeled header is not subject to the cap. This config key joins the existing synthesis config block.

5. **Consecutive tombstone scenario is a session-abort concern, not a window design flaw.** If questions 5, 6, and 7 all tombstone, the session is at or below the `min_success_fraction` abort threshold for most session lengths and should not reach question 8. If it does, that is a config miscalibration. The window design is not responsible for masking session-level failure; `min_success_fraction` is. The window passes what it receives — tombstones included — and does not attempt to detect or compensate for consecutive failure patterns. Compensating logic in the window would duplicate session-abort responsibility and create two code paths with divergent behavior.

6. **Config block for prior-doc context management contains exactly two keys: `prior_doc_window` (3) and `prior_doc_max_tokens` (500).** `prior_doc_window` was established in Q4. `prior_doc_max_tokens` is added here. These two keys join the existing synthesis reliability config block containing `synthesis_retry_count`, `synthesis_retry_backoff_seconds`, `synthesis_call_timeout_seconds`, and `min_success_fraction`. No additional keys are introduced for window behavior. Window size is adjustable without code changes; the builder tunes it by editing config.

7. **The fragment extractor prompt template is unresolved and is the primary implementation blocker.** Every prior round has noted it as open. It has not been drafted. The template requires exactly four extraction targets — `question_id`, `decision`, `needs_your_call`, `blocker` — each constrained to one sentence, with classification rules for the confidence enum embedded in the extraction instructions. It is a 15-line prompt. Carrying it as an open item past this question is pure context overhead. This question does not resolve it — the window discussion is orthogonal — but it must be the first item addressed in the next question, not deferred again.

---

## Unresolved Open Questions

- **[from Q2, Q3, Q4, Q5] Exact prompt template for the per-question fragment extractor.** Still unresolved. Blocks implementation. Must be addressed next — not deferred.
- **[from Q4] Whether the combined extraction call has its own fallback independent of the sync-gate sentinel.** The sync gate writes sentinels for missing slots at sync time, but the policy for a call that fails mid-execution versus one that never launches remains unspecified.
- **[from Q5] Whether `prior_doc_max_tokens` triggers a warning log when truncation occurs.** Not decided. Recommended: log truncation events with question_id and token count for observability, but this is not a blocker.
- **[from Q5] Actual distribution of design doc lengths in the beta system.** The 500-token default is a reasonable prior. Instrumenting 10 beta runs to validate it is the right long-term action but is not a prerequisite for shipping the window implementation.
<!-- complete -->
