# Pre-mortem subject: Is the V2 critical path (build order) right?

The roadmap proposes this build order: blind proposals -> manifest versioning -> phase system -> key takeaways -> stale detection -> anti-sycophancy detection, with the BIT system in parallel. Is this the right plan?

## Current engine facts (as of 2026-10-05, verified against the code)

- C# .NET 8 engine shells out to `claude -p` for every agent turn; one system prompt per persona, built from YAML.
- A session runs a list of questions. Each question runs fixed rounds from a mode (e.g. propose -> critique -> evaluate),
  agents speak sequentially within a round, then one synthesis call writes a design doc.
- Between rounds, agents only see earlier rounds' "## Position Summary" blocks (3 sentences each); within a round they
  see earlier speakers in full.
- Context per turn: persona reminder, focus lens, role overlay, brief context, decided items + decisions ledger,
  headings of the previous design doc, open questions carried from earlier docs, discussion so far, the question.
  A budget enforcer trims unprotected sections when a payload exceeds ~10k tokens.
- The decisions ledger (DECIDED / CONTESTED / OPEN lines per question) chains forward to later questions.
  Until 2026-10-05 the synthesis template was never rendered, so no session before then produced a real ledger.
- An Evaluator exists: after a session it scores design docs (7 dimensions) and transcripts (10 dimensions) 1-10 via an
  LLM judge and writes a report. Nothing reads those scores back; persona YAML is static and edited by hand.
- There is no phase system, no moderator input channel, no research engine, and no live/rolling synthesis in the
  running code. Templates for rolling synthesis exist but are unused.
- One developer, solo project. Sessions are run occasionally, not in production. 17 sessions exist on disk.


---

# Source document: docs/v2/ROADMAP.md

# V2 Roadmap

## Confirmed V2 Features (from PRD Growth Section)

These are the features explicitly scoped as post-MVP growth:

1. **Phase System** — Brainstorm → Refine → Specify → Review with automatic transitions
2. **Moderator Input** — Live steering via HTTP during discussions
3. **Dynamic Turn Ordering** — Rebuttal priority / urgency meter
4. **Key Takeaway Mechanism** — Convergence detection and voting
5. **Evaluation Engine** — Rubric scoring against design doc quality dimensions
6. **Multiple Output Artifact Types** — PRD, architecture doc, user stories
7. **Research Engine** — External data gathering during discussions

## Critical Path (from Agent Panel Analysis)

Recommended build order based on dependency analysis and user value:

1. **Blind Proposals** (1-2 days) — Suppress prior context in propose phase. Highest immediate user value.
2. **Manifest Versioning** (0.5 day) — Co-deliver with blind proposals for schema evolution.
3. **Phase System** (2-3 days) — Metadata labeling, phase-specific prompt injection, transition logic. Foundational infrastructure for most V2 features.
4. **Key Takeaways** (1 day) — Extraction at phase boundaries.
5. **Stale Detection** (2 days) — Compare outputs across phase boundaries for repetition signals.
6. **Anti-Sycophancy Detection** (2 days) — Measure blind vs revealed position drift (measurement only).
7. **BIT System** (parallel track) — Personality dimensions, measurable independently.

Key insight: Start with blind proposals (changes what user reads immediately) rather than phases (invisible infrastructure). Phases enable blind proposals to be cleaner, but blind proposals work without phases.

## Vision (Post-V2)

- **Team Configuration Layer** — Multi-team with spokesperson/internal deliberation
- **MCP Message Broker** — Cross-team communication channel
- **Full Magnitude System** — Ideas/stances tracking and BackgroundAgents
- **Intra-team Deliberation** — Between rounds
- **Context Management** — Prior sessions, RAG, research findings
- **Web UI** — Session monitoring and artifact browsing
- **Agent Library** — Sharable team configurations

## Idea Index

| Idea | Summary | Scope |
|------|---------|-------|
| [entity-model.md](ideas/entity-model.md) | Magnitude-based ideas/stances, BackgroundAgents, complex entity persistence | Vision |
| [orchestrator-event-cadence.md](ideas/orchestrator-event-cadence.md) | Per-turn convergence detection and event-driven orchestration | V2 |
| [key-takeaway-mechanism.md](ideas/key-takeaway-mechanism.md) | Convergence voting system for extracting key insights | V2 |
| [rebuttal-priority.md](ideas/rebuttal-priority.md) | Dynamic turn ordering based on conversation content | V2 |
| [moderator-input.md](ideas/moderator-input.md) | Live steering via HTTP during discussions | V2 |
| [phase-dynamics.md](ideas/phase-dynamics.md) | Per-phase personality weighting in creativity engine | V2 |
| [session-platform.md](ideas/session-platform.md) | Agent library, session-as-package, management layer | Vision |
| [research-scope-controls.md](ideas/research-scope-controls.md) | 4-layer research cost control for external data gathering | V2 |
| [agent-behavior-philosophy.md](ideas/agent-behavior-philosophy.md) | Ego simulation, behavioral prescription mechanisms | V2 |
| [implementation-gaps.md](ideas/implementation-gaps.md) | V2+ gaps identified during spec review | V2 |
| [team-configuration.md](ideas/team-configuration.md) | Multi-team YAML surface with spokesperson/deliberation | Vision |
| [mcp-message-broker.md](ideas/mcp-message-broker.md) | Cross-team communication backbone via MCP | Vision |
| [research-engine.md](ideas/research-engine.md) | External knowledge gathering during discussions | V2 |
| [agent-identity-and-resolution.md](ideas/agent-identity-and-resolution.md) | GUID-based agent identity, multi-source resolution, session snapshots | V2 |

