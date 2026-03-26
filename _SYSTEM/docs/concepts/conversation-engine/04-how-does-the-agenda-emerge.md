# How does the "agenda" emerge?

*Generated: 2026-03-17 21:43 | Question 4 | 150s*

The spec is ready to write -- just needs your file write permission. Here's what I synthesized:

**Spec: Agenda Emergence** -- reconciled from all six panel voices into one authoritative document.

**The decision:** No agenda object. The agenda emerges from magnitude-ranked `activeIdeas`, made legible by the curator's Situation block, with soft steering in the round-open Task prompt. This was already implicitly decided when `sharedAgenda` was cut from DiscussionRound state.

**Three pipeline stages (all already exist, no new machinery):**
1. **Magnitude ranking** during deterministic filter -- the raw agenda. Added: **magnitude delta flags** surfacing ideas with significant between-round movement (one extra sort, zero LLM calls). This was the Pragmatist's contribution -- counteracts popularity bias.
2. **Curator emphasis** -- translates ranking into narrative weight in the Situation block. Hidden agenda-setter whether you call it that or not.
3. **Soft steering** -- round-open Task includes a short ranked topic list. Agents can ignore it. Exists for nudging and observability.

**The Adversarial Critic's real contribution:** observability. The spec requires logging the magnitude-ranked list, delta flags, curator output, and Task prompt so operators can diff "what the system recommended" vs. "what agents discussed." Without this, you're debugging blind when sessions produce garbage.

**Four open issues flagged:** magnitude delta threshold calibration, decay rate (still unresolved from prior specs), curator emphasis measurement for V2, and consensus detection.

Please approve the file write to save it to `output/spec_agenda_emergence.md`.