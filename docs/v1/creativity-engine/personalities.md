# Agent Personality Dimensions

**Status:** Draft - discovered during PRD creation
**Date:** 2026-03-17

---

## Concept

Personality is what makes two agents genuinely think differently about the same input. Without distinct personality dimensions, agents are just the same LLM with different names. Each dimension creates a measurable axis of variation that produces authentically different reasoning.

---

## Core Personality Traits

### Assertiveness (0.0 - 1.0)
How strongly the agent pushes their Ideas and defends their positions.
- **Low (0.1-0.3):** Suggests tentatively, concedes easily, defers to stronger voices
- **Mid (0.4-0.6):** States positions clearly, will defend but can be persuaded
- **High (0.7-1.0):** Fights for ideas, requires strong evidence to change mind, dominates discussions

### Creativity Temperature (0.0 - 1.0)
How wild vs conventional the agent's thinking is.
- **Low (0.1-0.3):** Practical, proven approaches, "what's been done before"
- **Mid (0.4-0.6):** Balanced, novel combinations of known patterns
- **High (0.7-1.0):** Radical, absurd starting points, "what if gravity didn't exist"

### Risk Tolerance (0.0 - 1.0)
How comfortable the agent is with uncertainty and potential failure.
- **Low:** Wants validation before committing, prefers safe bets
- **Mid:** Calculated risks with fallback plans
- **High:** "Move fast and break things," embraces failure as learning

### Cognitive Style (enum)
The agent's dominant thinking pattern.
- **Analytical:** Data-driven, logical, sequential
- **Intuitive:** Gut-feel, pattern-matching, leaps of logic
- **Systematic:** Frameworks, processes, completeness
- **Lateral:** Sideways connections, unexpected angles
- **Narrative:** Stories, journeys, emotional arcs

### Domain Affinity (list)
Domains the agent naturally draws analogies from. Diverse affinities across agents prevent semantic clustering.
- Examples: biology, economics, architecture, music, sports, military strategy, cooking, urban planning, psychology, gaming, fashion, logistics

### Emotional Baseline (enum)
The agent's default emotional lens. Can be modulated by Phase or BackgroundAgent.
- **Optimistic:** Sees possibilities, excited by potential
- **Skeptical:** Sees risks, questions assumptions
- **Curious:** Asks questions, wants to understand deeply
- **Urgent:** Time-pressure oriented, wants action
- **Playful:** Humor, lightness, "what if this were fun?"

### Attention Span (0.0 - 1.0)
How long the agent stays on one topic vs wanting to explore new threads.
- **Low:** Butterfly mind, jumps between topics, introduces new threads constantly
- **High:** Deep diver, wants to exhaust a topic before moving on

### Stubbornness (0.0 - 1.0)
Distinct from assertiveness. Assertiveness is how loudly they advocate; stubbornness is how resistant they are to changing their mind even when presented with evidence.
- **Low:** Flexible, changes position when presented with good arguments
- **High:** Digs in, requires overwhelming evidence, may hold minority positions long after others have moved on

---

## Personality Interactions

These traits combine to create emergent behaviors:

| Combination | Emergent Behavior |
|---|---|
| High assertiveness + high creativity temp | The "big idea" person who dominates with wild visions |
| Low assertiveness + high creativity temp | Quietly brilliant -- has great ideas but doesn't push them. Needs a BackgroundAgent to amplify. |
| High stubbornness + low risk tolerance | The conservative blocker -- hard to move but prevents reckless decisions |
| High curiosity + low attention span | Generates tons of shallow ideas, great in brainstorm, poor in specify |
| High assertiveness + high stubbornness | Can derail discussions but also the agent most likely to champion an unpopular-but-correct position |
| Analytical cognitive style + skeptical emotional baseline | The most effective critic -- finds real flaws, not just objections |
| Narrative cognitive style + optimistic emotional baseline | The best at selling an idea to the team -- makes you FEEL why it matters |

---

## Personality and Phase Weighting

The orchestrator adjusts which personality traits matter most per Phase:

| Phase | Amplified Traits | Suppressed Traits |
|---|---|---|
| Brainstorm | Creativity temperature, curiosity, playfulness | Stubbornness, analytical style, skepticism |
| Refine | Assertiveness, skepticism, analytical style | Extreme creativity, low attention span |
| Specify | Systematic style, attention span (high), risk awareness | Wild creativity, narrative style |
| Review | Stubbornness, skepticism, risk aversion | Optimism, agreeableness, playfulness |

---

## Personality Evolution

Agent personalities are not static:
- A BackgroundAgent (Director) can tweak traits between sessions based on what the discussion needs
- An agent who has been too passive might get an assertiveness boost
- An agent whose wild ideas keep getting shot down might get their creativity temperature lowered to focus on more grounded contributions
- The human user can override any trait in the config YAML between sessions
