# Design Decisions to Keep

Synthesized from beta agent panel output across all rounds. These are the ideas
worth carrying forward into the real design specs.

---

## The Turn

### Three-layer context model

Every turn is constructed from three layers, in order:

1. **Identity** (who am I) -- persona, bias statement, team goal, differentiation. Static across the conversation.
2. **Situation** (where are we) -- current phase, conversation summary, recent messages, artifacts, open questions. Curated per-turn by the orchestrator.
3. **Task** (what am I being asked right now) -- a specific ask ending in a concrete question or directive, constraints, turn type indicator.

The ordering matters. Identity frames interpretation of situation, which frames the task.

### Bias statements as instincts, not rules

Personality traits should be written as lived experience and values, not behavioral directives. Write: *"You instinctively distrust solutions that require coordination between more than three teams. You've been burned by 'elegant' designs that nobody could debug at 2am."* Not: *"You are a senior architect. Always consider scalability."*

### Forcing function on every turn

Every turn prompt must end with a concrete question or directive. Never "continue the discussion." Agents asked to "discuss" will summarize. Agents asked to "defend or attack a specific claim" will think. This is the single biggest anti-filler mechanism.

### Signals alongside content

Agents produce natural language prose plus lightweight metadata signals. Signals are for the orchestrator only -- other agents see only the prose.

Required signals:
- **stance** -- agreeing, challenging, extending, proposing, synthesizing, pivoting, questioning
- **confidence** -- 0.0 to 1.0
- **ready_to_advance** -- true/false phase transition vote
- **key_claim** -- one sentence forcing the agent to know its own point

Optional signals:
- **needs** -- more-research, team-input, counter-argument, evidence
- **topics** -- list of topic tags
- **directed_at** -- agent ID for deliberation turns

Signal integrity rules:
- Missing signals default gracefully. Never retry a turn for missing signals.
- Inconsistency is diagnostic, not error. If stance says "agreeing" but content disagrees, log it.
- Signals are hints, not gospel. Weight actual content over signals when they conflict.

### Orchestrator as editor, not pipe

Agents never see the raw transcript. The orchestrator curates context: recent messages appear in full, older exchanges are compressed into a 3-5 point summary. The goal is enough context to respond to a specific claim, not so much that the agent writes a book report.

### Arc position, not countdown

Agents receive phase progress as qualitative arc position:
- **Progress:** early, midway, late, wrapping-up
- **Momentum:** diverging, exploring, converging, stuck

Agents never see raw turn counts, turns remaining, total budget, or transition thresholds. Countdown awareness causes premature convergence -- agents with visible limits optimize for completion over quality.

### Two turn types

1. **Internal deliberation** -- audience is teammates only, never visible to opposing team. Candid, exploratory, allowed to be wrong. Shorter token budget. Working memory.
2. **Cross-team** -- audience is the opposing team via MCP. Considered, clear, represents team consensus. Longer token budget. This is what the user reads.

### Turn cycle rhythm

1. Team A sends a cross-team message
2. Team B receives it
3. Team B deliberates internally (N turns, budget-limited)
4. Team B sends one cross-team response
5. Reverse

The cross-team response represents the output of deliberation, not one agent's unfiltered reaction.

### Deliberation budgets by phase

| Phase | Internal turns before cross-team response | Rationale |
|---|---|---|
| Brainstorm | 1-2 | Move fast, generate volume, don't overthink |
| Refine | 2-3 | Worth debating priorities and tradeoffs |
| Specify | 3-4 | Details matter, get them right |
| Review | 2-3 | Focused critique, not open-ended exploration |

Budget can be terminated early if all agents signal ready_to_advance and stances have stabilized. Extended by 1 if confidence is low across the team.

### Drift correction as conditional injection

