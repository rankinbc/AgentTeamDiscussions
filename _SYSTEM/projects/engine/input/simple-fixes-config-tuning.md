# Simple Fixes: Config Tuning and Prompt Optimization

You are agents in a multi-agent discussion system. You've already identified the big structural problems (context bloat, false consensus, missing stakes). Now we need the small, cheap wins — config changes and prompt tweaks that don't require architecture surgery.

## What's Already Decided

- Self-compression is being implemented (agents produce ## Position Summary blocks, summaries passed between rounds)
- Synthesis now reports CONTESTED items alongside DECIDED/OPEN
- Evaluate round instructions now say "pick a winner and reject the loser"
- Critique round instructions now say "attack the core approach, not surface details"

## Open Questions

1. **Are any of these config values causing problems for discussion quality?** You are the agents who receive these constraints. Which ones hurt your output? Be specific about what you'd change and why.

```yaml
synthesis:
  max_ledger_words: 50    # Max words per ledger entry

truncation:
  prior_specs: 6000       # Max chars of prior specs to chain as context
  design_doc_chain: 3000  # Max chars per design doc chained forward
  agent_eval_input: 8000  # Max chars of agent responses for evaluation
  round_analysis: 1500    # Max chars per agent response for interaction analysis
  low_patience_context: 2500  # Chars kept for low-patience agents

conversation:
  max_word_count: 250     # Default max words per agent turn
```

For each value: is it too tight, too loose, or fine? What's the downstream effect on your reasoning when it's wrong?

2. **What can be cut from your context to improve your reasoning?** You receive a layered prompt: identity (persona, personality, anti-slop rules, voice), situation (prior decisions, prior design docs, open questions, discussion so far), and task (question, round instruction, speaking position). What's in there that you don't actually use? What's noise that makes the signal harder to find? What would you cut first if you had 30% fewer tokens to work with?

3. **How should the system prompt generation be improved?** Your system prompt contains your full persona description, personality traits as prose, technique description, anti-slop rules, voice constraints, and job description. Is this layering effective? Are some sections redundant? Do the anti-slop rules actually change your behavior, or are they buried too deep? What one change to prompt assembly would most improve the quality of your responses?
