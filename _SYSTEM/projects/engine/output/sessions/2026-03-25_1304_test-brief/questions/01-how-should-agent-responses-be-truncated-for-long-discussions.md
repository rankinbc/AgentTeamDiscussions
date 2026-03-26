# How should agent responses be truncated for long discussions?

*Generated: 2026-03-25 13:06 | Question 1 | 160s | Mode: compete*

## Decisions

### Resolved

1. **Context management is not yet an active constraint.** At current session lengths (~30 turns, mixed 300–600 word responses), total history is approximately 18,000 tokens — well within a 200K context window. No truncation infrastructure is required before empirical data confirms it is needed.

2. **Role-stratified retention (four-role taxonomy) is deferred.** The cognitive independence argument is sound in theory, but building four filter branches before stress-testing real sessions is premature. The four-role model may be revisited once two-mode behavior is validated.

3. **Summarization is deferred.** No summarization logic ships until at least one session demonstrably degrades due to context size. Summarization adds complexity and homogenizes agent knowledge; neither cost is justified without evidence of benefit.

4. **The two-mode anchored/accumulating model is the target design** when context management becomes necessary. It captures the core insight — critics must not drift with synthesis consensus — without requiring a multi-branch routing table.

5. **Morning Brief quality is the primary quality signal.** Coherence metrics, semantic distance scores, and turn-level analysis are secondary. If the critique section of the Brief sharpens under anchored mode, that is sufficient evidence to keep it. If it does not, the mode is not earning its complexity.

---

## Context Management Design (to be activated at threshold)

### Activation Condition

Context management activates when any session log records token usage exceeding **60% of the active model's context window**. Below that threshold, agents receive full session history.

Log token counts per session turn. When the threshold is crossed for the first time, the data captured (turn distribution, per-agent verbosity, session phase at crossing) informs calibration of the two-mode parameters.

### Agent Modes

Each agent carries a single field in its YAML config:

```yaml
context_mode: anchored   # or: accumulating
```

**Anchored** agents receive:
- The original discussion brief in full
- The last N turns verbatim (N is a configurable integer; default: 4)
- No synthesized summaries

**Accumulating** agents receive:
- Compressed round summaries (one paragraph per completed round)
- Logged decisions and open questions
- No verbatim debate content

Anchored is the default. Accumulating is opt-in for roles whose function is specifically to track progress across the full arc of a session (e.g., synthesizers, session-level evaluators).

### Hard Constraint on "Anchored"

Anchored is a hard selection rule, not a preference. An anchored agent **never** receives synthesized summaries mixed into its context window, even if total token count is high. If the verbatim window must shrink to fit, reduce N (turns retained) — do not substitute summaries. This preserves critic independence at the cost of recency, which is the correct tradeoff.

### Turn Budget Calculation

The per-agent context budget is computed at dispatch time:

```
available_tokens = window_limit × 0.80
reserved_for_response = 2,000 tokens (fixed)
history_budget = available_tokens − brief_tokens − reserved_for_response
```

For anchored agents: fill history_budget from most recent turns, dropping oldest first.  
For accumulating agents: fill history_budget with round summaries, oldest first.

Do not assume uniform turn size. Measure actual token counts at the time of dispatch.

### Turn-Size Variance

Proposal turns are approximately half the length of critique turns. Any buffer calculation that assumes uniform turn size will be off by up to 2×. The dispatch-time budget calculation above handles this correctly because it measures actual token counts rather than estimating from turn count alone.

---

## Agent YAML Interface

Add one field to the agent definition schema:

```yaml
context_mode: anchored | accumulating   # default: anchored
```

No other agent-config changes are required to support the two-mode system.

`experiment_modes.yaml` role-swapping is compatible with this model. When an agent plays a different role in a given mode, it retains its configured `context_mode`. If a specific mode requires a different context behavior for a particular agent, that override is expressed in the experiment mode config, not the agent config.

---

## Deferred Items

| Item | Reason Deferred |
|---|---|
| Four-role taxonomy (Proposer / Critic / Synthesizer / Implementer context filters) | No implementer role exists; adds routing complexity before two-mode is validated |
| Summarization engine | No session has required it; cost is homogenized knowledge |
| Semantic distance measurement | Useful for research; not required for product decision |
| Sliding window as default | Silently breaks critic continuity; two-mode anchored is strictly better when activation is needed |

---

## Measurement Plan

Run ten sessions after two-mode context management activates. For each session:

- Log token counts per turn and per agent
- Record which turn (if any) crossed the 60% threshold
- Read the Morning Brief critique section: does the same objection appear more than once rephrased?
- Note whether critic turns in rounds 3+ introduce objections not present in rounds 1–2

If Morning Brief quality does not improve under anchored mode after ten sessions, revisit the two-mode assumption before expanding the taxonomy.
<!-- complete -->
