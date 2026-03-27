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
