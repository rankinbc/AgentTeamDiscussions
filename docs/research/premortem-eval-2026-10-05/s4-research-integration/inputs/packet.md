# Pre-mortem subject: How do research engine results integrate into the context assembly pipeline?

V2 plans a Research Engine that gathers external knowledge during discussions. Open question: how do its results enter the per-turn context assembly?

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

# Source document: docs/v2/ideas/research-engine.md

# Research Engine

> **V2 Concept** — Not in V1 scope. Documented here to capture intent and inform V1 design decisions.

## What It Is

The Research Engine gives agents the ability to look things up during a discussion. Instead of reasoning purely from what's in their prompt, agents can spawn research sub-tasks that verify claims, check API feasibility, survey competitive approaches, or gather domain-specific data. It's the difference between agents debating from opinion and agents debating from evidence.

## Why It Exists

V1 agents are closed-world reasoners — they can only work with what's in their context window. This is fine for brainstorming and high-level design, but falls short of the "no gaps" promise. Thorough specifications require grounding:

- "Use WebSockets for real-time updates" — but does the target platform support them?
- "Integrate with Stripe for payments" — but what does their API actually look like?
- "This approach scales to 10K users" — based on what evidence?

The Research Engine closes the gap between "plausible spec" and "grounded spec" by letting agents verify their assumptions against real information.

## How It Would Fit the System

- **Triggered by Conversation Engine**: When an agent signals `needs: more-research`, the engine can spawn a research sub-task
- **Results flow through Context Management**: Research findings become part of the situation layer for subsequent turns
- **Scoped by Session Platform**: Research has a budget (max spawns, max time) to prevent runaway costs
- **Independent of Creativity Engine**: Research agents don't need personality — they need accuracy

## Core Responsibilities (Planned)

### Research Sub-Agent Spawning
- Dedicated research agents with web search, documentation lookup, and API exploration capabilities
- Scoped queries with clear deliverables ("verify that X supports Y" not "research everything about X")
- Results formatted for context injection — concise, factual, citable

### Feasibility Verification
- Check that technical assumptions in specs are grounded
- Verify API capabilities, library support, platform constraints
- Flag specs that make unverifiable claims

### Competitive and Domain Research
- Survey existing solutions in the problem space
- Identify patterns and anti-patterns from similar systems
- Bring external context that agents can't generate from training data alone

### Budget Management
- Maximum research spawns per session
- Time limits per research task
- Cost tracking (research calls consume additional LLM invocations)

## Key Design Constraints

- Research must be scoped and budgeted — unbounded research defeats the overnight autonomy goal
- Research results must be concise enough to fit in context windows without displacing discussion history
- Research agents are utility agents, not discussion participants — they don't have opinions
- Results should be cached within a session to avoid redundant lookups

## V1 Implications

Even without a Research Engine, V1 should:
- Design Context Management to accommodate external data injection (future-proofing the situation layer)
- Include `needs: more-research` as a valid agent signal, even if nothing acts on it yet
- Structure the Session Platform to store research artifacts when they eventually exist

## Current State

Not implemented. V1 agents reason from training data and provided context only. The Research Engine is planned for V2 alongside multi-team support and the MCP Message Broker.

---

# Source document: docs/v2/ideas/research-scope-controls.md

# What controls research task scope?

*Generated: 2026-03-17 22:01 | Question 9 | 180s*

It looks like I need write permission to save the file. Could you approve the file write to `output/spec_research_scope_controls.md`?

Here's what the synthesized spec covers -- 11 sections distilled from all six panel voices across three rounds:

**Core decision: Four-layer control stack, three mechanical, one design-time.**

1. **Control Stack** -- Ordered by impact: question specificity (highest leverage), input token cap (15k), output token cap (2k), call count (2/session). No time limits, no word limits.

2. **Question Specificity** -- The real scope control. The thinking routine that triggers research must produce a single focused query. No separate validation gate (costs 12 extra calls per session). Instead: tighten the source prompt, log questions, monitor truncation rates.

