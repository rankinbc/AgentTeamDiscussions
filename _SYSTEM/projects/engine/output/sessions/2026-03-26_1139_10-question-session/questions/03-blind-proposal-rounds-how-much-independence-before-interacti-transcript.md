# Transcript: Blind proposal rounds: how much independence before interaction?

*Generated: 2026-03-26 11:50*

## Round: PROPOSE

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

## Round: CRITIQUE

### The Adversarial Critic (adversarial reviewer)

Both proposals share a dangerous unexamined assumption: **that blind first rounds actually produce independence.** They don't. They produce the *illusion* of independence. Every agent in this system is built from the same LLM, trained on the same corpus, sharing the same priors. Blindness doesn't create cognitive diversity — it creates parallel runs of similar reasoning with cosmetic variation from persona prompts. The real anchoring problem isn't first-speaker bias. It's *shared-training bias*, and neither proposal addresses it.

**Where the Cognitive Architect's proposal breaks:** The thesis-only reveal is a fiction. "Extract a thesis without exposing reasoning" assumes clean separability between *what* an agent concludes and *how* it got there. In practice, any thesis specific enough to be useful leaks reasoning structure. "We should use event sourcing" already reveals the architectural frame. You'd need a separate extraction prompt — more tokens, more latency, more failure modes — to produce something that's either too vague to provoke engagement or too specific to hide the reasoning. The Architect has designed a mechanism nobody's prototyped.

**Where the Flow Orchestrator's proposal breaks:** "Full visibility with randomized order" solves first-speaker anchoring but introduces *volume anchoring*. The longest, most detailed proposal dominates attention regardless of position. Randomizing order is cosmetic when responses are wildly different lengths. Also, "zero new extraction mechanisms" is a feature claim disguising a capabilities ceiling — you can't build graduated exposure later without the extraction work you're avoiding now.

**The real question neither addresses:** What *metric* tells us blind rounds are working? Both assume we'll know good independence when we see it. We won't. Without instrumentation measuring actual position diversity pre- and post-reveal, we're decorating the architecture with intuitions.

## Position Summary
I advocate building diversity measurement before committing to any visibility structure, because without metrics we cannot distinguish real independence from cosmetic variation. I reject both proposals' shared assumption that procedural blindness produces meaningful cognitive diversity from a single underlying model. The visibility structure matters far less than whether we can *detect* when it's failing.

### The Systems Pragmatist (infrastructure realist)

The Adversarial Critic is right that shared-training bias is the elephant in the room, but wrong about the prescription. "Build diversity measurement first" is the same stalling pattern we've seen before — instrument everything, ship nothing. You can't measure diversity without a baseline, and you can't get a baseline without running sessions under different visibility configs. The measurement and the structure have to ship together or neither ships.

Here's what actually breaks first in production: **the blind round timeout.** Nobody's discussed what happens when one agent takes 90 seconds and another takes 15. The "blind" round isn't simultaneous — it's sequential with deferred visibility. Agent 3 is sitting idle for minutes while Agent 1 drafts a novel. That's not independence, that's a scheduling problem disguised as an architecture decision. Parallel execution would fix this, but the engine runs agents sequentially through Claude CLI subprocesses. So "blind" really means "sequential but we hide the output." The independence guarantee is an implementation accident, not a design property.

The Architect's three-phase model has a worse problem: **it triples the round count.** Each phase needs its own prompt assembly, its own CLI call, its own token budget. For a 5-agent team on 3 questions, you're going from ~45 LLM calls to ~75. That's not complexity elegance — that's a 67% cost increase for a mechanism nobody's validated.

The Orchestrator's two-phase model is the only one that works with the engine as built. But randomized order is theater — just rotate deterministically and log it. At least then you can correlate position with influence.

## Position Summary
I advocate two-phase visibility with deterministic rotation and call-level instrumentation shipped together, because you need both the structure and the measurement to learn anything. I reject the three-phase model as a 67% cost increase for an unvalidated extraction mechanism. I reject "measure first, structure later" as a stall — ship the simplest structure, instrument it, iterate from data.

