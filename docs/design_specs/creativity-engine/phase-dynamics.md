# Phase Dynamics -- How the Creativity Engine Changes Per Phase

**Status:** Draft - discovered during PRD creation
**Date:** 2026-03-17

---

## Concept

The creativity engine isn't static. Each Phase activates different personality weightings, bench configurations, communication modes, technique categories, and anti-slop mechanisms. The system shifts from maximum divergence (brainstorm) through progressive convergence (refine, specify) to adversarial validation (review).

---

## Phase Configurations

### Brainstorm Phase

**Goal:** Maximum idea quantity and diversity. Push past obvious ideas into genuinely novel territory.

| Dimension | Setting |
|---|---|
| Communication mode | YES-AND -- build, extend, never critique |
| Active technique categories | creative, wild, theatrical, biomimetic, quantum, cultural |
| Bench priority | High creativity-temperature agents, Connector, Anarchist, Visionary archetypes |
| Anti-slop emphasis | Domain pivot triggers, convergence suppression, uncomfortable idea quota |
| Deliberation profile | Short internal turns, high volume, breadth over depth |
| Phase exit gate | Minimum Idea count (configurable, default 50+), domain diversity threshold |
| Agreement tax | Maximum -- pure agreement costs a turn |
| Muse activity | High -- frequent random stimuli and provocations |
| Devil's advocate duty | Active, rotating every 5 turns |

### Refine Phase

**Goal:** Challenge assumptions, find gaps, stress-test the best ideas from brainstorm. Kill weak ideas. Strengthen strong ones.

| Dimension | Setting |
|---|---|
| Communication mode | CHALLENGE -- poke holes, question assumptions, demand evidence |
| Active technique categories | deep, structured, risk analysis |
| Bench priority | Challenger, Detective, Skeptic archetypes. Customer and Competitor positions amplified. |
| Anti-slop emphasis | Perspective enforcement, novelty scoring (but applied to critiques -- are critiques diverse or all the same?) |
| Deliberation profile | Longer internal turns, depth over breadth, position papers for significant disagreements |
| Phase exit gate | All major Ideas have been challenged and either defended or killed. Disagreement queue below threshold. |
| Agreement tax | Moderate -- agreement is fine if paired with "and here's the remaining risk" |
| Muse activity | Low -- focused analysis, not random stimulation |
| Devil's advocate duty | Not needed -- the Phase itself is adversarial |

### Specify Phase

**Goal:** Pin down requirements and acceptance criteria for surviving ideas. Precision over creativity. The output of this phase should be implementable.

| Dimension | Setting |
|---|---|
| Communication mode | SPECIFY -- define exactly, accept criteria, edge cases, no ambiguity |
| Active technique categories | structured (Decision Tree, Solution Matrix, Morphological Analysis) |
| Bench priority | Systematic cognitive style, Builder position, high attention span agents |
| Anti-slop emphasis | Perspective enforcement (Builder position asking "what exactly happens when...?"), silence as signal for non-relevant agents |
| Deliberation profile | Long internal turns, completeness checks, each Decision logged with full provenance |
| Phase exit gate | All requirements have acceptance criteria. Builder agent confirms specs are implementable. No undefined edge cases. |
| Agreement tax | Low -- agreement on specifications is productive |
| Muse activity | Off -- this is not the time for random stimulation |
| Devil's advocate duty | Off -- replaced by Builder agent's natural "is this buildable?" pressure |

### Review Phase

**Goal:** Adversarial validation. Find every weakness in the specs. The Competitor, Skeptic, and Regulator positions are most active.

| Dimension | Setting |
|---|---|
| Communication mode | ADVERSARIAL -- actively try to break the specs, find contradictions, missing pieces |
| Active technique categories | risk, competitive, deep (Failure Analysis, Chaos Engineering, Pre-mortem) |
| Bench priority | Competitor, Regulator, Skeptic, Support/Ops positions. High stubbornness agents. |
| Anti-slop emphasis | Surprise audits on review quality (are reviewers finding real issues or surface-level nits?) |
| Deliberation profile | Medium internal turns, focused on specific weaknesses |
| Phase exit gate | Spec validation gate passes. All critical issues resolved. Agreement score above threshold. |
| Agreement tax | Maximum for the reviewing agents -- "it's fine" is not acceptable |
| Muse activity | Off |
| Devil's advocate duty | Not needed -- entire Phase is adversarial |

---

## Phase Transition Dynamics

When transitioning between phases:
1. BackgroundAgent (Weaver) generates a Briefing summarizing the outgoing phase
2. AgentMinds get adjusted -- Idea magnitudes recalculated based on phase outcomes
3. Bench rotation happens -- agents appropriate for the new phase come in
4. Communication mode switches (the orchestrator's per-turn prompt changes)
5. Anti-slop mechanism weights adjust
6. Phase-specific technique categories activate
