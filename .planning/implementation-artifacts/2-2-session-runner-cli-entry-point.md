# Story 2.2: Session Runner CLI Entry Point

Status: done

## Story

As a user,
I want to run `python session_runner.py brief.md` from the command line,
so that a complete discussion session executes without further intervention.

## Acceptance Criteria

1. **Given** a valid brief file
   **When** I run `python session_runner.py brief.md`
   **Then** a timestamped session folder is created under sessions/ and the session pipeline starts

2. **Given** a `--team` flag pointing to a YAML file
   **When** I run `python session_runner.py brief.md --team my-team.yaml`
   **Then** that team config is used instead of the default (beta-agents.yaml)

3. **Given** `--team` is not specified
   **When** the runner starts
   **Then** it defaults to `data/teams/beta-agents.yaml` relative to the engine

4. **Given** a missing brief file
   **When** I run `python session_runner.py nonexistent.md`
   **Then** a clear error message is printed and the process exits with code 1

5. **Given** a `--team` flag pointing to a non-existent YAML
   **When** the runner starts
   **Then** a clear error message is printed and the process exits with code 1 (not a raw traceback)

6. **Given** `--help` flag
   **When** I run `python session_runner.py --help`
   **Then** the process exits with code 0 and the help text documents all flags

## Tasks / Subtasks

- [x] Task 1: Fix team YAML validation in `main()` (AC: 5)
  - [x] 1.1: After resolving `team_yaml` path from `args.team` in `main()`, check if the resolved path exists
  - [x] 1.2: If not found, print `"ERROR: Team config not found: {path}"` and call `sys.exit(1)`
  - [x] 1.3: Insert this check BEFORE calling `run_session()` (at lines ~940-942 in `session/runner.py`)

- [x] Task 2: Add CLI smoke tests in `_SYSTEM/tests/test_session_runner_cli.py` (AC: 1–6)
  - [x] 2.1: Create new test file; use `subprocess.run` to invoke `session_runner.py` as a subprocess
  - [x] 2.2: `TestSessionRunnerCLI` class with:
    - `test_help_exits_zero` — `--help` returns exit code 0
    - `test_help_shows_flags` — `--help` output contains `--mode`, `--team`, `--timeout`
    - `test_missing_brief_exits_one` — nonexistent brief → exit code 1
    - `test_missing_brief_prints_error` — stderr/stdout contains "ERROR" or "Brief not found"
    - `test_missing_team_exits_one` — `--team nonexistent.yaml` → exit code 1
    - `test_missing_team_prints_error` — output contains "ERROR" and the bad path

## Dev Notes

### BROWNFIELD: Implementation Already Exists

**DO NOT rewrite the session runner.** The full implementation lives in:
- `_SYSTEM/projects/engine/session/runner.py` — `main()`, `run_session()`, `run_question_with_cascade()`
- `_SYSTEM/projects/engine/session_runner.py` — thin backward-compat wrapper (3 lines)

The existing `main()` handles:
- `argparse` with `--mode`, `--timeout`, `--eval`, `--resume`, `--no-session`, `--live`, `--output-dir`, `--port`, `--team`
- Missing brief check: `if not brief_path.exists(): sys.exit(1)` (already exists at ~line 917)
- Default team: `TEAM_CONFIG = _DATA_DIR / "teams" / "beta-agents.yaml"` (from `discussion/engine.py`)

**The only gap** (AC 5): If `--team path/to/nonexistent.yaml` is passed, `main()` currently constructs `Path(args.team).resolve()` and passes it to `run_session()`. Inside `run_session()`, `load_team(str(_team_path))` raises `FileNotFoundError`. This propagates as an unhandled exception (Python traceback) instead of a clean error message.

### Fix Location (Task 1)

In `_SYSTEM/projects/engine/session/runner.py`, the `main()` function ends with:

```python
    team_yaml=Path(args.team).resolve() if args.team else None,
```

Add validation just before the `await run_session(...)` call (~line 930):

```python
    if args.team:
        team_path = Path(args.team).resolve()
        if not team_path.exists():
            print(f"ERROR: Team config not found: {team_path}")
            sys.exit(1)
    else:
        team_path = None

    await run_session(
        ...
        team_yaml=team_path,
    )
```

