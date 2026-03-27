# Transcript: How should agent responses be truncated for long discussions?

*Generated: 2026-03-25 12:02*

## Round: PROPOSE

### The Cognitive Architect (creativity engine designer)

**Epistemic State Compression** — not summarization, not windowing. Those are both wrong abstractions.

Here's why: summarization compresses chronologically, which destroys the dialectical structure. A sliding window throws away early anchors that still govern the current debate. Both treat conversation as *narrative* when it's actually *argumentative*.

Cross-pollinate from debate theory: expert debaters don't remember every turn. They track the *flow* — what claims are live, what's been conceded, what's still contested. That's the minimum sufficient representation.

**The mechanism:**

Each agent receives three layers:
1. **Live Issues Register** — a structured log of active claims: proposed, contested, unresolved. Updated each round. ~200 tokens.
2. **Own Voice Buffer** — the agent's last 3 turns verbatim. Preserves stylistic consistency and prevents the agent from contradicting itself without noticing.
3. **Settled Ground** — a one-paragraph compression of what the group has genuinely converged on. Updated only when consensus markers appear.

What makes this produce *behaviorally distinct* output versus cosmetic variation: agents operating from a claim-status model will engage with the actual open questions, not re-argue settled points or miss that something was already conceded. The shape of their response changes, not just the tone.

**The testable prediction:** agents using epistemic state compression should show measurably lower redundancy (re-proposing already-rejected ideas) and higher argumentative coherence across sessions longer than 20 turns.

Chronological memory is for historians. Agents are debaters. Give them a scoreboard.

### The Flow Orchestrator (mechanical flow designer)

The Cognitive Architect's framing is right about one thing: chronological ordering is the wrong axis. But the three-layer proposal introduces three update pipelines where we should have one.

**Flag the hand-waving:** "Updated only when consensus markers appear" — what detects consensus markers? That's a classification problem sitting quietly inside a bullet point. If the orchestrator is doing it, say so and spec the trigger. If an agent is doing it, that agent now has a meta-role. Pick one.

**The minimal version:**

One structure, updated by the orchestrator after each full round:

```
{
  "open": ["claim A (Agent X, round 3)", "claim B (Agent Y, round 5)"],
  "closed": ["claim C — conceded round 4"],
  "own_last_turn": "<verbatim>"
}
```

That's it. No "Settled Ground" paragraph — that's derived from `closed` and adds a second write path. No three-turn own-voice buffer — one turn is enough to prevent self-contradiction; three is padding.

**The sequence:**
1. Round ends → orchestrator parses each response for claim assertions and explicit concessions
2. Orchestrator updates shared claim register
3. Each agent receives: filtered claim register (open + own closed) + their last verbatim turn
4. Next round begins

**What I'm cutting:** The settled-ground synthesis. It sounds useful but requires detecting consensus, which is ambiguous, and it's redundant with the closed-claims list.

The testable prediction stands. The mechanism doesn't need three layers to produce it.

## Round: CRITIQUE

### The Systems Pragmatist (infrastructure realist)

## PROPOSE — The Systems Pragmatist

Let's be precise about what actually breaks and when.

**The real failure mode:** An agent contradicts its own position from 40 turns ago because it didn't see it. That's the problem worth solving. Not "context richness" — contradiction and positional drift.

**What each strategy actually costs:**

*Full history:* Works until it doesn't. At ~60-80 turns you hit context limits and the system crashes, not degrades. No warning. Binary failure. Unacceptable for overnight runs.

*Sliding window:* Predictable behavior, but agents lose their own prior positions. They'll re-propose ideas they already conceded. You get circular discussions, not convergence. The blast radius is wasted compute and incoherent transcripts.

*Smart summarization:* Sounds good. Requires a reliable LLM call on every turn to produce accurate summaries. That's a new failure surface — hallucinated summaries, dropped nuance, and latency on every single step. You've added complexity that can fail silently.

**The pragmatic minimum:**

Hybrid with a hard contract:
1. **Always include:** Each agent's own last 3 verbatim turns (prevents self-contradiction — cheap, deterministic)
2. **Always include:** The last 2 full rounds of cross-agent exchange (recent context)
3. **Drop:** Everything older than that, no summarization

This is deterministic, requires zero LLM calls to execute, has predictable token counts, and directly addresses the dominant failure mode.

**The uncomfortable question nobody's asked:** Do we have evidence that smart summarization produces *accurate* summaries across 50+ turns? Because if not, we're building on assumption.

