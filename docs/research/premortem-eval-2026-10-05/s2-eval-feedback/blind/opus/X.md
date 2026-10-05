## What breaks

1. **The feedback loop tuned agents against noise, because the scores were never stable enough to act on.** v1-spec-gaps #7 says the judge invents its own dimensions and "scores are not comparable across runs". Nothing in the roadmap fixes that before the loop is built. With 17 sessions on disk and runs that happen only now and then, each behavior change was driven by one or two noisy 1-10 numbers.

2. **Scores could not be traced to any agent, so the loop changed the wrong personas.** Design-doc scores rate the output of one synthesis call, and transcript scores rate the whole session (engine facts). Neither says which persona caused a weak doc. So the feedback was either the same for every agent, which changes no one's behavior, or blame was guessed from heuristics, which nobody can check.

3. **Agents converged on what the judge likes, which killed the friction the project exists for.** An LLM judge rewards docs that are coherent, complete and in agreement. Feeding that back pushes personas toward polished consensus. This directly breaks Principle 1, "genuine friction over theatrical opposition", and the Morning Brief test. The agents in agent-behavior-philosophy.md also concluded that showing an agent its own scores "produces confabulation, not introspection".

4. **The feedback was cut from context or crowded out what mattered.** Each turn already carries persona, lens, overlay, brief, the ledger, prior-doc headings, carried-forward open questions and the discussion, all under a ~10k-token enforcer that trims unprotected sections (engine facts). If the feedback was left unprotected, it was silently dropped. If it was protected, it squeezed out the discussion and ledger.

5. **The baselines were invalid from the start.** Before 2026-10-05 the synthesis template never rendered, so no earlier session had a real ledger (engine facts). Every historical score measures a different engine. Any "improvement" after the loop shipped partly reflects the ledger fix, not the feedback.

6. **Auto-edited personas drifted and could not be reproduced.** Persona YAML is static and edited by hand. Once evaluation wrote changes into it, or into an overlay, sessions were no longer repeatable. Manifest versioning and agent-identity snapshots were still unbuilt (ROADMAP critical path; agent-identity idea). Hand edits returned.

7. **It was built off the critical path and abandoned.** The ROADMAP critical path (blind proposals, phases, takeaways, stale detection, anti-sycophancy) does not include evaluation feedback. The user reads the Morning Brief, not the evaluator report. A solo developer spent days on infrastructure whose payoff could only appear across many sessions, so it was dropped.

## Undecided

- What the loop is meant to change: persona YAML, a per-session overlay, private idea inventories, mode/round structure, or only the human's hand edits.
- Whether the judge gets fixed first (fixed dimensions, extraction by dimension name, repeat-scoring for variance).
- How a doc or transcript score is assigned to an individual persona, if it is assigned at all.
- Which signals feed back: judge scores, or behavioral measures already planned (blind-vs-revealed drift, stale detection, retraction counts).
- Whether feedback is a protected context section, how many tokens it gets, and what it displaces.
- Whether persona changes are versioned, reviewed by the human before they apply, and reversible.
- How "better" is shown: the evidence threshold, and whether the 17 pre-ledger sessions are excluded from the baseline.
- How the loop guards against convergence on the judge's taste, for example scoring originality or penalizing agreement.

## Questions for you

- Do you want evaluation to change agents automatically, or to tell you which personas to hand-edit?
- What is the one outcome that would show the loop worked: a better Morning Brief, more divergence, or higher rubric scores?
- Do you trust the current judge enough to act on its scores, or does fixing the dimensions come first?
- Should agents ever see their own scores, given that your agents concluded this produces confabulation?
- Does this come before or after blind proposals and the phase system on your build order?
- How many sessions will you realistically run in the next three months to produce feedback data?
