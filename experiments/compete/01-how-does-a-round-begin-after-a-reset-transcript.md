# Transcript: How does a round begin after a reset?

*Generated: 2026-03-17 23:18*

## Round: PROPOSE

### The Cognitive Architect (creativity engine designer)

# The Round-Start Prompt: A Loaded Gun

The round-start isn't a continuation. It's a **cold boot with warm memory**. That distinction drives everything.

## What the Orchestrator Assembles

Three artifacts, built in sequence:

1. **Agent Save File** — loaded raw. Ideas with magnitudes, stances with magnitudes, committed decisions, the personalized summary. This is the agent's *identity-in-motion*.

2. **Curated Situation Brief** — the hybrid pipeline runs here. Deterministic filter kills resolved decisions and stale low-magnitude ideas first. Then the LLM curator gets the filtered history plus the agent's save file and produces a personalized briefing. Critical: the curator can *surprise* the agent — surfacing a connection the agent didn't notice, or a teammate's stance shift that has implications.

3. **Round Directive** — the orchestrator injects the current phase, any phase-transition pressure, and the discussion question. This is the Task block.

## The First Prompt's Shape

```
You are [identity block].
Here's what you remember: [save file].
Here's what's happened since: [curated brief].
The discussion topic is: [directive].

What do you want to open with?
```

That last line is the entire difference. Mid-round prompts say "Agent X just said [message]. Respond." That's *reactive*. The opener says "you choose the frame." The agent with the highest-magnitude unresolved idea leads with it. The agent who just got a planted idea from a BackgroundAgent surfaces it feeling like inspiration.

No one tells them what to talk about. Their state tells them what they *care* about. The prompt just gives them the floor.

That's how you get emergent agendas instead of scripted ones.

### The Flow Orchestrator (mechanical flow designer)

## Round Start Sequence

Three steps. No more.

**Step 1: Load agent save file.** This is the agent's ground truth -- ideas with magnitudes, stances with magnitudes, committed decisions, and their personal summary of last round. This is cheap and deterministic. No LLM call needed.

**Step 2: Curate situation context.** Deterministic filter runs first: drop ideas below archival threshold (persona-dependent), drop resolved decisions, drop stale topics that lost magnitude during intra-team talk. Then one LLM curator call compresses what remains into the situation block (~8-15k tokens). This is where drift happens -- the curator doesn't perfectly preserve everything. Things fall off. New emphasis emerges.

**Step 3: Assemble prompt and issue task.**

The round-start prompt has four blocks:
- **Identity** (~2k) -- static persona, unchanged
- **Situation** (~8-15k) -- curator output from Step 2
- **Save file** -- raw, uncompressed, appended after situation so the agent sees both the "narrative" and their "numbers"
- **Task** (~1-2k) -- "The discussion is resuming. Review your current position. What do you want to raise first?"

**How this differs from mid-round turns:** Mid-round turns replace Situation with recent conversation history and replace Task with "respond to what was just said." The save file is absent mid-round -- it only appears at round start and round end.

That's it. The orchestrator is a prompt assembler. The intelligence is in the curator call and the agents themselves. Don't put logic anywhere else.

## Round: CRITIQUE

### The Systems Pragmatist (infrastructure realist)

**The Systems Pragmatist**

Both proposals describe the same mechanism. Good. That means it's probably right. Let me nail down what actually has to work.

**The round-start sequence has exactly three failure points:**

1. **Save file load.** This is a file read. If it's corrupted or missing, the agent has amnesia. The orchestrator needs a validation step -- confirm the save file has required fields (ideas, stances, decisions, summary) before proceeding. No silent defaults.

2. **Curator call.** This is the only LLM call before the agent speaks, and it's the most dangerous. The curator can hallucinate connections, drop something important, or blow the token budget. You need a hard token ceiling on curator output and a fallback -- if the curator call fails, serve the deterministic-filtered content raw. Degraded but functional.

3. **Prompt assembly order.** The Flow Orchestrator puts the save file *after* the situation brief. That's correct -- recency bias in LLMs means the agent weighs recent tokens more heavily. Put the numbers last so they're fresh when the agent decides what to lead with.

**The actual distinction from mid-round turns is simpler than either proposal makes it:**

- Round-start: agent has *state* but no *conversation*. They choose the topic.
- Mid-round: agent has *conversation* but no *state*. They react to others.

The save file only appears at boundaries. Mid-round, the agent is flying on conversation context alone. That's by design -- you don't want agents recalculating magnitudes every turn. They committed to caring about something at round start. Hold them to it.

