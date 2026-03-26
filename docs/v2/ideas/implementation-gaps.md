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
