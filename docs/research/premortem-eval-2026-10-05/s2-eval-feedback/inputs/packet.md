# Pre-mortem subject: How does the evaluation engine feed back into agent behavior for subsequent sessions?

The roadmap lists an Evaluation Engine (rubric scoring of design docs). Open question: how should evaluation results change agent behavior in later sessions?

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

# Source document: docs/v1/v1-spec-gaps.md

# V1 Orchestrator Spec Gaps

An adversarial review of the V1 orchestrator spec found 13 issues. These are the top 7 that need design decisions before implementation.

## What's Already Decided

- V1 is a single-team, single-phase discussion system (no MCP, no two-team, no BackgroundAgents, no magnitude)
- Agents are configured via YAML and invoked as stateless `claude -p` CLI calls
- Structured 3-round discussions: propose -> critique -> evaluate -> synthesize
- Session output goes to a timestamped folder with design docs, transcripts, decisions, and a Morning Brief
- The beta experiment system (run_discussion.py) has the working orchestration loop
- Each question produces: a design doc, a transcript, extracted decisions, and extracted open questions
- Prior design docs chain forward as context for subsequent questions
- The evaluator (evaluate_experiment.py) scores output on behavioral and quality dimensions

## Open Questions

1. **How does the Morning Brief get generated?** The Morning Brief is the only artifact the user actually reads. It needs a specific prompt, input strategy (what if 10 design docs exceed context?), output format, and a way to surface risk flags from critic rounds. Design the prompt, the input assembly, and the fallback if the call fails. Consider: should the brief be generated incrementally (after each question) or all-at-once at the end?

2. **How does decision extraction work?** Design docs are free-form markdown from an LLM synthesis call. We need to extract structured decisions with confidence scores into decisions.json. What prompt extracts decisions? What schema does decisions.json follow? How does the extractor distinguish a firm decision from a recommendation from a suggestion? What happens when the extractor produces garbage?

3. **What is the error handling strategy?** A 10-question session makes 70+ LLM calls. Failures are guaranteed. Design the failure strategy: what gets retried, what gets skipped, what gets saved on partial failure. If question 6 of 10 fails, do we skip it and continue? Do we save the partial transcript? What does the Morning Brief say about failed questions? What if synthesis fails but all rounds succeeded?

4. **How do we keep the synthesis step from being a bottleneck?** The synthesis call receives all agent responses (potentially 9000+ words) plus prior context and must produce a coherent design doc. In beta, this is the slowest and most failure-prone step. How do we make it more reliable? Options: chunk the input, use a two-pass approach (outline then fill), add a retry with simplified input on failure, or accept degraded output over no output.

5. **How does prior context get managed as questions accumulate?** By question 8 of 10, there are 7 prior design docs. The beta system truncates to 6000 chars. What is the right strategy? Summarize prior docs into a compressed context? Keep only decisions and open questions? Use a sliding window? The answer affects whether later questions build coherently on earlier ones or drift.

6. **What does session recovery look like?** If the process crashes at question 5 of 10, what state is on disk? Can the user restart and pick up at question 6? What file marks progress? What does the Morning Brief say about incomplete sessions? Design the checkpoint strategy.

7. **How do we make the evaluation feedback loop reliable?** The evaluator currently lets the LLM invent its own scoring dimensions instead of using the specified ones. Scores are not comparable across runs. How do we fix this so the iterate-and-improve loop actually works? Should we post-process LLM responses to extract scores by expected dimension names? Use a different evaluation approach entirely?

---

# Source document: docs/v2/ideas/agent-behavior-philosophy.md

# Agent Behavior Mechanisms

*Findings from live agent conversations (2026-03-18) + design direction from Brian*

## Context

Two 72-turn live conversations explored whether agents should track ideas and stances as structured data, and whether magnitude scores should be self-reported or computed from behavior. The agents produced architectural conclusions, but some were corrected by Brian based on the actual project goal: producing useful overnight specs, not performed disagreement.

## What the Agents Concluded

### Ideas and Stances (Conversation 1)

The agents proposed a "Behavioral Prescription Pipeline" -- forced assignments where the orchestrator tells each agent what to steelman and what to attack, round-robin across ideas, with phase-varying templates (Brainstorm: build/mutate, Refine: steelman/attack, Specify: pin down/find gap, Review: find fatal flaw/defend).

Key distinction articulated: "thermostat vs diary" -- the system should prescribe behavior rather than describe internal state.

