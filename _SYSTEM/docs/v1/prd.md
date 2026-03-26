---
stepsCompleted: ['step-01-init', 'step-02-discovery', 'step-02b-vision', 'step-02c-executive-summary', 'step-03-success', 'step-04-journeys', 'step-05-domain-skipped', 'step-06-innovation', 'step-07-project-type', 'step-08-scoping', 'step-09-functional', 'step-10-nonfunctional', 'step-11-polish', 'step-12-complete']
classification:
  projectType: cli_tool
  domain: scientific
  complexity: medium
  projectContext: brownfield
inputDocuments:
  - '_SYSTEM/docs/features/prd.md'
  - '_SYSTEM/docs/features/v1-orchestrator-spec.md'
  - '_SYSTEM/docs/features/entity-model.md'
  - '_SYSTEM/docs/features/session-platform.md'
  - '_SYSTEM/docs/features/research-scope-controls.md'
  - '_SYSTEM/docs/features/conversation-engine/turn-anatomy.md'
  - '_SYSTEM/docs/features/conversation-engine/context-assembly-template.md'
  - '_SYSTEM/docs/features/conversation-engine/orchestrator-event-cadence.md'
  - '_SYSTEM/docs/features/conversation-engine/key-takeaway-mechanism.md'
  - '_SYSTEM/docs/features/conversation-engine/morning-brief-format.md'
  - '_SYSTEM/docs/features/conversation-engine/rebuttal-priority.md'
  - '_SYSTEM/docs/features/conversation-engine/moderator-input.md'
  - '_SYSTEM/docs/features/creativity-engine/personalities.md'
  - '_SYSTEM/docs/features/creativity-engine/positions.md'
  - '_SYSTEM/docs/features/creativity-engine/techniques.md'
  - '_SYSTEM/docs/features/creativity-engine/anti-slop-mechanisms.md'
  - '_SYSTEM/docs/features/creativity-engine/phase-dynamics.md'
  - '_SYSTEM/docs/concepts/design-principles.md'
  - '_SYSTEM/docs/concepts/agent-behavior-philosophy.md'
  - '_SYSTEM/docs/concepts/creativity-engine-overview.md'
  - '_SYSTEM/docs/concepts/briefs/conversation-system-v1.md'
  - '_SYSTEM/docs/concepts/research/research-applied.md'
  - '_SYSTEM/docs/plans/conversation-engine-review.md'
  - '_SYSTEM/docs/plans/implementation-gaps.md'
  - '_SYSTEM/docs/plans/v1-spec-gaps.md'
documentCounts:
  briefs: 1
  research: 4
  brainstorming: 0
  projectDocs: 21
workflowType: 'prd'
---

# Product Requirements Document - AgentTeamDiscussions

**Author:** Badmin
**Date:** 2026-03-25

## Executive Summary

AgentTeamDiscussions converts product ideas into implementation-ready specifications overnight through autonomous multi-agent AI discussions. A user provides a high-level idea before leaving for the day. A team of AI agents -- each with distinct personality traits, stakeholder positions, and reasoning techniques -- debates, challenges, refines, and specifies the idea across structured discussion rounds. By morning, the user receives a Morning Brief: a concise report of confirmed decisions, unresolved disagreements, and generated specification artifacts (PRDs, architecture docs, user stories) -- all produced without human monitoring.

The system runs as a Python CLI tool, orchestrating multiple Claude conversations via subprocess calls. Each agent operates in its own stateless context window, receiving curated situation context per turn. A conversation engine manages turn-taking, context assembly (4,000-token payload ceiling), and round progression (propose/critique/evaluate). A creativity engine ensures genuine intellectual friction through 8-dimension personality models, stakeholder positions that create authentic self-interest, and anti-slop mechanisms that suppress LLM default behaviors (polite agreement, semantic clustering, premature convergence).

### What Makes This Special

