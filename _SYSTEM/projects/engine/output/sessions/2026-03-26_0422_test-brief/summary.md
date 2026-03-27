# Morning Brief: 2026-03-26_0422_test-brief

*Generated: 2026-03-26 04:25*

# Overnight Design Session Summary: History Window & Context Management

## What Was Decided (12 Decisions)

### Core Strategy
The team settled on a **uniform sliding window** approach for agent history management. All agents see identical history — no role-based differentiation. This is intentionally simple: one config knob (`history_window_rounds: 3` in `config/defaults.yaml`), no per-agent overrides, no role mappings.

### What Gets Pinned (Always Visible)
- **Round 1** (the brief) is always pinned, regardless of window size
- **Most recent synthesis turn** is always pinned as compressed running state

### Sliding Window Behavior
- Last **N rounds** are kept (default N=3, configurable)
- Window is a **fallback only** — no truncation when history fits within the token budget
- Dropped rounds get **omission markers with count** (`[N rounds omitted]`), never silently removed
- **Deduplication** ensures pinned turns that overlap with the sliding window are never sent twice

### Token Budget
- `available_history_tokens` is computed **once at session start** and held static for the entire session

### Prompt Assembly Order
```
system prompt + persona → Round 1 → omission marker → pinned synthesis → last N rounds → current-turn instruction
```

## What Was Deferred to Phase 2 (4 Open Items)

| Item | Gate Condition |
|---|---|
| **Role-stratified windows** | Morning Brief quality score degrades at 6+ rounds with uniform N=3 |
| **LLM-based smart summarization** | Token budget becomes insufficient after adding new prompt features |
| **Per-mode window sizes** | User requests for longer windows in specific experiment modes |
| **Retrieval-augmented history** | Agent/round count grows beyond what sliding windows can service |

## Key Takeaway

The session produced a clean, minimal design: **one knob, uniform windows, pin the bookends** (brief + latest synthesis). All complexity (role stratification, smart summarization, RAG) was explicitly deferred behind measurable quality gates rather than speculated into the initial implementation. This means Phase 1 implementation should be straightforward — primarily changes to prompt assembly and a new config value in `defaults.yaml`.
<!-- complete -->
