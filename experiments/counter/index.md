# Proposed Design Docs

Generated: 2026-03-17 22:40
Brief: conversation-system-v1.md
Mode: counter -- 1st proposer solo, 2nd proposer sees 1st and must counter-propose
Total generation time: 6.6 minutes

## Round Structure

- **Propose**: The Cognitive Architect (creativity engine designer)
- **Counter**: The Flow Orchestrator (mechanical flow designer)
- **Critique**: The Systems Pragmatist (infrastructure realist), The Adversarial Critic (adversarial reviewer)
- **Evaluate**: The Product Oracle (user advocate), The Context Surgeon (context efficiency evaluator)

## Design Docs

- [01. How does a round begin after a reset?](01-how-does-a-round-begin-after-a-reset.md) ([transcript](01-how-does-a-round-begin-after-a-reset-transcript.md))
- [03. What's in the Discussion and DiscussionRound state?](03-what-s-in-the-discussion-and-discussionround-state.md) ([transcript](03-what-s-in-the-discussion-and-discussionround-state-transcript.md))

## Accumulated Open Questions

- [Q1] What is the exact format of the save file? The spec says "ideas with magnitudes, stances with magnitudes, committed decisions, 3-5 sentence personal recap" but doesn't define the serialization. JSON? Markdown? YAML? The format affects token efficiency and curator parseability.
- [Q1] How are magnitude deltas computed when multiple between-round processes modify the same value? If intra-team talk shifts Idea X by +1.5 and a BackgroundAgent shifts it by -0.8, does the delta show "+0.7" (net) or both changes separately? Net is cheaper on tokens; itemized is more informative.
- [Q1] Who decides the round-open agenda? The task prompt says "here's the agenda" but it's unclear whether the agenda is orchestrator-determined (based on highest-magnitude unresolved items), phase-determined (brainstorm has no agenda, review has explicit checklist), or absent (agents self-select what to open with).
- [Q1] How does the archival threshold interact with round-open assembly? If a stubborn agent's threshold keeps a low-magnitude idea alive that a flexible agent would have dropped, does the idea appear in both agents' save files with different magnitudes, or only in the stubborn agent's save file?
- [Q3] **Save file serialization format.** The save file contains ideas with magnitudes, stances with magnitudes, committed decisions, and a 3-5 sentence personal recap. The format (JSON, YAML, structured markdown) affects token efficiency when injected into Layer 0 and parseability by the curator. JSON is most compact; YAML is most readable in session review; structured markdown is most natural for LLM consumption. This needs a decision before implementation.
- [Q3] **Archival threshold interaction with idea_registry.** When a stubborn agent's persona-dependent threshold keeps a low-magnitude idea alive that a flexible agent would have dropped, the idea exists in `idea_registry` with different per-agent magnitudes. The archival sweep must be per-agent -- an idea can be archived for Agent A (magnitude fell below their threshold) while remaining active for Agent B (whose stubbornness keeps the threshold lower). The registry needs to track per-agent magnitude, not a single global magnitude. The IdeaRecord structure must account for this.
- [Q3] **Event log as optional V1 backing store.** Multiple participants noted that an append-only event log is valuable for debugging and session review ("what happened to Idea X over 15 rounds?") but agreed it should not be load-bearing for agent context. The question is whether to build it in V1 as a write-only audit trail or defer entirely. Building it is cheap (just append); not building it means reconstructing history from snapshots, which is lossy.
- [Q3] **Random event system specifics.** The `random_events` field exists in round state but the event system's mechanics are undefined: what is the probability distribution, what kinds of events exist, how many agents can be affected per round, and can events contradict each other? This needs its own design pass.