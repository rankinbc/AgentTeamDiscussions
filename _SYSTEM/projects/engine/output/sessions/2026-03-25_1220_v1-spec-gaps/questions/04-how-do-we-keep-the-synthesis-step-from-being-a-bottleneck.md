# How do we keep the synthesis step from being a bottleneck?

*Generated: 2026-03-25 12:32 | Question 4 | 159s | Mode: compete*

## Decisions

1. **The synthesis bottleneck question was a false premise.** The Morning Brief synthesis step already has a bounded, structured input: extracted fields (decisions, open questions, sharpest objection) plus the prior brief. That input contract was closed in a prior question. The 9000-word problem belongs to step 5 — the design doc write — which had no input contract. Two rounds of discussion were spent on a solved problem. This is a session-level failure mode: stale question framing propagates wasted compute.

2. **Input routing is finalized.** Propose and critique round outputs go to transcript only. The evaluate round output is the sole LLM input to the design doc write (step 5), in addition to the extracted fields. The brief synthesis step (step 6) remains unchanged: extracted fields plus prior brief only.

   Confirmed execution sequence:
   1. Propose → transcript only
   2. Critique → transcript only
   3. Evaluate → transcript + design doc input (after truncation)
   4. Extract fields from evaluate output → `decisions`, `open_questions`, `sharpest_objection`
   5. Design doc write: `evaluate_output (truncated) + extracted_fields` → `design_doc_{n}.md`
   6. Synthesize: `extracted_fields + previous_brief` → `brief.md` or `brief_fallback.md`

3. **Evaluate output is truncated at 1500 words before entering step 5.** This is a conservative bound that covers dense discussions; anything beyond it is repetition. The threshold is logged in `defaults.yaml`. Empirical tuning against session output is deferred to V2. This number is decided — it is not a placeholder.

4. **Truncation is enforced in the orchestrator, not in the prompt.** The Python orchestrator performs a hard word-count and slices the string before the LLM call is made. Leaving truncation to the model's judgment adds a failure surface and spends tokens on text that was never supposed to arrive. One line of code; the contract is enforced before the token is spent.

5. **On step 5 failure, write `design_doc_{n}_fallback.md` using the raw (truncated) evaluate output verbatim.** The evaluate output is already on disk, already structured, already forward-usable. This fallback activates on API failure or timeout only — not on output quality judgment. Naming follows the existing `brief_fallback.md` convention.

6. **Fallback design docs are inherited identically to primary design docs.** `design_doc_{n}_fallback.md` is the design doc for question n. Q(n+1) inherits it without detection logic, without branching, without special handling. The state machine does not distinguish fallback from primary. Simpler is correct here.

7. **`## What Got Built` is omitted when `previous_brief` is empty.** On the first question, the section is skipped entirely. This was previously open; it is now closed.

## Open Questions

- What is the correct behavior when evaluate output is below the 1500-word truncation threshold — is the full output passed as-is, or is there a minimum floor? (Presumed yes, pass as-is; not yet explicit.)
- Does the fallback trigger for the design doc write (step 5) include malformed output — e.g., an LLM response that returns but produces unusable content — or strictly API failure and timeout? The existing `brief_fallback.md` trigger scope covers API failure, invalid JSON, and missing required keys; step 5 has no analogous validation rule.

## Watch Out

- The 1500-word threshold is a reasoned estimate, not a measured one. If evaluate output in practice consistently runs under 1000 words or over 2000, the threshold should be adjusted in V2 against actual session data. Do not treat `defaults.yaml` as permanently correct.
- Truncation at the Python layer means the orchestrator owns the boundary, not the prompt template. If the truncation logic is ever moved or removed from the orchestrator, the input contract silently breaks. The truncation step must be treated as a required pipeline stage, not an optional optimization.
- Fallback doc inheritance (decision 6) means a low-quality fallback silently enters the context chain and chains forward. There is no signal to the next question that its inherited doc is degraded. This is an acceptable tradeoff for V1 simplicity; V2 should consider a quality signal in the session log.

## Your Move

- Add `evaluate_output_truncation_words: 1500` to `defaults.yaml`.
- Update the orchestrator to apply hard word truncation to evaluate output before step 5, in Python, before the LLM call.
- Confirm that the design doc write step receives `evaluate_output (truncated) + extracted_fields` only — remove any path that passes propose or critique output to step 5.
- Update question framing validation: before a discussion brief is run, check that its open questions do not re-litigate closed decisions. Log a warning if a question maps to a field with an existing DECIDED entry.
<!-- complete -->
