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


<!-- complete -->
