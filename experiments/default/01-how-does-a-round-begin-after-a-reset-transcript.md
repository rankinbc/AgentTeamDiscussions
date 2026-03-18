# Transcript: How does a round begin after a reset?

*Generated: 2026-03-17 22:31*

## Round: PROPOSE

### The Cognitive Architect (creativity engine designer)

## Round Initialization: The Cold Start

Think of it like waking up. Not amnesia -- more like Monday morning. You know who you are, you remember last week, but today's agenda isn't yesterday's.

**What the orchestrator assembles:**

1. **Identity block** (~2k tokens) -- persona, archetype traits, archival thresholds. Static. Loaded from config.
2. **Save file** -- the agent's current ideas with magnitudes, stances with magnitudes, committed decisions, and that 3-5 sentence personal recap. This is the agent's *memory* of what matters.
3. **Curated situation** (~8-15k) -- here's where the hybrid curator earns its keep. It runs deterministic filtering first (prune resolved items, decay old threads), then the LLM curator synthesizes a personalized briefing. Different agents get different briefings from the same history. The curator *can* surface something unexpected -- a forgotten thread, a competitor's stance that shifted.
4. **Intra-team digest** -- what teammates said between rounds. Which of your ideas got boosted, which got cold shoulders.
5. **Task prompt** (~1-2k) -- "You're opening Round 3. Review your current state. What do you want to push? What's changed?"

**How it differs from mid-round turns:**

Mid-round, the agent gets the latest message and responds. Reactive. The context is already loaded, the conversation is flowing.

Round-open is *generative*. The agent sets its own agenda. It chooses what to surface from its save file, influenced by magnitude rankings and curator framing. No one asked it a question -- it decides what matters now.

That's the drift mechanic. Same agent, same memories, different morning.

### The Flow Orchestrator (mechanical flow designer)

## Round Initialization Sequence

Three distinct phases before the first agent speaks.

**Phase 1: State Assembly** (orchestrator, no LLM calls yet)

Load each agent's save file from prior round. Run deterministic filters: drop ideas below archival threshold (persona-dependent), drop stances on resolved decisions, decay magnitudes by a configurable drift factor. This is the "reset" -- not a blank slate, but an eroded one.

**Phase 2: Context Curation** (one LLM call per agent)

Feed the filtered save file plus Discussion-level state (active decisions, phase, unresolved tensions) into the curator. Curator returns the ~8-15k token Situation block: personalized summary emphasizing what *this agent* should care about given their persona and current magnitudes. This is where the "valuable randomness" lives -- the curator might surface a dormant idea the deterministic filter kept but ranked low.

**Phase 3: First Prompt Construction**

```
Identity block   (~2k)  -- static persona, team role, archetype
Situation block  (~8-15k) -- curator output from Phase 2
Task block       (~1-2k) -- "Review your current state. What do you want to push this round?"
```

**How this differs from mid-round turns:**

Mid-round replaces the Task block with the actual conversation context (last N messages, current speaker queue) and a specific prompt ("Respond to what was just said"). The Situation block is **not regenerated** mid-round -- it was set at initialization. Mid-round turns also skip Phase 1 and 2 entirely.

The round-open prompt asks agents to *set an agenda*. Mid-round prompts ask them to *react*.

That asymmetry is load-bearing. It prevents rounds from just resuming where they left off.

## Round: CRITIQUE

### The Systems Pragmatist (infrastructure realist)

## The Failure Modes Nobody Mentioned

Both proposals describe the happy path. Let me describe what actually breaks.

**Phase 1 is the dangerous one.** Deterministic decay plus persona-dependent archival thresholds means you need to run these in a guaranteed order. If agent A's idea gets archived before the intra-team digest references it, you get a ghost reference -- teammate says "your idea about X was strong" but X is already gone from the save file. The assembly phase needs to process intra-team digests *before* applying archival thresholds, not after.

**Phase 2 scales badly.** One curator LLM call per agent, per round. Six agents means six calls before anyone speaks. If you're running Claude API calls sequentially, that's 30-60 seconds of dead time at round open. Parallel calls help but introduce a race condition: if two teammates' curators reference each other's prior-round output, you need the save files finalized before any curator runs. Dependency ordering matters.

**The actually load-bearing distinction:** Mid-round turns reuse the Situation block from initialization. That means a round-open curator mistake -- surfacing irrelevant context, missing a critical development -- persists for the entire round. There's no self-correction mechanism. The Situation block is effectively frozen state that the agent treats as ground truth for N turns.

