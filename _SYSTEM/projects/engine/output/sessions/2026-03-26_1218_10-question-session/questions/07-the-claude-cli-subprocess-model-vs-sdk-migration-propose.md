### The Cognitive Architect (creativity engine designer)

# The SDK Migration Is a Trap -- Ship It Last

The SDK migration is the most dangerous item on the V2 roadmap because it feels essential while being almost entirely orthogonal to output quality. Every decided validation criterion asks one question: "Did V2 surface a perspective V1 missed?" Streaming doesn't surface perspectives. Token counting doesn't surface perspectives. Cancellation doesn't surface perspectives.

**What actually blocks on ClaudeRunner changes: nothing on the critical path.** Blind proposals are a PromptBuilder change. Phase system is round orchestration. Context window management is prompt assembly. Tiered summarization is prompt assembly. Every V2 feature that matters lives upstream of the subprocess call. ClaudeRunner is a dumb pipe, and dumb pipes are fine.

The cognitive science argument is even sharper. Research on creative group output (Paulus & Nijstad, 2003) consistently shows that **what you ask** matters orders of magnitude more than **how fast you ask it**. Latency reduction improves developer experience. It does not improve discussion quality. And the decided validation framework explicitly rejects automated quality metrics -- so the SDK's token-counting capabilities give you data you've already decided not to use.

**The one legitimate SDK benefit:** proper timeout/cancellation when an agent hangs. But V1's retry mechanism in ClaudeRunner already handles this adequately for the session volumes you're running.

Ship SDK migration after all prompt-level V2 features are validated through paired comparison. It's a developer experience improvement, not a discussion quality improvement. Sequence it accordingly.

## Position Summary
I advocate shipping SDK migration last in the V2 timeline, after all prompt-architecture features are validated, because it improves plumbing without improving the only thing that matters: discussion output quality. I reject treating it as a prerequisite or parallelizing it early, because it will consume engineering bandwidth that should go toward blind proposals and phase system -- the features that actually change what agents say. The decided validation framework already told us the answer: if paired human comparison is the only quality signal, optimize for what changes the prompts, not what changes the transport.

### The Flow Orchestrator (mechanical flow designer)

# The Architect Is Right on Sequencing, Wrong on "Nothing Blocks"

I agree with the conclusion -- ship SDK last -- but the reasoning has a gap I need to close.

The Architect says "nothing on the critical path blocks on ClaudeRunner changes." That's true today. But trace the message lifecycle forward through V2 features and you hit a real dependency: **tiered summarization needs to know how much context was consumed by the previous turn.** Right now ClaudeRunner returns raw text. No token counts. No usage metadata. The decided eviction order (hardcoded, last-cut to first-cut) needs a trigger -- something has to signal "we're approaching the limit, start evicting."

Without the SDK, that trigger is... what? A character-count heuristic? Token estimation from string length? Both are fragile. Both require calibration work that the SDK gives you for free.

But here's why that still doesn't change the sequencing: **you don't need accurate token counts for V2 validation.** The decided approach is five paired runs with human comparison. You can run those with conservative static budgets. You only need precise eviction when you're operating near the boundary in production, which is post-validation.

So the actual dependency chain is:

1. Prompt snapshots (prerequisite, decided)
2. Blind proposals via PromptBuilder
3. Phase system in round orchestration
4. Tiered summarization with static budgets
5. Paired validation runs
6. SDK migration (enables precise eviction for production)

Six discrete steps. No parallelization needed. The SDK is step 6 because every prior step works without it, just less efficiently.

The Architect's appeal to creativity research is decoration. The sequencing argument is mechanical: trace the data dependencies, the SDK has none until production tuning.

## Position Summary
I advocate the same terminal position -- SDK migration last -- but ground it in explicit dependency tracing rather than cognitive science analogies. I reject any framing that treats the SDK as "just developer experience," because it does carry a real production dependency for token-aware eviction, but that dependency activates after validation, not before. The sequence is: prompt changes, validate with static budgets, then add precise instrumentation.


<!-- complete -->
