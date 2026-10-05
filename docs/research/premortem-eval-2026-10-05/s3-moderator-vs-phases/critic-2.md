1. **The question is answered by the wrong layer: a moderator message is just another transcript line, so "who wins" is decided by whichever prompt text the LLM happens to weigh more.** The moderator spec says authority comes only from a system-prompt sentence, with "no special treatment" in context handling. Phase specs inject a communication mode (YES-AND vs CHALLENGE vs ADVERSARIAL) into the same prompt. A mid-Brainstorm "poke holes in this" collides with "never critique", and at 3 AM nobody can say which instruction won. In practice this means conflict is resolved non-deterministically per turn, and it fails silently.

2. **The moderator spec is written for a different engine and does not map onto this one.** It describes live_conversation.py, a shared history list, a thread-safe queue checked between agent turns, and SSE. The real engine runs fixed rounds of sequential `claude -p` calls, and between rounds agents see only 3-sentence Position Summary blocks. A moderator line injected into "history" either vanishes at the round boundary (trimmed by the ~10k budget enforcer or lost in summarisation) or must be made a protected section, which nobody has designed. The failure mode is a steering message that agents never see after the current round.

3. **The phase system's trigger conditions are all undecided, so auto-transitions cannot be built.** The ROADMAP's own open question asks time, convergence or round count, and the exit gates (50+ Ideas, "all major Ideas challenged", agreement score above threshold) depend on Idea magnitudes, a disagreement queue and Weaver/BackgroundAgent machinery that the engine facts say do not exist. The 2-3 day estimate covers labelling and prompt injection only. The first real run will either never transition or transition on round count, which makes it indistinguishable from today's fixed modes.

4. **No evidence either feature changes outcomes, and nothing measures it.** The Evaluator scores output but nothing reads scores back. Sessions are occasional, and 17 exist, and until 2026-10-05 no ledger was real. The roadmap itself says blind proposals give more user value than phases. The likely abandonment story: a solo developer builds both, cannot tell whether results improved, and drops them.

5. **Moderator input mutates the decisions ledger with no rule for it.** The moderator spec says moderator messages do not count as agreement signals and are not private. The ledger chains DECIDED/CONTESTED/OPEN forward. If a moderator directive contradicts a DECIDED line, synthesis has no precedence rule. A single human steer could be recorded as CONTESTED or ignored.

6. **A human override can break a phase gate.** If the moderator pushes a Refine-phase thread back to divergence, the exit gate may never fire, or fires mid-correction. There is no pause, lock or veto defined.

**Undecided, author-only questions:**
- Is the moderator an authority that outranks phase gates, or just another voice?
- Does a moderator message persist across rounds and phases, or expire?
- Is the HTTP channel real-time or queued to the next round boundary, given `claude -p` turns cannot be interrupted?
- What is the single trigger for transitions, and who may override it?
- What evidence would convince you either feature is worth keeping?
