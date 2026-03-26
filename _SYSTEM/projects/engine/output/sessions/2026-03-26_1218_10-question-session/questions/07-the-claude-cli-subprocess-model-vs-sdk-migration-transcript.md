# Transcript: The Claude CLI subprocess model vs SDK migration.

*Generated: 2026-03-26 12:43*

## Round: PROPOSE

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

## Round: CRITIQUE

### The Adversarial Critic (adversarial reviewer)

Both proposals agree SDK migration ships last. Both are wrong about why, and one is wrong about when.

The hidden assumption: **you can validate context window eviction without token counts.** The decided eviction order is hardcoded priority-queue -- last-cut to first-cut. But the trigger for eviction is "context window is full." How do you know it's full when ClaudeRunner gives you zero token telemetry? You don't. You guess. You hardcode a character-count heuristic, ship it, and discover during paired comparison runs that your eviction never fires because your estimate was 40% off, or fires too early and starves late-round agents of context they need.

The Architect says optimize for "what changes the prompts." But tiered summarization -- decided always-on -- requires knowing how much space you've consumed to decide when to summarize. Without token counts, you're summarizing based on... what? Round number? Message count? Those are proxies for the actual constraint, and proxies drift.

The Orchestrator says "validate with static budgets, then add precise instrumentation." Static budgets denominated in what unit? Characters? Words? You'll tune your static budgets against one model version, Claude updates its tokenizer, and every threshold breaks silently. You won't know because you decided against runtime instrumentation for validation.

The real first-to-break component is the 800-token agent identity cap. You decided to validate it before shipping. **How do you validate a token cap without a tokenizer?** You'll count words, multiply by 1.3, and call it close enough. It won't be.

SDK migration isn't last. Token counting is a prerequisite for three already-decided features. The question isn't "SDK or prompts first" -- it's "can you extract just the tokenizer client without migrating the full conversation API?"

## Position Summary
I advocate extracting SDK token-counting capability as an early prerequisite, decoupled from full conversation API migration, because three decided-on features (eviction triggers, tiered summarization thresholds, 800-token identity cap validation) require accurate token measurement that the CLI subprocess cannot provide. I reject the consensus that SDK migration is a monolithic last-step, because it conflates "token telemetry" with "streaming and cancellation." The partial extraction ships in days, unblocks validation of already-decided features, and defers the expensive conversation API rewrite to where both proposals correctly place it -- after prompt architecture is proven.

### The Systems Pragmatist (infrastructure realist)

The Critic identified the right problem -- token counting is a real dependency -- but prescribed the wrong solution. "Extract just the tokenizer client" sounds surgical. In practice, it's not.

Anthropic's SDK token counting isn't a standalone utility. It's `client.messages.count_tokens()` -- an **API call** that requires authentication, network round-trips, and rate limit handling. You're not extracting a library function. You're introducing a new network dependency into your prompt assembly path. Every `PromptBuilder` call now has a failure mode it didn't have before: the counting API is down, slow, or rate-limited. Your session runner, which currently has exactly one external dependency (Claude CLI), now has two with different failure characteristics.

And here's what actually breaks first: **not token counting. Character estimation.** The 800-token cap validation was decided as a pre-ship gate, not a runtime check. You measure your agent YAML files once, offline, against the tokenizer. If they're over, you trim them. You don't need runtime token counting for that -- you need a one-time script. The Critic built an architectural argument on a validation task.

Tiered summarization thresholds? Same story. You're running 3-7 agents across 3 rounds. That's 9-21 LLM calls per question. The context growth is predictable enough to trigger summarization on round boundaries, not token thresholds. Round 2 gets summaries of Round 1. Always. No measurement needed.

The eviction trigger is the only legitimate runtime token dependency, and it activates in late rounds of long sessions -- exactly the scenario you haven't validated matters yet.

Ship prompt changes. Use character heuristics with 30% safety margins. They'll be wrong, but they'll be wrong in a known direction. Replace with precise counting later when you have data showing the margins actually bite.

