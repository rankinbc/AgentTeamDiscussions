## Decisions Ledger

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

