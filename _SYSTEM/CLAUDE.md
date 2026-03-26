# _SYSTEM

All active application code, data, docs, and configuration for AgentTeamDiscussions.

---

## Hard Rules

**ALWAYS** import from `agentteam.*` directly. `lib/` has been deleted — it no longer exists.

**ALWAYS** install the package before running: `pip install -e .` from `_SYSTEM/`.
All entry points require the `agentteam` package on `sys.path`.

---

## Structure

```
agentteam/          → Installable library: types, prompts, runner, session I/O, synthesis
config/             → Shared config (currently empty — engine project has its own config/)
data/               → Agent/team YAML definitions + reusable briefs (authoritative source)
  discussionAgents/ → One YAML file per agent
  teams/            → Team manifest YAMLs
  briefs/           → Discussion brief markdown files (user-created, reusable)
docs/               → Design documentation — concepts/, v1/, ideas/, references/, archive/
projects/
  engine/           → Primary discussion app
tests/              → pytest test suite for agentteam package
pyproject.toml      → Package definition (hatchling, Python 3.11+)
```

**Output** (repo root `output/`) — all runtime artifacts write here:
- `output/sessions/` — full session runs
- `output/design-docs/` — design docs from `--no-session` runs
- `output/panel-runs/` — brainstorm panel analysis

---

## Conventions

**Use** `pathlib.Path` for all file I/O with explicit `encoding="utf-8"`. Never `os.path`.

**Use** `platform.system() == "Windows"` checks for subprocess calls — `shell=True` + `list2cmdline` on Windows, `subprocess_exec` on others.

**Run tests** from `_SYSTEM/`: `python -m pytest`

---

## Reference

Read `_SYSTEM/docs/concepts/` before modifying the conversation engine or discussion rounds.
Read `_SYSTEM/docs/v1/` before changing session lifecycle, ledger, or Morning Brief generation.
Read `_SYSTEM/docs/CONCERNS.md` before touching known fragile areas (live synthesizer, history truncation, hallucination check, prior_specs chaining).
