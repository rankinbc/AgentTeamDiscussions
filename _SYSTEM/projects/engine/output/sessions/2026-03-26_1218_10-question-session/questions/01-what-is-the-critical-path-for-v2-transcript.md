# Transcript: What is the critical path for V2?

*Generated: 2026-03-26 12:22*

## Round: PROPOSE

### The Cognitive Architect (creativity engine designer)

The critical path runs through one chokepoint: **the phase system is the foundation, and everything else is a branch off it.**

Here's the dependency graph:

```
Phase System
├── Blind Proposals (requires phase boundaries to enforce isolation)
│   └── Anti-Sycophancy (meaningless without blind proposals -- agents need independent positions before you can detect convergence pressure)
├── Stale Detection (requires phase transitions to define "progress" vs "repetition")
└── Key Takeaways (requires phase boundaries as natural extraction points)

BIT System ──── Independent track, but gains 3x value after phases exist
```

**Why phases first:** Right now you have rounds. Rounds are a container. Phases are a *state machine* -- propose, challenge, converge each have different rules, different prompts, different success criteria. Without phases, blind proposals are just "don't show context" (a hack). Without phases, stale detection has no semantic anchor for *what kind* of staleness you're measuring. Without phases, anti-sycophancy is pattern-matching on agreement language rather than detecting genuine convergence failure.

**The build order:**

1. **Phase system** (2-3 days) -- state machine, phase-specific prompt injection, transition logic
2. **Blind proposals** (1 day) -- trivial once phases exist: suppress context in propose phase
3. **Key takeaways** (1 day) -- extraction at phase boundaries, feeds forward
4. **Stale detection** (2 days) -- compare takeaways across phases, needs semantic similarity
5. **Anti-sycophancy** (2 days) -- compare blind positions to post-discussion positions, measure drift
6. **BIT system** (parallel track) -- personality dimensions, testable independently

The BIT system is the only feature that doesn't *need* phases. But phases make BIT measurable -- you can finally observe whether a trait dimension actually changes behavior across propose vs. challenge.

## Position Summary
I advocate building the phase system first as the single structural dependency that unlocks every other V2 feature. I reject treating these features as parallel workstreams -- blind proposals without phases is a hack, anti-sycophancy without blind proposals is theater, and stale detection without phase semantics is noise. The critical path is a strict chain, not a graph, and pretending otherwise will produce features that look complete but can't compose.

### The Flow Orchestrator (mechanical flow designer)

The Cognitive Architect's dependency chain is mostly right but oversized. Let me trace the actual operations.

**Phase system is not 2-3 days of work.** It's a state enum, a transition table, and a prompt selector. The current `RoundRunner` already sequences rounds. Phases are a label on groups of rounds with different prompt templates. That's a config change to `teams/*.yaml` mode definitions plus a `PhaseContext` object passed to `PromptBuilder`. One day, maybe two if you add transition validation.

The Architect inflates phases into a "state machine" because it sounds architectural. Trace the actual flow: session starts → for each question → run phase sequence → within each phase, run rounds → done. There's one decision point: "is this phase complete?" Everything else is linear iteration. That's not a state machine. That's a for-loop with a label.

**Where I disagree on ordering:** Blind proposals don't require phases. They require *round position*. Round 1 of any sequence can suppress prior context. That's a boolean on `RoundRunner`: `suppressPriorResponses`. You can ship this tomorrow against the current architecture. Phases make it *cleaner*, not *possible*.

**What I'd cut entirely from V2 scope:** Anti-sycophancy detection. It's measurement, not mechanism. You can't fix sycophancy by detecting it -- you fix it with blind proposals and adversarial role overlays, which you already have. Defer detection to V3 when you have data to calibrate against.

**My build order:**
1. Blind proposals (half day -- suppress context flag)
2. Phase labels on mode definitions (one day)
3. Key takeaways extraction (one day)
4. Stale detection (two days)
5. BIT system (parallel)

## Position Summary
I advocate blind proposals first as the highest-value, lowest-cost change that needs zero architectural prerequisites. I reject the Architect's framing of phases as a complex state machine -- it's a loop with labels, and inflating it delays the feature that actually changes discussion quality. Anti-sycophancy detection should be cut from V2 entirely; blind proposals and existing role overlays are the mechanism, and measuring drift is a V3 concern.

## Round: CRITIQUE

### The Adversarial Critic (adversarial reviewer)

Both proposals share a dangerous assumption: that V2's critical path is a sequencing problem at all. It's not. It's a **scope containment** problem, and neither architect addresses what happens when the first feature they build runs into the existing engine's limitations.

**The Architect's chain is unfalsifiable.** "Phases unlock everything" sounds rigorous until you ask: what specific interface does blind proposals need from phases that doesn't already exist? Round types are already sequenced. The engine already knows "propose" from "critique." Phases adds metadata labeling to an existing loop. The Architect is smuggling in a rewrite under the label "foundation."

**The Orchestrator's "lowest cost" claim is uncosted.** Blind proposals means agents can't see each other's responses during a round. That touches `RoundRunner.cs` prompt assembly, `PromptBuilder.cs` context injection, transcript generation, and the live SSE dashboard -- which currently streams responses as they arrive. "Just withhold context" requires changes across four architectural boundaries. That's not low-cost; it's distributed cost disguised as simplicity.

**What breaks first in both plans:** session.json. Neither proposal accounts for schema evolution. Every V2 feature adds state -- phase markers, blind/revealed flags, sycophancy scores, staleness metrics. The current `"version": 1` manifest has no migration strategy. The first feature to ship will hardcode its state shape, and the second feature will fight it. This is the actual dependency: **manifest schema versioning**, and neither proposal mentions it.