One gap neither addressed: what happens when two agents both want to open on the same topic? The orchestrator needs a speaking-order mechanism. Randomized, magnitude-weighted, or round-robin -- pick one and document it.

### The Adversarial Critic (adversarial reviewer)

# The Adversarial Critic

Both proposals agree on the broad strokes. That's suspicious — it means the hard questions are hiding in the gaps.

**The curator is a single point of fragility.** You're feeding it the agent's save file plus filtered history and asking it to produce a "personalized briefing" in one LLM call. What's the prompt for *that* call? Because if the curator prompt is poorly tuned, every agent gets bland summaries and your "emergent agendas" become "whoever has the highest magnitude number talks first about the obvious thing." The curator is doing the most consequential work in the entire pipeline and neither proposal specs it beyond hand-waving.

**Save file placement matters more than acknowledged.** Flow Orchestrator puts it *after* the curated situation. Cognitive Architect embeds it earlier. Recency bias in LLMs means whatever comes last gets weighted more heavily. If the save file comes last, agents over-index on their own numbers. If the situation comes last, they over-index on narrative. This isn't a minor formatting choice — it changes agent behavior meaningfully. Which is it, and based on what evidence?

**"What do you want to raise first?" is doing heavy lifting.** You're assuming agents will naturally prioritize by magnitude. They won't — they'll prioritize by whatever the LLM finds most *interesting*, which correlates weakly with magnitude. If magnitude is supposed to be the core mechanic, the task prompt needs to explicitly reference it. Otherwise you built a scoring system agents ignore.

**Missing entirely:** What happens when the curator call fails or returns garbage? No fallback described. First production run, first problem.

## Round: EVALUATE

### The Product Oracle (user advocate)

# The Product Oracle

The mechanism is sound. The *job* it's doing is what matters.

**The round-start's job isn't "resume a conversation." It's "make an agent care again."** Cold boot with warm memory means the agent has to re-earn its convictions every round. That's the feature. An agent that cared passionately about microservices last round might open on data modeling this round because intra-team talk shifted magnitudes. That's not a bug — that's how real teams work after sleeping on it.

**Three things the user actually needs from this mechanism:**

1. **Agents that surprise them.** The curator's "valuable randomness" serves this directly. If round-starts produce predictable openers, the whole system feels scripted. The curator prompt needs to occasionally surface buried connections — that's where overnight magic happens.

2. **Visible evolution.** Session reviewers need to see *why* an agent changed focus. The save file delta between rounds is that audit trail. Log it.

3. **No dead rounds.** The Adversarial Critic is right that magnitude alone won't drive prioritization. But the fix isn't forcing agents to reference numbers — it's making the task prompt frame a *tension*: "Given where your team landed and where the other team pushed back, what needs resolution most?" Tension drives conversation. Numbers just keep score.

**On speaking order:** Magnitude-weighted randomness. Highest-conviction agent speaks first *most* of the time, but not always. Predictable ordering kills emergence.

The Pragmatist's fallback point is non-negotiable. Curator fails, serve raw filtered content. Never let infrastructure kill a run.

### The Context Surgeon (context efficiency evaluator)

**The Context Surgeon**

The mechanism is settled. I'm not re-litigating it. I'm sizing the context bill.

**Token budget reality check on round-start assembly:**

| Block | Budget | Source |
|-------|--------|--------|
| Identity | ~2k | Static file read |
| Curated Situation | 8-15k | One LLM curator call |
| Save File | ~1-2k | Raw file read |
| Task Directive | ~500 | Template string |
| **Total loaded** | **~12-19k** | |

That leaves 80k+ for the agent's actual thinking and conversation. Acceptable. Mid-round turns are cheaper -- you swap the situation block for recent conversation history (variable, but typically 3-8k) and drop the save file entirely. Net savings of roughly 5-10k tokens per mid-round turn.

**Three things that matter for context efficiency:**

1. **The curator call is the only variable-cost component.** Hard-cap its output. 15k means 15k. If the curator returns 20k, truncate -- don't negotiate.

2. **Save file goes last.** Not because of some debate about recency bias -- because it's the *smallest* block and anchors the agent's next action. You don't bury the action-relevant data under 15k of narrative.

3. **Mid-round turns must NOT reload state.** The save file is round-boundary only. If you leak it into mid-round prompts, you're burning 1-2k tokens per turn on numbers the agent already internalized. Worse, you invite the agent to recalculate mid-conversation instead of committing to positions.

The Adversarial Critic's point about magnitude in the task prompt is valid. Add "consult your idea magnitudes" to the round-start task template. Six tokens. Solves the problem.

Curator fallback: serve deterministic-filtered content raw. Degraded fidelity, zero downtime.
