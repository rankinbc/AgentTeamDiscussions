### The Adversarial Critic (adversarial reviewer)

## Adversarial Critic: The Proposal Has a Structural Hole

The Flow Orchestrator's incremental append model sounds clean. It isn't.

**Five problems before anyone ships this:**

**1. Garbage in, garbage out — compounded.** The micro-brief prompt feeds on synthesis output. If synthesis round 3 is weak (rushed, truncated, low-signal), the micro-brief inherits that weakness. There's no quality gate. You're automating the transcription of mediocre output into the one artifact the user actually reads.

**2. "500-token excerpt" is unspecified.** First 500 tokens? Last 500? A summary? This detail determines whether the micro-brief captures the real decision or the preamble. Nobody has defined the selection logic.

**3. Appended bullets ≠ coherent brief.** Ten questions × 3-5 bullets = an unstructured list. The user opens it at 8am and reads... what, exactly? No narrative thread, no priority ordering, no signal about which questions matter most. The assembly step was doing real work — synthesizing *across* questions — and it just got silently dropped.

**4. The "fail: block or skip?" question was raised and left open.** That's not a flag, that's a blocker. If you skip, the brief has silent gaps. If you block, a transient API failure corrupts the session. Neither answer is in the design.

**5. Ordering dependency is baked in.** Question 1's micro-brief is written without knowing what questions 2-10 will surface. A critical risk that only emerges in question 7 won't appear in earlier bullets. The brief is structurally biased toward early-session concerns.

The incremental model solves context overflow. It doesn't solve coherence.

### The Systems Pragmatist (infrastructure realist)

## Systems Pragmatist: The Critic Is Right, But Drawing the Wrong Conclusion

The Adversarial Critic landed real hits. But the conclusion should be "fix the incremental model," not "resurrect the assembly step."

**The assembly-at-end call is the worst possible failure mode.** Session runs for 4 hours overnight. User goes to sleep. Final call fails — API timeout, context overflow, rate limit. Morning Brief: null. That's not a degraded experience, that's a broken promise at the exact moment the user most needs the artifact.

**Incremental with a defined answer to each critique:**

**On "500 tokens unspecified":** Last 500 tokens of synthesis output. Not first, not summarized — the tail of the synthesis is where convergence lands. One-line implementation decision, commit to it.

**On "appended bullets ≠ coherent brief":** Correct. So the micro-brief prompt does light framing work: `[Question N: {title}] decision: X. risk: Y.` The brief reads as a structured list per question, not free bullets. Coherence across questions is a V2 concern — don't let perfect kill shipped.

**On "block or skip":** Skip with a visible marker. `[Q3 brief generation failed — see transcript]`. Silent gaps are worse than honest gaps.

**On ordering dependency:** This is real and unsolvable incrementally. Accept it. Questions are ordered by the user's brief — earlier questions are structurally more important. If question 7 surfaces a critical risk, the transcript exists.

**The assembly step solves coherence at the cost of catastrophic tail failure. That's the wrong trade.**


<!-- complete -->
