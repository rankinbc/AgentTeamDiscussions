# Session Platform & Agent Management Design Spec

**Status:** Draft
**Date:** 2026-03-24
**Pillar:** Session Platform (with Agent pillar additions)

---

## Overview

This spec covers the usability and management layer for AgentTeamDiscussions -- the systems that wrap around the existing conversation mechanics to make discussions easier to set up, more productive to run, and more useful to learn from.

It introduces five new subsystems:

1. Agent Library (three-tier storage with metadata and discovery)
2. Session-as-Package (self-contained, reproducible session format)
3. Interactive Setup Flow (guided session creation)
4. Mode-as-Plugin (composable feature system for discussion configuration)
5. Post-Session Feedback Loop (structured learning across sessions)

This spec does NOT duplicate existing design docs. It references them where the systems connect.

### Relationship to Other Specs

- **prd.md** defines the product vision and user journeys. This spec implements Journey 1 (Idea Submitter -- the setup flow) and Journey 4 (System Tuner -- feedback loop and mode configuration). It also provides the management infrastructure that all journeys depend on.
- **v1-orchestrator-spec.md** defines the current V1 scope, which explicitly excludes MCP, two-team separation, background agents, and phases. This spec is designed to work with V1's single-team model today and scale to the full architecture later. Features in mode.yaml that depend on unimplemented systems (bench, background research, inner deliberation) ship as `enabled: false`.
- **entity-model.md** defines DiscussionAgent as a GUID-bearing entity with AgentMind. The agent library in this spec stores agent *definitions* (templates), not agent *instances*. When a library agent is used in a session, it becomes an instance with its own AgentMind state for that session. The library agent is the blueprint; the session agent is the living thing.

---

## Four-Pillar Architecture

The project is organized into four pillars. This spec primarily covers the **Session Platform** pillar and additions to the **Agents** pillar.

| Pillar | Owns | Key Docs |
|---|---|---|
| **Agents** | Definition, AgentMind (ideas, magnitudes, stances), personality, evolution | entity-model.md, agent-creation-guide.md, creativity-engine/personalities.md |
| **Environment** | Between-round events, background agents (Curator, Muse, Director, etc.), external influence on AgentMind, moderator input | creativity-engine/anti-slop-mechanisms.md, conversation-engine/agent-behavior-mechanisms.md |
| **Discussion System** | In-round mechanics: turns, phases, signals, anti-slop, context windows, bench rotation, cross-team communication | conversation-engine/design-decisions.md, conversation-engine/turn-anatomy.md, creativity-engine/phase-dynamics.md |
| **Session Platform** | Setup, lifecycle, mode config, feedback, output, agent library | **This spec** |

**Boundary rules:**
- Discussion System owns what happens DURING rounds.
- Environment owns what happens BETWEEN rounds.
- Both read/write AgentMind (owned by Agents) through defined interfaces.
- Session Platform is the container everything runs in.

---

## 1. Agent Library

### Problem

Agent definitions currently live scattered across team YAML files in `projects/beta-agent-interaction/config/teams/`. There's no way to discover, reuse, or share agents across sessions. Claude can't recommend agents from past sessions because there's no indexed catalog.

### Three-Tier Storage

| Tier | Location | Git-tracked | Purpose |
|---|---|---|---|
| System | `agents/system/` | Yes | Agents designed for improving AgentTeamDiscussions itself |
| Common | `agents/common/{category}/` | Yes | General-purpose archetypes useful across many topics |
| User | `agents/user/{category}/` | No (.gitignored) | Per-user agents, promoted from sessions or hand-crafted |

### Agent File Format

Each library agent file is the existing YAML agent definition (per agent-creation-guide.md) plus a metadata header:

```yaml
meta:
  id: systems-pragmatist
  category: product-design
  tags: [infrastructure, failure-analysis, distributed-systems, skeptic]
  source_session: null           # null = hand-crafted, or session ID if promoted
  quality_notes: "Strong critic role. Works well paired with creative proposers."
  created: 2026-03-17
  last_used: 2026-03-18
  times_used: 4

# Standard agent definition follows (name, description, personality, position, etc.)
```

### Index

`agents/index.yaml` is auto-generated from individual agent files. It contains agent ID, name, tier, category, tags, and quality_notes for each agent. This is a convenience for quick browsing and Claude's search -- not a source of truth.

