# What's in the Discussion and DiscussionRound state?

*Generated: 2026-03-17 21:40 | Question 3 | 185s*

The spec is ready to write. Here's what I synthesized from the full panel discussion:

**Spec: Discussion and DiscussionRound State** -- reconciled from all five panel voices (Cognitive Architect, Flow Orchestrator, Systems Pragmatist, Adversarial Critic, Product Oracle, Context Surgeon) into one authoritative document.

**Discussion State (session-lifetime, 7 fields):**
- `phase` -- enum gating task templates and turn caps
- `roundNumber` -- integer driving bootstrap vs. full pipeline
- `activeIdeas[]` -- the heartbeat: id, text, origin, magnitude, roundIntroduced. Updated by agents, research, BackgroundAgents, intra-team talk
- `activeStances[]` -- positions on ideas with magnitude. Curator clusters these to surface tensions
- `decisions[]` -- settled ground truth. Append-only ratchet that moves conversations forward
- `activeArtifacts[]` -- specs under construction for specify/review phases
- `transcriptRef` -- pointer only, curator reads it, agents never see raw transcript

**DiscussionRound State (per-round, disposable, 5 fields):**
- `turnCount` -- termination trigger against phase cap
- `speakerOrder[]` -- deterministic rotation set at round-open
- `roundTranscript[]` -- append-only, IS the mid-round context
- `temperature` -- stance magnitude variance driving curator emphasis and BackgroundAgent urgency
- `roundTheme` -- **cut candidate** (decorative, nothing enforces it)

**Key decisions made:**
- `roundNumber` belongs on Discussion (session-owned), not DiscussionRound -- Adversarial Critic caught the conflict
- `sharedAgenda` cut for V1 -- redundant with magnitude-ranked activeIdeas
- Write ownership resolved: BackgroundAgents run before thinking routines in the explicit 7-step between-round pipeline
- Temperature uses stance magnitude variance as single V1 metric

**Six open issues flagged:** magnitude inflation control (decay vs. hard cap), roundTheme cut/keep, temperature formula calibration, per-phase turn cap defaults, shared agenda V2 reconsideration, and decay vs. hard cap decision.

Please approve the file write to save it to `output/spec_discussion_and_round_state.md`.