3. **Input Token Cap** -- Locked at 15k, not a range. This is the hidden cost lever everyone almost missed. The orchestrator physically controls what goes into the call.

4. **Output Token Cap** -- 2k via `max_tokens` API parameter. The only constraint enforced mechanically by the API itself.

5. **Call Count Cap** -- 2 per agent per session (not per round). Per-session prevents "use it or lose it" behavior.

6. **Cost Envelope** -- ~204k tokens total research spend per session, ~3-4% of projected 6.4M budget. Only holds if all three mechanical caps hold.

7. **Failure Behavior** -- Skip and log. No retry for research (unlike save files). Truncation at 2k is logged as a quality signal.

8. **Observability** -- Six logging points including the key ROI signal: did the agent actually use the research result in the next round?

9. **Scope Exclusions** -- Research prompt template, tool access, and result integration are separate design items.

10. **Design Rationale** -- Why no gate, why 15k not higher, why per-session not per-round, why 2k is enough.

11. **Open Items** -- 11 items consolidated, 2 blocking (curator prompt versioning, thinking routine templates).

---

# Source document: docs/v1/conversation-engine/context-assembly-template.md

# Agent Context Assembly Template

*Derived from: context-assembly-spec.md, key-takeaway-mechanism.md, orchestrator-event-cadence.md, live_conversation.py*

## Invocation Pattern

Each agent turn is a single stateless `claude -p` call with two inputs:

- **System prompt** (~2K tokens, static across session): agent identity, personality traits, position, technique, anti-slop rules, conversation rules, optional project context. Built once from YAML config at session start. Not covered by this template.

- **User payload** (variable, rebuilt every turn): everything below. This template defines the assembly order, token allocation, and cut priority for the user payload.

---

## Hard Token Ceiling

**User payload ceiling: 4,000 tokens.**

Rationale: system prompt consumes ~2K tokens. The agent needs ~1-2K tokens for reasoning and response. On a 200K context window this ceiling is conservative, but the constraint is not the window -- it is attention quality. Research on LLM context utilization shows degraded attention to mid-context content beyond ~4K tokens of input. The ceiling forces the orchestrator to rank all content sources every turn rather than dumping everything in.

At steady state with 5 confirmed takeaways, 2 tombstones, and 20+ messages in history, the raw content exceeds this ceiling by ~20-30%. The cut priority (below) governs what gets dropped.

---

## Assembly Order

The user payload is assembled in the following order. Position matters: LLMs attend most strongly to content at the beginning and end of context. The most important framing goes first; the most important action directive goes last.

```
[SECTION 1] MODERATOR OVERRIDE (if present)                     ~80 tokens
[SECTION 2] ORCHESTRATOR EVENT (if triggered)                   ~150 tokens
[SECTION 3] PERSPECTIVE REMINDER + CHALLENGE STATE              ~100 tokens
[SECTION 4] CONFIRMED TAKEAWAYS + TOMBSTONES                   ~500 tokens max
[SECTION 5] THE QUESTION                                        ~60 tokens
[SECTION 6] PHASE BRIEFING (if phase transition occurred)       ~500 tokens
            OR CONVERSATION HISTORY (normal turns)              ~2200 tokens
[SECTION 7] TASK DIRECTIVE + RESPONSE FORMAT                    ~150 tokens
                                                         CEILING: 4000 tokens
```

### Why this order

