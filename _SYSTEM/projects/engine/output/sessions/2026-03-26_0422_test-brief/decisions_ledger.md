

- DECIDED: Uniform sliding window — all agents see identical history, no role-stratified differentiation
- DECIDED: Smart summarization deferred to Phase 2, pending evidence that uniform windowing degrades Morning Brief quality
- DECIDED: Role-stratified windows deferred to Phase 2, gated on measured quality data showing uniform windows produce inferior output
- DECIDED: Pin Round 1 (brief) always, regardless of window size
- DECIDED: Pin the most recent synthesis turn always as compressed running state
- DECIDED: Sliding window of last N rounds, configurable, default N=3
- DECIDED: Omission markers with count — dropped rounds replaced with `[N rounds omitted]`, never silent
- DECIDED: Token budget (`available_history_tokens`) computed once at session start and held static for the session
- DECIDED: No truncation when history fits — sliding window is a fallback, not a default mode
- DECIDED: Prompt assembly order: system prompt + persona → Round 1 → omission marker → pinned synthesis → last N rounds → current-turn instruction
- DECIDED: Deduplication when pinned turns overlap with sliding window — never send a round twice
- DECIDED: Single config knob `history_window_rounds: 3` in `config/defaults.yaml` — no per-agent overrides, no role mappings
- DECIDED: Window is uniform across all agents in a given round, no exceptions
- OPEN: Role-stratified windows — gated on Morning Brief quality score degradation at 6+ rounds with uniform N=3
- OPEN: LLM-based summarization — gated on token budget becoming insufficient after adding new prompt features
- OPEN: Configurable per-mode window sizes — gated on user requests for longer windows in specific experiment modes
- OPEN: Retrieval-augmented history — gated on agent/round count growing beyond what sliding windows can service

<!-- complete -->
