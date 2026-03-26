### The Cognitive Architect (creativity engine designer)

# Agent Verbosity and Context Window Management

## The Real Problem Isn't Length — It's Attention

Hard token limits are a blunt instrument that produces compressed garbage. An architect forced into 200 tokens doesn't think more concisely — they produce a worse version of what they'd say in 400. The actual problem is that accumulated context becomes an undifferentiated wall of text, and agents responding later in a round are processing noise alongside signal.

## My Design: Role-Selective Context Curation

Instead of limiting what agents *produce*, filter what they *receive*.

**The mechanism:** Before each agent's turn, a lightweight curation pass extracts the context subset relevant to that agent's cognitive function. The critic sees claims and reasoning chains. The pragmatist sees proposals and implementation specifics. The architect sees structural patterns and dependencies. Everyone gets the current round's raw contributions, but prior rounds arrive pre-filtered through their cognitive lens.

**Why this works:** Selective attention is how actual expert groups function. A security reviewer reading an architecture document doesn't process the UX rationale — they're scanning for attack surfaces. This isn't information loss; it's the same cognitive filtering that makes specialized roles valuable.

**Implementation:** This is a prompt-assembly concern, not a runtime intervention. The `PromptBuilder` already does 3-layer assembly. Add a fourth layer: context relevance filtering using the agent's personality dimensions as selection criteria. No SDK migration needed. No CLI flags. No hard limits that degrade output quality.

**The verbosity problem solves itself:** Agents receiving focused context produce focused responses. Bloat comes from agents responding to everything because they see everything.

## Position Summary

I advocate role-selective context curation — filtering what each agent receives based on their cognitive function rather than capping what they produce. I reject hard token limits, which treat a signal-to-noise problem as a volume problem and guarantee quality degradation. Selective attention is how real expertise works; building it into the prompt assembly layer gives us context management that actually improves discussion quality instead of merely constraining it.

### The Flow Orchestrator (mechanical flow designer)

# Agent Verbosity and Context Window Management

## The Cognitive Architect Is Designing a System Nobody Asked For

Role-selective context curation sounds elegant. It's also a new subsystem with non-trivial failure modes that we have zero evidence we need.

**The sequence problem:** Who runs this "lightweight curation pass"? If it's an LLM call, you've added one Claude invocation per agent per round. For a 5-agent, 3-round session, that's 15 extra calls — roughly doubling session cost and duration. If it's rule-based keyword matching, it will filter wrong and agents will produce incoherent responses because they're missing context they actually needed. Either path introduces a new failure class into the message lifecycle that doesn't exist today.

**The actual trigger is missing.** We decided in Q2 to instrument before allocating. We have no token usage data. We don't know which agents exceed the soft limit, by how much, how often, or whether truncation is actually degrading output. The Architect is proposing a fourth prompt-assembly layer to solve a problem we haven't measured.

**What I'd actually ship:** One thing. Add response token counts to the existing session output logging. That's it. When we have data showing which agents consistently blow past limits and whether that correlates with quality degradation or context truncation, we design the intervention that matches the actual problem.

If the data eventually says "context is the issue," then per-role filtering *might* be the right shape. But building the filtering system before the measurement system is backwards. We decided this already in Q2 and Q5. Stop relitigating.

## Position Summary

I advocate logging response token counts per agent per round as the sole V2 change — the instrumentation we already committed to in Q2. I reject role-selective context curation as premature engineering that introduces a new failure class (bad filtering, doubled latency) without evidence that context volume is the actual problem. Measure first, then design the intervention that matches reality.


<!-- complete -->
