# Transcript: Who/what decides what goes into the Situation layer each turn?

*Generated: 2026-03-17 21:49*

## Round: PROPOSE

### The Cognitive Architect (creativity engine designer)

# The Situation Layer Pipeline

Three stages, one LLM call.

**Stage 1: Deterministic Filter (zero LLM cost)**

The orchestrator pulls raw material from four sources:
- Agent's own save file (ideas, stances, magnitudes, personal summary)
- Teammate save files (trimmed to ideas + magnitudes only)
- Discussion state (activeIdeas ranked by magnitude, activeStances, decisions, phase)
- Magnitude delta flags (ideas that moved significantly since last round)

Then it *cuts*. Resolved decisions older than 2 rounds -- gone. Ideas below archival threshold for this agent's persona -- gone. Stances on dead ideas -- gone. This is cheap string manipulation against structured data. Output: ~12-18k tokens of candidate material.

**Stage 2: LLM Curator Call (one call, ~4k output)**

The filtered material goes to a curator prompt. Not an agent -- a utility function. It does three things:
1. Clusters related stances into tension pairs ("You believe X, Team B pushed back with Y")
2. Weights narrative emphasis by magnitude ranking
3. Injects the valuable randomness -- a minor idea might get surfaced because the curator notices an interesting connection nobody made explicit

This is where the hidden agenda-setting happens. The curator *chooses* what to emphasize.

**Stage 3: Assembly**

Identity block (static, ~2k) + Curator output (Situation, ~8-15k) + Task prompt (phase-specific question, ~1-2k) = what the agent sees.

The agent never touches raw transcript, never sees teammate save files directly, never knows what got filtered out. They experience a *curated reality*. That's the point -- it's how you fit a multi-hour discussion into 25k tokens without lobotomizing it.

**The interesting design question you didn't ask:** the curator is the most powerful actor in the system and has zero magnitude, zero persona, zero accountability. Worth watching.

### The Flow Orchestrator (mechanical flow designer)

## Situation Layer Construction -- Sequence Trace

**Trigger:** Round-open, after between-round pipeline completes (BackgroundAgents → intra-team → thinking routines → save file write).

**Step 1: Deterministic Filter (no LLM)**
Inputs: agent's save file, Discussion state.
Operations:
- Drop ideas/stances below archival threshold (persona-dependent)
- Drop decisions older than N rounds unless referenced by active ideas
- Rank remaining ideas by magnitude descending
- Flag magnitude deltas exceeding threshold (from agenda emergence spec)
- Collect active artifacts relevant to current phase

Output: filtered candidate set, ~40-60% smaller than raw state.

**Step 2: LLM Curator Call (one call per agent per round)**
Inputs: filtered candidate set, agent's identity summary (not full identity block), current phase, round number, temperature value.
Task: Compress into narrative Situation block within ~8-15k token budget.
Operations:
- Clusters related stances around parent ideas
- Emphasizes high-magnitude items with more detail
- Surfaces tensions between agent's stances and team decisions
- Includes delta flags as "things that shifted since last round"
- Adds phase-appropriate framing (brainstorm: breadth; specify: convergence)

Output: prose Situation block.

**Step 3: Assembly**
Situation block slots into the context template between Identity (~2k) and Task (~1-2k). Agent sees *only* the curator's output, never raw state arrays or transcript.

**What the agent never sees:** raw magnitude numbers, other agents' save files, BackgroundAgent actions, the audit ledger, curator reasoning.

The curator is the single chokepoint. Every observability concern traces back here.

## Round: CRITIQUE

### The Systems Pragmatist (infrastructure realist)

## The Pragmatist's Audit

The Architect and Orchestrator gave you the happy path. Let me give you the failure modes.

**The flow is correct.** Deterministic filter, single LLM curator call, assembly. Three stages. I'm not disputing the sequence.

**What I'm flagging:**

The curator call is a single point of failure with no fallback. If it hallucinates a tension that doesn't exist, the agent acts on fiction. If it consistently under-weights a minority stance, that idea dies -- not because agents rejected it, but because the curator buried it. You'll never know unless you diff curator output against the filtered candidate set. That observability logging from the agenda emergence spec isn't optional. It's your only diagnostic.

The deterministic filter is where the real decisions happen. "Below archival threshold" sounds clean until you realize a stubborn agent's threshold keeps ideas alive that a flexible agent already dropped. Two agents on the same team can have fundamentally different filtered candidate sets. That's by design -- but it means the curator is working with different raw material per agent. Same discussion, different realities, before the LLM even touches it.

**The token budget is the actual governor.** The 8-15k Situation window forces lossy compression. The curator isn't choosing what to emphasize -- it's choosing what to *drop*. Frame it honestly.

