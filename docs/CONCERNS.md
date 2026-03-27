# Codebase Concerns

**Analysis Date:** 2026-03-25 | **Last Updated:** 2026-03-26

---

## Tech Debt

**Duplicate prompt builder — engine has its own copy:**
- Issue: `build_system_prompt`, `build_perspective_reminder`, `build_context_lens`, and `filter_prior_rounds` have an independent copy at `_SYSTEM/projects/engine/prompt_builder.py` separate from the canonical `agentteam.prompts.builder`. A wording change in one does not propagate.
- Files: `_SYSTEM/agentteam/prompts/builder.py` (canonical), `_SYSTEM/projects/engine/prompt_builder.py` (stale copy)
- Fix approach: Audit which callers use `engine/prompt_builder.py` and redirect to `agentteam.prompts.builder`. Then delete the engine copy.

**`model` parameter accepted but ignored in `run_claude_async`:**
- Issue: `run_claude_async` accepts `model: str = None` but silently ignores it. Callers passing `"sonnet"` believe they are switching models when they are not. Model is determined by `ANTHROPIC_MODEL` env var.
- Files: `_SYSTEM/agentteam/runner/claude.py`
- Fix approach: Pass `--model {model}` to CLI when `model` is not None, or remove the parameter entirely and document that model is env-only.

---

## Known Behavioral Issues

**Agent verbosity — word limit is advisory, not enforced:**
- Issue: Agents are instructed "250 words max" or "Under 300 words" via prompt text, but the Claude CLI has no hard token limit applied. Agents frequently ignore this instruction, especially in complex rounds where prior context is long.
- Files: `_SYSTEM/projects/engine/discussion/engine.py` (lines 141–143), `_SYSTEM/agentteam/prompts/builder.py` (lines 106–115)
- Impact: Downstream `accumulated_discussion` grows faster than expected, causing earlier context to be truncated at the `truncation_threshold` sooner and compressing the history window mid-session.
- Fix approach: Apply `--max-tokens` via CLI flag or switch to the Claude SDK with explicit `max_tokens` per call. No fix is possible with the current subprocess model unless the CLI exposes a `--max-tokens` flag.

**`model` parameter is accepted but unused in `run_claude_async`:**
- Issue: Both `run_claude_async` signatures accept a `model: str = None` parameter with the comment "model param is accepted but unused (set via env)". Many callers pass explicit model strings (e.g., `"sonnet"`) expecting them to take effect.
- Files: `_SYSTEM/agentteam/runner/claude.py` (line 51–53), `_SYSTEM/projects/live-ui/conversation.py` (lines 270, 799, 906, etc.)
- Impact: Model selection via argument is silently ignored. Callers believe they are switching models when they are not. The model is determined by whatever `ANTHROPIC_MODEL` env var or CLI default is active.
- Fix approach: Either pass `--model {model}` to the CLI command when `model` is not None, or document clearly that model is env-only and remove the parameter to prevent confusion.

**Role differentiation degrades over long discussions:**
- Issue: Agents share a single `accumulated_discussion` string that grows with each round. By question 8+ of a 10-question brief, all agents receive essentially the same 6,000-character context window. The `filter_prior_rounds` truncation is only agent-specific in the `agentteam` package version; the engine's `_build_agent_payload` applies a single truncation for all agents identically.
- Files: `_SYSTEM/projects/engine/discussion/engine.py` (lines 126–133), `_SYSTEM/agentteam/prompts/builder.py` (lines 160–174)
- Impact: Agent differentiation — the core quality metric — degrades as sessions get longer. This was identified in experiment reports as the primary output quality issue.
- Fix approach: Apply per-agent `filter_prior_rounds` (from `agentteam.prompts.builder`) in `_build_agent_payload` rather than passing the same unfiltered prior rounds to all agents.

**Anti-slop `uncomfortable_idea_quota` trigger interval is inverted:**
- Issue: In `_build_antislop_section`, the interval formula is `max(5, 10 - quota)`. A quota of 5 (maximum) yields interval=5 (fires every 5 turns). A quota of 1 (minimum non-zero) yields interval=9 (fires every 9 turns). This means a higher quota value produces *more frequent* triggers, but the calculation `10 - quota` means the semantic meaning ("how many uncomfortable ideas per 10 turns") is correct only if the quota is interpreted as a frequency not a count. The formula is confusing and produces counterintuitive prompts: "Every 5 turns" is presented to the agent with no further context.
- Files: `_SYSTEM/agentteam/prompts/builder.py` (lines 45–47), `_SYSTEM/agentteam/conversation/state.py` (lines 55–60)
- Impact: Agents receive ambiguous instructions; the interval number in the prompt has no clear semantic meaning to the LLM without explanation.

