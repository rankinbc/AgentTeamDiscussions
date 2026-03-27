---
stepsCompleted: ["step-01-init", "step-02-discovery", "step-02b-vision", "step-02c-executive-summary", "step-03-success", "step-04-journeys", "step-05-domain-skipped"]
inputDocuments: []
workflowType: 'prd'
documentCounts:
  briefs: 0
  research: 0
  brainstorming: 0
  projectDocs: 0
classification:
  project_type: developer_tool
  domain: AI/automation
  complexity: medium-high
  context: greenfield
---

# Product Requirements Document - AgentTeamDiscussions

**Author:** Brian
**Date:** 2026-03-17

## Executive Summary

AgentTeamDiscussions is an autonomous multi-agent discussion system that converts product ideas into implementation-ready specifications without requiring continuous human involvement. A user defines an idea and configures a client agent team via YAML. The system then orchestrates structured discussions between the client team and a BMAD agent team -- each operating in separate Claude context windows, communicating through an MCP server message broker, managed by a Python orchestrator that spawns `claude -p` CLI processes authenticated via Claude Max subscription OAuth.

Discussions progress through four phases (Brainstorm, Refine, Specify, Review), each with distinct communication modes, agent behavior profiles, and exit gates. Agents hold stakeholder positions (Customer, Investor, Builder, Skeptic, etc.) with configurable personality dimensions (assertiveness, creativity temperature, stubbornness, cognitive style) that produce genuine disagreement rather than polite consensus. Background agents analyze conversation history, detect quality degradation, inject provocations, and trigger corrective interventions. Agents can independently research topics, create artifacts, hold internal team deliberations, and develop private positions before responding.

The system runs overnight on idle Max subscription tokens, producing a Morning Brief with prioritized escalation (items for user awareness, items wanting input, items needing decisions), a complete spec set, an Action Log event stream, and full conversation transcripts. The human can steer discussions, approve research requests, make executive decisions, and resume where agents left off. All entities (agents, ideas, decisions, artifacts) persist across sessions with provenance chains, magnitude-based relevance tracking, and warm/cold archive boundaries.

The system is designed to be tuned through trial and error. All thresholds, personality weights, phase triggers, and anti-slop mechanisms are configurable and observable. Observability and configurability are first-class requirements -- quality emerges from iteration, not from getting initial settings right.

### What Makes This Special

The core insight: solo builders don't lack ideas or build tools -- they lack patience for the spec grind. AgentTeamDiscussions fills that gap by converting idle subscription tokens and sleeping hours into thoroughly stress-tested requirements.

Unlike single-pass AI document generation, this system produces specs that have been argued over by agents with genuine stakes, independent research capability, and engineered cognitive diversity. The creativity engine -- personality dimensions, positional framing, 10 anti-slop mechanisms, 62 brainstorming techniques as cognitive patterns, phase-specific dynamics -- exists to solve the hardest problem: making multiple instances of the same LLM produce output that is genuinely diverse, surprising, and useful rather than homogeneous slop.

The discussion transcript itself is a product -- transparent, entertaining, and readable. Agents don't just generate documents; they debate, research, concede, escalate, and evolve their positions. The system balances autonomous orchestration (background agents, phase transitions, convergence suppression) with organic agent behavior (independent ideas, private analysis, stubborn defense of positions) to produce conversations that feel like a real product team, not an LLM talking to itself with different names.

## Project Classification

| Dimension | Value |
|---|---|
| Project Type | Developer Tool |
| Domain | AI / Automation |
| Complexity | Medium-High |
| Context | Greenfield |

## Success Criteria

### User Success

- The system produces ideas, features, and solutions the user hadn't considered -- clever, non-trivial thinking, not obvious suggestions
- Overnight runs produce specs detailed enough to serve as a foundation for architecture and development, even if the user tweaks them before proceeding
- The conversation transcript is worth reading -- surprising, coherent, not boring, repetitive, or dull
- Problems and edge cases surface that the user wouldn't have caught on their own
- The Morning Brief gives the user a clear picture of what happened, what needs attention, and where they can steer

### Business Success

- Not the primary driver for v1 -- this is a personal productivity tool for the user's own idea pipeline
- If the tool proves effective, it may be applied to business-oriented ideas where it could produce market-facing specs
- Long-term potential as a product for other solo builders (Vision territory)

### Technical Success

- Two agent teams reliably exchange messages through the MCP server without loss or corruption
- Sessions run to completion overnight without crashing, stalling, or looping
- Context efficiency mechanisms prevent context window blowouts over long sessions
- Agents maintain distinct personalities and positions -- no degradation into generic responses
- The system is observable: Action Log captures typed, timestamped events for what happened, when, and why
- All configuration (agents, teams, environment, thresholds) is tunable via YAML without code changes
- The system fails gracefully -- state is preserved for analysis or resumption

### Measurable Outcomes

