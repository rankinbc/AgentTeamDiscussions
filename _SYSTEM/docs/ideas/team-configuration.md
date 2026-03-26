# Team Configuration

> **V2 Concept** — V1 uses agent configuration (YAML-defined agents in a single group). This document describes the V2 multi-team layer that builds on top of agent configuration.

## What It Is

Team Configuration extends agent configuration into a multi-team system. Where V1 defines a group of agents that participate in structured rounds, V2 Team Configuration organizes agents into separate teams with independent context windows, internal deliberation channels, and cross-team communication rules.

## Why It Exists

V1's single-group structure gets productive tension from role-based rounds (propose/critique/evaluate). But some discussions benefit from genuine information asymmetry — a product team and an engineering team developing positions independently before negotiating. Team Configuration makes this possible without code changes.

## How It Would Fit the System

Team Configuration sits upstream and feeds into multiple V2 components:

- **Feeds Creativity Engine**: Per-team personality and anti-slop configurations
- **Feeds Conversation Engine**: Team composition determines cross-team turn-taking and deliberation budgets
- **Defines Discussion Agents**: Agents belong to teams, which determines their visibility and communication boundaries
- **Configures MCP Message Broker**: Team definitions establish which agents share internal channels
- **Informs Context Management**: Team membership determines what messages an agent can see

## Core Responsibilities

### Agent Definition
Each agent in a team YAML file specifies:

- **Identity**: Name, description, role within the team
- **Personality**: 8+ scalar traits that shape behavior (assertiveness, creativity, risk tolerance, etc.)
- **Position**: What drives them, what they push back on, intensity of convictions
- **Technique**: Primary thinking approach and specific behavioral rules
- **Anti-slop**: Per-agent settings for agreement tax, perspective enforcement, idea quotas
- **Voice**: Tone, vocabulary hints, phrases to avoid, brevity level
- **Output**: Operating level (requirements/design/implementation) and job type (propose/critique/evaluate)

### Team Composition
Teams are designed as ensembles. The agents within a team should collectively cover:
- Multiple thinking styles (analytical, creative, pragmatic, adversarial)
- Multiple value orientations (user-first, system-first, risk-aware, innovation-driven)
- Complementary roles (proposers, critics, evaluators, synthesizers)

A well-configured team produces productive tension. A poorly configured one either agrees on everything or argues without progress.

### Discussion Briefs
Alongside team configuration, the system accepts discussion briefs — the input material that seeds the conversation:
- High-level idea descriptions
- Open questions to resolve
- Constraints and context
- Prior decisions or existing requirements

### Idea Seeds
Reusable idea files that can be referenced from team configs. A user can maintain a library of product ideas and pair any idea with any team configuration.

## Configuration Examples

The system ships with 5 example teams demonstrating range:

| Team | Agents | Domain | Style |
|---|---|---|---|
| beta-agents | 7 | Platform self-design | Technical, adversarial, mechanism-focused |
| game-data-pipeline | 5 | Game data cataloging | Analytical, schema-obsessed, practical |
| normal-people | 6 | Music production tools | Realistic personas, consumer perspective |
| tmos-dreamers | 5 | Retro game remake | Nostalgic, creative, scope-conscious |
| spec-builders | 5 | NES RPG remake | Design-focused, constraint-aware |

## Key Design Constraints

- **YAML only**: No code required to create or modify teams. Anyone who can edit a text file can configure a discussion
- **Self-contained**: A team config file + a brief must contain everything needed for an autonomous session
- **Validated on load**: Configuration is parsed into Pydantic models with validation — catch errors before a multi-hour run starts
- **Extensible without code changes**: New personality traits, techniques, or output modes can be added by extending the YAML schema

## Interactions

| Component | Relationship |
|---|---|
| Creativity Engine | Consumes personality, position, technique, anti-slop, and voice definitions |
| Conversation Engine | Consumes team composition and agent role assignments |
| Discussion Agents | Each agent is instantiated from its YAML definition |
| Context Management | Team structure informs visibility boundaries |
| MCP Message Broker | Team definitions establish channel membership |
| Session Platform | Config snapshot saved with each session for reproducibility |

## V1 Agent Configuration (Current)

V1 has a working YAML-to-prompt pipeline: agent configs are loaded, validated via Pydantic, and synthesized into system prompts by the prompt builder. Five example agent groups demonstrate the configuration range. The schema supports all personality, position, technique, anti-slop, and voice parameters described above.

The multi-team layer (separate teams, independent context, spokesperson model, cross-team channels) is V2 scope, dependent on the MCP Message Broker.
