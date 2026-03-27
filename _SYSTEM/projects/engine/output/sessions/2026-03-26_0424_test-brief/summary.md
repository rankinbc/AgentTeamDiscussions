# Morning Brief: 2026-03-26_0424_test-brief

*Generated: 2026-03-26 04:28*

# Overnight Design Session Summary: Context Management System

## What Was Designed

The session designed a **context management system** for the multi-agent discussion engine — specifically how agents receive conversation history as sessions grow long. This addresses the core problem of fitting meaningful context into finite LLM token budgets across multi-round discussions.

---

## Key Decisions (24 decided, 3 deferred)

### Architecture: Uniform Sliding Window + Scaffold

The teams converged on a **uniform sliding window** approach: every agent sees the same truncated history plus a persistent structured scaffold. Per-agent filtering was explicitly deferred to V1-later.

**Context is assembled fresh every round** in this fixed order:
1. **Scaffold** — append-only structured memory
2. **Summary** — rolling compression of older discussion
3. **Sliding window** — last N rounds of raw messages
4. **Role prompt + round instructions**

### The Scaffold (Structured Memory)

A plain markdown document with four append-only sections:
- **Decisions** — what's been decided
- **Open tensions** — unresolved disagreements
- **Current question** — what's being discussed now
- **Constraints** — hard boundaries

Key properties:
- Flat lists, no nesting — kept deliberately simple
- Two density modes: `compact` (≤300 tokens) and `full` (≤800 tokens), controlled by `scaffold_detail` in `defaults.yaml`
- `full` is auto-selected when briefs have >5 open questions or `--eval` mode is active
- Also recommended for overnight runs where Morning Brief quality matters most
- **Doubles as Morning Brief source material** — the final scaffold feeds directly into the morning deliverable

### The Summary (Rolling Compression)

- Synthesizer compresses the *outgoing* window messages plus the prior summary — never re-reads full history
- Capped at **1,500 tokens** via config
- Separate concern from scaffold — both are synthesizer output fields, not separate subsystems

### Sliding Window

- **Rounds-based**, not message-count-based — round boundaries carry semantic meaning
- Default: **last 2 rounds**, configured via `history_window_rounds` in `defaults.yaml`

### Safety Rails

| Guard | Behavior |
|---|---|
| **Scaffold corruption check** | Hashes decisions list each round; halts with `SCAFFOLD_CORRUPTION` if any decision disappears |
| **Scaffold compaction** | Fires when scaffold exceeds 30% of context budget; merges decisions, drops resolved tensions |
| **Compaction failure** | Session halts, scaffold written to disk for manual review |
| **Summary drift check** | Compares scaffold decisions against summary; logs `DRIFT_WARNING` if a decision keyword is absent for 2 consecutive rounds (non-halting) |
| **Budget pressure** | If remaining budget <2,000 tokens → reduce window by 1 round → force compaction → halt if still over |
| **Token budget logging** | Logs scaffold, summary, window, and remaining budget every round |

### Implementation Approach

- **No new engine components** — truncation is handled as a template concern using existing Jinja2 infrastructure
- **One config surface** — all knobs in `defaults.yaml`, no per-agent configuration
- Engine passes `scaffold`, `summary`, and `window_messages` as template variables; templates control layout

---

## Deferred Items (3 open questions)

| Item | Trigger to Revisit |
|---|---|
| **Per-agent role-filtered windows** | Data showing agents lose coherence on role-specific points despite uniform windows |
| **On-demand full-history retrieval** | Sessions regularly exceed 10 rounds with scaffold corruption events |
| **Semantic relevance filtering** | Scaffold compaction fires >1× per session on average across 20+ runs |

---

## Implementation Impact

**Files likely affected:**
- `config/defaults.yaml` — new keys: `history_window_rounds`, `scaffold_detail`, `summary_max_tokens`, budget thresholds
- `templates/prompts/*.md.j2` — new template variables for scaffold/summary/window assembly
- Synthesizer output — needs to produce scaffold fields and rolling summary
- `session/runner.py` — Morning Brief reads final scaffold + last synthesis instead of full transcript

**What stays unchanged:** No new engine components, no per-agent config, no changes to discussion round orchestration logic.
<!-- complete -->
