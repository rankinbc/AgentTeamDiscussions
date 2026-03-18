# AgentTeamDiscussions - Entity Model

**Date:** 2026-03-17
**Status:** Draft - discovered during PRD creation, pre-architecture

---

## Core Entities

### AgentTeamDiscussion
Top-level entity representing one idea/vision being explored. Spans multiple sessions. Owns all entities below it. Never deleted. Carries rollup-friendly status fields (phase, decision count, unresolved escalations, health score) for future portfolio views.

### AgentDiscussionState
The "working memory" of an AgentTeamDiscussion. Contains only what is current and pressing. Teams interact with this, not the full history. BackgroundAgents analyze the deep history and make surgical modifications to this state. This is the lightweight surface that sessions operate against.

### Session
One execution run within an AgentTeamDiscussion. Has a start, end condition (time-based, turn-based, token-based, or convergence-based), and resource budget (max invocations, max research spawns, max BackgroundAgent runs). Includes a preparation step that prepares each agent's context. Multiple sessions per AgentTeamDiscussion. Between sessions: curation, analysis, idea/question injection.

### Team
A named group of DiscussionAgents with a shared system prompt and role. Configured via YAML with sensible defaults. An AgentTeamDiscussion has 2+ teams. Teams can be reconfigured between sessions.

### DiscussionAgent
An individual persona within a Team. Has a permanent GUID -- never deleted, can be archived/unarchived. Full history preserved even after they stop participating. Can be created from config templates OR created by AI analysis mid-discussion with specific parameters. Snapshotted per session so swapping agents between sessions doesn't break message history.

**Personality properties:**
- Assertiveness (how strongly they push their ideas)
- Curiosity (likelihood of reading ProposalArtifacts on topics outside their focus)
- Other traits TBD during architecture

**Roster status:**
- Active: participating in current turn's exchange
- Bench: on the team but not active for this exchange. Activation criteria determines when they come in.
- Archived: no longer participating, full history preserved, can be unarchived

### AgentMind
Per-DiscussionAgent internal state. Contains Ideas, concerns, each with magnitude. Personality traits influence behavior (high assertiveness + high magnitude idea = fights for it). Serialized between sessions. Between sessions, magnitude adjusts up/down, and low-magnitude items get trimmed from the "CurrentAgentMind" that gets loaded into context. Full historical AgentMind preserved for analysis.

---

## Agent Behavior Entities

### PrivateAction
Something a DiscussionAgent does outside of any conversation that affects their AgentMind. Not visible to other agents unless it produces a ProposalArtifact. Examples:
- Reading another agent's ProposalArtifact and shifting magnitude on a related Idea
- Writing a rebuttal ("here's why you're wrong") as a ProposalArtifact
- Independent analysis of a topic that strengthens or weakens a stance
- After conceding, attempting to change teammates' minds during next internal team deliberation

### ProposalArtifact
A longer-form argument or position piece created by a DiscussionAgent through a PrivateAction. Different from conversation Messages -- these are structured, persistent, and independently analyzable.

**Types:**
- Position argument ("here's why X is the right approach")
- Rebuttal ("here's why your position on Y is wrong")
- Analysis ("I looked into Z and here's what I found")
- Vision piece ("imagine if we did it this way...")

**Behavior:**
- Goes into a shared set visible to all agents
- Agents may choose to read or ignore based on criteria (relevance to their Ideas, curiosity trait, stance on the topic)
- Reading a compelling ProposalArtifact can shift an agent's magnitude on related Ideas, or trigger a Concession
- Can be analyzed by BackgroundAgents outside the main discussion context

### Concession
When a DiscussionAgent gives up a stance on an Idea or Disagreement.

**Effects:**
- The Idea's magnitude drops to zero or the Idea state moves to "resolved"
- May trigger the agent to advocate for the new position during internal team deliberation (trying to bring teammates along)
- Cascading: one agent's concession can shift the team's overall agreement score
- Recorded with provenance (what caused the concession -- a ProposalArtifact, a convincing Message, a TieBreakerGhost ruling)

