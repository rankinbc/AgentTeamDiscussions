# Discussion Productivity Mechanisms -- Ideas & Status

**Date:** 2026-03-24
**Pillar:** Environment + Discussion System

The core problem: agent discussions tend toward circular debate. Agents bicker, restate positions, and never commit. This document tracks mechanisms that force conversations toward productive outcomes.

---

## Already Designed (in existing docs)

These mechanisms are documented but not yet implemented. Reference the source docs for full details.

### Discussion System (in-round)

| Mechanism | Source Doc | Status |
|---|---|---|
| Forcing function on every turn (concrete question/directive) | conversation-engine/design-decisions.md | Partially implemented in live_conversation.py |
| Agent signals (stance, confidence, ready_to_advance, key_claim) | conversation-engine/design-decisions.md | Not implemented |
| Arc position (early/midway/late/wrapping-up) instead of countdown | conversation-engine/design-decisions.md | Not implemented |
| Two-tier phase evaluation (heuristic + LLM evaluator) | conversation-engine/design-decisions.md | Not implemented |
| Dynamic turn ordering by urgency/rebuttal priority | conversation-engine/rebuttal-priority.md | Not implemented |
| Urgency meter (passive growth + challenge spikes) | conversation-engine/rebuttal-priority.md | Not implemented |
| Ego injection when challenged (scaled by assertiveness * bluntness) | conversation-engine/agent-behavior-mechanisms.md | Not implemented |
| Challenger persistence (scaled by stubbornness) | conversation-engine/rebuttal-priority.md | Not implemented |
| Phase exit gates (idea count, disagreement resolution, etc.) | creativity-engine/phase-dynamics.md | Not implemented |
| Sub-cycle loops for non-foundational gaps | conversation-engine/design-decisions.md | Not implemented |

### Environment (between-round)

| Mechanism | Source Doc | Status |
|---|---|---|
| Convergence Suppression (detect agreement pile-on, inject provocation) | creativity-engine/anti-slop-mechanisms.md | Not implemented |
| Agreement Tax (must add substance when agreeing) | creativity-engine/anti-slop-mechanisms.md | In agent prompts only |
| Devil's Advocate Duty (rotated responsibility) | creativity-engine/anti-slop-mechanisms.md | In agent prompts only |
| Domain Pivot Triggers (cross-domain injection when stuck) | creativity-engine/anti-slop-mechanisms.md | Not implemented |
| STRETCH / Uncomfortable Idea Quota | creativity-engine/anti-slop-mechanisms.md | In agent prompts only |
| Drift correction (conditional injection on 3+ agreeing turns) | conversation-engine/design-decisions.md | Not implemented |
| Escalation (nudge -> directive -> constraint) | conversation-engine/design-decisions.md | Not implemented |
| Shannon entropy quality gate (3.5 threshold) | conversation-engine/design-decisions.md | Not implemented |
| Background Agent: Muse (random stimuli, provocations) | creativity-engine/anti-slop-mechanisms.md | Not implemented |
| Background Agent: Curator (novelty scoring, domain pivots) | creativity-engine/anti-slop-mechanisms.md | Not implemented |
| Background Agent: Director (trait tweaking, position addition) | creativity-engine/anti-slop-mechanisms.md | Not implemented |
| Background Agent: Weaver (cross-thread connection, groan zone synthesis) | creativity-engine/anti-slop-mechanisms.md | Not implemented |
| Background Agent: TieBreakerGhost (deadlock resolution) | creativity-engine/anti-slop-mechanisms.md | Not implemented |

---

## New Ideas (from 2026-03-24 design session)

These are additions to the existing design, introduced in session-platform-and-agent-management.md.

### Topic-Level Attributes (Layer A)

**discussion_type** -- Shapes the entire conversation flow:
- `decision` -- must end with a committed choice, dissent recorded
- `exploration` -- divergent, no commitment required
- `critique` -- tear apart an existing proposal
- `spec-building` -- produce a document section by section

**urgency** -- Controls how aggressive the orchestrator is (low/medium/high/critical). High urgency enables deadline pressure, forced commitments, stakes escalation.

**challenges** -- Specific forcing functions injected into the conversation. Problems the group MUST address. If unaddressed by midway, the orchestrator surfaces them explicitly. Different from general topic -- these are specific questions or decisions that can't be deferred.

**success_criteria** -- What "done" looks like. Gives the orchestrator a target to evaluate against.

**deliverables** -- Concrete outputs the session must produce (a decision, a document, a ranked list).

### Orchestrator Dynamics (Layer B)

**Perspective Shift** -- When stuck, the orchestrator asks agents to argue FROM a different position. Forces steelmanning the opposition. Trigger: stale detection.

**Stakes Escalation** -- Orchestrator introduces real consequences to cut through abstract debate. "If you ship this and it's wrong, what breaks?" Makes decisions feel consequential.

**Concrete Scenario** -- Orchestrator drops a specific situation agents must react to. "A user just cancelled after the free trial. Why?" Forces agents out of generalities into specifics.

**Force Commitment** -- Starting at the converge phase, agents must state a preference in a specific format: "I advocate for [X] because [Y]." No more hedging.

**Deadline Pressure** -- Visible round countdown in later phases. "You have N rounds left to reach a decision." Counterpoint to the existing design decision against countdown visibility -- this applies only in converge/commit phases where urgency is appropriate.

**Stale Detection** -- If the same positions repeat for N rounds (configurable, default 3), the orchestrator intervenes with one of: perspective shift, concrete scenario, stakes escalation, or direct "you're going in circles" callout.

---

## Implementation Priority (suggested)

**Tier 1 -- Highest impact, simplest to build:**
- Forcing function on every turn (partially exists)
- discussion_type and urgency in brief config
- challenges as injected forcing functions
- Stale detection (simple repetition check)
- Force commitment in later phases

**Tier 2 -- High impact, moderate complexity:**
- Agent signals (stance, confidence, ready_to_advance)
- Convergence Suppression
- Drift correction
- Perspective shift
- Concrete scenario injection
- Stakes escalation

**Tier 3 -- Full environment layer:**
- Dynamic turn ordering
- Urgency meter with challenge spikes
- Background agents (start with Curator and Muse)
- Between-round context pipeline
- Shannon entropy quality gate

**Tier 4 -- Advanced:**
- Ego simulation and challenger persistence
- Director agent (personality evolution)
- Weaver agent (cross-thread synthesis)
- TieBreakerGhost
- Full bench system with heuristic rotation
