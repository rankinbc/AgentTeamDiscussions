1. **The feedback loop got built, and the user never noticed a difference in the Morning Brief.** Per the Oracle's rule, the moment that matters is what the Morning Brief says. The packet says nothing reads scores back, and the Morning Brief is "the only artifact the user actually reads" (v1-spec-gaps, Q1). Three months on, scores moved but the brief read the same. The doc never names the user moment that eval feedback improves. Would the user notice if it were removed? Probably not.

2. **Scores are not comparable, so any feedback tuned on them chased noise.** v1-spec-gaps Q7 says the LLM judge invents its own dimensions and scores are not comparable across runs. The engine facts still describe a judge scoring 1-10 on fixed dimensions, with no baseline. With 17 sessions on disk, mostly produced before a real ledger existed (the synthesis template was never rendered until 2026-10-05), the training signal is largely junk. Changing persona behavior on a one-point swing from a judge with no calibration is superstition.

3. **Auto-edited personas became unreadable.** The persona YAML is static and hand-edited today. If eval results inject themselves into prompts, the user can no longer tell why an agent said what it said. That is exactly the "cannot understand why the agents said what they said" failure. The solo developer gets a config that drifts and no diff to review.

4. **The feedback optimized the judge's taste, not the spec's usefulness.** The roadmap's own principle is that mechanisms must pass the Morning Brief test. A rubric on design-doc dimensions rewards thorough, well-structured output, which the Oracle calls "thorough but unreadable". Agents learn to write for the evaluator. This is the same trap the behavior-philosophy doc flags: framing changes, not thinking.

5. **It collided with the context budget and cost more than it earned.** Every turn is already squeezed toward ~10k tokens, and the budget enforcer trims unprotected sections. Adding "last session's weaknesses" either got trimmed silently or displaced the ledger or open questions that actually carry coherence. Nobody checked which.

6. **It was built ahead of its dependencies.** The roadmap's critical path puts blind proposals and phases first. Eval feedback is not on that path, and sessions run only occasionally. With so few runs, there is no loop to close. The loop was built, then abandoned for lack of sessions.

**Undecided, and only the author can answer:**
- Which concrete user moment does feedback improve: the brief, the spec, or the persona? Pick one.
- Is the feedback human-in-the-loop (suggested YAML edits the author approves) or automatic? Both Oracle and author-trust arguments favor suggestions only.
- Will the author actually run enough sessions per month to make a loop meaningful?
- Does a rubric score count as success, or does the author's own judgment of the brief?
