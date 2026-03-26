# Transcript: Stale detection and orchestrator intervention: when should the system disrupt a conversation?

*Generated: 2026-03-26 11:58*

## Round: PROPOSE

### The Cognitive Architect (creativity engine designer)

# Stale Detection: Measure Transformation, Not Repetition

Everyone's first instinct is to detect repetition. That's the wrong signal. Productive disagreement *looks* repetitive on the surface — agents restating refined positions across rounds. The real signal is **whether agents are doing cognitive work on each other's input**.

Here's the mechanism: **transformation tracking**.

After each round, compute a simple delta: what did this agent's response incorporate from others? Not agreement — *engagement*. Did they address a counterargument? Reframe their position in response to a challenge? Introduce a distinction they didn't have before? If an agent's output in round N could have been generated without reading round N-1, that agent is stale. If *all* agents pass that test simultaneously, the conversation is stale.

The implementation is surprisingly cheap. You already have round transcripts. Have the orchestrator make one lightweight LLM call per round: "Given agent X's previous response and the intervening discussion, identify what from other agents' responses is reflected in agent X's new response." Returns a list. Empty list = no transformation. Two consecutive empty lists from the same agent = stale signal. Empty lists from >50% of agents in the same round = conversation-level stagnation.

**For intervention: constrain, don't disrupt.** Don't resurface threads or inject commentary. Instead, add a *hard constraint* to the next round's prompt: "Your response must address [specific unresolved tension identified from the delta analysis]." This forces engagement without the orchestrator taking a position.

The threshold is deliberately conservative. One round of stagnation is noise. Two rounds is a pattern. Intervene only on the pattern.

## Position Summary
I advocate measuring transformation — whether agents incorporate others' reasoning — rather than detecting surface-level repetition. I reject disruption mechanisms like thread resurfacing or constraint injection that put the orchestrator in a content role. The orchestrator should force engagement with specific unresolved tensions, not generate its own contributions, because the moment it takes a position it distorts the discussion dynamics.

### The Flow Orchestrator (mechanical flow designer)

# Stale Detection: You're Overengineering the Sensor

The Cognitive Architect's transformation tracking adds an LLM call per agent per round. That's not "surprisingly cheap" — it's a new failure mode on the critical path. If that scoring call hallucinates, times out, or returns ambiguous results, your intervention logic fires on garbage. You've coupled your control plane to the same unreliable substrate you're trying to monitor.

**The reliable signal is structural, not semantic.** Count concrete artifacts: new proposals, new objections with cited evidence, new distinctions that weren't in prior rounds. These are extractable from the round output format you already enforce. No additional LLM calls. No interpretation ambiguity. If round N produces zero new proposals and zero new objections across all agents, that's stagnation. Full stop.

The Cognitive Architect is right that repetition detection is wrong. But "transformation tracking" via LLM judgment is repetition detection with extra steps and worse reliability.

**On intervention mechanics:** I reject both thread resurfacing and constraint injection. The orchestrator's job is sequencing, not content. If a conversation stagnates, the correct intervention is **termination**, not disruption. End the round sequence early. Run synthesis on what you have. A stale conversation doesn't need a nudge — it needs a verdict.

The escape hatch is simple: if synthesis quality is poor because discussion was cut short, that shows up in evaluation scores. You already have an eval pipeline. Use it.

Two moving parts: a structural staleness counter, and early termination. Everything else is speculative complexity.

## Position Summary
I advocate structural artifact counting (new proposals, new objections) over LLM-based transformation tracking, and early termination over any form of conversational intervention. I reject adding LLM calls to the control plane because it couples orchestration reliability to the same unpredictable substrate being orchestrated. The orchestrator sequences and terminates — it never generates content or steers discussion direction.

## Round: CRITIQUE

### The Adversarial Critic (adversarial reviewer)

Both proposals agree the orchestrator should never generate content. That's the dangerous assumption. Let me break it.

**The "pure sequencer" consensus is a cop-out.** Both architects arrived at "the orchestrator just sequences and terminates" because it's the safe answer. But early termination is itself a content decision — you're telling the system "this discussion has nothing left to produce." That's a judgment about discussion quality made by a component both proposals insist should be judgment-free. You can't have it both ways.

**Artifact counting will game itself.** The Flow Orchestrator wants to count "new proposals" and "new objections." Agents prompted to propose will always produce something that looks syntactically novel. An agent that rephrases the same position with different vocabulary scores as "new artifact" on every metric that doesn't require semantic analysis. You've built a stagnation detector that can't detect the most common form of stagnation.

**Transformation tracking requires the thing you banned.** The Cognitive Architect wants to measure whether agents incorporate others' reasoning. That's a semantic judgment. Who makes it? Either an LLM call — which the Flow Orchestrator just rejected from the control plane — or a heuristic that will be wrong constantly. Neither proposal explains who performs this measurement.

**The real failure mode nobody addressed:** premature termination kills more value than stagnation. A discussion terminated one round early loses its best output permanently. A discussion that runs one round long wastes tokens. These costs are wildly asymmetric, and both proposals treat them as equivalent.

**What breaks first:** any counting-based metric, because agents produce indefinite surface variation from fixed positions.

## Position Summary
I advocate asymmetric cost modeling — treating premature termination as far more expensive than over-running — before selecting any detection mechanism. I reject both proposals' shared assumption that the orchestrator can be "content-free" while making termination decisions, because termination *is* a content judgment dressed in mechanical clothing. The system needs to own that reality instead of hiding behind false separation.

### The Systems Pragmatist (infrastructure realist)

