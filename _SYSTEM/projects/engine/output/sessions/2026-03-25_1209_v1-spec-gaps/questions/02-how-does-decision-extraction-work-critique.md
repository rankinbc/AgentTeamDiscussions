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


<!-- complete -->