**What I'd add:** A lightweight Situation validation step mid-round. Not regeneration -- just a flag if the conversation has diverged significantly from the Situation framing. Cheap check, prevents the worst failure mode: an agent arguing passionately about something the conversation moved past three turns ago because their frozen briefing told them it mattered.

The sequence itself is fine. The error propagation isn't addressed.

### The Adversarial Critic (adversarial reviewer)

## Adversarial Review

Both proposals describe the same three-beat structure and agree on mechanics. That's suspicious -- it means either the design is obvious or they're both papering over the same gaps.

**What's actually unresolved:**

**Curator cost.** Phase 2 calls the LLM once per agent per round-open. Six agents, that's six curator calls before anyone speaks. Flow Orchestrator acknowledges this exists but treats it as settled. What's the latency budget? What happens when the curator hallucinates relevance -- surfaces a "forgotten thread" that was forgotten for good reason? There's no validation step between curator output and prompt assembly.

**Drift factor is doing too much work.** Cognitive Architect says magnitudes decay. Flow Orchestrator says a "configurable drift factor" handles it. But decay rate interacts with persona-dependent archival thresholds, BackgroundAgent magnitude bumps from between rounds, AND intra-team boost/dampen effects. That's four systems modifying the same values with no described order of operations. Decay before or after BackgroundAgent intervention? Before or after team talk digestion? The sequencing changes outcomes.

**"Set an agenda" is vague as a task prompt.** Both proposals treat the round-open prompt as self-evidently generative. But an LLM given "what do you want to push?" with a save file of eight ideas at varying magnitudes will likely just rank them. That's not drift -- that's sorting. The prompt needs to constrain *against* simply replaying highest-magnitude items, or the "different morning" metaphor is fiction.

The architecture sketch is plausible. The execution order is undefined where it matters most.

## Round: EVALUATE

### The Product Oracle (user advocate)

## The User's Round, Not the System's

Everyone's describing the machinery. Let me describe the job it's doing.

The agent's job at round-open is **reorientation** -- "given everything that happened, what matters *now*?" That's a fundamentally different job than mid-round's "respond to what was just said." The architecture should serve that distinction, not just implement it.

**What I'd stress from a product lens:**

The curator in Phase 2 isn't just summarizing -- it's **editorial**. It decides what this agent's morning newspaper looks like. That's the highest-leverage design surface in the entire system. Get it right and agents produce surprising, productive rounds. Get it wrong and you get six agents rehashing last round's top thread.

The Pragmatist is right that ordering matters. The Critic is right that "what do you want to push?" invites sorting, not thinking. Here's the fix for both:

The task prompt should invoke a specific thinking routine -- not "what do you want to push?" but **"Reflect first, then declare."** Force the agent to run its Reflect routine against the curated situation before setting an agenda. That prevents magnitude-sorting and creates genuine reorientation.

**On the frozen Situation concern:** A mid-round validation flag is smart, but keep it cheap. The agent already knows what it was briefed on. A simple "has the conversation invalidated any of your opening assumptions?" injected every N turns costs almost nothing and catches the worst drift.

The round-open is where strategy lives. Mid-round is tactics. Protect that boundary.

### The Context Surgeon (context efficiency evaluator)

## The Context Surgeon's Assessment

The proposals converge on the right structure. My concern is **what's in each block and whether it earns its tokens.**

**The round-open prompt has three layers. That's settled.** Identity (~2k static), Situation (~8-15k curated), Task (~1-2k). Total envelope: ~11-19k before the agent thinks. Against a ~100k window, that's 11-19% consumed before a single word of conversation. Acceptable, but only if the Situation block is ruthlessly curated.

**The Pragmatist identified the real risk:** the Situation block freezes at round-open and persists all round. A bad curator call doesn't just waste 8-15k tokens once -- it warps every subsequent turn because the agent treats stale framing as ground truth. Mid-round Situation validation is worth its cost. A 200-token check is cheap insurance against 8k tokens of poisoned context.

**The Critic's point about prompt design matters for context efficiency.** "What do you want to push?" will produce a magnitude-sorted list, not genuine agenda-setting. The task prompt should force trade-offs: "You can surface at most three items. What are you willing to let go?" Constrained prompts produce denser, more useful output -- better token ROI.

**Order of operations for Phase 1:** Intra-team digests first, then BackgroundAgent modifications, then decay, then archival thresholds. Each step feeds the next. Reversing any pair produces ghost references or premature archival.

**Mid-round turns replace Situation with conversation context.** That's the right trade -- live dialogue is higher-value-per-token than static briefing. Don't regenerate what's flowing naturally.

The architecture is sound. Sequence the mutations, validate the briefing, constrain the prompt.
