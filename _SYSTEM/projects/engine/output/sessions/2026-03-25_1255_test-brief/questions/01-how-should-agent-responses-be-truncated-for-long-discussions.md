# How should agent responses be truncated for long discussions?

*Generated: 2026-03-25 12:58 | Question 1 | 158s | Mode: compete*

## Decisions

### What We Decided (and Why)

**1. Instrument before optimizing.**
No summarization scheme ships until empirical data confirms degradation is real and measurable. The discussion produced strong theoretical arguments on all sides, but no session transcript showing an agent contradicting a prior commitment due to truncation. Engineering against a ghost is cost with no return.

**2. The primary constraint is tokens, not turns.**
Each agent invocation is a stateless CLI call with an explicitly constructed context payload. "Full history" means you are paying real token costs every turn. Size all limits in tokens. Turn count is a proxy metric — acceptable for logging, not for architecture decisions.

**3. Ship a hard token limit as the baseline.**
Until instrumentation establishes a real failure shape, the default behavior is: pass full history up to a fixed token ceiling, then hard-stop. No compression, no summarization, no routing complexity. The ceiling is honest about what it discards.

**4. Role-differentiated memory is an experiment mode, not infrastructure.**
The asymmetric summarization proposal is theoretically sound and testable. It belongs in the experiment modes system, not the base flow. It is not promoted to baseline until the uniform-summary baseline is proven insufficient.

---

## Behavior Rules

### Truncation Trigger
- Measure input token count per agent call at construction time, before dispatch.
- Trigger truncation when the assembled context payload exceeds the configured `context_token_limit`.
- Do not trigger on turn count. Turn count may be logged alongside token count but does not gate truncation.

### Default Truncation Strategy: Hard Limit
- Drop oldest turns until the payload falls within the token limit.
- Preserve the system prompt and agent role configuration unconditionally — these are never truncated.
- Preserve the most recent N turns verbatim (default: last 8 turns). This number is configurable in `config/defaults.yaml`.
- Everything outside the verbatim window is dropped entirely. No compression.
- Log a structured truncation event: `{ turn, tokens_before, tokens_after, turns_dropped }`.

### Verbatim Window Sizing
- Default: 8 turns.
- Rationale: covers one full propose/critique/evaluate round with buffer. Adjustable based on observed average turn length.
- Do not conflate verbatim window size with context quality. The window exists to maintain local coherence, not to preserve the full decision record.

### What a Hard Limit Discards
This strategy deliberately discards early context when the limit is reached. Known risks:
- An agent may not see a scoping constraint established early in discussion.
- An agent may not see a commitment that was accepted and not repeated.

These are accepted risks at baseline. If they produce visible output failures (see Degradation Definition below), the strategy is revisited.

---

## Instrumentation Requirements

These metrics are collected unconditionally, regardless of whether truncation fires.

| Metric | Description |
|---|---|
| `input_tokens_per_call` | Token count of the assembled context payload sent per agent invocation |
| `turn_number` | Turn index within the session |
| `truncation_fired` | Boolean — did truncation trigger on this call |
| `turns_dropped` | Count of turns removed if truncation fired |
| `session_total_cost` | Cumulative token expenditure across all agent calls in session |

Cost-per-session is a first-class metric. Track the inflection point where token cost grows faster than session length. That inflection point is the calibration target for limit sizing.

---

## Degradation Definition

Before any summarization scheme is evaluated, "degradation" must be operationally defined. A session is degraded if the output contains any of the following:

1. **Contradiction of prior commitment** — The Morning Brief or a generated artifact recommends X when an earlier round explicitly accepted Y as settled.
2. **Re-litigated closure** — An agent raises a question already answered and marked resolved, with no new information.
3. **Missing constraint** — A scoping constraint established in rounds 1–5 is absent from the final artifact without explanation.

Degradation is detected by reviewing Morning Briefs and generated artifacts from near-limit sessions. It is not inferred from token counts alone.

---

## Escalation Path

If instrumentation reveals confirmed degradation:

**Step 1 — Uniform summary baseline.**
One summarization call per truncation event. All agents receive identical compressed history plus verbatim window. Single point of failure is handled by fallback to hard-limit behavior if the summarization call times out or returns malformed output. Evaluate whether Morning Brief quality recovers.

**Step 2 — Role-differentiated summarization (experiment mode).**
If uniform summary is insufficient, implement as an experiment mode: one summarization call per agent per truncation event, with role-specific summarization prompts. Measure cross-agent semantic similarity in proposals as primary quality signal (lower similarity = better role differentiation). Measure cost increase against quality delta. Promote to baseline only if quality gain is confirmed and the operational complexity is justified.

---

## Deferred Questions

These questions were raised but require measurement data before answering:

- At what turn count do current discussions empirically hit the context ceiling?
- What is the average token cost per agent turn across current experiment modes?
- Does the Morning Brief quality hold through 40-turn sessions under current (unconstrained) behavior?

These are answered by running 10 sessions to natural completion with full instrumentation enabled, then reviewing outputs manually against the degradation definition above.

---

## Configuration Surface

All tunable values live in `config/defaults.yaml`. No truncation behavior is hardcoded.

```yaml
context:
  token_limit: 80000          # Hard ceiling for assembled context payload per call
  verbatim_window_turns: 8    # Turns always preserved verbatim (most recent)
  summarization_timeout: 30   # Seconds before summarization fallback fires (when enabled)
  log_token_usage: true       # Enable per-call token instrumentation
```
<!-- complete -->
