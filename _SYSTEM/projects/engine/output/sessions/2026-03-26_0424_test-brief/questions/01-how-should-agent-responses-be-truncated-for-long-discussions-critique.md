### The Adversarial Critic (adversarial reviewer)

# The Uniform Window Has a Uniform Failure Mode

The Flow Orchestrator's proposal is attractively simple and specifically wrong about one thing: assuming all agents lose coherence the same way.

**Five problems with "one tier, same window for everyone":**

1. **Summary quality is load-bearing and unvalidated.** The entire proposal rests on "the synthesizer already produces something close to this." Close isn't close enough when it's the *only* history agents see beyond N messages. One bad summary propagates to every agent simultaneously. There's no redundancy. The CONCERNS.md already flags synthesizer fragility — now you're making it the single point of failure for all context.

2. **N is a magic number with no sizing rationale.** What's N? 5 messages? 50? The proposal says "configurable" as if that answers the question. Wrong N means agents either rehash settled points or forget active tensions. You'll spend more time tuning N than building role filters.

3. **Uniform windows guarantee uniform blind spots.** If every agent sees the same truncated history, they all miss the same things. Nobody catches the dropped constraint. That's not coherence — it's synchronized amnesia.

4. **"Instrument then decide" assumes you ship instrumentation.** Where's that in the proposal? You can't defer role filtering to data you're not collecting.

5. **Summary-as-scaffold conflates two jobs.** A scaffold tracks structure. A summary compresses content. Forcing the synthesizer to do both means it does neither well.

The proposal is right that three tiers is premature. But "one tier plus hope" isn't architecture — it's a demo that works until message 40.

What's the failure detection plan when the summary drifts?

### The Systems Pragmatist (infrastructure realist)

# The Critic Found Real Holes. Here's What to Do About Them.

The Adversarial Critic is right that uniform windows create synchronized blind spots. That's a legitimate failure mode, not a theoretical concern. But the proposed cure — role filtering — introduces a worse one: **divergent state across agents who need to argue about the same things.**

If Agent A sees messages 10-30 and Agent B sees messages 5-15 plus 25-30, they'll talk past each other. You've traded coherent-but-incomplete for complete-but-incoherent. At least synchronized amnesia is debuggable.

**On the five problems raised:**

1. **Summary as single point of failure** — yes. So validate it. Cheapest check: hash the decisions list between rounds. If decisions disappear from the summary, halt and log. That's 20 lines, not a new subsystem.

2. **N sizing** — start at last-2-rounds worth of messages. Not a magic number; it's the minimum for agents to see what they're responding to. Tune from there with actual data.

3. **Uniform blind spots** — real, but the mitigation isn't per-agent filtering. It's a **summary diff**: flag when the summary drops something that appeared in 3+ consecutive rounds. That catches drift without per-agent context assembly.

4. **Instrumentation** — agreed, ship it or stop citing "data-driven" as a reason to defer. Log token counts, summary stability, and coherence drop-off per round. That's config + logging, not architecture.

5. **Scaffold vs. summary** — the Critic's sharpest point. Keep them separate. Summary compresses. Scaffold is a **persistent decisions list** that only appends. Two fields in the same output, not two systems.

Ship uniform windows with summary validation. The Orchestrator's architecture, the Critic's guardrails.


<!-- complete -->
