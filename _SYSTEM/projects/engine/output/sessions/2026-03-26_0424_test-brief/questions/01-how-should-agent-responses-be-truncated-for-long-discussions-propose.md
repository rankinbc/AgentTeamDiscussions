### The Cognitive Architect (creativity engine designer)

# Stratified Memory Architecture

The answer isn't sliding window, full history, or summarization. It's **all three simultaneously, at different layers** — because that's how productive human groups actually maintain coherence over long deliberations.

Research on transactive memory systems (Wegner, 1987) shows that effective groups don't all remember the same things. They develop *differentiated memory* — each member holds different pieces, plus a shared index of who knows what. We should steal this directly.

**Three memory tiers, applied per-agent:**

**Tier 1 — Shared Scaffold (always present).** A running structural summary: decisions made, open tensions, current question. Every agent sees this identically. This is the group's shared reality. ~500 tokens, updated each round by the synthesizer.

**Tier 2 — Role-Relevant Window (sliding, filtered).** Each agent sees the last N messages, but *filtered by relevance to their role*. The critic sees prior objections and rebuttals. The architect sees prior structural proposals. This isn't cosmetic — it produces genuinely different response patterns because agents are literally reasoning from different evidence bases.

**Tier 3 — Full History (available on demand).** When an agent's response references something outside their window, a retrieval step pulls the specific passage. Most rounds won't trigger this.

**Why this beats the alternatives:**

Uniform sliding windows create artificial amnesia — agents forget their own prior positions. Full history wastes tokens on irrelevant cross-talk. Pure summarization loses the texture that makes critique sharp.

Stratified memory produces the cognitive diversity that matters: **agents arguing from different but overlapping evidence**, exactly like real expert panels.

The synthesizer already exists in this system. Make it do double duty as the shared scaffold maintainer.

### The Flow Orchestrator (mechanical flow designer)

# Three Tiers Is Two Too Many for V1

The Cognitive Architect's proposal is intellectually elegant and operationally premature. Let me trace the actual execution sequence it requires:

1. Synthesizer produces shared scaffold (new responsibility)
2. Role-relevance filter classifies every message per agent role (new component)
3. Retrieval system detects references and pulls history passages (new component)
4. All three layers merge into a per-agent context assembly (new component)

That's three new subsystems bolted onto a synthesizer that already has known fragility concerns. The CONCERNS.md flags the live synthesizer as a fragile area *today*. Adding scaffold maintenance to it compounds risk.

**What actually solves the problem with minimal moving parts:**

One tier. Shared summary + sliding window. Same window for every agent.

The summary is the scaffold — decisions made, open questions, current tensions. The synthesizer already produces something close to this. The window is the last N messages, unfiltered. N is configurable in `defaults.yaml`.

That's it. No role-based filtering. No on-demand retrieval. No per-agent context assembly.

**Why role-filtered windows are a deferral, not a cut:**

The differentiated-evidence idea has merit, but it's an optimization. You need baseline data showing *where* agents actually lose coherence before you know what filtering rules to write. Ship uniform windows, instrument them, then decide.

**The exact sequence I'd implement:**

Round starts → synthesizer emits summary → prepend summary → append last N messages → send to agent.

One path. One config knob. Zero new components.


<!-- complete -->
