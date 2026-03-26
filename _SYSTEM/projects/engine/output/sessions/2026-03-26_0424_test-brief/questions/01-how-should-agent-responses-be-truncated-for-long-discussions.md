# How should agent responses be truncated for long discussions?

*Generated: 2026-03-26 04:27 | Question 1 | 165s | Mode: compete*

## Decisions

1. **Uniform sliding window with structured scaffold** — all agents see the same truncated history plus a persistent scaffold. No per-agent filtering in V1.

2. **Scaffold and summary are separate concerns** — the scaffold is an append-only decisions/tensions list. The summary compresses recent discussion. Both are fields in the synthesizer output, not separate subsystems.

3. **Scaffold serves as Morning Brief source material** — its format is designed for downstream synthesis into the final deliverable, not just for agent context.

4. **Truncation is a template concern** — prompt assembly uses the existing Jinja2 templates to compose scaffold + window + current-round prompt. No new engine components.

5. **One config surface** — all tunable knobs live in `defaults.yaml`. No per-agent configuration.

---

## Context Assembly Rules

Each agent prompt is rebuilt from scratch every round. The assembled context follows this structure, in order:

1. **Scaffold** — persistent, append-only. Contains: decisions made, open tensions, current question, and active constraints. Updated by the synthesizer after each round. Never truncated; compacted when oversized.

2. **Summary** — compressed narrative of discussion history older than the sliding window. Regenerated each round by the synthesizer from prior summary + outgoing window messages.

3. **Sliding window** — the raw messages from the most recent rounds. Identical for all agents.

4. **Role prompt + current-round instructions** — from the agent's YAML definition and the Jinja2 prompt template.

---

## Sliding Window Sizing

- **Default window: last 2 rounds of messages.** This is the minimum for agents to see what they are responding to and what others responded to their prior output.
- **Config key:** `history_window_rounds` in `defaults.yaml`. Integer, minimum 1.
- **Rationale for rounds-based (not message-count-based):** round boundaries are semantically meaningful. A round contains one contribution per active agent plus a synthesis. Message counts vary per mode; round counts do not.

---

## Scaffold Specification

### Contents (append-only fields)

| Field | Description | Update rule |
|---|---|---|
| `decisions` | Numbered list of things the group has agreed on | Append when synthesizer detects convergence. Never remove. |
| `open_tensions` | Active disagreements or unresolved tradeoffs | Add when raised, remove only when resolved into a decision |
| `current_question` | The specific question the next round should address | Replaced each round by the synthesizer |
| `constraints` | Hard requirements surfaced from the brief or prior decisions | Append-only |

### Format

Plain markdown. No nested structure. Each field is a headed section with a flat list.

### Density control

- **Config key:** `scaffold_detail` in `defaults.yaml`. Values: `compact` | `full`.
- `compact` — decisions and tensions as single-line items. Target: under 300 tokens.
- `full` — decisions include one-sentence rationale. Tensions include which agents disagree and why. Target: under 800 tokens.
- **Default:** `compact`. Use `full` when the discussion brief has more than 5 open questions or when `--eval` mode is active (richer scaffold improves evaluation scoring).

### Compaction rule

If scaffold token count exceeds 30% of available context budget, force compaction:
1. Merge any decisions that are subsets of later decisions.
2. Drop resolved tensions (should already be removed, but enforce here).
3. Truncate rationale strings to first clause.

Log a warning when compaction fires. If compaction cannot bring the scaffold under 30%, halt the session and write the scaffold to the session directory for manual review.

---

## Summary Specification

- Produced by the synthesizer alongside the scaffold each round.
- Covers all discussion history older than the sliding window.
- **Max token budget:** available context minus scaffold, window, and role prompt. In practice, cap at 1,500 tokens via config key `summary_max_tokens` in `defaults.yaml`.
- **Generation approach:** the synthesizer receives its own prior summary plus the messages about to leave the sliding window, and produces an updated summary. This is a rolling compression — no full-history re-read.

---

## Failure Detection

### Summary drift check

After each round, compare the scaffold's `decisions` list against the summary text. If any decision keyword is absent from the summary for 2 consecutive rounds, log a `DRIFT_WARNING` with the missing decision text. Do not halt; the scaffold is the authoritative record and agents still see it.

### Scaffold stability check

Hash the `decisions` list after each round. If a decision present in round N is absent in round N+1, halt the session and log `SCAFFOLD_CORRUPTION`. This should never happen under append-only rules; its occurrence indicates a synthesizer prompt defect.

### Token budget monitoring

Log per round:
- Scaffold token count
- Summary token count
- Window token count
- Remaining budget for role prompt + agent response

If remaining budget drops below 2,000 tokens, reduce `history_window_rounds` by 1 for the next round and log `WINDOW_REDUCED`. If window is already at 1, force scaffold compaction. If still over budget after compaction, halt.

---

## Config Surface

All keys in `defaults.yaml`:

```yaml
# Context management
history_window_rounds: 2          # Number of recent rounds in sliding window
scaffold_detail: compact          # compact | full
scaffold_max_budget_pct: 30       # Max % of context budget for scaffold
summary_max_tokens: 1500          # Hard cap on summary length
context_min_remaining: 2000       # Min tokens reserved for role prompt + response
```

---

## Template Integration

Prompt assembly is handled in the Jinja2 templates under `templates/prompts/`. The context assembly order is:

```jinja2
{{ scaffold }}
---
{{ summary }}
---
{{ window_messages }}
---
{{ role_prompt }}
{{ round_instructions }}
```

The engine passes `scaffold`, `summary`, and `window_messages` as template variables. The template controls ordering and delimiters. Changing the assembly strategy means editing the template, not the engine.

---

## What This Design Defers

| Deferred capability | Trigger to revisit |
|---|---|
| Per-agent role-filtered windows | Data showing agents lose coherence on role-specific points despite uniform windows. Requires instrumentation shipping first. |
| On-demand full-history retrieval | Sessions regularly exceeding 10 rounds with scaffold corruption events. |
| Semantic relevance filtering | Scaffold compaction firing more than once per session on average across 20+ runs. |

---

## Relationship to Morning Brief

The scaffold's `decisions` and `open_tensions` fields are the primary input to Morning Brief generation. The Morning Brief synthesizer reads the final scaffold and the last round's synthesis — not the full transcript. This means scaffold quality directly determines Morning Brief quality.

If `scaffold_detail: full` is used, the Morning Brief can include per-decision rationale without re-reading history. If `compact`, the Morning Brief synthesizer must infer rationale from the final-round synthesis only.

Recommendation: use `full` for overnight runs where Morning Brief quality is the primary deliverable. Use `compact` for interactive or exploratory sessions where token efficiency matters more.
<!-- complete -->