Not every turn. Only injected when the orchestrator detects:
- An adversarial agent has signaled "agreeing" or "extending" for 3+ consecutive turns
- An agent has not introduced a new key_claim in 3+ turns
- Conversation has been circular for 2+ exchanges
- A phase transition just occurred (prophylactic re-anchoring)

Format: short, direct, under 150 words total for the full perspective reminder.

### What agents must NOT see

- The opposing team's internal deliberation
- Raw orchestrator state (turn counters, thresholds, budget remaining)
- Orchestrator decision logic
- Each other's signal metadata

---

## Phase Transitions

### Phase Transition Document (PTD)

At phase boundaries, a Phase Transition Document replaces the raw transcript in context. This is a context refresh, not context loss. The PTD carries forward key decisions, open tensions, and artifact status.

### Two transition mechanisms

- **Sub-cycles** for non-foundational gaps within a phase. The system loops back on a specific topic without resetting the whole phase.
- **Full regression** for foundational problems (Specify reveals a fundamental assumption was wrong). Maximum one regression per session, with halved deliberation budget.

### Two-tier phase evaluation

- **Tier 1:** Agent turn signals (stance distribution, ready_to_advance votes, topic coverage) feed cheap heuristic checks. Runs every turn.
- **Tier 2:** A lightweight LLM evaluator fires only when Tier 1 signals are ambiguous. Not every turn -- only at evaluation checkpoints.

---

## Anti-Slop

### Two-layer model: prompt vs orchestrator

- **Layer 1 (prompt-only, zero runtime cost):** Agreement Tax, Perspective Enforcement, Specificity Mandate, STRETCH Protocol. These live entirely in the agent's system prompt.
- **Layer 2 (orchestrator logic):** Convergence Suppression for MVP. Checks signal patterns, intervenes when needed.

### One intervention per turn maximum

Never stack multiple anti-slop interventions. If multiple mechanisms want to fire, use priority order: phase check > convergence > STRETCH > stance diversity.

### Escalation, not stacking

If a nudge doesn't work, the next trigger escalates rather than adding a second nudge:
1. Nudge -- gentle redirection in the task layer
2. Directive -- explicit instruction to change behavior
3. Constraint -- hard requirement on the next turn's output

### Consensus drift is Convergence Suppression

Not a separate mechanism. Same signals, same detection, same intervention. Don't duplicate.

---

## AgentMind

### Kill idea magnitude

Numeric conviction scores are fake precision that makes output worse. Let conviction emerge naturally from the conversation -- how hard an agent argues for something IS the magnitude.

### Kill mood tracking as a variable

Replace with interaction pattern detection. *"Your last two proposals were challenged on feasibility"* beats *"You're feeling frustrated."* Track what happened, not how the agent "feels."

### Agents don't see their own tracked state

Orchestrator-only. Showing agents their state causes anchoring ("my confidence is 0.8 so I should act confident") and meta-commentary waste.

### No cross-session agent memory

User references prior session artifacts in new session config. Continuity is explicit and user-controlled, not magical persistence.

### AgentMind is V1.5, not V1

Ship without explicit AgentMind tracking. Use stance signal patterns from the Turn spec as a proxy for internal state. Add a position ledger (claims, reversal count, unresolved objections) after real transcripts prove the need exists.

---

## Cross-Team Communication

### Spokesperson model

After internal deliberation, one agent synthesizes the team's position into a cross-team message. Raw internal debate never crosses the boundary. The other team sees a composed position, not a transcript of the argument that produced it.

### Sender-pays compression

The sending team is responsible for making their message consumable. The receiving team should not have to wade through verbose output to find the point.

### Contested decisions surfaced explicitly

When teams disagree and neither budges, the artifact says so. *"Teams disagreed on X. Team A argued [position]. Team B argued [position]. This spec follows Team A's approach."* Mushy compromise is worse than transparent disagreement.

---

## User Input

### "Sparks" field

The user's half-formed "what ifs" and shower thoughts. These go into the session seed unprocessed because they capture what made the user excited about the idea -- which an expansion step can never infer.

