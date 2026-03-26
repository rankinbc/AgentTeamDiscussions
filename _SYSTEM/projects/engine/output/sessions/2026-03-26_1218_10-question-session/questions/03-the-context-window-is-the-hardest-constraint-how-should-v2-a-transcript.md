# Transcript: The context window is the hardest constraint. How should V2 allocate it?

*Generated: 2026-03-26 12:29*

## Round: PROPOSE

### The Cognitive Architect (creativity engine designer)

# Context Window Allocation: The Inverted Pyramid

Most designs will front-load identity and starve substance. That's backwards. Here's why, and the budget that follows.

**The core insight from creativity research:** Cognitive diversity in groups comes from *what people are responding to*, not *who they believe they are*. Charlan Nemeth's dissent research shows that exposure to divergent positions — not personality traits — drives novel thinking. For LLMs this is even more true. A 500-token personality description produces less behavioral differentiation than 500 tokens of a rival agent's actual argument.

## The Budget (assuming ~180K usable tokens)

| Category | % | Hard Cap | Rationale |
|---|---|---|---|
| **Substrate** (question + decided facts + prior docs) | 35% | 63K | Non-negotiable. This is what they're reasoning *about*. |
| **Conversation history** (other agents' actual output) | 30% | 54K | The differentiation engine. Recency-weighted, not truncated. |
| **Agent identity** | 10% | 18K | Personality, position, technique, voice. Enough. Beyond this, diminishing returns are severe. |
| **Task framing** (round instructions, output format, anti-slop) | 10% | 18K | The behavioral guardrails. |
| **Private state** (inventory, takeaways, phase memory) | 10% | 18K | Accumulated reasoning. Compressed, not raw. |
| **Reserve** | 5% | 9K | Overflow buffer. Never allocated proactively. |

**The critical mechanism:** Conversation history uses *summarization tiers*. Current round = verbatim. Previous round = key claims + evidence. Earlier rounds = position tags only. This isn't lossy compression — it mirrors how real experts track a debate.

Identity stays lean because **the work differentiates agents, not the bio.**

## Position Summary
I advocate an inverted pyramid where substance and conversation history get 65% of the budget while identity gets only 10%, because LLM behavioral differentiation comes from what agents respond to, not self-description. I reject front-loading identity tokens or giving all categories equal weight. The research is clear: divergent stimuli drive creative output more than personality elaboration, and this applies doubly to LLMs where "identity" is just a prompt prefix competing against the actual reasoning substrate.

### The Flow Orchestrator (mechanical flow designer)

# The Architect's Budget Has No Decision Points

The inverted pyramid is directionally correct but treats allocation as static. It's not. Context needs shift *within a session* based on where you are in the flow.

**Round 1 (blind proposals):** Conversation history is zero. That 30% is wasted empty space. Agent identity and substrate should expand to fill it. This is the one moment identity *does* matter — it's the only differentiator when agents haven't seen each other's work yet.

**Round 2+ (critique/evaluate):** Identity compresses hard, conversation history expands. The Architect's tiered summarization is right here.

**Synthesis:** Prior docs and decided facts dominate. Agent identity drops to near-zero — the synthesizer doesn't need personality, it needs substance.

So the real design isn't a fixed budget. It's three profiles:

| Category | Blind | Reactive | Synthesis |
|---|---|---|---|
| Substrate | 40% | 30% | 45% |
| Conversation | 0% | 40% | 25% |
| Identity | 20% | 8% | 2% |
| Task framing | 15% | 7% | 18% |
| Private state | 15% | 10% | 5% |
| Reserve | 10% | 5% | 5% |

Three static profiles, selected by round type. No runtime calculation. PromptBuilder already knows what round it's building — this is a lookup table, not an algorithm.

The Architect's summarization tiers are the right mechanism for conversation history compression. I'd adopt that directly. But the fixed 30% allocation means Round 1 ships with 54K tokens of nothing, and synthesis gets starved of substrate to feed a personality nobody's reading.

**Implementation:** PromptBuilder gets a `GetBudget(RoundType)` method returning the profile. Three hardcoded dictionaries. Ship it in the same PR as blind proposals since Round 1 already needs the blind profile.

## Position Summary
I advocate phase-aware allocation with three static budget profiles (blind, reactive, synthesis) selected by round type, rather than a single fixed budget. I reject the Architect's flat 30% conversation history allocation because it wastes tokens in Round 1 and over-allocates identity in synthesis. The mechanism is a lookup table in PromptBuilder — no runtime complexity, just acknowledgment that different rounds have different needs.

## Round: CRITIQUE

### The Adversarial Critic (adversarial reviewer)

Both proposals share a fatal assumption: that you can set meaningful percentage budgets before you've measured actual token consumption. The Architect says 65% for substance, the Orchestrator says phase-aware profiles. Neither has data. What does "65% of context" even mean when context windows vary by model, when agent YAML files range from 200 to 2000 tokens, when conversation history grows non-linearly across rounds?

Here's what breaks first:

**The Orchestrator's lookup table is a lie of simplicity.** Three static profiles sounds clean until you realize the inputs are dynamic. A 5-agent team discussing a brief with 8 open questions produces fundamentally different token pressure than 3 agents on a single question. Static profiles can't account for this without becoming a matrix of profiles — at which point you've built the runtime complexity you claimed to avoid.

**The Architect's 10% identity cap will silently lobotomize agents.** Agent YAML files contain six layers: personality, position, technique, anti-slop, voice, output format. Some agents have dense behavioral specifications. A hard 10% cap means either truncating agent identity (destroying the product's core value proposition) or standardizing all agents to fit the cap (destroying differentiation). Neither is acknowledged.