- **Section 1 first:** Moderator is the human. Their input overrides everything. If present, the agent must address it before any other thread. Placing it first guarantees attention regardless of payload length.
- **Section 2 early:** Orchestrator events (disruption injection, dropped-thread callback) frame what the agent should be thinking about this turn. They go before history so the agent reads history through the lens of the event.
- **Section 3 early:** Identity reinforcement and challenge state (ego injection, challenger injection) prime the agent's behavioral mode before they encounter the conversation.
- **Section 4 before history:** Takeaways are the compressed record of what has been decided. The agent reads these before encountering the raw conversation, so they don't re-derive conclusions that are already confirmed. Tombstones prevent zombie re-proposals.
- **Section 5 as anchor:** The original question sits between the state sections and the conversation, acting as a lens for interpreting what follows.
- **Section 6 as bulk:** Conversation history is the largest section and the one most subject to compression. It sits in the mid-context zone where attention is weakest, but this is acceptable because the most important historical content has already been promoted into takeaways (Section 4) or events (Section 2).
- **Section 7 last:** The task directive and response format instruction go last, where recency bias gives them the strongest attention. This is where the agent gets told exactly what to produce.

---

## Section Details

### Section 1: Moderator Override

Present only when the moderator has spoken since this agent's last turn. Goes at the absolute top of the payload.

```
>>> MODERATOR (the human running this session) <<<
[moderator message text]
>>> YOU MUST address the moderator's point BEFORE anything else. <<<
```

Token budget: ~80 tokens. Never compressed. Never cut. If multiple moderator messages are queued, concatenate them.

### Section 2: Orchestrator Event

Present only when the orchestrator has triggered an event for this turn. Three possible event types, mutually exclusive:

**Disruption injection** (stagnation detected):
```
=== ORCHESTRATOR: STAGNATION DETECTED ===
The discussion has stalled. This thread was raised earlier but never resolved:
"[dropped thread text]"
Address this before continuing the current line of discussion.
=== END EVENT ===
```

**Dropped-thread callback** (dead-zone timeout):
```
=== ORCHESTRATOR: UNFINISHED BUSINESS ===
This point was raised but nobody followed up:
"[dropped thread text]"
Does this change anything about the current discussion?
=== END EVENT ===
```

**Dissent fetch** (contested takeaway scalar above threshold):
```
=== ORCHESTRATOR: CONTESTED DECISION ===
Takeaway [N] has a contestation score of [X]. Dissenting reasons:
- [voter reason 1]
- [voter reason 2]
Consider whether this takeaway should be challenged.
=== END EVENT ===
```

Token budget: ~150 tokens. Never compressed. Cut only if moderator override is present AND total payload exceeds ceiling (moderator always wins).

### Section 3: Perspective Reminder + Challenge State

Always present. Combines identity reinforcement with challenge/ego state.

```
[You are [Agent Name] -- [role]. Style: [cognitive_style], [emotional_baseline]. Technique: [technique]. Stay in character. Add substance or stay silent.]
```

If this agent was challenged since their last turn:
```
[CHALLENGED by [Challenger Name]. They attacked your point on [topic]. Your assertiveness is [X], your bluntness is [Y]. Respond accordingly.]
```

If this agent challenged someone else:
```
[You challenged [Target Name] on [topic]. Your stubbornness is [X]. Press your point or concede with reason.]
```

Token budget: ~100 tokens. Never compressed. Never cut.

### Section 4: Confirmed Takeaways + Tombstones

Always present once any takeaways exist. Protected content -- these are the compressed record of decisions already made. Cutting them reintroduces the re-derivation problem the mechanism exists to solve.

```
=== Confirmed Takeaways ===
[1] "[takeaway text]" (contestation: 0.2)
[2] "[takeaway text]" (contestation: 0.5)
[3] "[takeaway text]" (contestation: 0.7)

=== Rejected (tombstones) ===
[X] "[rejected takeaway text]"
    Killed by: "[killing blow text]"
=== End Takeaways ===
```

Token budget: ~50-100 tokens per takeaway, ~50 per tombstone. At 5 takeaways + 2 tombstones = ~600 tokens max.

**Scaling rule:** If takeaways exceed 600 tokens, compress low-contestation takeaways (scalar below 0.2) into a summary line: "[N] clean takeaways confirmed (details available on challenge)." Tombstones age out at phase boundaries per the Key Takeaway spec. High-contestation takeaways are never compressed.

