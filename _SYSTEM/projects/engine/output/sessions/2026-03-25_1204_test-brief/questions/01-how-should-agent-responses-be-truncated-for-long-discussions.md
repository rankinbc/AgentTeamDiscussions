# How should agent responses be truncated for long discussions?

*Generated: 2026-03-25 12:07 | Question 1 | 165s | Mode: compete*

## Decisions

### D1: No LLM-based summarization in v1

Summarization requires a compressor agent that can hallucinate position shifts, flatten genuine disagreement, add latency per turn, and fail silently. Silent failure — where every subsequent agent reasons from a corrupted shared premise — is undetectable from within the discussion and unrecoverable without replaying from the audit log. This failure mode is disqualifying for v1. Summarization is deferred until the simpler approach demonstrably fails on a measurable dimension.

### D2: Window mode is the v1 truncation strategy

Each agent receives the last N turns of discussion history verbatim. No transformation, no compression, no additional LLM calls. This is a pure string-slicing operation with known, bounded failure characteristics: critical framing established early may fall outside the window. This failure is observable from the outside and tunable via window size. It is preferable to failures that are invisible to both agents and operators.

### D3: Truncation occurs at message construction time, per-agent

The truncation point is immediately before the CLI call is constructed for each agent. The stored session file is never modified, trimmed, or summarized. The full session file is the audit log — it records exactly what each agent was constructed to receive at every turn. If truncation behavior must be debugged, the session file is the source of truth. This invariant is non-negotiable.

### D4: History mode is configured per agent in YAML

Each agent YAML file exposes a `history_mode` field. In v1, only `window` is a valid value. The field exists now so the schema supports future modes without structural changes.

```yaml
history_mode: window
window_turns: 10
```

`window_turns` is the number of prior turns passed to the agent. It defaults to a system-wide value if not specified per agent.

### D5: Turns, not tokens, is the unit of measurement in v1

Token-count variation across turns is a real problem: turn N could be 50 tokens or 5,000. However, with structured prompts and consistent agent roles, average turn length is roughly stable, making turns an acceptable proxy. Token budgeting is the more rigorous solution but requires infrastructure (per-turn token counting, dynamic window sizing) that is second-order complexity for v1. The turns-as-proxy assumption should be revisited if discussions show high turn-length variance in practice.

### D6: Role-differentiated history is acknowledged but deferred

The insight that challengers benefit from structural ignorance of the persuasion arc — and that domain specialists benefit from seeing original framing alongside recent claims — is theoretically sound and worth preserving. The `bookends` mode (first turn + last M turns) addresses specialist drift-detection cheaply, with no LLM calls. However, shipping both `window` and `bookends` simultaneously introduces two untested variables. `bookends` is the next mode to implement after `window` is validated.

The full taxonomy (`arc | window | bookends`) remains the design target. `arc` requires summarization and is explicitly deferred beyond v1.

---

## Rules

### R1: The session file is append-only and untruncated

No process may modify, trim, or overwrite a session file that contains completed turns. Truncation is a read-time operation, applied when constructing agent inputs, never a write-time operation applied to stored state.

### R2: Truncation is always per-agent

There is no global truncation applied to a session before it is dispatched. Each agent independently receives history sliced according to its own `window_turns` value. Two agents in the same round may receive different history lengths.

### R3: The original framing prompt is always included

Regardless of window size, the first turn of a session (the original framing or brief prompt) is always prepended to the history slice passed to any agent. This prevents window-mode's primary failure — loss of foundational constraints — without requiring `bookends` mode. If the first turn falls within the window, it is not duplicated.

### R4: Window size has a floor and a ceiling

`window_turns` must be between 2 and 50. Values below 2 produce incoherent agent behavior. Values above 50 are not prohibited by the model but indicate the operator should assess whether session length itself is the problem.

### R5: Truncation events are logged

When truncation occurs — i.e., the session has more turns than `window_turns` — the message construction layer logs: session ID, agent ID, total turns in session, turns passed to agent, and timestamp. This is the instrumentation baseline needed to answer whether truncation is the binding coherence constraint.

---

## Deferred

| Item | Trigger for reconsideration |
|---|---|
| `bookends` history mode | Window mode ships and specialist agents surface original-framing drift in briefs |
| Token-based window sizing | Turn-length variance is measured and shown to exceed 3× average in production sessions |
| `arc` summarization mode | Both `window` and `bookends` are validated and a clear use case for arc-compression emerges |
| Coherence measurement tooling | User feedback signals (brief flagged as repetitive or missing context) cannot be collected behaviorally |

---

## Open Questions

**OQ1:** What is the system-wide default for `window_turns` if not specified per agent? A starting value of 10 is implied by the discussion but not agreed. This should be set before implementation.

**OQ2:** When `history_mode` is absent from an agent YAML, does the agent receive full history or the system default window? Full history is safe but defeats the purpose of the mechanism at scale. System default window is safer operationally but must be documented as a breaking change for any agent currently relying on full context.

**OQ3:** The Adversarial Critic correctly noted that history truncation may not be the binding coherence constraint — prompt design, agent ordering, and turn limits are candidates. The logging in R5 produces data on truncation frequency. Is there a corresponding instrumentation plan for the other candidate constraints, or is this the only variable being tracked?
<!-- complete -->
