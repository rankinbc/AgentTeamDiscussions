### The Product Oracle (user advocate)

**Verdict: the plain size-triggered window wins. The disagreement spine and the output cap lose.**

From the user's perspective, the moment that matters is the Morning Brief. The user wakes up and asks one thing: why did the agents land here, and did anyone fight for the other side? Truncation only matters if it changes that answer.

[WINNER] Full history by default, oldest whole round dropped first, question and decided items always kept. The user can explain this in one sentence. The config is a single size threshold with a sane default, so a first-run YAML needs no tuning. If it fails, the failure is visible: an early round is gone, and that can be stated in the transcript.

[LOSES] Disagreement spine. It sounds like it protects dissent, but someone has to decide what counts as an unresolved conflict, and nobody has defined who or how. The user would never tune it or notice it working. It improves an internal metric, surviving distinct positions, with no proof the Morning Brief reads better. That is over-engineering before we know users want it.

[LOSES] Output length cap. The Critic's instinct to bound growth is sound, but the Pragmatist is right that it can't be enforced at the model. Worse, a hard cap chops the one sentence that carried the dissent, so the user gets thinner arguments and can't tell why.

[CONDITION] Define the overflow-retry behavior first. If a round is over budget even after dropping old rounds, the system must say so in the output, not trim silently. A silent failure is the only way this approach hurts the user.

[DEFER] Revisit summarization or a spine only after real briefs show the window dropped a position the user cared about. The retention question is whether the output stays worth reading, and we can't answer that by building mechanisms first.

## Position Summary
I advocate full history by default with a size-triggered window that drops the oldest whole round first and always keeps the question and decided items. I reject the disagreement spine, any summarization stage, and the output cap, because each adds an unspecified or unenforceable step the user can't see or tune. The window is the simplest approach to configure and explain, and it fails visibly, which protects the Morning Brief.

### The Context Surgeon (context efficiency evaluator)

**Verdict: the size-triggered window wins. The disagreement spine and the output cap lose.**

The Product Oracle picked the right winner, but the argument leaves out the token cost, so here it is.

The token cost of full history is linear per round and compounds per agent. Seven agents each re-reading every prior round is the real bill. Because every CLI call is stateless, the engine rebuilds the whole prompt each time, and nothing is cached on the model side. That is why a trigger tied to the engine's existing budget enforcement matters. It is the only mechanism here that already counts tokens instead of guessing.

The spine loses on signal-to-noise. Verbatim conflicts get appended on top of the latest round, so the agent receives the same dissent twice, once in the spine and once in the round that produced it. It also needs a classifier to decide what is "unresolved", and nobody has specified one. When context fills, the spine is the one thing that never shrinks, so it displaces everything else.

The output cap loses. The Pragmatist is right that it cannot be enforced at generation, and it does nothing about history already accumulated. It also cuts the dense sentence and keeps the preamble.

I push back on the Oracle's "oldest whole round first" on one point. Dropping whole rounds is coarse. It can discard the entire propose round, which holds each agent's original framing, while keeping the critiques that react to it. The window needs a floor: always keep the question, the decided items, and the first round's position summaries. The Position Summary blocks are already dense, three sentences each. They are the cheapest dissent carrier we have, and they require no new extraction step.

The overflow condition stands. If a round is over budget after eviction, the transcript must say so.

## Position Summary
I advocate full history by default with a size-triggered window tied to the existing budget enforcement. It drops the oldest whole round first, and always keeps the question, the decided items and the early position summaries. I reject the disagreement spine because it duplicates content and needs an undefined classifier, and I reject the output cap because it cannot be enforced and does not bound history. The window is the only option that counts tokens and fails visibly.


<!-- complete -->