- A single overnight run produces a spec set the user considers worth refining, not discarding
- Agent contributions are distinguishable by voice, position, and reasoning style
- The user continues using the system for additional ideas after the first successful run
- Tuning iterations produce noticeably different results

## Product Scope

### MVP - Minimum Viable Product

- Two teams (BMAD + configurable client) communicate through MCP server message broker
- Python orchestrator manages turn-taking via `claude -p` CLI processes
- Client team configurable via YAML (agent names, personality traits, positions)
- Agent Model: agents have mood, ideas (with magnitude and passive decay), personality dimensions, and positions. When forming a response, agents scan for relevant ideas and surface them. Opposing arguments shift idea magnitude. Ideas below threshold are conceded/abandoned (archived). Ideas have origin types (original, reactive, researched).
- Basic conversation -- agents respond to each other, maintain perspective, can disagree
- Session runs to completion with configurable turn limits
- Full transcript output, basic summary generation
- No phase system, no environmental system -- raw conversation between configured agents

### Growth Features (Post-MVP)

- **AgentDiscussionEnvironment** -- ambient state variables (phase-like dynamics as environmental shifts) that influence agents and teams. One-directional: environment acts on agents. BackgroundAgents close the feedback loop by observing agents and modifying environment.
- **BackgroundAgent system** -- Specter, Muse, Director, Curator, Weaver, TieBreakerGhost, Oracle analyzing and influencing the discussion environment
- **Agent Model expansion** -- mood with inertia/momentum, energy/fatigue, frustration accumulator, concession taxonomy (evidence-based, social pressure, exhaustion, trade), idea cross-pollination, voice modulation based on mood + personality state
- **Anti-slop mechanisms** -- primarily baked into agent construction and idea/thought generation methods, with some environmental knobs
- **Morning Brief** with prioritized escalation tiers (FYI / want input / need input / need tiebreaker)
- **Action Log event stream** -- typed, timestamped events distinct from conversation
- **Human steering** -- executive decisions, research approval queue, direction changes
- **Research sub-agents** -- agents request research, human approves to control token spend
- **Mood tracking** as diagnostic signal and environmental input
- **Multi-session persistence** -- AgentMinds, ideas, decisions carry across sessions with warm/cold archive boundaries
- **Highlights and summarization**

### Vision (Future)

- Environmental system sophisticated enough to consistently produce genuinely interesting, non-repetitive output
- Agent-to-agent relational state (affinity, credibility perception, alliance/rivalry emergence)
- Idea lineage tracking and visualization
- Specs consistently good enough to feed directly into automated build pipelines
- Discussion templates for different output types
- Full autonomous pipeline: idea -> overnight discussion -> specs -> automated build -> working product
- Potential productization for other solo builders

### Core Engines

The system decomposes into these primary engines:

1. **Conversation Engine** -- MCP server, orchestrator, turn management, message routing, context efficiency
2. **Agent Model Engine** -- internal architecture of DiscussionAgents (mood, ideas with magnitude, personality, stances, voice modulation)
3. **Creativity Engine** -- agent generation methods, anti-slop in construction, technique-as-cognition, idea production methods
4. **Influence/Effects Engine** -- AgentDiscussionEnvironment, what affects what, property dependency graph
5. **BackgroundAgent Engine** -- observer agents that analyze and modify the environment
6. **Tracking & Analysis Engine** -- Action Log, mood tracking, summarization, Morning Brief, highlights
7. **Team-vs-Team Interaction Engine** -- cross-team message exchange, disagreement surfacing, escalation
8. **Intra-Team Interaction Engine** -- internal deliberation, private analysis, bench system
9. **Configuration Engine** -- YAML-based config, templates, validation, the "mixing board"
10. **Persistence & State Engine** -- entity serialization, archive boundaries, session continuity, provenance

## User Journeys

### Journey 1: The Idea Owner -- "I had an idea in the shower"

Brian has been thinking about a product idea for weeks -- a tool that helps freelancers track unbilled time across multiple clients. He's got the core concept but doesn't have the patience to sit down and flesh out every edge case, pricing model, and user flow. He opens his AgentTeamDiscussions config folder.

He creates a new YAML file for the client team: a Power User freelancer, a Casual User who's new to freelancing, an Investor who wants to see monetization potential, a Skeptic who's seen ten time-tracking apps fail, and a Builder who'll push for clear specs. He gives the Power User high assertiveness and stubbornness -- she needs to fight for the features that matter. The Skeptic gets high creativity temperature so his objections come from unexpected angles.

He writes a brief idea description: "A time tracker for freelancers that automatically detects billable work across tools (Slack, email, IDE, browser) and generates invoices. The insight is that freelancers lose 15-20% of billable hours because they forget to start timers."

He kicks off the session, sets a turn limit of 200, and goes to bed.

**Requirements revealed:** Idea input format, client team YAML configuration, session initialization, turn limit configuration, overnight autonomous operation.

