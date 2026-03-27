### The Product Oracle (user advocate)

## Stop. Ask Who Reads This.

The Morning Brief is the user-facing artifact. decisions.json is for "downstream tooling." But this is V1. The downstream tooling doesn't exist yet. Before we spend more rounds debating extraction fidelity, someone should say what decisions.json is *for*.

If it's for the user to review, it competes with the Morning Brief and loses — they'll read one document over coffee, not a JSON array. If it's for future tooling, we're optimizing an API for a consumer that hasn't been built.

**My position:** decisions.json is a low-stakes artifact in V1. The Brief is high-stakes. We're spending more design energy on the wrong one.

That said — four things need locking, and I'll push for the simple answer on each:

1. **One call, two outputs.** The Adversarial Critic's correlated failure argument is technically correct but practically irrelevant — the fallback for both is the same: continue the session, produce the Morning Brief, log the failure. Lose decisions.json for that question. That's acceptable.

2. **Minimal schema.** No `grounding`. Three fields: `question_id`, `statement`, `confidence`. The design doc *is* the grounding.

3. **Linguistic markers in the prompt, not post-processing.** The Pragmatist and Architect agree here. Lock it.

4. **Malformed JSON gets logged and skipped.** Schema validation before writes is a one-liner. Not a design question.

The Critic is right that position-based join keys break on retry. Use `question_id + statement` as the stable identifier.

Decide these. Ship the Brief.

### The Context Surgeon (context efficiency evaluator)

## The Extraction Call's Input Budget: Nobody Has Specified It

The Oracle is right that decisions.json is low-stakes in V1. I'll extend that: the extraction call itself is a token liability if nobody has specified what goes into its context window.

Current proposals assume the extractor reads the design doc. The design doc is a synthesis over a 3-round discussion — already compressed. Good. But has anyone stated explicitly that the extractor does **not** receive the raw transcript? Because if someone hands it the full transcript "for grounding," you've just tripled the input tokens for a low-stakes artifact.

**Lock this now:** The extractor receives the design doc only. Not the transcript. Not prior design docs. The design doc is the canonical compressed output — it's the right input surface.

On schema: Oracle's three fields (`question_id`, `statement`, `confidence`) are correct. Confidence as a scalar (0-1) is less useful than confidence as an enum: `firm | likely | suggestion`. Scalar invites hallucinated precision. Enum maps directly to the Critic's core problem — distinguishing firm decisions from recommendations — without requiring linguistic surface feature analysis on paraphrased text.

The Critic's point about linguistic markers not surviving synthesis is the strongest objection in this thread. The fix isn't post-processing — it's the enum. Instruct the extractor: "If you cannot classify with confidence, use `suggestion`." Garbage flows to `suggestion`, not to `firm`.

One call, two outputs. Malformed JSON gets logged and skipped. `question_id + statement` as the join key.

That's the spec. What's blocking a decision?


<!-- complete -->
