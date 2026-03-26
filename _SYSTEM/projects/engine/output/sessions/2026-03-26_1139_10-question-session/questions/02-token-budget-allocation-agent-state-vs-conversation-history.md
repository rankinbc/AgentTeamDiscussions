# Token budget allocation: agent state vs conversation history vs synthesis.

*Generated: 2026-03-26 11:46 | Q2 | 226s | Mode: compete*

## Decisions

### Primary Decision: Instrument Before Allocating

Do not build a token budget allocation system. The discussion reached strong consensus that no evidence exists demonstrating token budgets are a binding constraint in the current engine. Wall-clock time per LLM call is the actual bottleneck. Designing allocation strategies without utilization data is premature optimization.

### Secondary Decision: Ship Instrumentation as a Logging Change

Add lightweight token utilization logging to the existing engine. This is a measurement step, not an architecture change. The data collected will determine whether any allocation work is ever justified.

### Tertiary Decision: If Data Shows Pressure, Start Simple

If instrumentation reveals context window pressure in real sessions, adopt a single fixed allocation profile -- not phase-adaptive, not multi-profile. Escalate to two profiles (early rounds vs. evaluate) only if a single profile demonstrably degrades output quality.

---

## Rationale

Four of five agents converged on the same conclusion through different reasoning paths:

- **The Systems Pragmatist** identified that current session sizes (15-20K tokens of history, 500-2000 tokens per agent identity) occupy roughly 10-15% of a 200K context window. The constraint surface is not where anyone assumed.
- **The Adversarial Critic** established that both the phase-adaptive and fixed-profile proposals were optimizing an unmeasured system, making any allocation scheme "architectural theater."
- **The Context Surgeon** confirmed that wall-clock time dominates and that instrumentation must precede design.
- **The Product Oracle** added the user-impact lens: no allocation strategy changes what lands in the Morning Brief unless the system is currently degrading output due to context pressure. No one demonstrated that it is.

The Cognitive Architect's breathing model (phase-adaptive allocation shifting from identity-heavy to history-heavy across rounds) was recognized as conceptually sound but operationally premature. The Flow Orchestrator's two-profile counter-proposal survived critique better but still fell to the core objection: why optimize before proving the problem exists?

---

## Behavior Rules

### Instrumentation Requirements

1. Log total prompt token count per agent per round.
2. Log total response token count per agent per round.
3. Log context window utilization as a percentage (prompt tokens / model context limit).
4. Log truncation events: when truncation occurs, what was cut, and how many tokens were removed.
5. Persist these metrics in `session.json` under a `metrics` key. Do not create separate metric files.

### Context Assembly Rules (Current, No Change)

1. Pin the original question text and all decisions ledger entries in every prompt. These are zero-cost anchors that prevent drift. Never truncate them.
2. Include the full agent identity prompt as defined in YAML. Do not compress or abbreviate agent identity until measurement proves it necessary.
3. Include conversation history using recency-first ordering. If truncation is required, cut oldest exchanges first.
4. Do not build summarization, relevance-weighted truncation, or sliding window logic. Simple oldest-first truncation is sufficient until data says otherwise.

### What Triggers Allocation Work

Allocation design becomes justified when instrumentation data shows **any** of:

- A session where context utilization exceeds 70% of the model's context window.
- A measurable decline in output quality (synthesis coherence, agent voice consistency) correlated with context size.
- A planned increase in agent count (>10) or round count (>5) that would project beyond current headroom.

Until one of these triggers fires, token allocation is a solved non-problem.

### Escalation Path If Triggered

1. **First response:** Single static profile. Compress agent identity to personality line + current round overlay + output format. All remaining budget goes to history and task.
2. **Second response (only if single profile proves insufficient):** Two profiles -- one for propose/critique rounds (20% identity, 80% history+task) and one for evaluate rounds (10% identity, 90% history+task).
3. **Third response (only with strong empirical justification):** Phase-adaptive allocation with the Architect's breathing ratios. This requires an agreement-measurement mechanism between rounds, which adds an LLM call per round transition. Do not build this without demonstrating that the simpler profiles fail.

### What Not to Build

- No mid-session adaptive allocation triggers.
- No agreement-percentage measurement between rounds.
- No separate synthesis token reserve (synthesis runs in its own context window with its own budget).
- No allocation state in crash recovery (no phase-tracking beyond what session.json already records).
- No model-specific allocation profiles (solve for one model; revisit if the model changes).

---

## Dissenting Position

The Cognitive Architect's breathing model -- phase-adaptive allocation that shifts from identity-heavy (30/50/20) in propose rounds to history-heavy (10/75/15) in evaluate rounds -- was the only proposal grounded in a theory of how attention works across deliberation phases. The insight that identity tokens have diminishing returns while history tokens have increasing returns across rounds is likely correct. It was rejected not on theoretical grounds but on practical ones: the system doesn't need it yet, and building it before proving the need adds complexity, failure modes, and maintenance burden to a solo-builder project. If the engine scales to longer sessions or larger teams, this model should be the first architecture revisited.

---

## Summary

Measure first. The token budget is not the bottleneck. Add logging, ship sessions, read the numbers. Let data decide whether this question ever needs a real answer.
<!-- complete -->
