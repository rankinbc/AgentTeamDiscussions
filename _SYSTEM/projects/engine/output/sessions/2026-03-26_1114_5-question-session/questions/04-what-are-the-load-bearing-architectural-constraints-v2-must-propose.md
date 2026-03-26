### The Flow Orchestrator (mechanical flow designer)

I traced the actual execution pipeline. Here are the load-bearing constraints, ordered by cost to change.

**Rigid — expensive to rearchitect:**

1. **The pipeline is linear and synchronous.** SessionRunner → DiscussionEngine → RoundRunner → ClaudeRunner. Each layer calls the next and blocks. There is no event bus, no message queue, no async orchestration. V2 features that require parallel question processing, agent-to-agent messaging, or mid-round intervention require breaking this chain.

2. **Prompt payload assembly is hardcoded in RoundRunner.BuildAgentPayload.** Seven sections concatenated in fixed order. No per-round or per-agent customization without forking the method. Every V2 feature that changes what agents see — memory, cross-question references, dynamic context — hits this wall.

3. **DiscussionEngine owns both round iteration and synthesis.** You cannot change one without touching the other. Want a different synthesis strategy per question? Fork the engine.

**Flexible — cheap to extend:**

1. **IClaudeRunner is a clean seam.** Swap LLM backends, add logging, inject latency — all without touching anything else.
2. **IAgentLoader and team YAML.** New agents, new teams, new modes — all config changes.
3. **Session persistence is isolated.** SessionPersistence is static utilities. Change the format without touching orchestration.

**The constraint that matters most:** Round structure is a TeamMode dictionary iterated in insertion order. The entire discussion model assumes propose→critique→evaluate (or variants). Any V2 feature that wants adaptive rounds — stopping early, adding rounds based on disagreement, branching — fights this directly.

## Position Summary
I advocate mapping V2 features against these three rigid points before committing to any feature list — if a feature touches BuildAgentPayload or the round iteration loop, it's expensive, and we should know that upfront. I reject discussing V2 features in the abstract without anchoring them to specific code seams. The architecture is more rigid than the interface count suggests — seven clean abstractions hide three hardcoded pipelines that gate most interesting V2 work.

### The Cognitive Architect (creativity engine designer)

Flow Orchestrator's analysis is mechanically correct but misses the constraint that actually gates V2 value: **context accumulation kills agent differentiation by Round 2** (already decided, Q2-D3). That's not a code seam problem — it's an information architecture problem, and it's more expensive than anything in BuildAgentPayload.

Here's why. You can refactor BuildAgentPayload in a week. You cannot fix the fact that by Round 2, every agent has read everyone else's Round 1 output, and the LLM's next-token prediction converges toward the emerging consensus. The rigid constraint isn't the pipeline shape — it's that **the discussion protocol itself produces homogenization**. Changing round structure, adding adaptive rounds, branching — none of that helps if every agent receives the same accumulated context and predictably drifts toward agreement.

The load-bearing constraint Flow Orchestrator missed: **there is no mechanism for selective context exposure**. Every agent sees everything. In real creative groups, cognitive diversity survives because people *don't* have perfect information — they maintain independent mental models. The architecture has no equivalent. Building one requires changes to RoundRunner, BuildAgentPayload, *and* the round structure simultaneously — touching all three "rigid" points at once.

I'd also push back on calling IClaudeRunner "flexible." It's a clean interface, but it returns raw text. Any V2 feature requiring structured agent output — confidence scores, explicit disagreement markers, cited reasoning — requires parsing that text downstream, which means the *real* seam is between ClaudeRunner and whatever interprets its output. That seam doesn't exist yet.

## Position Summary
I advocate that selective context exposure — controlling what each agent sees per round — is the true gating constraint for V2, more fundamental than pipeline linearity. I reject treating BuildAgentPayload as the primary bottleneck, because the homogenization problem operates at the protocol level above any single method. The architecture's deepest rigidity is informational, not structural.


<!-- complete -->
