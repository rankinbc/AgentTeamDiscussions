# How does a round begin after a reset?

*Generated: 2026-03-17 23:26 | Question 1 | 138s | Mode: angles*

## Decisions

### D1: Round-Start Assembly Serves Conviction, Not Comprehension

The orchestrator assembles the round-start prompt backward from urgency. The goal is not to brief the agent on what happened -- it is to make the agent care enough about something unfinished to speak first. Every component of the assembled prompt is evaluated against this criterion: does it sharpen conviction or dilute it?

### D2: The Round Boundary Carries All Complexity

Steps 1-6 of the pipeline run exclusively at round boundaries. Mid-round turns are reactive conversation with no curation, no state mutation, no BackgroundAgent interference. Error budgets, performance budgets, and design complexity concentrate at the boundary. Mid-round is just "here's what was said, respond."

### D3: State Mutations Use Snapshot-Diff Architecture

Each pipeline step (BackgroundAgents, intra-team talk, thinking routines) operates on a snapshot of agent state and produces a diff. Diffs apply sequentially. Any step can be replayed, reordered, or dropped without corrupting the base state. This eliminates order-dependent bugs and enables auditability.

### D4: Intra-Team Talk Runs Before BackgroundAgents

Organic team dynamics play out first. BackgroundAgent ("angel") interventions apply after, so planted ideas and magnitude shifts reflect divine intervention on top of natural team consensus rather than getting laundered through team discussion before the agent ever sees them directly. Planted ideas surface in the agent's own voice at round-start rather than being pre-socialized.

### D5: Speaking Order Uses Magnitude-Weighted Random Selection

When multiple agents emerge from the pipeline ready to champion items, the opening speaker is selected by weighted random draw. Weight equals the agent's highest unresolved item magnitude. High-conviction agents open more often without making the order deterministic. This prevents rounds from feeling like sequential monologues and preserves emergent debate dynamics.

### D6: The Subjective Recap Collapses to a Single-Sentence Anchor

The agent save file stores a one-sentence narrative anchor, not a 3-5 sentence recap. The LLM curator's agent-specific Situation block replaces the longer recap. Paying for both a self-narrative and a curated summary is redundant. The anchor sentence provides identity continuity; the curator provides situational awareness.

### D7: Group Direction Is a Precomputed Magnitude Vector

"Group apparent direction" is not computed at prompt-assembly time through expensive aggregation. It is a precomputed vector: for each active topic, the mean magnitude across all agents' stances. This vector updates once per round boundary (after Step 4, before Step 5) and is available to the curator and the tension formula as a cheap lookup.

---

## Round-Start Pipeline

The orchestrator executes the following steps sequentially before any agent receives a round-start prompt. Every step logs its output. If any step fails, the round does not start.

### Step 1: Load Agent Save Files

Read each agent's persisted state:
- Ideas with magnitudes
- Stances with magnitudes
- Committed decisions
- One-sentence narrative anchor

Corrupt or missing save files halt the pipeline with an explicit error.

### Step 2: Run Intra-Team Talk

Teammates exchange views. Magnitude shifts are logged as deltas with before/after values. Output is a diff against the Step 1 snapshot. Good ideas gain magnitude through team reinforcement; weak ideas decay.

### Step 3: Run BackgroundAgents

BackgroundAgents read conversation history and current agent state (post-intra-team). They produce discrete mutations: magnitude bumps, stance shifts, planted ideas. Each mutation is logged with before/after values and the BackgroundAgent's rationale. Output is a diff that applies on top of Step 2 results.

### Step 4: Run Thinking Routines

Each agent receives up to three separate LLM calls (not part of the discussion context):

- **Reflect**: Review own ideas and stances against what happened last round. Adjust magnitudes.
- **Research**: Spawn a focused research call on the agent's highest-uncertainty item. Results become new ideas or modify existing magnitudes.
- **Strategize**: Consider what to push for next round given team goals and current state.

Output feeds back into the save file as a final diff.

### Step 5: Compute Group Direction Vector