### Magnitude Scoring (Conversation 2)

The agents unanimously killed self-reported conviction scores. Their reasoning: LLMs across stateless CLI calls cannot reliably introspect on conviction. Feeding an agent its own previous scores produces confabulation, not introspection.

They proposed behavioral scoring instead: track defenses vs drops through explicit retraction signals ("I retract: [claim X]"), with the Curator detecting these at phase-end. Absence of retractions itself signals potential consensus drift.

The group also concluded that semantic claim identity (determining whether two statements reference the "same" idea) is unsolvable cheaply, and should be handled through agent-assigned claim tags at emission time rather than post-hoc classification.

## Brian's Design Corrections

The agents debated the wrong framing on several points:

### Private Inventory, Not System-Reported Scores

Brian's vision: each agent has a private inventory of ideas with magnitudes, visible only to that agent. The agent consults this inventory when deciding what to talk about. This is not self-reporting scores to the system for validation -- it's private state that shapes what the agent chooses to say. The system instructs the agent to "review your ideas and decide what matters most right now."

### Forced Disagreement Kills Genuine Discourse

Telling agents "you must attack X" produces theatrical opposition, not genuine intellectual friction. The goal is agents who actually develop different perspectives based on their personality, expertise, and idea inventory -- not agents performing assigned debate roles. The test: does the Morning Brief contain ideas the user hadn't considered, or just arguments that were structurally guaranteed to happen?

### Simulated Ego

LLMs can't have real egos, but the behavioral effects could be simulated to produce natural divergence:

- When challenged, a high-ego agent should get defensive and push back harder
- Being called wrong should make them more committed, not less
- They should take it personally when their ideas are dismissed
- This naturally breaks consensus because ego-driven agents resist convergence

This is distinct from stubbornness (whether they change their mind) -- ego is about the emotional response to being challenged. A stubborn agent holds their position quietly. An ego-driven agent fights back.

Potential implementation: personality trait (ego/pride 0-1). When the system detects an agent was directly challenged, inject defensive framing into their next prompt scaled by their ego trait.

### Dynamic Turn Order

Instead of fixed sequential speaking order:

- If Agent3 directly challenges Agent2, Agent2 should speak next (rebuttal priority)
- This creates natural back-and-forth confrontations
- Other agents queue behind the rebuttal
- Detection: simple text matching -- if an agent's response names or references another agent's specific claim

Why: Round-robin produces polite serial monologues. Reactive ordering produces arguments. Arguments produce better specs because they force ideas to survive real pressure.

## Conversation 3 Findings (2026-03-18, 90 turns)

Agents debated all four mechanisms (ego, competition, urgency meter, live evaluator). They ironically demonstrated the drift problem by spending 15 turns speccing a FAILED.md error format instead of answering the question. The Product Oracle caught it at turn 13.

Key finding: agents are great at infrastructure design but terrible at examining their own limitations. They unanimously said "none of these change my behavior, they change my framing" -- which is itself the consensus-trained response the mechanisms are meant to break.

The agents produced useful work on observable drift infrastructure (structured position declarations, declaration-vs-body mismatch detection, evaluator with thread-header-plus-recent-window scoping) but never addressed the core question of how to make themselves genuinely diverge.

Source: `sessions/conversations/2026-03-18_1611_conversation.md`

## Two Separate Problems (Brian's insight)

The agents and the design conversations kept conflating two different problems:

### Problem 1: Position Persistence (solved by private inventory)

How do agents maintain their own positions across turns and context resets?

Brian's design: each agent has a private inventory of ideas/stances with magnitudes, stored in their own file, injected fresh every turn. The conversation history gets compressed by a separate summary model, but the agent's inventory is preserved independently. Even if the summary drifts toward harmony, the agent's high-magnitude ideas pull them back.

This is NOT self-reported scores for the system to validate. It's private state that shapes what the agent chooses to talk about. The system instructs the agent to consult their inventory, not to report it.

The inventory weighs as heavily in context as the conversation summary. This is the key: the agent's own positions are as prominent as what everyone else said.

### Problem 2: Conversation Dynamics (needs outside influence + behavioral mechanisms)

How do agents actually engage with each other in ways that produce useful friction?

This is where ego simulation, urgency meters, competition, and the live evaluator come in. These mechanisms control WHO speaks WHEN and HOW the conversation flows -- not what positions agents hold.