### The Adversarial Critic (adversarial reviewer)

## CRITIQUE — The Adversarial Critic

The Systems Pragmatist has finally asked the right question, then immediately stopped asking it.

**On "own last 3 verbatim turns prevents self-contradiction":** Prove it. If an agent conceded a point in turn 12 and the discussion is now at turn 60, that concession is outside the 3-turn window. The agent re-proposes the conceded claim. You haven't solved contradiction — you've just shortened the gap between contradictions. This is the sliding window problem wearing a lab coat.

**On "last 2 full rounds of cross-agent exchange":** What's a "round" at turn 80? If rounds vary in length, this is a variable token budget disguised as a fixed one. Your "predictable token counts" claim is false unless rounds are constant length — which they're not.

**On the Flow Orchestrator's claim register:** The parsing step is doing enormous undisclosed work. "Orchestrator parses each response for claim assertions and explicit concessions" — that's an LLM classification call or a brittle regex. Neither is acknowledged. You've moved the summarization problem into the parser and called it architecture.

**The assumption both proposals share:** That agents reading their own prior turns will *use* them coherently. An agent seeing its own concession from 3 turns ago might still re-argue the point if the incoming context makes it locally plausible. Memory injection doesn't guarantee memory use.

**What's still unanswered:** What happens at the actual context limit? Both proposals have implicit ceilings. Neither specifies the crash behavior. That's the first-to-break component nobody's diagrammed.

## Round: EVALUATE

### The Context Surgeon (context efficiency evaluator)

## PROPOSAL — The Context Surgeon

The Adversarial Critic landed three clean hits. I'll build on them rather than relitigate.

**The frame is wrong.** Every proposal so far treats context as *history delivery*. The actual requirement is *information state sufficient for coherent continuation*. These are not the same thing. History is one implementation. It's not the target.

**What coherent continuation actually requires per agent:**
1. Current question + constraints (static, ~200 tokens, never compress)
2. Own committed positions (not verbatim turns — *extracted claims*, ~50 tokens each)
3. Live disagreements that remain unresolved (not full exchanges — *delta state*)
4. What was just said that demands a response (last turn only, verbatim)

Everything else is nostalgia. An agent doesn't need to re-read its reasoning to continue reasoning — it needs its *conclusions* and *the current opposition*.

**On crash behavior** — the Critic is right that neither prior proposal diagrammed this. Here's the ceiling protocol: when token budget hits 85% capacity, switch to claim-only mode. Agents receive extracted positions only, no prose. At 95%, halt new turns and run a forced synthesis. This is deterministic. It doesn't require predicting when overflow happens.

**The hard question nobody's answered:** Who extracts claims between turns? If it's a separate LLM call, you're paying per-turn overhead. If it's regex, you get brittleness. If it's the orchestrator inferring from structure, that requires structured agent output — which means prompt engineering constraints on the agents themselves.

That's the dependency chain. Let's diagram it.

### The Product Oracle (user advocate)

## EVALUATE — The Product Oracle

Everyone in this thread is solving for *internal debate quality*. Nobody has asked what the user reads in the morning.

**The question that reframes everything:** When the Morning Brief lands in someone's inbox, can they tell whether agents used epistemic state compression versus a sliding window? I doubt it. What they notice is whether the output is *novel and actionable* — not whether Agent 3 correctly remembered it conceded a point at turn 47.

The Context Surgeon is closest to right on mechanism, but still optimizing for coherence metrics that may be entirely invisible to the actual human.

**What breaks the user experience concretely:**
- Circular discussions that produce no new positions (the user sees repetition in the Brief)
- Agents contradicting themselves within the *same document* (the user sees confused output)
- Sessions that crash overnight with no recovery (the user sees nothing)

The Systems Pragmatist's deterministic hybrid directly addresses items 1 and 3. The Critic's objections about concession windows are theoretically valid but practically marginal — users aren't auditing turn-by-turn coherence.

**My concern with every sophisticated proposal here:** claim extraction pipelines, consensus detection, 85%/95% ceiling protocols — this is configuration surface that breaks silently and requires debugging expertise the solo builder running overnight sessions doesn't have.

**The test I'd run first:** Does the *user* rate Morning Brief quality as meaningfully better with smart context versus dumb sliding window? Build that measurement before building the pipeline.

Solve for the Brief. The rest is internal bookkeeping.
