# How does decision extraction work?

*Generated: 2026-03-18 03:51 | Question 2 | 112s | Mode: compete*

## Decisions

### Extraction is a Single CLI Call Per Question

One `claude -p` call per question. Input: the design doc markdown (synthesis section only). Output: JSON to stdout. The orchestrator validates and writes two files: `decisions.json` and `open_questions.json`. No intermediate files, no fragment accumulation.

### Schema: decisions.json

```json
[
  {
    "id": "q3-d1",
    "decision": "Use WebSocket transport, not polling",
    "commitment": "firm | recommendation | suggestion",
    "confidence": "high | medium | low",
    "resolution_status": "resolved | partially_resolved | unresolved",
    "supporting_evidence": "Quote from synthesis grounding the classification",
    "dissent": "Quote from critic round, or null",
    "source_round": "q3"
  }
]
```

### Schema: open_questions.json

```json
[
  {
    "id": "q3-oq1",
    "statement": "Whether to support multi-region deployment",
    "blocking": true,
    "source_round": "q3"
  }
]
```

No nested objects. No metadata beyond what the Morning Brief consumes downstream. The two files ship as separate artifacts matching the Morning Brief input contract.

### Commitment Classification Uses Linguistic Markers

The extraction prompt defines three tiers by the language patterns in the synthesis:

- **firm**: Declarative language with no hedging. "We will", "the system uses", definitive present or future tense.
- **recommendation**: Advisory or conditional language. "Should", "the preferred approach is", endorsement with qualifiers.
- **suggestion**: Exploratory or deferred language. "Worth considering", "one option is", "could", mentioned as viable but not endorsed.

The extractor classifies based on these markers. It does not invent commitment levels. If the synthesis language is ambiguous, the default is `suggestion` with `confidence: low`.

### Extraction Scope is the Synthesis Section Only

The extractor reads the final synthesis output from each question's design doc. Critic objections, propose-round speculation, and evaluation commentary are not extraction sources. Without this boundary, critic objections get classified as decisions, producing contradictory decision sets.

The prompt must include an explicit instruction: "Extract decisions only from the synthesis section. Critic passages and earlier round content are context, not decisions."

### Open Questions Are Explicitly Deferred Items

An open question is something the discussion identified as unresolved and requiring future input. It is not a hedged recommendation.

Distinguishing rules for the prompt:

- "This requires human judgment on X" --> open question
- "We need to decide Y before proceeding" --> open question, `blocking: true`
- "One option is X" --> suggestion (goes in decisions.json)
- "We should consider X" --> suggestion (goes in decisions.json)

The `blocking` field indicates whether the open question gates downstream work. The prompt must define blocking as: "the discussion explicitly stated this must be resolved before implementation can proceed."

### Supporting Evidence is Prompt Discipline, Not Verification

The extraction prompt requires the model to quote the synthesis sentence that justifies each commitment classification. This forces grounding -- the model must look before it classifies.

The orchestrator does not perform substring matching against the source document. LLMs paraphrase consistently enough that literal matching produces false demotions, which trains the human to ignore risk flags. Validation is structural only: the `supporting_evidence` field must be non-empty and longer than ten characters. Nothing more.

### Garbage Handling: Two Gates, No Retry Loops

**Gate 1: JSON parse.** `json.loads()` on the CLI output. If it fails, retry once with a nudge appended to the prompt: "Your previous response was not valid JSON. Return only the JSON array." If the second attempt also fails, write a stub file (`[]` for decisions, `[]` for open questions) and log the failure.

**Gate 2: Field validation.** Each decision object must contain all required fields with values matching the allowed enums. Strip any decision missing required fields or containing out-of-enum values. Do not fail the session over one malformed entry.

No retry loops beyond the single retry. Two parse failures means the design doc produced unparseable synthesis. The stub file ensures the Morning Brief pipeline does not break. The brief will note the missing round as a gap.

### Confidence and Resolution Status Come From Upstream

The evaluator synthesis step (the final round of each question's discussion) tags each decision with:

- `confidence`: derived from degree of consensus in the evaluate round
- `resolution_status`: whether critic concerns were addressed (`resolved`), partially addressed (`partially_resolved`), or acknowledged but unresolved (`unresolved`)

The extraction prompt carries these tags through. The extractor does not independently assess confidence or resolution. It reads what the synthesis stated and maps it to the enum values. If the synthesis did not explicitly state confidence or resolution, the extractor defaults to `medium` confidence and `partially_resolved`.

### Extraction Prompt

```
You are extracting structured decisions from a design synthesis document.

Read the SYNTHESIS section only. Ignore critic passages and earlier
round content.

For every statement that prescribes a choice, extract it as a decision.
Classify its commitment level using these rules:
- firm: declarative, no hedging ("we will", "the system uses")
- recommendation: advisory or conditional ("should", "preferred approach")
- suggestion: exploratory or deferred ("could", "worth considering")

For each decision, quote the synthesis sentence that justifies your
commitment classification. If you cannot find a supporting sentence,
set commitment to "suggestion" and confidence to "low".

Quote any unresolved dissent from the critic round. If none, set
dissent to null.

Separately, extract open questions: items the discussion explicitly
identified as unresolved and needing future input. A hedged
recommendation is a suggestion, not an open question. Mark an open
question as blocking only if the discussion stated it must be resolved
before implementation proceeds.

Return two JSON arrays:
1. decisions: [{id, decision, commitment, confidence, resolution_status,
   supporting_evidence, dissent, source_round}]
2. open_questions: [{id, statement, blocking, source_round}]

Use the id format "qN-dN" for decisions and "qN-oqN" for open questions
where N is the question number.

Return only valid JSON. No markdown fencing. No commentary.
```