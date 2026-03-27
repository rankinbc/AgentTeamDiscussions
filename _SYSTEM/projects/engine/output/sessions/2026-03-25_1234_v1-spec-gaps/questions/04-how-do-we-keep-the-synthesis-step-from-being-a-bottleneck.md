# How do we keep the synthesis step from being a bottleneck?

*Generated: 2026-03-25 12:46 | Question 4 | 191s | Mode: compete*

## Decisions

1. **Synthesis receives the fragment log, not the transcript.** The full agent transcript is never passed to the synthesis call. Synthesis input is bounded to approximately 1150 tokens: the fragment log plus output format template plus word limit. This was decided in Q2 and is not reopened. Per-agent position extraction is rejected for V1 — it adds 12 modified agent calls to solve a token budget problem the fragment log already constrains.

2. **Prior design doc chain is windowed at 3.** Synthesis receives the last 3 design docs as prior context, not all prior docs. The chain grows linearly — Question 8 carries 7 prior docs before transcript arrives — and this is the actual accumulation risk. A window of 3 caps the prior-doc contribution at roughly 1,800 words regardless of session length. Earlier docs are archived in the session folder; they are not passed forward. This directly protects Morning Brief quality in longer sessions, where degradation is otherwise invisible to the builder until several sessions in.

3. **Synthesis retry policy: 2 retries, 30-second backoff, then deterministic concatenation.** If the synthesis call fails after 2 retries, fall back to deterministic concatenation of fragment fields into the three-section framing. This resolves the open question carried from Q3. The policy matches the extraction call policy. No separate configuration keys for synthesis vs. extraction retry behavior; the shared defaults apply.

4. **Per-call synthesis timeout is 60 seconds, config key `synthesis_call_timeout_seconds`.** Retry count is meaningless without a per-attempt timeout. An attempt that hangs indefinitely never exhausts retries. 60 seconds is the default. This key lives in the same config block as the retry keys. Without it, the retry policy is theater.

5. **Deterministic fallback must apply the same empty-blocker conditional as the synthesis path.** The "Don't Start Yet" section is omitted if no blockers exist — this was already decided for synthesis. The deterministic fallback path must enforce the same rule. Concatenating empty `blocker` fields produces either a blank section or undefined behavior. The conditional is one line and must be specified explicitly in the implementation rather than inferred from the happy-path behavior.

6. **Sync point uses ID-slot tracking, not task-registration tracking.** Question slots are registered by ID at session start. The sync gate waits for all slots to have a fragment or sentinel before invoking synthesis. If a slot has no fragment at sync time — because the extraction task threw before registration or was never launched — the gate writes the sentinel for that slot. The gate then operates on a complete log by construction. "Await all futures" is insufficient because futures that threw before registration are invisible to an awaiter. The slot registry is the source of truth, not the task queue.

7. **Majority-failure abort threshold is a config key, not hardcoded.** Config key: `min_success_fraction`, default `0.5`. The threshold uses strict `>`, not `>=`. One failure on a 2-question session is exactly 0.5 — this should not abort. A Morning Brief with one sentinel fragment is more useful than no Morning Brief. Hardcoding fails silently on short sessions where a single failure swings the percentage. The default of 0.5 is calibrated for a 5-question session, which is the expected common case for first-time users.

8. **Chunking and two-pass synthesis are rejected for V1.** Both approaches solve a problem not yet measured at the fragment log's actual token budget. The beta system was slow; slow is not the same as unreliable at 1150 tokens. Structural changes of this kind are deferred until evidence of failure exists.

9. **Config block for synthesis reliability contains exactly five keys.** The keys are: `synthesis_retry_count` (default 2), `synthesis_retry_backoff_seconds` (default 30), `synthesis_call_timeout_seconds` (default 60), `min_success_fraction` (default 0.5), and `prior_doc_window` (default 3). These defaults must be correct for a 5-question session without any user tuning. No additional keys are added for V1.

---

## Open Questions

- **Exact prompt template for the per-question fragment extractor.** Carried from Q2 and Q3. Not addressed in this discussion.
- **Whether the combined extraction call has its own fallback independent of the sync-gate sentinel.** The sync gate writes sentinels for missing slots, but the policy for a call that fails mid-execution versus one that never launches is not fully specified.
<!-- complete -->
