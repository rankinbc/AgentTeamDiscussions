# How does decision extraction work?

*Generated: 2026-03-25 12:39 | Question 2 | 169s | Mode: compete*

## Decisions

1. **decisions.json is a low-stakes V1 artifact.** It exists for downstream tooling that does not yet exist. The Morning Brief is the user-facing artifact; decisions.json is machine-readable output. No design decision should optimize for decisions.json at the expense of the Brief.

2. **One extraction call, two outputs.** Fragment extraction and decisions extraction share a single async LLM call triggered after each design doc is written to disk. The extractor sees the design doc once and returns both the fragment JSON and the decisions array. This is acceptable despite correlated failure because the fallback for both artifacts is identical: continue the session, produce the Morning Brief, log the failure, and omit decisions.json for that question.

3. **The extractor receives the design doc only.** Not the raw transcript. Not prior design docs. The design doc is the canonical compressed output of the 3-round discussion and is the correct input surface. Passing the transcript is explicitly disallowed.

4. **Minimal schema:**
   ```json
   {
     "question_id": "str",
     "decisions": [
       {
         "statement": "str — one sentence, active voice",
         "confidence": "firm | provisional | suggestion"
       }
     ]
   }
   ```
   No `decision_id`. No `grounding`. The design doc is the grounding; it must not be duplicated inside the artifact. `question_id + statement` is the stable join key. Array position is not a valid join key and must not be used by downstream tooling.

5. **Confidence is an enum, not a scalar.** `firm | provisional | suggestion` maps directly to the extractor's classification task without inviting hallucinated numeric precision. The three tiers are defined by linguistic commitment markers applied to the design doc text:
   - `firm` — past-tense resolved statement with no hedge words (e.g., *"The system uses X"*, *"X was chosen"*)
   - `provisional` — contains modal hedges: *should*, *recommend*, *consider*, *prefer*
   - `suggestion` — speculative language (*could*, *might*, *worth exploring*) or any statement that cannot be classified with confidence

6. **Linguistic markers are a prompt constraint, not a post-processing step.** The classification rule belongs in the extraction prompt. The prompt explicitly enumerates the marker words for each tier. The instruction "if you cannot classify with confidence, use `suggestion`" is normative. Garbage flows to `suggestion`; it does not flow to `firm`.

7. **The extractor does not distinguish original phrasing from synthesis paraphrase.** The design doc is already a synthesis pass — original "DECIDED:" phrasing may have been smoothed. The extractor classifies the design doc as written. This means some genuinely firm decisions may land as `provisional` after paraphrase; this is acceptable precision loss given the artifact's low stakes in V1.

8. **Schema validation runs before any write.** Malformed JSON is logged and skipped. The question's decisions.json entry is omitted. Session continues. This is a one-liner, not a design question.

9. **No garbage flag.** Low confidence *is* the signal. Statements that fail extraction emit as `confidence: "suggestion"`. No additional field marks them as extraction failures; downstream tooling filters by confidence level.

10. **Fallback for combined call failure:** Log the failure with the question_id, omit both the fragment and the decisions entry for that question, and continue. The Morning Brief fallback (direct concatenation of fragment fields) already handles missing fragments. The session never exits without a morning_brief.md regardless of extraction failures.

---

## Extraction Prompt (normative)

```
You are extracting structured output from a design document.

The design document is the result of a multi-round agent discussion.
Extract two things:

**1. Fragment** — one JSON object:
{
  "question_id": "{{ question_id }}",
  "decision": "one sentence — what was resolved",
  "needs_your_call": "one sentence — the tension requiring human judgment, or empty string",
  "blocker": "one sentence — any BLOCKER: or RISK: flagged item, or empty string"
}

**2. Decisions** — an array of JSON objects:
{
  "question_id": "{{ question_id }}",
  "decisions": [
    {
      "statement": "one sentence, active voice — what the system will do, is, or will not do",
      "confidence": "firm | provisional | suggestion"
    }
  ]
}

**Confidence classification rules (apply strictly):**
- firm: past-tense resolved statement with no hedge words. Examples: "was chosen", "is used", "will not support".
- provisional: contains should, recommend, consider, prefer, or similar modal hedges.
- suggestion: speculative language (could, might, worth exploring), or any statement you cannot classify with confidence. When in doubt, use suggestion.

**Scope:** Extract only option-closing statements — what the system will do, is, or will not do. Do not extract discussion observations, open questions, or process descriptions.

Return valid JSON only. No prose. No explanation.

<design_doc>
{{ design_doc }}
</design_doc>
```

---

## Open Questions

- **Retry policy for the combined extraction call.** Two retries with 30-second backoff has been recommended but not decided.
- **Whether fragment extraction has its own fallback** if the combined call fails and fragments are missing at brief synthesis time (distinct from the synthesis fallback, which handles present-but-malformed fragments).
<!-- complete -->