### Journey 2: The Morning Reviewer -- "What did they come up with?"

Brian wakes up and opens the Morning Brief. It shows:

- **Session summary:** 187 turns across the discussion. 23 ideas generated, 8 survived refinement. 3 major disagreements resolved, 1 unresolved.
- **Needs your input (2 items):** The team split on whether automatic time detection should be opt-in or opt-out (privacy implications). The Investor and the Power User deadlocked on whether to offer a free tier.
- **FYI (5 items):** The Skeptic raised a strong point about competing with Toggl's new AI feature. The Builder flagged that cross-tool detection requires browser extensions which adds complexity. Three new feature ideas emerged that nobody expected.
- **Highlights:** The best exchange was the Casual User arguing with the Power User about complexity -- the Casual User said "If I need a tutorial to start a timer, you've already lost me" which reframed the entire onboarding discussion.

Brian reads the highlights, skims a few interesting exchanges in the transcript, then makes his executive decisions: "Opt-in for automatic detection. Yes to free tier but limited to 2 clients." He queues these as directives for the next session.

**Requirements revealed:** Morning Brief generation with prioritized tiers, highlights extraction, unresolved disagreement surfacing, human directive input, session continuation with new directives.

### Journey 3: The Participant -- "Let me talk to the team"

Brian reads the Morning Brief and notices the Skeptic has been pushing hard against the browser extension approach. He wants to understand why before making a call. He opens a direct conversation with the Skeptic in converse mode.

"Why are you so against the browser extension?"

The Skeptic responds in character: "Three reasons. First, Chrome's Manifest V3 restrictions are going to limit what extensions can do -- I've seen two competitors get burned by this. Second, your casual user persona hates installing things. Third, the maintenance burden of supporting extensions across browsers will eat your development capacity for the first year."

Brian thinks that's a good point but he has context the Skeptic doesn't. He switches to suggest mode: "What if we started with a desktop app that monitors active windows instead of a browser extension? It would cover browser activity without needing an extension."

The Skeptic considers it -- the suggestion carries heavy weight but he doesn't just agree. "That solves the browser problem but introduces a new one: desktop apps need OS-level permissions that are getting harder to get on macOS. Still, it's better than extensions. I'd shift my objection from 'strong oppose' to 'cautious concern.'"

Brian is satisfied. But he also notices the Builder agent has been too passive -- barely contributing. He switches to command mode: "Builder, your assertiveness is now 0.8. I want you pushing harder on technical feasibility in the next session."

**Requirements revealed:** Direct agent conversation (converse mode with no influence), suggest mode (high-weight influence), command mode (direct state/value override), per-agent interaction, mode switching.

### Journey 4: The System Tuner -- "Why was that session so boring?"

Brian runs a session on a new idea and the output is disappointing. The agents agreed too quickly, the ideas were obvious, and the transcript was dull. He opens the Action Log.

The event stream tells the story: by turn 15, all agents had converged on the same basic approach. No agent surfaced a dissenting idea after turn 20. Mood flatlined to "neutral" across all agents by turn 30. The session ran for 150 more turns of polite elaboration on the same concept.

Brian identifies the problem: the team composition was too homogeneous. All agents had moderate assertiveness and low stubbornness. Nobody was configured to fight. He opens the client team YAML and makes changes:

- Adds a new agent: a Competitor position with high creativity temperature and high stubbornness
- Bumps the Skeptic's assertiveness from 0.4 to 0.8
- Changes the Customer variant from Casual to Frustrated Switcher (someone with strong existing opinions)
- Lowers the Investor's agreeableness by raising stubbornness

He re-runs the session on the same idea with the adjusted team. This time the Action Log shows sustained disagreement through turn 80, three idea pivots, and two "I changed my mind" concession events. The output is substantially better.

**Requirements revealed:** Action Log with diagnostic event stream, mood tracking visualization, YAML configuration editing and re-running, agent personality adjustment between sessions, re-running the same idea with different configurations, before/after comparison capability.

### Journey Requirements Summary

| Capability Area | Revealed By |
|---|---|
| Idea input and session initialization | Journey 1 |
| Client team YAML configuration | Journey 1, Journey 4 |
| Overnight autonomous operation | Journey 1 |
| Morning Brief with prioritized tiers | Journey 2 |
| Highlights extraction from transcript | Journey 2 |
| Human directive input for next session | Journey 2 |
| Direct agent conversation (converse mode) | Journey 3 |
| Suggest mode (high-weight influence) | Journey 3 |
| Command mode (direct override) | Journey 3 |
| Per-agent interaction and mode switching | Journey 3 |
| Action Log event stream for diagnostics | Journey 4 |
| Mood tracking and visualization | Journey 4 |
| Re-run same idea with adjusted config | Journey 4 |
| Before/after comparison across runs | Journey 4 |
| Session continuation with new context | Journey 2 |