### Bench
A Team's inactive roster for a given exchange. Not all DiscussionAgents participate in every turn.

**Activation criteria (determines who comes off the bench):**
- Topic relevance to agent's expertise/Ideas
- Agent has a high-magnitude Idea relevant to the current exchange
- Rotation to ensure all agents participate over time
- Director BackgroundAgent can override

---

## Communication Entities

### Channel
A communication pathway. Types:
- Cross-team (brainstorm channel between teams)
- Internal (team deliberation, not visible to other teams)

### Message
A single communication. Stored as individual files (guid filename) for context efficiency. Metadata in a pointer file (current.json), content in markdown.

**Properties:**
- GUID
- Sender (team + DiscussionAgent)
- Channel
- Type: question, proposal, agreement, challenge, statement
- Confidence score
- Summary (for metadata-only reads)
- Timestamp, sequence number
- Provenance chain (created_by, source references)

---

## Process Entities

### Phase
A stage of the conversation governing ideation style, not technical depth. These teams are ideation and requirements machines -- they debate "what should this product do and why," not technical implementation details like programming languages or algorithms.

**Phase types:**
- **Brainstorm**: Wild ideas, expansive thinking, no bad ideas. High creativity weighting.
- **Refine**: Challenge assumptions, narrow scope, find gaps. High assertiveness weighting.
- **Specify**: Pin down requirements, acceptance criteria, user stories. Precision emphasis.
- **Review**: Adversarial check of the requirements. Every weakness found.

**Phase properties:**
- Entry/exit criteria
- Deliberation profile: internal turn budget, prompt emphasis, which AgentMind traits to weight higher
- Spec validation gates before completion
- Communication style guidance (freeform Messages during brainstorm, structured Proposals during specify)

Technical implementation decisions (tech stack, algorithms, performance optimization) are explicitly out of scope for these discussions -- that work is done by specialized developer agents downstream.

### ResearchRequest
A question spawned as a separate claude process. Isolated from team context -- only the findings get fed back. Linked to the Message that triggered it. Results written to a file, requesting team reads just the conclusion.

### Briefing
Session-level compressed summary for context seeding. Generated at phase transitions or session boundaries. Used to seed fresh context windows when the orchestrator resets a team's context.

### DiscussionBriefing
Discussion-level "catch me up on everything" summary. Distinct from session Briefing. The comprehensive overview for returning to an AgentTeamDiscussion after time away.

---

## Idea & Decision Entities

### Idea
A queued thought/suggestion associated with a DiscussionAgent. Universal injection point for multiple features.

**Properties:**
- Magnitude (influences how assertively the agent pushes it)
- State: queued, surfaced, discussed, resolved, faded
- Source: analyst finding, research result, human injection, agent reasoning, BackgroundAgent, cross-pollination from another AgentTeamDiscussion (future)

Magnitude rises and falls over time. Low magnitude Ideas fade into irrelevance and get trimmed from CurrentAgentMind. High magnitude Ideas with assertive agents get defended vigorously.

### Decision
A logged choice made during discussion.

**Properties:**
- Topic
- Choice made
- Rationale
- Confidence score
- Agreement score (cross-team)
- Provenance chain (which Messages, Ideas, ResearchRequests led to this)
- Type: consensus, executive, tiebreaker

### Disagreement
A tracked conflict between parties.

**Lifecycle:**
1. Minor (short-lived): Parked in "come back later" queue, may resolve naturally
2. Significant (persists across N turns): Triggers remediation
   - Each party writes a PositionPaper
   - TieBreakerGhost BackgroundAgent analyzes and rules
   - May tweak an agent's AgentMind (reduce opposing idea magnitude)
   - OR escalate to ExecutiveDecision
3. Critical (blocks progress): Escalate to human

**Properties:**
- Parties involved
- Topic
- Agreement score over time
- Position papers
- Resolution method and outcome
- Queue priority

### PositionPaper
A formal argument written by one side of a Disagreement. Contains reasoning for why their position is correct and the opposing position is wrong. Used as input to TieBreakerGhost resolution.

