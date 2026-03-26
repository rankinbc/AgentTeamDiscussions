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


<!-- complete -->
