# Morning Brief: 2026-03-25_1304_test-brief

*Generated: 2026-03-25 13:07*

## Overnight Design Session Summary

**Source:** Decisions Ledger (summarized strictly from ledger entries — no external knowledge used)

---

### Session Focus

The session addressed **context management architecture** for the agent discussion system — specifically, when and how to manage growing context windows as sessions run longer.

---

### Key Decisions Made

#### 1. Deferral Decisions (What Was Ruled Out *For Now*)
- **No truncation infrastructure needed yet** — current session lengths (~18,000 tokens) do not make context management an active constraint.
- **Role-stratified retention (four-role taxonomy) deferred** — will not be built until two-mode behavior is validated first.
- **Summarization deferred** — will not be implemented until at least one session demonstrably degrades due to context size.

#### 2. Target Architecture: Two-Mode Model
When context management *does* activate, the design is a **two-mode anchored/accumulating model**:

| Mode | Behavior |
|---|---|
| **Anchored** (default) | Agent receives the original brief in full + last N verbatim turns (default N=4). No synthesized summaries — ever. If the window must shrink, N is reduced rather than substituting summaries. |
| **Accumulating** (opt-in) | Agent receives compressed round summaries and logged decisions. No verbatim debate content. |

- Each agent carries a single `context_mode` field in YAML config.
- Experiment mode role-swapping **retains** the agent's configured `context_mode`; any overrides belong in experiment mode config, not agent config.

#### 3. Activation Trigger
- Context management **activates** when any session log records token usage **exceeding 60% of the active model's context window**.

#### 4. Token Budget Mechanics
- Per-agent context budget is computed **at dispatch time** (not estimated from turn count).
- Formula: `available_tokens = window_limit × 0.80`, minus brief tokens and 2,000 reserved for response.

#### 5. Validation Signal
- **Morning Brief critique section sharpness** is the primary quality signal for validating whether the two-mode model is working.

#### 6. Measurement Plan
- Ten sessions after activation, tracking:
  - Turn-level token counts
  - Threshold crossings
  - Morning Brief critique quality

---

### Open Questions (Unresolved)

1. Whether **critic turns in rounds 3+** introduce new objections not present in rounds 1–2 — to be observed across ten sessions.
2. **Calibration of N** (verbatim turns retained for anchored agents) — pending empirical data from threshold-crossing sessions.
3. Whether the **two-mode assumption holds** after ten sessions, or whether the taxonomy must be expanded.
4. Whether **experiment mode config** will need per-mode `context_mode` overrides for specific agents.

---

### Bottom Line

The session produced a clear, deferred-until-needed architecture: do nothing until the 60% threshold is crossed, then activate the anchored/accumulating two-mode model. The design is intentionally conservative — anchored is the default and "hard" (no silent fallback to summaries), accumulating is opt-in, and the whole system is validated through Morning Brief quality over ten sessions before any further complexity is added.
<!-- complete -->
