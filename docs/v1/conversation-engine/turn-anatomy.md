# What Is a Turn

*Generated: 2026-03-17 10:04 | Spec ID: 01*

I've drafted the synthesized spec. Let me present it here since I'm having trouble writing to the output directory. Here's the complete requirements spec:

---

# Requirements Spec: The Turn

**Status:** Draft  
**Source:** Synthesized from three design proposals (Cognitive Architect, Systems Pragmatist, Product Oracle)  
**Date:** 2026-03-17

---

## 1. Definition

A **turn** is the atomic unit of conversation in the system. It is one agent producing one response given a curated context. Every turn has exactly one author, belongs to exactly one team, and targets either that team (internal deliberation) or the opposing team (cross-team exchange).

---

## 2. Turn Types

The system has two distinct turn types. They differ in audience, purpose, and expected behavior.

### 2.1 Internal Deliberation Turn

- **Audience:** Teammates only. Never visible to the opposing team.
- **Purpose:** Stress-test the team's position, surface uncertainty, strategize, assign roles.
- **Expected behavior:** Candid, exploratory, allowed to be wrong. Agents should admit uncertainty, challenge teammates directly, and request help.
- **Token budget:** Shorter than cross-team turns. These are working memory, not output.
- **Addressing:** Each deliberation turn should indicate which teammate (if any) it is responding to, preventing "speaking to the room" monologues.

### 2.2 Cross-Team Turn

- **Audience:** The opposing team (routed through the MCP server).
- **Purpose:** Advance the conversation -- propose, challenge, synthesize, or decide.
- **Expected behavior:** Considered and clear. Represents team consensus. Should acknowledge the other team's points before countering. Must move the conversation forward, not just react.
- **Token budget:** Longer, more polished. This is the product the user reads.

### 2.3 Turn Cycle

The fundamental rhythm is:

1. Team A sends a cross-team message.
2. Team B receives it.
3. Team B deliberates internally (N turns, budget-limited).
4. Team B sends one cross-team response.
5. Reverse.

The cross-team response represents the output of deliberation, not one agent's unfiltered reaction.

---

## 3. Turn Context

Every turn is constructed by the orchestrator from three layers. The order matters -- identity frames interpretation of situation, which frames the task.

### 3.1 Identity Layer (who am I)

Provided every turn. Contains:

- **Persona:** Role name, expertise domain, and perspective.
- **Bias statement:** What this agent prioritizes over other concerns. Written as instincts and values, not behavioral rules. Example: *"You instinctively distrust solutions that require coordination between more than three teams. You've been burned by 'elegant' designs that nobody could debug at 2am."* Not: *"You are a senior architect. Always consider scalability."*
- **Team goal:** 1-2 sentences on what the team is collectively trying to achieve.
- **Differentiation:** What this agent brings that others on the team do not.

### 3.2 Situation Layer (where are we)

Provided every turn. Contains:

- **Current phase:** Name and objective (e.g., "Brainstorm -- generate at least 5 distinct approaches").
- **Conversation summary:** Orchestrator-generated compression of key points, open tensions, and decisions made. Not the raw transcript. Target: 3-5 key points.
- **Recent messages:** The last 2-3 full messages relevant to this turn (cross-team messages for cross-team turns; team-internal messages for deliberation turns).
- **Artifacts:** List of any produced artifacts with their current status (draft, revised, approved).
- **Open questions:** Explicitly listed unresolved tensions or pending decisions.

**Context curation rule:** The orchestrator must act as editor, not pipe. Agents should never receive the full raw transcript. Recent messages appear in full; older exchanges are compressed into the summary. The goal: enough context to respond to a specific claim, not so much that the agent writes a book report.

### 3.3 Task Layer (what am I being asked right now)

Provided every turn. Contains:

- **Instruction:** A specific ask. Must end with a concrete question or directive. Never "continue the discussion." Examples: *"The other team claims X relies on assumption Y. Defend or dismantle that assumption."* or *"Synthesize proposals A and B into a single approach."*
- **Constraints:** Expected length, format requirements, focus area.
- **Turn type indicator:** Whether this is an internal deliberation turn or a cross-team turn.

**Forcing function:** Every turn prompt must contain something the agent has to react to. Agents asked to "discuss" will summarize. Agents asked to "defend or attack a specific claim" will think.

### 3.4 What Agents Must NOT See

