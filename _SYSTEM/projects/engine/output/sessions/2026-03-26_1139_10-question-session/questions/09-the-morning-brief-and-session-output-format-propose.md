### The Cognitive Architect (creativity engine designer)

The Morning Brief isn't a summary problem. It's a **decision archaeology** problem.

Every synthesis tool I've seen makes the same mistake: it tries to compress the discussion into agreement. But the overnight reader doesn't need agreement — they need the **decision topology**. What was contested, what was conceded, and what was silently dropped.

**My design: The Three-Layer Output**

**Layer 1: The Decision Record** (machine-structured, not extracted)
Each question produces exactly one decision record written by the synthesis step — not regex-parsed from agent output. Fields: `decision`, `dissent` (who disagreed and their strongest argument), `confidence` (synthesis agent's honest assessment), `dropped_threads` (ideas raised but never resolved). This is YAML, not prose. The synthesis agent writes it as structured output, not free text that gets parsed later.

**Layer 2: The Tension Map** (the actual value)
A short prose section — 3-5 sentences per question — that captures *unresolved tensions*. Not "what was decided" but "what almost went the other way." This is what makes the brief worth reading. A summary of agreements is worthless; a map of fault lines is strategic intelligence.

**Layer 3: The Transcript** (already exists, keep it)
Full round-by-round output stays as-is for deep dives.

The Morning Brief itself becomes a rendering of Layers 1 and 2 — a template-driven document, not an LLM summarization pass. The synthesis agent's job is producing structured Layer 1 and Layer 2 content. The Morning Brief is just a Scriban template over that data.

This eliminates the fragile regex problem entirely. You never extract — you generate structured output at the point of synthesis.

## Position Summary
I advocate making the synthesis step produce structured decision records and tension maps as its primary output, with the Morning Brief as a deterministic template render over that data. I reject any architecture that extracts structure from prose after the fact — regex parsing, post-hoc summarization, or key-takeaway mechanisms bolted onto discussion rounds. The reason: extraction is lossy and fragile by definition; generation at the point of synthesis is where the LLM actually has full context, so that's where structure should be created.

### The Flow Orchestrator (mechanical flow designer)

The Cognitive Architect's three-layer design is almost right but has a critical sequencing flaw: it doesn't specify *when* the synthesis agent runs relative to what data.

Let me trace the actual operation sequence.

**Current flow:** Rounds complete → DiscussionEngine calls synthesis → MorningBriefGenerator runs over ledger → output files written. Two separate LLM passes, second one parsing prose from the first.

**The Architect's proposal collapses this to one pass.** Good. But "the synthesis agent writes structured YAML" hides the hard question: what's in the synthesis prompt's context window?

For each question, the synthesis agent needs: all round outputs (propose, critique, evaluate). That's potentially 7 agents × 3 rounds × ~500 words = 10,500 words of input just for transcript. The structured output request (decision record + tension map) adds template instructions. This is fine today. It stops being fine if we add rounds or agents.

**My correction:** The synthesis step should receive **round outputs only** — not prior questions' synthesis results, not the session manifest, not the decisions ledger. One question in, one structured output out. The Morning Brief generator then assembles across questions using only the structured records. No LLM pass for assembly — pure template rendering.

This gives us exactly two LLM calls per question (synthesis) and zero for the brief itself. Deterministic assembly from structured parts.

The "dropped threads" field is the only part I'd cut. It requires the synthesis agent to reason about absence — what *wasn't* said — which is unreliable. If a thread matters, an agent will raise it. If none did, it wasn't dropped; it was rejected implicitly.

## Position Summary
I advocate the Architect's single-pass structured synthesis with one correction: strict input scoping (one question's rounds only, no cross-question context) and deterministic template assembly for the Morning Brief with zero additional LLM calls. I reject the "dropped threads" field because detecting absence is an unreliable LLM operation that adds complexity without trustworthy signal. The reason: every piece of this pipeline must have a traceable input→output path, and "what wasn't said" has no input to trace.


<!-- complete -->
