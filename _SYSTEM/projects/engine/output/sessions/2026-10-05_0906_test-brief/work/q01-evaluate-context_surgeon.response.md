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
