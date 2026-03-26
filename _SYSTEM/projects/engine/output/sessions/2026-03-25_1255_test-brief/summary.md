# Morning Brief: 2026-03-25_1255_test-brief

*Generated: 2026-03-25 12:59*

## Overnight Design Session Summary

**Source:** Decisions Ledger (ledger-only extraction)
**Session Focus:** Context management strategy — truncation, token limits, memory, and instrumentation

---

### What Was Decided

The session produced **15 recorded decisions** across four thematic areas:

#### 1. Core Strategy: Hard Token Limits (No Summarization Yet)
- **No summarization ships** until empirical instrumentation first confirms degradation is real and measurable.
- The **primary constraint is tokens**, not turns — all limits are token-sized; turn count is a proxy metric only.
- **Default behavior is a hard token limit**: pass full history up to a fixed ceiling, then hard-stop. No compression or summarization in the default path.
- A **summarization fallback** exists but degrades to hard-limit behavior if the summarization call times out or returns malformed output.

#### 2. Truncation Mechanics
- **Truncation triggers on token count** at context construction time, not on turn count.
- **Most recent 8 turns are always preserved verbatim**; everything outside that window is dropped entirely.
- System prompt and agent role configuration are **never truncated** under any strategy.
- The verbatim window size (8 turns) is **configurable in `config/defaults.yaml`**, not hardcoded.
- A **structured truncation event is logged** with: `turn`, `tokens_before`, `tokens_after`, `turns_dropped`.

#### 3. Configuration
All tunable values live in **`config/defaults.yaml`**:
| Key | Value |
|---|---|
| `token_limit` | `80000` |
| `verbatim_window_turns` | `8` |
| `summarization_timeout` | `30` |
| `log_token_usage` | `true` |

#### 4. Metrics & Degradation Definition
- **Five metrics collected unconditionally** per call: `input_tokens_per_call`, `turn_number`, `truncation_fired`, `turns_dropped`, `session_total_cost`.
- **Cost-per-session is a first-class metric**; the token cost inflection point is the calibration target for limit sizing.
- **Degradation is defined by three observable output failures**: contradiction of a prior commitment, re-litigated closure, or a missing constraint — not inferred from token counts alone.
- **Escalation path** if degradation is confirmed: Step 1 → uniform summary baseline; Step 2 → role-differentiated summarization as an experiment mode.
- **Role-differentiated memory is an experiment mode**, not infrastructure — not promoted to baseline until the uniform-summary baseline is proven insufficient.

---

### What Remains Open

Three questions were explicitly left unresolved:

1. At what turn count do current discussions empirically hit the context ceiling?
2. What is the average token cost per agent turn across current experiment modes?
3. Does Morning Brief quality hold through 40-turn sessions under current unconstrained behavior?

---

### Key Takeaway

The session landed on a **conservative, instrumentation-first posture**: ship the simplest possible mechanism (hard truncation with a verbatim recency window), collect real data, and only escalate to summarization if the data proves it's needed. No architectural decisions were deferred to design docs — all recorded decisions are fully specified in the ledger.
<!-- complete -->
