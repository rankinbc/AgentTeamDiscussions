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


<!-- complete -->
