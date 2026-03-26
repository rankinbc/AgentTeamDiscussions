### The Context Surgeon (context efficiency evaluator)

# Evaluation: V2 Migration Strategy

**The Pragmatist wins. The Critic identified the right target but proposed the wrong first move.**

The Architect and Orchestrator both committed the same error: designing scaffolding before proving what needs scaffolding. The strangler fig assumes the round loop is the right abstraction boundary. The state machine assumes blind proposals and phase gates compose at the state level. Neither has evidence. Both are architectural speculation dressed as methodology.

The Critic correctly identified PromptBuilder's context assembly as the actual coupling hotspot -- this is where blind proposals force real changes, where phase context must flow, where every V2 feature ultimately manifests. That insight is sharp. But the Critic's prescription -- "ship the first V2 feature by modifying the smallest surface area" -- is reckless without a regression signal. You'd be changing the most critical component with no way to detect prompt degradation.

The Pragmatist's prompt output snapshots solve this. Capture known-good prompt output for existing sessions. Now you have a diff target. Now you can measure which modification path produces the smallest blast radius per feature. The migration strategy stops being a philosophical debate and becomes an empirical question.

**Execution order:** Snapshots first (days, not weeks). Then blind proposals through PromptBuilder modification (the Critic's target, validated by the Pragmatist's signal). The round loop abstraction emerges from actual feature delivery, not from upfront design.

The Architect's strangler fig may end up being the right pattern. But you earn that conclusion through evidence, not assumption.

## Position Summary
I advocate prompt output snapshots as the non-negotiable first deliverable, followed by PromptBuilder-targeted feature delivery that lets the migration pattern emerge empirically. I reject all upfront architectural scaffolding -- strangler fig, state machine, interface extraction -- as premature commitments without regression data. The system that preaches "iterate against real output" must apply that principle to its own evolution.

### The Product Oracle (user advocate)

# Evaluation: V2 Migration Strategy

**The Pragmatist and Critic together form the right answer. The Surgeon's synthesis is almost correct but misses the product question.**

Everyone is debating *how* to migrate. Nobody asked *what the user notices*.

The Morning Brief is the product. Design docs are the product. If blind proposals produce sharper design docs, users care. If the migration strategy produces identical output for three months while you build scaffolding, users see nothing. The strangler fig and state machine are engineering comfort blankets -- they make developers feel safe, not users feel served.

The Surgeon correctly sequenced snapshots-then-PromptBuilder. But snapshots aren't just a regression signal. They're a **product baseline**. Capture current Morning Brief quality. Now every V2 change answers: did the brief get better? Not "did the architecture improve" -- did the *output the human reads* improve?

The Critic's insight about PromptBuilder is correct precisely because it's the component closest to what the user experiences. Blind proposals change what agents see, which changes what they write, which changes the design doc, which changes the Morning Brief. That's the value chain. Start where value flows.

The Architect's strangler fig and the Orchestrator's state machine both optimize for internal elegance. A solo builder running this system doesn't care about state machine purity. They care that Tuesday's brief is better than Monday's.

**Ship blind proposals through PromptBuilder modification, measured against Morning Brief quality, within the first week.** If it improves output, you've validated V2's core thesis. Everything else is sequencing.

## Position Summary
I advocate measuring every V2 change against Morning Brief quality improvement, starting with blind proposals through PromptBuilder modification as the first user-visible deliverable. I reject all upfront architectural work -- strangler fig, state machine, interface extraction -- because they optimize for developer comfort while delivering zero user value. The migration strategy that wins is the one where the user notices improvement fastest.


<!-- complete -->
