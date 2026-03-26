# Creativity Engine

## What It Is

The Creativity Engine is the subsystem that makes AI agents produce genuinely different, non-convergent output. It encompasses the personality model, anti-slop mechanisms, voice constraints, and cognitive techniques that prevent the default LLM behavior of polite agreement and homogeneous responses.

## Why It Exists

LLMs have a fundamental problem in multi-agent discussions: they converge. Without active countermeasures, six agents with different system prompts will produce six variations of the same safe, consensus answer. This defeats the entire purpose of having multiple agents.

The Creativity Engine exists to solve this. It's the difference between "six AIs that agree" and "a team that actually debates."

For overnight unmonitored operation, this is critical. There's no human to nudge the conversation when it goes stale. The Creativity Engine must autonomously maintain productive tension and idea diversity across hours of discussion.

## How It Fits the System

The Creativity Engine defines *how agents think and express themselves*. It doesn't control *when* they speak (that's the Conversation Engine) or *what context they see* (that's Context Management). It controls the character, perspective, and behavioral constraints of each agent's output.

- **Fed by agent configuration**: Personality traits, positions, techniques, and voice rules come from YAML configs
- **Enforced by Conversation Engine**: Anti-slop rules are checked at turn boundaries; the engine can inject forcing functions when creativity drops
- **Shapes Discussion Agents**: Each agent's system prompt is built from Creativity Engine parameters
- **Observable by Session Platform**: Creativity signals (novelty, stance diversity) feed into session health metrics

## Core Responsibilities

### Personality Model
Eight scalar dimensions (0.0-1.0) that shape agent behavior:
- **Assertiveness**: How forcefully they state positions
- **Creativity Temperature**: How wild vs. grounded their ideas are
- **Risk Tolerance**: Appetite for unconventional approaches
- **Cognitive Style**: Analytical vs. intuitive thinking
- **Emotional Baseline**: Measured vs. passionate expression
- **Attention Span**: Deep-dive vs. breadth-first exploration
- **Stubbornness**: How easily they yield ground
- **Idea Receptivity**: Openness to building on others' ideas

These traits are translated into natural language behavioral descriptions in the system prompt — not exposed as numbers to the agent.

### Positional Framing
Each agent has a role-based position that creates authentic motivation:
- What **drives** them (e.g., "proving mechanisms actually work at scale")
- What they **push back on** (e.g., "complexity that doesn't earn its keep")
- **Intensity** level of their convictions

This creates genuine disagreement because agents are motivated by different values, not just instructed to disagree.

### Anti-Slop Mechanisms
Active countermeasures against LLM consensus drift:
- **Agreement Tax**: Agents must contribute something new if they agree with a prior point — no "I agree, and..." without substance
- **Perspective Enforcement**: Stay in character; don't drift toward generic helpful AI
- **Devil's Advocate Duty**: Rotating obligation to challenge the prevailing direction
- **Uncomfortable Idea Quota**: Required novel/contrarian ideas per turn
- **Domain Pivot Trigger**: When discussion gets stuck, agents must pull from outside domains

### Cognitive Techniques
Each agent has a primary thinking approach mapped to their archetype:
- Cross-pollination (steal ideas from other domains)
- Failure-mode analysis (think about what breaks)
- Constraint-based creativity (work within limits)
- First-principles reasoning (rebuild from fundamentals)

### Voice Constraints
Per-agent voice rules that maintain distinctiveness:
- **Tone**: Professional, casual, provocative, measured
- **Vocabulary hints**: Domain-specific language the agent naturally uses
- **Anti-patterns**: Phrases the agent must never use (e.g., "As an AI", "Great point!")
- **Brevity level**: How concise vs. expansive the agent is

## Key Design Constraints

- All creativity shaping happens through prompt engineering — no fine-tuning or model modification
- Personality traits must produce *measurably different* output, not just cosmetic variation
- Anti-slop mechanisms must work without human monitoring for 8+ hours
- The system must prevent both convergence (everyone agrees) and divergence chaos (no productive direction)

## Interactions

| Component | Relationship |
|---|---|
| Agent Configuration (YAML) | Source of all personality, position, technique, and voice parameters |
| Discussion Agents | Agents are the runtime expression of Creativity Engine rules |
| Conversation Engine | Enforces anti-slop at turn boundaries; can trigger interventions |
| Context Management | Perspective reminders injected into context to fight identity drift |
| Session Platform | Creativity health metrics feed session monitoring |

## Current State

V1 implements the full personality model (8 traits), positional framing, anti-slop mechanisms (5 types), voice constraints, and cognitive techniques. These are proven across 14 experiment runs with measurably different agent outputs. Experiment modes (competitive, counter-proposal, lean) tested different creativity configurations.
