1. **The feedback loop was built on a signal that was never validated, so it steered personas on noise.** v1-spec-gaps Q7 says the evaluator lets the LLM invent its own dimensions and scores "are not comparable across runs"; the engine facts only say it scores 7+10 dimensions 1-10 via an LLM judge. Nothing shows the judge is stable. In practice this means a persona edit triggered by a 6 vs a 7 is a coin flip. At 3 AM nobody can tell whether a score moved because of the change or because the judge rolled differently. Before we build the loop, let us prove run-to-run variance on the same transcript.

2. **Attribution is impossible, so the loop corrects the wrong thing.** A design doc score is produced by synthesis, which sees only 3-sentence Position Summaries between rounds, a ~10k-token budget enforcer that silently trims sections, and a ledger that was never real before 2026-10-05. A low score could come from the persona, the trimming, the template, the question, or the brief. Feeding it back to "agent behavior" assumes the persona is the cause. The failure mode is tuning personas against defects that live in context assembly.

3. **There is no baseline and no sample size to detect improvement.** One developer, occasional sessions, 17 on disk, and none before 2026-10-05 had a real ledger, so most existing scores come from a different pipeline. Any before/after comparison compares incomparable runs. Three months in, nobody can say whether feedback helped.

4. **Automated feedback collides with the agent-behavior philosophy.** agent-behavior-philosophy.md says forced behavior produces theatre, that agents "cannot reliably introspect" on scores, and that feeding an agent its own scores yields confabulation. Injecting evaluator scores or critiques into prompts is that exact pattern. It also spends context budget the enforcer is already fighting over, and what gets trimmed first is unspecified.

5. **Optimizing the rubric Goodharts the Morning Brief test.** The doc's own test is whether the output holds ideas the user had not considered. Rubric dimensions reward structure and completeness. Personas tuned toward the rubric converge on rubric-shaped, agreeable documents, which is the consensus drift the project fights.

6. **The roadmap ordering starves this item.** The critical path (blind proposals, phases, takeaways, stale detection) never mentions evaluation, and the "Anti-Sycophancy Detection" item is measurement-only. A solo dev will build those first, leaving the evaluator unread, which is today's state.

**Still undecided, only the author can answer:**
- Is feedback automatic (scores edit or inject into prompts) or human-in-the-loop (report read, YAML edited by hand)? The facts suggest the second already exists and is unused. Why?
- What score movement would make you call this a success, and what would make you abandon it?
- Which of the 17 sessions count as valid baselines given the ledger fix?
- Is the unit of change the persona, the template, or the context assembly?
