# Deferred Work

## Deferred from: code review of 3-6-team-config-agent-swapping (2026-03-26)

- Unknown `JobType` values default silently to `"propose"` via `.get(..., "propose")` fallback in `_JOB_TO_ROUND` — intentional per spec; address if new job types are added that should not be proposers
- `load_agent_by_key` glob match is non-deterministic when multiple `*__{key}.yaml` files exist — pre-existing; sort glob results and assert uniqueness if team namespacing becomes important
- `list_teams` and `load_team` have inconsistent contracts for a missing `agents` key (permissive vs strict) — pre-existing; standardize if `list_teams` is ever used for validation
- Integration tests (`test_real_beta_agents_team_loads_and_assigns`, `test_agent_file_in_agents_dir_still_works`) have no `skipif` guard for missing data directory — add `pytest.mark.integration` or data-dir `skipif` if CI runs without the data dir
- `resolve_agent` `hasattr(agent, "id")` guard is always `True` for Pydantic model (field always present); guard should be `agent.id is not None` — pre-existing minor bug
- Absolute `agent_file` path in team YAML accidentally works via pathlib join behavior (`_AGENTS_DIR / "/abs/path"` discards left side) — pre-existing undocumented; document or add explicit check if absolute paths become a use case
- Empty `agents: []` in team YAML silently returns empty `TeamConfig` without error — pre-existing; add explicit guard in `load_team` when empty-team detection matters
- Dict-format `agents` branch bypasses all new `load_team` path-resolution logic — by design per Task 3.3; document that dict-format teams don't support co-located agent files
- `load_team_by_name` has no `team_dir` fallback — intentional per Task 3.3; document that portable co-located teams must use `load_team()` not `load_team_by_name()`
- `status["team"]` not written in no-session mode (`session_management=False`) — by design; AC5 is scoped to full-session path; add if no-session mode ever gains session metadata
- `assign_rounds_from_job_types` not re-exported from top-level `agentteam` package — pre-existing pattern; add to `agentteam/__init__.py` if public API surface needs flattening

## Deferred from: code review of 3-5-perspective-drift-detection-reminders (2026-03-25)

- "Generic response" third drift signal (AC1) not implemented — AC1 specifies three signals; generic-response heuristic was not defined in Dev Notes; no clear algorithm specified; address in E4 context assembly or E7 cognitive action system
- Curly-quote apostrophes not normalized before phrase matching (drift.py) — frozenset phrases use straight apostrophes; LLM output may use U+2019 curly quotes; add unicode normalization if false-negative rate becomes observable
- No cooldown/deduplication on drift reminder injection (orchestrator.py) — reminder injected every drifting turn with no cap; token growth unbounded; address when token budget enforcement added in E4
- No runtime enforcement of `< 100 words` docstring constraint (drift.py `build_drift_reminder`) — only test-time assertion enforces the contract; add guard if drives/pushback configs become user-editable with unbounded length
- Asymmetric punctuation handling — extraction strips `.,;:` from words but `!?'"` variants not handled; low risk since detection is substring-based on raw response
- No word boundaries in anchor matching — `word in lower` substring check; anchor "scope" matches in "microscope"; direction of error is missed drift (false negative) rather than false alarm; address with regex if false-negative rate becomes observable
- `previous_responses` key format mismatch undetected — silent `.get(agent_key, "")` fallback; hyphen vs underscore key drift silently skips detection; add validation when `previous_responses` gains real callers
- Stateless detection — `detect_drift` has no memory across turns; intentional per-call design; address in E7 cognitive action system if turn-accumulating drift tracking is needed

## Deferred from: code review of 3-4-output-constraints-anti-pattern-enforcement (2026-03-25)

- `_jinja_env` module global uses no lock (output.py) — same lazy-init pattern as identity.py and ConfigLoader; CPython GIL prevents corruption; pre-existing design choice
- Jinja2 autoescape disabled in output.py env — template injection via config fields is theoretically possible but identical to identity.py; use SandboxedEnvironment if config fields ever accept untrusted user input
- Template path resolved via `__file__` (output.py) — fails in zip-imported packages; pre-existing pattern from identity.py
- Empty `tone` string produces malformed `Tone: ` line in output.j2 — VoiceConfig default is "professional"; no agent YAML triggers this; add `{% if tone %}` guard if tone becomes user-editable
- Anti-pattern value containing `"` corrupts double-quoted bullet in output.j2 — no agent YAML triggers this; address in agent YAML authoring/validation guidelines
- Multi-line anti-pattern strings corrupt bullet list in output.j2 — same class as Story 3.3 multi-line description defer; address in E4 context assembly story
- `_job_desc`/`_level_desc` silent fallback for missing enum entries (output.py) — intentional safety valve; update both dict and fallback when adding new enum values
- `vocabulary_hints` with empty-string items passes through unguarded — address when vocabulary_hints gain min_length=1 validation (same deferral as Story 3.2 anti_patterns)
- `uncomfortable_idea_quota` implements turn cadence, not a count — naming mismatch from original builder.py; address in Epic 7 Cognitive Action System work

