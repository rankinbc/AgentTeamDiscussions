# Discussion Brief: Orchestrator Event Cadence -- What Happens When

## Project Summary

AgentTeamDiscussions is a multi-agent conversation system where 3-7 AI agents debate design questions across 15-30 turns. The orchestrator drives the conversation by building context, managing turn order, and routing messages. Currently, the orchestrator does very little beyond turn management -- agents talk, challenges are detected, urgency drives speaking order.

We are designing the full event architecture: what actions the orchestrator should perform, at what cadence, and what artifacts those actions produce. The goal is to maximize the quality and usefulness of conversation output without overwhelming the token budget or slowing down the session.

## What Exists Today

### Per-turn (every agent message):
- Build agent context (system prompt + conversation history + perspective reminder)
- Detect challenges in agent output (string matching for disagreement signals)
- Update urgency scores (challenged agents get rebuttal priority)
- Compress older messages (first sentence only for messages beyond the recent 7)
- Emit SSE events to the live UI

### Per-session (once at start/end):
- Load team config, build system prompts
- Save transcript to disk (end)
- Rolling synthesis every 5 turns (currently broken -- parser fails)

### Missing entirely:
- Key Takeaway mechanism (spec exists, not implemented)
- Morning Brief generation (exists in session_runner.py but not in live conversation mode)
- Any form of mid-session quality assessment
- Any form of conversation steering by the orchestrator itself
- Any periodic analysis of conversation health
- Post-session artifacts beyond raw transcript

## The Design Question

We need to define the complete event lifecycle for a conversation session. For each possible action, we need to decide:
1. **When does it fire?** (per-turn, every N turns, at phase boundaries, on-demand, post-session)
2. **What triggers it?** (clock, agent behavior, moderator request, threshold)
3. **What does it consume?** (full history, recent messages, structured state, nothing)
4. **What does it produce?** (context injection for next turn, shared state update, output artifact, nothing visible)
5. **What does it cost?** (LLM call, token budget, latency, nothing)

## Candidate Actions to Evaluate

These are not all good ideas. Some may be wasteful, redundant, or counterproductive. The discussion should evaluate each and decide where it belongs in the cadence -- or whether it belongs at all.

### Context Management
- **History compression** -- When and how aggressively to compress older messages
- **Context relevance scoring** -- Should the orchestrator evaluate which prior messages are most relevant to the current thread, rather than just using recency?
- **Agent-specific context curation** -- Should different agents see different subsets of history based on their role? (The context lens already does lightweight attention framing, but not actual filtering)

### Conversation Quality
- **Convergence detection** -- Detecting when agents are circling the same points without progress
- **Diversity audit** -- Checking whether agent responses are genuinely distinct or converging into sameness
- **Topic drift detection** -- Detecting when the conversation has wandered from the original question
- **Depth vs breadth balance** -- Has the conversation gone deep on one subtopic while ignoring others?
- **Participation balance** -- Are some agents dominating while others are silent?

### Decision Capture
- **Key Takeaway proposals** -- When should the system prompt agents to propose takeaways vs letting it happen organically?
- **Concession detection** -- When an agent explicitly concedes a point, should that be captured structurally?
- **Position tracking** -- Maintaining a running map of where each agent stands on each open question
- **Decision confidence scoring** -- How confident is the group in each conclusion?

### Synthesis and Summaries
- **Rolling synthesis** -- Periodic summary of what has been discussed/decided (currently broken)
- **Phase transition briefing** -- Summary at phase boundaries that becomes context for the next phase
- **Thread extraction** -- Identifying the distinct conversational threads and their resolution status
- **Morning Brief generation** -- Post-session summary for the human

### Orchestrator Interventions
- **Anti-stagnation injection** -- When conversation stalls, should the orchestrator inject a provocative question?
- **Rebalancing** -- If one agent has been silent, should the orchestrator prompt them specifically?
- **Topic advancement** -- When a subtopic is exhausted, should the orchestrator propose the next one?
- **Quality gate** -- Should the orchestrator evaluate whether a response is substantive enough before adding it to history?

### Post-Session Actions
- **Morning Brief** -- What should it contain and how should it be generated?
- **Decision log** -- Structured record of what was decided, what was rejected, what is unresolved
- **Transcript enhancement** -- Should the raw transcript be post-processed with annotations (challenge markers, concession markers, topic boundaries)?
- **Next session prep** -- Should the system generate a brief for the next session based on what was left unresolved?

## Constraints

- 250 words max per response
- Every proposed action must justify its cost in LLM calls and token budget
- The system runs overnight on a solo builder's subscription -- every unnecessary LLM call is waste
- Actions that sound good but have no observable effect on output quality should be cut
- Stay at requirements/design level -- describe what happens and when, not how to code it
- Reference the existing Key Takeaway spec when relevant -- it already defines some of these mechanisms

## What Good Output Looks Like

A concrete event cadence table: each action, when it fires, what it costs, what it produces, and whether it belongs in v1 or is deferred. The table should be sorted by when actions fire (per-turn, periodic, phase boundary, post-session). For each action, name the specific artifact or state change it produces and who consumes it (agents, orchestrator, Morning Brief, human).
