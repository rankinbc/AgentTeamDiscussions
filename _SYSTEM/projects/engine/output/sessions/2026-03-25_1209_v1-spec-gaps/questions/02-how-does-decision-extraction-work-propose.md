### The Cognitive Architect (creativity engine designer)

## Decision Extraction: Source-Anchored Commitment Taxonomy

**The core problem:** Synthesis prose encodes commitment level implicitly through verb tense and hedging language. The extractor needs a rubric that reads those signals, not a vague "how confident does this seem" prompt.

**The prompt design:** Single-pass extraction with an explicit commitment taxonomy baked into the instructions:

> *Scan this synthesis text. For each decision, recommendation, or suggestion, identify: (1) the claim text, (2) its commitment level using these exact categories — DECIDED (past-tense resolution: "agreed," "will use," "is resolved"), RECOMMENDED (directional but conditional: "should," "better to," "leaning toward"), SUGGESTED (exploratory: "might," "could," "worth trying") — and (3) the specific phrase that signals that level. Return only what's explicitly stated, not inferences.*

The evidence field is load-bearing. It forces the extractor to cite its source, which makes garbage immediately detectable.

**Schema:**
```json
{
  "question": "...",
  "decisions": [{
    "text": "...",
    "commitment": "decided|recommended|suggested",
    "confidence": 0.0–1.0,
    "evidence": "the phrase that triggered this classification"
  }],
  "extraction_failed": false
}
```

**Garbage detection:** If `decisions` is empty, or mean confidence < 0.4, or any `evidence` field is blank — mark `extraction_failed: true` and trigger the already-decided 500-token fallback. Don't retry. Don't crash. The morning brief still gets generated.

**The key bet:** Asking for evidence phrases converts a vague classification task into a citation task. LLMs are worse at confabulating citations than confabulating judgments.

### The Flow Orchestrator (mechanical flow designer)

## Flow Trace: What Actually Consumes This Output

The Cognitive Architect's taxonomy is well-structured. One question before endorsing it: **what does the downstream consumer actually use?**

Trace the sequence:
1. Synthesis completes → extractor runs → writes to `decisions.json`
2. Micro-brief prompt receives extracted decisions → writes one block to `morning_brief.md`
3. Morning Brief block has exactly one field that cares about decisions: `**Decided:**`

The brief template has no "Recommended" field. No "Suggested" field. It has **Decided** and **Unresolved risk**.

That means the `recommended` and `suggested` tiers are being extracted for... what, exactly? If `decisions.json` has no other consumer in V1, we're building taxonomy for a reader that doesn't exist yet.

**My cut:** Collapse to two tiers — `decided` and `open`. Pass only `decided` items to the micro-brief. Surface `open` items as candidates for the "Unresolved risk" field. That's it.

The confidence float I'd also drop. We have the evidence field for garbage detection — the discrete taxonomy does the same work a float does, without the false precision.

**What I'd keep from the proposal:** The evidence-as-citation approach is the right bet. Blank evidence = `extraction_failed: true` = fallback. That's clean.

**Revised schema minimum:**
```json
{
  "decisions": [{"text": "...", "tier": "decided|open", "evidence": "..."}],
  "extraction_failed": false
}
```

Add tiers back when something actually consumes them. Not before.


<!-- complete -->
