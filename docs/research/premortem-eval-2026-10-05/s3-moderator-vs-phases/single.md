## What breaks

1. **Moderator messages are silently lost at the first round boundary, so steering "works" for one speaker and then evaporates.** The spec says moderator input gets "no special treatment in context compression" (moderator-input.md), but in this engine agents see only 3-sentence Position Summaries from earlier rounds, and the budget enforcer trims unprotected sections over ~10k tokens (engine facts). An instruction typed in "propose" never reaches "critique" or synthesis unless it is promoted to a protected section or the decisions ledger, and the spec never asks for that.

2. **The phase exit gates cannot be evaluated, so "automatic transitions" turn into fixed round counts and the boundary question goes away.** Gates like "50+ Ideas, domain diversity threshold", "all major Ideas challenged" and "Builder confirms implementable" (phase-dynamics.md) need Idea tracking and convergence detection that do not exist. The roadmap still lists the trigger as an open question. What gets built is the existing propose→critique→evaluate mode under new names, and the moderator becomes the only real transition trigger, done by hand.

3. **Phase mode and moderator authority give opposite instructions in the same prompt, and nothing says which one wins.** Brainstorm requires "YES-AND, never critique". The moderator is "a priority directive" that agents should "address before continuing", but they "can disagree". A moderator saying "tear apart idea 3" during brainstorm gets whatever the LLM picks for each turn.

4. **The moderator spec is written for a Python runtime that no longer exists.** It edits `live_conversation.py`, uses the GIL, `history.append` and `CONVERSATION_SYSTEM`. The engine is C# and runs a sequential `claude -p` subprocess per turn, with no input channel (engine facts). The port requires a new control channel into the round loop and a new context section for "moderator", plus rules for timing.

5. **Timing races put moderator messages in the wrong phase.** Each turn is a blocking subprocess call that takes tens of seconds, so the moderator reacts to output that is already stale. A message queued at the end of brainstorm gets injected into the first turn of refine, after the communication mode has changed (phase-dynamics.md, transition step 4). Neither document says whether queued messages are dropped, carried over or re-framed when the phase changes.

6. **Half of the phase transition procedure depends on Vision-tier pieces, so the 2-3 day estimate fails.** The procedure relies on the Weaver BackgroundAgent, AgentMinds, Idea magnitudes, bench rotation and the Muse (phase-dynamics.md). The roadmap places the entity model and BackgroundAgents in "Vision (Post-V2)".

7. **Nobody can tell whether either feature helped.** Evaluator scores are never read back, and the ledger has only been real since 2026-10-05 (engine facts). With 17 sessions run occasionally, there is no baseline for comparing steered and unsteered runs, or phased and fixed-round runs. The feature gets dropped because nobody can see what it changed.

## Undecided

- Precedence: does a moderator message override the current phase's communication mode, or does it work inside it?
- Can the moderator force, veto or delay a phase transition? Do transitions wait for an "ok" from the moderator?
- Do transitions happen only at round boundaries, or mid-round?
- How long a moderator message lasts: one turn, the rest of the round, the rest of the question, or entered into the decisions ledger and synthesis?
- What happens to queued messages when the phase changes?
- Are phases a replacement for modes or a layer above them? Does a phase span one question or several?
- What should an unattended run do? Should auto-transitions only be active when no moderator is connected?

## Questions for you

- Do you actually watch sessions live often enough for in-run steering to beat editing the brief and rerunning?
- In your last sessions, what would you have typed as moderator, and would it have been a topic redirect or "move on to the next phase"?
- When you as moderator disagree with an automatic transition, should the system obey you without asking or push back?
- Is the Python `live_conversation.py` spec still the intended design, or should it be rewritten against the C# round loop?
- Should a moderator directive become a DECIDED/CONTESTED entry that chains to later questions?
