### The Adversarial Critic (adversarial reviewer)

The sliding window of 3 is decided. Stop re-proposing it.

Here are the actual failure modes nobody has addressed:

**1. Tombstones poison the window disproportionately.**
Window slots are 3. If questions 5, 6, 7 all tombstone, the window for question 8 contains three one-sentence failure notices and zero substantive context. The agent proceeds with effectively no prior context. This isn't a gap — it's a silent context collapse that looks identical to a healthy window. The downstream agent has no way to distinguish "prior questions resolved cleanly" from "prior questions all failed."

**2. Window position 3 is an unvalidated assumption.**
Why 3? The prior doc says it "caps prior-doc contribution at roughly 1,800 words." That calculation assumes average design doc length. What's the actual distribution? A question that resolves in one round produces a short doc. A question that hits retry limits and partial rounds produces a tombstone. The 1,800-word estimate could be off by 3x in either direction. This has never been measured against the beta system's actual outputs.

**3. The inject format is unspecified and consequential.**
The Flow Orchestrator correctly flags this as unresolved. Unlabeled raw concatenation of three docs will cause the proposing agent to lose track of which context belongs to which question. This isn't a prompt template detail — it's a context corruption risk.

**4. "Written design docs by slot position" has a race condition.**
Async extraction means a design doc could be written but its fragment not yet appended. The window reads the doc; the fragment log lags. These diverge silently.

The prompt template for context injection needs to be decided now, not deferred again.

### The Systems Pragmatist (infrastructure realist)

The Adversarial Critic's point 1 is real but the response to it is wrong.

**Consecutive tombstone scenario:** Three tombstones in the window is a symptom, not a failure mode. The actual failure mode is that the session didn't abort when it should have. `min_success_fraction` exists precisely for this. If questions 5, 6, and 7 all fail, you're already at or below the abort threshold for most session lengths. The session shouldn't reach question 8. If it does, that's a config miscalibration, not a window design flaw.

**The race condition (point 4) is the real issue.** Async fragment extraction means "doc written to disk" and "fragment appended to log" are not atomic. The window reads the doc. The prior-doc chain and the fragment log can diverge. This isn't theoretical — it's a predictable interleaving failure. The fix is straightforward: context assembly for question N reads docs from disk directly, not from the fragment log. The fragment log feeds synthesis only. These are different consumers. Don't conflate them.

**The inject format cannot be deferred again.** Raw concatenation is a context corruption vector. Minimum viable spec: each doc prefixed with a labeled header (`## Prior Context: Question {id} — {title or FAILED}`), newline-separated. That's it. One line per doc, deterministic, no LLM involvement. This is an implementation detail that becomes a debugging nightmare if left unspecified.

**Window size of 3:** The 1,800-word estimate is untested. Instrument the beta system. Measure actual doc lengths across 10 runs before assuming the window holds.

Prompt template is still open. That's the blocker.


<!-- complete -->