### Test Architecture

Tests in `_SYSTEM/tests/test_session_runner_cli.py` use **subprocess** to invoke the CLI.
This avoids the module-level config imports in `session/runner.py` which need `config_loader`, `discussion.engine`, etc. — all of which require the engine config files to be present. Testing via subprocess sidesteps all of that cleanly.

```python
import subprocess, sys
from pathlib import Path

ENGINE_DIR = Path(__file__).parent.parent / "projects" / "engine"
RUNNER = str(ENGINE_DIR / "session_runner.py")

def run_cli(*args, **kwargs):
    return subprocess.run(
        [sys.executable, RUNNER, *args],
        capture_output=True, text=True,
        cwd=str(ENGINE_DIR),
        **kwargs,
    )
```

**Why subprocess and not `subprocess.run([sys.executable, "-m", ...])`**: `session_runner.py` is not a package entry point; it's a script run directly as `python session_runner.py`. Use the file path approach above.

**timeout**: All subprocess calls should pass `timeout=15` to prevent hanging if the runner accidentally starts a session.

### What NOT to Test (Scope Boundaries)

- Do NOT test that a full discussion session runs (that requires live Claude CLI calls)
- Do NOT test `--mode`, `--resume`, or `--no-session` flags (those are E5/E6 stories)
- Do NOT mock internal functions — subprocess tests verify the real CLI behavior

### Architecture Rules

- `pathlib.Path` only — never `os.path`
- Line length: **100** (ruff, not 79/88)
- No `print()` or `logging` in `agentteam/` library — the `session/runner.py` is a runner (allowed)
- Python 3.11+ union syntax: `str | None`, not `Optional[str]`

### Testing Rules

- New file: `_SYSTEM/tests/test_session_runner_cli.py`
- Run from `_SYSTEM/`: `python -m pytest tests/test_session_runner_cli.py -v`
- Use class `TestSessionRunnerCLI` (not module-level functions)
- No `@pytest.mark.asyncio` needed — subprocess tests are sync
- `timeout=15` on all `subprocess.run` calls to prevent hangs

### File Touch List

| File | Action |
|---|---|
| `_SYSTEM/projects/engine/session/runner.py` | Add team YAML existence check in `main()` before `run_session()` |
| `_SYSTEM/tests/test_session_runner_cli.py` | New file — CLI subprocess tests |

### Review Findings

- [x] [Review][Patch] `team_path.exists()` passes for directories — change to `team_path.is_file()` [session/runner.py:932]
- [x] [Review][Defer] Non-YAML file (any existing file) passes CLI validation [session/runner.py:932] — deferred, pre-existing; `load_team()` is correct fix location
- [x] [Review][Defer] TOCTOU race between validation and `shutil.copy2` in `run_session()` [session/runner.py] — deferred, pre-existing in run_session
- [x] [Review][Defer] Import-crash in session/runner.py makes all subprocess tests exit-1 spuriously [tests/test_session_runner_cli.py] — deferred, pre-existing architecture limitation of subprocess tests

### References

- [Source: _SYSTEM/projects/engine/session/runner.py#main] — full `main()` function (lines 846–946)
- [Source: _SYSTEM/projects/engine/session_runner.py] — thin wrapper entry point
- [Source: _SYSTEM/agentteam/agents/loader.py#load_team] — raises `FileNotFoundError` if team not found
- [Source: _bmad-output/planning-artifacts/epics.md#Story 2.2] — acceptance criteria
- [Source: _bmad-output/project-context.md] — project rules

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6

### Debug Log References

### Completion Notes List

- Added team YAML existence check in `main()` (runner.py lines 930–936): resolves path, checks `.exists()`, prints `ERROR: Team config not found: {path}` and calls `sys.exit(1)`
- Created `tests/test_session_runner_cli.py` with `TestSessionRunnerCLI` (8 tests via subprocess)
- `test_help_*` tests split into 3 (mode, team, timeout flags) plus exit-code check
- `sample_brief` fixture sourced from `conftest.py` (pre-existing)
- 8/8 tests passing; full suite (211 tests) — no regressions

### File List

- _SYSTEM/projects/engine/session/runner.py
- _SYSTEM/tests/test_session_runner_cli.py
