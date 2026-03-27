### The Adversarial Critic (adversarial reviewer)

## Five Unaddressed Failure Modes in the Current Proposal

The Flow Orchestrator's tombstone approach has clean instincts but skips the hard cases. Here's what breaks:

**1. The context chain gap is unaddressed.**
Prior decisions: design docs chain forward as context for subsequent questions. If Q6 fails and produces no design doc, Q7 runs with a hole in its context window. "Increment counter, continue" pretends this is fine. It isn't. Either Q7 gets stale context (Q5's doc) or no context — neither is specified. This is the most consequential failure mode and nobody has named it.

**2. "Retry" is undefined.**
How many retries? Fixed delay or backoff? Does a timeout count as failure or get its own retry budget? "Retry applies to the specific failing round call" is a policy without a mechanism. One retry? Three? This needs a number.

**3. Two write mechanisms for brief.md is a contract violation.**
The decided contract: synthesis overwrites brief.md OR writes brief_fallback.md. The tombstone-via-direct-append is a third path that bypasses both. Now brief.md can be in a state no part of the system produced intentionally. That's how corruption enters.

**4. Synthesis failure after all rounds succeed is unaddressed.**
The question explicitly asks about this case. The proposal doesn't touch it. Rounds succeeded, extraction succeeded, synthesis fails — do we ship the session without a brief update for that question? That's the decided fallback path (brief_fallback.md), but nobody said so.

**5. "Failures are guaranteed" but retry budget isn't bounded.**
A flaky API under load could cause every question to exhaust retries. What's the session-level abort condition?

Resolve the context chain gap first. Everything else is recoverable. That one isn't.

### The Systems Pragmatist (infrastructure realist)

## The Critic is Right. Here's the Minimal Fix.

The context chain gap is the only genuinely unrecoverable failure. Address it first with the simplest mechanism: **on Q6 failure, Q7 inherits Q5's design doc.** The context chain skips the hole. No doc synthesis, no placeholder file — just pass the last successful doc forward. This is already implicit in how the chain works; the proposal just needs to say it explicitly.

**Retry budget:** One retry, no delay. That's it for V1. The goal is catching transient API blips, not building SLA-grade resilience. If the retry fails, declare the round dead and move on. Three retries with backoff is complexity the hypothesis doesn't require evidence for yet.

**Direct append is wrong.** The Critic is correct — two write paths for brief.md is a contract violation. Kill the tombstone-via-append. The clean rule: on question failure, **brief.md is not touched.** The previous brief remains valid. The tombstone is transcript-only. The brief doesn't acknowledge the failure at all — it just doesn't advance. This is simpler and preserves the contract.

**Synthesis failure after successful rounds:** Already decided — write brief_fallback.md. This case needs no new mechanism, just needs someone to say "yes, the existing fallback covers this exact scenario."

**Session abort:** If 3 consecutive questions fail, abort with a session-level error log. Not 2 (that's too aggressive for transient issues), not unbounded (that's a runaway process).

The complexity ceiling for V1 error handling should be: one retry, one fallback file, skip-and-continue. Everything else is scope creep.


<!-- complete -->
