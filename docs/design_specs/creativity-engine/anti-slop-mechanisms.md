# Anti-Slop Mechanisms

**Status:** Draft - discovered during PRD creation
**Date:** 2026-03-17

---

## The Problem

LLMs have default behaviors that produce bad brainstorming:

1. **Semantic clustering** -- ideas 2-10 are variations of idea 1
2. **Premature convergence** -- "great idea, let's go with that" after two exchanges
3. **Polite agreement** -- "that's a wonderful point" instead of genuine pushback
4. **Restating** -- rephrasing the same concept to appear productive
5. **Safe ideas** -- conventional, expected, "what a consultant would say"
6. **Sycophancy** -- agreeing with the stronger voice / more detailed argument regardless of merit
7. **List completion** -- when asked for ideas, producing a formatted list that feels complete but is shallow
8. **Token momentum** -- once the conversation heads in a direction, all agents drift the same way

These must be actively combated or the system produces expensive nothing.

---

## Mechanism 1: Domain Pivot Triggers

**Problem addressed:** Semantic clustering, token momentum

Every N contributions on a single domain, a BackgroundAgent (Curator) analyzes the recent messages for domain concentration. If 80%+ of recent ideas are in the same domain (e.g., all about UX, all about monetization), it injects a forced pivot:

"Your recent ideas have clustered around [domain]. Approach the next idea from: [random orthogonal domain]."

The pivot domain is selected to be maximally different from the current cluster.

---

## Mechanism 2: Convergence Suppression

**Problem addressed:** Premature convergence, polite agreement

During brainstorm Phase, the orchestrator monitors for convergence signals:
- Multiple agents agreeing in sequence without adding new ideas
- Decision language ("let's go with," "that settles it") before minimum idea count
- Decreasing idea diversity (measured by topic/domain spread)

When detected, the orchestrator:
- Refuses to advance Phase (IdeaCountGate)
- Injects a provocation or random stimulus via Muse BackgroundAgent
- Activates a high-creativity-temperature agent from the bench
- Explicitly instructs the next agent: "Do not agree. Find a problem with the current direction or propose something completely different."

---

## Mechanism 3: Agreement Tax

**Problem addressed:** Polite agreement, sycophancy

If an agent agrees with another agent's position, they must pay an "agreement tax" -- they can only agree if they ADD something new. Pure agreement ("great point") is flagged by the orchestrator and the agent is prompted to either:
- Extend the idea in a new direction
- Identify a risk or edge case
- Apply the idea to a different context
- Provide specific evidence or an analogy

"I agree" without addition is treated as a wasted turn.

---

## Mechanism 4: Novelty Scoring

**Problem addressed:** Restating, list completion, shallow ideas

A BackgroundAgent (Oracle type) periodically scores recent ideas against all previous ideas in the discussion for semantic similarity. Ideas that are >0.85 similar to existing ideas get flagged. The flag goes into the DiscussionAgent's AgentMind as: "Your last idea was too similar to [existing idea]. Your next contribution must be from a different angle."

This doesn't block the agent -- it makes them aware they're repeating, which changes their next output.

---

## Mechanism 5: Devil's Advocate Duty

**Problem addressed:** Polite agreement, token momentum, safe ideas

At any point, one agent in each team has "Devil's Advocate Duty" -- their job is to argue against the current consensus regardless of their personal position. This rotates. The agent on DA duty gets a prompt addition: "For this turn, your job is to find the strongest argument AGAINST the direction the team is heading. Even if you agree, argue against."

This ensures at least one voice is always pushing back.

---

## Mechanism 6: Perspective Enforcement

**Problem addressed:** All agents reasoning the same way despite different personas

Before each turn, the orchestrator reminds the agent of their Position and Personality:
"You are [Name], the [Position]. You care about [what drives them]. Your cognitive style is [style]. Respond from YOUR perspective, not the group's."

This is more than a system prompt -- it's a per-turn injection that fights the LLM's tendency to blend into the conversation's dominant voice.

---

## Mechanism 7: Surprise Audits

**Problem addressed:** Gradual quality degradation over long sessions

Every N turns, a BackgroundAgent (Specter) does a "surprise audit" -- it reads the last 10 messages and scores them on:
- **Genuine diversity:** Are agents actually saying different things?
- **Substantive content:** Is each message adding real value or padding?
- **Position authenticity:** Are agents staying true to their stakeholder positions?
- **Novelty:** Are new ideas still emerging or is the conversation recycling?

If scores drop below threshold, the Specter triggers interventions:
- Bench swap (rotate in fresh agents)
- Technique rotation (switch active creativity technique)
- Provocation injection
- Forced context reset (start fresh with a briefing instead of continuing degraded context)

---

## Mechanism 8: Uncomfortable Idea Quota

**Problem addressed:** Safe ideas, conventional thinking

Each agent has a periodic requirement to produce at least one idea that makes the OTHER team uncomfortable. Not offensive -- genuinely challenging to their assumptions. "What if we didn't need users at all?" "What if the free tier was the only tier?" "What if the product was intentionally hard to use?"

The quota is tracked in the AgentMind. If an agent hasn't produced an uncomfortable idea in N turns, they get prompted to do so.

---

## Mechanism 9: Silence as Signal

**Problem addressed:** All agents feeling obligated to contribute to every topic

Not every agent needs to speak every turn. If an agent's Position and expertise aren't relevant to the current topic, they should stay silent (remain on bench). Forced contributions on topics outside an agent's domain produce generic filler.

The bench system handles this -- but the key insight is that silence is a FEATURE, not a bug. A customer agent who stays quiet during a business model discussion is more authentic than one who offers a tepid "sounds reasonable."

---

## Mechanism 10: Post-Hoc Diversity Check

**Problem addressed:** Subtle homogenization over time

After each session, a BackgroundAgent analyzes the full set of Ideas generated and measures:
- Domain distribution (are ideas spread across many domains or clustered?)
- Position attribution (did all positions contribute meaningfully?)
- Argument diversity (are there genuine opposing positions or did everyone converge?)
- Surprise factor (how many ideas would be unexpected to a human reader?)

This report goes into the session analysis and informs the next session's agent configuration -- if the discussion was too homogeneous, the Director BackgroundAgent adjusts agent traits or adds new agents to increase diversity.
