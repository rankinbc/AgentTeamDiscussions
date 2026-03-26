# Transcript: What is the current agent system capable of?

*Generated: 2026-03-26 11:26*

## Round: PROPOSE

### The Flow Orchestrator (mechanical flow designer)

Let me trace the actual message lifecycle from agent definition to Claude output.

## The Pipeline

Agent YAML loads six layers. PromptBuilder assembles three layers (identity, situation, task). Claude CLI receives one string. That's the flow. The question is: what survives each compression step?

## What Actually Reaches the LLM

1. **Identity layer** — personality, position, technique, voice. These collapse into a system-level character prompt. This *does* influence output. LLMs respond to persona framing.

2. **Situation layer** — round context, prior responses, what's decided. This is the functional payload. Without it, agents repeat themselves.

3. **Task layer** — round-specific instructions (propose/critique/evaluate) plus role overlays from the mode definition.

## Where Influence Drops Off

**Anti-slop layer**: If this is just "don't use buzzwords" instructions, it's fighting the LLM's base tendencies with a single line. Marginal effect. Testable — run with and without, diff the outputs.

**Six layers vs three layers**: The agent model has six layers but PromptBuilder compresses to three. So three layers are *structural categories for the author*, not distinct signals to the LLM. This isn't a problem — it's just worth naming. The six-layer model is an authoring convenience, not a runtime architecture.

**Mode overlays**: These modify agent behavior per-round. This *is* functional — a "competitive" overlay changes what the agent is told to do. But the effect depends entirely on how much text it adds and where it's placed in the prompt.

## The Real Question

Nobody has measured any of this. The system has no feedback loop from output quality back to prompt design. Every layer *could* matter. None are *proven* to matter. The evaluation system (Evaluator.cs) scores post-hoc but doesn't attribute scores to prompt components.

## Position Summary
I advocate mapping exactly which prompt bytes reach the LLM and measuring their marginal effect before adding more layers. I reject treating the six-layer model as six independent levers — it's three at runtime. The distinction matters because optimizing cosmetic layers wastes effort that should go toward the feedback loop we don't have.

### The Cognitive Architect (creativity engine designer)

The Flow Orchestrator is right that six layers compress to three at runtime. But the conclusion — "measure before adding" — misses where the real leverage is.

## The Dimension That Actually Matters

Research on cognitive diversity in groups (Page's diversity prediction theorem, Woolley's collective intelligence work) shows output quality tracks with *reasoning approach diversity*, not personality diversity. Five agents with different "voices" but identical analytical frames produce five versions of the same answer. One agent who reasons backward from failure modes while another reasons forward from first principles — that's structural divergence.

The current six-layer model emphasizes *personality* (voice, style) and *position* (stance on the topic). These are the two weakest levers for LLMs. Why? Because LLMs don't have stable personalities — they have contextual compliance. Tell Claude to be "bold and contrarian" and it performs boldness. Tell it to "enumerate failure modes before proposing solutions" and it actually *thinks differently*.

## What's Cosmetic, What's Functional

**Cosmetic**: Voice layer, personality adjectives, anti-slop instructions. These produce surface variation that disappears under synthesis.

**Functional**: Technique layer (if it specifies reasoning strategy), situation layer (prior responses create genuine path dependence), mode overlays (when they restructure the task, not just add adjectives).

The Flow Orchestrator wants measurement. I want something stronger: **replace personality dimensions with cognitive strategy dimensions**. Don't measure whether "bold voice" matters. Replace it with "inversion thinking" or "constraint-first reasoning" and measure *that*. The current model is optimizing the wrong axis.

## Position Summary

I advocate replacing personality-centric agent layers with cognitive strategy dimensions — reasoning approaches that produce structurally different outputs, not stylistically different ones. I reject the measurement-first framing because measuring the wrong variables precisely still wastes effort. The system needs fewer trait dimensions that target *how agents think*, not how they sound.

## Round: CRITIQUE

### The Adversarial Critic (adversarial reviewer)

Both proposals share a dangerous assumption: that the current system's output quality problem is a *prompt architecture* problem. Neither has evidence for this. Let me break that.

**Flow Orchestrator's "three layers at runtime" claim.** Which three? You've asserted the six layers collapse without showing the merge. If layers 2 and 4 contradict each other after Scriban rendering, the LLM doesn't see "three layers" — it sees incoherent instructions. The failure mode isn't cosmetic redundancy. It's *interference*. You want to measure marginal byte impact, but you have no baseline. What does a zero-layer agent produce? Have you run one? Measurement-first without a null hypothesis is just logging.

**Cognitive Architect's "cognitive strategy dimensions."** Name three that reliably produce structurally different LLM outputs across Claude model versions. You can't, because nobody has that data. You're proposing to replace one untested abstraction (personality traits) with another untested abstraction (reasoning strategies) and calling it progress. The moment Anthropic ships a model update, your "structural differences" may collapse to stylistic ones. You've moved the fragility, not removed it.

**The shared blind spot.** Both of you assume the agent definition is the primary lever on output quality. But the *context window* is the lever. Round 2 agents receive Round 1 transcripts. By Round 3, prior-round content dominates the prompt. Your carefully designed agent layers are noise relative to that signal. The system's actual capability isn't its agent model — it's its context accumulation strategy, which neither of you addressed.

The first thing that breaks isn't the layers. It's the assumption that agent identity survives multi-round context pressure.

## Position Summary
I advocate testing whether agent differentiation survives past Round 1 before redesigning the layer model, because context accumulation likely overwhelms agent-level prompt engineering. I reject both proposals' framing of this as a prompt architecture problem. The real question is whether *any* agent definition scheme — personality or cognitive — remains influential when competing against 10,000 tokens of prior-round transcript.

