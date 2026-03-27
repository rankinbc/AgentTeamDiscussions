

- DECIDED: Uniform sliding window with structured scaffold — all agents see the same truncated history plus a persistent scaffold; no per-agent filtering in V1
- DECIDED: Scaffold and summary are separate concerns — scaffold is append-only decisions/tensions list, summary compresses recent discussion, both are synthesizer output fields not separate subsystems
- DECIDED: Scaffold serves as Morning Brief source material — format designed for downstream synthesis into final deliverable
- DECIDED: Truncation is a template concern — prompt assembly uses existing Jinja2 templates to compose scaffold + window + current-round prompt; no new engine components
- DECIDED: One config surface — all tunable knobs live in `defaults.yaml`; no per-agent configuration
- DECIDED: Context assembly order is scaffold → summary → sliding window → role prompt + round instructions, rebuilt from scratch every round
- DECIDED: Default sliding window is last 2 rounds of messages, configured via `history_window_rounds` in `defaults.yaml`
- DECIDED: Window sizing is rounds-based not message-count-based because round boundaries are semantically meaningful
- DECIDED: Scaffold contains four append-only fields: decisions, open_tensions, current_question, and constraints
- DECIDED: Scaffold format is plain markdown with headed sections and flat lists — no nested structure
- DECIDED: Scaffold density controlled by `scaffold_detail` config key with values `compact` (under 300 tokens) or `full` (under 800 tokens), defaulting to `compact`
- DECIDED: Use `full` scaffold detail when brief has more than 5 open questions or when `--eval` mode is active
- DECIDED: Scaffold compaction fires when token count exceeds 30% of available context budget — merges subset decisions, drops resolved tensions, truncates rationale
- DECIDED: Session halts if compaction cannot bring scaffold under 30% budget, writing scaffold to session directory for manual review
- DECIDED: Summary is rolling compression — synthesizer receives prior summary plus outgoing window messages, no full-history re-read
- DECIDED: Summary capped at 1,500 tokens via `summary_max_tokens` config key
- DECIDED: Summary drift check compares scaffold decisions against summary text; logs `DRIFT_WARNING` if decision keyword absent for 2 consecutive rounds but does not halt
- DECIDED: Scaffold stability check hashes decisions list each round; halts session with `SCAFFOLD_CORRUPTION` if any decision disappears between rounds
- DECIDED: Token budget monitoring logs scaffold, summary, window, and remaining budget per round
- DECIDED: If remaining budget drops below 2,000 tokens, reduce `history_window_rounds` by 1; if already at 1, force scaffold compaction; if still over budget, halt
- DECIDED: Engine passes scaffold, summary, and window_messages as template variables; template controls ordering and delimiters
- DECIDED: Morning Brief reads final scaffold and last round's synthesis — not the full transcript
- DECIDED: Recommend `full` scaffold detail for overnight runs where Morning Brief quality is primary deliverable; `compact` for interactive/exploratory sessions
- OPEN: Per-agent role-filtered windows — deferred until data shows agents lose coherence on role-specific points despite uniform windows; requires instrumentation first
- OPEN: On-demand full-history retrieval — deferred until sessions regularly exceed 10 rounds with scaffold corruption events
- OPEN: Semantic relevance filtering — deferred until scaffold compaction fires more than once per session on average across 20+ runs

<!-- complete -->
