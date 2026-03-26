# Transcript: Phase separation: brainstorm vs refine vs specify vs review.

*Generated: 2026-03-26 12:02*

## Round: PROPOSE

### The Cognitive Architect (creativity engine designer)

# Phase Separation Through Constraint Gradients

Hard phase gates are theater. Soft detection is vaporware. Both miss what actually drives different LLM output: **constraint density**.

Here's the mechanism that matters. An LLM given "brainstorm approaches to authentication" and an LLM given "evaluate whether JWT rotation solves the session fixation problem identified in Round 2" produce fundamentally different text — not because you labeled one "divergent" and one "convergent," but because the second prompt has higher constraint density. More of the token generation is determined by prior context.

**My design: Constraint Gradient Rounds.**

Each mode definition already specifies rounds. Instead of labeling phases, each round specifies a **constraint profile**:

- **Open rounds**: Minimal context injection. Agent sees the question and its own identity. No prior responses. Success = novelty count (distinct approaches surfaced).
- **Anchored rounds**: Agent sees all prior responses plus its identity. Prompt demands engagement with specific prior proposals. Success = reference density (how much builds on vs. ignores others).
- **Bound rounds**: Agent sees synthesized positions plus explicit criteria. Prompt requires judgment against those criteria. Success = decision coverage (did it address every open point).

What changes between profiles isn't which agents participate — it's **how much prior context enters the prompt and what the prompt demands they do with it.** Same agents, different cognitive environments.

This is testable today. You measure output similarity across agents per round. Open rounds should show high variance. Bound rounds should show convergence. If they don't, your constraint profiles aren't working.

No phase detection needed. No new abstractions. Just prompt engineering formalized into the mode YAML.

## Position Summary
I advocate constraint gradient rounds where each round specifies how much context enters the prompt and what agents must do with it, producing genuinely different cognitive behavior through prompt structure alone. I reject both hard phase gates and soft phase detection as unnecessary abstractions that add complexity without adding testable behavioral change. The reason: LLMs don't have "modes" — they have prompts, and the measurable lever is constraint density, not phase labels.

### The Flow Orchestrator (mechanical flow designer)

# The Cognitive Architect Is 90% Right — But Sloppy on Sequencing

The constraint gradient idea is sound. I'll go further: it's what the system already does, just not named. Look at `RoundRunner.cs` — each round type (propose, critique, evaluate) already injects different context and demands different output. "Constraint Gradient Rounds" is a description of the current architecture with a marketing name.

Where the proposal gets sloppy: **it doesn't specify the ordering contract.** "Open, Anchored, Bound" implies a sequence, but the design says "each round specifies a constraint profile" — which means someone has to decide which profile each round gets. That's either the mode YAML author (static, already works) or some runtime logic (dynamic, scope creep).

I say: **static, mode-defined, full stop.** The mode YAML already defines round order and which agents participate. Add a `context` field per round: `none`, `prior_responses`, `synthesized`. Three values. That's the entire implementation. No gradient abstraction, no similarity measurement, no novelty counting.

The measurement proposal — similarity scoring, reference density, novelty count — is evaluation, not orchestration. It belongs in the post-hoc instrumentation we already decided on (Q5). Don't mix it into round execution.

What the Cognitive Architect calls "constraint profiles" I call **context injection rules**: a per-round config that controls what goes into the prompt. One enum field on the round definition. Ship it in the mode YAML. Measure later whether it changes output quality.

Everything else proposed here — detection, scoring during rounds, success criteria per profile — is scope that contradicts our Q5 decisions. Defer it.

## Position Summary
I advocate adding a single `context` enum field (`none`, `prior_responses`, `synthesized`) to round definitions in mode YAML, controlling what prior material enters each agent's prompt. I reject runtime phase detection, in-round similarity scoring, and any abstraction beyond static mode configuration. The reason: the orchestrator's job is deterministic sequencing with explicit data flow — measurement is a separate concern we already scoped to post-hoc instrumentation.

## Round: CRITIQUE

### The Adversarial Critic (adversarial reviewer)

Both proposals converge on the same core claim: static prompt configuration is sufficient to produce meaningfully different cognitive behavior across rounds. This is the most dangerous assumption on the table and neither author stress-tested it.

**Problem 1: "Constraint density" is not a behavioral lever you've measured.** The Cognitive Architect asserts that varying context in prompts produces "genuinely different cognitive behavior." Where's the evidence? LLMs are completion engines. Giving an agent less context doesn't make it brainstorm — it makes it hallucinate fill-in assumptions. You'll get *different* outputs, not *divergent-then-convergent* outputs. Those are not the same thing.

**Problem 2: The `context` enum is a three-state illusion.** `none`, `prior_responses`, `synthesized` — what happens when `synthesized` material is poor? The agent receives garbage context with no mechanism to distinguish it from good context. You've created a silent quality dependency between rounds with zero feedback path.

**Problem 3: Both proposals dodge the actual question.** The question asks what changes between phases — agent selection, anti-slop rules, communication mode, success criteria. Both answers say "just change the prompt context." That's one lever. The question named four. Neither explains why three of them don't matter.

**Problem 4: You can't validate this without defining what "brainstorm behavior" looks like in output.** If you ship context-controlled rounds and declare victory, how do you know round 1 actually diverged? You have no success criteria for phase-appropriate behavior, which means your post-hoc instrumentation has nothing to measure against.

**Problem 5: Static mode config assumes the right round count is knowable in advance per question type.** It isn't.

## Position Summary
I advocate defining measurable output criteria for each phase type before selecting any mechanism to produce phase separation. I reject both proposals' shared assumption that controlling prompt context alone produces meaningfully distinct cognitive phases. Without success criteria for what "brainstorming" or "refinement" looks like in LLM output, you're building configuration knobs attached to nothing.

