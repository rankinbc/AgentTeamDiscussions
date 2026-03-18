# How does a round begin after a reset?

*Generated: 2026-03-17 23:18 | Question 1 | 109s | Mode: compete*

## Decisions

### D1: Round-Start Is a Cold Boot with Warm Memory

A round-start is not a continuation of the previous conversation. It is a fresh prompt assembly where the agent re-enters the discussion with no prior conversation context, only its persisted state and a curated briefing. The agent must re-earn its convictions each round based on its current state.

### D2: Three-Step Assembly Sequence

The orchestrator executes exactly three steps to begin a round:

1. **Load agent save file.** File read, no LLM call. Validate required fields (ideas, stances, decisions, summary) before proceeding. Fail loudly on corruption or missing fields -- no silent defaults.

2. **Curate situation context.** Deterministic filter runs first (drop resolved decisions, drop ideas below persona-dependent archival threshold, drop stale low-magnitude topics). Then one LLM curator call compresses the filtered remainder into the situation block. Hard-capped at 15k tokens -- truncate if exceeded, never negotiate.

3. **Assemble prompt and issue task.** Concatenate four blocks in fixed order and deliver to the agent.

### D3: Prompt Block Order and Budget

The round-start prompt assembles four blocks in this exact order:

| Order | Block | Budget | Source |
|-------|-------|--------|--------|
| 1 | Identity | ~2k tokens | Static persona file, unchanged between rounds |
| 2 | Curated Situation | 8-15k tokens | LLM curator output from Step 2 |
| 3 | Save File | ~1-2k tokens | Raw, uncompressed agent state |
| 4 | Task Directive | ~500 tokens | Template with phase and discussion question |

**Total context load: ~12-19k tokens.** Remaining budget (80k+) is reserved for agent thinking and response.

**Save file placement rationale:** It appears after the situation brief because it is the smallest block and contains the action-relevant data (magnitudes, stances). Recency bias in LLMs means the agent weighs later tokens more heavily. Magnitudes should be fresh in context when the agent decides what to lead with.

### D4: Round-Start vs. Mid-Round Prompt Structure

| Dimension | Round-Start | Mid-Round |
|-----------|-------------|-----------|
| Identity block | Present (static) | Present (static) |
| Situation block | Curated briefing (~8-15k) | Recent conversation history (~3-8k) |
| Save file | Present, raw | Absent |
| Task block | "Review your position, consult your idea magnitudes, and raise what needs resolution most" | "Agent X said [message]. Respond." |
| Agent posture | Proactive -- agent chooses the frame | Reactive -- agent responds to others |
| Token cost | ~12-19k loaded | ~6-12k loaded |

**The save file is a round-boundary artifact only.** It never appears in mid-round prompts. Leaking it mid-round wastes tokens and invites the agent to recalculate positions instead of committing to them.

### D5: Task Prompt Must Reference Magnitude

The round-start task directive must explicitly instruct the agent to consult its idea magnitudes. Without this, agents will prioritize by whatever the LLM finds narratively interesting, which correlates weakly with magnitude scores. The task template should frame a tension rather than simply asking "what do you want to raise":

> "The discussion is resuming. Consult your idea magnitudes. Given where your team landed and where the other team pushed back, what needs resolution most? Open with it."

This ensures the magnitude system actually drives behavior rather than serving as ignored bookkeeping.

### D6: Speaking Order Is Magnitude-Weighted Random

When multiple agents want to open on a topic, the orchestrator selects speaking order using magnitude-weighted randomness. The agent with the highest-conviction unresolved idea speaks first most of the time, but not deterministically. Predictable ordering kills emergence.

Implementation: weight each agent's selection probability by the magnitude of their highest-priority idea. Randomize within those weights.

### D7: Curator Call Specification

The curator call is the most consequential and most fragile step in the pipeline. It requires explicit specification:

**Curator inputs:**
- Agent's save file (ideas, stances, magnitudes, summary)
- Deterministically filtered history (resolved decisions and sub-threshold ideas already removed)
- Current phase and round number

**Curator job:**
- Compress filtered history into a personalized briefing for this specific agent
- Surface connections the agent may not have noticed (teammate stance shifts, cross-team implications)
- Occasionally introduce unexpected emphasis -- this is the "valuable randomness" that prevents scripted-feeling rounds

**Curator constraints:**
- Hard output ceiling: 15k tokens, enforced by truncation
- Must not fabricate events that did not occur in the filtered history
- Must not editorialize on what the agent should do -- only report what happened

**Curator prompt must be explicitly authored and tested.** A poorly tuned curator prompt degrades every agent's round-start quality. This is not a generic summarization task.

### D8: Curator Fallback on Failure

If the curator call fails (timeout, error, garbage output), the orchestrator serves the deterministically filtered content raw in place of the curated situation block. This produces a degraded but functional round-start -- the agent gets uncompressed history instead of a tailored briefing. The run continues. Infrastructure failures never kill a session.

### D9: Save File Delta Logging

The orchestrator must log the save file delta between rounds for each agent. This is the audit trail that makes agent evolution visible to session reviewers. When an agent shifts focus between rounds, the delta explains why (magnitude changes from intra-team talk, BackgroundAgent interventions, thinking routine outcomes).

Log format: previous save file and current save file, stored per-agent in the session's internal directory. Diff computation is a review-time concern, not a runtime one.

### D10: Save File Validation Contract

The save file must contain exactly these fields to pass validation:

- **Ideas**: list of ideas with numeric magnitudes
- **Stances**: list of stances with numeric magnitudes
- **Decisions**: list of committed decisions (may be empty)
- **Summary**: 3-5 sentence personalized narrative of last round

If any required field is missing or malformed, the orchestrator halts that agent's round-start and reports the error. No partial boots, no inferred defaults.