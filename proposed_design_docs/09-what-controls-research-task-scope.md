# What controls research task scope?

*Generated: 2026-03-17 22:01 | Question 9 | 180s*

It looks like I need write permission to save the file. Could you approve the file write to `output/spec_research_scope_controls.md`?

Here's what the synthesized spec covers -- 11 sections distilled from all six panel voices across three rounds:

**Core decision: Four-layer control stack, three mechanical, one design-time.**

1. **Control Stack** -- Ordered by impact: question specificity (highest leverage), input token cap (15k), output token cap (2k), call count (2/session). No time limits, no word limits.

2. **Question Specificity** -- The real scope control. The thinking routine that triggers research must produce a single focused query. No separate validation gate (costs 12 extra calls per session). Instead: tighten the source prompt, log questions, monitor truncation rates.

3. **Input Token Cap** -- Locked at 15k, not a range. This is the hidden cost lever everyone almost missed. The orchestrator physically controls what goes into the call.

4. **Output Token Cap** -- 2k via `max_tokens` API parameter. The only constraint enforced mechanically by the API itself.

5. **Call Count Cap** -- 2 per agent per session (not per round). Per-session prevents "use it or lose it" behavior.

6. **Cost Envelope** -- ~204k tokens total research spend per session, ~3-4% of projected 6.4M budget. Only holds if all three mechanical caps hold.

7. **Failure Behavior** -- Skip and log. No retry for research (unlike save files). Truncation at 2k is logged as a quality signal.

8. **Observability** -- Six logging points including the key ROI signal: did the agent actually use the research result in the next round?

9. **Scope Exclusions** -- Research prompt template, tool access, and result integration are separate design items.

10. **Design Rationale** -- Why no gate, why 15k not higher, why per-session not per-round, why 2k is enough.

11. **Open Items** -- 11 items consolidated, 2 blocking (curator prompt versioning, thinking routine templates).