# Pre-mortem subject: What's the boundary between moderator input and phase system auto-transitions?

V2 plans both live moderator steering via HTTP and automatic phase transitions. Open question: where is the boundary between the two, and who wins when they conflict?

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

# Source document: docs/v2/ideas/moderator-input.md

# Moderator Input (Live Steering)

*Implementation spec for injecting human direction into live conversations*

## Problem

Once `live_conversation.py` starts, there's no way to influence the discussion. If agents go off-topic, circle endlessly, or miss an important angle, you just watch. The only option is Ctrl+C and restart with a different question.

## Goal

Add a text input to the web UI that lets the user inject messages into the conversation as a "Moderator" -- a participant with special authority. Agents see the moderator's message in their context and respond to it like any other message, but the moderator's input carries weight because the system prompt tells agents to treat moderator messages as priority directives.

## Design

### How It Works

1. User types a message in the input box at the bottom of the UI
2. Browser POSTs the message to `/moderator`
3. Server injects the message into the conversation history as a moderator entry
4. Next agent to speak sees it in their context and responds to it
5. The message appears in the chat UI with a distinct "MODERATOR" style

### Message Injection

The moderator message is added to the `history` list like any agent message, but with a special marker:

```python
history.append({
    "agent": "__moderator__",
    "name": "MODERATOR",
    "text": message,
    "turn": current_turn,
})
```

Agents see it in their context as:
```
[MODERATOR]: Consider the privacy implications of this approach.
```

### System Prompt Addition

Add to `CONVERSATION_SYSTEM`:
```
- If the MODERATOR speaks, treat their message as a priority. Address their point before continuing
  other threads. The moderator is the person who submitted this topic -- they're steering the
  discussion toward what matters to them.
```

### UI Changes

Add an input bar below the turn counter:

```html
<div class="moderator-bar">
    <input type="text" id="mod-input" placeholder="Steer the conversation..." />
    <button onclick="sendModMessage()">Send</button>
</div>
```

Styling: subtle, not dominant. Dark input field matching the existing aesthetic. The input should be clearly available but not visually competing with the conversation.

Moderator messages in the chat use a distinct style:
```css
.msg.moderator {
    border-left-color: var(--amber);
    background: rgba(245, 166, 35, 0.06);
}
.msg.moderator .m-name { color: var(--amber); }
```

### Server Endpoint

```python
def do_POST(self):
    if self.path == "/moderator":
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode()
        data = json.loads(body)
        message = data.get("message", "").strip()
        if message:
            # Add to shared queue that the conversation loop checks
            moderator_queue.append(message)
            emit("system_message", {"message": f"Moderator: {message}"})
            # Also emit as a proper message for the chat
            emit("moderator_message", {"text": message})
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"ok":true}')
```

### Conversation Loop Integration

```python
# Shared state between HTTP server thread and conversation loop
moderator_queue = []

# In run_conversation(), after each agent speaks and before next agent:
while moderator_queue:
    mod_msg = moderator_queue.pop(0)
    history.append({
        "agent": "__moderator__",
        "name": "MODERATOR",
        "text": mod_msg,
        "turn": turn,
    })
```

Threading note: `moderator_queue` is a plain list accessed from two threads. In CPython, list.append and list.pop(0) are effectively atomic due to the GIL. For safety, wrap in the existing `_event_lock` or use `collections.deque` (which has thread-safe append/popleft).

### Context Handling

Moderator messages are treated like any other message in the context window:
- Recent (last 5): shown verbatim
- Older: compressed to first sentence like agent messages

No special treatment in context compression. The moderator's authority comes from the system prompt instruction, not from persistence tricks.

### What This Changes

- `live_conversation.py`:
  - Add `moderator_queue` (thread-safe deque)
  - Add `do_POST` handler to `ConvHandler`
  - Add moderator input bar to HTML
  - Add `moderator_message` SSE event type
  - Add moderator CSS styles
  - Update `CONVERSATION_SYSTEM` with moderator instruction
  - Check queue between agent turns

### What This Doesn't Change

- Agent system prompts (personality, voice)
- Speaking order computation
- Context compression logic (moderator messages compress like any other)
- Convergence detection (moderator messages don't count as agreement signals)
- Transcript saving (moderator messages saved with `MODERATOR` attribution)

## Edge Cases

- **Message while no agents are speaking**: Queued and picked up before the next agent's turn.
- **Multiple messages queued**: All injected in order before the next agent speaks.
- **Empty message**: Ignored (whitespace check).
- **Very long message**: No explicit limit, but it enters the context window like any other message. If it's too long it'll compress to first sentence in older history.
- **Message after conversation ends**: Ignored (conversation loop has exited).

## What the Moderator Should NOT Be

- NOT a way to give agents private instructions (all agents see it)
- NOT a voting mechanism
- NOT a way to force conclusions (agents can disagree with the moderator)
- NOT displayed differently in transcripts (it's part of the conversation record)

## Success Criteria

1. User can type a message and see it appear in the chat immediately
2. The next agent to speak addresses the moderator's point
3. Moderator messages are preserved in the saved transcript
4. The input doesn't interfere with the conversation flow (no pausing, no blocking)
5. Multiple moderator messages can be queued without issues

---

# Source document: docs/v2/ideas/phase-dynamics.md

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