## Deferred from: code review of 3-3-identity-layer-prompt-builder (2026-03-25)

- `_jinja_env` module global uses no lock (identity.py) — same lazy-init pattern as ConfigLoader; CPython GIL prevents data corruption; low-priority until async multi-threaded engine work
- `style_description=""` suppression path not directly tested — empty default suppresses section via Jinja2 `{% if %}`; implicitly covered by minimal_agent tests; add explicit test if style_description becomes configurable
- Multi-line `description`/`domain_affinities` entries produce extra blank lines in rendered output — no agent YAMLs trigger this; address in E4 context assembly story
- `keep_trailing_newline=True` in Jinja2 env not specified in Dev Notes — harmless; taken from ConfigLoader pattern; document if Jinja2 env config becomes a maintenance concern
- `filter_prior_rounds` idx=-1 edge case (no `\n[` in tail when text is truncated) — pre-existing function, unchanged by Story 3.3; address in Epic 5 crash-safe / session reliability work

## Deferred from: code review of 2-1-brief-parser-question-extraction (2026-03-25)

- IO exceptions from `read_text` not wrapped as `BriefParseError` (parser.py:18,36) — design choice, module handles missing sections not missing files; callers can add wrapping if needed
- BOM-prefixed UTF-8 files cause H1 stripping to fail in `parse_brief_structured` (parser.py) — use `utf-8-sig` encoding to fix; low-priority edge case on Windows

## Deferred from: code review of 2-3-three-round-discussion-orchestration (2026-03-25)

- `build_agent_payload` ternary for `question_section` is fragile to future edits (orchestrator.py) — code is functionally correct; refactor opportunity when touching that function
- `run_round` does not handle future case where `run_claude_async` raises instead of returning error string (orchestrator.py) — migration target documented in CLAUDE.md; address when runner error handling is migrated to exceptions

## Deferred from: code review of 2-5-transcript-session-output (2026-03-25)

- Stale `.tmp` file not cleaned up if `write_text` fails mid-write (agentteam/utils/io.py) — harmless in practice (next call overwrites stale tmp); proper cleanup belongs in Epic 5 story 5-1 (crash-safe disk writes)
- Bare `KeyError` raised if `question` dict missing `title` key (agentteam/output/transcripts.py) — all callers use validated dicts from brief parser; add `.get()` with fallback if direct construction ever bypasses validation

## Deferred from: code review of 3-2-anti-pattern-anti-slop-configuration (2026-03-25)

- Non-empty string items not enforced in `anti_patterns` field — AC1 says "non-empty strings" but `VoiceConfig(anti_patterns=["","","","","","","",""])` passes validation; fix: `list[Annotated[str, Field(min_length=1)]]`; same deferral as Story 3.1 drives/behaviors
- YAML position-based trimming unverified by content tests — `adversarial_critic` (15→12) and `idea_merchant` (17→12) had last N items removed; no test validates specific retained phrases; low risk since removed items were generic ("I appreciate the effort", "Step 1")
- Pydantic v2 asymmetry inline comment missing in `agent.py` — `VoiceConfig()` passes but `VoiceConfig(anti_patterns=[])` raises; a one-line comment on the field would help future maintainers; covered by test docstring for now

## Deferred from: code review of 3-1-agent-yaml-schema-validation (2026-03-25)

- Non-empty string items not enforced in `drives`, `pushback_on`, `behaviors` fields — AC 3 & 4 say "non-empty strings" but `PositionConfig(drives=["","",""])` passes validation; fix with `list[Annotated[str, Field(min_length=1)]]`; low priority since all real agent YAMLs contain non-empty strings
- `loader.py:21` null-check missing — `yaml.safe_load()` returns `None` for empty/whitespace-only files, causing `AttributeError` on `.pop()`; add `if raw is None: raise ValueError(...)` guard
- `TestLoadAgentRealFiles` collection-time glob — `get_agent_yamls()` is called at module import; if `_AGENTS_DIR` doesn't exist, parametrize receives empty list and all 33 tests are silently skipped with no failure; add `assert len(files) > 0` guard in conftest or test

## Deferred from: code review of 2-2-session-runner-cli-entry-point (2026-03-25)

- Non-YAML / non-valid file passes CLI team validation (session/runner.py) — `.is_file()` check added but no extension or content check; proper validation belongs in `load_team()` with user-friendly error propagation
- TOCTOU race between `team_path.exists()` check and `shutil.copy2(_team_path, ...)` inside `run_session()` — very low probability; fix during Epic 5 crash-safe I/O work
- Import crash in `session/runner.py` makes all subprocess CLI tests exit code 1 spuriously (test_missing_brief_exits_one, test_missing_team_exits_one would pass even with broken import) — pre-existing limitation of subprocess test pattern; add import-smoke test when revisiting CLI tests
