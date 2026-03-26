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
