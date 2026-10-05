**Verdict: the plain size-triggered window wins. The disagreement spine and the output cap lose.**

From the user's perspective, the moment that matters is the Morning Brief. The user wakes up and asks one thing: why did the agents land here, and did anyone fight for the other side? Truncation only matters if it changes that answer.

[WINNER] Full history by default, oldest whole round dropped first, question and decided items always kept. The user can explain this in one sentence. The config is a single size threshold with a sane default, so a first-run YAML needs no tuning. If it fails, the failure is visible: an early round is gone, and that can be stated in the transcript.

[LOSES] Disagreement spine. It sounds like it protects dissent, but someone has to decide what counts as an unresolved conflict, and nobody has defined who or how. The user would never tune it or notice it working. It improves an internal metric, surviving distinct positions, with no proof the Morning Brief reads better. That is over-engineering before we know users want it.

[LOSES] Output length cap. The Critic's instinct to bound growth is sound, but the Pragmatist is right that it can't be enforced at the model. Worse, a hard cap chops the one sentence that carried the dissent, so the user gets thinner arguments and can't tell why.

[CONDITION] Define the overflow-retry behavior first. If a round is over budget even after dropping old rounds, the system must say so in the output, not trim silently. A silent failure is the only way this approach hurts the user.

[DEFER] Revisit summarization or a spine only after real briefs show the window dropped a position the user cared about. The retention question is whether the output stays worth reading, and we can't answer that by building mechanisms first.

## Position Summary
I advocate full history by default with a size-triggered window that drops the oldest whole round first and always keeps the question and decided items. I reject the disagreement spine, any summarization stage, and the output cap, because each adds an unspecified or unenforceable step the user can't see or tune. The window is the simplest approach to configure and explain, and it fails visibly, which protects the Morning Brief.
<!-- complete -->
