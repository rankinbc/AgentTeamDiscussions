---
name: list-teams
description: List the discussion teams, their agents, modes and round structures available to /agent-discuss:discuss.
allowed-tools: Bash(python3 *)
---

Run:

```
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/discuss" list-teams
```

Present the JSON as a compact table per team: team name and default mode, then each agent
(`key` — `name`, `role`), then each mode with its rounds (`round: agents`) and overlays.
Finish with one example invocation, e.g.
`/agent-discuss:discuss input/test-brief.md --team beta-agents --mode compete`.
