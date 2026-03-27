### The Cognitive Architect (creativity engine designer)

## Decision Extraction: One Call, Epistemic Markers, Fail-Empty

**The core insight:** LLMs signal commitment level through modal verbs. "We will use X" is categorically different from "We should consider X" or "X might work." The extractor should detect these epistemic markers, not infer intent from position or emphasis.

**The extraction prompt:**

```
Read the design doc below. Extract every decision, recommendation, and suggestion.

Classify each by commitment level:
- FIRM: "will", "decided", "we are using", past tense conclusions
- WORKING: "should", "recommend", active voice without hedge
- TENTATIVE: "might", "could", "worth considering", "one option"

Return JSON only. No explanation.
```

**Schema:**

```json
{
  "decisions": [
    {
      "id": "q1_d1",
      "question_index": 1,
      "text": "one sentence, present tense",
      "commitment": "firm | working | tentative",
      "evidence": "verbatim phrase that triggered classification",
      "extracted_at": "ISO timestamp"
    }
  ]
}
```

**Why `evidence` matters:** It's the anti-hallucination anchor. If the extractor can't quote the source, the classification is suspect. Downstream reviewers can audit it.

**Garbage handling:** Validate that the response is parseable JSON with at least one item. On failure — malformed JSON, empty array when design doc is non-empty, or missing required fields — write `decisions_fallback_{n}.json` and log the raw response. Never write partial data to `decisions.json`. This also resolves the open question on fallback trigger scope: structural validation catches garbage before it corrupts the chain.

**Bonus:** This same call extracts the sharpest objection — add one field: `"sharpest_objection": "verbatim sentence"`. One extraction call handles both open questions from Q1.

### The Flow Orchestrator (mechanical flow designer)

## Agree on one call. Cut the three tiers. Fix the sequencing.

**What the Cognitive Architect gets right:** Single extraction call that also captures `sharpest_objection` — that's the right move. Resolves both Q1 open questions in one shot. The evidence field is a legitimate audit anchor, not gold-plating.

**Cut the commitment tiers.** Firm / working / tentative sounds useful but trace who consumes it. The brief generator gets `decisions` as input — does it treat tentative items differently? If not, we're extracting three categories and using one. Ship one tier: it's a decision or it isn't. If the extractor is uncertain, it should omit, not classify.

**Sequencing problem.** The decided execution order is: `evaluate → extract fields → write design_doc.md → synthesize`. The Cognitive Architect's prompt says "read the design doc below" — but design_doc isn't written yet at extraction time. The extraction source is the **evaluate round output**, not design_doc. This needs to be explicit in the prompt and in the sequence spec.

**Minimum schema:**

```json
{
  "decisions": [{"text": "...", "evidence": "..."}],
  "open_questions": ["..."],
  "sharpest_objection": "..."
}
```

Drop `id`, `question_index`, `commitment`, `extracted_at`. Session folder provides timestamp. Downstream can index by array position if needed.

**Fallback trigger** resolves to: API failure OR invalid JSON OR missing required top-level keys. Write `extraction_fallback_{n}.json`. Never write partial data. This is consistent with the synthesis fallback pattern already decided.


<!-- complete -->