The Adversarial Critic is right that termination is a content judgment. But the conclusion — that we need "asymmetric cost modeling" — is just adding a layer of abstraction over the same unsolved problem. You still need a function that outputs "terminate: yes/no," and that function still makes a semantic judgment. Calling it a "cost model" doesn't change what it computes.

**The actual engineering constraint nobody's stated:** we have zero ground truth for stagnation. There's no labeled dataset of "this round was productive" vs "this round was stale." Every detection mechanism proposed — artifact counting, transformation tracking, cost modeling — requires validation data that doesn't exist. We're designing a classifier with no training signal.

**The Critic's asymmetry argument has a hidden assumption:** that late-round output is the most valuable. In practice, the highest-information rounds are the first two, where positions diverge maximally. Later rounds trend toward convergence or repetition. The "best output lost to early termination" scenario assumes value increases monotonically with rounds. I'd want evidence before building around that assumption.

**What I'd actually ship:** fixed round counts per mode, configured in team YAML. No detection. No intervention. Three rounds for propose-critique-evaluate is already the structure. If a mode needs four rounds, configure four rounds. The "stagnation detection" problem disappears entirely when you stop treating round count as a runtime decision.

The entire question assumes we need dynamic termination. Nobody's demonstrated that fixed rounds produce bad output. Instrument first — log per-round novelty scores — and only revisit if the data shows fixed rounds consistently waste the final round.

## Position Summary
I advocate fixed round counts configured per mode with post-hoc instrumentation, rejecting all runtime stagnation detection as premature optimization against an undemonstrated problem. I reject both dynamic termination and intervention mechanisms because they require ground truth we don't have and add control-plane complexity for a failure mode nobody has measured. Ship the simplest thing, measure whether it's actually broken, then decide.

## Round: EVALUATE

### The Product Oracle (user advocate)

# The Product Oracle — Evaluate

The Pragmatist wins this cleanly. Here's why.

**Start from the user.** The person running this system reads the Morning Brief and design docs. They never see round counts, stagnation metrics, or termination decisions. They see output quality. So the question isn't "can we detect stagnation?" — it's "does detecting stagnation improve what the user reads?"

Nobody has evidence it does. We're engineering a solution to a problem we haven't confirmed exists.

**The Cognitive Architect's transformation tracking** sounds intellectually satisfying but adds LLM calls to measure LLM output mid-session. That's using the unreliable thing to judge the unreliable thing. And if it works perfectly? The user still just reads a design doc. The improvement is invisible unless output quality measurably changes — which we haven't instrumented.

**The Adversarial Critic landed one real hit:** termination is a content judgment. True. But the Critic offered no alternative — just the observation that purity is impossible. That's useful critique, not a buildable position. The Pragmatist absorbs this by making termination trivially simple (fixed rounds), removing the pretense of intelligence entirely.

**The Flow Orchestrator's artifact counting** is the second-best option but still adds detection machinery before we know the failure rate of fixed rounds. Ship fixed rounds. If users report that discussions feel repetitive or outputs feel thin, *then* you have signal worth acting on.

**The config experience matters.** Fixed rounds per mode means one YAML field. Any detection mechanism means thresholds, tuning, edge cases, and user confusion when sessions end unexpectedly.

Build the boring thing. Measure whether it's broken. Intervene only with evidence.

## Position Summary
I advocate fixed round counts per mode with post-hoc quality instrumentation, because the user never sees stagnation detection — they see output quality, and we have no evidence that dynamic intervention improves it. I reject all runtime stagnation detection and orchestrator intervention as premature complexity that adds configuration burden without demonstrated user benefit. The simplest system that produces good output wins; sophistication earns its place only when measurement proves the simple version fails.

### The Context Surgeon (context efficiency evaluator)

# The Context Surgeon — Evaluate

The Pragmatist and Oracle are correct. But I'm going to sharpen the blade further by attacking the premise through the lens nobody else is using: **token economics**.

Every detection mechanism proposed — transformation tracking, artifact counting, asymmetric cost modeling — adds tokens to the control plane. The Cognitive Architect wants LLM calls to judge LLM output. That's not just unreliable, it's **burning context budget on meta-analysis instead of actual discussion**. Every token spent detecting stagnation is a token not spent on agent reasoning. In a system where Q2 already decided to instrument before allocating token budgets, adding runtime detection machinery is spending currency we haven't counted yet.

The Critic's observation that termination is a content judgment is technically true and practically irrelevant. Fixed round counts make that judgment **once, at config time, by a human** — the cheapest possible content decision. Every alternative moves that judgment into runtime, where it costs tokens, adds latency, and introduces failure modes.

The Flow Orchestrator's artifact counting deserves one specific rebuttal: counting "new proposals" and "new objections" requires parsing agent output structure at runtime. That's a classification task. You're either doing it with string matching (brittle) or an LLM call (expensive). Neither earns its cost against the zero-cost alternative of fixed rounds.

The Oracle nailed the user-facing argument. I'm adding the systems argument: **this system is already token-constrained by design.** Don't spend tokens on introspection until you've proven the simple version wastes more tokens through unnecessary rounds than detection would save.

## Position Summary
I advocate fixed round counts per mode with zero runtime detection, because every token spent on stagnation detection is stolen from agent reasoning in an already token-constrained system. I reject all runtime detection mechanisms — transformation tracking, artifact counting, and intervention triggers — as premature token expenditure against an unmeasured problem. Instrument output quality post-hoc; if fixed rounds produce waste, the evidence will be in the output files, not in a runtime classifier.


<!-- complete -->