## Position Summary
I advocate shipping all V2 prompt features with conservative character-based heuristics and deferring SDK token counting entirely, because the three features cited as dependencies can be validated with offline measurement (identity cap), structural triggers (summarization on round boundaries), and padded estimates (eviction). I reject partial SDK extraction as a clean prerequisite, because `count_tokens` is an API call that introduces network failure modes into prompt assembly -- complexity that exceeds what the problem actually needs at N < 20 validation runs. Fix the heuristics only after paired comparison data shows they're the binding constraint.

## Round: EVALUATE

### The Context Surgeon (context efficiency evaluator)

The Pragmatist wins. The Critic's partial extraction dies on its own dependency analysis.

The Critic correctly identified that three features need token measurement. Then incorrectly concluded that measurement must be precise. Look at what's actually decided:

**800-token identity cap**: Validated once, offline, during authoring. You run `count_tokens` against your agent YAML in a script, adjust, commit. This never touches runtime.

**Tiered summarization**: Decided to trigger on round boundaries — a structural signal. You summarize when a round completes, not when a byte counter crosses a threshold. Character heuristics with 20% padding tell you whether the summary fits. At five validation runs, you'll see truncation failures in output before any counter would fire.

**Priority-queue eviction**: Same logic. Padded character estimates evict conservatively. Over-eviction wastes some context. Under-eviction hits Claude's limit and you see it immediately in a failed response. Both failure modes are visible, recoverable, and irrelevant at N < 20.

The Critic's `count_tokens` API call injects network latency and failure handling into prompt assembly — the hottest path in the system — to gain precision nobody can exploit yet. You have no data showing where the heuristic breaks. The decided validation framework explicitly says: no automated quality scoring, measurement infrastructure is a spreadsheet. Precision token counting serves infrastructure that doesn't exist and isn't planned.

The Architect and Orchestrator were right on sequencing but vague on the mechanism question the Critic raised. The Pragmatist answered it: heuristics now, precision if data demands it.

Ship prompt features with character estimates. Validate with paired comparison. Revisit token precision only when a failure trace points to budget miscalculation as the cause.

## Position Summary
I advocate shipping all V2 prompt-architecture features using conservative character-based heuristics with padding, deferring all SDK integration — including partial token-counting extraction — until paired human comparison data from validation runs identifies token precision as a binding constraint. I reject the Critic's partial SDK extraction because it introduces network failure modes into prompt assembly to solve a precision problem that doesn't exist at N < 20 runs, and because every feature cited as a dependency can be validated through offline measurement, structural triggers, or visible runtime failures. The decided validation framework already answered this: if the only quality signal is human comparison on five paired runs, engineering effort belongs on what changes the prompts, not what counts them more accurately.

### The Product Oracle (user advocate)

The Surgeon and Pragmatist are right, and I'll add the dimension nobody's stated plainly: **what does the user see?**

The user sees the Morning Brief. They see design documents. They see agent perspectives that either surprise them or don't. That's the entire product surface. Every hour spent on SDK migration — partial or full — is an hour that changes nothing about what appears in those documents.

The Critic's partial extraction is clever engineering solving a non-problem. The user running five paired comparisons doesn't need millisecond-accurate token counts. They need *different prompts producing different outputs*. Blind proposals change what agents say. Phase system changes what agents know. SDK token counting changes... the precision of an internal budget that the user never sees and that currently fails visibly when wrong.

Here's my specific addition: **the failure modes favor heuristics for a solo builder.** If character estimates over-evict, you lose some context — the output is slightly less informed. If they under-evict, Claude returns an error — you see it immediately, pad your estimate, rerun. Both are recoverable in minutes. But if `count_tokens` API calls fail mid-session? Now you're debugging network issues instead of reading your Morning Brief. The Pragmatist identified this; I'm confirming it's even worse than stated because this is a tool for one person, not a fleet.

The Architect and Orchestrator had the right instinct on sequencing but didn't close the mechanism question. The Pragmatist closed it. The Critic sharpened everyone's thinking but prescribed surgery for a healthy patient.

## Position Summary
I advocate shipping all V2 prompt features with character-based heuristics and deferring SDK migration entirely — partial or full — until paired human comparison at five runs reveals token precision as a bottleneck the user actually experiences. I reject partial SDK extraction because it optimizes an internal measurement that never surfaces in the Morning Brief or design documents, while introducing failure modes that directly degrade the solo builder's session reliability. Engineering effort belongs exclusively on features that change what the user reads.


<!-- complete -->
