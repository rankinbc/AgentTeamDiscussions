## What breaks

1. **The plan is built from specs written for a different engine, so steps 3-6 hit design work nobody budgeted.** implementation-gaps.md describes phases, takeaways and voting against `live_conversation.py` chat mode: 25-turn sessions, per-turn footers and a cadence orchestrator. The real engine is C#, runs fixed rounds per question, and makes one synthesis call (engine facts). Every estimate after step 2 assumes a spec that has to be translated first, and that translation is not on the roadmap.

2. **The phase system blows its 2-3 day estimate and stalls the whole chain.** implementation-gaps.md Gap 3 calls it "Large -- full design + implementation". The roadmap's own Open Questions have not settled how transitions are triggered or where moderator input ends and auto-transition begins. Modes already define a round sequence (propose -> critique -> evaluate). Phases either repeat that idea under new names or require a rewrite of the round loop. Steps 4-6 all depend on "phase boundaries", so a slip here halts everything after it.

3. **Blind proposals ship but do not visibly change what the user reads.** Between rounds the engine already hides prior rounds except for 3-sentence Position Summaries. Blindness only changes within-round visibility in the propose round. The user reads the synthesized design doc, and a single synthesis call can flatten any added diversity. "Highest immediate user value" (ROADMAP) is asserted without any measurement. It is also unclear what "suppress prior context" removes: the ledger, the earlier doc's headings and the carried open questions are themselves prior context.

4. **No baseline exists, so nobody can tell whether any step helped.** The ledger was broken in all 17 sessions before 2026-10-05, the Evaluator's scores are never read back, and sessions run only occasionally (engine facts). Blind-proposal value, stale detection and drift measurement all need before/after comparison, and there is neither a clean "before" nor enough runs.

5. **Steps 5 and 6 produce measurements that nothing consumes.** Both are "measurement only". Persona YAML is static and hand-edited, and evaluation feedback is still an open question (ROADMAP). The drift signal is also confounded: the "revealed" condition only sees compressed 3-sentence summaries, so measured drift reflects the summarizer as much as sycophancy. That is four days of detectors with no lever attached.

6. **Key takeaways turn out to be two different features.** The roadmap's version is "extraction at phase boundaries", estimated at 1 day. key-takeaway-mechanism is a voting system that is blocked by an unwritten voting prompt (Gap 1). It also adds 30-60 seconds per proposal of blocking side-channel calls (Gap 4) and depends on a footer compliance test that has never been run (Gap 2). Whichever version gets built will contradict the other spec.

7. **Phase injections get silently trimmed.** Phase-specific prompt text adds to a payload that already has nine sections, under an enforcer that trims unprotected sections above about 10k tokens (engine facts). Unless phase text is protected it disappears, and if it is protected it pushes out the discussion history.

8. **"Parallel" BIT does not exist for a solo developer, and moderator input is missing entirely.** One developer means BIT just competes for the same time. Moderator input is a confirmed V2 feature, the cheapest way to steer a session, and is absent from the critical path.

## Undecided

- What "blind" covers: within-round only, or also the ledger, the previous doc's headings and the carried open questions.
- Whether phases replace modes, wrap them, or map onto rounds.
- Phase transition trigger: round count, convergence signal or moderator.
- Takeaways: extraction or voting, which prompt, and blocking or async.
- What the manifest versions, and whether the 17 existing sessions get migrated or are treated as legacy.
- Which success metric judges each step, and whether the Evaluator is that metric.
- Whether phase text is protected from the budget enforcer.
- Where stale and drift signals go: a report, a persona edit, or a live intervention.
- Whether the chat-mode specs (cadence, footers, tombstones) still apply to the C# engine.

## Questions for you

- Was the "Agent Panel Analysis" that produced this order run before the ledger fix, and do you still trust it?
- What specific shortcoming in current design docs are you trying to fix first?
- Would you accept blind proposals if the Evaluator showed no score change?
- Is live moderator steering more valuable to you than automatic phases?
- Do you plan to run enough sessions in the next three months to make drift and staleness statistics meaningful?
- Is chat mode (`live_conversation.py`) dead, or is it a target you still intend to support?
- How much time per week do you actually have for this, and does BIT get any of it?
