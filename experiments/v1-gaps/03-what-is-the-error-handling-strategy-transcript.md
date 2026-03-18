# Transcript: What is the error handling strategy?

*Generated: 2026-03-18 03:54*

## Round: PROPOSE

### The Cognitive Architect (creativity engine designer)

# Error Handling Strategy

## The Core Principle: Never Lose Completed Work, Never Block on Failed Work

Every successful LLM call writes its output to disk immediately. Not buffered, not batched -- written. If the process dies at call 47, calls 1-46 are intact on disk. This is non-negotiable.

## Retry Policy: One Retry, Then Classify and Move On

Each CLI call gets exactly one retry with a 30-second backoff. Two attempts total. Why not three? Because at 70+ calls, aggressive retry turns a rate-limit hiccup into a cascade that burns your entire overnight window on one stubborn question.

## Failure Classification

**Round failure** (propose/critique/evaluate fails): Skip that round, mark the question as `partial`. The synthesizer receives whatever rounds completed. A question with only propose + critique but no evaluate still produces a design doc -- just a weaker one.

**Synthesis failure** (all rounds succeeded, synthesis fails): This is the one case worth a second retry. The rounds are the expensive work. Retry synthesis twice more (three total). If it still fails, write rounds to disk as `raw_rounds.md`. The human gets the ingredients without the meal.

**Extraction failure** (decisions/open_questions extraction fails): The design doc exists. The Morning Brief proceeds without that question's extractions. The brief lists it under a new section: `## Incomplete Extractions`.

**Question-level skip**: If propose fails on both attempts, skip the entire question. Log it. Continue to question 7.

## Morning Brief Contract

The brief adds one section when failures occurred:

```
## Session Gaps
- Q6: Synthesis failed. Raw rounds saved. Read raw_rounds.md.
- Q8: Extraction incomplete. Read design doc directly.
```

No gaps section when everything succeeded. Its presence alone is the signal.

## What the Orchestrator Tracks

A `session_status.json` written after each question completes:

```json
{
  "q6": {
    "status": "partial",
    "completed_rounds": ["propose", "critique"],
    "failed_step": "evaluate",
    "artifacts_saved": ["design_doc_partial.md", "raw_rounds.md"]
  }
}
```

The Morning Brief generator reads this file to build the gaps section. No inference required.

### The Flow Orchestrator (mechanical flow designer)

## Error Handling Strategy

### One Retry, Then Skip

Every CLI call gets exactly one retry with no backoff. If the retry fails, that step is marked `failed` and the orchestrator moves forward. No exponential backoff, no retry queues, no circuit breakers. At V1 scale, a second failure on the same call means the problem isn't transient.

### Failure Granularity is the Round, Not the Question

If propose fails, skip the entire question -- critique and evaluate have no input. If critique fails, run evaluate with only the proposal (degraded but usable). If evaluate fails, the proposal and critique still have value. If synthesis fails, the three rounds are still saved.

**Rule: always save what succeeded.** Every completed round writes its output immediately. No buffering until question completion.

### Partial Questions Get Marked, Not Hidden

The session folder gets a `status.json`:

```json
{
  "q3": {"status": "partial", "failed_step": "synthesis", "completed": ["propose", "critique", "evaluate"]},
  "q6": {"status": "skipped", "failed_step": "propose", "completed": []}
}
```

### Extraction Skips Failed Questions

No extraction attempt on questions missing synthesis. The Morning Brief input contract already handles missing rounds -- it proceeds without them.

### Morning Brief Reports Gaps

Add one section to the brief template:

```
## Incomplete Questions
Questions where failures prevented full processing.
State which step failed and what output is available.
```

### What We're Not Building

No dead-letter queues. No post-session retry jobs. No health checks between questions. The human reads the Morning Brief, sees the gaps, re-runs if they care.

## Round: CRITIQUE

### The Systems Pragmatist (infrastructure realist)

## CRITIQUE - The Systems Pragmatist

Both proposals agree on the fundamentals: write immediately, don't block on failures, track status in JSON. Good. Let me focus on where they diverge and where both miss.

**Retry policy**: Cognitive Architect wants 30-second backoff with one retry. Flow Orchestrator wants no backoff. Neither is thinking about *why* the call failed. A rate-limit 429 with a `retry-after` header is a different animal than a malformed response or a timeout. One retry with zero backoff will hit the same rate limit. One retry with 30 seconds wastes time on a genuine model error. Read the exit code. If it's rate-limiting, wait. If it's anything else, skip immediately.

**Synthesis getting extra retries**: Cognitive Architect gives synthesis three total attempts. Justified reasoning -- rounds are expensive. But this is a policy exception that complicates the retry logic for one edge case. At V1, keep it uniform. If synthesis fails, save the rounds. The human has the material.

**The real gap neither addresses**: What happens when the CLI hangs? Not fails -- *hangs*. A stuck process burns the overnight window worse than any failure. Every call needs a timeout. 120 seconds, kill it, count it as a failure. Without this, your "guaranteed to finish by morning" promise is hollow.

