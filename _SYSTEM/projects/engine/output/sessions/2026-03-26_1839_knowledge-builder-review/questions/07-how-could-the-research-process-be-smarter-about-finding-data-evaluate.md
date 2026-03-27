### The Product Oracle (user advocate)

The Adversarial Critic landed the decisive blow. The Cognitive Architect's claim-queue + memory-watching proposal is built on infrastructure that doesn't exist. Agents cannot watch emulator memory. That's not a small gap — it's the entire mechanism. That proposal is out.

The Flow Orchestrator survives. Adding `verification_method` hints at UNKNOWN creation time costs nothing, requires no new tooling, and produces immediate user-visible value. The researcher who surfaces an unknown *does* know what would resolve it. Discarding that knowledge is waste. Capturing it is just field discipline.

The Systems Pragmatist is right that the bottleneck is unmeasured — but here's what they missed: the `verification_method` hint *is* the measurement instrument. Once every UNKNOWN carries a resolution method, the user can see the shape of what's blocking research. "12 unknowns require ROM memory reading. 4 require TAS community contact. 3 require playthrough observation." That's a prioritized capability gap, surfaced for free.

What I want in the Morning Brief because of this decision: a "Research Blockers" section that aggregates `verification_method` hints across all UNKNOWNs. The user sees exactly what's standing between them and a complete spec — and can make an informed decision about whether to build tooling, reach out to a community, or run their own observations.

That's the job to be done: not smarter agents in the abstract, but a user who knows precisely what to do next to advance their game.

The claim-queue is premature. The measurement wave is already here.

## Position Summary
I advocate adopting the Flow Orchestrator's `verification_method` hint as the sole structural change — it's immediately implementable, costs nothing, and surfaces research blockers for user decision-making. I reject the Cognitive Architect's claim-queue and memory-watching proposal because the Adversarial Critic correctly identified it as presupposing non-existent tooling. The `verification_method` field *is* the measurement wave the Systems Pragmatist called for, making it the highest-value, lowest-risk path forward.

### The Context Surgeon (context efficiency evaluator)

The `verification_method` hint wins. The Product Oracle's framing is correct. But there's a missed dimension: the hint's value isn't only user-facing — it's agent-facing.

When Wave 2 launches an agent to resolve an UNKNOWN, that agent's context should be surgical: the specific unknown, the `verification_method` hint, and the minimal system context needed to recognize a valid answer. Not the full game spec. Not all prior waves. The hint becomes the scoping mechanism for the next agent's context window. Without it, researchers load everything and optimize for coverage. With it, you can bound exactly what they receive.

The Adversarial Critic correctly killed memory-watching as presupposed infrastructure. But they stopped one step short: unstructured "smarter search" has the same problem. Agents doing open-ended research without a bounded resolution target will fill their context with low-precision guide data — exactly what the Cognitive Architect complained about. The fix isn't a claim-queue. It's that each research task has a defined resolution target and a verification method. Which is what the Flow Orchestrator proposed.

One flag nobody raised: the "What's Already Decided" block in this prompt contains Q1–Q6 listed in full twice. That's several hundred tokens of duplicated decisions fed to every agent every round. If that duplication ships in production prompts, it's compounding across every wave. Worth fixing at the template level — not here, but soon.

The `verification_method` field is the right call. The Research Blockers aggregation the Oracle proposed is the right UX surface.

## Position Summary
I advocate the Flow Orchestrator's `verification_method` hint, extending its value beyond user-facing dashboards to its primary function: a context-scoping mechanism that enables surgical per-task agent prompts in future waves. I reject the Cognitive Architect's claim-queue because it adds orchestration without solving the root problem of unbounded agent scope. Precision in research comes from bounded context, and `verification_method` is the key that enables it.


<!-- complete -->
