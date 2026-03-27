# Transcript: How does decision extraction work?

*Generated: 2026-03-25 12:39*

## Round: PROPOSE

### The Cognitive Architect (creativity engine designer)

## Decision Extraction: Commitment Signal Detection

The core problem isn't extraction — it's calibration. A design doc contains dozens of declarative sentences. The extractor needs to distinguish *option-closers* from *option-openers*.

**The principle:** Decisions close options. Recommendations keep them open. Suggestions generate them.

This distinction is detectable via linguistic commitment markers, which LLMs actually reproduce reliably because they're trained on technical writing that uses them conventionally.

---

**Schema:**
```json
{
  "question_id": "str",
  "decision_id": "str",
  "statement": "str — one sentence, active voice",
  "confidence": "firm | provisional | suggestion",
  "grounding": "str — the constraint or tradeoff that justifies this"
}
```

`grounding` is the key non-obvious field. A firm decision with no grounding is a guess dressed as a commitment. Requiring grounding forces the extractor to distinguish genuine resolution from confident-sounding drift.

---

**Extraction prompt (core instruction):**

> Find every statement that closes an option — that says what the system *will do*, *is*, or *will not do*. Classify by commitment marker: firm (past-tense resolved, no hedges), provisional ("should," "recommend," "prefer" — contingent), suggestion ("could," "might," "worth exploring"). Extract the grounding: what constraint or tradeoff made this the answer? If no grounding exists, confidence is capped at suggestion.

---

**Garbage handling:** Validate that `statement` is a single sentence and `grounding` is non-empty for `firm` entries. On failure: emit the raw text as `confidence: "suggestion"`, `grounding: "unextracted"`. Never discard — garbage signals extraction model drift worth reviewing.

The fallback preserves the fragment; the grounding requirement filters false confidence.

### The Flow Orchestrator (mechanical flow designer)

The Cognitive Architect's schema is for a different artifact than the one decided. `decisions.json` is machine-readable output for downstream tooling — not a reasoning trace. The `grounding` field makes the extractor synthesize justifications, not extract statements. That's a harder LLM task with more failure surface. Cut it.

**The sequencing problem nobody addressed:**

Extraction runs async after each design doc lands on disk. That means:
1. Design doc write completes → trigger extraction
2. Fragment extractor runs (already decided: async, non-blocking)
3. Decisions extractor runs — same async window? Separate trigger? Same LLM call?

This needs an answer before the prompt matters.

**Minimal schema:**
```json
{
  "question_id": "str",
  "statement": "str",
  "confidence": "firm | provisional | suggestion"
}
```

Array per question. No `decision_id` — question_id + array position is sufficient for any downstream join. No `grounding` — the design doc *is* the grounding; don't duplicate it in the artifact.

**On confidence classification:** The three-tier taxonomy is defensible but only if the extractor's classification is constrained by the same linguistic markers the Architect described. The prompt instruction is sound: past-tense resolved = firm, hedged modal = provisional, speculative = suggestion.

**Garbage handling:** Emit as `confidence: "suggestion"` — agreed. But don't label it `grounding: "unextracted"` — that field shouldn't exist. Garbage is just a low-confidence statement. Downstream tooling filters by confidence; it doesn't need a garbage flag.

**Open issue still open:** What is the exact trigger for decisions extraction — same async call as fragment extraction, or a second pass?

## Round: CRITIQUE

### The Systems Pragmatist (infrastructure realist)

## Proposal: Decisions Extraction — Constrain the Problem First

The sequencing question from prior discussion is still open and it matters: if fragment extraction and decisions extraction share an async window, they should share an LLM call. Two separate calls on the same design doc is unnecessary overhead and doubles the failure surface.

**My position: one extraction call, two outputs.**

Single prompt. Single call per question. Returns both the fragment JSON and the decisions array. The extractor sees the design doc once; you get both artifacts or neither.

**Schema — minimal:**
```json
{
  "question_id": "str",
  "decisions": [
    {
      "statement": "str",
      "confidence": "firm | provisional | suggestion"
    }
  ]
}
```

No `decision_id`. No `grounding`. Array position + `question_id` is sufficient for any downstream join.

**Confidence classification — the real failure mode:**

LLMs will hallucinate confidence. If the prompt says "classify as firm/provisional/suggestion based on your judgment," you get noise. If it says "firm = past tense resolved statement with no hedge words; provisional = contains 'should', 'recommend', 'consider'; suggestion = anything else" — you get consistent extraction from linguistic surface features. That constraint belongs in the prompt, not in post-processing.

**Garbage handling:**

Emit as `confidence: "suggestion"`. Don't add a garbage flag. Low confidence *is* the signal.

**What I need decided:**

1. Confirmed: one call, two outputs, or separate calls?
2. Confirmed: fallback behavior if the combined call fails?

Nothing else moves until those are locked.

### The Adversarial Critic (adversarial reviewer)

## Problems Nobody Has Addressed

**"One call, two outputs" creates correlated failure.** Two separate calls fail independently. One combined call fails atomically — you lose both artifacts simultaneously. The Systems Pragmatist frames this as halving the failure surface. It's the opposite: you've coupled two independent failure modes into one. Fragment extraction already has a decided fallback. Decisions extraction doesn't. What's the fallback for the combined call? Still unanswered.

**Linguistic surface features don't survive LLM synthesis.** The design doc is already a synthesis over a 3-round discussion. The original "DECIDED:" phrasing from the discussion gets paraphrased, smoothed, and restructured in synthesis. You're now running a classifier on paraphrased output of paraphrased output. Past tense in a design doc doesn't mean firm — it means the synthesizer wrote in past tense. This will misclassify constantly.

**Array position as a join key breaks on retry.** If the extractor fails and retries, the decisions array may come back in different order. You've just invalidated any downstream join that used position. `question_id + statement hash` is stable. Position isn't.

**"Garbage emits as suggestion" assumes the extractor returns valid JSON.** What happens when it returns malformed JSON? What happens when it hallucinates extra fields? Neither proposal has a schema validation step before writes.

**The sequencing question has been open for two rounds.** The Pragmatist says nothing moves until it's locked, then doesn't lock it. That's a stall, not a proposal. Someone decide: same call or separate trigger. I don't care which — pick one.

## Round: EVALUATE

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
