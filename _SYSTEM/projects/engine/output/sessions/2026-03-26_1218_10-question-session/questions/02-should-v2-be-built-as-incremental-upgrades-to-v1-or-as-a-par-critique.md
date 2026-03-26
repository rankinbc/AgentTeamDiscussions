### The Adversarial Critic (adversarial reviewer)

Both proposals share a dangerous assumption: that V1's round loop is the right boundary for restructuring. Neither has examined whether that's actually where things break first.

**The round loop isn't the problem.** The round loop is sequential, predictable, and boring. It calls agents, collects responses, moves on. The actual complexity lives in SessionRunner's cascade error handling, the persistence layer's completion markers, and the prompt assembly pipeline that threads context between rounds. A strangler fig around the round loop gives you a clean abstraction around the easiest part of the system while leaving the hard parts untouched.

**The state machine is premature formalization.** The Orchestrator wants explicit states and transitions before extracting interfaces. But we have seven working modes across two teams. The state machine must accommodate all of them without regression. Has anyone actually enumerated the state space? Compete mode's scoring, counter mode's dialectic structure, ideas mode's brainstorm-then-debate -- these aren't variations of one state machine, they're fundamentally different control flows wearing the same interface. Formalizing prematurely locks you into a unification that may not exist.

**What breaks first:** The prompt builder. Blind proposals require withholding prior round context. Phase gates inject new context boundaries. Both mutate what PromptBuilder assembles, and PromptBuilder is already the most coupled component -- it touches agent config, session state, round history, and role overlays simultaneously. Neither proposal addresses this.

**The hidden question nobody asked:** Can you ship blind proposals without touching the round loop at all? Just modify PromptBuilder's context assembly. If yes, the entire migration debate is premature optimization.

## Position Summary
I advocate starting from the actual coupling hotspot -- PromptBuilder's context assembly -- rather than the round loop abstraction both proposals assume is the right boundary. I reject both the strangler fig and the state machine as starting points because they formalize structure around the wrong component. The first V2 feature should ship by modifying the smallest surface area possible, which reveals the real constraints before we commit to architectural scaffolding.

### The Systems Pragmatist (infrastructure realist)

The Critic is right that PromptBuilder is the coupling hotspot, but wrong about the implication. "Just modify PromptBuilder" is the incremental patching approach the Architect already rejected, and for good reason: every V2 feature touches context assembly differently. Blind proposals subtract context. Phase gates partition it. Stale detection timestamps it. You don't get to make four separate "small" changes to the most coupled component and call it low-risk. That's four overlapping mutations to a function that already juggles six concerns. The blast radius isn't one change -- it's the interference pattern between them.

**The assumption everyone shares and nobody's tested:** that the current prompt assembly is a single pipeline that can be selectively modified. Has anyone actually traced a prompt through assembly for compete mode versus ideas mode? If PromptBuilder already has implicit branching per mode, then "just modify PromptBuilder" means modifying N code paths, not one. The Critic's "smallest surface area" might be larger than the Architect's strangler fig.

**What actually breaks first:** Not the round loop, not the state machine, not even PromptBuilder in isolation. It's the **test coverage gap**. You have 78 tests, none of which (based on the test descriptions) validate prompt content. Any structural change -- whether strangler fig, state machine, or "just modify PromptBuilder" -- ships without a regression signal for the thing that matters most: what the agents actually see. You're arguing about migration strategies without a safety net.

**The real first step nobody proposed:** Snapshot current prompt output for every mode. That's your regression oracle. Then the migration strategy argument resolves itself empirically -- whichever approach changes fewer snapshots per feature wins.

## Position Summary
I advocate building prompt output snapshots as the literal first deliverable before any structural work, because every proposed approach lacks a regression signal for the system's most critical output. I reject all three starting points (strangler fig, state machine, PromptBuilder modification) as premature without empirical evidence of actual coupling boundaries. The migration strategy should be determined by data -- which approach produces the smallest diff per feature against known-good prompt output -- not by architectural aesthetics.


<!-- complete -->
