# How does a round begin after a reset?

*Generated: 2026-03-18 02:13 | Question 1 | 125s | Mode: ideas*

## Decisions

### Round Start Assembly Pipeline

A round start is a **reconstruction from artifacts**, not a continuation. The orchestrator assembles a fresh prompt for each agent from three blocks, in order:

1. **Identity Block** (~2k tokens, static) -- Persona definition, team role, archetype, disposition traits, stubbornness coefficient, archival thresholds. Loaded from config. Does not change between rounds.

2. **Situation Block** (~8-15k tokens, curated) -- The agent's current world. Built through a sequential pipeline with strict ordering:

   ```
   Save File
     -> Intra-Team Talk Results (magnitude shifts from teammates)
     -> BackgroundAgent Mutations (planted ideas, stat bumps, stance shifts)
     -> Random/Dream Events (if any fired)
     -> Deterministic Filter (drop archived ideas, drop resolved decisions)
     -> LLM Curator Pass (compress, editorialize, surface surprises)
     -> Final Situation Block
   ```

   Each pipeline stage has a timeout. If a stage fails, it is skipped and the pipeline continues with the previous stage's output. The deterministic filter output is the **minimum viable situation block** -- the curator improves it but is never required.

3. **Task Block** (~1-2k tokens, phase-appropriate) -- A provocation, not a continuation prompt. References the agent's own state deltas where possible. See Task Prompt Templates below.

### Mid-Round Turns

Mid-round turns are structurally different from round starts:

- **No curator call.** No save file reload. No pipeline.
- The agent receives the **ongoing transcript** plus a lightweight response prompt ("respond to what was just said").
- The agent operates from **conversational momentum**, not reconstructed state.
- Mid-round turns are cheap. Round starts are expensive (N agents x curator call + state deserialization + prompt assembly).

### The Drift Mechanism

The gap between what the agent remembers caring about and what their state says matters now is the core behavioral feature. Drift is produced by the cumulative effect of:

- BackgroundAgent stat manipulation (agents don't know which changes were external)
- Intra-team talk magnitude shifts (good ideas rise, bad ideas fall)
- Random/dream events
- Curator editorial choices (what gets surfaced, what gets buried)
- Archival threshold differences (stubborn agents hold ideas longer)

An agent entering Round 3 has genuinely changed since Round 2 ended. They speak from **internal state**, not reaction to prior transcript.

### Task Prompt Templates

Task prompts are phase-appropriate provocations. They should reference agent state deltas, not just generic framing. Templates per phase:

**Brainstorm Phase:**
- "Your highest-magnitude idea is [X] at [N]. What's your strongest conviction entering this round, and what's behind it?"
- "A new idea appeared in your state: [planted idea]. Does it change how you see the problem?"

**Refine Phase:**
- "Your stance on [X] shifted from [old] to [new] after team talk. Do you still hold it?"
- "Which open disagreement has the highest stakes for the final outcome?"

**Specify Phase:**
- "[Decision X] has [N] committed agents. What would lock it in or break it apart?"
- "What's still underspecified about [highest-magnitude undecided topic]?"

**Review Phase:**
- "The team committed to [decisions]. What's the weakest link?"
- "What got dropped that shouldn't have?"

The task block is a nudge -- agent behavior is dominated by the situation block's content. But state-delta references force agents to **process drift** rather than ignore it, which is where the interesting behavior lives.

### Curator Behavior and Failure Mode

**Normal operation:** The LLM curator receives the deterministic filter output and produces a narrative situation block. It compresses prior-round key moments, editorializes ("you were passionate about X but got pushback"), and decides what's surprising enough to include. Budget: ~8-15k tokens.

**Fallback operation:** If the curator call fails, times out, or returns malformed output, the deterministic filter output is used directly. This is the agent's filtered save file -- ideas with magnitudes, stances, commitments, personal summary, plus any BackgroundAgent and intra-team mutations applied. Estimated size: ~3-4k tokens. The agent receives a smaller, less narrative situation block but can still function coherently.

**Validation:** Curator output is not audited in V1. The error budget is implicitly bounded by the fact that agents re-derive priorities from magnitudes each round -- a curator mischaracterization affects tone and framing but not the underlying numeric state. Flag for V2: add curator output validation or at minimum log curator inputs and outputs for post-session review.

### Save File Format

Each agent's save file between rounds contains:

- Current ideas with magnitudes (numeric, rise and fall based on discussion/intervention)
- Current stances with magnitudes
- Decisions committed to (with confidence values)
- 3-5 sentence personalized summary: "what happened last round from your perspective"

This is the **source of truth** for agent state. Everything in the round-start pipeline reads from or writes to this file.

### Pipeline Timeout and Fallback Rules

Each stage in the assembly pipeline runs with an independent timeout. Fallback behavior per stage:

| Stage | On Failure | Effect |
|---|---|---|
| Save File Load | Fatal -- cannot start round for this agent | Agent skips round |
| Intra-Team Talk | Skip -- use pre-talk magnitudes | Agent misses teammate influence |
| BackgroundAgent Pass | Skip -- no external mutations applied | Agent state unchanged from last round |
| Random/Dream Events | Skip -- no random shifts | Deterministic round |
| Deterministic Filter | Fatal -- required for valid state | Agent skips round |
| LLM Curator | Skip -- use deterministic filter output directly | Smaller, less narrative situation block |

Two stages are fatal: save file load and deterministic filter. All others degrade gracefully.

### Operator Visibility

Round boundaries produce a **one-line diff summary per agent** in the session log. Examples:

- "Agent shifted from advocating monolith to questioning it (magnitude 8 -> 3)"
- "Agent received planted idea: event-driven architecture (magnitude 6)"
- "No significant drift -- top priorities unchanged"

This lets the operator see whether the system is evolving or churning without reading full transcripts.

## Open Items for Pre-Implementation Resolution

1. **Mid-round state refresh trigger.** At what turn count or token threshold does a mid-round turn require a state re-injection? Long rounds (12+ turns) will push early context out of the window. Define the trigger condition and what a mid-round refresh includes (lightweight state reminder vs. mini-curator call). This determines whether the clean two-mode distinction (round-start vs. mid-round) holds at scale.

2. **Curator token budget variance.** The situation block ranges from ~3-4k (fallback) to ~8-15k (full curator). This means the agent's available thinking budget swings by ~10k tokens depending on curator success. Decide whether to pad the fallback output to a consistent size or let agents operate with variable context budgets.

3. **Task prompt template completeness.** The templates above are starting points. Each phase needs 2-3 variants selected based on agent state (e.g., high-drift agent gets a different prompt than a stable one). Specify selection logic.