1. **The research results were injected faithfully, and the Morning Brief still read the same, so the user never noticed and the feature was abandoned.** The retention question is whether the user would notice if this were removed. Research-engine.md justifies the feature as "debating from evidence", but its only signal is a "needs: more-research" flag from agents. The scope-controls spec's own ROI signal, "did the agent use the result in the next round?", is the only measure of value, and nothing in the plan ties that to what the user reads. Between rounds, agents see only 3-sentence Position Summaries. A 2k-token finding injected into one turn is likely to disappear by the next round, so the evidence never reaches the design doc.

2. **The injection point was chosen against a budget that no longer exists, and findings got trimmed or displaced.** The context-assembly template sets a 4,000-token ceiling with protected sections. The engine fact is ~10k with an enforcer that trims "unprotected sections". Research is in neither list. If it is unprotected, it is cut exactly when the payload is large, which is when research matters. If it is protected, it displaces discussion history. The ROADMAP open question, "how do results integrate", is still open, and the two documents give different ceilings.

3. **The cost envelope was calibrated to a system that does not exist.** The scope-controls figures (2 calls per agent, 204k tokens, 3-4% of a 6.4M budget) assume per-turn spend tracking and turn-level triggers. The real engine shells out to `claude -p` per turn, has no live synthesis, and runs fixed rounds. Nobody can say what a "research call" is in this engine: a fourth subprocess, a tool inside a turn, or a pre-session step. The 3-4% claim is unverified.

4. **Research findings were treated as ledger-grade facts, and wrong findings were locked into DECIDED lines.** The decisions ledger chains forward, and it has never produced a real ledger before 2026-10-05. A mistaken research claim cited in a DECIDED line then propagates to every later question. Nothing in the plan says how a finding is marked as sourced, disputed or expired.

5. **Research agents "without opinions" produced undigested summaries that personas ignored or over-deferred to.** In sequential rounds a research result inserted before a speaker acts as an authority anchor and suppresses the blind-proposal diversity that the ROADMAP ranks as the highest-value item. Blind proposals also conflict with injecting research into the propose round, and the plan does not say which wins.

6. **Building this before the earlier critical-path items meant the user never got a trustworthy base.** Blind proposals, phases and takeaways come first on the ROADMAP. The Evaluator scores are never read back. A solo developer running 17 sessions has no way to tell whether research improved anything.

**Undecided, author only:**
- Is research a pre-session brief step, a between-round step, or an agent-triggered mid-turn call? This decides everything above.
- Does research enter the propose round, or only critique and evaluate?
- Which ceiling applies, 4k or 10k, and is the research block protected?
- What counts as success: a different design-doc paragraph, or a different Morning Brief?
- Is the fix worth the cost in a project where sessions are run occasionally?
