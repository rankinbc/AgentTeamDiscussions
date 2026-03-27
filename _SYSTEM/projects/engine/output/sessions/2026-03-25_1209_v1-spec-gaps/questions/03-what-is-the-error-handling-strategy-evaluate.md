### The Product Oracle (user advocate)

## The User Reads the Morning Brief at 9am. Design for That Moment.

The Adversarial Critic found the real problem. Silent corruption — confident decisions extracted from incomplete deliberation — is worse than a visible failure. A failed question produces a skip marker. A half-deliberated question produces false confidence. That's the failure mode that actually damages the user.

**What I'd decide:**

The Systems Pragmatist's transcript-level skip marker is the right fix and it's cheap. One line written to the transcript before synthesis: `[ROUND 2 SKIPPED — call failed after retry]`. The synthesizer reads it. The synthesizer knows. Cost: one conditional write. Payoff: no silent corruption.

**Cut the evaluate-turn synthesis fallback.** The Flow Orchestrator is right on this one. That's complexity serving an edge case. If synthesis fails after complete rounds, mark it, skip the brief block, continue. The transcript has everything — the user can read it.

**On retry taxonomy:** Rate-limit vs. transient matters only if we handle them differently. If both get one retry, the distinction is documentation, not code. Decide handling first, then label it. For V1: one retry for everything, immediate. Rate limits are rare in overnight runs; if they become a pattern, add delay then.

**Morning Brief:** The Adversarial Critic is right that bare failure counts are noise. But I don't want failure type tags in the brief — I want one human-readable line per failure: *"Question 6: synthesis failed after complete rounds — see transcript."* Actionable. Scannable. No new schema fields.

`rounds_skipped_count` in the header: yes. That's the signal that tells a user whether to trust the session.

### The Context Surgeon (context efficiency evaluator)

## The Information Preservation Problem Is the Real Design Question

The Pragmatist and Oracle have converged on the right tactical answer: transcript-level skip markers, one retry, no evaluate-turn fallback. I won't re-argue what's settled.

**What hasn't been said:** each `claude -p` call is stateless. Failure state lives only in files. Your recovery model is only as good as what you wrote to disk before the call died.

The write-before-call pattern solves this, but incompletely. The real question is: **what context does a resumed or synthesizing call need to reconstruct what happened?**

A bare `[ROUND 2 SKIPPED]` marker in the transcript is the minimum. But the synthesizer's prompt receives that transcript and needs to reason about it. A one-line marker is scannable by humans. Is it unambiguous to the model? "Round 2 skipped" doesn't say whether the proposer turn completed before the skip. That distinction changes what the synthesizer can legitimately conclude.

**Proposed marker format — no new schema, just precision:**

```
[ROUND 2 SKIPPED — proposer completed, critique call failed after 1 retry]
```

Two bits of extra information. Cost: ~10 tokens per failure. Payoff: the synthesizer gets accurate completeness signal, not just a gap marker.

**On `rounds_skipped_count` in the header:** yes, but only if the synthesizer prompt also receives it. Header fields that only humans read are documentation, not control flow. If it's not wired into anything, cut it from the schema until it is.

Cut complexity. Preserve precision. The token cost of a well-formed error marker is trivial. The cost of a synthesizer hallucinating completeness from an ambiguous gap is not.


<!-- complete -->
