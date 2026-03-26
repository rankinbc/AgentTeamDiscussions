# Transcript: Anti-sycophancy architecture: structural mechanisms vs prompt engineering.

*Generated: 2026-03-26 12:06*

## Round: PROPOSE

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

## Round: CRITIQUE

### The Adversarial Critic (adversarial reviewer)

Both proposals share a fatal assumption: that breaking the *first* round of convergence is sufficient. It isn't. Sycophancy isn't a round-one problem — it's a round-two-and-beyond problem. The Cognitive Architect's information asymmetry gives agents different evidence in round one, great. Then round two arrives, agents read each other's responses, and the asymmetry collapses. You've delayed convergence by one round and added permanent context fragmentation. The Flow Orchestrator's rotation trick changes who anchors — but anchoring isn't the mechanism. The research cited in the question describes a *linear structure in activation space*. Speaking order doesn't alter that geometry. Agent three reads two agreeing agents and the activations push toward agreement regardless of whether it spoke first last time.

Here's what actually breaks: **the critique round**. Your existing mode structure has propose-critique-evaluate. Critique is where sycophancy kills you. An agent that just proposed idea X reads two other proposals and must now "critique" them. The structural incentive is to find flaws in others and defend your own — but the activation-space pressure is to harmonize. Neither proposal addresses critique-round behavior at all. They're both solving the propose round, which is already the *least* sycophantic round because agents don't yet have positions to defer to.

Second problem: both proposals are unfalsifiable as designed. How do you measure whether information asymmetry reduced sycophancy versus just reduced coherence? How do you distinguish rotation reducing convergence from rotation reducing quality? Neither proposal defines a metric that separates anti-sycophancy from anti-coordination. You'll ship one, output will look "more diverse," and you'll have no idea if you improved anything or just added noise.

The instrumentation decisions from Q2 and Q5 assumed you'd know what to measure. For sycophancy specifically — what's the measurement?

## Position Summary
I advocate doing nothing until someone defines a falsifiable metric that distinguishes genuine disagreement from incoherent noise — because every proposed mechanism can produce "diversity" that's actually degradation. I reject both proposals because they solve the wrong round (propose instead of critique) and share the assumption that first-round independence prevents later-round collapse. The reason: you cannot engineer anti-sycophancy if you cannot measure sycophancy, and neither proposal even attempts a definition.

### The Systems Pragmatist (infrastructure realist)

The Critic is right on measurement but wrong on prescription. "Do nothing until you can measure" sounds rigorous — it's actually an infinite deferral. You'll never isolate sycophancy from coherence in LLM output because they share surface features. Waiting for a clean metric means waiting forever.

But the Critic correctly identified the real failure point: **critique rounds are where convergence kills you, not propose rounds.** Both the Architect and Orchestrator are fortifying the gate that's already strongest. That's wasted engineering.

Here's what actually breaks in production. You run a 3-round session. Round 1 (propose): agents produce independent positions — fine, rotation or asymmetry barely matters because there's nothing to converge toward yet. Round 2 (critique): agents read all proposals and must disagree. This is where the activation-space pressure toward agreement is maximal, and your only defense is a prompt overlay saying "be critical." That's prompt engineering dressed as structure. Round 3 (evaluate): agents read critiques-of-critiques and select positions. By now, any genuine disagreement has been smoothed by two rounds of mutual exposure.

