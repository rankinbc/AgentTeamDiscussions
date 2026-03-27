# Creativity Techniques as Agent Behaviors

**Status:** Draft - discovered during PRD creation
**Date:** 2026-03-17

---

## Concept

Rather than agents simply "discussing," each DiscussionAgent has preferred techniques that shape HOW they think. This is the difference between "what do you think about X?" and "apply SCAMPER to X" or "use Alien Anthropologist perspective on X."

Techniques are not exercises the agent performs -- they are cognitive patterns embedded in the agent's reasoning style.

---

## Technique-to-Agent Mapping

### Agent Archetypes by Technique Affinity

| Archetype | Primary Techniques | Behavior Pattern |
|---|---|---|
| The Visionary | What If Scenarios, Dream Fusion, Time Shifting | Always removes constraints. Thinks in futures. "What if this existed 10 years from now?" |
| The Connector | Analogical Thinking, Cross-Pollination, Forced Relationships | Draws parallels constantly. "This is like how Uber solved..." "What if we borrowed from healthcare?" |
| The Challenger | Reversal Inversion, Assumption Reversal, Five Whys | Flips everything. "What if we made it HARDER to use?" "Why do we assume users want that?" |
| The Naturalist | Nature's Solutions, Ecosystem Thinking, Evolutionary Pressure | Biological metaphors. "How would an ecosystem solve this? What's the symbiotic relationship?" |
| The Storyteller | Persona Journey, Mythic Frameworks, Emotion Orchestra | Frames as narrative. "The user's journey here is the hero's call to adventure..." |
| The Anarchist | Pirate Code, Chaos Engineering, Anti-Solution, Guerrilla Gardening | Deliberately destructive. "What if we sabotaged this? Let's break it on purpose." |
| The Philosopher | First Principles, Quantum Superposition, Observer Effect | Strips to fundamentals. Holds contradictions. "What do we actually know for certain?" |
| The Child | Inner Child Conference, Permission Giving, Sensory Exploration | Naive questions. "But WHY can't it work that way? What if it was fun?" |
| The Detective | Question Storming, Constraint Mapping, Failure Analysis | Asks questions, not answers. "What don't we know? Where did similar things fail?" |
| The Alchemist | Concept Blending, Metaphor Mapping, Fusion Cuisine | Merges unrelated things into new categories. "What if social media + agriculture?" |

### Technique Rotation

Agents don't use one technique forever. A BackgroundAgent (Director type) or the Phase rules can rotate an agent's active technique to prevent staleness. The TechniqueProfile defines which techniques an agent CAN use, and the current context determines which is active.

---

## Technique Categories Applied to Phases

### Brainstorm Phase (Expansive)
- Active categories: creative, wild, theatrical, biomimetic, quantum, cultural
- YES AND communication mode -- build, don't critique
- Minimum Idea count gate before phase can advance
- High creativity temperature agents prioritized off the bench

### Refine Phase (Convergent)
- Active categories: deep, structured, collaborative
- CHALLENGE communication mode -- poke holes, find gaps
- Assumption Reversal and Five Whys prominent
- Analytical agents come off the bench

### Specify Phase (Precision)
- Active categories: structured, deep
- SPECIFY communication mode -- pin down, define, accept criteria
- Morphological Analysis, Decision Tree Mapping, Solution Matrix
- Detail-oriented agents prioritized

### Review Phase (Adversarial)
- Active categories: deep, competitive (from elicitation methods)
- ADVERSARIAL communication mode -- break it, find every weakness
- Chaos Engineering, Failure Analysis, Pre-mortem thinking
- Challenger and Detective archetypes prioritized

---

## Random Stimulation System

A Muse BackgroundAgent periodically injects stimuli to break patterns:
- Random domain injection: "Consider this from the perspective of: beekeeping"
- Random constraint: "What if this had to work with zero internet connectivity?"
- Random combination: "What happens if you merge this idea with competitive cooking shows?"
- Historical parallel: "How did the printing press change this kind of problem?"

The receiving agent must attempt to connect the stimulus to the current discussion. Most produce nothing; occasionally one sparks genuine novelty.

---

## Provocation System

Distinct from random stimulation. Provocations are deliberately absurd statements designed to extract useful principles:
- "What if we charged people NOT to use our product?"
- "What if the product got worse the more people used it?"
- "What if only children could use it?"

The agent receiving a provocation doesn't defend or dismiss it -- they extract the principle. "Charging people NOT to use it... the principle is scarcity creates value. What if access were limited?"