---

## Fragile Areas

**`write_with_marker` is not atomic (crash window):**
- Issue: Crash-safe persistence uses `write_with_marker`, which writes content then appends `<!-- complete -->` in two separate `f.write()` calls within the same file handle. If the process is killed between the two flushes, the file will have content but no marker. The `is_complete` check will return False and the question will be re-run on resume — but the partial file will be overwritten, which is the correct behavior. However if the OS buffers the second flush and the first write is visible, there is a brief window where content appears complete but the marker is missing.
- Files: `_SYSTEM/agentteam/session/persistence.py` (lines 8–10)
- Impact: Low probability in practice. The main risk is re-running an expensive question unnecessarily on resume, not data corruption.
- Fix approach: Write both content and marker in a single `f.write(content + COMPLETION_MARKER)` call, or use a temp file + rename for true atomicity.

**`hallucination_check` uses fragile regex to count doc sections:**
- Issue: The function counts `"### D\d"` or `"### [A-Z]"` patterns to estimate doc decision count. If the synthesis model changes its heading format (e.g., uses `## Decision 1` instead of `### D1`), the count returns 0 and the function returns True (passes) regardless of ledger content, defeating its purpose.
- Files: `_SYSTEM/agentteam/session/ledger.py` (lines 17–24)
- Impact: Hallucination detection silently stops working if synthesis output format drifts. The check passes even when the ledger has wildly more or fewer entries than the doc.
- Fix approach: Detect heading format from the actual synthesis output rather than hardcoding patterns.

---

## Performance Bottlenecks

**Sequential agent execution within rounds:**
- Issue: `run_round` defaults to `sequential=True`, which means agents speak one-at-a-time. With 6 agents at 60–120s per call, a single round takes 6–12 minutes. With 3 rounds per question and 10 questions, a full session takes 3–6 hours.
- Files: `_SYSTEM/projects/engine/discussion/engine.py` (lines 187–218)
- Impact: Long wall-clock time is the primary user experience bottleneck. Sequential mode was chosen so agents can see each other's responses (which improves discussion quality), but it is the single largest time cost.
- Note: The parallel path exists (`sequential=False`) but is labeled "legacy" and would sacrifice response quality for speed.

**Synthesis is a serial bottleneck per question:**
- Issue: After all rounds complete, synthesis is a single LLM call that cannot be parallelized. At 120s timeout, synthesis alone adds 2+ minutes per question.
- Files: `_SYSTEM/projects/engine/discussion/engine.py` (lines 221–260), `_SYSTEM/projects/engine/session/runner.py` (lines 308–353)
- Impact: Unavoidable with current architecture. Could be partially mitigated by starting synthesis for question N while question N+1's first round runs, but that would require significant refactoring.

**Ledger extraction adds an additional LLM call per question:**
- Issue: After synthesis, `session/runner.py` makes a separate `extract_ledger_from_doc` call to extract decisions. This adds another 30–60s per question.
- Files: `_SYSTEM/projects/engine/session/runner.py` (lines 83–104)
- Impact: ~10 minutes of additional overhead per 10-question session. Could be merged into the synthesis prompt itself.

**Rolling synthesis fires every 5 turns with a 30s timeout:**
- Issue: `LiveSynthesizer.maybe_synthesize` fires a background Claude call every 5 turns. In a high-activity session this can produce synthesis calls overlapping with agent calls, contending for CLI subprocess slots.
- Files: `_SYSTEM/agentteam/synthesis/live.py` (lines 57–75)

---

## Security Considerations

**System prompt injection via agent YAML:**
- Risk: Agent `description`, `drives`, `pushback_on`, `behaviors`, and `anti_patterns` fields are rendered verbatim into system prompts without sanitization. If a user-crafted YAML file contains prompt injection text (e.g., `"\n\nIgnore all prior instructions..."`), it will be embedded directly in the system prompt sent to Claude.
- Files: `_SYSTEM/agentteam/prompts/builder.py` (all `_build_*` functions), `_SYSTEM/agentteam/agents/loader.py`
- Current mitigation: None. YAML parsing uses `yaml.safe_load` which prevents code execution but does not sanitize string content.
- Recommendations: Validate string fields against a maximum length and character allowlist before rendering into prompts.