**Staleness clock:** Each confirmed takeaway has a turn counter that increments every turn and resets to zero when any agent fires `reference_takeaway` or `challenge_takeaway` targeting it. When the counter exceeds N (YAML-configurable, default 10), the orchestrator fires the following sequence:

1. **Pulse.** The orchestrator selects the agent most likely to care about the takeaway (highest original vote score or most recent reference) and injects a one-line prompt into their next turn: "Takeaway [N] has not been referenced in [count] turns. Is it still load-bearing for the current discussion? Use `reference_takeaway: [N]` if yes."
2. **Wait one turn.** The pinged agent responds. The orchestrator reads their footer.
3. **Evaluate response.** Two outcomes:
   - Agent fires `reference_takeaway: [N]` -- staleness clock resets. Takeaway stays in active context.
   - Agent does NOT fire `reference_takeaway` in their footer -- this absence is read as a **confirmed inert signal**, not a timeout. The takeaway is no longer load-bearing in the current discussion.
4. **Compress or retain.** If confirmed inert, the takeaway is compressed to a summary line: "[takeaway text] (confirmed turn [T], no longer active)." If referenced, no action.

**Hard exemption:** Takeaways with contestation scalar above 0.5 are permanently exempt from the staleness clock. They remain in active context regardless of reference frequency, because high-contestation takeaways represent live disagreements that may resurface unpredictably.

**Cut priority: PROTECTED.** Takeaways are cut only as a last resort, after all other sections have been compressed. Cutting takeaways reintroduces re-derivation waste.

### Section 5: The Question

Always present. The original discussion topic, restated as an anchor.

```
## THE QUESTION: [question text, max 100 chars]
```

Token budget: ~60 tokens. Never compressed. Never cut.

### Section 6: Conversation History OR Phase Briefing

This section is mutually exclusive: either the agent sees conversation history (normal turns) or a phase briefing (first turn after a phase transition).

#### 6a: Conversation History (normal turns)

The largest and most compressible section. Three tiers of content:

**Tier 1 -- Recent exchanges (verbatim).** The last 7 messages in full. These are what the agent directly responds to.

```
[Recent exchanges]
[Agent Name]: [full message text]
[Agent Name]: [full message text]
...
```

Token budget: ~1400 tokens (7 messages x ~200 tokens each). Compressed to last 5 messages if ceiling is tight. Compressed to last 3 messages as final cut before touching protected sections.

**Tier 2 -- Earlier discussion (compressed).** Messages older than the recent window, compressed to first sentence only. Capped at 10 messages.

```
[Earlier discussion summary]
- [Agent Name]: [first sentence only].
- [Agent Name]: [first sentence only].
...
```

Token budget: ~300 tokens. Cut entirely before compressing Tier 1. This is the first section cut when payload exceeds ceiling.

**Tier 3 -- Moderator messages in history (never compressed).** Any moderator message in the history window is always shown verbatim, regardless of age.

```
>>> MODERATOR: [full message text] <<<
```

Token budget: variable. Never compressed. Never cut.

#### 6b: Phase Briefing (first turn of new phase)

**Replaces all conversation history.** The phase briefing is the model synthesis output from the previous phase, promoted as the sole historical context for the new phase.

```
=== PHASE BRIEFING: Entering [Phase Name] ===
Previous phase concluded with:

Positions held:
- [position summary]

Concessions made:
- [concession summary]

Unresolved threads:
- [thread summary]

Your task in this phase: [phase-specific directive]
=== END BRIEFING ===
```

Token budget: ~500 tokens. This is the bounded synthesis output from the orchestrator-event-cadence spec (reads running summaries only, not raw history).

