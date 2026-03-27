### The Cognitive Architect (creativity engine designer)

## Decision Extraction: Commitment Signal Detection

The core problem isn't extraction — it's calibration. A design doc contains dozens of declarative sentences. The extractor needs to distinguish *option-closers* from *option-openers*.

**The principle:** Decisions close options. Recommendations keep them open. Suggestions generate them.

This distinction is detectable via linguistic commitment markers, which LLMs actually reproduce reliably because they're trained on technical writing that uses them conventionally.

---

**Schema:**
```json
{
  "question_id": "str",
  "decision_id": "str",
  "statement": "str — one sentence, active voice",
  "confidence": "firm | provisional | suggestion",
  "grounding": "str — the constraint or tradeoff that justifies this"
}
```

`grounding` is the key non-obvious field. A firm decision with no grounding is a guess dressed as a commitment. Requiring grounding forces the extractor to distinguish genuine resolution from confident-sounding drift.

---

**Extraction prompt (core instruction):**

> Find every statement that closes an option — that says what the system *will do*, *is*, or *will not do*. Classify by commitment marker: firm (past-tense resolved, no hedges), provisional ("should," "recommend," "prefer" — contingent), suggestion ("could," "might," "worth exploring"). Extract the grounding: what constraint or tradeoff made this the answer? If no grounding exists, confidence is capped at suggestion.

---

**Garbage handling:** Validate that `statement` is a single sentence and `grounding` is non-empty for `firm` entries. On failure: emit the raw text as `confidence: "suggestion"`, `grounding: "unextracted"`. Never discard — garbage signals extraction model drift worth reviewing.

The fallback preserves the fragment; the grounding requirement filters false confidence.

### The Flow Orchestrator (mechanical flow designer)

The Cognitive Architect's schema is for a different artifact than the one decided. `decisions.json` is machine-readable output for downstream tooling — not a reasoning trace. The `grounding` field makes the extractor synthesize justifications, not extract statements. That's a harder LLM task with more failure surface. Cut it.

**The sequencing problem nobody addressed:**

Extraction runs async after each design doc lands on disk. That means:
1. Design doc write completes → trigger extraction
2. Fragment extractor runs (already decided: async, non-blocking)
3. Decisions extractor runs — same async window? Separate trigger? Same LLM call?

This needs an answer before the prompt matters.

**Minimal schema:**
```json
{
  "question_id": "str",
  "statement": "str",
  "confidence": "firm | provisional | suggestion"
}
```

Array per question. No `decision_id` — question_id + array position is sufficient for any downstream join. No `grounding` — the design doc *is* the grounding; don't duplicate it in the artifact.

**On confidence classification:** The three-tier taxonomy is defensible but only if the extractor's classification is constrained by the same linguistic markers the Architect described. The prompt instruction is sound: past-tense resolved = firm, hedged modal = provisional, speculative = suggestion.

**Garbage handling:** Emit as `confidence: "suggestion"` — agreed. But don't label it `grounding: "unextracted"` — that field shouldn't exist. Garbage is just a low-confidence statement. Downstream tooling filters by confidence; it doesn't need a garbage flag.

**Open issue still open:** What is the exact trigger for decisions extraction — same async call as fragment extraction, or a second pass?


<!-- complete -->
