1. **The critical path builds six features with no way to tell whether any of them worked.** The Evaluator scores design docs and transcripts, but "nothing reads those scores back," and the roadmap itself lists "how does evaluation feed back" as an open question. Blind proposals, takeaways, stale detection and sycophancy detection all claim to improve discussion quality. With 17 sessions on disk and no baseline, three months on nobody can show that quality moved. The unstated assumption is that the Evaluator is trustworthy. Nobody has validated it against a human read of those 17 sessions.

2. **Anti-sycophancy detection measures a quantity the engine cannot produce.** It compares blind positions to revealed positions. Between rounds, agents see only 3-sentence Position Summary blocks. The summary compression itself changes what agents see, so any drift measured is confounded with the lossy summaries. The step also depends on blind proposals being clean, which the roadmap admits works "without phases" but is "cleaner" with them. No one has defined what drift counts as sycophancy.

3. **The 1-2 day estimate for blind proposals is hand-waving.** Context assembly includes the decisions ledger, previous design doc headings, open questions and brief context. "Suppress prior context" does not say which of those is suppressed. The ledger only became real on 2026-10-05, so the feature that chains context is untested while the plan is already removing context from it. The budget enforcer trims unprotected sections, so blind mode could silently reintroduce trimmed context or drop protected ones.

4. **Manifest versioning is justified by a schema that does not exist.** "Schema evolution" assumes a manifest with consumers. Whether a manifest exists, and what it versions, is not stated. It is a half-day item that quietly becomes the place where phase and takeaway schemas are decided too early.

5. **The phase system is estimated at 2-3 days while its core question is unanswered.** The roadmap's own open question asks how transitions are triggered (time, convergence or round count), and it asks what the boundary with moderator input is. Takeaways and stale detection both depend on "phase boundaries." Fixed rounds from a mode already behave like phases. Nobody explains what phases add over the existing propose, critique, evaluate modes.

6. **The path ignores the one defect the facts expose.** Synthesis was never rendered before today, so every earlier session lacks a real ledger. The first thing to break is the ledger chain, yet the plan stacks features on it instead of validating it.

7. **Solo developer, occasional sessions.** Stale detection and takeaways need many runs to tune thresholds, and there is no run volume to tune them.

**Only the author can answer:**
- What outcome would make you call V2 a success?
- Is the Evaluator trusted?
- Why is BIT "parallel" for one developer?
- Does a manifest exist today?