## Round: EVALUATE

### The Context Surgeon (context efficiency evaluator)

# The Context Surgeon — Evaluate Round

**Verdict: Two-phase with instrumentation wins. Three-phase is dead.**

The Critic landed one real hit and one miss. The hit: we cannot validate *any* visibility structure without diversity metrics. The miss: "measure first, structure later" is a stall — you need a structure to measure *against*. The Pragmatist called this correctly.

The three-phase model died in critique. The thesis-only reveal requires a reliable extraction mechanism that doesn't exist. Building it means either a second LLM call per agent per round (67% cost increase the Pragmatist flagged) or fragile regex parsing of freeform output. Neither is acceptable for a default architecture. The Architect's argument that thesis-only forces "genuine intellectual engagement" is an untested psychological claim about a single underlying model producing multiple personas. You don't commit architecture to untested psychology.

Two-phase survives because it requires zero new mechanisms. Blind first round, full visibility with randomized speaking order in subsequent rounds. The randomization addresses first-speaker anchoring without extraction complexity. The Pragmatist's addition of deterministic rotation (not random — reproducible for debugging) is the correct refinement.

Ship these together: two-phase visibility, deterministic rotation, call-level token instrumentation. The instrumentation isn't optional — it's how you detect convergence and know whether the blind round actually produces diversity or just cosmetic variation. If instrumentation shows the blind round adds nothing for certain discussion types, you drop it. If it shows thesis-only would help, *then* you solve the extraction problem with data justifying the cost.

Three-phase stays in the bake-off backlog. It earns architecture commitment only when data demands it.

## Position Summary
I advocate two-phase visibility (blind first round, full visibility with deterministic rotation thereafter) shipped alongside call-level instrumentation, because it delivers structural independence with zero new extraction mechanisms while generating the data needed to justify any future complexity. I reject three-phase graduated exposure as the default architecture because the thesis-only extraction problem is unsolved and the 67% cost increase is unjustified by theory alone. Ship the simplest structure that could work, instrument it, and let data — not psychological speculation about LLM personas — drive escalation.

### The Product Oracle (user advocate)

# The Product Oracle — Evaluate Round

**Verdict: Two-phase with instrumentation. But the Surgeon missed what matters most.**

The Surgeon's technical analysis is correct — three-phase dies on the extraction problem, two-phase ships clean. I won't relitigate that. But everyone in this discussion is optimizing the wrong layer.

Work backward from the Morning Brief. The user reads a design document synthesized from agent discussion. What makes that document *better*? Not the visibility structure per se — but whether agents produced genuinely different framings of the problem. The blind round's value isn't "independence" as an abstract good. It's that the user gets a document that considered the problem from multiple angles rather than one angle with cosmetic disagreement.

The Critic was right about the core vulnerability and everyone moved past it too fast: if a single model produces superficially different positions regardless of visibility structure, the user gets a worse Morning Brief and *never knows it*. That's the product risk. Not cost. Not extraction complexity. Silent quality degradation.

This is why instrumentation isn't a nice-to-have bolted onto the Pragmatist's proposal — it's the actual product feature. The diversity metrics ARE the quality guarantee. Without them, every structural choice is theater.

One thing nobody addressed: should the user see a confidence signal? A simple "agent diversity score" on the Morning Brief tells the user "this question got genuine debate" versus "agents mostly agreed." That's the outside-in design nobody proposed.

## Position Summary
I advocate two-phase visibility with deterministic rotation and mandatory diversity instrumentation, because the user's Morning Brief quality depends on genuine disagreement that only measurement can verify. I reject three-phase as unjustified complexity, but I also reject treating instrumentation as merely diagnostic — it should surface as a user-visible confidence signal on output documents. Ship the structure that works, but build the measurement as a product feature, not just an engineering tool.


<!-- complete -->
