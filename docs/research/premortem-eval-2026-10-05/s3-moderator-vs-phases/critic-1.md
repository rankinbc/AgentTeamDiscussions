1. **The question is being answered before anything it governs exists.** The engine facts say there is no phase system, no moderator channel, and no live synthesis. The ROADMAP open question asks who wins a conflict between two unbuilt things. Three months in, the boundary was written into a spec, then the phase system shipped without the moderator hook and the spec rotted. Nobody has said which one is built first.

2. **The moderator spec describes a loop this engine does not have.** moderator-input.md is written for `live_conversation.py`: a shared history list, an HTTP thread, and a queue checked between speakers. The C# engine shells out to `claude -p` per turn. Each turn gets a rebuilt payload trimmed by a budget enforcer at about 10k tokens. The spec says moderator messages "compress like any other." Between rounds, agents only see 3-sentence Position Summaries. So a steering message is trimmed or lost the moment the round ends. That contradicts the spec's own success criterion that the next agent addresses it. Nobody has decided whether the moderator message is a protected section.

3. **"Priority directive" in a system prompt collides with phase-specific communication modes.** phase-dynamics.md has Brainstorm as "never critique" and Review as "it's fine is not acceptable". The moderator spec tells every agent to address the moderator first. A moderator saying "challenge this" during Brainstorm gets one of two outcomes. The agents obey and break the phase contract, or they ignore it and the moderator learns steering is decorative. The documents never say which wins. A prompt-level conflict has no deterministic referee.

4. **Phase exit gates are unmeasurable, so auto-transitions will never fire or will fire randomly.** Gates such as "50+ Ideas," "domain diversity threshold," and "disagreement queue below threshold" depend on the entity model, which is Vision-tier and unbuilt. The ledger only began rendering on 2026-10-05, so there is no real data to calibrate any threshold. The ROADMAP's own open question ("time, convergence, or round-count?") is unanswered. A moderator override is meaningless without a defined transition trigger to override.

5. **A moderator "force transition" would break the fixed-rounds model.** Sessions run fixed rounds per question, followed by one synthesis call. Skipping a phase mid-round leaves the Position Summary chain and decisions ledger half-written. The moderator spec forbids forcing conclusions, which leaves "advance now" with no home.

6. **A solo developer who runs sessions occasionally will not build live steering, and the whole V2 effort will stall on this question.** The critical path puts blind proposals first and phases at 2-3 days. The moderator feature is not on that path at all.

**Only the author can answer:**
- Who wins on conflict: moderator or phase? Is there a veto?
- Can the moderator trigger, delay, or skip a transition?
- Is a moderator message protected from budget trimming?
- Do you actually steer live, or do you only read finished sessions?
