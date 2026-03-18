# Transcript: How do we keep the synthesis step from being a bottleneck?

*Generated: 2026-03-18 03:56*

## Round: PROPOSE

### The Cognitive Architect (creativity engine designer)

## The Retry IS the Degradation

Don't add a mechanism. Repurpose the one you have.

D4 already gives you one retry per call. Make synthesis's retry a **different prompt**, not the same prompt again. First attempt: full context, full fidelity. If it fails or times out, the retry sends a **compressed input** — just the propose-round positions and critic objections as bullet points, no full transcripts. The orchestrator builds this compressed version *before* the first attempt, so it's ready instantly on failure.

This produces two tiers of design doc from the same retry policy:

- **Full synthesis**: Coherent narrative integrating all rounds. The good outcome.
- **Skeleton synthesis**: Structured decisions with rationale bullets. Less elegant, fully functional. Every downstream consumer (extraction, Morning Brief) still gets what it needs because the schema doesn't require prose — it requires positions and classifications.

Why this beats the alternatives:

**Two-pass** doubles the call count for synthesis on *every* question, burning budget even when the single call would have succeeded. You're optimizing for the failure case at the cost of the common case.

**Chunking** breaks cross-agent coherence — the entire point of synthesis is to reconcile contradictions *between* agents. Split it and you get summaries, not synthesis.

**Accepting degraded output** is what this does, but *only on failure*, and the degradation is controlled — you designed the fallback prompt, not the model's truncation behavior.

The compressed input is ~40% of the original token count. Well within the comfort zone for a single call. The skeleton doc is worse writing but equivalent signal.

### The Flow Orchestrator (mechanical flow designer)

## Synthesis Bottleneck

### D1: Accept the Single-Pass Call as Default

Synthesis is one `claude -p` call. It already gets one retry per D4. Don't add a two-pass outline-then-fill approach. That doubles the call count for every question, doubles the failure surface, and the outline pass can fail too. You haven't removed a bottleneck -- you've created two.

Chunking is worse. You split input, now you need a merge step. The merge step is just synthesis again with extra coordination problems.

### D2: Fallback to Truncated Input on Retry

When synthesis fails its first attempt, the retry does not resend the same payload. Instead:

1. Strip the propose round entirely (the critique and evaluate rounds already subsume it).
2. Strip prior design doc context beyond the immediately preceding question.
3. Retry with this reduced input.

This cuts token count by roughly 40% without architectural changes. The orchestrator already has the individual round files on disk (per D1 from error handling). Building the truncated payload is string concatenation, not a new subsystem.

### D3: No Degraded-Output Mode

If synthesis fails both attempts, mark the question as `partial` in `session_status.json` and move on. The individual round outputs are already on disk. A human can read propose/critique/evaluate and synthesize manually. Emitting a "degraded synthesis" creates a file that looks authoritative but isn't -- worse than an honest gap.

### What This Doesn't Do

No new call types. No new retry policies. No new file formats. One conditional branch in the retry path: if step is synthesis, truncate input before retry. Everything else is already built.

## Round: CRITIQUE

### The Systems Pragmatist (infrastructure realist)

## CRITIQUE — The Systems Pragmatist

Both proposals converge on the same mechanism: retry with truncated input. Good. That's a signal, not a coincidence. Let me stress-test the differences.

### The "Skeleton Synthesis" Is a Liability

Cognitive Architect wants the retry to use a *different prompt* producing a structurally different document. Now you have two output formats downstream consumers must handle. The extraction prompt expects a synthesis section with specific linguistic markers for commitment classification. A bullet-point skeleton changes the surface the extractor reads. You either write a second extraction prompt or accept misclassification. Neither is free.

Flow Orchestrator's approach is cleaner: same prompt, less input. The output format doesn't change. Extraction doesn't care.

### Pre-Building the Compressed Input Is Correct

One point from Cognitive Architect worth keeping: build the fallback payload *before* the first attempt. If you wait until failure, you're doing string manipulation inside an error handler. Do it upfront, discard it on success. Cheap insurance.

### "No Degraded Output" Is the Right Default

Flow Orchestrator says mark it `partial` and move on. Correct. A missing synthesis with intact round files is an honest signal. A skeleton doc that *looks* complete but was generated from 40% of context is a subtle lie. The Morning Brief consumer can flag a `partial` question. It cannot flag a plausible-looking doc built from incomplete input.

### The Actual Risk Nobody Mentioned

