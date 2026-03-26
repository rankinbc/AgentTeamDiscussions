# Transcript: What's the difference between a "round" and a "turn"?

*Generated: 2026-03-17 21:37*

## Round: PROPOSE

### The Cognitive Architect (creativity engine designer)

Good question. These get conflated fast if you don't nail them now.

**Turn** -- one agent speaks. That's it. Agent B receives what Agent A said, thinks, responds. The turn ends when their response is delivered. Mid-turn, nothing changes structurally. Same situation block, same curated context. It's a volley in a rally.

**Round** -- a complete cycle of cross-team exchange. Both teams get to speak, respond, and counter-respond up to some configured limit (say, 4-8 turns per round). The round ends when either the turn limit hits or a phase-transition condition fires -- whichever comes first.

**Between turns:** Nearly nothing. Next agent gets the new message appended to their context. No re-curation, no thinking routines, no BackgroundAgent intervention. Cheap. Fast.

**Between rounds:** Everything. This is where the machinery lives:
- Intra-team talk (teammates discuss what just happened)
- BackgroundAgents analyze and manipulate magnitudes
- Save files written (atomic, schema-validated)
- Thinking routines run (Reflect, Research, Strategize)
- Deterministic filter prunes dead weight
- LLM curator rebuilds the situation block
- Prompt reassembled from scratch

Think of it like boxing. A **turn** is a punch. A **round** is three minutes of fighting. Between rounds you go to your corner, your coach talks to you, the cutman patches you up, and you come back different.

The round boundary is where drift happens. Where agents forget, reprioritize, get new ideas planted. Turns are reactive. Rounds are evolutionary.

**Open item:** What triggers round-end besides turn count? Consensus detection? Energy decay? Worth specifying.

### The Flow Orchestrator (mechanical flow designer)

## Round vs. Turn: Boundary Definitions

**Turn**: One agent speaks once. That's it. Agent receives Task prompt ("Agent X said this, respond"), generates output, output gets routed. Turn ends when the agent's response is committed to the transcript.

**Round**: A sequence of turns where all participating agents have engaged on a shared agenda. Round ends when a termination condition fires:

- All agents have taken at least N turns (minimum threshold)
- No new ideas surfaced in the last full rotation (stagnation detection)
- Phase-specific turn cap hit (hard ceiling, prevents runaway cost)
- A decision reaches commitment threshold

**What happens between turns**: Almost nothing. Next agent gets the latest transcript appended to their existing Situation block. No re-curation, no thinking routines, no BackgroundAgent intervention. Fast and cheap.

**What happens between rounds**: Everything expensive. Save files written. BackgroundAgents run analysis and manipulate state. Intra-team talk executes. Thinking routines fire (Reflect, Research, Strategize). Deterministic filter prunes. LLM curator rebuilds Situation blocks. Prompt reassembly. This is the reset with drift.

**The sequence**:
```
Round N
  Turn 1 → Turn 2 → ... → Turn K → [termination fires]
Between-Round Processing
  Save → BackgroundAgents → IntraTeam → ThinkingRoutines → Filter → Curate → Assemble
Round N+1
  Turn 1 → ...
```

**Critical constraint**: Mid-round context only grows (append-only transcript). Between-round context gets rebuilt from scratch. That's what makes rounds the natural cost and coherence boundary.

Six open items remain: minimum turn threshold, stagnation detection window, per-phase turn caps, decision commitment threshold values, intra-team turn budget, and whether BackgroundAgents can trigger early round termination.

## Round: CRITIQUE

### The Systems Pragmatist (infrastructure realist)

**Round vs. Turn: The Failure-Mode-Informed Definition**

A **turn** ends when an agent's response is committed to the transcript. One agent, one output, done. Between turns: append the new message to the next agent's context. No re-curation, no state manipulation. If this boundary gets expensive, something is architecturally wrong.

A **round** ends when a termination condition fires. The two proposals largely agree here, so let me focus on what actually matters -- which termination conditions are *implementable* versus *aspirational*:

**Reliable (build these):**
- Hard turn cap per phase (configurable, prevents runaway cost)
- Minimum turn threshold (everyone speaks at least once)

**Fragile (defer these):**
- Stagnation detection ("no new ideas") requires defining "new" -- that's an LLM classification call mid-round, which contradicts the "between turns is cheap" principle
- Consensus detection and decision commitment thresholds sound great but need magnitude tracking mid-round, which we said doesn't happen until between-round processing

Start with the hard cap. Add smart termination later when you have session data showing *where* rounds actually go stale.

