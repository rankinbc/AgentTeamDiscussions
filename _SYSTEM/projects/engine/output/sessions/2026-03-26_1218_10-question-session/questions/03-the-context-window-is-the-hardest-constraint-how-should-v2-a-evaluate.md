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
