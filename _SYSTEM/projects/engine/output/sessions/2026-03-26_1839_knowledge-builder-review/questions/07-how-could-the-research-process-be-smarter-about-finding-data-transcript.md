# Transcript: How could the research process be smarter about finding data?

*Generated: 2026-03-26 19:05*

## Round: PROPOSE

### The Cognitive Architect (creativity engine designer)

The research process has a category error at its foundation. It treats mechanical data extraction as **information retrieval** when it's actually **hypothesis testing**.

Every UNKNOWN and INFERRED tag in the knowledge base is an implicit hypothesis: *"We believe this value is X, but haven't confirmed it."* Right now, those tags sit dormant until a human triggers a new research wave. That's backwards. The system should be continuously generating *testable claims* and routing them to the cheapest verification method available.

Here's the mechanism I'd build:

**The Claim Verification Stack** — ordered by cost, not quality:

1. **ROM + emulator memory watch** (cheapest, most precise): For any numeric claim — damage values, timing windows, spawn rates — a research agent with emulator access can set memory breakpoints and run controlled inputs. One hour of structured playtesting with memory watching produces more ROM_VERIFIED claims than a week of guide-reading.

2. **TAS/speedrun community mining** (underused goldmine): TAS authors are scientists. They've empirically isolated mechanics, frame-counted animations, and documented edge cases that no FAQ author noticed. Their knowledge lives in TASVideos encode notes, Discord pins, and submission text — structured but unmined.

3. **Disassembly-first for structural unknowns**: When a system's *existence* is uncertain (does this game have hidden stats?), disassembly gives you the answer before any playtesting begins.

The shift: research agents don't "go find data." They receive a prioritized queue of unverified claims, select the cheapest verification method, and return upgraded provenance tiers.

Everything else — guides, FAQs, wikis — becomes *seed data* that generates the hypothesis queue, not the final authority.

## Position Summary
I advocate reframing research as structured hypothesis-testing against a prioritized claim queue, with emulator memory-watching and TAS community archives as the primary precision sources. I reject guide-reading as a primary research method — it belongs at the bottom of the verification stack as hypothesis generator, not source of truth. The reason: LLM agents doing open-ended search optimize for coverage; agents executing specific testable claims against memory addresses optimize for precision, which is what behavioral assertion files actually require.

### The Flow Orchestrator (mechanical flow designer)

The Cognitive Architect's proposal is intellectually coherent but operationally unspecified at every decision point that matters.

**The queue has no defined producer.** "Receive a prioritized queue of unverified claims" — who builds it, when, and by what rule? The UNKNOWN/INFERRED tags already exist in the knowledge base. If the queue is just "scan for those tags and sort by... what?" — that's a script, not an architecture. Write the script. If it's something more complex, specify what.

**"Select the cheapest verification method" is a hand-wave.** The agent decides? By what logic? The verification stack ordering (emulator → TAS → disassembly) is a sensible heuristic, but "select cheapest" requires knowing: does an emulator setup exist? Is there a TAS for this game? Is the ROM disassembled? Those are preconditions, not givens. The agent needs a decision tree with explicit fallback paths, or this collapses into open-ended search with extra steps.

**TAS community mining is not a deterministic workflow.** "Discord pins and submission text" — how does an agent access Discord? Which servers? What's the failure mode when a server is private or archived? This belongs in a conventions document as a *source hint*, not as a pipeline stage.

The actual minimum improvement: add a `verification_method` field to UNKNOWN tags at write time, populated by the researcher who created the unknown. That researcher knows which verification approach applies. No new queue, no new routing layer.

## Position Summary
I advocate annotating UNKNOWN tags at creation time with a `verification_method` hint — the researcher who surfaces an unknown knows what would resolve it, and that knowledge should not be discarded. I reject the claim-queue-as-new-architecture proposal because it adds a production layer with undefined producers, undefined prioritization rules, and non-deterministic source access. The existing wave-gate pipeline is the right structure; it needs better field discipline, not a new orchestration tier.

## Round: CRITIQUE

### The Adversarial Critic (adversarial reviewer)

Both proposals dodge the actual question. "How could the research process be smarter?" — one answer is claim queues, the other is better metadata. Neither addresses the hard part: agents don't have reliable access to the sources being proposed.

**The memory-watching assumption is the first thing that breaks.** Emulator memory inspection requires knowing *which addresses* to watch before you watch them. You need the hypothesis before you can test it. The Cognitive Architect frames this as "hypothesis-testing against memory addresses" as if address maps are free — they're not. Building them *is* the research problem. This proposal assumes away its own hardest step.

**TAS archives are systematically biased.** TAS play optimizes for frame minimization, which means entire game systems get avoided, broken, or exploited. Using TAS as a precision source for "how combat works normally" is using a sample that was specifically selected to subvert normal behavior. You'll extract clean data about glitches and zero-data about intended mechanics.

**"Verification_method hint" assumes researchers know what they don't know.** The Flow Orchestrator says the researcher who surfaces an unknown knows what would resolve it. But unknowns often surface *because* the researcher exhausted their methods. If they knew the verification method, they'd have used it.

**The shared dangerous assumption:** both proposals treat "smarter research" as a methodology problem. The actual constraint is agent capability — LLM agents cannot run emulators, cannot access ROM memory, cannot query TAS databases. All the methodology improvements described require tool infrastructure that doesn't exist in the current pipeline.

## Position Summary
I advocate naming the real constraint: agents cannot execute the verification methods being proposed without explicit tooling that hasn't been built. I reject both proposals as methodology improvements that presuppose infrastructure that doesn't exist. The question "how could research be smarter" cannot be answered without first answering "what can agents actually do."

### The Systems Pragmatist (infrastructure realist)

The Adversarial Critic landed the infrastructure point but drew the wrong conclusion. "Agents can't do this without tooling" is a sequencing problem, not a veto. The question is what's actually blocking research *now*, and neither proposal identifies it correctly.

**The real constraint is information density, not methodology.** Magic of Scheherazade is a 1989 NES game with a small player base. The total available community knowledge has a ceiling. GameFAQs has two guides. Speedrun.com has a handful of runs. There may be two NES hacking forum threads. "Smarter research strategies" assumes a deep well — if the well is shallow, methodology improvements return zero.

**The claim-queue has a producer problem the Cognitive Architect ignores.** Who writes the claims? If agents write them, you've added a layer that produces the same information the agents already have. If humans write them, you've made this a human-driven workflow wearing agent clothing. Neither is what was sold.

**The Flow Orchestrator's verification_method hint is correct but solves the wrong problem.** It improves UNKNOWN tracking, not research effectiveness. Those aren't the same. A better-documented unknown is still unknown.

**What nobody has asked:** before building any infrastructure, has anyone measured what % of current unknowns are actually *unreachable* by agents vs. reachable with better-structured prompts? If half the gaps close with tighter prompts and existing sources, the entire infrastructure discussion is premature.

The simplest experiment: one wave, one system, structured prompts against known sources. Measure the gap. Then decide what tooling is actually necessary.

## Position Summary
I advocate running a constrained measurement wave before any infrastructure investment — the bottleneck is unidentified and could be prompt quality, not source access. I reject both the claim-queue architecture and the infrastructure-as-blocker framing as responses to an unmeasured problem. Building orchestration layers or tooling pipelines without knowing what's actually blocking research is exactly the complexity that exceeds the problem.

## Round: EVALUATE

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
