## What breaks

1. **The loop tunes agents against a judge nobody has shown to be stable, so changes chase noise.** docs/v1/v1-spec-gaps.md item 7 says the LLM judge invented its own dimensions and scores were not comparable across runs. The engine facts say it now scores 7 and 10 fixed dimensions on a 1-10 scale, but nothing in the packet shows run-to-run variance has been measured. A persona edit triggered by a 6 versus a 7 may be a coin flip.

2. **A low score cannot be attributed to a persona, so edits hit the wrong cause.** A design-doc score depends on the brief, the question, the synthesis template, ledger carry-forward, 3-sentence Position Summaries between rounds, the ~10k-token budget trimming, and the whole team. The roadmap item and open question never name the unit of feedback (persona, team, mode, template or context assembly). With occasional solo sessions, each change gets a sample of one.

3. **There is no usable baseline, so no one can tell whether feedback helped.** The synthesis template was never rendered before 2026-10-05, so none of the 17 sessions on disk has a real ledger. Any improvement after the fix may be the fix itself. Before/after comparisons mix different pipelines.

4. **Injecting scores into prompts repeats a pattern the project's own research rejected.** agent-behavior-philosophy.md records agents saying "none of these change my behavior, they change my framing". It also records the finding that feeding agents their own scores produces confabulation, and that forced behavior produces theatre. Scores in prompts also compete for the budget the enforcer already trims, and it is unspecified what gets trimmed first or whether the ledger and open questions get displaced.

5. **Optimizing the rubric Goodharts the Morning Brief test.** The rubric rewards structure and completeness of design docs. The Morning Brief is the only artifact the user reads (v1-spec-gaps Q1), and the Evaluator does not score it. Agents tuned toward the rubric drift toward agreeable, rubric-shaped prose. Scores could rise while the brief gains no new ideas, and no human rating would reveal it.

6. **Automatic persona changes break reproducibility and legibility.** Persona YAML is static and hand-edited today. Auto-edits or injected feedback make sessions incomparable over time and hide why an agent said what it said. The session snapshots proposed in agent-identity-and-resolution are not built, and there is no diff to review.

7. **The item is not on the roadmap's critical path and sessions are infrequent, so the loop may never close.** The critical path lists blind proposals, manifest versioning, phases, takeaways, stale detection, anti-sycophancy and BIT, and none involves evaluation. The evaluator is already written and unread today. A solo developer building the other items first leaves it unread.

## Undecided

- Whether feedback is automatic (scores edit or inject into prompts) or human-in-the-loop (report read, YAML edited by hand, or suggested edits the author approves).
- The unit that feedback changes: persona, team, mode, template or context assembly.
- Whether the judge is calibrated, for example by scoring the same document repeatedly.
- Which of the 17 sessions, if any, count as valid baselines after the ledger fix.
- The success measure: rubric score movement, or the author's own judgment of the Morning Brief.
- The abandonment criterion: what result would end the effort.
- Where the item sits against blind proposals and the phase system.

## Questions for you

- Which concrete moment does feedback improve: the Morning Brief, the design doc, or persona quality?
- Has the judge ever been run twice on the same document, and how far did the scores differ?
- Why are the existing evaluator reports not being read and used to edit personas by hand today?
- How many sessions will you realistically run per month to feed a loop?
- What independent signal of a better session do you trust other than the LLM judge?
