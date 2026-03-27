# Transcript: What is the error handling strategy?

*Generated: 2026-03-25 12:29*

## Round: PROPOSE

### The Cognitive Architect (creativity engine designer)

## Error Handling: Layer-Aware Blast Radius

The key insight is that failure modes have different blast radii. One retry policy for 70 calls is wrong. The policy should match what each layer is worth.

**Three failure layers, three policies:**

**Round failures (propose/critique/evaluate):** These are the session's core value. One retry with 15-second backoff. If retry fails, write a tombstone entry to the transcript — `[ROUND FAILED: propose, question 6]` — and skip that question entirely. Do not attempt extraction or synthesis on partial round output. The tombstone is the record.

**Extraction failures:** Already decided — degrade gracefully (empty arrays, log raw output). No retry. The extraction call is cheap enough that a second attempt on malformed JSON rarely recovers.

**Synthesis failures:** Already decided — `brief_fallback.md`, never corrupt `brief.md`. Design doc still writes. Session continues from last valid brief state.

**Transcript writes are incremental, per round, not per question.** If the session dies at question 6, rounds 1–5 and completed rounds of question 6 are already on disk. Nothing is lost. This is the most important single implementation decision here.

**Morning Brief on failed questions:** Include a one-line tombstone in `## Still In Play` — *"Question 6 failed before extraction — [topic] is unresolved."* The chain needs to know the gap exists or downstream synthesis halts confabulate an answer.

**First-call behavior resolution:** When `previous_brief` is empty, omit `## What Got Built` entirely. Including it with zero content produces structural noise.

### The Flow Orchestrator (mechanical flow designer)

## Agreed on Layers. One Sequence to Pin Down.

The three-layer policy is correct. I won't re-argue it. What's missing is the exact state machine for "skip question" — because "skip" is ambiguous until you trace what does and doesn't run.

**Exact sequence on round failure (post-retry):**

1. Write tombstone line to transcript: `[ROUND FAILED: propose, Q6]`
2. **Stop.** No extraction call. No design doc write. No synthesis call.
3. Append tombstone to `## Still In Play` in current `brief.md` via direct file append — **not** a synthesis call.
4. Increment question counter. Continue to Q7.

That last point matters: the tombstone brief update is a file write, not an LLM call. Calling the synthesizer on a failed question is backwards — you'd be feeding it incomplete data to produce a brief update that should be a static string. The tombstone text is deterministic. Write it directly.

**Retry scope:** Retry applies to the specific failing round call only. If `propose` fails and retries successfully, `critique` runs normally. Don't re-run completed rounds.

**First-call behavior:** Agree — omit `## What Got Built` when `previous_brief` is empty. Mark this **DECIDED**.

**One flag:** The proposal says "write tombstone to transcript per round" but also "skip that question entirely." If `propose` succeeds and `critique` fails, the propose output is already on disk. The tombstone should name the failing round specifically — `[ROUND FAILED: critique, Q6]` — so the partial record is interpretable.

## Round: CRITIQUE

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

## Round: EVALUATE

### The Product Oracle (user advocate)

## Evaluate: The User Wakes Up to a Brief, Not a Status Page

The three-layer policy is correct and should be decided as-is. The debate worth resolving is what the Morning Brief says about failure — because that's the only failure artifact the user actually reads.

**Resolve first-call behavior now: DECIDED — omit `## What Got Built` when `previous_brief` is empty.** Both proposers agreed. Empty structural scaffolding is noise. Close it.

**On the brief and failed questions:** The Pragmatist says don't touch `brief.md`. The Architect says write a tombstone to `## Still In Play`. The Pragmatist wins on mechanism — direct append violates the write contract. But the Architect wins on intent — a user reading the brief shouldn't believe Q6 was answered when it wasn't. 

Resolution: tombstone is **transcript-only** for V1. The brief stays at last valid state. The user who wants to understand gaps reads the transcript. The brief remains clean and contractually intact. This is acceptable for a solo builder running overnight experiments — they'll check the transcript when something looks thin.

**Context chain gap:** Inherit last successful design doc. The Pragmatist named the simplest correct mechanism. Decide it.

**Retry budget:** One retry, no delay. The Pragmatist is right — we're catching blips, not building SLAs.

**Session abort:** Three consecutive failures. Reasonable signal that something systemic is wrong.

**Synthesis failure after successful rounds:** The existing fallback (`brief_fallback.md`) covers this. Say so explicitly and close the open question.

Five decisions ready to land. No new complexity introduced.

### The Context Surgeon (context efficiency evaluator)

## Evaluate: Five Decisions Land. One Context Efficiency Note.

The Oracle correctly enumerated five ready decisions. The Pragmatist named the right mechanisms. I'll validate and add one efficiency point, then close.

**DECIDED: Omit `## What Got Built` when `previous_brief` is empty.** Empty scaffolding is structural noise and wastes synthesis tokens. Both proposers agreed. Closed.

**DECIDED: On question failure, `brief.md` is not touched.** Tombstone is transcript-only. The brief stays at last valid state. The append-to-brief path violates the write contract and — critically — injects failure noise into the synthesis context chain. Every token spent on tombstone language in `previous_brief` is a token displaced from substantive decisions. The brief is a forward-looking compression artifact, not a status log.

**DECIDED: On question failure, Q(n+1) inherits Q(n-1)'s design doc.** Skip the gap in context. Simplest correct mechanism.

**DECIDED: One retry, no delay.** Transient blip recovery only.

**DECIDED: Abort after 3 consecutive failures.** Systemic failure signal.

**DECIDED: Synthesis failure after successful rounds is covered by the existing `brief_fallback.md` mechanism.** No new path needed. Close the open question.

**One context note:** When Q6 fails, the evaluator's scoring will incorrectly treat Q6 as absent rather than failed. Log the failure to `session.log` with question index and failure reason. This costs zero tokens in the brief chain and gives the evaluator the signal it needs. Not a new mechanism — just an explicit log write.

Six decisions. No open questions remaining on this topic.

<!-- complete -->
