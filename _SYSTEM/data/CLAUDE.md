# _SYSTEM/data

Authoritative agent persona and team manifest definitions. Loaded at runtime by `agentteam.agents.loader`.

---

## Hard Rules

**NEVER** put briefs, team YAMLs, or agent YAMLs inside `projects/engine/` — the authoritative source is here.

---

## Structure

```
discussionAgents/   → One file per agent: {team-name}__{agent_key}.yaml
teams/              → Team manifests: {team-name}.yaml (lists agent keys + file refs)
briefs/             → Discussion brief markdown files (user-created, reusable input)
```

## Brief Files (`briefs/`)

Discussion briefs are the input to a session. Put them here so they are versioned alongside agent definitions, not scattered in project subfolders.

Format:
```markdown
## What's Already Decided
- Decision 1

## Open Questions
1. **Question Title** Question body with context.
```

Run a session:
```bash
python session_runner.py _SYSTEM/data/briefs/my-brief.md
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
