# Are between-round activities separate `claude -p` calls per agent?

*Generated: 2026-03-17 21:58 | Question 8 | 244s*

It looks like I need write permission to that output directory. Could you approve the file write?

Here's a summary of what the spec covers -- synthesized from all six panel voices across three rounds:

**11 sections, one authoritative document:**

1. **Core Answer** -- Yes, separate `claude -p` calls. 4-6 per agent, 30-40 per between-round cycle for 6 agents.

2. **Call Sequence Per Agent** -- Four distinct call stages: Save File Write (1 call, canonical checkpoint), Thinking Routine (1-2 calls, agent picks Reflect/Research/Strategize), Intra-Team Talk (1 call, group-read solo-write), LLM Curator (1 call, compresses filtered state into Situation block). BackgroundAgents run in parallel, not counted against agent budget.

3. **Dependency Graph** -- ASCII diagram showing the critical path. Save file is the gateway. Intra-team requires all teammates' save files. Curator requires everything. Parallelization opportunities at each stage.

4. **Token Budget Tables** -- Per-agent (46-84k input, 10-22k output), per-round (276-504k input, 62-133k output), per-session (3.4-6.4M total for 10 rounds including discussion calls).

5. **Cost Constraint** -- The Pragmatist's wall: between-round spend must not exceed discussion round spend. Levers to pull if violated.

6. **Research Budget** -- 2 calls per agent per session, 2k output cap, hard timeout. The only unbounded cost vector, now bounded.

7. **Failure Contract** -- Skip and log at every stage. Save file gets retry; thinking routines don't. Curator falls back to deterministic filter output. No silent corruption.

8. **Write Semantics** -- Six valid mutation sources, all tagged for audit. Agents write only to their own magnitudes.

9. **What Agents Never See** -- Raw magnitudes, other agents' save files, BackgroundAgent actions, audit ledger, curator reasoning.

10. **Open Items** -- 11 items consolidated from this and predecessor specs, 4 blocking.

11. **Design Rationale** -- Why separate calls (provenance), why save file is isolated (contamination risk), why Research is capped (damage radius), why 5-10% survival rate is correct (lossy by design).