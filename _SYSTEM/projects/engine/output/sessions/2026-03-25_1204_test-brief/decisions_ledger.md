

- DECIDED: No LLM-based summarization in v1; deferred until simpler approach demonstrably fails on a measurable dimension
- DECIDED: Window mode is the v1 truncation strategy — last N turns verbatim, pure string-slicing, no compression, no additional LLM calls
- DECIDED: Truncation occurs at message construction time per-agent; session file is never modified, trimmed, or summarized
- DECIDED: Session file is the audit log and source of truth for truncation debugging; this invariant is non-negotiable
- DECIDED: History mode is configured per agent in YAML via `history_mode` field; only `window` is valid in v1
- DECIDED: Schema includes `history_mode` and `window_turns` fields now to support future modes without structural changes
- DECIDED: Turns (not tokens) are the unit of window measurement in v1
- DECIDED: Token-based window sizing is deferred pending evidence of high turn-length variance (threshold: >3× average in production)
- DECIDED: `bookends` mode is the next history mode to implement after `window` is validated; not shipped simultaneously with `window`
- DECIDED: Full taxonomy target is `arc | window | bookends`; `arc` requires summarization and is deferred beyond v1
- DECIDED: Session file is append-only and untruncated; truncation is a read-time operation only
- DECIDED: Truncation is always per-agent; two agents in the same round may receive different history lengths
- DECIDED: The original framing prompt (first turn) is always prepended to any agent's history slice regardless of window size; not duplicated if it falls within the window
- DECIDED: `window_turns` must be between 2 and 50 inclusive
- DECIDED: Truncation events are logged with session ID, agent ID, total turns, turns passed, and timestamp
- DECIDED: Role-differentiated history (challengers benefit from structural ignorance of persuasion arc; specialists benefit from original framing alongside recent claims) is acknowledged as theoretically sound but deferred
- OPEN: System-wide default value for `window_turns` — 10 is implied but not agreed; must be set before implementation
- OPEN: When `history_mode` is absent from agent YAML, whether agent receives full history or system default window — full history is safe but operationally problematic at scale; system default is safer but is a breaking change for agents relying on full context
- OPEN: Whether there is an instrumentation plan for coherence constraints other than truncation (prompt design, agent ordering, turn limits) — R5 logging only covers truncation frequency

<!-- complete -->
