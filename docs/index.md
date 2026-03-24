# Documentation Index

Reading guide for the AgentTeamDiscussions design documentation.

---

## Start Here

1. **[design_specs/prd.md](design_specs/prd.md)** -- Product requirements document. Defines the problem, user journeys, and success criteria. Read this first.

2. **[design_specs/entity-model.md](design_specs/entity-model.md)** -- Data model. The nouns of the system: sessions, teams, agents, turns, phases, artifacts. Read after the PRD to understand the domain.

---

## How Conversations Work

3. **[design_specs/conversation-engine/design-decisions.md](design_specs/conversation-engine/design-decisions.md)** -- Synthesized design decisions from beta testing. Covers the turn model, phase transitions, anti-slop, AgentMind, bench system, cross-team communication, and user input. The authoritative "what we decided and why" document.

4. **[design_specs/conversation-engine/turn-anatomy.md](design_specs/conversation-engine/turn-anatomy.md)** -- Requirements spec for the Turn: context layers, turn types, output signals, perspective reminders, positional awareness, and deliberation budgets.

---

## How Agents Think Differently

5. **[design_specs/creativity-engine/index.md](design_specs/creativity-engine/index.md)** -- Index for the creativity engine specs. Covers techniques, personalities, positions, anti-slop mechanisms, phase dynamics, and applied research.

---

## Session Platform & Agent Management

7. **[design_specs/session-platform-and-agent-management.md](design_specs/session-platform-and-agent-management.md)** -- Agent library (three-tier storage), session-as-package format, interactive setup flow, mode-as-plugin system, and post-session feedback loop. The usability and management layer.

---

## Beta Testing Artifacts

6. **[beta-agent-output/known-issues.txt](beta-agent-output/known-issues.txt)** -- Diagnostic notes from beta agent runs. Known behavioral problems observed during testing.

Raw test output files live in `../projects/beta-agent-interaction/output/`.

---

## Directory Structure

```
docs/
    index.md                              # This file
    design_specs/
        prd.md                            # Product requirements
        entity-model.md                   # Data model
        session-platform-and-agent-management.md  # Session platform spec
        agent-creation-guide.md           # Agent YAML reference
        v1-orchestrator-spec.md           # V1 orchestrator design
        creativity-engine/                # How agents think differently
            index.md
            personalities.md
            positions.md
            techniques.md
            anti-slop-mechanisms.md
            phase-dynamics.md
            research-applied.md
            RESEARCH-PROMPT.md
            ResearchResults/
        conversation-engine/              # How conversations work
            design-decisions.md
            turn-anatomy.md
            agent-behavior-mechanisms.md
            moderator-input.md
            rebuttal-priority.md
    beta-agent-output/                    # Test run artifacts
        known-issues.txt
```