### Key Behaviors

- Agents are **copied** into sessions, never referenced by pointer. Editing a library agent does not affect past sessions.
- Categories are folders. One agent, one category. Tags allow cross-cutting discovery.
- Claude uses the index + tags + quality_notes + past session-review.yaml files when recommending agents.

### Promotion Flow

All auto-generated or session-specific agents live only in the session package. A user can explicitly promote an agent to the library:
1. User requests promotion (e.g., "save Marcus to my library")
2. Claude copies the agent definition from the session, adds metadata, applies any tweak suggestions from session feedback
3. Agent is written to `agents/user/{category}/`
4. Index is regenerated

---

## 2. Session-as-Package

### Problem

Sessions are currently output-only folders. They don't capture the inputs that produced them, making sessions non-reproducible and hard to learn from.

### Package Structure

```
/sessions/
  {timestamp}_{topic-slug}/
    config/
      brief.yaml                # Topic, goals, constraints, challenges, sparks
      team.yaml                 # Full agent definitions (snapshot from library or generated)
      mode.yaml                 # Discussion mode with feature toggles
    output/
      transcript.md             # Full conversation
      decisions.md              # Extracted decisions/outcomes
      artifacts/                # Generated specs, PRDs, etc.
    feedback/
      user-feedback.md          # Raw debrief notes
      session-review.yaml       # Structured review (see Section 5)
```

### brief.yaml

```yaml
topic: "What should the pricing model be for an AI mixing assistant?"
discussion_type: decision        # decision | exploration | critique | spec-building
urgency: high                    # low | medium | high | critical
goals:
  - "Identify the primary revenue model"
  - "Stress-test willingness to pay"
constraints:
  - "Target audience is bedroom producers, not studios"
sparks:
  - "What if the free tier IS the product?"
challenges:
  - "The free tier question must be resolved, not deferred"
  - "Someone must argue the case for no free tier at all"
success_criteria:
  - "Team converges on ONE pricing model with rationale"
  - "At least two alternatives considered and rejected with reasons"
deliverables:
  - type: decision
    description: "Primary revenue model"
    required: true
  - type: document
    description: "Pricing rationale one-pager"
    required: false
```

`discussion_type` shapes the flow:
- **decision** -- must end with a committed choice, dissent recorded
- **exploration** -- divergent thinking, no commitment required
- **critique** -- input is an existing proposal, output is problems and recommendations
- **spec-building** -- produce a structured document section by section

`urgency` tells the orchestrator how aggressive to be with productivity mechanisms. Low urgency gets gentle nudges. Critical gets deadline pressure, forced commitments, and stakes escalation.

`challenges` are forcing functions. If unaddressed by midway, the orchestrator surfaces them explicitly.

### team.yaml

Full agent definitions snapshotted at session creation. Same schema as agent-creation-guide.md. This ensures sessions are self-contained -- agent library changes don't affect past sessions.

### Relationship to Existing Docs

- The turn mechanics inside a session are governed by conversation-engine/design-decisions.md and conversation-engine/turn-anatomy.md.
- Phase progression follows creativity-engine/phase-dynamics.md.
- Between-round activities follow the pipeline documented in proposed_design_docs/07-* and 08-*.
- The session package is the container; the existing specs govern what happens inside it.

---

## 3. Interactive Setup Flow

### Problem

Setting up a discussion requires writing 100+ line YAML files per agent, composing a brief, and running specific Python commands. This friction prevents experimentation.

### Entry Point

`python setup.py` (or integrated into existing CLI)

### Flow

**Step 1 -- Topic.** Claude asks: "What do you want your agents to discuss?" User provides anything from one sentence to a detailed brief. Claude expands it into the `brief.yaml` structure and shows it back for confirmation.

**Step 2 -- Discussion Type & Urgency.** Claude presents the four types with plain-language descriptions. Asks about urgency. These populate `brief.yaml` and inform `mode.yaml` defaults.

**Step 3 -- Challenges & Success Criteria.** Claude proposes challenges and success criteria based on the topic. User can accept, edit, or add their own.

**Step 4 -- Team Composition.** Claude proposes agent roles based on topic and discussion type. Shows candidates from the library. Offers to generate agents for gaps. User can:
- Pick and customize roles
- Say "you decide" -- Claude optimizes the full team for productive discussion (conflicting drives, diverse cognitive styles, mixed job types per agent-creation-guide.md Section 10)

