# How does a round begin after a reset?

*Generated: 2026-03-17 21:34 | Question 1 | 245s*

The file write is awaiting permission. Here's a summary of what I've synthesized:

**Round Initialization Design Spec** -- distilled from all five panel agents into a single authoritative document covering:

**The Pipeline (5 stages, sequential per agent):**
1. **Load Save File** -- hydrate ideas, stances, decisions, recap from prior round. Round 1 bootstraps from team config + idea brief instead.
2. **Thinking Routines** -- Reflect (adjust magnitudes), Research (spawn focused call), Strategize (reorder priorities). Each has a wall-clock timeout with graceful skip on failure. BackgroundAgent effects are already baked in before this stage runs.
3. **Deterministic Filter** -- prune below-threshold ideas, stale stances, resolved decisions. Persona-dependent thresholds. No LLM call.
4. **LLM Curator** -- transforms filtered state into ~8-15k token Situation block with valuable randomness. Validated by magnitude-weighted check (did top 3 ideas survive?). Falls back to deterministic assembly on failure. Skipped for Round 1.
5. **Prompt Assembly** -- Identity (static ~2k) + Situation (~8-15k) + Task (~1-2k) + remaining (~80k+).

**The key distinction:** Round-open Task is generative ("name what changed, identify your biggest tension, make your opening move") with structural novelty pressure. Mid-round Task is reactive ("here's what Agent X said, respond"). Situation block persists mid-round without re-curation -- round length limits manage staleness.

**Error handling** covers thinking routine timeouts, save file corruption (atomic writes + schema validation), curator failure (deterministic fallback), and research contradictions (surface tension, don't auto-resolve).

**Cost reality:** Up to 24 LLM calls per round-open for a 6-agent session before anyone speaks. Round 1 is cheapest by design.

The spec also flags 6 open items for future work (timeout values, check thresholds, round length limits, save file schema, curator prompt template, intra-team talk mechanics).

Please approve the file write to save it to `output/spec_round_initialization.md`.