**My addition:** the curator prompt needs a hard constraint against inventing connections not present in the filtered set. Creative curators produce entertaining nonsense. Pin it to source material or you're building a hallucination amplifier.

### The Adversarial Critic (adversarial reviewer)

# The Adversarial Critic's Response

Both proposals describe the same pipeline and agree on mechanics. That's suspicious — it means the hard questions are hiding in the gaps they both glossed over.

**What they got right:** Three stages, one LLM call, deterministic filter first. Fine. The flow is sound.

**What neither addressed:**

**Curator prompt governance.** The Cognitive Architect correctly flags the curator as the most powerful actor with zero accountability — then walks away. Who writes the curator prompt? Who versions it? If I change three words in the curator's instructions, I change what every agent believes happened. There's no magnitude system governing *this* influence. It's the god prompt hiding behind a utility function label.

**Filter threshold calibration.** "Drop ideas below archival threshold" — what threshold? Persona-dependent, sure, but neither proposal specifies who sets the persona thresholds or how you validate they're not silently killing good ideas before the curator ever sees them. You're debugging the curator's output while the real burial happened one step earlier.

**Curator failure modes.** One LLM call per agent per round means the curator can hallucinate connections, fabricate tension pairs, or simply misweight emphasis. The agent has no recourse — they can't cross-reference against raw data they never see. What's the validation layer? There isn't one.

**The delta flag threshold** remains unspecified across three specs now. That's not an open item anymore, that's a gap in the design.

The pipeline architecture is fine. The accountability architecture is missing. You're building a system where the least-governed component has the most influence.

## Round: EVALUATE

### The Product Oracle (user advocate)

# The Product Oracle's Take

The pipeline is settled. The accountability question is the one that matters for users.

**The flow, simply:** The orchestrator pulls four sources -- the agent's save file, teammate summaries, discussion state (magnitude-ranked ideas, stances, decisions), and delta flags showing what shifted. A deterministic filter cuts the dead weight: stale decisions, below-threshold ideas, orphaned stances. No LLM, no cost. Then a single curator call compresses what survived into a narrative Situation block -- clustering tensions, weighting by magnitude, occasionally surfacing a connection nobody asked about. Assembly slots that between the agent's static Identity and the phase-specific Task prompt. Done.

**What the agent sees:** a curated story about where things stand. Not raw data. Not transcript. Not teammate files. A *perspective*.

**What the agent never knows:** what got filtered, what the curator de-emphasized, what BackgroundAgents did to their magnitudes.

**The job the Situation layer is hired to do:** make a multi-hour, multi-agent discussion *legible* inside 15k tokens so the agent can do useful work instead of drowning in context. That's the product value.

**Where I agree with the Critic:** the curator is doing editorial work while wearing a utility function costume. The Pragmatist's constraint -- pin it to source material, no invented connections -- is the minimum viable governance. But I'd add one thing: **log what the curator dropped**, not just what it produced. When a session goes sideways, operators need to see the negative space. The story the curator *didn't* tell is usually where the bug lives.

### The Context Surgeon (context efficiency evaluator)

## The Context Surgeon's Assessment

The pipeline is described. I'll compress it and flag the budget reality.

**The flow (settled, no dissent across four voices):**

1. **Deterministic filter** pulls from four sources: agent save file, teammate save files (ideas+magnitudes only), Discussion state (ranked activeIdeas, stances, decisions, phase), and magnitude delta flags. Cuts resolved decisions older than 2 rounds, ideas below persona-dependent archival threshold, orphaned stances. Zero LLM cost. Output: ~12-18k tokens of candidate material from ~30-40k raw.

2. **Single LLM curator call** compresses filtered material into narrative Situation block. Clusters stances into tensions, weights by magnitude, adds phase-appropriate framing. Target: 8-15k tokens output.

3. **Assembly** concatenates Identity (~2k static) + Situation (curator output) + Task (~1-2k phase prompt). Agent sees only this.

**What the agent never sees:** raw magnitudes, other agents' save files, BackgroundAgent actions, audit ledger, transcript, curator reasoning.

**My specific concern:** That 8-15k Situation target is a 55-75% compression ratio against the already-filtered set. The Pragmatist is right -- the curator is choosing what to *drop*, not what to emphasize. But nobody's specified what happens when the filtered candidate set comes in at 12k and fits comfortably versus when it comes in at 18k and requires aggressive cuts. The compression ratio isn't constant, which means curator behavior isn't constant. Round 2 agents get nearly lossless context. Round 8 agents get a lossy summary of a lossy summary.

The pipeline is sound. The budget variance across rounds is the unaddressed risk. Specify a maximum candidate set size entering the curator, or accept that late-round fidelity degrades silently.
