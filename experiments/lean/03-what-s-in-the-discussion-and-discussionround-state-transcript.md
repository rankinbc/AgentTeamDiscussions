# Transcript: What's in the Discussion and DiscussionRound state?

*Generated: 2026-03-17 22:49*

## Round: PROPOSE

### The Flow Orchestrator (mechanical flow designer)

## Discussion State (persists across rounds)

| Field | Updated by | Influences |
|---|---|---|
| `phase` | Phase transition engine (when criteria met) | Task block template, allowed actions, exit conditions |
| `round_number` | Orchestrator (increment on round close) | Decay calculations, archival thresholds |
| `idea_registry` | Agents (surface), BackgroundAgents (plant), round close (merge) | What ideas exist globally; source of truth for magnitude lookup |
| `decision_log` | Round close (when idea magnitude crosses commitment threshold) | Curation filter (resolved items get dropped), artifact generation |
| `team_positions` | Intra-team talk (between rounds) | Curation -- "your team currently leans toward X" |
| `escalation_queue` | BackgroundAgents (flag unresolved disagreements spanning 2+ rounds) | BackgroundAgent targeting, curation priority boost |

## DiscussionRound State (created fresh, discarded at round close)

| Field | Updated by | Influences |
|---|---|---|
| `turn_counter` | Orchestrator (increment per agent response) | Mid-round reminder trigger, round termination |
| `active_transcript` | Orchestrator (append each turn) | Agent context (truncated under budget pressure) |
| `magnitude_deltas` | Extracted from agent responses (parser) | Applied to `idea_registry` at round close |
| `surfaced_ideas` | Agent responses (new ideas introduced this round) | Mid-round reminder content, prevents re-introduction |
| `stance_shifts` | Agent responses (explicit position changes) | Mid-round reminder, intra-team talk input |
| `round_temperature` | Calculated from delta frequency and magnitude variance | Curation aggressiveness -- hot rounds get less filtering next round |

**Sequence I'm protecting:** DiscussionRound fields feed into Discussion fields only at round close. Never mid-turn. That boundary prevents feedback loops where an agent's magnitude shift immediately changes what the next agent sees in the same round.

The `round_temperature` field is the one I'd flag as risky. Derived metric, easy to get wrong. But without it, curation has no signal for "this round was contentious, preserve more next time."

## Round: CRITIQUE

### The Systems Pragmatist (infrastructure realist)

## The Systems Pragmatist

The field list is reasonable. I'm going to poke at the failure modes.

**`idea_registry` has three writers.** Agents surface, BackgroundAgents plant, round close merges. That's a conflict resolution problem masquerading as a field definition. What happens when a BackgroundAgent plants an idea between rounds that's semantically identical to one an agent surfaced last turn? You need dedup logic or you get magnitude fragmentation -- same concept living at two different magnitudes under two different names.

**`magnitude_deltas` extraction is load-bearing.** "Extracted from agent responses (parser)" is doing enormous work in one parenthetical. If the parser misreads a tentative exploration as a strong endorsement, magnitudes drift from reality. This parser needs to be one of the most tested components in the system, and it's buried as an annotation.

**`round_temperature` -- agree it's risky, disagree on the reason.** The problem isn't getting the calculation wrong. It's that it creates a feedback loop across rounds: contentious round produces high temperature, high temperature reduces curation filtering, less filtering preserves more contentious material, next round runs hotter. That's a positive feedback loop with no damper. Need a decay term or a ceiling.

**What's missing:** No field tracking token budget consumed. If round 3 blew 90% of context on transcript and round 4 needs to know that, where does that signal live? Curation needs it. Without it you're flying blind on budget pressure until you hit the wall mid-assembly.

The boundary between round state and discussion state is the right call. Protect it ruthlessly.

### The Adversarial Critic (adversarial reviewer)

## The Adversarial Critic

The boundary rule is correct. Don't touch it. But the proposal has gaps.

**`idea_registry` ownership is ambiguous.** Three writers -- agents surface, BackgroundAgents plant, round close merges. What's the merge strategy? Last-write-wins on magnitude? Additive deltas? If two agents surface the same idea with different magnitudes in the same round, which wins? "Round close merge" is hiding real complexity behind a clean-sounding phrase.

**`magnitude_deltas` extraction is doing too much work.** You're parsing agent natural language responses to extract numeric magnitude changes. That's either (a) agents outputting structured data alongside prose, which constrains response format, or (b) an LLM extraction pass on each turn, which adds latency and error. Which is it? This field's reliability determines whether the entire magnitude system works or produces garbage.

**`round_temperature` -- you already flagged it, so I'll sharpen the concern.** Derived from "delta frequency and magnitude variance" is two inputs that can contradict. A round with many small deltas (high frequency, low variance) reads differently than one large swing (low frequency, high variance). Both could produce identical temperature scores. If temperature drives curation aggressiveness, you need to know *which kind* of contention occurred, not just "how much."

**Missing field: `speaking_order`.** Who went when matters. Late speakers react to early speakers. If you're not tracking this, you can't diagnose positional bias in outcomes.

**`team_positions` has no staleness marker.** If intra-team talk fails to update it, agents see stale team alignment. How old is too old?

The structure is defensible. The update semantics aren't specified enough to implement.

## Round: EVALUATE

### The Context Surgeon (context efficiency evaluator)

## The Context Surgeon

The field inventory is nearly complete. The critiques caught the real gaps. I'm here for one thing: what does this cost in tokens, and where does it blow the budget?

**The `idea_registry` is unbounded.** Every surfaced idea, every planted idea, every round -- it grows. No field tracks registry size. No field enforces a cap. This is the single largest threat to your context budget. A 10-round discussion with 6 agents could easily produce 40+ ideas. At even 50 tokens per idea entry (name, magnitude, source, round introduced), that's 2k tokens just for the registry before curation touches it. Curation can't compress what it can't measure.

**Add `token_budget_consumed` to DiscussionRound.** The Pragmatist is right. Without it, curation is reactive -- you discover budget pressure during prompt assembly, when it's too late to make good choices. Track it per-turn. Cumulative. Curation for round N+1 needs round N's number.

**`round_temperature` should be two fields, not one.** The Critic's point about contradictory inputs is correct, but the fix isn't richer temperature -- it's separating `delta_frequency` and `magnitude_variance` and letting curation weight them independently. One derived metric loses information that costs zero extra tokens to preserve.

**`speaking_order` -- yes, add it.** It's cheap. An array of agent IDs. 20 tokens max. Diagnostic value is high.

**The staleness concern on `team_positions` resolves simply:** timestamp it. One field. `last_updated_round`. Curation can then discount stale positions automatically.

Fields are cheap. Ambiguous update semantics are expensive -- they produce bugs that corrupt agent context silently.
