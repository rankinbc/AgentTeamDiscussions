# Agent Identity and Resolution

**Status:** Design intent — captures constraints for future implementation
**Date:** 2026-03-26

## Problem

Agents are currently file-only (`_SYSTEM/data/discussionAgents/{team}__{key}.yaml`). The engine loads them via `AgentLoader` at session start and caches them. This works for curated agents but prevents:

- Generating agents on the fly (LLM-generated, UI-created, API-sourced, engine-spawned)
- Evolving agents over time based on evaluation feedback or manual tuning
- Mixing ephemeral and persistent agents in the same session

## Core Principle

**The engine consumes `AgentConfig` objects — it should not care where they come from.** The file system is one source, not the only one.

## Agent Identity Model

Every agent gets a unique identity:

- **Saved agents** — stable GUID stored in their YAML file, persists across sessions
- **Ephemeral agents** — GUID generated at creation time, lives only for the session
- **Evolved agents** — keep their original ID as they change, enabling lineage tracking

The `id` field is the primary key. The `key` field (e.g., `cognitive_architect`) remains as a human-readable label but is not the identity.

## Agent Sources

The engine should accept agent configs from any source. A resolution layer sits between the caller and the engine:

| Source | Example | Persistence |
|--------|---------|-------------|
| YAML files | `_SYSTEM/data/discussionAgents/` | Saved, versioned |
| LLM generation | "Create a devil's advocate for this topic" | Ephemeral or saved |
| UI form | Agent Workshop web interface | Saved on submit |
| API call | External system provides agent config | Ephemeral |
| Engine-spawned | Engine creates a specialist mid-session | Ephemeral |
| Session snapshot | Replay a prior session's exact agents | Loaded from snapshot |

## Session Snapshots

Sessions must record the **full agent config** used, not just a key or file reference. This ensures:

- **Reproducibility** — you can rerun with identical agents even if the source file changed or the agent was ephemeral
- **Lineage** — if an agent evolves, you can see what version was used in each session
- **Debugging** — compare agent configs across sessions to understand behavioral differences

The snapshot goes in `session.json` alongside the existing session manifest data.

## What This Means for Current Design

**Don't do yet:**
- Don't build the resolution layer
- Don't build agent mutation/evolution mechanics
- Don't add the `id` field to YAML schema yet

**Do protect:**
- Don't add assumptions that agents must come from files
- Don't use file paths as agent identity in new code
- Don't assume agent configs are immutable across sessions
- When adding new agent-related features, use `AgentConfig` as the contract boundary, not file I/O

## Teams

Teams follow the same pattern — they're currently file-only but should eventually support dynamic composition. A team is just a named set of agents + mode definitions. The same identity and resolution model applies:

- Teams get IDs
- Team configs can come from files, generation, or API
- Sessions snapshot the team config used

## Open Questions

- What triggers agent evolution? (Evaluation scores? User feedback? Automated tuning?)
- What changes when an agent evolves? (Traits? Anti-slop rules? Technique? All of the above?)
- Should evolution be automatic or require explicit approval?
- How do you fork an agent vs. evolve in place?
- Should there be an agent version history (like git for agent configs)?
- How does the Agent Workshop UI interact with this model?
