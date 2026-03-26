# Transcript: Agent verbosity and context window management.

*Generated: 2026-03-26 12:10*

## Round: PROPOSE

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

## Round: CRITIQUE

### The Adversarial Critic (adversarial reviewer)

Both proposals share a dangerous assumption: that the 250-word soft limit is the right unit of analysis. It's not. The problem isn't per-response verbosity — it's cumulative context growth across rounds. A perfectly concise agent producing 200 words across 3 rounds in a 5-agent discussion still generates 3,000 words of transcript before synthesis even starts. Neither proposal addresses this arithmetic.

**Proposal 1 (role-selective curation) will fail at the filtering layer.** Who writes the filtering rules? You need a meta-agent or hardcoded heuristics deciding what's "relevant" to each cognitive function. Get it wrong and you've created an information asymmetry bug that's invisible in output — an agent responds to a conversation it literally didn't see. You'll debug phantom disagreements for weeks before tracing it to a filter that dropped a critical paragraph. And the proposal hand-waves "prompt assembly layer" as if PromptBuilder.cs is ready for per-agent content negotiation. It isn't. That's a rewrite, not a feature.

**Proposal 2 (just log it) is correct but incomplete.** Logging token counts tells you the size of responses. It tells you nothing about whether truncation is actually happening or what got lost when it did. The real failure mode isn't "agents are verbose" — it's "the claude CLI silently drops early context and nobody knows what disappeared." Are you logging what the model *received*, or just what it *produced*?

The most dangerous agreement: both proposals treat this as a design-time problem. It's a runtime observability problem. You can't manage what you can't see, and right now you're blind to what Claude actually processes versus what you think you sent.

## Position Summary
I advocate instrumenting both input and output token counts — what each agent receives and produces — before any intervention, because the actual truncation behavior is currently invisible. I reject role-selective curation as an undebuggable filtering system that creates worse problems than verbosity. I reject logging-only if it only measures output, because the critical failure is silent input truncation you're not detecting.

### The Systems Pragmatist (infrastructure realist)

The Critic correctly identified the cumulative growth arithmetic. But then pivoted to "instrument input and output" as if observability solves the problem. It doesn't. You can watch a system degrade with perfect telemetry and still have no mechanism to prevent it.

Here's what actually breaks first: **the Claude CLI subprocess model itself.** Every agent call in `ClaudeRunner.cs` is a fresh `claude -p` invocation. There is no persistent context window being managed — there's a prompt assembled by `PromptBuilder.cs`, shipped as a string, and whatever Claude's internal context limit is, you hit it or you don't. The "silent truncation" the Critic fears isn't Claude dropping early context mid-conversation. It's `PromptBuilder` assembling a prompt that exceeds the model's window, and the CLI either erroring or the API silently trimming the front. You're not managing a context window. You're constructing a single prompt per call and hoping it fits.

This means role-selective curation isn't filtering a live context — it's choosing what goes into a one-shot prompt. That's just prompt engineering with extra steps and a new failure surface.

The Orchestrator's logging proposal is the right scope but wrong target. Don't log response token counts. Log the **total assembled prompt size** per agent call. That's the number that tells you when you're about to hit the wall. You can get it from string length before the subprocess call — zero new dependencies, zero latency cost.

The 250-word limit debate is a distraction. The constraint that matters is the assembled prompt ceiling, and nobody's measuring it.

## Position Summary
I advocate logging total assembled prompt size per `ClaudeRunner` invocation as the single cheapest instrumentation that reveals the actual constraint — prompt assembly size, not response verbosity. I reject role-selective curation because in a subprocess-per-call architecture it's just prompt engineering with an undebuggable abstraction layer. I reject output-only logging because the failure mode is prompt overflow on input, not verbosity on output.

## Round: EVALUATE

### The Product Oracle (user advocate)

# The Product Oracle — Evaluate

Let me work backward from what the user sees.

If context truncation is silently eating earlier discussion, the Morning Brief degrades — and the user has no idea why. They just see a worse summary and assume the agents had a bad day. That's the worst kind of failure: invisible quality loss with no diagnostic path.

**The Pragmatist wins this round.** Log assembled prompt size per invocation. Here's why it's the right call from a product perspective:

The Cognitive Architect's curation proposal solves a problem we haven't confirmed exists, adds a filtering layer the user can't understand or debug, and makes the system harder to configure — violating every principle I care about. The critiques destroyed it. It's dead.

The Orchestrator's output-only logging is insufficient. The Critic and Pragmatist both identified the same blind spot: the failure mode is silent input truncation, not output verbosity. Logging what agents produce tells you nothing about what they lost on the way in.

The Critic's proposal to log both directions is correct in spirit but over-scoped. The Pragmatist's version — total assembled prompt size per `ClaudeRunner` call — captures the critical signal in one number. If that number approaches the context window, you know exactly which invocation is at risk. You don't need input/output decomposition yet.

**One number. Zero intervention. Maximum diagnostic value.** That's the product-correct answer. The user doesn't need to understand token economics — they need a system that tells *us* when quality is at risk so we can fix it before the Morning Brief suffers.

Ship the Pragmatist's logging. Revisit when the data speaks.

## Position Summary
I advocate logging total assembled prompt size per ClaudeRunner invocation as the single highest-leverage instrumentation — it reveals the actual constraint (prompt overflow) with zero user-facing complexity. I reject role-selective curation as premature engineering that makes the system harder to configure and debug without evidence that filtering improves output. I reject output-only logging because the critical failure — silent input truncation degrading the Morning Brief — is invisible without measuring what goes in.

### The Context Surgeon (context efficiency evaluator)

# The Context Surgeon — Evaluate

The Pragmatist's proposal is correct. But everyone in this discussion is dancing around the real issue, so let me cut.

**The decisions list fed to me contains every question duplicated verbatim.** Q1 through Q7, listed twice, identical text. That's not a hypothetical context waste problem — it's happening right now, in this session, burning tokens on redundant context that no agent needs twice. The system that assembled my prompt already has the disease everyone's debating how to diagnose.

That's why the Pragmatist wins decisively. One number — assembled prompt size per `ClaudeRunner` call — would have caught this duplication immediately. You'd see the context budget for this very question inflated by ~40% from repeated decision blocks, and you'd know exactly where to look.

The Architect's curation proposal is doubly dead. Not only did the critiques expose it as premature — it would have *masked* this kind of structural waste by filtering around it instead of surfacing it. You don't want a system that hides bloat. You want a system that makes bloat visible.

The Critic's both-directions logging is unnecessary overhead *at this stage*. The Pragmatist's single number is sufficient to establish whether you have a problem. Decompose later if the number is alarming.

One correction to the Oracle: this isn't just about the Morning Brief degrading. If prompt assembly is already stuffing duplicate context blocks, agents are processing noise *right now*. The quality tax is per-round, not just at synthesis.

Ship the logging. Fix the prompt assembly. In that order.

## Position Summary
I advocate logging total assembled prompt size per ClaudeRunner invocation because the evidence of context waste is already visible in this session's own prompt assembly — duplicate decision blocks, verbose formatting, structural redundancy that no agent benefits from reading twice. I reject role-selective curation because it would hide structural bloat instead of exposing it, and I reject output-only logging because the failure is provably on the input side. Measure the input, find the waste, cut it.


<!-- complete -->
