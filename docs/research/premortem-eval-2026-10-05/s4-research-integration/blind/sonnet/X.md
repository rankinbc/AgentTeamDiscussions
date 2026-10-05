## What breaks

1. **Research findings get trimmed away or crowd out the discussion.** The engine's budget enforcer trims "unprotected" sections at ~10k tokens, while the context-assembly template assumes a 4,000-token ceiling with its own protected list, and research is in neither. If findings are unprotected they are cut exactly when the payload is large; if protected they displace the ledger or history. research-scope-controls allows 2k output per call and 2 calls per agent, so six agents could add up to 24k tokens per session.

2. **Findings vanish at the round boundary, so the critique and evaluate rounds debate without the evidence.** Between rounds agents see only 3-sentence Position Summaries, and a mid-round result reaches only later speakers. Nothing says whether findings are persisted, cached per session (as research-engine.md claims, though every turn is a stateless `claude -p` call) or re-injected. The scope-controls ROI signal ("did the agent use it next round") would then read near zero.

3. **Unverified findings become DECIDED ledger lines and propagate forward.** The ledger chains across questions and never produced a real one before 2026-10-05. A wrong web snippet cited by one persona can harden into a decision with no provenance, and nothing marks a finding as sourced, disputed or expired. The Evaluator scores output but nothing reads the scores back, so nothing catches it.

4. **The trigger is unbuilt and unreliable.** research-engine.md fires on an agent footer signal `needs: more-research`, but the template's own open prerequisite (a 50-call, 90% footer-compliance test) has not been run. Scope-controls says failed research is "skip and log", so a parse failure, a timeout, a hallucinated citation and a real "no" all look the same: the debate proceeds as if research never happened.

5. **The cost and scope numbers describe a system that does not exist.** The 15k in, 2k out, 2 calls and ~204k tokens (3-4% of 6.4M) figures come from a panel transcript (it opens with "I need write permission"), not from measurement. It explicitly excludes result integration, which is this open question, and lists 2 blocking items. Nobody can say what a "research call" is in this engine: a fourth subprocess, a tool inside a turn, or a pre-session step.

6. **Research placed before a speaker anchors them and undermines blind proposals.** ROADMAP ranks blind proposals as the highest-value item. Injecting findings into the propose round, with sequential speakers, makes the result an authority anchor and suppresses diversity. The plan does not say which wins.

7. **It is built before the base it needs, and there is no way to tell if it helped.** Research Engine is not on the ROADMAP critical path (blind proposals, phases, takeaways, stale detection). There is no phase system, moderator channel or live synthesis to attach results to. With 17 sessions and no real ledger, every number is tuned against zero data. The only value signal is the scope-controls "did the agent use it" metric, which nothing ties to what the user reads in the design doc.

## Undecided

- Where findings enter the payload: system prompt, a protected section, or attached to a claim or ledger entry.
- Which ceiling governs, 4k or ~10k, and whether the research block is protected.
- Whether research runs as a pre-session step, a between-round step, or an agent-triggered mid-turn call, and whether it blocks the turn or arrives a round late.
- Whether findings are shared with all agents or only the requester, and how they survive past Position Summaries.
- Whether research enters the propose round or only critique and evaluate.
- Whether a finding can ever enter the ledger, how it is marked (sourced, disputed, expired), and who wins if it contradicts a DECIDED line.
- Whether research output is evidence attached to a claim or a participant that speaks.
- Failure behavior beyond "skip and log", including what a hallucinated or timed-out result does to the round.
- Whether this waits until the ledger works across one real multi-question session.

## Questions for you

- Is the 204k-token research spend per session acceptable for a project where sessions are run occasionally?
- What would count as success: a different design-doc paragraph, a different reader outcome, or a measurable score change?
- Do you want to run the footer compliance test before building the `needs: more-research` trigger?
- Should blind proposals and phases ship first, as the ROADMAP critical path says?
- Is there a baseline run you can compare against to tell whether research changed any output?