For each active topic, compute mean magnitude across all agents' stances. Store as a flat lookup table. This is cheap arithmetic, not an LLM call.

### Step 6: Curate Situation Block

Two-pass curation:

**Deterministic pass**: Drop resolved decisions. Drop ideas below the agent's persona-dependent archival threshold. Drop topics where the agent has no stance and magnitude is below a global floor.

**LLM curator pass**: Summarize remaining state for this specific agent. The curator emphasizes what should feel unfinished given the agent's persona, high-magnitude items, and gaps between agent stance and group direction vector. The curator sharpens narrative tension; it does not produce neutral summaries. Cache the output.

### Step 7: Compute Tension Item

For each agent, identify the idea or stance with the largest gap between the agent's magnitude and the group direction vector's value for that topic. This is the agent's highest-tension item.

If the agent's highest-magnitude items align with group direction (the agent "won" last round), the tension item becomes the agent's highest-magnitude uncommitted item framed as "what's next" rather than "what's unresolved."

### Step 8: Select Speaking Order

Weighted random selection across all agents. Weight equals the agent's highest-tension item magnitude. Draw without replacement to produce a full ordering.

### Step 9: Assemble First Prompt

For the opening agent:

| Block | Content | Token Budget |
|---|---|---|
| Identity | Static persona definition. Cached across rounds. | ~2k |
| Situation | Output of Step 6. Agent-specific curated state. | 8-15k |
| Task | The tension item from Step 7, framed as a choice or question. Not "continue the discussion." Not "what do you want to push for." A specific, loaded prompt: "You believe [X] at magnitude [N]. The group moved toward [Y]. What do you do with this?" | ~1-2k |

For subsequent agents in the opening sequence (before any agent has responded to another): same structure, but the Task block additionally notes who spoke before them and what those agents opened with. This prevents redundant openings without introducing full conversation dynamics.

---

## Mid-Round Prompt Structure

Mid-round prompts skip Steps 1-8 entirely. The agent already has context from the conversation.

| Block | Content |
|---|---|
| Identity | Same static block (cached) |
| Conversation history | Accumulated turns from this round |
| Task | "Here is what [Agent] just said. Respond." |

No curation. No thinking routines. No BackgroundAgent mutations. No tension calculation.

### Mid-Round Truncation Strategy

Conversation history accumulates linearly. When it exceeds 70% of available context (after Identity and Task blocks), apply rolling summarization: older exchanges compress into a summary block while recent turns (last 3-4) remain verbatim. This preserves immediate conversational thread while managing token growth in long rounds.

---

## Failure Modes and Handling

**Corrupt save file**: Pipeline halts. No silent degradation. Operator must resolve before round starts.

**BackgroundAgent mutation conflict**: Two BackgroundAgents target the same magnitude on the same agent. Last-write-wins within a single step; the diff log preserves both mutations for audit. If this becomes frequent, introduce a merge strategy.

**Curator produces oversized Situation block**: Hard cap at 15k tokens. If the curator exceeds this, deterministic truncation drops lowest-magnitude items until the block fits. Log what was cut.

**All agents have low tension**: If no agent's tension item exceeds a minimum threshold, the round starts with a randomly selected agent and a generic "what matters most to you right now" task. This is the fallback, not the design target. If it fires frequently, the magnitude system or BackgroundAgents need tuning.

**Thinking routine timeout**: Each thinking routine call has a wall-clock timeout. If Research times out, the agent proceeds without new information. Reflect and Strategize timeouts use the pre-routine save file state. Log the skip.

---

## Key Asymmetries

| Property | Round Start | Mid-Round |
|---|---|---|
| State mutations | Yes (Steps 2-4) | No |
| LLM curator call | Yes (Step 6) | No |
| Thinking routines | Yes (Step 4) | No |
| BackgroundAgent intervention | Yes (Step 3) | No |
| Context source | Curated Situation block | Conversation history |
| Task framing | Provocation from tension item | Reaction to prior speaker |
| Token cost driver | Curation pipeline | Conversation accumulation |
| Failure risk | Pipeline complexity | Context overflow |