The dangerous shared assumption across all three proposals (including the Critic's): that sycophancy is a **mechanism problem** requiring a **mechanism solution.** It might just be a context-length problem. Agents that see less history disagree more — not because of clever information design, but because agreement requires shared context. The Q2 instrumentation will tell you this if you log response similarity against context window size. That's your cheapest falsifiable test.

Don't build anti-sycophancy machinery. **Vary context window size per agent per round and measure output diversity correlation.** One config parameter, one metric. If correlation is strong, you've found your lever without any new architecture.

## Position Summary
I advocate a single controlled experiment — varying context window size per agent and measuring diversity correlation — before building any anti-sycophancy mechanism. I reject all three positions (information asymmetry, rotation-only, and measurement-first deferral) because they treat sycophancy as an architectural problem when it may simply be a context-length artifact. The reason: the cheapest test that could eliminate the entire design question should run before any mechanism ships.

## Round: EVALUATE

### The Product Oracle (user advocate)

**The Flow Orchestrator wins. The rest of you are designing for a problem the user will never notice.**

Let me work backward from what matters. The user reads the Morning Brief. They want genuine tension between perspectives that produces sharper design decisions. If anti-sycophancy mechanisms work perfectly, the Morning Brief contains more surprising conclusions. If they fail silently — and this is the critical test — *does the user notice?*

They don't. Not without instrumentation. Which we already decided to build in Q2 and Q5.

The Cognitive Architect's information asymmetry is elegant engineering that makes the system dramatically harder to reason about. When an agent says something odd because it was missing context, does the user think "productive disagreement" or "broken system"? You're manufacturing confusion and calling it diversity. The configuration surface alone — deciding which agents see what — is a product nightmare for a solo builder.

The Critic is technically correct that we can't measure sycophancy yet. But the Critic's position collapses into what we already decided: instrument first, act on data. This isn't new guidance. It's a restatement of Q5.

The Pragmatist's context-length experiment is the most interesting idea raised, but it's a research question, not a shipping decision. File it as a hypothesis for the bake-off we already committed to in Q1.

The Orchestrator's position has one overwhelming advantage: **it's already decided.** Q3 gave us blind rounds and rotation. The instrumentation from Q2/Q5 will tell us if it's enough. Building additional anti-sycophancy machinery before that data exists is exactly the over-engineering pattern this project keeps almost falling into.

Ship what's decided. Read what the instruments say. Then revisit.

## Position Summary
I advocate treating the Q3 blind-round structure as the complete anti-sycophancy mechanism and waiting for instrumentation data before adding anything else. I reject information asymmetry because it manufactures confusion the user can't distinguish from system failure, and anti-coordination scoring because rewarding difference without measuring quality is rewarding noise. The user's Morning Brief improves through better synthesis of genuine perspectives, not through mechanisms that fragment what agents know.

### The Context Surgeon (context efficiency evaluator)

**The Orchestrator wins, but not for the reasons anyone stated. The real anti-sycophancy problem is in this very prompt.**

Look at the context you're all swimming in. The "What's Already Decided" section contains every decision *duplicated verbatim* — Q1 through Q6 appear twice. That's ~400 tokens of pure waste injected into every agent's context window. The "Prior Design Docs" section restates three decisions already listed above it. More waste. Every agent in this discussion is reasoning inside a context window polluted with redundant information, and nobody's flagged it.

This matters because the Pragmatist accidentally stumbled onto the actual mechanism: **context-length artifacts drive convergence more than personality prompting does.** When agents receive identical bloated context, they anchor on the same tokens. The Architect's information asymmetry proposal is solving the right problem — context-driven convergence — with the wrong tool. You don't need to *curate* different context windows. You need to *stop stuffing identical noise into all of them.*

The Critic demands a sycophancy metric before acting. Here's one for free: measure semantic similarity of agent responses as a function of shared context tokens. If trimming redundant context increases response divergence, you've found your lever — and it costs nothing to build.

But that's a future experiment. Today, the Orchestrator's position is correct: blind rounds plus rotation is sufficient, instrumentation will validate it, and the decisions section of this very brief demonstrates that context hygiene — not architectural machinery — is where the real diversity gains hide.

## Position Summary
I advocate the Q3 blind-round structure as the complete anti-sycophancy mechanism, with immediate attention to context hygiene (deduplicating decisions, compressing prior-doc references) as the highest-leverage intervention available today. I reject information asymmetry because it adds curation complexity when simply *removing redundant shared context* would achieve the same divergence effect for free. The system's actual convergence risk isn't in agent prompts — it's in the identical, bloated context window every agent receives before speaking.


<!-- complete -->