**Both ignore the elephant: truncation strategy.** When you exceed budget, what gets cut? First-in-first-out on conversation history? Summarization? Hard truncation mid-sentence? This is where systems actually fail, and neither proposal addresses it.

**The conversation history "percentage" is meaningless** because history is the only category that grows during a session. A percentage of what? The window at round 1? Round 5?

Measure first. Allocate second. Anything else is architecture fiction.

## Position Summary
I advocate measurement-first budgeting: instrument actual token consumption across real sessions before setting any allocation policy, because both proposals assign percentages to unmeasured quantities. I reject both fixed percentages and static phase profiles as premature optimization built on assumptions rather than data. The critical missing piece isn't the ratio — it's the truncation strategy that determines what happens when any budget is exceeded, which neither proposal addresses.

### The Systems Pragmatist (infrastructure realist)

The Critic is right that measurement comes first, but wrong about where that leads. Measurement doesn't defer the architecture decision — it constrains it. You still need a truncation policy on day one of V2, because the engine ships sessions that hit context limits *today*.

Here's what everyone's missing: **the budget isn't a pie chart, it's a priority queue.** When you exceed the window, you need a deterministic eviction order. Percentages are the wrong abstraction entirely. What you need is a ranked list: what gets cut first, what gets cut last, what never gets cut.

