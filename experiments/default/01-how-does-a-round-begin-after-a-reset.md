# How does a round begin after a reset?

*Generated: 2026-03-17 22:31 | Question 1 | 378s | Mode: default*

It seems I need explicit write permission to be granted. While that gets sorted, here is the complete synthesized design spec from the discussion:

---

# Round Initialization Design Spec

**Status:** Draft
**Last Updated:** 2026-03-17
**Source:** Agent team design discussion (Propose/Critique/Evaluate)

---

## Purpose

This spec defines how the orchestrator assembles context and constructs the first prompt when a new round begins after a reset. It covers the three initialization phases, the structure of the round-open prompt, how round-open differs from mid-round turns, and the error-handling mechanisms that protect against stale or malformed context.

---

## Core Principle

Round-open is **generative**. The agent sets its own agenda -- it chooses what to surface, what to push, what to let go. Mid-round is **reactive**. The agent responds to what was just said.

This asymmetry is load-bearing. It prevents rounds from simply resuming where they left off. The architecture must enforce it.

---

## Initialization Sequence

Three phases execute in strict order before the first agent speaks in a new round. No agent receives a prompt until all three phases complete for all agents.

### Phase 1: State Assembly

**Executor:** Orchestrator (deterministic, no LLM calls)

**Purpose:** Rebuild each agent's working state from the prior round's save file, incorporating all between-round modifications.

**Inputs per agent:**
- Save file from prior round (ideas with magnitudes, stances with magnitudes, committed decisions, personal recap)
- Intra-team talk digest (which ideas teammates boosted or dampened)
- BackgroundAgent modifications (magnitude bumps, planted ideas, stance shifts)
- Discussion-level state (active decisions, phase, unresolved tensions)

**Mutation order (strict):**

1. **Load save file** -- raw state from end of prior round
2. **Apply intra-team digests** -- teammate reactions modify idea/stance magnitudes
3. **Apply BackgroundAgent modifications** -- magnitude bumps, planted ideas, stance shifts
4. **Apply decay** -- multiply all magnitudes by a configurable drift factor (0 < drift < 1)
5. **Apply archival thresholds** -- drop ideas/stances below the agent's persona-dependent threshold

This order is mandatory. Each step feeds the next. Rationale for key ordering decisions:

- **Intra-team before BackgroundAgent:** Team consensus should be visible to BackgroundAgents if they run reactively. Even if BackgroundAgents ran between rounds (before this phase), their planted ideas need to survive the subsequent decay and archival steps.
- **Intra-team before archival:** Prevents ghost references. If a teammate said "your idea about X was strong" but X gets archived before the digest is processed, the agent receives a reference to something it no longer holds. Processing digests first lets a teammate boost save an idea from archival.
- **Decay before archival:** Decay reduces magnitudes; archival removes items below threshold. Reversing this would archive first at pre-decay magnitudes, then decay survivors -- meaning some items survive archival but end up below threshold afterward with no cleanup pass.

**Output:** Filtered, mutated agent state ready for curation.

### Phase 2: Context Curation

**Executor:** One LLM curator call per agent (parallelizable with constraints)

**Purpose:** Transform the filtered agent state into a personalized Situation briefing that fits the context budget and serves the agent's reorientation needs.

**Inputs:**
- Filtered agent state from Phase 1
- Discussion-level state (active decisions, current phase, unresolved tensions)
- Agent persona and archetype traits (for editorial framing)

