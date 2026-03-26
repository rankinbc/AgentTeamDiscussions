# Discussion Brief: V1 Conversation System Design

## Project Summary
AgentTeamDiscussions is an autonomous multi-agent discussion system that converts
product ideas into implementation-ready specs overnight. Two AI teams communicate
through a message broker, each in their own context window, driven by a Python
orchestrator spawning `claude -p` CLI processes.

## What's Already Decided

1. **Context curation is hybrid** -- deterministic filtering first (drop old stuff, drop resolved ideas), then LLM curator call for personalized summary. LLM adds valuable randomness/unexpectedness.

2. **Magnitude is the core mechanic** -- ideas and stances have numeric values that rise and fall based on discussion, research, BackgroundAgent intervention, and between-round team talk.

3. **Archival threshold is persona-dependent** -- stubborn agents hold ideas longer (lower threshold before conceding), flexible agents drop faster.

4. **BackgroundAgents are "angels"** -- they don't speak to DiscussionAgents. They analyze history and directly manipulate agent stats (bump idea magnitude, plant new ideas, shift stances). Some modify what agents "know," others just tweak values.

5. **BackgroundAgents can plant ideas** -- analyze unresolved disagreements, synthesize answers, inject as new Ideas into an agent's state. Agent surfaces it next round as if they thought of it.

6. **Rounds don't continue seamlessly** -- there's a reset with drift/evolution. Previously hot topics may not be top of agenda. Agents get pushed off stale topics.

7. **Discussion and DiscussionRound have their own state** -- this state changes and influences conversation direction, and the conversation affects it back. Bidirectional.

8. **Intra-team talk happens between rounds** -- agents talk to teammates, good ideas increase magnitude, bad ideas decrease. This shapes what they care about going into the next round.

9. **Random event system** -- "dream events" and similar mechanics that unpredictably shift agent stances. Anti-predictability feature.

10. **Agent "save file" between rounds** -- current ideas with magnitudes, current stances with magnitudes, decisions committed to, 3-5 sentence personalized summary of "what happened last round from your perspective."

11. **Three thinking routines for V1** -- Reflect (review ideas/stances against what happened, adjust magnitudes), Research (spawn focused research call, return with new info), Strategize (consider what to push for next round given team goals).

12. **Context budget split** -- Identity ~2k tokens (static), Situation ~8-15k tokens (curated), Task ~1-2k tokens (specific question), Remaining ~80k+ for agent thinking and response.

## Open Questions for This Session

1. **How does a round begin after a reset?** What information does the orchestrator assemble, what does the first prompt look like, and how does it differ from mid-round turns?

2. **What's the difference between a "round" and a "turn"?** Define the exact boundary -- when does a round end, when does a turn end, and what happens in between each?

3. **What's in the Discussion and DiscussionRound state?** Name the specific fields, what updates them, and how they influence what agents see in their context.

4. **How does the "agenda" emerge?** Is it a literal agenda object the orchestrator builds from magnitudes, or emergent from what agents choose to talk about? What are the tradeoffs?

5. **How does intra-team discussion differ from cross-team mechanically?** Same prompt format? Different context? How does it feed back into the next round?

6. **Who/what decides what goes into the Situation layer each turn?** Walk through the exact flow: what sources are consulted, what filtering happens, and what the agent actually sees.

7. **How much between-round output feeds back into next turn's context?** After thinking routines, intra-team talk, and BackgroundAgent modifications -- what percentage of that makes it into the next prompt?

8. **Are between-round activities separate `claude -p` calls per agent?** If so, how many calls per agent per round, and what's the total token budget for between-round work?

9. **What controls research task scope?** When an agent spawns a research sub-call, what determines the scope -- token cap, word limit, time limit, or something else?

10. **How do artifacts (specs, PRDs) actually get created?** Does an agent draft them inline? Is there a dedicated artifact-creation call? Who decides "this is ready to write down"?

## Expected Output
- For each question: a concrete, implementable answer
- No code -- describe behavior, rules, data flow, and decisions
- Name specific tradeoffs and state which side you come down on
- If a question cannot be answered, say exactly what information is missing

## Constraints
- 250 words max per response
- Stay at requirements/design level
- Reference existing decisions when relevant
