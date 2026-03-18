# What's in the Discussion and DiscussionRound state?

*Generated: 2026-03-17 22:49 | Question 3 | 352s | Mode: lean*

It looks like file write permissions are pending. Here's a summary of the synthesized spec while we wait:

**The spec consolidates all four reviewers' input into a single document covering:**

**Discussion State (6 fields):**
- `phase`, `round_number`, `idea_registry`, `decision_log`, `team_positions`, `escalation_queue`
- Key addition: **merge rules** for `idea_registry` resolving the three-writer conflict (dedup on semantics, BackgroundAgents merge first, deltas are additive, 50-idea cap)
- Key addition: `last_updated_round` staleness marker on `team_positions`

**DiscussionRound State (9 fields -- 3 new from critique):**
- Original 6: `turn_counter`, `active_transcript`, `magnitude_deltas`, `surfaced_ideas`, `stance_shifts`, plus the contention signals
- **`round_temperature` split into two fields:** `delta_frequency` and `magnitude_variance` (Critic's point -- different contention types need different signals)
- **`speaking_order` added** (Critic -- cheap, high diagnostic value)
- **`token_budget_consumed` added** (Pragmatist -- curation can't plan without knowing last round's consumption)

**Key design decisions:**
- Magnitude delta extraction uses **structured output format constraint**, not LLM parsing -- parse failures log a flag and record no deltas rather than guess
- **Contention runaway protection:** 30% decay on contention signals between rounds, 80% hard ceiling on curation permissiveness, human review flag after 3+ consecutive elevated rounds
- Complete **round lifecycle sequence** documented: round close, BackgroundAgent phase, intra-team talk, deterministic decay, context curation, round open

**Four open questions** flagged for implementation: dedup threshold tuning, delta block schema, persona-to-threshold mapping, and staleness cutoff for team positions.

Would you like to approve the file write, or should I adjust anything in the spec first?