**`os.system("")` used to enable Windows VT100 mode:**
- Risk: The evaluator uses `os.system("")` to trigger Windows terminal VT100 mode. This is a known pattern but calls the OS shell with an empty command.
- Files: `_SYSTEM/projects/engine/evaluation/evaluator.py` (line 32)
- Current mitigation: The `# noqa: S605` comment acknowledges this. It is benign but should use `ctypes` or `colorama` instead.

---

## Missing Critical Features

**No rate limiting or backpressure on Claude CLI calls:**
- Problem: All async callers fire `run_claude_async` concurrently without any concurrency limiter. In evaluation mode, `evaluate_pair` launches multiple parallel LLM calls per doc (doc eval + transcript eval + N agent evals), all simultaneously. With 10 questions and 7 agents, this can spawn 90+ concurrent subprocess calls.
- Files: `_SYSTEM/projects/engine/evaluation/evaluator.py` (lines 598–603), `_SYSTEM/projects/engine/discussion/engine.py` (lines 183–185)
- Blocks: Reliable overnight runs on large briefs
- Fix: Add `asyncio.Semaphore` to cap concurrency in both evaluation and parallel discussion modes.

**No moderator input handling in session runner:**
- Problem: The structured session runner (`session/runner.py`) has no way to inject moderator input between rounds or questions.
- Files: `_SYSTEM/projects/engine/session/runner.py`
- Blocks: Moderator-guided overnight sessions

**No retry/backoff for empty responses in async runner:**
- Problem: `run_claude_async` has no retry logic — it returns `"[Empty response from claude CLI]"` immediately on empty output. Only `run_claude_sync` has retry with `time.sleep(2)`. In practice async calls are the primary path for all discussion and synthesis.
- Files: `_SYSTEM/agentteam/runner/claude.py` (lines 47–92)
- Blocks: Reliability on flaky CLI connections or rate-limited calls

---

## Test Coverage Gaps

**Engine project has no unit tests:**
- What's not tested: `discussion/engine.py`, `session/runner.py`, `evaluation/evaluator.py`, `live/server.py`, `conversation/modes.py`, all of `brainstorm/`
- Files: `_SYSTEM/projects/engine/` — no `tests/` directory exists here
- Risk: Session resume logic, round health checks, failure cascade, and ledger extraction can all break silently
- Priority: High — session runner is the primary user-facing entry point

**`agentteam` tests do not cover the runner or synthesis modules:**
- What's not tested: `agentteam/runner/claude.py` (subprocess behavior), `agentteam/synthesis/live.py` (JSON parse failure paths, `is_topic_exhausted` logic), `agentteam/conversation/state.py` (history truncation edge cases)
- Files: `_SYSTEM/tests/` — only 5 test files covering brief parser, config loader, prompt builder, ledger, and persistence
- Risk: Synthesis parse errors silently produce degraded snapshots (`mood="unknown"`) with no alerting
- Priority: Medium

**No integration tests for end-to-end session flow:**
- What's not tested: The full pipeline from brief parsing → team loading → round execution → synthesis → ledger extraction → Morning Brief generation
- Risk: Module boundary issues (e.g., the `run_discussion` import breakage described above) would not be caught before a production run
- Priority: High

---

## Dependencies at Risk

**`agentteam` has no declared dependency on `jinja2` but uses it via `ConfigLoader`:**
- Risk: `jinja2` is listed in `pyproject.toml` but `agentteam.config.loader` only imports it inside `_get_jinja_env()` as a lazy import. If `jinja2` is not installed and a caller never renders a template, the missing dependency is invisible until first use.
- Files: `_SYSTEM/agentteam/config/loader.py` (lines 50–58), `_SYSTEM/pyproject.toml`
- Impact: Fails only on first `render_prompt` call, potentially mid-session

**No pinned dependency versions:**
- Risk: `pyproject.toml` specifies only lower bounds (`pydantic>=2.0.0`, `pyyaml>=6.0`, `jinja2>=3.1.0`). A breaking update to Pydantic v3 (if released) would silently break all model parsing.
- Files: `_SYSTEM/pyproject.toml`
- Impact: Reproducibility risk for overnight production runs

---

*Concerns audit: 2026-03-25*
