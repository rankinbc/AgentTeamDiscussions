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


<!-- complete -->