**Curator behavior:**
- Synthesize a personalized ~8-15k token Situation block
- Emphasize items relevant to this agent's persona and current high-magnitude concerns
- May surface dormant items the deterministic filter kept but ranked low (this is the "valuable randomness" -- the curator's editorial discretion)
- Must not contradict the deterministic output of Phase 1 (no resurrecting archived items, no inventing magnitudes)

**Parallelization constraint:** All Phase 1 processing must complete for all agents before any Phase 2 curator call begins. Save files must be finalized first. Curator calls themselves may run in parallel since each operates on independent per-agent state.

**Latency note:** Six agents means six curator calls. At ~5-10 seconds each, sequential execution adds 30-60 seconds of dead time. Parallel execution is strongly preferred. Budget for this in round-transition timing.

**Failure mode -- curator hallucination:** The curator may surface irrelevant context or frame a "forgotten thread" that was forgotten for good reason. There is no validation step between curator output and prompt assembly in V1. Accept this risk, but log curator outputs for post-hoc review. See the Mid-Round Situation Validation section for the downstream mitigation.

**Output:** One Situation block per agent (~8-15k tokens).

### Phase 3: Prompt Construction

**Executor:** Orchestrator (deterministic assembly)

**Purpose:** Assemble the three-block prompt that each agent receives to open the round.

**Prompt structure:**

```
[Identity Block]     ~2k tokens    Static persona, team role, archetype traits,
                                   archival thresholds. Loaded from config.
                                   Does not change between rounds.

[Situation Block]    ~8-15k tokens Curator output from Phase 2. Personalized
                                   briefing. Different agents receive different
                                   briefings from the same discussion history.

[Task Block]         ~1-2k tokens  Round-open directive. See below.
```

**Total context consumed at round-open:** ~11-19k tokens out of ~100k window (11-19%). The remaining ~80k+ is reserved for agent thinking, response generation, and subsequent mid-round conversation context.

**Task block design -- round-open:**

The task prompt must not invite simple magnitude-sorting. "What do you want to push?" produces a ranked list, not genuine reorientation. The prompt must force trade-offs and invoke the Reflect thinking routine.

Required elements:
- **Invoke Reflect:** Direct the agent to review its ideas and stances against the curated situation before declaring an agenda.
- **Constrain scope:** "You can surface at most three items this round. For each, state why it matters now -- not why it mattered before."
- **Force letting go:** "Name one item you held last round that you are deprioritizing and why."
- **Acknowledge change:** "What is different about your position since last round?"

This produces denser, more useful output than an open-ended "what do you want to push?" and creates genuine reorientation rather than replay.

---

## Mid-Round Turn Structure

Once the round is open and agents have declared their agendas, subsequent turns follow a different pattern.

**What changes:**
- The Task block is replaced with conversation context (last N messages, current speaker queue) and a reactive prompt ("Respond to what was just said").
- The Situation block is **not regenerated**. It persists from round-open for the entire round.
- Phase 1 and Phase 2 do not re-execute.

**What stays the same:**
- The Identity block remains.
- The frozen Situation block remains in context as background framing.

**The key behavioral difference:** Mid-round prompts ask agents to react. Round-open prompts ask agents to set strategy. Protect this boundary -- do not allow mid-round prompts to drift into agenda-setting, and do not allow round-open prompts to become reactive to the prior round's final exchange.

---

## Mid-Round Situation Validation

**Problem:** The Situation block freezes at round-open and persists all round. A bad curator call or a conversation that diverges from the briefing's framing means the agent carries stale or irrelevant context for every subsequent turn. An agent may argue passionately about something the conversation moved past because its frozen briefing says it matters.

**Mitigation:** Inject a lightweight validation check every N turns (configurable, suggest every 3-5 turns).

**Mechanism:** Append to the mid-round task prompt:

> "Has the conversation invalidated any of your opening assumptions? If so, note what has changed and adjust accordingly."

**Cost:** ~200 tokens added to the task block. No additional LLM calls. No Situation regeneration. The agent self-corrects within its existing turn.

**This is not Situation regeneration.** It is a nudge for the agent to notice when its frozen briefing no longer matches reality. Cheap insurance against the worst failure mode of frozen context.

---

## Summary of Behavioral Rules

1. **Initialization is three phases in strict order.** State Assembly, Context Curation, Prompt Construction. No phase begins until the prior phase completes for all agents.

2. **Phase 1 mutation order is fixed.** Load, intra-team, BackgroundAgent, decay, archival. No reordering.

3. **Phase 2 curator calls may run in parallel** but only after all Phase 1 processing is complete.

4. **The Situation block is generated once per round** at initialization. It is not regenerated mid-round.

5. **Round-open prompts are generative.** They invoke the Reflect routine and constrain the agent to surface at most three items with explicit trade-offs.

6. **Mid-round prompts are reactive.** They provide conversation context and ask for response to what was said.

7. **Mid-round validation fires every N turns.** A lightweight self-check prompt, not a Situation rebuild.

8. **Different agents receive different Situation briefings** from the same discussion history, shaped by persona and magnitude state.

9. **The curator may surface unexpected items** (dormant low-magnitude ideas) but must not contradict Phase 1 outputs (no resurrecting archived items).

10. **Context budget discipline:** Round-open consumes 11-19% of the window. The remaining 80%+ is for thinking, response, and conversation.

---

## Open Questions for V2

- **Curator validation:** Should there be a programmatic check between curator output and prompt assembly to catch hallucinated references? V1 accepts the risk; V2 may need guardrails.
- **Adaptive drift factor:** Should decay rate vary based on discussion phase (brainstorm vs. specify) or round count? Currently a single configurable value.
- **Situation refresh trigger:** Instead of fixed-interval validation, should significant conversation events (new decision logged, phase transition) trigger a Situation refresh? Cost-benefit unclear.
- **BackgroundAgent timing:** V1 assumes BackgroundAgents run between rounds before Phase 1. If they run during Phase 1 or reactively to intra-team digests, the mutation order needs revision.

---

I wasn't able to write the file due to permission restrictions on this session. The full spec is above -- you can save it to `docs/design_specs/round-initialization.md` or `output/design_spec_round_initialization.md`, whichever you prefer. Want me to try a different path, or is the inline version sufficient for now?