**Conflict note:** The context-assembly brief asks "does the phase briefing replace or sit alongside history?" The orchestrator-event-cadence spec says synthesis reads summaries only, not raw history. Resolution: **phase briefings replace history entirely.** The briefing IS the history for the new phase. Agents in phase two have no access to phase one's raw messages -- only the promoted summary. This is the correct behavior: phase boundaries are compression events, and carrying raw history across phases defeats the purpose.

### Section 7: Task Directive + Response Format

Always present. Goes last for recency bias. Contains the action instruction and the structured output format.

```
=== YOUR TURN ===
Respond to the discussion since your last message. Stay on the question.
If the discussion has drifted, pull it back. Keep it to 2-4 sentences.

After your response, add this footer on a new line:
---signals---
changed: [one sentence: what shifted in the discussion this turn]
stance: [agreeing | challenging | extending | proposing | synthesizing | pivoting | questioning]
confidence: [0.0 to 1.0]
ready_to_advance: [true | false]
key_claim: [your single most important point this turn, one sentence]
propose_takeaway: [null | "proposed takeaway text if you believe the group has converged on something"]
challenge_takeaway: [null | takeaway number if you want to reopen a confirmed takeaway because you believe it is wrong or incomplete]
reference_takeaway: [null | takeaway number if removing that takeaway would invalidate the point you just made -- use this when your argument depends on a confirmed decision holding true]
=== END ===
```

**Footer reliability policy:**

The footer fields are split into two blocks with different failure policies, borrowing the aviation challenge-response / do-verify distinction:

*Do-verify fields* (`stance`, `changed`, `confidence`, `ready_to_advance`, `key_claim`): **skip on parse failure.** The orchestrator loses signal resolution but session state remains valid. These fields feed counters and instrumentation -- missing one degrades quality signals but does not corrupt shared state. Default values on failure: stance=null, changed=null, confidence=0.5, ready_to_advance=false, key_claim=null.

*Challenge-response fields* (`propose_takeaway`, `challenge_takeaway`, `reference_takeaway`): **hard retry on parse failure, no inference fallback.** These are state mutation events -- a missed proposal means a group decision was never logged, a missed challenge means a live disagreement was silently dropped. Both corrupt shared state permanently.

*Terminal failure condition* (if hard retry also fails): flag to the Morning Brief as an unlogged decision event. The session continues -- halting breaks overnight operation. The flag reads: "Agent [name] produced an unparseable response at turn [N]. A takeaway proposal or challenge may have been lost. Review the raw transcript for this turn."

Never halt the session. Never drop silently. Never infer what the agent meant.

*Token cost note:* each hard retry is a full ~4K context reassembly. At an estimated 1-2 retries per 25-turn session (based on typical LLM instruction compliance rates), this adds ~4-8K tokens to session cost. Price this into budget math.

*Open prerequisite:* run a compliance test (50 synthetic `claude -p` calls with the footer instruction, measure footer presence and field validity rates) before writing retry logic. If baseline compliance is below 90%, simplify the footer format first -- retry logic built on a broken format just fails faster.

**Footer field triggers:**

- `propose_takeaway`: Use when you sense genuine convergence -- multiple agents have agreed on a point across several turns and formalizing it would free the discussion to move on. Do not propose takeaways on points that are still being actively debated.
- `challenge_takeaway`: Use when you believe a confirmed takeaway is wrong, incomplete, or no longer valid given what has been discussed since it was confirmed. This triggers the voting mechanism to re-evaluate the takeaway.
- `reference_takeaway`: Use when your current argument depends on a confirmed takeaway remaining true -- i.e., if that takeaway were removed, your point would collapse. This resets the staleness clock on the referenced takeaway, signaling to the orchestrator that the decision is still load-bearing in the current discussion. Matched by integer equality against the takeaway registry only.

Token budget: ~150 tokens. Never compressed. Never cut.

---

## Cut Priority (what gets dropped when payload exceeds 4,000 tokens)

Tiers are cut in order. The orchestrator drops from Tier 1 first and works down. Protected sections are never cut.

