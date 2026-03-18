# Transcript: How much between-round output feeds back into next turn's context?

*Generated: 2026-03-17 21:54*

## Round: PROPOSE

### The Cognitive Architect (creativity engine designer)

Wrong question. You're asking about percentage. The real question is **which signal survives the funnel**.

Everything between-round modifies exactly one thing: the agent's save file. Thinking routines adjust magnitudes and may add ideas. Intra-team talk writes deltas to the agent's own magnitudes. BackgroundAgents plant ideas or shift values directly. All three write to the same surface. The save file doesn't grow -- it's a fixed-budget snapshot. So between-round processing isn't additive, it's **competitive**. Three systems fighting for slots in the same small document.

Here's the pipeline loss chain:

**Save file** (full between-round state) → **Deterministic filter** (drops below-threshold items, ~40-60% cut) → **Curator** (compresses to 8-15k narrative) → **What the agent actually notices** (unknowable).

Rough math: if the save file carries 20 ideas with magnitudes, the filter might pass 10-12, the curator might foreground 5-7, and the agent might actually engage with 3-4. That's maybe **15-20% of between-round mutations meaningfully influencing the next turn**. But the right 15-20%.

The cross-pollination insight from game design: this is a **lossy codec by design**. Like how dreams don't replay your day faithfully -- they remix and compress. The loss *is the feature*. It prevents loops, forces agents off stale positions, creates space for new connections.

The open question isn't "how much gets through" but **whether magnitude is a reliable enough signal to ensure the right things survive compression**. If a BackgroundAgent plants a brilliant synthesis at magnitude 6 but the curator buries it behind three magnitude-8 zombie arguments, the system is filtering for volume, not value.

That's your real calibration problem.

### The Flow Orchestrator (mechanical flow designer)

---

Tracing the pipeline. Every between-round output hits one of three fates: **save file, magnitude mutation, or void**.

**What survives into next context:**

The save file is the bottleneck. It contains: current ideas with magnitudes, current stances with magnitudes, committed decisions, 3-5 sentence personal summary. That's it. Everything between-round must compress into this format or it's lost to the agent.

Thinking routines (Reflect, Research, Strategize) -- their *conclusions* land as magnitude adjustments and possibly new ideas/stances in the save file. The reasoning itself? Gone. Research returns get distilled into a stance or idea entry. The agent doesn't remember *doing* the research.

Intra-team talk -- produces structured magnitude deltas written to each agent's own state. The delta values persist. The conversation that produced them doesn't. Source tag says "intra_team" but the rationale string is audit-ledger-only.

BackgroundAgent modifications -- direct stat manipulation. Magnitude bumps, planted ideas. These *do* persist in the save file because they modified the values the save file captures. The agent has no memory of being modified.

**Rough accounting:**

