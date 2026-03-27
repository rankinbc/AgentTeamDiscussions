

- DECIDED: Generation strategy is incremental append — one micro-brief block written per question immediately after synthesis completes, no final assembly pass
- DECIDED: Micro-brief prompt receives extracted decisions from synthesis, not full synthesis prose; fallback is last 500 tokens of synthesis output
- DECIDED: Context budget per micro-brief call is ~1,500–2,000 tokens; each call is fully isolated with no prior questions or chained docs
- DECIDED: Micro-brief block template is fixed four fields: Decided, Why this beat alternatives, Unresolved risk, Assumption challenged
- DECIDED: All four fields are mandatory; "none" answers are valid and expected
- DECIDED: "Assumption challenged" prompt instructs model to write "none — conclusion was predictable" if result was unsurprising, flagging only genuine surprises
- DECIDED: Risk extraction is prompt-driven via the "Unresolved risk" field; no regex scanning of critic turns, no tagging mechanism in the orchestrator
- DECIDED: Failed micro-brief calls append a labeled skip marker in the format `### [Question title] — brief generation failed, see transcript` and the session continues
- DECIDED: Silent omission of failed blocks is not acceptable; the question title must appear in the marker for scannability
- DECIDED: Ordering limitation of incremental model is accepted for V1 — late-emerging risks do not retroactively update earlier blocks
- DECIDED: Cross-question synthesis pass reordering by risk severity is deferred to V2, contingent on user feedback
- DECIDED: morning_brief.md opens with a minimal header containing session-id, date, question count, completed count, and failed brief count — no narrative introduction
- DECIDED: There is no quality gate on synthesis output before it feeds the micro-brief prompt in V1
- DECIDED: Automated quality scoring runs post-session as a separate pass and is not a dependency of brief generation
- OPEN: When structured decision extraction is implemented, replace the last-500-tokens fallback with extracted decisions as the micro-brief input
- OPEN: V2 cross-question assembly pass to reorder blocks by risk severity — build only if ordering proves to be a real problem in practice

- DECIDED: Decision extraction is implemented by modifying the synthesis prompt to emit a structured `## Decisions` / `## Open` section, not via a separate post-hoc LLM extractor call
- DECIDED: `decisions.json` uses a flat two-tier schema with `text` and `tier` fields (`decided` or `open`) plus `extraction_failed` boolean; no confidence float, no evidence citation, no recommended/suggested sub-tiers
- DECIDED: The micro-brief prompt receives only `decided`-tier items as primary input; `open`-tier items are available as candidates for the "Unresolved risk" field only
- DECIDED: The last-500-token fallback for micro-brief input is replaced by structured synthesis output once instrumentation is implemented
- DECIDED: Parser treats absent `## Decisions` section, empty section, or malformed list structure as extraction failure and sets `extraction_failed: true`
- DECIDED: On extraction failure the parser falls back to last 500 tokens of synthesis output for micro-brief input
- DECIDED: Extraction failure must surface visibly in `morning_brief.md` as `### [Question title] — brief generation failed, see transcript`; silent fallback is not acceptable
- DECIDED: The three-tier commitment taxonomy (DECIDED / RECOMMENDED / SUGGESTED) is not implemented in V1; the distinction will only be added when a downstream consumer with a concrete use case requires it
- OPEN: No open items identified in this document

<!-- complete -->
