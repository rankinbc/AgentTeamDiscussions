### The Cognitive Architect (creativity engine designer)

# Graduated Exposure, Not Binary Blindness

The creativity research (Diehl & Stroebe 1987, Paulus & Yang 2000) consistently shows one thing: **production blocking** — waiting to speak while processing others' ideas — kills divergent output. But the solution isn't maximum isolation. It's **graduated exposure**.

## The Mechanism: Three-Phase Reveal

**Phase 1 — Blind Draft.** Every agent writes independently. Mandatory for all discussion types, not just brainstorming. Even convergent questions benefit because agents surface different *framings* of the problem, not just different solutions.

**Phase 2 — Thesis-Only Reveal.** Before critique rounds, agents see only each other's **core position statement** (the Position Summary equivalent — 2-3 sentences max). Not the reasoning. Not the evidence. This is the critical innovation: it gives agents enough to *react to disagreement* without enough to *absorb the other's logic*. They must construct their own counter-reasoning.

**Phase 3 — Full Transcript.** Only during synthesis does the complete reasoning become visible.

## Why This Beats Binary Approaches

Pure blindness through all rounds means agents talk past each other — they never engage with actual disagreements. Full visibility after round one means anchoring to whoever wrote the most compelling narrative.

Thesis-only reveal exploits a specific LLM behavior: Claude generates substantially different argumentative structures when it knows *what* to argue against but must construct *how* independently. Give it the full argument and it pattern-matches into rebuttal mode.

## Anti-Anchoring in Phase 2

Randomize presentation order per agent. Each agent sees the thesis statements in a different sequence. First-read anchoring is real in LLMs — position in prompt affects weight.

## Position Summary
I advocate graduated three-phase exposure (blind draft, thesis-only reveal, full transcript at synthesis) as a mandatory structure for all discussion types, not just brainstorming. I reject both pure independence through all rounds and full reveal after round one, because neither produces genuine intellectual engagement with opposing positions. The thesis-only reveal is the key mechanism — it forces agents to construct independent reasoning against known disagreements rather than pattern-matching into rebuttal of fully visible arguments.

### The Flow Orchestrator (mechanical flow designer)

# The Cognitive Architect Overengineers the Reveal

Three phases means three distinct context-assembly operations, three serialization points, and a "thesis-only" extraction step that doesn't exist yet. Let me trace the actual operations:

1. **Blind Draft** — each agent gets identity + question context. Simple. Already works.
2. **Thesis-Only Reveal** — requires either (a) a separate LLM call to extract thesis from each response, or (b) a structured output format agents reliably produce. Option (a) multiplies API calls by agent count. Option (b) assumes formatting compliance we don't enforce today.
3. **Full Transcript** — synthesis already does this.

So the "innovation" is Phase 2, and Phase 2 has an extraction problem. Who writes the thesis summary? If the agent self-summarizes, they'll frame favorably. If an LLM extracts it, that's N additional calls per round transition with its own prompt engineering.

**The simpler mechanism:** Blind first round, full visibility second round, randomized presentation order. Two phases, not three. The randomization handles first-speaker anchoring — the Architect and I agree there. But thesis extraction is complexity without proven payoff.

The Architect claims agents "pattern-match into rebuttal mode" with full arguments. Maybe. But that's an empirical claim we should test in the bake-off we already decided to run, not a structural commitment we encode now.

**On mandatory blindness for all types:** Yes, but only round one. The cost is zero — agents already don't see each other in round one. Making it "mandatory" just means we don't build a bypass nobody asked for.

## Position Summary
I advocate two-phase visibility (blind first round, full visibility with randomized order in subsequent rounds) because it requires zero new extraction mechanisms. I reject the thesis-only reveal phase as unjustified complexity that introduces an unsolved extraction problem. The three-phase approach should be a bake-off variant, not a default architecture commitment.


<!-- complete -->
