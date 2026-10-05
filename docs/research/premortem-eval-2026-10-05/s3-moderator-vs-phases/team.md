## What breaks

1. **A moderator directive and a phase's communication mode collide inside the same prompt, so "who wins" is decided by the model per turn, and silently.** moderator-input.md gives authority only through one system-prompt sentence ("address their point before continuing") and says context handling has "no special treatment". phase-dynamics.md injects YES-AND (Brainstorm, never critique) or ADVERSARIAL (Review) into that same prompt. A mid-Brainstorm "poke holes in this" either breaks the phase contract or is ignored, and nothing in the docs says which outcome is correct.

2. **The moderator spec describes an engine this project does not have, and a steering message will vanish at the round boundary.** The spec is written for `live_conversation.py` (shared history list, HTTP thread, queue checked between speakers). The C# engine runs fixed rounds of sequential `claude -p` calls, rebuilds each payload, and trims unprotected sections at ~10k tokens. Between rounds agents see only 3-sentence Position Summary blocks. The spec's own success criterion (the next agent addresses the point) is not guaranteed unless the message becomes a protected section, which nobody has designed.

3. **Phase auto-transitions cannot be built as specced, so they will fire on round count and override the human.** The exit gates (50+ Ideas, domain diversity, disagreement queue, agreement score) depend on the entity model, Weaver/BackgroundAgents and a validation gate. The engine facts say none of that exists, and the roadmap's own question (time, convergence or round count) is unanswered. The 2-3 day estimate covers labelling and prompt injection only. With only a clock available, a moderator saying "stay on this" loses to a trigger the user cannot see.

4. **A moderator action has no defined effect on a phase gate.** If the moderator pushes a Refine thread back toward divergence, the exit gate may never fire or may fire mid-correction. A "advance now" or "skip" request also has no home: the spec says the moderator is not a way to force conclusions, and the engine runs fixed rounds followed by one synthesis call, so skipping mid-round would leave the Position Summary chain half-written.

5. **Moderator input has no rule for the decisions ledger.** The ledger chains DECIDED / CONTESTED / OPEN lines forward, and was only first rendered on 2026-10-05, so there is no real data. The moderator spec says moderator messages are not agreement signals, but nothing says what synthesis does when a directive contradicts a DECIDED line.

6. **The boundary is being settled before either side exists, and the build order may leave it moot.** There is no phase system and no moderator channel in the running code. The ROADMAP critical path puts blind proposals first, phases third, and moderator input nowhere. Nothing reads Evaluator scores back, and sessions are occasional (17 on disk), so there is no way to tell whether either feature improved results. A solo developer risks writing an arbitration rule for a system nobody has exercised, or stalling on this question.

## Undecided

- Whether the moderator outranks phase gates, or is just another voice that a phase can hold against.
- Whether a moderator message can trigger, delay, pause, skip or reset a transition.
- Whether a moderator message is protected from budget trimming and whether it persists across rounds and phases or expires.
- Whether steering is real-time or queued to the next round boundary, given that a running `claude -p` turn cannot be interrupted.
- The single trigger for transitions (time, convergence or round count) and who may override it.
- Whether a human message counts as convergence evidence or as a disruption, and how it enters the decisions ledger.
- Which feature is built first, and what evidence would show either is worth keeping.

## Questions for you

- Do you actually steer sessions live, or do you mostly run them and read the finished output?
- If the moderator and the phase conflict, should the moderator always win?
- Should a moderator be able to force or block a phase transition?
- Should a moderator message be exempt from the ~10k-token budget trimming?
- If phase triggers must start with round count only, are you willing to ship that and call it auto-transition?