### The Systems Pragmatist (infrastructure realist)

The Critic identified the right problems but pulled the wrong conclusion. "Define measurable output criteria before selecting any mechanism" sounds rigorous — it's actually a block. You will spend weeks defining what "brainstorm behavior" looks like in LLM output and arrive at nothing actionable, because there's no ground truth for divergent thinking in text completions. That's a research project, not a shipping decision.

Here's what actually breaks first: **the assumption that phase separation is a problem worth solving at this scale.** We have fixed round counts per mode (already decided), deterministic rotation (decided), and post-hoc instrumentation (decided). The question presupposes we need an additional phase mechanism. What evidence says current output suffers from insufficient phase separation? None has been presented.

The Flow Orchestrator's `context` enum is the only proposal that doesn't add moving parts. But even that's premature. Adding `none` context to round 1 doesn't produce brainstorming — it produces uninformed responses. The Critic is right that less context means more hallucination, not more creativity. The Cognitive Architect's "constraint gradient" is the same thing with fancier language.

**The real failure mode nobody's addressing:** if you ship any phase mechanism without first running sessions and measuring whether current output already exhibits natural phase-like variation, you're solving a problem that may not exist. The decided instrumentation work hasn't happened yet. We're designing controls for a system we haven't observed.

The round count is already fixed per mode. Context already varies by round definition. What specific output failure are we engineering against?

## Position Summary
I advocate deferring all phase separation work until post-hoc instrumentation (already decided, not yet shipped) produces data showing current output lacks sufficient behavioral variation across rounds. I reject both prompt-context mechanisms and output-criteria-first approaches as premature engineering against an undemonstrated problem. Without evidence that current fixed-round modes produce insufficiently diverse output, any phase mechanism is complexity with no validated purpose.

## Round: EVALUATE

### The Product Oracle (user advocate)

**The Systems Pragmatist wins. The critique didn't just damage the proposals — it made them irrelevant.**

Here's the product test neither proposal passed: if phase separation works perfectly, what changes in the Morning Brief? Neither the Cognitive Architect nor the Flow Orchestrator answered this. They described mechanisms. They didn't describe outcomes a user would notice.

The Adversarial Critic landed a real hit asking for measurable output criteria first. But even that's premature — you need to know the *current* output is deficient before defining what "better" looks like. The Pragmatist correctly identifies that we haven't shipped the instrumentation we already decided on. We're stacking design decisions on top of unvalidated assumptions.

**From the user's chair:** Brian drops a brief into `input/`, waits for agents to discuss, reads the Morning Brief. Does he think "these agents all sounded the same in every round"? We don't know. We haven't measured it. We haven't even asked. The entire premise of this question — that phases need separating — is an internal hypothesis with zero user signal behind it.

The Cognitive Architect's constraint gradient idea is genuinely interesting and worth preserving as a design note. If instrumentation later reveals that rounds 1 and 3 produce near-identical output despite different round labels, that's a mechanism worth testing. But building it now is classic premature sophistication — impressive engineering that makes the system harder to configure without evidence it improves what the user reads.

**Ship instrumentation. Read the data. Then decide if this question even needs answering.**

## Position Summary
I advocate deferring all phase separation work until shipped instrumentation demonstrates that current fixed-round modes produce insufficiently varied output — making this a data-gated decision, not a design decision. I reject both the context-enum and constraint-gradient proposals as premature mechanisms that add configuration surface area without evidence they improve user-facing output. The reason: no user has complained that rounds feel samey, no data shows they are, and the decisions we already made (instrument first, fixed rounds per mode) haven't been executed yet — building phase gates on top of unvalidated assumptions is the definition of over-engineering.

### The Context Surgeon (context efficiency evaluator)

**The Pragmatist is right, but the Oracle just made the stronger case for why.**

The Oracle's product test is the kill shot: "if phase separation works perfectly, what changes in the Morning Brief?" Neither proposal answered this. That's not a gap in their proposals — it's evidence the question itself is premature.

I want to address the Critic's position directly because it sounds rigorous but actually creates busywork. Defining "measurable output criteria for each phase type" before we have data showing phases are needed is building a test harness for a feature nobody requested. You don't write acceptance criteria for a solution to an undemonstrated problem. The Critic is applying good methodology at the wrong stage of the pipeline.

The Cognitive Architect's constraint gradient idea has genuine intellectual merit — varying context density across rounds *would* produce different prompt behavior. But "would produce different behavior" isn't "would produce better output." The Flow Orchestrator's context enum is cleaner engineering but suffers the same gap: it's a well-designed knob connected to no validated need.

Here's what I'd preserve: the Cognitive Architect's constraint gradient concept belongs in a design notes file. If instrumentation later shows rounds 1 and 3 produce statistically similar output, that's the mechanism to test first. But that's a bookmark, not a work item.

**The sequencing is non-negotiable:** ship instrumentation (already decided), run sessions, measure round-over-round output diversity, *then* decide if this question deserves engineering time.

## Position Summary
I advocate deferring all phase separation work until shipped instrumentation produces data demonstrating insufficient behavioral variation across current fixed rounds — making this question data-gated, not design-gated. I reject both the context-enum and constraint-gradient proposals as premature mechanisms solving an unvalidated problem, and I reject the Critic's "define criteria first" position as premature rigor applied before the problem is confirmed. The reason: every decision made so far (instrument first, fixed rounds per mode, post-hoc quality measurement) points to the same conclusion — we don't build phase gates until data says we need them, and we haven't collected that data yet.


<!-- complete -->