- The opposing team's internal deliberation (architectural boundary).
- Raw orchestrator state: turn counters, phase transition thresholds, budget remaining.
- The exact total turn budget or countdown (see Section 6).
- Orchestrator decision logic.

---

## 4. Turn Output

Every turn produces two components: content and signals.

### 4.1 Content

Natural language. No structural constraints on format. This is where the thinking happens. This is what other agents read and respond to.

### 4.2 Signals

Lightweight metadata attached to every turn. The orchestrator reads signals to make routing and phase-transition decisions. Other agents do not see signals -- they read only the content.

**Required signals:**

| Signal | Values | Purpose |
|---|---|---|
| `stance` | agreeing, challenging, extending, proposing, synthesizing, pivoting, questioning | Enables convergence detection and drift analysis |
| `confidence` | 0.0 - 1.0 | Flags hand-waving vs. commitment; low-confidence agents are worth probing |
| `ready_to_advance` | true / false | Explicit phase-transition vote |
| `key_claim` | One sentence | Forces the agent to know its own point |

**Optional signals:**

| Signal | Values | Purpose |
|---|---|---|
| `needs` | more-research, team-input, counter-argument, evidence | Tells orchestrator what to serve next |
| `artifact_action` | none, draft, revise, approve, reject | Triggers artifact workflows |
| `topics` | List of topic tags | Enables topic-level tracking |
| `directed_at` | Agent ID (deliberation turns only) | Prevents "speaking to the room" |

### 4.3 Signal Integrity Rules

- **Missing signals default gracefully.** If an agent omits signals, the orchestrator infers what it can from content or uses safe defaults. Never retry a turn for missing signals.
- **Inconsistency is diagnostic, not error.** If an agent signals `stance: agreeing` but the content clearly disagrees, log the inconsistency as a prompt quality signal. Do not validate signals against content at runtime.
- **Signals are hints, not gospel.** The orchestrator should weight actual content over signals when they conflict.

---

## 5. Perspective Reminder

The mechanism that prevents agent drift -- the convergence toward generic, agreeable responses that makes every agent sound identical by turn 8.

### 5.1 Structure

Three components, injected at the system level (not as a user message the agent feels compelled to respond to):

**Anchor (static, always present):** 2-3 sentences capturing the agent's identity as values and instincts. Unchanged across the conversation. Must stay under 50 words.

**Phase focus (semi-static, changes per phase):** What this agent's role specifically demands in the current phase. E.g., *"We're in REFINE. Your job: challenge any assumption that hasn't been validated."*

**Drift correction (dynamic, injected conditionally):** A nudge when the orchestrator detects the agent is acting out of character. E.g., *"In your last 2 turns you agreed with everything. That's not your role. Find something to push back on, or explicitly state why you're genuinely convinced."*

### 5.2 Injection Rules

- The anchor and phase focus appear on **every turn**. Non-negotiable.
- The drift correction appears **only when triggered** by the orchestrator's behavioral analysis.
- Total perspective reminder must stay **under 150 words**. Longer reminders get ignored and eat context window.
- At **phase transitions**, the phase focus resets and the anchor is re-emphasized.

### 5.3 Drift Detection Triggers

The orchestrator should inject a drift correction when:

- An agent whose role is adversarial (skeptic, QA, critic) has signaled `agreeing` or `extending` for 3+ consecutive turns.
- An agent has not introduced a new `key_claim` distinct from previous turns in 3+ turns.
- The conversation has been circular for 2+ exchanges (same topics recycling without new substance).
- A phase transition just occurred (prophylactic re-anchoring).

### 5.4 Anti-Filler Directive

Every perspective reminder must include an explicit permission to be brief: *"Add substance or stay silent. If you agree with what's been said and have nothing to add, say so in one line and yield."* This is the single most effective forcing function against filler.

---

## 6. Positional Awareness

Agents need a compass, not a clock. The system provides arc position, never raw turn counts.

### 6.1 What Agents Receive

- **Phase name and objective:** Always.
- **Phase progress:** One of: early, midway, late, wrapping-up. Computed by orchestrator from elapsed turns relative to phase budget and convergence signals.
- **Momentum indicator:** One of: diverging, exploring, converging, stuck. Computed from recent signal patterns:
  - Predominantly `extending` + `synthesizing` = converging
  - Predominantly `pivoting` = diverging
  - Repeated `needs` with no resolution = stuck
  - Mix of `challenging` and `extending` = exploring (healthy)