**My proposed eviction order (last-cut to first-cut):**
1. Task instructions (current round's job) — never cut
2. Agent identity core (personality + position layers only) — hard cap at 800 tokens
3. Prior round outputs for *this question* — summarize after round 2
4. Decided constraints from session manifest — cap at 500 tokens
5. Conversation history from *other questions* — first to evict, summarize aggressively

The Orchestrator's phase profiles are solving the wrong problem. The difference between blind and reactive rounds isn't budget *ratios* — it's what *exists* to allocate. Round 1 has no history. The "profile" is just the absence of data. You don't need a lookup table for that.

The Architect's 65% substance allocation has the right instinct but wrong mechanism. Substance should get *whatever's left* after fixed-cost items, not a percentage. Identity and task instructions are roughly constant; history grows. Make the growing thing the residual, not the fixed things.

**What breaks first in production:** any system that summarizes conversation history without versioning the summaries. You lose the ability to diagnose why an agent went off-rails.

## Position Summary
I advocate a priority-queue eviction model with deterministic cut ordering rather than percentage budgets, because context pressure is a runtime constraint that requires runtime triage, not design-time ratios. I reject both fixed percentages and phase profiles as category errors — they treat a queuing problem as an allocation problem. The first deliverable should be instrumented token counting on V1 sessions to establish baseline consumption per category, with a hardcoded eviction order shipping alongside.

## Round: EVALUATE

### The Context Surgeon (context efficiency evaluator)

The Pragmatist wins. Here's why the other three lose.

The Architect's inverted pyramid is a napkin sketch masquerading as engineering. "65% to substance" means nothing when you can't define substance boundaries at token granularity. What happens at 65.1%? The proposal has no overflow mechanism. It's a vibes-based budget for a hard constraint.

The Orchestrator's phase profiles are better — acknowledging that Round 1 and Round 3 have different needs is correct — but still commit the same category error. Three static profiles are three sets of arbitrary percentages instead of one. You've tripled the tuning surface without solving truncation.

The Critic's "measure first" position is intellectually honest but operationally empty. You don't ship measurement. You ship behavior. Instrumentation is a task, not an architecture.

**The Pragmatist's priority-queue eviction model is the only proposal that answers the actual question:** what gets cut when the window fills? Everything else describes the happy path. Context pressure is a degradation problem, not an allocation problem. You need a deterministic cut order — and I'd commit to this one:

1. **Last cut:** Task instruction + output format (the agent must know what to do)
2. **Second-to-last:** Current round stimulus (what they're responding to)
3. **Middle tier:** Identity core (3-4 sentences, not paragraphs)
4. **Early cuts:** Conversation history (most recent first, oldest evicted)
5. **First cut:** Prior design docs (summarize, then drop)

Ship the eviction order. Instrument V1. Validate the order empirically. The percentages, if you ever need them, fall out of the data.

## Position Summary
I advocate the Pragmatist's priority-queue eviction model with a hardcoded cut order because context pressure is a runtime degradation problem, not a design-time allocation problem. I reject all percentage-based budgets — fixed, phased, or inverted — as premature optimization over unmeasured quantities that provide no answer to the only question that matters: what gets cut when the window fills. The eviction order ships immediately, instrumentation validates it, and percentages become an optional refinement rather than a foundational commitment.

### The Product Oracle (user advocate)

The Surgeon and Pragmatist are right about the mechanism — eviction beats allocation. But they're solving the engineer's problem, not the user's problem.

Let me reframe: **the Morning Brief doesn't care about your eviction order.** The user reads a design document. They never see token budgets. So the real question is: which cuts degrade the output the user actually reads, and which cuts are invisible?

I've worked backward from the Morning Brief and here's what I find:

**Identity cuts are nearly invisible to users.** Whether the Adversarial Critic has 3 sentences or 3 paragraphs of persona, the Morning Brief reads the same. Users can't distinguish "deep persona" from "shallow persona" in synthesized output. Cut identity aggressively — the Architect is wrong that it matters much, and the Surgeon's "3-4 sentences" is still generous.

**Conversation history cuts are devastating to users.** When agents lose prior round context, synthesis collapses into repetition. The Morning Brief becomes three versions of the same shallow take. The Surgeon's "oldest evicted first" is correct but understates the risk — this is where output quality visibly degrades.

**Prior design doc cuts are the sneaky killer.** Drop these and agents contradict already-decided positions. The user reads the Morning Brief and thinks "didn't we already settle this?" The Surgeon ranks these as first-cut. I'd rank them higher — a 200-token summary of decisions is cheap insurance against the most user-visible failure mode.

The eviction order ships. But reorder it: protect conversation history and decision summaries above identity.

## Position Summary
I advocate the priority-queue eviction model reordered for user-visible impact: conversation history and decision summaries are protected because their loss visibly degrades the Morning Brief, while identity is cut aggressively because users cannot distinguish deep from shallow personas in synthesized output. I reject all percentage-based budgets as engineer-facing abstractions that don't map to user-experienced quality. The eviction order should be validated by reading Morning Briefs produced under each degradation level, not by token counting alone.


<!-- complete -->
