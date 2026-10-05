## What breaks

1. **The path ships behaviour changes, and the instrument that would show whether they worked comes last or never.** The Evaluator scores design docs and transcripts, but nothing reads the scores back. The roadmap lists "how does evaluation feed back" as an open question. Anti-sycophancy detection, the only measure of blind versus revealed drift, is step 6 and "measurement only". With 17 sessions on disk and no baseline or before/after comparison, three months from now nobody can show blind proposals, takeaways or stale detection improved anything. Nobody has checked that the Evaluator itself is trustworthy.

2. **The phase system is estimated at 2-3 days but is an unscoped dependency that stalls steps 4-6.** The roadmap's open questions leave the transition trigger (time, convergence or round count) undecided, as well as the boundary with moderator input. implementation-gaps.md labels phases "Large -- full design + implementation" and scopes v1 to single-phase. Key takeaways ("at phase boundaries") and stale detection ("across phase boundaries") both need them. Fixed-round modes already behave like phases, and nobody says what phases add.

3. **"Suppress prior context" in blind proposals is undefined, so the 1-2 day estimate and the blindness itself are unreliable.** Each turn's context includes the decisions ledger, previous design-doc headings, open questions and brief context. The roadmap does not say which of these a blind proposer may see. On question two onward, the ledger and carried-forward items can leak earlier conclusions into a supposedly blind round. The budget enforcer, which trims unprotected sections, could also silently reintroduce or drop context. Between rounds agents already see only 3-sentence Position Summaries, so how much blind mode changes is itself unclear.

4. **Anti-sycophancy detection measures drift that the engine's own summaries confound.** Position Summary compression changes what agents see between rounds, so measured drift is mixed with lossy summarisation. The step also depends on blind proposals being clean, which the roadmap admits is easier with phases. Nobody has defined what drift counts as sycophancy.

5. **The ledger foundation is untested.** The synthesis template was never rendered before 2026-10-05, so no earlier session has a real ledger. Takeaways, stale detection and drift all assume trustworthy DECIDED / CONTESTED / OPEN chaining. The first real sessions will probably surface ledger bugs rather than exercise the roadmap items. The 17 existing sessions predate the ledger, so there is also no evidence of the repetition that stale detection is meant to catch.

6. **Several steps rest on a design that does not match the running engine.** The supporting gap specs describe `live_conversation.py` chat mode, with voting side-channels, orchestrator cadence and footers. The engine is C# with fixed rounds and one synthesis call. Takeaway voting (5 blocking `claude -p` calls per proposal, with the voting prompt in Gap 1 still unwritten) has no obvious home in it, so expect rework mid-build.

7. **Manifest versioning is justified by a schema that is not shown to exist.** "Schema evolution" assumes a manifest with consumers, which the packet does not describe. A half-day item could quietly become the place where phase and takeaway schemas are fixed too early.

8. **The BIT "parallel track" is not parallel for one developer, and the invisible steps never change what the reader sees.** Parallel work just means the critical path slips. Steps 2, 5 and 6 are schema, signals and measurement, which a brief reader would not notice, against the roadmap's own rule of starting with what changes what the user reads. Stale and takeaway thresholds also need many runs to tune, and sessions are only run occasionally.

## Undecided

- Which context sections (ledger, prior headings, open questions, brief) a blind proposer sees on later questions.
- The phase transition trigger and its boundary with moderator input, given that Gap 3 says v1 stays single-phase.
- Whether Evaluator scores will ever be read back, and what success metric applies to each of the six steps.
- What counts as sycophancy drift, and how to separate it from Position Summary compression effects.
- Whether measurement (the Evaluator, drift detection) comes before the behaviour changes.
- Whether BIT is real capacity or deferred until the main path is done.
- Whether the gap specs get rewritten for the C# round-based engine before steps 4-6.

## Questions for you

- What outcome would make you call V2 a success: better design docs or a measurable research instrument?
- Do you trust the Evaluator enough to use it as the baseline across the 17 existing sessions?
- Does a manifest exist today, and what would versioning it protect?
- Is the target a single-sitting overnight run or multi-phase sessions?
- What single change would the Morning Brief reader notice first?
- Should the Evaluator be allowed to change persona behaviour?
