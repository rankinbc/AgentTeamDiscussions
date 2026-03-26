# How does decision extraction work?

*Generated: 2026-03-25 12:15 | Question 2 | 173s | Mode: compete*

## Decisions

### 1. No Post-Hoc Extractor — Instrument the Synthesizer Instead

Decision extraction does not run as a separate LLM call on free-form synthesis prose. Instead, the synthesis prompt is modified to emit a mandatory structured section at the end of its output:

```
## Decisions
- [one sentence per firm decision reached]

## Open
- [one sentence per unresolved question or deferred item]
```

The parser reads that section directly. This eliminates the second LLM call, removes the hallucination-of-structure failure surface, and produces `decisions.json` from output the synthesis call was explicitly instructed to generate.

**Rationale:** A post-hoc extractor asks a model to impose structure on prose that was written for human readers, not machine parsing. Every failure mode identified in this discussion — invented decisions, disagreement between extractor and synthesizer, circular evidence citation — traces to that root cause. The synthesis prompt is editable (`templates/prompts/*.md.j2`). Fix the root cause.

---

### 2. Schema: Flat, Two-Tier, No Confidence Float

`decisions.json` uses the following schema:

```json
{
  "question": "...",
  "decisions": [
    { "text": "...", "tier": "decided" },
    { "text": "...", "tier": "open" }
  ],
  "extraction_failed": false
}
```

**Tier semantics:**
- `decided` — a firm resolution reached during the session: the group converged, a direction was chosen, the question is closed.
- `open` — unresolved, deferred, or still contested: candidates for the brief's "Unresolved risk" field.

**What is not in the schema:**
- No `confidence` float. The tier encoding carries the same signal without false precision. Nothing in V1 branches on a numeric confidence value.
- No `evidence` citation field. Evidence anchoring was designed to detect extractor confabulation. With structured synthesis output, there is nothing to confabulate — the synthesizer wrote the block under instruction.
- No `recommended` or `suggested` sub-tiers. Nothing in the V1 micro-brief template consumes them. Add tiers when a downstream consumer exists, not before.

---

### 3. Micro-Brief Input: Decided-Tier Items Only

The micro-brief prompt receives only the `decided`-tier items from `decisions.json`. The `open`-tier items are available as candidates when the model populates the "Unresolved risk" field, but are not passed as primary input.

This replaces the previously-decided last-500-token fallback once structured synthesis output is implemented, as noted in the open item from the prior session.

---

### 4. Garbage Handling: Parser Detects, Flag Surfaces in Brief

The parser treats the following conditions as extraction failure:
- The `## Decisions` section is absent from synthesis output.
- The `## Decisions` section is present but contains no items.
- The section is malformed (unparseable list structure).

On failure, the parser sets `extraction_failed: true` in `decisions.json` and falls back to the last 500 tokens of synthesis output for micro-brief input, per the prior decision.

**The flag must surface in the brief.** A failed extraction appends the already-decided skip marker:

```
### [Question title] — brief generation failed, see transcript
```

Silent fallback is not acceptable. The user reading `morning_brief.md` must be able to see that a question produced no structured output. That signal — which questions failed to resolve — is itself information worth having.

---

### 5. Firm vs. Recommendation vs. Suggestion: Not Distinguished in V1

The three-tier commitment taxonomy (DECIDED / RECOMMENDED / SUGGESTED) is not implemented. The distinction is only meaningful if something downstream branches on it. In V1, the micro-brief template has no "Recommended" field, no "Suggested" field — only "Decided" and "Unresolved risk." Extracting three tiers populates schema fields with no reader.

If a future consumer requires finer-grained commitment levels, add the tier back at that point with a concrete downstream use case driving the design.
<!-- complete -->