| Priority | Section | Action When Tight |
|----------|---------|-------------------|
| **Cut first** | Tier 2 history (earlier discussion compressed) | Drop entirely. Agents still have recent exchanges + takeaways. |
| **Cut second** | Tier 1 history (recent exchanges verbatim) | Reduce from 7 to 5, then to 3. Below 3, the agent has insufficient context to respond meaningfully. |
| **Cut third** | Orchestrator event (Section 2) | Drop if moderator override is present. Otherwise protected. |
| **Cut fourth** | Takeaway scaling rule | Compress low-contestation takeaways to summary line. |
| **PROTECTED** | Moderator override (Section 1) | Never cut. |
| **PROTECTED** | Perspective reminder (Section 3) | Never cut. |
| **PROTECTED** | Confirmed takeaways with contestation > 0.2 | Never cut. |
| **PROTECTED** | The question (Section 5) | Never cut. |
| **PROTECTED** | Task directive + response format (Section 7) | Never cut. |

**Justification:** History is the most compressible because its most important conclusions have already been promoted into takeaways. Cutting compressed older messages costs almost nothing -- the agent still has recent exchanges and the takeaway block. Cutting recent exchanges below 3 is the hard floor: the agent needs to see what was just said to respond relevantly. Protected sections are structural (identity, decisions, task format) -- removing them breaks the mechanism, not just the quality.

---

## Conflict Log

| Conflict | Resolution |
|----------|-----------|
| The context-assembly brief lists the current task instruction as "2-3 sentences, one point." The updated CONVERSATION_SYSTEM says "2-4 sentences." The per-turn task instruction at line 1948 of live_conversation.py still says "2-3 sentences, one point." | **Use "2-4 sentences" consistently.** The CONVERSATION_SYSTEM was intentionally updated; the per-turn instruction is stale and should be updated to match. |
| The context-assembly brief asks whether phase briefings replace or sit alongside history. The orchestrator-event-cadence spec says synthesis reads summaries only. | **Phase briefings replace history entirely.** See Section 6b rationale. |
| The key-takeaway-mechanism spec says dissent text is fetched on-demand via lazy loading. The context-assembly brief lists it as a separate context source. | **Dissent text is an orchestrator event (Section 2), not a standing section.** It appears only when the orchestrator triggers a dissent fetch based on contestation scalar threshold. This is consistent with both specs. |
| The key-takeaway-mechanism spec defers per-turn magnitude re-evaluation. The context-assembly brief's structured output format includes no magnitude field. | **No conflict.** Magnitude re-evaluation is deferred. The structured footer includes `challenge_takeaway` as the behavioral signal instead of a self-reported score, consistent with the finding that LLMs cannot reliably introspect on conviction. |

---

## Relationship to Existing Specs

- **key-takeaway-mechanism.md** -- Section 4 (Takeaways + Tombstones) implements the "Shared State: What Agents See Each Turn" block defined in that spec. The `propose_takeaway` and `challenge_takeaway` fields in the response footer implement the proposal and challenge triggers. The cut priority protects takeaways as specified.

- **orchestrator-event-cadence.md** -- Section 2 (Orchestrator Event) implements the disruption injection and dropped-thread callback mechanisms. The per-turn pattern-match capture operates on the agent's raw response after it is received, consuming the `---signals---` footer. The concession log reads the `stance` and `changed` fields. The position tracker reads `key_claim` and `stance`.

- **turn-anatomy.md** -- This template supersedes the implicit assembly order in live_conversation.py. The three-layer context model (Identity, Situation, Task) maps to: Identity = system prompt (not in this template), Situation = Sections 1-6, Task = Section 7.

- **agent-behavior-mechanisms.md** -- The `propose_takeaway` field replaces the need for agents to embed takeaway proposals in prose. The `challenge_takeaway` field provides a structured challenge trigger that the orchestrator can act on without parsing natural language.