The core insight: a single AI produces surface-level specs with gaps because nobody pushes back. A *team* of AI agents with genuinely different perspectives -- a skeptic who distrusts elegant solutions, a customer advocate who demands user value, a builder who asks "what's simplest?" -- finds gaps through real friction, not performed debate. The user doesn't orchestrate agents or monitor conversations. They state an idea, go to sleep, and wake up to specs that have survived pressure-testing from six different angles. The differentiator vs multi-agent frameworks (CrewAI, AutoGen, LangGraph): those are plumbing. This is a product that delivers an outcome -- implementation-ready specifications from a one-sentence idea.

## Project Classification

- **Type:** Python CLI tool / developer tool hybrid
- **Domain:** AI research tooling (multi-agent LLM orchestration)
- **Complexity:** Medium -- novel prompt engineering patterns, no regulatory requirements
- **Context:** Brownfield -- working beta with multi-round discussion modes, personality-driven prompt assembly, session management, and live web dashboard. V1 targets a shippable single-team session runner built on existing beta code.

## Success Criteria

### User Success

- User provides a product idea (1-2 pages of context) and receives a complete planning package within one overnight session (~8 hours)
- Output covers requirements, edge cases, and architectural decisions the user hadn't explicitly considered -- genuine gap-filling, not parroting input back
- Idea-oriented agents propose features beyond the user's input; the team debates feasibility and value, filtering out low-ROI suggestions autonomously
- Output is structured and complete enough to hand directly to AI coding agents (Claude Code, Cursor, etc.) for implementation
- User spends < 1 hour reviewing and modifying output before it's implementation-ready
- User feels "I would've missed that" at least 3 times per session -- the system adds value beyond what a single AI conversation produces

### Business Success

- 3-month: Tool reliably produces usable specs for the creator's own product ideas, saving 2-3 days of planning per idea
- 6-month: Output quality high enough that AI-generated code from these specs requires minimal rework
- 12-month: Potential to share with other builders who want the same "idea to plan" acceleration

### Technical Success

- Sessions complete unattended overnight without crashes or data loss
- Session recovery works -- if interrupted, can resume from last completed question
- Morning Brief accurately reflects the session's decisions (no hallucinated conclusions)
- Output artifacts are well-structured markdown usable by downstream AI tools
- System runs on a single machine with Claude Max subscription -- no infrastructure required

### Measurable Outcomes

- End-to-end: idea input to complete spec package in < 8 hours unattended
- Spec completeness: output addresses > 80% of requirements that a human PM would identify
- Gap discovery: at least 3 non-obvious insights per session that weren't in the input
- Feature discovery: at least 1-2 novel feature proposals per session survive team scrutiny
- Reliability: < 10% session failure rate on well-formed inputs

## Product Scope

### MVP - Minimum Viable Product

