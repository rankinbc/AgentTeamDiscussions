## Decisions

**Full history by default, with a size-triggered window.** Both evaluators (Product Oracle, Context Surgeon) picked this approach, and the Flow Orchestrator and Systems Pragmatist proposed or endorsed it. While the assembled prompt is under budget, nothing is cut. Most discussions never reach the limit, so they run untouched.

**The trigger is a measured size check against the engine's existing context budget enforcement.** The Context Surgeon argued this is the only mechanism on the table that already counts tokens. The limits live in the configuration defaults, so a first run needs no tuning.

**When over budget, the oldest whole round is dropped first.** Responses are never cut partway. Dropped rounds stay on disk in the transcript, so synthesis still has everything.

**The question and the decided items are never dropped.**

**The overflow case must be visible.** If a round is still over budget after old rounds are evicted, the system says so in the transcript. It does not trim silently. Both evaluators made this a condition of their verdicts. The Systems Pragmatist added that the overflow-retry behavior must be defined before anything else is built, so a context-overflow failure never resends the same oversized prompt in a loop.

**The disagreement spine lost.** Evaluators rejected it for three reasons:
- It needs a classifier to decide what counts as unresolved, and nobody specified one.
- A misclassified conflict is dropped silently.
- It repeats dissent that already appears in the latest round, and it never shrinks when context fills.

**The output length cap lost.** Evaluators rejected it for three reasons:
- The model cannot be forced to obey a word limit.
- A hard cut removes the dense sentence that carried the dissent, along with the closing Position Summary the engine relies on.
- It slows history growth but does not bound it.

**Neutral summarization was rejected for now.** The Cognitive Architect warned it averages positions into consensus. The Flow Orchestrator warned it adds an extraction step with no fallback. No one defended it.

**Early framing needs protection.** The Context Surgeon's floor addresses the Adversarial Critic's point that dropping the opening round removes the framing later agents rebut. The floor keeps the first round's Position Summaries, which are already dense and need no new extraction step. This was stated by one evaluator and not opposed. The Product Oracle's winning statement did not include it, so treat it as an amendment accepted without dispute rather than a unanimous ruling.

## Contested

**Whether to build a dissent-preserving mechanism now.**

- *For (Cognitive Architect):* Truncation decides how much divergent thinking survives each round. A sliding window loses early dissent, and a neutral summary manufactures consensus. A verbatim disagreement spine of live conflicts, plus the latest round in full, protects dissent. It can be tested by blind-scoring surviving distinct positions against full-history runs.
- *Against (Flow Orchestrator, Adversarial Critic, Systems Pragmatist, both evaluators):* The spine adds an undefined classification step and a new pipeline stage. The test needs an LLM judge, which is the same risky extraction step. The failure it targets has not been observed.

The evaluators ruled for the plain window. The Cognitive Architect's concern was not refuted: nobody showed how dissent loss will be detected once the lost content is no longer visible. The Adversarial Critic raised this and it was left unanswered.

**Whether to cap response length at the source.**

- *For (Adversarial Critic):* Capping each agent's output bounds history growth without eviction or extraction.
- *Against (Systems Pragmatist, both evaluators):* The cap cannot be enforced at the model, and it does not stop linear history growth. It also compresses reasoning that later agents need to rebut.

The evaluators ruled against the cap. The Critic's underlying instinct, that growth needs bounding, was accepted as sound.

## Deferred

- Revisit summarization or a disagreement spine only after real briefs show the window dropped a position the user cared about (Product Oracle, Flow Orchestrator).
- Role-differentiated history views, where a critic and a pragmatist see different context. The Adversarial Critic raised this and no one addressed it.

## Open Questions

- How is dissent loss detected, given that dropped content is invisible by definition? The "defer until measured" plan has no measurement method yet.
- What happens when a single latest round exceeds the budget on its own (for example, seven long responses)? The transcript must say so, but the behavior beyond that is undefined.
- How does resume rebuild the identical window after a crash? Token-count boundaries can differ between runs. Nobody specified what is stored to guarantee the same history on resume.
- What do the existing context budget enforcement and discussion compression do today, and what do they cost on failure? The Systems Pragmatist said this was never examined, and the window design should be tested against it first.
- What is the exact overflow-retry rule after a context-overflow failure from the subprocess call?

## Ledger

### Q1: How should agent responses be truncated for long discussions
- DECIDED: Show full history by default; truncate only when the assembled prompt exceeds the configured size budget.
- DECIDED: The trigger is a size check tied to the engine's existing context budget enforcement, configured in the defaults file.
- DECIDED: When over budget, drop the oldest whole round first; never cut responses partway.
- DECIDED: Always keep the question and decided items in every prompt.
- DECIDED: Dropped rounds remain on disk in the transcript for synthesis.
- DECIDED: If a round is still over budget after eviction, state it visibly in the transcript; never trim silently.
- DECIDED: Define overflow-retry behavior before building; a context-overflow failure must not resend the same oversized prompt.
- DECIDED: Reject the disagreement spine, the output length cap, and neutral summarization for now.
- DECIDED: Keep first-round Position Summaries as a floor against eviction (Context Surgeon amendment, unopposed).
- CONTESTED: Cognitive Architect advocates a verbatim disagreement spine to preserve dissent; Flow Orchestrator, Adversarial Critic, Systems Pragmatist and both evaluators reject it as an unclassified extraction step.
- CONTESTED: Adversarial Critic advocates capping output length at generation; Systems Pragmatist and both evaluators reject it as unenforceable and not bounding history.
- OPEN: How is dissent loss detected once dropped content is invisible?
- OPEN: What happens when one round alone exceeds the budget?
- OPEN: How does resume rebuild an identical window after a crash?
- OPEN: What do existing budget enforcement and compression do today, and what do they cost on failure?
