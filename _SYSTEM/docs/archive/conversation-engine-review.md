# Task: Review Conversation Engine Architecture

**Created:** 2026-03-25
**Priority:** High -- blocks understanding of which conceptual ideas to adopt

## Background

The agent-generated design panel (2026-03-17) produced 10 detailed specs exploring how the conversation engine could work. These specs assume a **magnitude system** with concepts like:

- **Ideas/Stances** -- tracked objects with magnitude scores that rise/fall based on agent support
- **BackgroundAgents** -- autonomous processes that run between rounds (research, synthesis, drift correction)
- **Intra-team deliberation** -- structured between-round processing where agents influence each other's magnitude scores
- **LLM Curator** -- a separate LLM call that compresses state into context for each turn
- **Agenda emergence** -- implicit topic steering via magnitude-ranked ideas

These mechanisms were designed to **push conversations toward conclusions** and prevent agents from going back and forth aimlessly. They may or may not be the right approach for V1.

## What Needs to Happen

1. **Map how the V1 conversation system actually works today** -- Read the v1-orchestrator-spec, the beta-agent-interaction code, and the existing conversation-engine feature specs. Document the current flow end-to-end.

2. **Identify the "aimless conversation" problem** -- Is the current system (propose/critique/evaluate rounds with synthesis) sufficient to drive toward conclusions? Or does it need additional steering mechanisms?

3. **Evaluate which conceptual ideas are needed:**
   - Magnitude system (ideas/stances with scores)
   - BackgroundAgents (between-round processing)
   - Intra-team deliberation
   - Curator-based context curation
   - Agenda emergence via magnitude ranking
   - Research scope controls (already promoted to feature spec)

4. **Decide:** For each concept, categorize as:
   - **Adopt for V1** -- needed now
   - **Stash for V2** -- good idea, not needed yet
   - **Replace** -- superseded by a simpler approach
   - **Drop** -- over-engineered, not worth the complexity

5. **Produce a conversation engine README** that describes how the system actually works and what's planned.

## Conceptual Ideas Location

All agent-generated concept docs are in:
```
_SYSTEM/docs/concepts/conversation-engine/
```

With raw transcripts in:
```
_SYSTEM/docs/concepts/conversation-engine/transcripts/
```

## Related Specs

- `features/v1-orchestrator-spec.md` -- current V1 design
- `features/conversation-engine/` -- 7 feature specs
- `features/entity-model.md` -- data model (includes magnitude concepts)
- `concepts/design-principles.md` -- core design philosophy
- `concepts/agent-behavior-philosophy.md` -- ego, urgency, forced disagreement findings
