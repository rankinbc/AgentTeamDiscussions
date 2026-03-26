# What's the difference between a "round" and a "turn"?

*Generated: 2026-03-17 21:37 | Question 2 | 176s*

The spec is ready to write -- just needs your file write permission. Here's what I synthesized:

**Spec: Round vs. Turn Boundaries** -- distilled from all six panel voices into one authoritative document:

**The clean definitions:**
- **Turn** = one agent, one response, committed to transcript. Between turns: append only, nothing expensive.
- **Round** = sequence of turns ending at a termination condition. Between rounds: the full 7-step pipeline runs (Save, BackgroundAgents, IntraTeam, ThinkingRoutines, Filter, Curate, Assemble).

**Key settled points:**
- Mid-round context is append-only; between-round context is rebuilt from scratch
- Save state runs first (clean snapshot before mutation)
- V1 termination: hard turn cap only (per-phase, configurable) with minimum threshold override
- Smart termination (stagnation, consensus) deferred -- requires mid-round LLM calls that contradict "turns are cheap"
- Round-open Tasks are generative; mid-round Tasks are reactive
- Round 1 is cheapest by design (no prior state to process)

**Seven open items flagged:** mid-round context bloat budget, BackgroundAgent vs. intra-team ordering justification, shared agenda assumption, per-phase turn cap defaults, intra-team talk budget, BackgroundAgent early termination, and round success metrics.

Please approve the file write to save it to `output/spec_round_vs_turn_boundaries.md`.