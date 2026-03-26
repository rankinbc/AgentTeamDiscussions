### The Flow Orchestrator (mechanical flow designer)

I'll trace the load-bearing sequences and name what's stable.

## Three Things V2 Must Not Touch

**1. The session.json manifest as single source of truth.**

The state lifecycle is clean: create manifest, hydrate runtime state, persist on transitions. Atomic writes (D1 from Q1) fix the only real gap. The shape of this file — config + runtime state in one document — means every component reads from one place. Splitting this into multiple stores or adding a database layer would break the simplest correct thing in the system.

**2. The round-based execution sequence: propose, critique, evaluate, synthesize.**

This is the spine. Every output artifact depends on this ordering. The round structure may be a latency multiplier (Q4-D6), but it is also what makes transcripts readable and synthesis possible. V2 should optimize within rounds (parallelism, speaking order rotation), not replace the sequence. "Dynamic round selection" or "agent-driven flow" would require rebuilding DiscussionEngine, RoundRunner, and every prompt template simultaneously.

**3. The file-system-as-database output model.**

Sessions write markdown files to predictable paths. The completion marker pattern works (Q1-D3). The eval command reads from disk. The UI reads from disk via SSE. There is no query layer because none is needed. Adding a persistence abstraction would be pure cost — the current model handles crash recovery, human readability, and tooling integration in one mechanism.

Everything else is fair game. Prompt templates, agent layers, config structure, synthesis strategy — all semi-rigid or flexible per the prior constraint classification.

## Position Summary
V2 should protect three mechanical sequences: manifest-as-truth, round execution order, and filesystem persistence. I reject any proposal that introduces new state stores, dynamic flow control, or persistence abstractions — these would replace working mechanisms with unproven ones. The cheapest V2 is the one that optimizes within these boundaries rather than redrawing them.

### The Cognitive Architect (creativity engine designer)

The Flow Orchestrator is right on two of three, but wrong on the one that matters most.

**Session.json and filesystem persistence — agreed, for the boring reason.** These work because they're simple. Nothing to add.

**The round sequence is NOT load-bearing in the way described.** The Orchestrator calls propose-critique-evaluate "the spine." But D3 from Q2 already established that context accumulation dominates agent identity by Round 2. The round *labels* aren't producing distinct cognitive phases — they're producing three chances for agents to converge on the same middle. Protecting this sequence from change is protecting a naming convention, not a mechanism. V2 should absolutely experiment with round structure — different orderings, different group compositions per round. That's where mode definitions already live (team YAML), and it's classified as flexible.

**What the Orchestrator missed: the prompt assembly interface.**

This is the actual untouchable. `PromptBuilder.cs` takes six agent layers + round context + prior responses and produces a single string that goes to Claude CLI. Every agent behavior difference lives or dies in that assembled prompt. The template structure (identity → situation → task) is the load-bearing contract between agent design and LLM output. Change the assembly order, change the relative token weight of layers, change where prior responses get injected — and you change every agent's behavior simultaneously with zero ability to isolate the effect.

D4 from Q2 says "audit transcript content before redesigning agent layers." That audit is meaningless if you've also changed the assembly pipeline. The prompt interface must be frozen while you measure everything else.

## Position Summary
V2 must freeze the prompt assembly interface (template structure and injection order) because it's the only mechanism where agent identity actually contacts LLM behavior — changing it invalidates all measurement. I reject protecting round sequence as architectural constraint; it's a mode-level concern already designed to vary. The Orchestrator correctly identified manifest and filesystem as stable, but missed the real load-bearing seam.


<!-- complete -->