### 6.2 What Agents Must NOT Receive

- Exact turn count or exact turns remaining.
- Countdown indicators (e.g., "3 turns left").
- The total turn budget for any phase.
- Orchestrator transition thresholds.

**Rationale:** Countdown awareness causes premature convergence. Agents with visible limits optimize for completion over quality -- they summarize, agree, and wrap up early. The orchestrator manages pacing invisibly. Agents should experience an open-ended conversation with structure, not a timed exam.

### 6.3 Phase-Progress-to-Behavior Mapping

| Progress | Expected agent behavior |
|---|---|
| Early | Generate options, explore widely, avoid premature convergence |
| Midway | Develop promising directions, begin comparing tradeoffs |
| Late | Converge, synthesize, identify remaining gaps |
| Wrapping-up | Finalize positions, resolve last disagreements, prepare artifacts |

---

## 7. Deliberation Budget

The number of internal turns a team takes before producing a cross-team response.

### 7.1 Defaults by Phase

| Phase | Budget | Rationale |
|---|---|---|
| Brainstorm | 1-2 | Move fast, generate volume, don't overthink |
| Refine | 2-3 | Worth debating priorities and tradeoffs |
| Specify | 3-4 | Details matter, get them right |
| Review | 2-3 | Focused critique, not open-ended exploration |

### 7.2 Budget Rules

- The orchestrator may terminate deliberation early if all team agents signal `ready_to_advance` and stances have stabilized.
- The orchestrator may extend deliberation by 1 turn if confidence scores are low across the team and positions are still shifting.
- Instrument and measure: track how often the team's cross-team position meaningfully changes between the second-to-last and last deliberation turn. If the answer is "rarely," the budget for that phase is too high.

---

## 8. Conditions for a Productive Turn

A turn is productive when all five of these conditions hold:

1. **The agent has a specific job** -- a concrete question to answer or claim to evaluate, not "respond to the conversation."
2. **The context is curated** -- the orchestrator compressed and selected, rather than dumping the full transcript.
3. **The agent is in character** -- the perspective reminder is active and drift correction has fired if needed.
4. **There is creative tension** -- the agent knows what the other side thinks AND has reason to engage with it critically.
5. **There is a clear output expectation** -- what form the response should take and what signals should accompany it.

### 8.1 Known Filler Patterns and Mitigations

| Filler pattern | Cause | Mitigation |
|---|---|---|
| "Great points! I agree that..." | No specific ask in the prompt | Every turn prompt ends with a concrete question |
| Restating what was already said | Too much raw transcript in context | Compress history into summary, not transcript |
| Surface-level response to everything | No focus constraint | Task layer specifies one thread to go deep on |
| Generic helpful voice | Identity drift | Bias-based anchor + drift correction nudges |
| Premature wrap-up | Countdown awareness | Hide turn budgets; use arc position only |
| Circular rehashing | Stale conversation | Orchestrator injects provocations or new constraints when stuck |
| Performative agreement | No permission to be brief | Anti-filler directive: "say so in one line and yield" |

---

## 9. Open Design Questions

These were surfaced across proposals but not fully resolved:

1. **Who speaks for the team?** After internal deliberation, does one designated agent produce the cross-team response, or does the orchestrator synthesize from all deliberation turns? The proposals assume a single speaker but don't specify selection logic.

2. **Summary generation:** The orchestrator must produce compressed conversation summaries for the situation layer. Should this be a separate LLM call, a deterministic extraction from signals, or the responsibility of a dedicated "note-taker" agent?

3. **Deliberation structure:** Should internal deliberation be free-form (any agent can respond to any agent) or structured (round-robin, designated facilitator)? Free-form is more natural but risks dominant-agent effects.

4. **Turn token budgets:** Specific token limits for internal vs. cross-team turns are not specified. These need empirical tuning but initial targets should be set.

5. **Drift correction authoring:** The drift correction nudges require the orchestrator to analyze recent behavior and generate targeted prompts. How sophisticated does this analysis need to be? Simple signal-pattern matching, or a dedicated LLM classification step?

6. **First turn bootstrapping:** The first turn of a conversation has no history, no summary, no signals to reference. What does the task layer contain for turn 1? How does the orchestrator seed productive divergence from the start?

---

The file write needs permission -- once granted I'll save it to `output/spec_turn_anatomy.md`. Want me to try again, or is the inline version above sufficient?