The sweet spot for a 10 PM submission: idea + 1-2 sparks + 1-2 constraints. Sixty seconds of typing.

### Minimum viable input is one sentence

Brainstorm phase is designed to be divergent. Vague input is a feature in divergent thinking, not a bug. The expansion step fills in obvious implications. Agent system prompts provide differentiation. Detailed input becomes valuable in later phases.

---

## Bench System

### Bench as strategic advantage, not just cost savings

Benched agents aren't idle -- they can do background research while the active agents deliberate. The architect gets benched during UX discussion, so redirect them to research technical feasibility of what the active agents are converging on. They return with something the group didn't have. Turns dead time into prep work.

### Mandatory recall for decision ratification

Before any decision gets locked in, all agents (including benched ones) get a brief window to object or endorse. Prevents the failure mode where someone gets benched right before a bad decision they would have caught.

### Three benching triggers

1. **Phase mismatch** (deterministic) -- pre-configured per phase in the phase definition. QA is benched during brainstorm, architect is benched during branding discussion.
2. **Diminishing signal** (heuristic) -- nobody built on the agent's last 2 contributions. They're adding noise not signal.
3. **Budget pressure** (structural) -- token budget running low, keep the top N contributors and bench the rest.

### Four recall triggers

1. **Phase transition** -- resets the full roster. Everyone starts active, re-evaluate from scratch.
2. **Topic shift** -- conversation drifts into a benched agent's domain. Orchestrator matches topic against benched agents' competency tags.
3. **Explicit request** -- an active agent flags a need that maps to a benched teammate. Mirrors how real teams work.
4. **Deadlock breaking** -- conversation going circular, pull in a benched agent for fresh perspective. The bench becomes a strategic reserve.

### Ghost influence

A benched agent's opinion from earlier turns may still be shaping the conversation, but they're not there to defend or refine it. Benching doesn't retract anything they said, but the system should track when influential agents leave so the context is clear.

### Dugout not penalty box

Benched agents shouldn't "know" they're benched in a way that changes behavior on return. When recalled, they get a catch-up summary of what they missed and jump back in at full capability. The bench is about keeping the conversation sharp, not punishing low performers.

### Phase-based benching is the 80/20

Build phase-based benching first. Heuristic signal-quality detection (redundancy, engagement tracking) is expensive and fragile -- add it only after real transcripts show actual noise problems.

### Quiet mode as alternative to full bench

Agent still observes (receives messages) but doesn't produce output. Cheaper than participation but preserves context buildup for when they're needed. Middle ground between active and fully benched.

### Hard rules

- **Min active agents: 2.** Never bench below this. Prevents one agent talking to themselves.
- **Bench cooldown: 1 turn.** Can't re-bench an agent the same turn they return. Prevents thrashing.

---

## Research-Backed Additions

*Sourced from "Engineering Robust Multi-Agent LLM Discussions" research review.*

### Goal-based tension (CrewAI role-goal-backstory triple)

Each agent needs a singular *goal* that naturally conflicts with other agents' goals. We have "drives" (multiple motivations) but not one clear objective that creates tension. The Cognitive Architect's goal might be "design systems that remain coherent and evolvable at scale" while the Systems Pragmatist's is "identify the simplest implementation that ships on time." The tension is structural, not instructed -- you don't tell them to disagree, their goals make agreement require genuine justification.

### Round 1 in parallel with no shared context

The opening round of any phase should have agents generate independently before seeing each other's output. Prevents anchoring on the first response. Research shows this forces genuinely independent reasoning and produces more diverse starting positions. After Round 1, agents see each other's work and the cross-referencing begins.

### Negative constraints need positive redirects

Our `operating_level: requirements` says "do NOT write code" but doesn't say what to do instead. Research shows prohibitions paired with alternatives are far more effective: "Do NOT write code, pseudocode, or schemas. INSTEAD describe systems as components, interfaces, data flows, and responsibilities." The positive redirect channels generation toward the desired level rather than relying on inhibition alone.

