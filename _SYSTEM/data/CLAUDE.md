# _SYSTEM/data

Authoritative agent persona and team manifest definitions. Loaded at runtime by `agentteam.agents.loader`.

---

## Hard Rules

**NEVER** put team YAMLs or agent YAMLs inside `projects/engine/` — the authoritative source is here.

**Briefs** have moved to `_SYSTEM/projects/engine/input/` — they live alongside the engine since briefs are both input and output of the discussion engine.

---

## Structure

```
discussionAgents/   → One file per agent: {team-name}__{agent_key}.yaml
teams/              → Team manifests: {team-name}.yaml (lists agent keys + file refs)
```

## Adding a New Agent

1. Create `discussionAgents/{team-name}__{agent_key}.yaml`
2. Register the agent in `teams/{team-name}.yaml` under `agents:`
3. No Python changes required

## File Naming

- Agent files: `{team-name}__{agent_key}.yaml` — double underscore separator
- Team files: `{team-name}.yaml`
- YAML keys match Pydantic `AgentConfig` field names exactly: `personality`, `position`, `technique`, `anti_slop`, `voice`, `output`
- Enum values are lowercase strings matching the Enum `.value`: `cognitive_style: lateral`
