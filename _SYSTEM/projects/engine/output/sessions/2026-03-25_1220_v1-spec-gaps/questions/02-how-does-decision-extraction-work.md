# How does decision extraction work?

*Generated: 2026-03-25 12:25 | Question 2 | 159s | Mode: compete*

## Decisions

1. **Extract from the evaluate round output, not the design doc.** The decided execution sequence is `propose → critique → evaluate → extract fields → write design_doc.md → synthesize`. Design docs have not been written when extraction runs. The question's framing ("free-form markdown from an LLM synthesis call") is a misdescription of timing. The extraction source is the evaluate round output, always.

2. **One extraction call handles all three downstream inputs.** The call extracts decisions, open questions, and the sharpest objection in a single pass. This resolves the open question from Q1 ("sharpest objection extraction mechanism") — no dedicated second call, no regex heuristic, no field from a separate evaluate prompt. The extraction prompt is the mechanism.

3. **Binary classification: decision or omission.** There are no tiers (firm / working / tentative). If the extractor can commit, it outputs a decision. If it cannot commit, the item is an open question or is dropped entirely. A hedged statement that cannot be classified as a conclusion is not a decision — it is noise that degrades the brief. Three categories that map to two downstream buckets produce maintenance burden without value.

4. **No evidence fields in the schema.** Evidence fields extracted by an LLM confabulate plausible-sounding citations rather than performing verbatim substring matches. The audit anchor is the full evaluate round output, logged as a sidecar file alongside `decisions.json`. That is one file copy, not an extraction task.

5. **The extraction prompt:**

   > From the agent evaluation below, extract firm decisions as JSON. A firm decision is a conclusion the group reached from this question's discussion only — do not infer from prior context. If uncertain, omit. Also extract unresolved questions and the single sharpest objection raised.

   The scope constraint ("from this question's discussion only — do not infer from prior context") prevents cross-context confabulation. The evaluate round output is the only valid source window.

6. **The schema:**

   ```json
   {
     "decisions": ["one sentence per conclusion the group reached"],
     "open_questions": ["one sentence per unresolved tension"],
     "sharpest_objection": "single sentence, verbatim from critique"
   }
   ```

   This schema maps exactly to the three inputs the synthesis prompt contract already specifies: extracted decisions, extracted open questions, sharpest objection. No impedance mismatch. Schema validity is fitness for its downstream consumer.

7. **Token budget is met.** Decisions at ~15 words each, open questions similar, one objection sentence. The schema stays well within the ~100 token per question bound established in prior decisions.

8. **Garbage recovery path:** Validation runs after extraction. Failure conditions are: API error, unparseable JSON, or missing required top-level keys (`decisions`, `open_questions`, `sharpest_objection`). On any failure: write raw evaluate output to `extraction_fallback_{n}.txt`, set `decisions = []` and `open_questions = []` as synthesis inputs, log the failure in `session.log`, and continue. Synthesis runs with empty inputs and produces a degraded brief. The session does not halt. A degraded brief is better than a halted session — the user wakes up to something.

9. **Never write partial data to `decisions.json`.** Either the full valid structure is written or nothing is written. Partial writes corrupt the chain.

---

## Open Questions Resolved

- **Sharpest objection extraction mechanism** — Resolved. Single extraction call, `sharpest_objection` field, sourced from evaluate round output.
- **Fallback trigger scope** — Resolved. Trigger on API failure, invalid JSON, or missing required top-level keys. Structural validation catches garbage before it enters the synthesis chain.

## Open Questions Remaining

- **First-call behavior** — On the first question, `previous_brief` is empty. The synthesis prompt should specify whether `## What Got Built` is omitted when there is only one entry or always included. Not resolved by this discussion.
<!-- complete -->
