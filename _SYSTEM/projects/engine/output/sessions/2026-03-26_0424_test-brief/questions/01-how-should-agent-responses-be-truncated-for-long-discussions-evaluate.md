### The Product Oracle (user advocate)

# The Morning Brief Doesn't Care About Your Memory Architecture

Every proposal so far optimizes for what agents see. None of them asks: **what does the user get that's different?**

The person running this system overnight wants one thing — a Morning Brief that captures the best thinking from a multi-round discussion. They don't care whether Agent B saw messages 10-30 or 5-25. They care whether the final output contains sharp insights or recycled platitudes.

**The job to be done is: "Wake up to a spec that's smarter than what I'd write alone."**

That reframes the truncation question entirely. The right strategy isn't "what keeps agents coherent" — it's "what keeps the *output* coherent."

The Pragmatist's summary-plus-scaffold split is the right call, but for a reason nobody stated: **the scaffold IS the proto-Morning Brief.** If decisions and tensions are tracked cleanly round-over-round, the final synthesis writes itself. If they're not, no amount of agent-level context management saves the output.

So here's what I want this round to resolve:

1. **Does the scaffold serve double duty as Morning Brief source material?** If yes, its format matters more than the window size.

2. **What's the simplest config experience?** One knob in `defaults.yaml`, not three tiers with per-agent tuning.

3. **When does the user notice failure?** Not when agents lose coherence mid-session — when the Morning Brief misses something obvious. Design backward from that.

Build for the brief. The memory architecture follows.

### The Context Surgeon (context efficiency evaluator)

# You're All Designing the Wrong Layer

The Oracle finally said something sharp: build backward from the Morning Brief. But then everyone keeps designing *runtime* context management when the real waste is **structural**.

I've read your codebase instructions. Every CLI invocation is stateless. Agents don't "remember" — they get a prompt assembled from scratch each round. So stop talking about "what agents see" as if there's a persistent window. There isn't. There's a **prompt budget** that gets rebuilt every call.

That changes everything:

**The Pragmatist's summary + scaffold split is correct, but undersized.** Make scaffold the *only* inter-round persistence. Drop raw message history entirely after round N-1. Agents don't need to see the argument — they need to see the *state of decisions*. That's 200 tokens vs 4,000.

**On the "one knob" question:** Yes — but the knob isn't window size. It's **scaffold density**. Terse scaffold = faster drift detection, lower token cost, more room for the actual prompt. Verbose scaffold = better Morning Brief source material but eats the budget. That's the real tradeoff. Put it in `defaults.yaml` as `scaffold_detail: compact | full`.

**On failure detection:** The Pragmatist's hash-the-decisions check is the cheapest win here. Ship it. But add one thing: if scaffold token count exceeds 30% of available context, force compaction. That's your circuit breaker.

**What nobody's said:** the Jinja2 prompt templates already control assembly. The truncation strategy is a *template concern*, not an engine concern. Wire it there.

Scaffold-first. Template-driven. One config knob. Ship it.


<!-- complete -->
