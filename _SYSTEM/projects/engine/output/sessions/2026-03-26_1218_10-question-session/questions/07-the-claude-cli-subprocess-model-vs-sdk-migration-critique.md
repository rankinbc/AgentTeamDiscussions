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


<!-- complete -->
