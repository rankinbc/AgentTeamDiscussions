# Proposed Design Docs

Generated: 2026-03-18 04:04
Brief: v1-spec-gaps.md
Mode: compete -- Competitive vs Minimalist proposers
Total generation time: 5.7 minutes

## Round Structure

- **Propose**: The Cognitive Architect (creativity engine designer), The Flow Orchestrator (mechanical flow designer)
- **Critique**: The Systems Pragmatist (infrastructure realist), The Adversarial Critic (adversarial reviewer)
- **Evaluate**: The Product Oracle (user advocate), The Context Surgeon (context efficiency evaluator)

## Design Docs

- [05. How does prior context get managed as questions accumulate?](05-how-does-prior-context-get-managed-as-questions-accumulate.md) ([transcript](05-how-does-prior-context-get-managed-as-questions-accumulate-transcript.md))
- [06. What does session recovery look like?](06-what-does-session-recovery-look-like.md) ([transcript](06-what-does-session-recovery-look-like-transcript.md))
- [07. How do we make the evaluation feedback loop reliable?](07-how-do-we-make-the-evaluation-feedback-loop-reliable.md) ([transcript](07-how-do-we-make-the-evaluation-feedback-loop-reliable-transcript.md))

## Accumulated Open Questions

- [Q5] **Extraction loss rate**: What percentage of meaningful constraints survive extraction into the ledger? The beta transcripts from questions 1-5 should be run through this scheme manually to measure coverage before relying on it at scale.
- [Q5] **Supersession clarity**: When a later decision supersedes an earlier one, agents must infer this from the ledger's chronological order. If this proves unreliable in practice, a lightweight "SUPERSEDES Q{n}" tag may be needed on ledger entries.
- [Q5] **Topic tag vocabulary**: Whether topic tags should be drawn from a fixed vocabulary or free-form. Fixed tags enable future retrieval optimizations but add a classification step. Free-form is simpler but less structured.
- [Q6] **Extraction loss rate** (from Q5): What percentage of meaningful constraints survive extraction into the ledger? Remains open. Not addressable by recovery design.
- [Q6] **Supersession clarity** (from Q5): Whether agents reliably infer that later decisions supersede earlier ones from chronological order alone. Remains open.
- [Q6] **Topic tag vocabulary** (from Q5): Whether topic tags should be fixed or free-form. Remains open.