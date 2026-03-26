# How should agent responses be truncated for long discussions?

*Generated: 2026-03-26 04:24 | Question 1 | 140s | Mode: compete*

## Decisions

### D1: Uniform Sliding Window — Adopted
All agents see identical history. No role-stratified differentiation. Rationale: eliminates debugging complexity (failures reproduce with identical context), requires no role taxonomy in config, prevents manufactured self-contradiction from asymmetric gaps.

### D2: Smart Summarization — Deferred
LLM-based summarization before each agent call adds a second failure point, latency, and a lossy transformation. Deferred to Phase 2 pending evidence that uniform windowing degrades Morning Brief quality.

### D3: Role-Stratified Windows — Deferred
Theoretically interesting (transactive memory, selective attention) but operationally unsound today. No role taxonomy exists in `experiment_modes.yaml`, debugging surface goes combinatorial, and proposers with context gaps will self-contradict. Revisit only with measured quality data showing uniform windows produce inferior output.

### D4: Three Pinning Rules
1. **Pin Round 1** — the brief anchors all reasoning. Always included regardless of window size.
2. **Pin the most recent synthesis turn** — serves as compressed running state of accumulated decisions. Zero additional LLM cost (already generated). Prevents self-contradiction across all window sizes.
3. **Sliding window of last N rounds** — configurable, default N=3.

### D5: Omission Markers — Adopted with Count
Dropped rounds are replaced with `[N rounds omitted]` (e.g., `[3 rounds omitted]`). Never silent. Cost: ~2 tokens. Value: agents modulate confidence when they know how much context they lack; developers can trace what was excluded.

---

## Behavior Specification

### Token Budget Calculation

At session start, compute `available_history_tokens` once:

```
available_history_tokens = model_context_limit
    - system_prompt_tokens
    - agent_persona_tokens
    - brief_tokens
    - response_reserve
```

This value is static for the session and determines when truncation activates.

### Truncation Logic (per agent call)

```
1. Measure total history tokens.
2. If total <= available_history_tokens → send full history. No truncation fires.
3. If total > available_history_tokens →
   a. Always include: Round 1 (brief).
   b. Always include: Most recent synthesis turn.
   c. Always include: Last N rounds (N = history_window_rounds from config).
   d. Drop all other rounds.
   e. Insert marker: "[X rounds omitted]" at the drop boundary.
```

Steps 3a–3c may overlap (e.g., the most recent synthesis *is* within the last N rounds). Deduplicate; never send a round twice.

### Prompt Assembly Order

```
1. System prompt + agent persona
2. Round 1 (brief / "What's Already Decided" + "Open Questions")
3. [X rounds omitted] marker (if any rounds dropped)
4. Pinned synthesis turn (if outside the sliding window)
5. Last N rounds in chronological order
6. Current-turn instruction
```

### Expected Token Budget (N=3 default)

| Component | Estimated Tokens |
|---|---|
| Pinned Round 1 (brief) | ~500 |
| Pinned last synthesis | ~800 |
| Sliding window (3 rounds) | ~3,000 |
| **Total history cost** | **~4,300** |

Leaves 80%+ of the context window for system prompt, agent persona, and response generation.

---

## Configuration

Single value in `config/defaults.yaml`:

```yaml
history_window_rounds: 3
```

No additional schema, no role mappings, no per-agent overrides. One knob.

---

## Rules

1. **No truncation when unnecessary.** If history fits, send all of it. The sliding window is a fallback, not a default mode.
2. **Round 1 is permanent.** It is never dropped, regardless of token pressure.
3. **Last synthesis is permanent.** It is never dropped. If no synthesis turn has occurred yet, this rule is a no-op.
4. **Drops are visible.** Every omission produces a marker with the count of rounds removed.
5. **Window is uniform.** Every agent in a given round sees identical history. No exceptions.
6. **Measure before differentiating.** Role-stratified windows and smart summarization are Phase 2 — gated on measured Morning Brief quality degradation at N=3.

---

## Open for Phase 2

| Candidate | Gate Condition |
|---|---|
| Role-stratified windows | Morning Brief quality scores degrade as sessions exceed 6+ rounds with uniform N=3 |
| LLM-based summarization | Token budget becomes insufficient after adding new prompt features (e.g., prior_specs chaining) |
| Configurable per-mode window sizes | Users request longer windows for specific experiment modes |
| Retrieval-augmented history | Agent count or round count grows beyond what sliding windows can service |
<!-- complete -->
