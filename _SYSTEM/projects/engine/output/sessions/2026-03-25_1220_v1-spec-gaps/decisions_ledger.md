

- DECIDED: Rolling synthesis architecture — Morning Brief regenerated after each question, not at session end
- DECIDED: Brief generator consumes only structured extracted fields (decisions, open questions, sharpest objection), not design docs
- DECIDED: Four required sections in order: What Got Built, Still In Play, Watch Out, Your Move
- DECIDED: Hard word budgets enforced in prompt (not token limits) — one sentence per question for What Got Built, max 4 bullets for Still In Play, one sentence per question verbatim for Watch Out, max 3 bullets for Your Move
- DECIDED: Synthesis prompt contract is fixed as specified (inputs: previous brief + new question summary; outputs: exactly four sections)
- DECIDED: Continuity enforced by prompt rule ("carry forward unless explicitly superseded"), not by architectural preservation mechanism
- DECIDED: Fallback on synthesis failure writes to brief_fallback.md (never brief.md); brief.md left at last successful state; fallback labeled with FALLBACK: Synthesis Failed header
- DECIDED: Execution sequence per question: propose/critique/evaluate → extract fields → write design_doc.md → synthesize → overwrite brief.md or write brief_fallback.md
- DECIDED: brief_history/ deferred to V2
- OPEN: Mechanism for extracting sharpest critic objection (dedicated extraction call vs regex heuristic vs field from evaluate round)
- OPEN: First-call behavior when previous_brief is empty (whether to omit What Got Built or always include it)
- OPEN: Fallback trigger scope — API failure only, or also malformed/structurally invalid output missing required sections

- DECIDED: Extraction source is the evaluate round output, not the design doc; execution sequence is propose → critique → evaluate → extract fields → write design_doc.md → synthesize
- DECIDED: One extraction call handles all three downstream inputs: decisions, open questions, and sharpest objection
- DECIDED: Binary classification only — a statement is either a decision or it is omitted; no tiers (firm/working/tentative)
- DECIDED: No evidence fields in the schema; the full evaluate round output is logged as a sidecar file alongside decisions.json as the audit anchor
- DECIDED: Extraction prompt scopes to current question's discussion only with explicit instruction not to infer from prior context
- DECIDED: Schema has exactly three fields: decisions (array), open_questions (array), sharpest_objection (string)
- DECIDED: Token budget is met at ~15 words per decision/open question plus one objection sentence, within the ~100 token per question bound
- DECIDED: Garbage recovery triggers on API error, unparseable JSON, or missing required top-level keys; on failure write raw evaluate output to extraction_fallback_{n}.txt, set decisions and open_questions to empty arrays, log failure, and continue with degraded synthesis
- DECIDED: Never write partial data to decisions.json — either the full valid structure is written or nothing is written
- DECIDED: Sharpest objection extraction mechanism is resolved via the single extraction call and sharpest_objection field sourced from evaluate round output
- DECIDED: Fallback trigger scope is API failure, invalid JSON, or missing required top-level keys
- OPEN: First-call behavior when previous_brief is empty — whether ## What Got Built is omitted when there is only one entry or always included is not resolved

- DECIDED: Three failure layers (round, extraction, synthesis) each have their own retry/degradation policy matched to their value
- DECIDED: Round calls get exactly one retry with no delay, scoped to the failing call only
- DECIDED: On round failure post-retry, write tombstone `[ROUND FAILED: <round>, Q<n>]` to transcript, skip extraction/doc/synthesis, increment to Q(n+1)
- DECIDED: `brief.md` is never written to on question failure — tombstone is transcript-only
- DECIDED: On question failure, Q(n+1) inherits the last successful design doc (no placeholder file)
- DECIDED: Extraction failures degrade gracefully with no retry — empty arrays passed to synthesis, raw evaluate output saved to `extraction_fallback_<n>.txt`
- DECIDED: Synthesis failure after successful rounds is handled by existing `brief_fallback.md` mechanism — no new path needed
- DECIDED: Transcript writes are incremental per round, written to disk as each round completes
- DECIDED: Session aborts after 3 consecutive question failures; session-level error log written with question indices and failure reasons
- DECIDED: All failures logged to `session.log` with question index and failure reason
- DECIDED: `## What Got Built` section is omitted when `previous_brief` is empty (first question)

- DECIDED: Morning Brief synthesis input contract is bounded to extracted fields (decisions, open questions, sharpest objection) plus prior brief only
- DECIDED: Propose round output goes to transcript only — not to design doc write input
- DECIDED: Critique round output goes to transcript only — not to design doc write input
- DECIDED: Evaluate round output is the sole LLM input to design doc write (step 5), plus extracted fields
- DECIDED: Brief synthesis (step 6) input is extracted fields plus previous brief only — unchanged
- DECIDED: Evaluate output is truncated at 1500 words before entering step 5
- DECIDED: Truncation threshold of 1500 words is logged in `defaults.yaml`
- DECIDED: Truncation is enforced by the Python orchestrator via hard word-count slice before the LLM call — not left to prompt or model judgment
- DECIDED: On step 5 failure (API failure or timeout only), write `design_doc_{n}_fallback.md` using raw truncated evaluate output verbatim
- DECIDED: Fallback trigger for step 5 is API failure or timeout only — not output quality judgment
- DECIDED: `design_doc_{n}_fallback.md` naming follows existing `brief_fallback.md` convention
- DECIDED: Fallback design docs are inherited identically to primary design docs with no detection logic, branching, or special handling in the state machine
- DECIDED: `## What Got Built` section is omitted entirely when `previous_brief` is empty (first question)
- OPEN: When evaluate output is below the 1500-word threshold, is full output passed as-is or is there a minimum floor?
- OPEN: Does the step 5 fallback trigger include malformed/unusable LLM output, or strictly API failure and timeout? No analogous validation rule exists for step 5 as exists for `brief_fallback.md`

<!-- complete -->
