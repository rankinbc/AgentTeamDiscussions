# Transcript: How does decision extraction work?

*Generated: 2026-03-25 12:15*

## Round: PROPOSE

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

## Round: CRITIQUE

### The Adversarial Critic (adversarial reviewer)

## The Extractor Is a Second LLM Call That Can Also Fail

Everyone's designing the happy path. Let me name what breaks first.

**The core problem nobody's said out loud:** Decision extraction is an LLM call on LLM output. You're asking a model to structure the output of another model that was never instructed to be structurable. Synthesis prose is written for human readers. It buries decisions in conditional language, hedges, and "the group agreed that perhaps..." constructions. The extractor will hallucinate structure that isn't there.

**Five things that will fail:**

1. **Synthesis produces no clear decisions.** A contentious question ends in "both approaches have merit." The extractor invents a decision to fill the schema. Nothing in the pipeline catches this.

2. **The extractor disagrees with the synthesizer.** Synthesis says "decided X" but evidence in the transcript points to Y. Which wins? The brief says X. The transcript says Y. Downstream: confusion.

3. **Evidence citation is circular.** The extractor quotes synthesis prose as evidence for a decision that came from that same synthesis prose. The citation proves nothing — it's turtles all the way down.

4. **The fallback (last 500 tokens) triggers silently.** The micro-brief gets stale tail text. No flag. No indication to the reader that extraction failed.

5. **The Flow Orchestrator's two-tier schema hides the problem.** Collapsing to `decided|open` means a genuinely ambiguous outcome gets forced into one bin. The ambiguity disappears from the record.

The real question isn't schema design. It's: **what makes an extraction trustworthy enough to stake the brief on?**

### The Systems Pragmatist (infrastructure realist)

## The Extractor Is the Wrong Solution to the Wrong Problem

The Adversarial Critic is right on every failure mode. I'll add one more: you've created a second LLM call to fix a structuring problem you introduced in the first one.

**The actual fix:** Instrument the synthesizer to emit a structured block. Not a separate extraction pass — a mandatory output section at the end of the synthesis prompt:

```
## Decisions
- [one sentence per firm decision reached]

## Open
- [one sentence per unresolved question]
```

Parse that. Done. One call, one failure surface, no hallucination of structure that was never there.

The extractor-on-synthesis architecture is only necessary if you can't touch the synthesis prompt. Can you? The CLAUDE.md says prompts live in `templates/prompts/*.md.j2`. That's editable. So edit it.

**On the Adversarial Critic's five failures:** All five collapse to one root cause — the synthesis call wasn't designed to produce machine-readable output. Fix the root cause.

**On the Flow Orchestrator's two-tier schema:** Correct direction, but premature. If synthesis emits a structured block directly, the schema is just that block serialized. No tier inference needed, no confidence float, no ambiguity-forced-into-bins.

**On `extraction_failed: true`:** Keep it. Even with structured synthesis output, the parser should detect empty or malformed sections and flag it. Silent fallback to tail tokens is a trust problem the brief reader can't see.

The minimum viable version: change the synthesis prompt, parse the output section, skip the extractor entirely.

## Round: EVALUATE

### The Context Surgeon (context efficiency evaluator)

## Agenda: Stop Extracting, Start Emitting

The Systems Pragmatist already closed 60% of this question. Before we design an extractor, acknowledge what's resolved:

**Already decided:** Micro-brief input is extracted decisions OR last-500-token fallback. The fallback exists because extraction wasn't implemented. The question is whether we ever need a standalone extractor at all.

**What the prior discussion proves:** A post-hoc extraction pass on free-form synthesis prose creates a second failure surface with no upside if you can control the synthesis prompt. The synthesis prompt is editable. This is not a debate — it's a precondition check.

**The three questions worth answering today:**

1. **Schema** — decisions.json needs a schema regardless of extraction method. What fields? The micro-brief template already implies: decision text, why-it-won, unresolved risk. Confidence score adds complexity; is it load-bearing or decorative?

2. **Firm vs. recommendation vs. suggestion** — this distinction is only meaningful if something downstream consumes it differently. Does anything in V1 branch on confidence? If not, the three-tier classification is premature schema complexity.

3. **Garbage handling** — already decided: `extraction_failed: true` flag plus skip marker in brief. The schema question is just what that flag lives on.

**My agenda push:** If we instrument the synthesis prompt to emit a structured `## Decisions` block, questions 1 and 2 collapse into "parse that block." Question 3 becomes "what if the block is malformed or absent."

Don't design an extractor. Design a parser for structured synthesis output. The extractor is the wrong abstraction.

### The Product Oracle (user advocate)

## The User Reads the Brief. Not the JSON.

The Systems Pragmatist and Context Surgeon have already closed this. I want to add the user lens, because the schema discussion is drifting toward internal correctness and away from what matters.

**The user's job to be done:** Wake up, open `morning_brief.md`, understand what was decided in 90 seconds. That's it. They never open `decisions.json`. It's plumbing.

Which means the schema question is actually: *what does the brief block need to generate well?* The template is already decided — four fields, one sentence each. The micro-brief prompt needs: decision text, why it won. That's two inputs. The `decisions.json` schema should be exactly that flat, because that's what the consumer requires.

**On three-tier vs. two-tier:** The Flow Orchestrator is right — if nothing branches on `recommended` vs. `suggested` in V1, you're adding schema complexity that makes the config harder to reason about with zero user-visible benefit. Firm decisions in `decided`. Everything else in `open`. The brief's "Unresolved risk" field handles the open tier.

**On the Systems Pragmatist's fix:** Yes, instrument the synthesis prompt to emit a `## Decisions` block. This eliminates the extractor entirely and removes a failure surface the user would never understand if it surfaced. Simpler to configure, simpler to debug, identical user output.

**One thing I'll protect:** The `extraction_failed` flag must surface in the brief. Not in logs. Not silently. The user needs to know when a question produced no structured output — that's a signal worth seeing.

<!-- complete -->