The agents' conclusion that "nothing changes our behavior" may be wrong. They haven't been tested with:
- Ego framing that makes challenges feel personal
- Competition that rewards originality over agreement
- Urgency that gives challenged agents rebuttal priority
- Context that's controlled enough that they can't just drift

Both problems need to be solved. Private inventory handles persistence. Behavioral mechanisms handle dynamics. Conflating them is why the agents kept going in circles.

## Design Principles (from all sources)

1. **Genuine friction over theatrical opposition** -- mechanisms should produce agents who actually think differently, not agents performing assigned disagreement roles
2. **Private state shapes behavior** -- agents should have internal state (ideas, stances, magnitudes) that influences what they choose to say, without the system second-guessing their self-assessment
3. **Emotional simulation drives divergence** -- simulated ego, defensiveness, and pride break consensus more naturally than forced role assignments
4. **Reactive dynamics over static structure** -- turn order, speaking priority, and confrontation patterns should emerge from what agents actually say, not from pre-assigned sequences
5. **The Morning Brief test** -- every mechanism must produce output that makes the solo builder's morning read more useful, not just more dramatic

## Urgency Meter (Speaking Priority System)

Each agent has a meter that slowly grows over time (while they're listening). When the meter hits a threshold, it's their turn to speak. But crucially:

- **When another agent contradicts you or disagrees with your stance, your meter jumps significantly**
- This makes it more likely that small disagreements escalate into bigger ones -- if Agent A challenges Agent B, Agent B's meter spikes and they get to respond quickly, which may provoke Agent A again
- Two agents "going at it" naturally emerges because their meters keep spiking each other
- Other agents with lower urgency wait until the confrontation cools down or their own meters naturally fill
- The meter is real system state that affects turn order -- not decorative

This replaces fixed round-robin AND simple assertiveness-based ordering with something that produces natural conversation dynamics: heated exchanges between disagreeing agents, with others chiming in when there's a natural pause.

## Simulating Ego and Emotion (Design Challenge)

The core problem: LLMs default to polite, measured, professional responses. We need agents that genuinely pull away from each other without the system cheating by forcing them to disagree.

### What we need to figure out:
- How do you make an LLM behave as if it has an ego -- getting defensive, taking challenges personally, fighting harder when called wrong?
- How do you simulate emotional responses (frustration, excitement, pride) that actually change what the agent says next?
- How do you make agents drive each other apart ORGANICALLY rather than through system-level forced assignments?
- The mechanism must make agents themselves want to diverge, not have the orchestrator tell them to diverge

### Competition/Points System (Brian's idea)
- Frame the agent's primary objective as "get the most points"
- Points for having good ideas that start discussions
- Points for defending your idea against a challenge and surviving
- Points LOST for agreeing without adding anything new
- Leaderboard visible to all agents to drive competitive behavior
- Key question: does competition produce genuine divergence, or just artificial contrarianism?
- Who awards the points? Self-awarded = gaming. System-awarded = back to forced mechanisms. Other-agent-awarded = social dynamics.

### Live Evaluator Agent (Brian's idea)
- A background agent that watches the conversation in real time
- Scores each comment on contribution quality (new idea, built on something, empty agreement, challenge)
- Tracks "current consensus" -- rolling average of last ~5 messages showing convergence/divergence
- Maintains a live decision tracker (tentatively decided vs still contested)
- This is a real system component that reads actual conversation, not post-hoc analysis
- Agents could see the consensus tracker -- if they see convergence, competitive agents might push back harder
- Produces the "Decisions Made" output from the original structured system but as a live evolving view

### Constraint:
Whatever we build must produce better SPECS, not just better arguments. The ego/emotion simulation is only valuable if it leads to ideas and perspectives the user wouldn't have reached alone.

## Open Questions

- Can ego simulation actually be implemented effectively through prompt engineering, or does it require structured state tracking?
- What's the right balance between private idea inventory (which requires context budget) and conversation history (which also requires context budget)?
- How does the urgency meter interact with the context window limit?
- Does the "challenged" detection need semantic understanding, or can simple name-mention + negative sentiment patterns work?
- How do we prevent ego simulation from making conversations unproductive (pure fighting with no resolution)?

## Source Transcripts

- `sessions/conversations/2026-03-18_1439_conversation.md` -- 72 turns on idea/stance tracking
- `sessions/conversations/2026-03-18_1509_conversation.md` -- 72 turns on self-reported vs behavioral scoring
