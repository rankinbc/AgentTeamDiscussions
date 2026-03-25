# Discussion Brief: Key Takeaway Mechanism for the Conversation Engine

## Project Summary

AgentTeamDiscussions is a multi-agent conversation system where 3-7 AI agents debate design questions. The system currently tracks challenges (agent-to-agent disagreements) and urgency (rebuttal priority), but has no mechanism for recording when agents reach productive conclusions. A human observer cannot tell what was decided without post-hoc analysis.

## The Problem We Just Observed

A 25-turn conversation with 5 agents produced genuinely productive debate. But:

- At least 5-6 clear convergence moments were buried in prose and never formalized
- An agent conceded a key point around turn 8 but nobody recorded it
- The group agreed on "progression topology" as a key missing concept but it was never captured as a decision
- By turn 20, agents were re-deriving conclusions they had already reached because those conclusions were not in their context
- A human had to manually extract the takeaways after the conversation ended
- The agents themselves did not know what they had agreed on

This is the core problem: **the conversation engine has no mechanism for recognizing, recording, or acting on productive conclusions as they happen.**

## The Proposed Mechanism: Key Takeaways

### Core Idea

Alongside the existing conversation flow, agents can propose, vote on, and maintain a set of "Key Takeaways" -- confirmed conclusions that become part of the shared conversation state. This is a parallel action system, not a replacement for the conversation.

### Lifecycle

1. **Proposal** -- An agent recognizes convergence and proposes a Key Takeaway as a discrete action alongside their regular message. The proposal is a concise statement of what was concluded.

2. **Voting** -- All other agents vote on the proposal using a 0-10 scale (0 = strongly disagree, 10 = strongly agree) plus a brief reason. This happens in a lightweight side-channel -- not as conversation turns, but as a separate action with abbreviated context (just the takeaway statement and recent relevant exchanges, not full history).

3. **Confirmation** -- If the vote meets a threshold (e.g., average >= 7, no score below 3), the takeaway becomes "confirmed" and enters the shared state. If it fails, the disagreement reasons feed back into the conversation as new context.

4. **Context Compression** -- Once a takeaway is confirmed, the conversation history that led to it can be compacted. The takeaway statement replaces the 5-8 turns of argument that produced it. This frees context budget for new discussion.

5. **Per-Turn Re-evaluation** -- Each turn, every agent evaluates their current "magnitude" (0-10 feeling of truth) on each active Key Takeaway. This is part of their turn state, not a separate action.

6. **Challenge Trigger** -- If an agent's magnitude on a takeaway drops below a threshold (e.g., below 3), they get urgency boost to challenge it. If they mildly disagree (e.g., magnitude 4-5) they will not bring it up again unprompted.

7. **Topic Steering** -- When a new takeaway is confirmed, agents can propose the next sub-topic that needs discussion. This provides natural conversation flow rather than circular re-hashing.

8. **Removal** -- Agents can propose that a takeaway be removed or revised, triggering the same voting process.

## What Already Exists in the System

### Current Agent State (per turn)
- Speaking order determined by urgency meter
- Challenge detection: named disagreements between agents (e.g., "Game Designer challenged Pipeline Pragmatist")
- Urgency: agents who were challenged get rebuttal priority
- Context: last 7 messages verbatim, older messages compressed to first sentence
- Perspective reminder: agent identity/role injected each turn

### Current Data Flow
- Each agent gets: system prompt (personality/role) + user payload (conversation context + question)
- System prompt is static across the conversation (built from YAML config)
- User payload is rebuilt each turn with compressed older messages + recent verbatim messages
- Agents are stateless between turns -- all state must be reconstructed from conversation history

### What This Means for Key Takeaways
- Takeaway state must be explicitly injected into each agent's context each turn (agents cannot "remember" takeaways)
- The voting side-channel requires additional claude -p calls beyond the main conversation turns
- Context compression of confirmed takeaways directly reduces token usage on subsequent turns
- The magnitude re-evaluation could be part of the agent's response format (structured output alongside their message)

## Open Questions for This Session

1. **When should an agent propose a Key Takeaway?** What signals indicate convergence versus premature closure? Should the proposal trigger be in the agent's instructions, or should a background process detect convergence and prompt agents to formalize? What prevents agents from proposing takeaways too early (before genuine debate) or too late (after the conversation has moved on)?

2. **How should the voting mechanism work?** Should voting happen as separate claude -p calls with abbreviated context, or inline with the next conversation turn? What context does each voter need to cast a meaningful vote -- just the takeaway statement, or the takeaway plus the exchange that produced it? How do we prevent the voting process from being token-expensive while still being meaningful?

3. **What should the confirmation threshold be?** Average score >= 7? No score below 3? Unanimous above 5? Should the threshold vary based on the number of agents? What happens to a takeaway that scores 6.5 -- close but not confirmed? Is there a "contested" state between confirmed and rejected?

4. **How should confirmed takeaways affect context?** Should the conversation history that led to a takeaway be fully replaced by the takeaway statement, partially compressed, or kept but de-prioritized? How much context does a takeaway statement need to be useful on its own -- just the conclusion, or the conclusion plus the key supporting argument? What happens when a later discussion invalidates an assumption that a confirmed takeaway relied on?

5. **How should per-turn magnitude re-evaluation work?** Should agents evaluate all takeaways every turn (expensive), or only when prompted by relevance? How does the magnitude score get into the agent's response -- as a structured output format, a separate call, or embedded in their message? What should the system do with magnitude data -- just store it, or actively use it to steer the conversation?

6. **How should takeaways interact with the existing challenge/urgency system?** When an agent's magnitude on a takeaway drops, should it boost their urgency the same way a direct challenge does? Should proposing a takeaway consume a turn, or be a free action alongside a regular message? Can a challenged agent defend by citing a confirmed takeaway?

7. **What are the failure modes?** Agents rubber-stamping every proposal to avoid conflict (the anti-slop problem applied to voting). Agents gaming the system by proposing obvious statements to "win" confirmation. Premature compression losing context that turns out to be needed later. Magnitude re-evaluation becoming performative (agents always scoring 7-8 on everything). The voting side-channel becoming more expensive than the conversation itself.

8. **What artifacts should this produce?** At the end of a conversation, what does the Key Takeaway record look like? Should it include the vote scores, the magnitude trajectory over time, which agents proposed and which contested? How does this feed into the Morning Brief or post-session summary?

## Constraints

- 250 words max per response
- Stay at requirements/design level -- describe behavior, rules, and data flow, not code
- Reference the existing system mechanics (challenges, urgency, context compression) when relevant
- Name specific failure modes and how to prevent them
- The system runs via stateless claude -p CLI calls -- agents cannot remember between turns without explicit context injection
- Token budget matters: every voting call costs real money and time
- The goal is to make productive conclusions visible in real-time, not just in post-hoc analysis

## Context from the Observed Conversation

The conversation that revealed this problem had these characteristics:
- 5 agents, 25 turns, chat mode
- Multiple clear convergence moments that were never captured
- The Pipeline Pragmatist conceded on citation verification (turn ~8) but this was never formalized
- "Progression topology as missing data layer" emerged as consensus across turns 4-9 but was never confirmed
- By turn 15, agents were re-deriving conclusions from turns 6-8 because those conclusions were not in context
- A human post-hoc analysis extracted 7 confirmed takeaways, 3 unresolved disagreements, and a prioritized action list -- none of which the system itself produced
- The synthesis feature (rolling summary) failed to parse in all 3 attempts, producing no usable output
- Even if synthesis had worked, it would have been a summary, not a set of confirmed decisions with agent buy-in