What happens when the *reduced* input also fails? Both proposals assume truncation fixes the problem. If the model is down or rate-limited, smaller input doesn't help. The timeout and exit-code logic from D3/D4 already handles this — just confirm the truncated retry still respects the same 120-second timeout and single-retry limit. No special cases.

### The Adversarial Critic (adversarial reviewer)

## Both of You Converged — That's Suspicious

You both landed on "truncate input on retry" independently. That should make everyone nervous, not confident. When two designers agree this fast, they've usually shared a blind spot.

Here's what neither of you addressed:

**You don't know why synthesis fails.** Is it token count? Model confusion from contradictory inputs? Timeout from generation length? Each cause demands a different intervention. Truncating input helps exactly one of these. If the model times out generating a 3000-word design doc, sending fewer input tokens changes nothing about output length. You've burned your one retry on the wrong fix.

**The "compressed input" is a design fiction.** Architect says build it *before* the first attempt "so it's ready instantly." That means the orchestrator now maintains two prompt variants for every synthesis call. Who validates the compressed version preserves the right signal? You've moved complexity from retry logic into prompt engineering — harder to test, harder to debug, silent when it degrades.

**Flow's "strip the propose round" heuristic is fragile.** It assumes critique and evaluate always subsume propose. They don't. When agents agree in propose and the critic nitpicks margins, the core position lives only in propose. Strip it and you've removed the load-bearing content.

**The real question you're both dodging:** What is the actual failure rate and failure mode distribution from beta? If synthesis fails 2% of the time, this entire discussion is over-engineering. If it fails 30%, truncated retry won't save you.

Measure first. Design the intervention to match the diagnosis, not the vibes.

## Round: EVALUATE

### The Product Oracle (user advocate)

## EVALUATE — The Product Oracle

The critic landed the punch: you're designing a fix without knowing the disease.

**The job the overnight user hired this system to do:** wake up to actionable output. A `partial` status with intact round files still does that job. A skeleton doc with misclassified commitments doesn't — it actively misleads.

Here's my read:

**Truncate-on-retry is fine as a cheap hedge.** Flow Orchestrator's version wins: same prompt, less input, no new output format. The extraction pipeline doesn't change. The Morning Brief doesn't need a second code path. Ship it and move on.

**But don't pre-build the fallback payload.** Architect's "build it before the first attempt" sounds disciplined but it's speculative work on every call to save time on the ~5% that fail. Build it in the retry path. String concatenation on files already on disk takes milliseconds. You're not in a hot loop.

**The real reliability play is upstream.** If synthesis is the bottleneck, the leverage point is input quality, not retry strategy. Tighter round prompts that produce more structured output give synthesis less reconciliation work. That's a prompt tuning task, not an architecture decision — but it's where the actual ROI lives.

**What to ship:**

1. Truncated input on retry (strip propose round, trim prior context)
2. Same prompt, same output format
3. `partial` status on double failure, no degraded-output mode
4. Instrument failure rate and failure mode from the first real runs

Measure, then revisit. Don't build machinery for a problem distribution you haven't observed yet.

### The Context Surgeon (context efficiency evaluator)

## EVALUATE — The Context Surgeon

The critic landed the hit nobody wants to acknowledge: **you don't know your failure distribution.** Everything else is premature.

But we ship V1 without beta failure telemetry, so here's what survives scrutiny:

**Truncate-on-retry is the only intervention with acceptable cost.** Both proposers converged here because the alternative space is genuinely poor. Two-pass doubles calls. Chunking breaks coherence. The convergence isn't a blind spot — it's a constrained solution space.

**Flow Orchestrator's version wins.** Same prompt, less input, same output format. No downstream extraction changes. Architect's skeleton synthesis introduces a second output contract that every consumer must handle. That's not degradation — it's a fork. Unacceptable in V1.

**Strip propose, keep critique and evaluate.** The Adversarial Critic's objection that propose contains load-bearing content is valid in theory but rare in practice. When agents agree, the evaluate round captures the consensus. When they disagree, critique captures the tension. The propose round is the highest-token, lowest-signal-density input. It's the correct cut.

**Pre-build the truncated payload.** Architect was right here. String manipulation in error handlers is where bugs hide. Build both payloads upfront, discard the fallback on success.

**No skeleton docs, no degraded output files.** Mark `partial`, move on. Round files are on disk. Honest gaps over plausible fictions.

**What V1 must also do:** Log the failure reason (timeout vs. malformed vs. rate-limit) so V2 can design targeted interventions instead of guessing. The Adversarial Critic's core point — measure before designing — becomes the V1 instrumentation requirement.
