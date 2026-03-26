# agentteam

Installable Python library — canonical types, prompt assembly, Claude subprocess runner, session I/O, synthesis. Consumed by `projects/engine/` and `projects/live-ui/`.

Install: `pip install -e .` from `_SYSTEM/`

---

## Hard Rules

**NEVER** emit output from library code — no `print()`, no `logging` calls anywhere in `agentteam/`. Output belongs in callers and runners only.

**NEVER** import from `lib/` within agentteam — the library is self-contained.

---

## Package Structure

```
types/          → AgentConfig and all sub-models (Pydantic) — authoritative
agents/         → loader.py: team and agent YAML loading
brief/          → parser.py: brief markdown parsing
config/         → loader.py: ConfigLoader with Jinja2 template rendering
conversation/   → state.py: Conversation and MultiConversation state machines
prompts/        → builder.py: build_system_prompt(), build_perspective_reminder(), build_context_lens()
runner/         → claude.py: run_claude_sync() / run_claude_async() subprocess wrappers
                  errors.py: ClaudeError hierarchy and is_error_response()
session/        → persistence.py: crash-safe file I/O with completion markers
                  ledger.py: append-only decisions ledger
synthesis/      → live.py: LiveSynthesizer with rolling snapshots
```

---

## Conventions

**Use** `pydantic.BaseModel` + `Field(ge=..., le=...)` for all config models. Use dataclasses for mutable runtime state (conversation history, snapshots).

**Follow** the default-instance pattern for singletons: create `_default_loader` at module level, expose free functions that delegate to it.

**Declare** an explicit `__all__` in `types/__init__.py` when adding new public types.

**Return** `[Error...]`-prefixed strings from `run_claude_sync/async` on failure; check with `is_error_response()`. New code should raise `ClaudeError` subclasses instead — the string-return pattern is a migration target.

**Add** a test file `_SYSTEM/tests/test_{module}.py` for every new module added to agentteam.

---

## Testing

```bash
cd _SYSTEM
python -m pytest                                    # all tests
python -m pytest --cov=agentteam --cov-report=term-missing  # with coverage
python -m pytest tests/test_brief_parser.py        # single file
```

**Mock** subprocess calls (`subprocess.run`, `asyncio.create_subprocess_*`) for runner tests.
**Use** `tmp_path` fixture for file I/O tests — never write to real session or data directories.
**Do not mock** Pydantic validation, YAML parsing from test fixtures, or prompt builder logic.
