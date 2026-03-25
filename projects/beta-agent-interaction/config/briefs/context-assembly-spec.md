# Discussion Brief: Agent Context Assembly -- What Goes In The Prompt

## Project Summary

AgentTeamDiscussions agents are stateless -- each turn is a fresh `claude -p` call where all context must be explicitly reconstructed. The orchestrator builds two inputs per turn: a system prompt (agent identity, personality, role -- static across the session) and a user payload (everything else -- rebuilt every turn).

We now have three specs that inject content into the user payload: the existing turn anatomy (conversation history + perspective reminder), the Key Takeaway mechanism (takeaway block + tombstones), and the orchestrator event cadence (disruption injections, dropped-thread callbacks, phase briefings). Nobody has specified how these pieces compose into a single prompt, what the priority order is when context budget is tight, or what gets cut first.

## What Currently Goes In The User Payload

Today the payload is assembled in this order:
1. Perspective reminder (agent identity reinforcement, ~50 tokens)
2. Ego/challenger injection if applicable (~30 tokens)
3. The original question (~50 tokens)
4. Compressed older messages (first sentence only, last 10, ~300 tokens)
5. Recent messages verbatim (last 7, ~1400 tokens)
6. Moderator priority framing if applicable (~50 tokens)
7. Task instruction ("respond to what was said, stay on topic", ~50 tokens)

Total: roughly 1900 tokens on a typical turn with 20 messages in history.

## What Needs To Be Added

From the Key Takeaway spec:
- Confirmed takeaways block (~50-100 tokens per takeaway)
- Tombstones with killing blows (~50 tokens per tombstone)
- Dissent text fetch for contested takeaways (on-demand, ~200 tokens when triggered)

From the orchestrator cadence spec:
- Disruption injection content when stagnation is detected (~100 tokens)
- Phase briefing after phase transition (~500 tokens)
- Dropped-thread callbacks (~100 tokens per callback)

From the existing signal spec:
- Structured output format for agent signals (stance, confidence, ready_to_advance, key_claim)

## Open Questions For This Session

1. **What is the assembly order?** When all these pieces are present, what order do they appear in the payload? The order matters because LLMs attend more strongly to content at the beginning and end of context. What goes first? What goes last? What goes in the middle where it's most likely to be overlooked?

2. **What is the priority hierarchy when context is tight?** On a long session where context budget is stressed, what gets compressed first, what gets cut entirely, and what is protected? Should takeaways be protected over recent messages? Should the question restatement always be present? Should tombstones age out?

3. **How should the "context lens" interact with the takeaway block?** The existing context lens (from prompt_builder.py) tells each agent what to focus on based on their role. Should the lens also frame which takeaways are most relevant to this agent's perspective? Should an adversarial agent see tombstones more prominently than confirmed takeaways?

4. **What structured output format should agents produce?** The signal spec defines stance, confidence, ready_to_advance, key_claim. The takeaway mechanism needs agents to be able to propose takeaways alongside their message. How should the agent's response be structured to carry both prose and metadata without making the output feel robotic or breaking the conversational flow?

5. **How do phase briefings replace conversation history?** At phase transition, the model synthesis produces a promoted summary. Does that summary REPLACE all prior conversation history in the next phase's context, or does it SIT ALONGSIDE compressed history? If it replaces, how much context does phase two lose?

6. **What does the moderator's injection look like in context relative to everything else?** Currently moderator messages get priority framing ("IMPORTANT: The MODERATOR just spoke..."). With all the new content in the payload, where does the moderator injection sit and how does it avoid being drowned out?

7. **What is the maximum token budget for the user payload?** The system prompt is ~2K tokens (personality, role, anti-slop rules). Claude's context window is 200K. The agent needs room to think and respond (~1-2K tokens). What's the practical ceiling for the user payload, and what's the target to leave headroom?

## Constraints

- 250 words max per response
- Stay at requirements/design level -- describe what goes where and why, not code
- Token costs matter: every token in the payload is a token the agent reads on every turn
- Reference the existing specs (turn-anatomy, key-takeaway-mechanism, orchestrator-event-cadence) when relevant
- The system runs via stateless CLI calls -- nothing persists between turns except what the orchestrator explicitly reconstructs
