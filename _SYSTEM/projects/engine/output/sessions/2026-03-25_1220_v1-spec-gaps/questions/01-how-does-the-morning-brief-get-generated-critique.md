### The Systems Pragmatist (infrastructure realist)

**The incremental vs. all-at-once question is already answered by the architecture.** If you're doing rolling synthesis after each question, the Morning Brief *is* the brief at session end. There's no separate final pass. Treat them as one thing or you're building two systems.

**The real failure modes:**

1. **Context overflow is the actual problem.** Ten design docs at 800 tokens each is 8K tokens of input before your prompt. Fine for now. At 20 questions with verbose outputs, you're over 16K just in docs. The rolling approach sidesteps this — you only ever pass `previous_brief + latest_design_doc`, not the full history. That's the winning argument for incremental, not "readable mid-session."

2. **Brief drift is undetectable.** If the synthesis call subtly drops a risk flag or misrepresents a decision across 10 rounds, you won't know until you read the final output. The `brief_history/` subfolder proposed in the last round is the only audit mechanism. That's load-bearing — don't treat it as optional.

3. **Fallback creates a different artifact.** The proposed fallback (append decisions to brief.md) produces a structured list, not a synthesized narrative. That's fine as a degradation mode, but label it — write `## FALLBACK: Synthesis Failed` so the user knows what they're reading.

**What needs designing right now:** The synthesis prompt. Specifically — what's the token budget for the output brief, and what sections are required? Without that contract, the rolling chain has no termination condition and the brief grows unbounded.

That's the blocking question. Everything else is implementation detail.

### The Adversarial Critic (adversarial reviewer)

**Three problems nobody has solved:**

**1. Synthesis compounds, not just drifts.** Rolling synthesis doesn't just *drift* — it permanently discards. If round 4's synthesis drops a risk flag from round 2, rounds 5–10 never see it. `brief_history/` lets you *detect* this after the fact. It doesn't prevent it. You need a mechanism that preserves high-confidence decisions across the chain, not just an audit log.

**2. The fallback poisons the chain.** If synthesis fails on round 6, you append raw decisions to `brief.md`. Round 7's synthesis call then receives a hybrid document — part narrative, part structured list — and synthesizes *that*. The fallback doesn't degrade gracefully; it corrupts the input contract for every subsequent call. The fix is a separate `brief_fallback.md` that the chain never reads from.

**3. "600 token cap" is unenforceable.** You can set `max_tokens=600` on the API call. The model will truncate mid-sentence. That's not a brief — that's a truncated brief that *looks* complete. The output contract needs a structured format (fixed sections, each with a word budget) that the prompt enforces, not the token limit.

**The Pragmatist is right that the synthesis prompt is blocking.** But the required sections aren't just a formatting question — they're the anti-corruption layer for the rolling chain. Without explicit sections like `## Preserved Decisions` and `## Active Risk Flags`, each synthesis call decides what's worth keeping. That's too much discretion.

Design the prompt sections first. Everything else follows.


<!-- complete -->
