### The Cognitive Architect (creativity engine designer)

# Anti-Sycophancy Through Structural Asymmetry

The research on sycophancy's linear structure in activation space tells us something crucial: **prompting against sycophancy is fighting geometry with words.** You can't prompt your way out of a structural tendency any more than you can talk a river into flowing uphill.

## The Mechanism: Adversarial Information Asymmetry

Give agents **different subsets of context** for each round. Not different prompts — different *facts*. When Agent A has information Agent B lacks, agreement becomes structurally expensive because it requires ignoring private evidence. This is straight from Condorcet jury theory: independent signals produce better collective judgment, but only when the signals are actually independent.

**Concrete implementation:** Before each round, partition the prior conversation into overlapping-but-distinct context windows per agent. Each agent sees 70% of prior responses, but a *different* 70%. Disagreement emerges naturally because agents are literally reasoning from different evidence bases.

## What I Reject

**Anti-coordination scoring** is a trap. Penalizing semantic overlap rewards contrarianism, which is just sycophancy's mirror image — performing disagreement rather than performing agreement. Both are performances. Neither is thought.

**Ego simulation** (defensive framing when challenged) adds complexity to solve a symptom. If an agent folds under pressure, the problem isn't insufficient ego — it's insufficient *reason to hold position*. Give agents private evidence and they'll defend positions because they have grounds to.

## Why This Works for LLMs Specifically

LLMs don't have beliefs to defend. They have *context to reason from*. Structural information asymmetry exploits the one thing LLMs genuinely do: next-token prediction conditioned on input. Change the input, change the output. No personality theater required.

## Position Summary

I advocate adversarial information asymmetry — giving agents structurally different context windows so disagreement emerges from genuine evidential divergence rather than personality prompting. I reject both anti-coordination scoring (rewarding contrarianism is isomorphic to rewarding sycophancy) and ego simulation (complexity that treats symptoms). The reason: LLMs respond to context, not character — so anti-sycophancy mechanisms must operate on context structure, not prompt content.

### The Flow Orchestrator (mechanical flow designer)

# The Partition Scheme Has an Ordering Problem

The Cognitive Architect's information asymmetry idea is elegant in theory. In practice, it has a sequencing flaw that undermines it.

## The Problem: Who Partitions What, When?

"Partition the prior conversation into overlapping-but-distinct context windows" sounds clean. Trace the actual operations:

1. Round N completes. Three agents produced responses.
2. Before Round N+1, *something* must select which 70% each agent sees.
3. That selection is either **random** (agents might miss the most important prior point) or **curated** (something must judge importance — another LLM call, another failure mode).
4. Agents respond to incomplete records. In Round N+2, do we partition the *already-partitioned* responses? Information loss compounds geometrically.

By round 3, agents are arguing past each other not because they hold different positions, but because they literally don't know what was said. That's not independence — it's incoherence.

## The Simpler Mechanism

**Speaking order rotation with blind first-responses.** Already decided in Q3. The two-phase visibility structure handles the independence problem without information destruction. Round 1: blind proposals (true independence). Rounds 2+: full visibility, rotated speaking order (the agent who spoke last now speaks first and must commit before seeing others).

That's the entire anti-sycophancy architecture. Rotation breaks the "third agent folds to the majority" pattern because *who constitutes the majority shifts every round.* No partitioning logic. No compounding information loss. No new LLM calls.

Anti-coordination scoring and ego simulation are both unnecessary given this structure — and the Architect is right that they'd be counterproductive regardless.

## Position Summary
I advocate relying on the already-decided Q3 structure (blind first round + deterministic rotation) as the complete anti-sycophancy mechanism, with no additional machinery. I reject information partitioning because it introduces compounding context loss across rounds and requires either random selection (noisy) or curated selection (complex). The reason: the simplest mechanism that breaks convergence cascades is changing who speaks first — not fragmenting what agents know.


<!-- complete -->