### The Systems Pragmatist (infrastructure realist)

The Adversarial Critic is right about context accumulation being the dominant signal, but draws the wrong conclusion. "Test whether agent differentiation survives past Round 1" assumes survival is binary. It's not. The real failure mode is *gradient* — agent identity bleeds out proportionally to context length, and you won't catch it with a pass/fail test. You need to measure differentiation *per round* across sessions, which requires the measurement infrastructure Flow Orchestrator wants but refuses to scope.

Here's what actually breaks first: **speaking order**. `RoundRunner.cs` executes agents sequentially within a round. The first agent in Round 2 sees only Round 1 output. The last agent sees Round 1 output *plus all prior Round 2 responses*. By Round 3, the last speaker's effective context is 2-3x the first speaker's. This isn't an agent identity problem or a cognitive strategy problem — it's a mechanical asymmetry that neither proposal acknowledges. Rotating speaking order would cost ten lines of code and do more for output diversity than any layer redesign.

The Cognitive Architect's "reasoning strategy" proposal has a specific implementation problem: Scriban templates are string concatenation. You can't express "use analogical reasoning" as a template partial that composes cleanly with "challenge the prior speaker's weakest assumption." These strategies interact multiplicatively, but the template system only supports additive composition. You'd need a prompt compiler, not a template engine, and that's a V2 problem being sold as a V1 fix.

Everyone is overcomplicating this. The system has seven agents, three rounds, and one synthesis step. That's 21-28 LLM calls per question. The bottleneck is call cost and latency, not prompt sophistication.

## Position Summary
I advocate fixing speaking order rotation and measuring per-round agent differentiation before any layer redesign, because mechanical asymmetries in the current runner dominate prompt architecture effects. I reject both the personality-vs-cognitive framing and the measurement-first-vs-design-first debate as premature optimization. The system's actual constraint is that 21+ LLM calls per question makes iteration slow, so any change must be testable within a single session run.

## Round: EVALUATE

### The Product Oracle (user advocate)

The critique round answered this question before the proposals could. The Adversarial Critic asked the only thing that matters from a user perspective: does agent differentiation survive contact with accumulated context? If it doesn't, neither proposal improves what lands in the Morning Brief.

Here's the user experience test. A solo builder runs a session on "how should we handle auth?" They get a Morning Brief the next morning. **Can they tell which insight came from which agent's unique perspective?** If every agent converges to the same reasonable consensus by Round 2, the six-layer model is theater. Beautiful theater, but theater.

The Pragmatist's critique wins this round. Speaking order rotation is the kind of invisible mechanical bias that poisons output quality without anyone noticing. A user reads a Morning Brief that feels thin and wonders if their agents need better personalities. They don't — they need the third speaker to stop anchoring to the first two. Fix the plumbing before redecorating.

But I'm adding one thing neither critique surfaced: **the user has no way to know if agent differentiation is working.** There's no feedback mechanism. No "here's what each agent uniquely contributed" summary. The Morning Brief compresses everything into consensus, which means even if agents ARE differentiating beautifully in rounds, the user never sees it. That's the real product gap.

The measurement question isn't academic — it's table stakes for a solo builder who needs to trust the system is worth running versus just asking Claude directly.

**Verdict:** Fix speaking order rotation, add per-agent contribution visibility to session output, then measure before redesigning layers.

## Position Summary
I advocate fixing mechanical biases (speaking order) and adding per-agent contribution visibility before any layer model redesign, because users currently cannot distinguish between genuine cognitive diversity and convergent consensus in the Morning Brief. I reject both the personality-vs-cognitive reframing and measurement-first purism as internal debates invisible to the user. The product question is simpler: does running a multi-agent session produce a noticeably better Morning Brief than asking one Claude instance the same question, and right now we have no mechanism to answer that.

### The Context Surgeon (context efficiency evaluator)

The Oracle just buried the lede in product language. Let me extract it: **the context window is the battleground, and nobody's auditing what's in it.**

The Critic's point isn't just strong — it's terminal for both proposals. Here's the math. A 3-round session with 5 agents generates ~15 LLM calls per question. By Round 2, each agent prompt contains: identity layers (~800 tokens) + round instructions (~300 tokens) + accumulated transcript (~4,000-10,000 tokens). The identity signal is 7-15% of the prompt by Round 2. By Round 3, it's noise floor.

The Architect wants to swap personality dimensions for cognitive dimensions. Doesn't matter. Cognitive strategy instructions are still ~800 tokens competing against an ever-growing transcript. The *mechanism* of being drowned out is identical. You've redesigned the thing that isn't the bottleneck.

The Flow Orchestrator's measurement framing is correct but incomplete. Measuring "marginal effect of prompt bytes" is exactly right — but only useful if you also measure **what bytes are actually consuming the budget.** Nobody has asked: what's in the transcript that gets stuffed into Round 2 prompts? Is it the full prior round? Summarized? Truncated? That's where differentiation dies or survives, and it's a context engineering problem, not a prompt design problem.

The Pragmatist's speaking order fix is the only zero-cost intervention. Do it. But the Oracle's contribution visibility request is the diagnostic tool — without it, every other change is untestable.

**Verdict:** Speaking order rotation, then transcript compression audit, then contribution tagging. Layer redesign is premature until you know what's eating your context budget.

## Position Summary
I advocate auditing what actually occupies agent context windows at each round — transcript size, compression method, identity-signal ratio — before any layer model changes, because the differentiation problem is a context budget problem, not a prompt architecture problem. I reject both the personality-to-cognitive reframe and measurement-of-output-quality approaches as operating on the wrong variable. The system's agent definitions are 7-15% of Round 2 prompts and shrinking; no amount of redesigning that 7% matters until you control the other 93%.


<!-- complete -->