## Open Questions (from V1 Spec Gaps Relevant to V2)

- How should phase transitions be triggered? (time-based, convergence-based, round-count?)
- How does the evaluation engine feed back into agent behavior for subsequent sessions?
- What's the boundary between moderator input and phase system auto-transitions?
- How do research engine results integrate into the context assembly pipeline?

---

# Source document: docs/v2/ideas/implementation-gaps.md

# Implementation Gaps

*Captured 2026-03-25 after spec review across all conversation-engine specs*

## Status: Ready to implement with scoped v1

The conversation engine specs are complete enough to begin implementation for single-phase conversations. These gaps should be resolved before or during implementation.

---

## Gap 1: Voting Side-Channel Prompt

**Blocking:** Yes (required for takeaway mechanism)
**Effort:** Small -- 30-minute design task, not a design question

The key-takeaway-mechanism.md spec says agents vote via separate `claude -p` calls with abbreviated context. Nobody has written the actual voting prompt: what the voter receives, the exact instruction text, and the expected output format (score + reason).

**Needs defined:**
- The system prompt for voting calls (reuse agent identity or a neutral voter prompt?)
- The user payload (takeaway statement + how many recent messages? + perspective reminder?)
- The expected output format (just "score: N, reason: text" or a structured block?)
- Whether anti-slop rules apply to voting prompts (agreement tax on high scores?)

**Ask the beta agents:** "Write the exact voting prompt that gets sent to each agent when a takeaway is proposed. What goes in the system prompt, what goes in the user payload, and what output format do you expect? Remember this is a lightweight side-channel -- keep it cheap."

---

## Gap 2: Footer Compliance Test

**Blocking:** No (can implement optimistically and fix if compliance is low)
**Effort:** Small -- automated test, ~1 hour

The context-assembly-template.md spec requires 50 synthetic `claude -p` calls to measure footer presence and field validity before writing retry logic. If baseline compliance is below 90%, the footer format needs simplifying before retry logic is built.

**Needs done:**
- Write a test script that sends 50 prompts with the Section 7 footer instruction
- Measure: footer presence rate, field validity rate per field, common malformation patterns
- If compliance < 90%: simplify footer format (fewer fields, simpler labels)
- If compliance > 95%: regex fallback may be vestigial -- note for future simplification

**Can run immediately** -- does not require agent discussion.

---

## Gap 3: Phase System

**Blocking:** No for v1 (scope v1 to single-phase conversations)
**Effort:** Large -- full design + implementation

Every spec references "phase boundaries" and "phase transitions" but the phase system (Brainstorm, Refine, Specify, Review) is not implemented in `live_conversation.py` chat mode. The orchestrator cadence spec's composite threshold triggers phase transitions, but there is no phase state machine to transition to.

**Affected features if phases are absent:**
- Phase briefings (which replace history) -- not available
- Phase-boundary synthesis (the only LLM call in the cadence) -- not available
- Tombstone lifecycle (released at phase close) -- tombstones persist for entire session instead
- Takeaway staleness clock exemptions -- no phase-reset behavior

**v1 scope decision:** Implement everything as a single continuous phase. Phase transitions, phase briefings, and phase-boundary synthesis are deferred. Tombstones persist for the full session. This is already how `live_conversation.py` works today.

**Ask the beta agents (future session):** "How should the phase state machine work in chat mode? The orchestrator cadence spec defines a composite convergence signal that should trigger phase transitions. What are the phases, what changes between them, and what does the transition sequence look like mechanically?"

---

## Gap 4: Voting / Conversation Loop Interaction

**Blocking:** No (default to blocking, optimize later)
**Effort:** Small -- design decision, not research

When an agent proposes a takeaway, the conversation pauses while all agents vote via side-channel calls. The mechanical question: does the conversation loop block during voting, or do votes happen async while the next agent speaks?

- **Blocking:** Adds ~30-60 seconds latency per proposal (5 voting calls x ~10s each). Simple to implement. Agents in subsequent turns see the resolved takeaway.
- **Async:** No latency hit but the next agent speaks without knowing a takeaway was just confirmed. Risks inconsistent shared state within a turn.

**v1 decision:** Block. Simplicity wins. 30-60 seconds per proposal at an estimated 3-5 proposals per 25-turn session = 90-300 seconds total overhead. Acceptable for overnight runs.

**Ask the beta agents (if blocking latency proves problematic):** "Should voting happen async while agents continue speaking? What happens if an agent speaks before a pending vote resolves?"

---

## Not Gaps (resolved but noting for implementers)

- **Confirmation threshold values** -- specced with starting defaults, YAML-configurable, tune from runs
- **Stagnation/convergence thresholds** -- specced with starting defaults, YAML-configurable
- **Staleness clock timeout** -- specced with default 10, YAML-configurable
- **Footer failure compliance threshold** -- specced at 15%, validate from compliance test
- **Regex pattern list** -- specced in orchestrator-event-cadence.md with full pattern lists
- **Morning Brief generation** -- specced as zero-LLM-call assembly from existing state
- **Detection hierarchy** -- fully specced as three-tier with explicit activation rules