**Step 5 -- Mode & Productivity.** Claude proposes a `mode.yaml` based on discussion type and urgency. Defaults are tuned by type. Power users can toggle features.

**Step 6 -- Review & Launch.** Claude shows the complete session package. On approval, writes to `/sessions/` and optionally starts the discussion.

### The Fast Path

"You decide" through steps 3-5 means a user can go from topic to running session with two inputs: the topic and "you decide."

### Claude's Recommendations

During setup, Claude searches:
- Agent library (all three tiers) for role matches
- Past `session-review.yaml` files for relevant signal (topic similarity, agent track record, mode tuning lessons)
- Applies tweak suggestions from past feedback automatically (with disclosure)

---

## 4. Mode-as-Plugin System

### Problem

Discussion modes are currently implicit in the code. Adding new features (background research, inner deliberation, bench rotation) requires code changes. There's no way for users to compose features or create custom modes.

### mode.yaml

A mode is a composition of independently toggleable features:

```yaml
name: "structured-decision"
description: "Phased discussion driving toward a committed decision"
base: structured                    # structured | freeform

phases:
  enabled: true
  sequence:
    - name: diverge
      rounds: 5
      goal: "Generate distinct approaches. No convergence allowed."
    - name: challenge
      rounds: 5
      goal: "Attack each approach. Find the fatal flaws."
    - name: converge
      rounds: 5
      goal: "Pick one. Defend your choice against the critics."
    - name: commit
      rounds: 5
      goal: "Finalize. Resolve remaining objections or record dissent."

features:
  urgency_injection:
    enabled: true
    escalation: linear

  deadline_pressure:
    enabled: true
    starts_at_phase: converge

  stale_detection:
    enabled: true
    threshold_rounds: 3

  force_commitment:
    enabled: true
    starts_at_phase: converge
    format: "I advocate for [X] because [Y]"

  devil_rotation:
    enabled: true

  challenge_surfacing:
    enabled: true

  dissent_recording:
    enabled: true

  perspective_shift:
    enabled: true
    trigger: stale

  stakes_escalation:
    enabled: true

  concrete_scenario:
    enabled: true

  # Future features (disabled until implemented)
  background_research:
    enabled: false
    description: "Between rounds, designated agents research specific questions"

  inner_team_deliberation:
    enabled: false
    description: "Team huddles between cross-team rounds"

  agent_research_task:
    enabled: false
    description: "Individual agent does focused research that updates their stance"

  bench_system:
    enabled: false
    description: "Agents rotate on/off active roster based on phase and signal quality"
```

### How It Works

- The orchestrator iterates over `features`, skips `enabled: false`, activates the rest.
- Each feature is self-contained with its own trigger logic and config.
- New features plug in by adding a block -- no mode schema changes needed.
- When a future feature gets implemented, users flip `enabled: true` and add config.

### Bundled Templates

```
/config/modes/
  freeform-exploration.yaml       # Minimal features, max divergence
  structured-decision.yaml        # Full productivity stack
  adversarial-critique.yaml       # Heavy on challenge mechanisms
  spec-building.yaml              # Section-by-section document production
```

Users and Claude can create new templates. The interactive setup starts from a template and customizes.

### Relationship to Existing Docs

The features in mode.yaml map to mechanisms already designed in the existing specs:
- Phase sequence and dynamics: creativity-engine/phase-dynamics.md
- Urgency and challenge mechanics: conversation-engine/rebuttal-priority.md
- Anti-slop interventions: creativity-engine/anti-slop-mechanisms.md
- Bench system: entity-model.md, creativity-engine/phase-dynamics.md
- Inner deliberation: conversation-engine/turn-anatomy.md, proposed_design_docs/05-*
- Between-round activities: proposed_design_docs/07-*, 08-*

The mode system doesn't redesign these mechanisms -- it provides a configuration layer to toggle and compose them per session.

---

## 5. Post-Session Feedback Loop

### Problem

Sessions produce output but no learning. There's no way to capture what worked, what didn't, or how to improve future runs. Team compositions and mode settings are tuned by trial and error with no memory.

### Trigger

After a session completes, Claude offers a debrief: "Want to review how that went?"

User can also initiate: `python review.py <session-id>`

### Debrief Conversation