### Refine Chain synthesis over map-reduce

Instead of feeding all agent responses to a synthesizer at once (which overwhelmed our synthesis step), use a sequential refinement pattern: start with one agent's output as the draft, then fold in each subsequent agent's key points one at a time. Two sequential calls processing ~3k tokens each instead of one call processing 12k+. Research shows this produces higher coherence because each step builds on an integrated document. Key instruction: "Only incorporate content from the additional input if it adds useful information; otherwise return the current draft unchanged."

### Shannon entropy for fast slop detection

Character-level entropy distinguishes real content from filler at zero API cost, 10x faster than LLM-as-judge. Professional prose stays above 4.5 entropy. AI filler ("I apologize for the confusion...") drops below 3.2. A threshold of 3.5 acts as a quality gate: outputs below this trigger regeneration. This could run on every agent response before accepting it into the conversation.

### Multi-tier context window

Research-backed structure with specific numbers:
- **Tier 1 (full fidelity):** Last 3-5 turns verbatim
- **Tier 2 (compressed):** Key decisions and facts extracted from turns 6-15
- **Tier 3 (summary):** Rolling summary paragraph for everything older

12-message window (6 exchanges) is the research-backed sweet spot for task-oriented dialogue. Rolling summary uses incremental updates (only summarize newly dropped content and merge) to keep cost at O(1) per turn.

### Decisions ledger separate from conversation history

A persistent structured object tracking three categories:
- **Decided items** -- with agreement attribution and round number
- **Items under active discussion** -- with each agent's current position
- **Open questions** -- unresolved issues

Injected as high-priority context in every agent call, separate from the conversation summary. This is shared team state, not per-agent state (different from AgentMind). It represents the "project state" that must survive all levels of context compression. When history gets truncated, the ledger persists.

### Observation masking

When compressing older turns, keep each agent's key proposals and critiques but drop the surrounding explanatory text. Research shows this matches or exceeds LLM summarization quality with simpler implementation. The insight: an agent's reasoning matters less than their conclusions for downstream context.

### Quality gate between rounds

Four-stage validation on every agent output before it enters shared state:
1. Regex check against anti-slop phrase list (instant, free)
2. Shannon entropy check with 3.5 threshold (instant, free)
3. Word count verification against per-agent limits (instant, free)
4. LLM-judge evaluation of role adherence (expensive, run selectively or sampled)

Failed outputs trigger regeneration with specific feedback: "Your previous response was rejected because [reason]. Regenerate with these corrections." Cap retries at 3 with progressive constraint tightening: first retry adds a gentle nudge, second adds explicit constraints, third uses few-shot examples.

### Self-verification in system prompt

Add to every agent's perspective reminder: "Before responding, verify: Does this response reflect my assigned role? Am I at the correct abstraction level? Am I genuinely adding perspective or just agreeing?" Lightweight continuous guardrail that costs nothing. Research (Reflexion pattern) shows self-evaluation prompts measurably reduce drift without external critic agents.

---

## Open Questions (surfaced but not resolved)

1. Who speaks for the team after deliberation? Designated spokesperson, rotating, or orchestrator-synthesized?
2. How is the conversation summary generated for the Situation layer? Separate LLM call, signal extraction, or dedicated note-taker agent?
3. Should internal deliberation be free-form or structured (round-robin, facilitator)?
4. What are the specific token budget targets for internal vs cross-team turns?
5. How sophisticated does drift correction analysis need to be? Simple signal patterns or LLM classification?
6. What does turn 1 look like? How does the orchestrator seed productive divergence with no history?
7. How does the STRETCH protocol (uncomfortable idea quota) actually get verified? Markers in the output? Orchestrator judgment?
8. When should Convergence Suppression fire relative to phase boundaries? Late-phase convergence is natural and desired.