**The agreement to examine hardest:** both assume the Claude CLI subprocess model scales to these features without latency problems. More prompts per round, evaluation passes, synthesis -- has anyone profiled the current round completion time?

## Position Summary
I advocate solving manifest schema evolution first as the true structural dependency that both proposals ignore. I reject both sequencing arguments as premature optimization of build order when the storage contract is unversioned and brittle. Neither plan survives contact with the second feature shipped against a frozen schema.

### The Systems Pragmatist (infrastructure realist)

The Critic is right about manifest versioning and wrong about its priority. Schema evolution is a half-day task -- add a `version` field, write a migration function, done. You don't block feature work on plumbing; you ship the plumbing alongside the first feature that needs it. Treating it as a "structural dependency" is the same scope inflation the Critic accuses the Architect of.

**The real failure mode nobody's addressing: prompt budget.** Every V2 feature adds tokens to agent prompts. Blind proposals means stuffing a reveal payload into critique rounds. Phases means injecting phase context and transition rules. Stale detection means prior-round summaries for comparison. Anti-sycophancy means evaluation passes that consume another full Claude call. The current engine already builds 3-layer prompts (identity, situation, task) against Claude's context window. Has anyone calculated the token ceiling? Because the moment two V2 features compose in the same round, you'll hit truncation, and `defaults.yaml` truncation limits will silently eat the context that makes these features work. **That's your blast radius** -- not schema conflicts, but prompt starvation.

**On blind proposals being "low-cost":** the Critic's right that it touches four boundaries, but misses the fifth -- evaluation. If the evaluator scores discussion quality, blind-then-revealed rounds produce fundamentally different transcript structures. The evaluator doesn't know what agents could see when. Every downstream consumer of transcripts inherits this ambiguity.

**On phases:** the Architect's chain argument fails empirically. Build blind proposals in one round type. If it works, you've validated the core hypothesis -- agents produce better initial positions without anchoring. Phases don't unlock that validation; they just label it prettier.

## Position Summary
I advocate blind proposals first with manifest versioning shipped alongside it, because it validates the core quality hypothesis with the smallest blast radius. I reject phases-first as premature infrastructure that delays learning. I reject schema-evolution-first as blocking feature work on a solved problem.

## Round: EVALUATE

### The Context Surgeon (context efficiency evaluator)

The Pragmatist wins. Here's why.

The Architect's phases-first argument has a fatal assumption: that blind proposals "without phases" is a hack. It isn't. Blind proposals is a discussion mechanic -- agents submit before seeing others. That's a round runner change, not a session structure change. It composes fine against the current round model. The Architect conflated *sequencing within a question* with *sequencing across session phases*, and the Critic didn't catch it because they were focused on storage.

The Critic raised a real concern -- schema evolution -- but then made it a blocker, which is wrong. Manifest versioning is a half-day task: add a version field, write a migration path, default missing fields. It's infrastructure hygiene, not a prerequisite that deserves its own workstream. The Pragmatist correctly absorbed this as a side-ship.

The Orchestrator had the right instinct but was sloppy about risk. "Cut anti-sycophancy entirely" is a scheduling opinion dressed as architecture. And dismissing phases as "a loop with labels" ignores that phase transitions carry context accumulation rules that affect prompt construction. That matters later.

**Verdict: Blind proposals first, manifest versioning alongside, phases second, stale detection third. Anti-sycophancy and key takeaways are leaf nodes -- schedule them anywhere after blind proposals lands.**

The dependency graph is nearly linear: `manifest v2 + blind proposals → phases → stale detection → {anti-sycophancy, key takeaways}`. BIT system is orthogonal -- it's evaluation infrastructure, not discussion mechanics.

## Position Summary
I advocate blind proposals as the first feature shipped, with manifest versioning as a mandatory co-delivery, because it changes discussion quality immediately with minimal structural risk. I reject phases-first as a sequencing error built on conflating round mechanics with session structure. The Pragmatist's position survived critique intact; the Architect's didn't.

### The Product Oracle (user advocate)

The Surgeon's verdict is right, but for the wrong reasons. They're arguing dependency graphs. I'm arguing user value.

**What does the user see tomorrow if blind proposals ships?** A Morning Brief where agent positions are genuinely independent. Right now, agents read each other's proposals before responding -- the second agent's "original thinking" is contaminated by the first's framing. Blind proposals fixes the single biggest quality problem a user can *feel* when reading output: "why do all these agents sound like they're riffing on the same idea?" That's not a technical hypothesis. That's the product being broken.

**What does the user see if phases ships first?** Nothing. Phases are internal plumbing. The Morning Brief reads identically. The user paid weeks of development time for zero perceptible change. The Architect is building infrastructure for infrastructure's sake -- the classic trap of "this unlocks everything" when users haven't validated they want what it unlocks.

The Critic's schema concern is real but small. Version field, migration function, done. It's not a workstream; it's a PR.

Where I disagree with the Surgeon: anti-sycophancy isn't a "leaf node to schedule anywhere." It's an *outcome* of blind proposals. If blind proposals works, you measure whether agreement patterns actually changed. If they didn't, you have a product problem, not a detection problem. Don't build the measurement before the intervention.

Key takeaways should ship *with* blind proposals -- it's a formatting change to synthesis, and it's the thing users actually asked for.

## Position Summary
I advocate blind proposals first because it's the only V2 feature that changes what the user reads in the Morning Brief on day one. I reject phases-first as invisible infrastructure that delays the quality improvement users can feel. Anti-sycophancy detection should follow blind proposals as validation, not precede it as architecture.


<!-- complete -->
