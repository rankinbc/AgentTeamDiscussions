# How does a round begin after a reset?

*Generated: 2026-03-17 22:43 | Question 1 | 196s | Mode: lean*

The file write is awaiting your permission to save to the output directory. Once approved, it'll create `spec_round_initialization.md` in the `output/` folder alongside the other design question outputs.

Here's what the synthesized spec covers:

**Four-step initialization sequence** (the key addition from critique was Step 1.5):
1. **Load save files** -- raw agent state from last round
2. **Merge BackgroundAgent modifications** -- hard boundary before curation begins (resolves the sequencing gap all reviewers flagged)
3. **Context curation** -- deterministic filtering first (decay, thresholds, resolved items), then LLM curator call producing the Situation block plus a curation rationale and deprioritized footer
4. **Assemble round-open prompt** -- Identity + Situation + Task

**Key design decisions consolidated from the critique:**
- **Curation rationale is mandatory output** -- both for debugging and for agent self-correction (the deprioritized footer goes into the prompt so agents can notice gaps)
- **Drift is two-layered** -- deterministic decay provides tunable baseline, LLM curator adds creative unpredictability. Neither alone is sufficient.
- **Mid-round state reminder has a 500-token hard floor** -- deterministic extraction only, no LLM call, positioned before transcript in the prompt
- **Two separate prompt templates** -- round-open and mid-round are maintained independently, never unified. The cognitive modes (internally-driven vs externally-driven) are fundamentally different.
- **Transcript truncation rule** -- when budget pressure hits, drop early transcript turns before ever touching the state reminder