### ExecutiveDecision
A Decision subtype made by human authority, not team consensus. Overrides team disagreement. Can be triggered by Escalation or predefined rules.

### Escalation
A question routed to the human when teams can't resolve it. Has question, context, options, and async response mechanism (webhook/notification). Conversation can continue on other topics while awaiting response.

---

## Background Entities

### BackgroundAgent
Operates on full history but is NOT a participant in team conversations. Reads deep history, writes to AgentDiscussionState, AgentMind, or Idea queues.

**Authority levels:**
- Advisory: injects Ideas, writes findings for optional consumption
- Authoritative: can pause sessions, force phase transitions, escalate to human

**Types:**
| Type | Role |
|---|---|
| Curator | Manages relevance -- surfaces, archives, adjusts magnitude of Ideas/concerns |
| Oracle | Deep pattern analysis -- trends, contradictions, missed connections |
| Specter | Conversation health -- detects stalling, circular arguments, one-sidedness. Has circuit breaker authority. |
| Director | Active intervention -- creates/archives DiscussionAgents, modifies teams, injects phase transitions |
| Weaver | Cross-pollination -- connects threads between sessions, links Decisions, synthesizes Briefings |
| TieBreakerGhost | Disagreement resolution -- analyzes position papers + research + randomness, produces rulings |
| Custom | One-off or user-defined with specific analysis goals |

**Configuration:** YAML-based, with frequency (every N turns), what they read, and authority level. Can be auto-spawned by other BackgroundAgents.

---

## Artifact Entity

### Artifact
A spec document produced by the process (PRD, architecture, epics, etc.). Has draft/final states. Cumulative across sessions. Must pass spec validation gate before moving to final -- checked for: traceability to Decisions, absence of ambiguity, implementation-readiness.

---

## Cross-Cutting Concerns

### Provenance
All entities that create or modify other entities record a provenance chain: created_by, source_message, triggered_by. Not for runtime use, but for post-session forensics and deep analysis.

### Context Efficiency
- Messages stored as individual files (guid.md) with pointer files (current.json)
- Teams read only latest messages; their own conversation history lives in their claude instance context
- Research results isolated from team context
- BackgroundAgent findings injected as small briefing notes, not full reports
- Briefings generated at phase transitions to enable context resets

### Data & Analysis
- Full history preserved on disk for all entities -- no shortage of storage
- Bulk data parseable into analysis-ready datasets
- Different analysis types: small focused datasets vs large comprehensive analysis
- Future: ML/neural network implementations for large-scale pattern detection
- BackgroundAgents are the primary consumers of deep history

### Session Preparation
Each session includes preparation:
- AgentMind serialization loaded per agent
- Magnitude-based trimming for CurrentAgentMind
- Ideas that are resolved/conceded removed
- Briefing or DiscussionBriefing loaded
- Resource budget set

---

## Entity Relationships

```
AgentTeamDiscussion 1──1 AgentDiscussionState
AgentTeamDiscussion 1──* Session
AgentTeamDiscussion 1──* Team
AgentTeamDiscussion 1──* Decision (cumulative)
AgentTeamDiscussion 1──* Artifact (cumulative)
AgentTeamDiscussion 1──* Disagreement
AgentTeamDiscussion 1──* DiscussionBriefing
Team                1──* DiscussionAgent
DiscussionAgent     1──1 AgentMind
AgentMind           1──* Idea
DiscussionAgent     0──* PrivateAction
DiscussionAgent     0──* ProposalArtifact (authored)
DiscussionAgent     0──* Concession
ProposalArtifact    *──* DiscussionAgent (readers)
Session             1──* Message
Session             1──* BackgroundAgent run
Session             1──* ResearchRequest
Session             1──1 Phase (current)
Session             1──* Briefing
Disagreement        1──* PositionPaper
Disagreement        0──1 ExecutiveDecision
Message             *──1 DiscussionAgent (sender)
Decision            *──* Message (provenance)
Idea                *──1 DiscussionAgent (assigned to)
BackgroundAgent     *──* AgentMind (modifies)
BackgroundAgent     *──* AgentDiscussionState (modifies)
```
