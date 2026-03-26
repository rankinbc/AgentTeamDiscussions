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


<!-- complete -->