**Between rounds** is where all the expensive machinery runs. The sequence matters for correctness: save state *before* BackgroundAgents mutate it (you need the clean snapshot), then BackgroundAgents, then intra-team talk, then thinking routines, then filter, then curate, then assemble.

**The real risk:** scope creep at the round boundary. Every clever feature someone wants to add will naturally gravitate here. Gate it hard or your between-round processing will cost more than the round itself.

### The Adversarial Critic (adversarial reviewer)

## The Adversarial Critic

You're both saying the same thing and acting like you've defined something. Let me push on what's actually unsettled.

**Turn definition is clean.** One agent, one response, transcript appended. No dispute. Move on.

**Round definition is where you're papering over problems.**

First: you both say "between turns, almost nothing happens." But context grows monotonically mid-round. By turn 8 in a round, you've appended 8 responses to a Situation block that was curated for freshness at round-open. You're re-creating the staleness problem you designed curation to solve. What's the actual token budget for mid-round growth before coherence degrades? Neither of you addressed this.

Second: Flow Orchestrator lists four termination conditions. That's four competing triggers with no priority order. What happens when stagnation detection fires at turn 3 but minimum threshold is 4? You need a precedence rule or these will conflict in implementation.

Third: "all participating agents have engaged on a shared agenda" -- what shared agenda? Agents enter rounds with independently curated Situation blocks. Agent A's top priority might not appear in Agent B's context at all. You're assuming agenda alignment that the architecture explicitly doesn't guarantee.

Fourth: the between-round pipeline is ordered sequentially, but you haven't justified why BackgroundAgents run before intra-team talk. If teammates surface something important that BackgroundAgents should amplify, you've got the wrong execution order.

**What's actually decided:** turns are cheap volleys, rounds are expensive resets. Everything else needs tighter specification before it's a design rather than a metaphor.

## Round: EVALUATE

### The Product Oracle (user advocate)

## The Product Oracle

The panel's converging. Let me frame what matters from the user's perspective.

A **turn** is an agent doing its job: receive message, think, respond. The user doesn't care about turns. They're invisible plumbing.

A **round** is a unit of *progress the user can observe*. When someone reviews a session transcript tomorrow morning, rounds are the chapters. Each round should leave the conversation measurably different from where it started -- new ideas surfaced, stances shifted, decisions closer to commitment. If a round ends and nothing changed, the system wasted money.

That's why the termination question matters so much. The Pragmatist is right: ship with hard turn caps, add smart detection later. But the *reason* to add it later isn't engineering elegance -- it's that users will immediately notice rounds that spin wheels. Session data will tell you exactly where.

The Critic raised the real unsolved problem: **mid-round context bloat**. If your Situation block was curated for 8-15k tokens at round-open, and you're appending 8 responses at ~500-1k tokens each, you've blown past your budget by turn 6. That's not a nice-to-have concern. That's a "coherence degrades and the user reads garbage" concern. You need a mid-round token ceiling that triggers early round termination. Not stagnation detection -- just a byte count.

**My recommendation:** Define round success criteria per phase. Brainstorm rounds succeed when new ideas emerge. Refinement rounds succeed when magnitudes converge. Review rounds succeed when decisions commit. Termination should serve the job the round was hired to do.

### The Context Surgeon (context efficiency evaluator)

**The Context Surgeon's Assessment**

The signal-to-noise ratio here is actually decent. Let me cut to what's settled versus what's still bleeding.

**Settled (high confidence, no contradictions):**

- **Turn**: one agent, one response, committed to transcript. Between turns: append only. No re-curation, no state mutation, no expensive calls.
- **Round**: a sequence of turns ending at a termination condition. Between rounds: the full pipeline runs (save, BackgroundAgents, intra-team, thinking routines, filter, curate, assemble).
- Mid-round context is append-only. Between-round context is rebuilt from scratch.

**Settled with caveats:**

- Between-round pipeline ordering: save-first is justified (clean snapshot before mutation). BackgroundAgents-before-intra-team is *not* justified -- the Critic's right that this needs a rationale or reversal.

**Not settled (being treated as settled):**

- Round termination conditions. Only hard turn cap and minimum threshold are implementable now. Stagnation detection and consensus detection require mid-round LLM calls or magnitude tracking, contradicting the "turns are cheap" principle. Defer them.
- Mid-round context bloat. Nobody specified a token budget for append growth. Eight turns of appended responses could push well past the curated Situation block's target range. This needs a number.
- "Shared agenda" is a fiction. Independently curated agents don't share agendas. The round concept works without this assumption -- drop it.

**My recommendation:** Spec the turn/round boundary as defined above. For V1 termination: hard cap only, configurable per phase. Log everything so you can design smart termination from real data later. Don't build detection machinery you can't yet calibrate.