**Status file timing**: Both write status per-question. Write it per-*round*. If the process crashes between round 2 and round 3, per-question status tells you nothing about what's on disk.

**Agreement**: Immediate writes, skip-and-continue, structured gap reporting in the brief. These are settled.

The timeout omission is the critical gap. Everything else is tuning.

### The Adversarial Critic (adversarial reviewer)

# CRITIQUE - The Adversarial Critic

Both proposals agree on the fundamentals: save immediately, retry minimally, skip and continue. Good. But the convergence masks unresolved gaps.

**The backoff disagreement matters.** Architect says 30-second backoff. Orchestrator says none. If the failure is a rate limit -- the most likely failure mode at 70+ calls -- zero backoff guarantees the retry fails too. You've burned your one retry for nothing. But 30 seconds times many failures adds up. Neither proposal models the actual failure distribution. What percentage of failures at this scale are rate limits vs. malformed output vs. timeouts? Without that, the retry policy is a guess wearing confidence.

**"Degraded but usable" is unvalidated.** Orchestrator claims running evaluate with only the proposal (no critique) produces degraded-but-usable output. Based on what? The evaluate prompt expects critique input. Feed it nothing and you get either a hallucinated critique response or a confused evaluation. Has anyone tested this degraded path? If not, it's aspirational, not a strategy.

**Synthesis gets special treatment without justification.** Architect gives synthesis three total attempts while everything else gets two. The argument -- "rounds are the expensive work" -- is about sunk cost, not success probability. If synthesis failed once, why would attempt three succeed? Same input, same prompt, likely same result.

**Neither addresses malformed output.** What happens when the call succeeds but returns unparseable JSON or off-schema content? That's not a retry problem -- it's a validation problem that both proposals ignore entirely.

The save-immediately principle is sound. The retry policies need grounding in actual failure modes, not intuition.

## Round: EVALUATE

### The Product Oracle (user advocate)

# EVALUATE - The Product Oracle

The user's job: wake up, spend 5 minutes, know what happened overnight. Every error handling decision flows backward from that.

**Immediate writes: settled.** Both proposers, both critics agree. Non-negotiable. Moving on.

**Retry policy: follow the exit code.** Systems Pragmatist nailed it. Rate limit? Wait. Everything else? Skip. This isn't splitting the difference -- it's the only policy that respects *why* the call failed. Zero backoff wastes retries. Fixed backoff wastes time. Read the signal.

**No special treatment for synthesis.** The sunk cost argument doesn't survive scrutiny. Same input, same prompt, third attempt adds hope, not probability. Save the rounds. The human has the raw material. They'll decide if it's worth re-running.

**Timeouts are mandatory.** The Pragmatist's gap catch is the most important contribution in this critique round. A hung process is worse than a failed one. 120-second kill timer on every call. This is a requirement, not a nice-to-have.

**Drop the degraded-round path.** Running evaluate without critique input is untested and the prompts aren't designed for it. If critique fails, save what you have, mark it partial. Don't feed malformed input chains forward hoping for the best.

**Add output validation.** The Adversarial Critic is right -- a 200 response with garbage JSON is a failure. Validate schema before writing. Failed validation counts as a failed call.

**Status written per-round, not per-question.** Crash recovery needs to know what's actually on disk.

The Morning Brief gap section is the user's contract. Present when needed, absent when not. That asymmetry *is* the UX.

### The Context Surgeon (context efficiency evaluator)

## EVALUATE - The Context Surgeon

The critics sharpened three real issues. Let me score what survives.

**Settled (implement as stated):**
- Write every completed round to disk immediately. Universal agreement, zero dissent.
- Skip-and-continue at question level when propose fails. No path forward without it.
- `status.json` tracking completed rounds and failure points.
- Morning Brief gap reporting section. Present only when failures occurred.

**Resolved by critique:**
- **Timeouts.** Pragmatist is right -- a hanging process is worse than a failed one. 120-second kill timer per call. This was the genuine blind spot.
- **Uniform retry policy.** Drop the synthesis special case. One retry, uniform. Architect's sunk-cost argument doesn't change success probability on attempt three.
- **Per-round status writes.** Write status after each round, not per-question. Crash recovery needs to know what's on disk.

**Needs specification:**
- **Backoff strategy.** Critic nailed it: read the exit code. Rate-limit (429 or equivalent) gets a 30-second wait. Any other failure skips immediately. This isn't complex branching -- it's one conditional.
- **Malformed output validation.** Adversarial Critic's strongest point. A "successful" call returning garbage is worse than a clean failure. Basic schema validation on JSON outputs, structure check on markdown. Fail validation = count as failure, enter retry path.

**Rejected:**
- Running evaluate without critique input. Untested degraded path. If critique fails, mark question partial with propose-only output. Don't feed broken inputs downstream.

**Context cost note:** The status.json schema from both proposals carries ~200 tokens per question. At 10 questions, that's 2K tokens feeding the brief generator. Well within budget. No compression needed.
