1. **The loop got built on scores nobody trusts, and it tuned personas to noise.** v1-spec-gaps item 7 admits the LLM judge invents its own dimensions and scores are not comparable across runs. The engine facts say the Evaluator scores 1-10 with an LLM judge, and nothing validates it. Feeding that back means the plan optimizes against a ruler that changes length. The unstated assumption is that a one-point move means something. With 17 sessions on disk and no repeat runs of the same question, nobody knows the judge's variance. A feedback loop on an uncalibrated judge is a random walk.

2. **The loop could not be attributed to anything, so every persona edit was a guess.** A design-doc score is the product of the brief, the question, the synthesis template, ledger carry-forward, budget trimming at ~10k tokens, and five or more personas. Nobody has explained how a low "specificity" score maps to a change in one persona's YAML. Roadmap item 5 and the open question never name the unit of feedback: persona, team, mode, or template. Solo developer, sessions "run occasionally": the sample size per change is one.

3. **The ledger was only just fixed, so the first scores measured a broken pipeline.** The synthesis template was never rendered before 2026-10-05, so no earlier session has a real ledger. All 17 sessions are a pre-fix baseline. Any "improvement" after the fix is the fix, not the feedback loop. Feedback built on that history teaches agents to compensate for a bug that no longer exists.

4. **Agents cannot act on feedback they do not see.** Agents see only 3-sentence Position Summaries between rounds, and every turn is a stateless `claude -p` call. agent-behavior-philosophy.md records agents saying "none of these change my behavior, they change my framing," and that feeding an agent its own scores produces confabulation. Injecting scores into prompts spends scarce budget in a context the enforcer already trims, to get performed compliance. The doc's own Morning Brief test is not applied: does the brief contain a new idea, or just a rubric-shaped one?

5. **The loop rewards the rubric, not the reader.** The only artifact the user reads is the Morning Brief, and the Evaluator never scores it. Optimizing the 7 design-doc dimensions pushes agents toward rubric-pleasing prose, which kills the genuine friction principle 1 demands. The failure mode that kills this: scores rise, the brief gets no more useful, and nobody notices because no human rating exists.

6. **Mutating static YAML automatically breaks the only reproducibility the project has.** Personas are hand-edited. Automatic or semi-automatic edits make sessions incomparable over time, and agent-identity-and-resolution plans session snapshots that are not built.

**Undecided, author only:**
- Is the loop automatic, or does Brian read scores and edit by hand? That is the whole question.
- What does Brian consider a better session, in a form independent of the LLM judge?
- Is the judge calibrated, meaning has anyone run it twice on the same doc?
- What is the feedback unit: persona, template, or mode?
- Does the roadmap earn this item before blind proposals and phases?