Freeform. Claude reads the session output and asks:
- How useful was the outcome?
- Did any agent surprise you or disappoint you?
- Did the discussion get stuck anywhere?
- Would you run this team again on a different topic?

### Output Artifacts

**feedback/user-feedback.md** -- raw debrief notes.

**feedback/session-review.yaml** -- structured data:

```yaml
session_id: 2026-03-24_2100_music-tool-pricing
overall_rating: 3
outcome_quality: "Good decision reached but took too long"

team_review:
  marcus:
    rating: 4
    strengths: "Kept discussion grounded in real producer behavior"
    weaknesses: null
    tweak_suggestions: null
  keiko:
    rating: 2
    strengths: "Represented the target user well"
    weaknesses: "Too agreeable, folded under pressure"
    tweak_suggestions:
      assertiveness: 0.5
      stubbornness: 0.4

mode_review:
  phases_worked: true
  stuck_points:
    - phase: challenge
      description: "Free vs paid debate went circular for 4 rounds"
  feature_notes:
    stale_detection: "Fired too late, should trigger after 2 rounds"
    concrete_scenario: "The cancelled-user scenario was the turning point"

reuse:
  same_team_different_topic:
    recommended: true
    good_for: "Any consumer pricing or market fit discussion"
  same_topic_different_team:
    suggested: "Add a technical agent to discuss implementation cost impact on pricing"
  agent_promotions:
    - agent: marcus
      reason: "Strong archetype for any consumer product discussion"
      suggested_category: "product-design"
```

### How Claude Uses Feedback

During interactive setup (Section 3), Claude searches past session-review.yaml files:
- **Topic similarity** -- "You discussed pricing before. That team worked well except Keiko was too passive."
- **Agent track record** -- "Marcus has been rated 4+ across three sessions on consumer topics."
- **Mode tuning** -- "Last time stale_detection triggered too late. I've set the threshold to 2 rounds."
- **Tweak suggestions** -- "You suggested bumping Keiko's assertiveness last time. Want me to apply that?"

### Agent Promotion

The `agent_promotions` field in session-review.yaml feeds the library workflow. When a user says "save Marcus," Claude copies the definition with tweaks applied into `agents/user/{category}/` with metadata including the source session.

---

## Scope Boundaries

### What this spec covers
- Agent library storage, metadata, discovery, and promotion
- Session package format and lifecycle
- Interactive setup flow
- Mode configuration as composable features
- Post-session feedback capture and forward propagation

### What this spec does NOT cover
- In-round conversation mechanics (see conversation-engine/)
- Between-round event pipeline (see proposed_design_docs/07-*, 08-*)
- Agent personality dimensions and AgentMind internals (see entity-model.md, creativity-engine/)
- Background agent types and behaviors (see creativity-engine/anti-slop-mechanisms.md)
- Anti-slop mechanisms (see creativity-engine/anti-slop-mechanisms.md)
- Phase transition logic (see creativity-engine/phase-dynamics.md)

### Future: Multi-Team Discussions

The existing design docs (conversation-engine/design-decisions.md, turn-anatomy.md) specify a two-team architecture (Team A and Team B with MCP message broker). This spec's session package and mode system are designed to be compatible with that model but do not yet address N-way team discussions (3+ teams).

Design decisions that should NOT accidentally close the door on multi-team:
- **team.yaml** currently holds one flat set of agents. When two-team is implemented, this becomes a list of teams, each with their own agents. The schema should allow for this without breaking single-team sessions.
- **mode.yaml phases** assume a back-and-forth turn cycle. Multi-team would need different turn routing (round-robin between teams, free-for-all, or topic-based routing).
- **Feedback** (session-review.yaml) reviews agents individually. Multi-team would also need team-level assessment (which team was more productive, how did cross-team dynamics work).
- **Interactive setup** (Step 4) currently composes one team. Multi-team setup would need to compose multiple teams with intentional inter-team tension.

None of this needs to be built now. The current spec works for single-team discussions and is forward-compatible with two-team once the MCP server and orchestrator support it. This note exists to prevent design choices that would make multi-team harder later.

### Deliberate omissions (YAGNI)
- No automatic agent promotion -- always user-initiated
- No cross-session agent memory -- continuity comes from session packages and feedback files
- No mode editor UI -- modes are YAML files
- No rating aggregation or dashboards -- Claude reads raw session-review files
- No agent versioning beyond what git provides for tracked tiers
