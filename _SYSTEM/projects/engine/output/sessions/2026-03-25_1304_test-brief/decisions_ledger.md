

- DECIDED: Context management is not an active constraint at current session lengths (~18,000 tokens); no truncation infrastructure required yet
- DECIDED: Role-stratified retention (four-role taxonomy) is deferred until two-mode behavior is validated
- DECIDED: Summarization is deferred until at least one session demonstrably degrades due to context size
- DECIDED: Two-mode anchored/accumulating model is the target design when context management becomes necessary
- DECIDED: Morning Brief quality (specifically sharpness of the critique section) is the primary quality signal for validating the two-mode model
- DECIDED: Context management activates when any session log records token usage exceeding 60% of the active model's context window
- DECIDED: Each agent carries a single `context_mode` field in YAML config (`anchored` or `accumulating`)
- DECIDED: Anchored agents receive the original brief in full plus last N verbatim turns (default N=4), never synthesized summaries
- DECIDED: Accumulating agents receive compressed round summaries and logged decisions, no verbatim debate content
- DECIDED: Anchored is the default; accumulating is opt-in
- DECIDED: Anchored is a hard selection rule — if verbatim window must shrink, reduce N rather than substitute summaries
- DECIDED: Per-agent context budget is computed at dispatch time using `available_tokens = window_limit × 0.80`, minus brief tokens and 2,000 reserved for response
- DECIDED: Actual token counts are measured at dispatch time rather than estimated from turn count
- DECIDED: Experiment mode role-swapping retains the agent's configured `context_mode`; overrides go in experiment mode config, not agent config
- DECIDED: Measurement plan is ten sessions after activation, tracking turn-level token counts, threshold crossings, and Morning Brief critique quality
- OPEN: Whether critic turns in rounds 3+ introduce new objections not present in rounds 1–2 (to be observed across ten sessions)
- OPEN: Calibration of N (verbatim turns retained for anchored agents) pending empirical data from threshold-crossing sessions
- OPEN: Whether the two-mode assumption holds after ten sessions, or whether the taxonomy must be expanded
- OPEN: Whether experiment mode config will need per-mode `context_mode` overrides for any specific agents

<!-- complete -->
