### The Cognitive Architect (creativity engine designer)

# The Strangler Fig Strategy

Neither incremental patches nor parallel rewrite. Both are false choices rooted in software engineering orthodoxy rather than how creative systems actually evolve.

**The answer is interface-first strangling.** You define the new round loop abstraction -- the one that supports blind proposals, phase gates, and synthesis hooks -- then you route V1's existing behavior *through* that abstraction unchanged. V1 becomes the first "mode" running on V2's skeleton. No rewrite. No feature flags. No parallel codebases rotting out of sync.

Here's why this is the only strategy that works for *this* system specifically:

**The round loop is the spine.** Blind proposals don't "layer on top" -- they fundamentally change when agents see each other's output. Phase gates don't "layer on top" -- they change what triggers the next round. If you try to patch these into V1's loop, you get conditionals breeding inside your orchestration logic until nobody can reason about execution order. I've seen this pattern kill three creative tooling projects.

**But a parallel rewrite kills your feedback signal.** You need real sessions producing real output to evaluate whether V2's structural changes actually improve discussion quality. A rewrite in isolation means you're designing blind -- exactly the anti-pattern your own system is trying to solve.

**The strangler approach:** New `IDiscussionPipeline` interface. V1's propose-critique-evaluate becomes one pipeline implementation. Blind proposals become another. Both run through the same `SessionRunner`. Ship the interface, then ship pipelines one at a time against live output.

The BIT system and key takeaways genuinely do layer on top. Build those whenever.

## Position Summary
I advocate a strangler fig migration where V2's round loop abstraction wraps V1's existing behavior before any new features ship, enabling pipeline-by-pipeline delivery against real session output. I reject both incremental patching (which creates orchestration spaghetti when the core loop must change) and parallel rewrite (which eliminates the feedback signal you need to evaluate structural changes). The discussion engine's own philosophy -- iterate against real output, not theory -- demands this approach.

### The Flow Orchestrator (mechanical flow designer)

# Cut the Metaphor, Trace the Sequence

The Cognitive Architect is 80% right and 20% naming things. Let me strip the poetry and trace what actually happens.

**What "strangler fig" actually means here:** Extract an `IDiscussionPipeline` interface from `DiscussionEngine.cs`. Make V1's propose-critique-evaluate the default implementation. Done. This is a refactor, not a strategy. Call it what it is.

**Where I agree:** The round loop *is* the spine. Patching blind proposals into `RoundRunner.cs` with conditionals will create state management hell. I've traced the current flow: `SessionRunner` → `DiscussionEngine.RunDiscussion` → `RoundRunner.RunRound` per round type. Blind proposals change *when visibility happens*, which means the orchestration boundary between rounds must move. You can't bolt that on.

**Where I disagree:** "Ship the interface, then ship pipelines one at a time" skips the hard question -- **what are the decision points inside the pipeline?** An interface without defined state transitions is just an empty box. Before extracting `IDiscussionPipeline`, you need:

1. The exact states a discussion passes through (not round names -- *execution states*)
2. What data flows between states
3. Where the phase gate check fires relative to round completion

The Architect jumped to the solution shape without specifying the state machine inside it. That's the part that actually determines whether blind proposals and phase gates compose cleanly or collide.

**My addition:** Define the state machine first. Three states minimum: `Collecting`, `Visible`, `Synthesizing`. If blind proposals and phase gates both map cleanly onto transitions between these states, the interface extraction works. If they don't, we've found the real design problem early.

## Position Summary
I advocate defining the discussion state machine (explicit states and transitions) before extracting any pipeline interface, because the interface shape depends on whether blind proposals and phase gates compose at the state level. I reject jumping to interface extraction without proving the states compose -- that risks building an abstraction that immediately leaks. The Architect's direction is correct but underspecified where it matters most: execution ordering.


<!-- complete -->