- Single-team session runner (one team of agents discussing one idea -- no multi-team, no MCP)
- Agent configuration via YAML (personalities, positions, techniques, actions) -- not "team configuration" (that's V2)
- Three-round discussion per question (propose/critique/evaluate + synthesis)
- Idea-oriented agents that propose features beyond user input; team debates and filters by feasibility/value
- Cognitive action system: orchestrator-injected Task directives defined in agent YAML with triggers (periodic, round-based, once-per-question). Max 1 action per turn. Pushes agents to propose features, find flaws, challenge assumptions on schedule
- Prior context chaining across questions (decisions ledger)
- Conversation engine with context management as a separate concern (designed to accommodate future external context sources: prior sessions, RAG, research findings)
- Morning Brief output with decisions, open items, and divergence flags
- Design doc template enforcement in synthesis prompts (decision-with-rationale, "what was cut and why", blocking/non-blocking open items)
- session_status.json per-round tracking
- Anti-pattern lists as core feature (8-12 forbidden phrases per agent, not optional)
- Session folder with transcripts and design docs
- Crash-safe disk writes with session resume
- Live dashboard mode (`--live`) for development/tuning via SSE
- CLI invocation: `python session_runner.py brief.md [--live]`

### V1 Should-Have (If Time Allows)

- Sparks field in brief input format (half-formed "what if" ideas as discussion fuel)
- Basic post-session evaluation (scoring rubric against design doc quality dimensions)
- Research action (limited: 2 calls per agent per session, 15k input cap, 2k output cap)

### Growth Features (Post-MVP)

- Phase system (Brainstorm → Refine → Specify → Review) with automatic transitions
- Moderator input (live steering via HTTP)
- Dynamic turn ordering (rebuttal priority / urgency meter)
- Key Takeaway mechanism (convergence detection and voting)
- Evaluation engine with rubric scoring
- Multiple output artifact types (PRD, architecture doc, user stories)
- Research engine (external data gathering during discussions)

### Vision (Future)

- Team Configuration layer -- multi-team with spokesperson/internal deliberation
- MCP Message Broker -- cross-team communication channel
- Full magnitude system with ideas/stances tracking and BackgroundAgents
- Intra-team deliberation between rounds
- Context management pulling from prior sessions, RAG, research findings
- Web UI for session monitoring and artifact browsing
- Agent library with sharable team configurations

## User Journeys

### Journey 1: "The Overnight Spec Run" (Primary -- Happy Path)

Meet Badmin. It's Monday evening. He's been noodling on an idea for a marketplace app all weekend -- knows the core concept but hasn't mapped out the details. He opens his terminal, writes a 2-page brief describing the idea, the target user, and a few constraints. He runs `python session_runner.py marketplace-brief.md`, watches the first agent response scroll by to confirm it's working, then goes to bed.

Overnight, six agents discuss the idea across 10 questions. The skeptic pokes holes in the payment flow. The customer advocate realizes the onboarding is too complex. The builder proposes a simpler MVP scope. One idea-oriented agent suggests a "seller reputation score" feature nobody had considered -- the team debates it, likes it, adds it to the spec.

Tuesday morning, Badmin opens the session folder. The Morning Brief has 8 confirmed decisions, 2 flagged disagreements (both about pricing strategy), and a link to the full design doc. He reads it in 15 minutes, tweaks one decision about the search algorithm, and hands the package to Claude Code. By Wednesday he's looking at a working prototype.

**Capabilities revealed:** Session lifecycle, multi-round orchestration, agent team composition, Morning Brief generation, design doc output, decisions ledger, idea-oriented agent proposals.

### Journey 2: "The Interrupted Session" (Edge Case -- Recovery)

Same setup, but at 2am the Claude CLI throws a timeout on question 7 of 10. The session runner catches it, writes the partial results to disk, logs the failure, and continues to question 8. In the morning, Badmin sees the Morning Brief has a System Alert: "Question 7 failed after retry -- 9 of 10 questions completed." He reviews the 9 completed questions, decides the gap isn't critical, and uses the output as-is. Later he re-runs just the missing question.

**Capabilities revealed:** Crash-safe disk writes, failure cascade per question, session resume, partial result handling, System Alert in Morning Brief.

### Journey 3: "The Team Tweaker" (Configuration)

Badmin has run a few sessions and notices the agents are too polite -- too much agreement, not enough pushback. He opens `config/teams/beta-agents.yaml`, bumps the skeptic's assertiveness from 0.6 to 0.9, adds a new anti-slop rule ("never agree with more than 2 agents in the same round"), and creates a new agent -- "The Devil's Advocate" with ego 0.95 and a bias toward finding fatal flaws. He re-runs the same brief and compares outputs.

**Capabilities revealed:** YAML agent configuration, personality trait tuning, anti-slop rule customization, agent creation, session comparison (same input, different team config).

### Journey 4: "The Brief Writer" (Input Quality)

Badmin has a vague idea -- "something with AI and recipes." He writes a one-paragraph brief and runs a session. The output is scattered -- agents went in different directions because the input was too thin. He learns that brief quality matters: next time he writes 2 pages with clear constraints, decided features, and open questions. The output is dramatically better. The system rewards thoughtful input.

**Capabilities revealed:** Brief format and structure, input quality correlation to output quality, brief template/guidance.

### Journey 5: "The Morning Review & Tuning" (Feedback Loop)

Wednesday morning. Badmin has the Morning Brief open and the specs look mostly good, but one section on authentication feels shallow -- the agents agreed too quickly and didn't explore alternatives. He needs to understand *why*.

He opens the session transcript for that question. He can see: the skeptic raised a concern but the builder shut it down and everyone folded. The anti-slop mechanisms didn't fire -- the agreement tax threshold was too high. Now he knows: the problem is *dynamics*, not *knowledge*. He notes "Skeptic needs higher stubbornness on security topics" and adjusts the YAML for next time.

Over time, these reviews create a feedback pattern: run → review → diagnose dynamics → tune agents → re-run. The specs get better because the *team* gets better.

**V1 scope for review:** Human-readable transcripts per question, Morning Brief flags low-confidence decisions (tells you *where* to look), per-question output in separate files for navigation. Structured review harness deferred to post-MVP.

**Capabilities revealed:** Readable session transcripts, per-question file navigation, Morning Brief as diagnostic entry point, feedback-driven agent tuning cycle.

### Journey Requirements Summary

| Capability | Journeys | Priority |
|---|---|---|
| Session lifecycle (start → overnight → output) | J1, J2 | MVP |
| Multi-round orchestration (propose/critique/evaluate) | J1 | MVP |
| Agent team configuration (YAML personalities, positions) | J1, J3 | MVP |
| Morning Brief generation | J1, J2, J5 | MVP |
| Design doc / spec output per question | J1, J5 | MVP |
| Decisions ledger with context chaining | J1 | MVP |
| Idea-oriented agents (feature proposals) | J1 | MVP |
| Crash-safe writes + failure cascade | J2 | MVP |
| Session resume from interruption | J2 | MVP |
| Anti-slop mechanisms in prompts | J3, J5 | MVP |
| Brief template / input guidance | J4 | MVP |
| Human-readable transcripts per question | J5 | MVP |
| Morning Brief as diagnostic (flags weak decisions) | J5 | MVP |
| Session comparison (same brief, different config) | J3 | Post-MVP |
| Structured review harness / UI | J5 | Post-MVP |
| Automated dynamics detection | J5 | Vision |

## Innovation & Novel Patterns

### Detected Innovation Areas

1. **Autonomous overnight spec generation** -- No existing tool takes a product idea and produces implementation-ready specs unattended. CrewAI, AutoGen, and LangGraph provide orchestration primitives, but none deliver a "sleep on it" product experience. The innovation is in the *outcome*, not the plumbing.

2. **Personality-driven intellectual friction** -- Existing multi-agent systems assign roles ("you are the researcher"). This system creates agents with genuine self-interest (positions), cognitive style (personalities), and reasoning methods (techniques) that produce *authentic disagreement* rather than performed debate. The 8-dimension personality model combined with stakeholder positions is novel.

3. **Three-layer approach to conversation quality:**
   - **Anti-slop (prevent bad defaults)** -- Explicitly engineers against 8 identified LLM failure modes (echo chamber, premature convergence, polite consensus, semantic drift, filler turns, role collapse) with 10 countermeasures. Treating "agents being too agreeable" as a bug to fix is uncommon.
   - **Creativity engine (make agents genuinely different)** -- Personality dimensions, stakeholder positions, and reasoning techniques create agents that think differently by construction, not just instruction.
   - **Conversation dynamics (actively provoke friction)** -- Challenge events, urgency meters, ego injection, and rebuttal priority actively create productive conflict that LLMs wouldn't produce on their own. Stretch agents beyond their default cooperative behavior. Simple foundation in V1, expandable to richer emotional simulation later.

4. **Idea-oriented agents as creative partners** -- Agents that propose features the user didn't ask for, then the team filters by feasibility and value. The system doesn't just document what you asked for -- it makes the product *better*. Combined with thorough user briefs, agents go deeper than the user would alone, finding the 20% that gets missed when you're too close to the idea.

5. **Self-directed product discovery (growth path)** -- V1 starts with user-provided questions in the brief. The path leads to agents generating their own design questions, interrogating the idea autonomously, and producing specs for a more complete product than the user originally imagined. The brief becomes a seed, not a script.

### Market Context & Competitive Landscape

- **CrewAI / AutoGen / LangGraph** -- Orchestration frameworks. User builds the workflow. No overnight-run product experience.
- **Devin / Claude Code / Cursor** -- Code generation from specs. Complementary, not competitive. This product feeds *into* these tools.
- **ChatGPT / Claude single-session** -- Can write specs but no internal debate, no multi-perspective pressure testing, no gap discovery. Quality ceiling is inherently lower.

### Validation Approach

Run 5 sessions on real product ideas where the user has domain knowledge. Compare output quality to specs the user would write manually. Measure: decisions the user hadn't considered, edge cases caught, feature proposals that survive review, time saved.

### Risk Mitigation

- **Risk:** Agents produce verbose, repetitive output rather than genuine novelty → **Mitigation:** Anti-slop mechanisms, agreement tax, personality-driven differentiation
- **Risk:** Output looks thorough but has hallucinated requirements → **Mitigation:** Morning Brief flags confidence levels; user reviews before handoff to coding agents
- **Risk:** Self-generated questions could be generic/obvious → **Mitigation:** Idea-oriented agents with domain-specific positions generate contextually relevant questions; anti-slop prevents boilerplate
- **Risk:** Conversation dynamics feel artificial → **Mitigation:** Start simple (challenge events, urgency meter), validate with real sessions, expand based on what actually produces better specs

## CLI Tool Specific Requirements

### Project-Type Overview

AgentTeamDiscussions is a scriptable Python CLI tool designed for unattended overnight execution. The user invokes a single command with an input brief, and the system produces a structured output folder. Configuration is file-based (YAML for agents, Markdown for briefs).

### Command Structure

```
python session_runner.py <brief.md> [--team <team.yaml>] [--eval] [--live [--port PORT]]
```

- `brief.md` -- Input brief with product idea and questions (required)
- `--team` -- Agent team configuration file (optional, defaults to `beta-agents.yaml`)
- `--eval` -- Run evaluation pass after session completes (optional)
- `--live` -- Launch with HTTP dashboard for real-time monitoring (default: headless/scriptable)
- `--port` -- Dashboard port (default: 8000)

**Two execution modes:**
1. **Headless (default)** -- Fire and forget. No UI. Output to session folder. The "overnight" mode.
2. **Live dashboard (`--live`)** -- Same execution, streams events to browser UI via SSE. Agent responses appear in real-time. The "development/tuning" mode. Read-only observation -- does not change execution.

Both modes produce identical session output.

### Output Structure

```
sessions/{timestamp}/
├── morning-brief.md          # Primary user artifact -- read this first
├── decisions.md              # Append-only decisions ledger
├── q01-{topic}/
│   ├── design-doc.md         # Synthesized design document
│   ├── round-1-propose.md    # Agent responses per round
│   ├── round-2-critique.md
│   └── round-3-evaluate.md
├── q02-{topic}/
│   └── ...
├── session-status.json       # Per-round completion tracking (updated after each round)
└── session-meta.json         # Timing, agent config used, completion status
```

### Configuration Schema

**Agent team config (YAML):**
- Agent definitions with personality traits (8 dimensions, 0.0-1.0 scale)
- Stakeholder positions with intensity
- Creativity techniques mapped to archetypes
- Cognitive actions with prompt directives and triggers (periodic, round-based, once-per-question)
- Anti-slop rules (agreement tax threshold, perspective enforcement flags)
- Anti-pattern lists per agent (8-12 forbidden phrases -- core feature, not optional)
- Voice constraints (vocabulary, brevity level)

**Input brief (Markdown):**
- Product description and context
- Already-decided constraints
- Open questions for discussion (V1: user-provided; future: agent-generated)

### Implementation Considerations

- **Python 3.9+** with no external dependencies beyond PyYAML and Pydantic
- **Claude CLI** (`claude -p`) via subprocess -- requires Claude Max subscription
- **Cross-platform** -- Windows (shell=True), macOS, Linux
- **No daemon, no server in headless mode** -- runs to completion and exits
- **Live dashboard** uses existing `live_session.py` infrastructure (SSE event streaming, embedded HTML/JS). Threading for HTTP server alongside conversation loop (already implemented in beta)
- **File-based state** -- all state in session folder, no database

## Project Scoping & Phased Development

### MVP Strategy & Philosophy

**MVP Approach:** Problem-solving MVP -- ship the smallest thing that produces specs better than a single AI conversation. Solo developer, personal use first.

**Resource Requirements:** Solo developer, ~30-40 hours to V1 (leveraging existing beta code). Claude Max subscription for runtime.

### Risk Mitigation Strategy

**Technical Risks:**
- Decision extraction quality (biggest risk) → Test with 5 real sessions, iterate on extraction prompt. Two-gate pipeline: JSON parse with retry, then field validation.
- Synthesis reliability (unknown failure rate) → Instrument failure modes. Log timeout vs malformed vs rate-limit separately. Target < 10% failure rate.

**Product Risks:**
- Output quality not meaningfully better than single Claude conversation → Compare side-by-side on same brief. If cognitive actions + anti-slop + multi-perspective don't produce gap discovery, the product doesn't justify its complexity.

**Resource Risks:**
- Scope creep beyond 30-40 hours → Strict MVP boundary. Defer everything not in must-have list. No magnitude system, no phase transitions, no research actions unless V1 core ships first.

## Functional Requirements

### Session Management

- FR1: User can start a new session by providing a brief file and optional team config via CLI
- FR2: User can run a session in headless mode (unattended, no UI) or live dashboard mode (real-time browser monitoring)
- FR3: System can execute a complete session across multiple questions without user intervention
- FR4: System can write session output to disk after every completed round (crash-safe)
- FR5: System can resume an interrupted session from the last completed question
- FR6: System can track per-round completion status in session_status.json
- FR7: System can cascade failures gracefully (skip failed rounds/questions, continue with remaining)
- FR8: User can review session output in a structured folder (Morning Brief, per-question design docs, transcripts, decisions ledger)

### Conversation Engine

- FR9: System can orchestrate a three-round discussion per question (propose, critique, evaluate)
- FR10: System can synthesize agent responses into a design document after each question's three rounds
- FR11: System can build agent context using a three-layer model (Identity, Situation, Task) within a token ceiling
- FR12: System can chain prior context across questions using a decisions ledger and previous design docs
- FR13: System can extract decisions from synthesis output into a structured ledger (decision, commitment level, confidence)
- FR14: System can detect and flag low-confidence or contested decisions
- FR15: System can detect agent consensus (majority agreeing stance for 2+ consecutive turns) and advance to synthesis early
- FR16: System can inject disruption prompts when premature consensus is detected before minimum turn threshold

### Agent Configuration

- FR17: User can define agents in YAML with personality traits (8 dimensions, 0.0-1.0 scale)
- FR18: User can assign stakeholder positions to agents (role, drives, intensity)
- FR19: User can assign creativity techniques to agents (primary reasoning method)
- FR20: User can define anti-pattern lists per agent (8-12 forbidden phrases)
- FR21: User can configure anti-slop rules per agent (agreement tax, perspective enforcement, uncomfortable idea quota)
- FR22: User can swap team configurations between sessions by specifying a different YAML file

### Cognitive Action System

- FR23: User can define cognitive actions in agent YAML with prompt directives
- FR24: System can evaluate action triggers per-turn (periodic, round-based, once-per-question)
- FR25: System can inject a maximum of one firing action into the Task layer before the base directive
- FR26: Agents can propose features, find flaws, challenge assumptions, or combine ideas based on injected action prompts

### Prompt Assembly

- FR27: System can build Identity layer prompts from agent YAML config (personality as lived experience, not directives)
- FR28: System can build Situation layer prompts with curated context (recent messages in full, older compressed)
- FR29: System can build Task layer prompts with forcing functions (concrete question or directive, never "continue the discussion")
- FR30: System can inject perspective reminders when agents show signs of role drift
- FR31: System can enforce output constraints per agent (word limits, format rules, anti-pattern compliance)

### Output & Artifacts

- FR32: System can generate a Morning Brief with four sections: confirmed decisions, flagged disagreements, open items, system alerts
- FR33: System can flag questions with low proposal divergence in the Morning Brief as potentially under-explored
- FR34: System can produce per-question design docs following a structured template (decision-with-rationale, exclusions, blocking/non-blocking open items)
- FR35: System can produce human-readable transcripts per question showing all agent responses per round
- FR36: System can write session metadata (timing, agent config used, completion status, question count)

### Input & Brief Format

- FR37: User can provide a product idea as a markdown brief with product description, constraints, and open questions
- FR38: System can parse brief files to extract individual questions for sequential discussion
- FR39: User can include already-decided constraints that agents must respect during discussion

### Live Dashboard (Development Mode)

- FR40: User can launch sessions with a live browser dashboard via `--live` flag
- FR41: System can stream agent responses and session events to the dashboard via SSE in real-time
- FR42: Dashboard displays agent responses as they occur without affecting session execution
- FR43: Both headless and live modes produce identical session output

### Agent Workshop - Core (Web UI)

- FR44: User can launch the Agent Workshop as a local web server (`python -m workshop` → `localhost:8420`) using FastAPI + htmx + Pico CSS with no npm or build step
- FR45: User can browse, search, filter, create, clone, and delete agents in a library view
- FR46: System assigns a GUID (UUID4) to each agent at creation as its stable, immutable identifier used in session output, group configs, and version history
- FR47: User can configure all agent dimensions via the editor: 8 personality sliders with live description rendering, position (drives/pushback/intensity), technique, anti-slop toggles, voice constraints, and output settings
- FR48: System renders a live system prompt preview with token count that updates on any config change (300ms debounce via htmx)
- FR49: System auto-saves agent configuration on change (2000ms debounce) with visual "Saving..."/"Saved" indicator

### Agent Workshop - Testing & Composition

- FR50: User can test a single agent with custom or preset prompts and view the response with word count and timing
- FR51: User can assemble agents into groups with round assignment (propose/critique/evaluate) and drag-to-reorder
- FR52: System displays group balance analysis: trait distribution, role coverage per round, anti-slop coverage, and cognitive diversity with warnings for gaps
- FR53: User can export a group as session-ready YAML identical to what the session runner accepts
- FR54: User can compare two agents (or two versions of the same agent) side-by-side with trait diffs and shared test prompt

### Agent Workshop - Generation & Import

- FR55: User can generate a complete agent config from a natural language description via AI
- FR56: User can import agents from existing YAML files (individual or team files parsed into separate library entries)
- FR57: System tracks version history per agent with timestamps, change notes, and revert to previous version

## Non-Functional Requirements

### Reliability

- NFR1: Sessions must complete 90%+ of questions without manual intervention on well-formed briefs
- NFR2: No data loss on crash -- all completed rounds persisted to disk before starting the next
- NFR3: Session resume must correctly identify the last completed question and continue without duplicating work
- NFR4: Individual question failures must not abort the entire session -- cascade rules skip and continue
- NFR5: Claude CLI timeout handling must retry once (120s timeout) before marking a call as failed

### Performance & Cost

- NFR6: Full 10-question session must complete within 8 hours (overnight window)
- NFR7: Per-question overhead (prompt assembly, disk writes, status tracking) must be < 5 seconds -- LLM call latency dominates, not orchestrator logic
- NFR8: Token usage per session should be trackable (log input/output token counts per call for cost awareness)
- NFR9: Cognitive action injection must add < 200 tokens to Task layer per turn

### Output Quality

- NFR10: Morning Brief must be < 300 words and readable in under 90 seconds
- NFR11: Design docs must follow the structured template (decision-with-rationale, exclusions section, open items) -- no free-form synthesis output
- NFR12: Decision extraction must achieve > 80% coverage of decisions present in synthesis text (validated manually on first 5 sessions)
- NFR13: Agent anti-pattern compliance must be measurable -- log instances of forbidden phrases per session for tuning

### Maintainability

- NFR14: Agent team configs must be fully declarative YAML -- no code changes required to modify agent behavior
- NFR15: Adding a new agent to a team requires only YAML editing, not orchestrator code changes
- NFR16: Action definitions must be YAML-configurable, not hardcoded in orchestrator

### Compatibility

- NFR17: Must run on Windows (primary dev environment) and macOS/Linux
- NFR18: Requires only Python 3.9+, PyYAML, and Pydantic as dependencies -- no compiled extensions
- NFR19: Requires Claude CLI on PATH with valid Claude Max subscription credentials