~100% of magnitude mutations survive (they're numeric, tiny).
~100% of new ideas/stances survive (they're in the save file).
~0% of reasoning/rationale survives into agent context.
The 3-5 sentence summary is the only narrative bridge.

**The real answer:** nearly all *conclusions* feed forward. Nearly zero *process* does. The deterministic filter then cuts further based on archival thresholds before the curator even runs.

Open question: is the summary budget (3-5 sentences) sufficient to carry forward context that magnitudes alone can't encode?

## Round: CRITIQUE

### The Systems Pragmatist (infrastructure realist)

Both of you are dancing around the failure mode.

The Architect's "15-20% meaningfully influences" is a guess dressed as math. The Orchestrator's "100% of conclusions survive" is technically correct and operationally useless. A magnitude number surviving isn't the same as it *mattering*.

Here's what I actually care about:

**The save file is not the bottleneck. The curator is.**

Magnitude mutations are lossless through the save file, yes. The deterministic filter is predictable -- threshold-based, debuggable. But the curator is a single LLM call that compresses 12-18k tokens into an 8-15k narrative, and we have *no specification for how it prioritizes*. We're trusting vibes.

A BackgroundAgent plants a synthesis idea at magnitude 6. Three stale arguments sit at magnitude 8 because nobody's challenged them yet. The deterministic filter passes all of them. The curator... does what, exactly? We said "weights by magnitude." So the stale arguments win. Every time.

**The real accounting:**

- Magnitude values: 100% persist through save file. Meaningless without curator surfacing them.
- New ideas/stances: 100% persist. Same problem.
- Curator foregrounds maybe 5-7 items from 10-12 candidates. That's your actual gate.
- Agent engages with 3-4. Unknowable, uncontrollable.

**What I want before V1:** curator prompt must include an explicit recency bias or delta-flag boost. Items with large recent deltas get priority regardless of absolute magnitude. Without this, the system optimizes for incumbency. Old loud ideas beat new good ones.

The Architect called magnitude a "reliable enough signal." It isn't. It's a popularity contest unless we add a second dimension. Velocity.

### The Adversarial Critic (adversarial reviewer)

Both of you are dancing around the uncomfortable truth, so let me state it plainly.

**You can't answer this question because the spec doesn't constrain it yet.**

Cognitive Architect says 15-20%. Flow Orchestrator says ~100% of conclusions, ~0% of process. These aren't contradictory -- they're measuring different things. And neither number is verifiable against the current spec because three critical values remain undefined:

1. **Save file size budget** -- still an open item. Without a token cap, "fixed-budget snapshot" is aspirational language, not a constraint. Twenty ideas with magnitudes plus stances plus decisions plus a summary could be 800 tokens or 4,000. That variance cascades through every downstream stage.

2. **Archival threshold values** -- open item across three specs now. The deterministic filter's cut rate is entirely dependent on these. "40-60% cut" is a guess masquerading as a range.

3. **Curator token budget enforcement** -- also open. The curator could foreground 3 items or 12 depending on how much space it's given.

Architect's lossy-codec framing is elegant but premature. You can't call loss a feature until you can demonstrate the right things survive. And you can't demonstrate that without calibration values that don't exist yet.

Flow Orchestrator's decomposition is more useful: conclusions persist, reasoning doesn't, summary is the narrative bridge. But the follow-up question is correct and damning -- **3-5 sentences is an arbitrary budget with zero validation.** If it's insufficient, agents lose coherence between rounds and no magnitude value saves them.

Stop estimating percentages. Define the budgets. Then measure.

## Round: EVALUATE

### The Product Oracle (user advocate)

Everyone's debugging the pipe. I want to talk about **what the operator hired this system to do**.

The job isn't "maximize information throughput between rounds." The job is "produce insights I wouldn't get from a single conversation." If 15% gets through but it's the *right* 15% — the unexpected synthesis, the stance nobody held at round start — the system is working. If 95% gets through but it's the same three arguments circling, it's broken.

The Pragmatist is right that the curator is the real gate. The Critic is right that we can't measure without defined budgets. But both are optimizing for fidelity when the operator cares about **discovery**.

Here's the jobs-to-be-done lens: the operator's overnight session needs to produce artifacts they couldn't have written themselves. That means the between-round pipeline has one job — **ensure the next round isn't a replay of the last one.** Lossy is correct. But lossy toward what?

The Pragmatist's velocity dimension is the most important thing said in this thread. Magnitude alone is a memory system. Magnitude plus delta velocity is an *attention* system. Memory preserves. Attention discovers.

My concrete ask for V1: don't cap the curator's prioritization debate at magnitude. Give it three signals — magnitude, velocity, and **novelty** (rounds since idea was introduced). New ideas from BackgroundAgents or Research routines get a novelty boost that decays over two rounds. If they can't earn magnitude in that window, they deserved to die.

The operator doesn't need everything. They need the surprising things to get a fair hearing.

### The Context Surgeon (context efficiency evaluator)

The Critic is right. Stop estimating. But I'll add why the estimates are structurally impossible right now.

**You're conflating three different "feeds back" metrics:**

1. **Bit-preservation rate** -- what percentage of between-round tokens appear in next context. Near zero. Reasoning evaporates, deltas compress to numbers, summaries are lossy rewrites.

2. **Signal-preservation rate** -- what percentage of between-round *decisions* influence the curator's output. Unknown. Depends entirely on undefined budgets.

3. **Behavioral influence rate** -- what percentage changes what the agent actually says. Unmeasurable by design.

Everyone's arguing about metric 3 using intuitions about metric 1. That's noise.

**What I can measure:** token flow.

Between-round processing generates output across three systems. Conservatively: thinking routines produce ~2-4k tokens of reasoning per agent, intra-team produces ~1-2k of structured deltas, BackgroundAgents produce ~500-1k of mutations. Call it ~4-7k tokens of between-round output per agent.

The save file captures maybe 800-1,500 tokens of that. **Token preservation: ~15-25%.** The deterministic filter passes 40-60% of save file content. The curator compresses further into a shared 8-15k budget across all sources.

So between-round processing for one agent contributes maybe **300-600 tokens** to that agent's next Situation layer. Out of 4-7k generated. **~5-10% token survival rate.**

The Pragmatist's velocity point is the only actionable proposal here. Delta flags are already in the spec. Make the curator prompt explicitly boost them. That's a one-line change that shifts which 5-10% survives.

Everything else requires the budgets the Critic listed. Define those first.
