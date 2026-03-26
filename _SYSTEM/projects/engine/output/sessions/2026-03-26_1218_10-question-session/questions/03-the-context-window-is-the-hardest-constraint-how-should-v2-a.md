# The context window is the hardest constraint. How should V2 allocate it?

*Generated: 2026-03-26 12:29 | Q3 | 224s | Mode: compete*

## Decisions

### DECIDED: Priority-Queue Eviction, Not Percentage Budgets

Context window allocation is a runtime degradation problem, not a design-time allocation problem. The engine uses a deterministic eviction order rather than percentage-based budgets. When the context window fills, categories are cut in a fixed sequence. Percentages are not assigned upfront; the budget for variable-cost items (conversation history, prior docs) is whatever remains after fixed-cost items are placed.

**Rationale:** All four discussants who proposed percentage budgets (fixed, phased, or inverted) were unable to answer the only question that matters: what gets cut when the window fills? A priority queue answers this directly. Percentages can be derived later from instrumented data if needed, but are never the foundational abstraction.

### DECIDED: Hardcoded Eviction Order (Last-Cut to First-Cut)

When context pressure requires trimming, categories are evicted in this order:

1. **Never cut:** Task instructions + output format (the agent must know what to do and how to respond)
2. **Last cut:** Current round stimulus (what agents are responding to -- other agents' outputs for the active round)
3. **Protected:** Decision summaries from session manifest (compact summary of already-decided positions; cap at 500 tokens but cut only under extreme pressure)
4. **Protected:** Conversation history from prior rounds on the current question (recency-weighted: current round verbatim, previous round as key claims, earlier rounds as position tags only)
5. **Early cut:** Agent identity (personality + position layers only; hard cap at 800 tokens per agent regardless of YAML source length)
6. **First cut:** Prior design docs and conversation history from other questions (summarize aggressively, then drop entirely if needed)

**Rationale:** This order is derived from user-visible impact on the Morning Brief, not engineering convenience:

- **Conversation history loss is the most damaging cut.** When agents lose prior round context, synthesis collapses into repetition. The Morning Brief becomes shallow and redundant. This was the strongest consensus point across all discussants.
- **Decision summary loss causes contradictions.** Agents re-litigate settled questions, producing the most user-visible failure mode ("didn't we already decide this?").
- **Identity loss is nearly invisible to users.** Whether an agent has 3 sentences or 3 paragraphs of persona, the synthesized output reads the same. Identity matters most in Round 1 (blind proposals) where it is the only differentiator, but even there, 800 tokens is sufficient for behavioral differentiation.
- **Prior design docs from other questions are the cheapest to lose.** They provide cross-question coherence but can be replaced with a compact summary of decisions without meaningful quality loss.

### DECIDED: Conversation History Uses Tiered Summarization

Conversation history is not truncated -- it is summarized in tiers based on recency:

| Distance from current round | Representation |
|---|---|
| Current round | Verbatim |
| Previous round | Key claims + supporting evidence |
| Earlier rounds | Position tags only (agent name + stance + one sentence) |

**Rationale:** This mirrors how experts track a live debate. It preserves the structure of disagreement (who argued what) while compressing the elaboration. Hard truncation mid-sentence or FIFO eviction destroys the thread of reasoning; tiered summarization degrades gracefully.

Summaries must be versioned (stored alongside raw transcripts) so that diagnostic review can trace why an agent responded as it did. Summarization without versioning makes debugging impossible.

### DECIDED: Round Type Determines Available Budget, Not a Profile Lookup

Different rounds have structurally different context compositions. This is not handled through phase-aware budget profiles but through the natural consequence of the eviction order applied to what exists:

- **Blind proposals (Round 1):** No conversation history exists. The space is naturally available for substrate and identity. No special profile needed.
- **Reactive rounds (critique/evaluate):** Conversation history grows. The eviction order handles pressure automatically -- identity compresses, history is retained.
- **Synthesis:** The synthesizer prompt is a different prompt entirely. Identity drops to near-zero; substrate and decision summaries dominate.

**Rationale:** Static phase profiles (blind/reactive/synthesis) triple the tuning surface without solving truncation. The Orchestrator's observation that different rounds have different needs is correct, but the eviction order already handles this without additional configuration. Round 1 doesn't need a "blind profile" -- it needs the same eviction logic applied to a context that happens to contain no history.

### DECIDED: Agent Identity Hard-Capped at 800 Tokens Per Agent

Agent YAML files contain six layers (personality, position, technique, anti-slop, voice, output format). Not all of these are loaded into every prompt. The identity payload sent to the LLM is capped at 800 tokens and prioritizes:

1. Position (what they advocate)
2. Personality (how they think)
3. Technique (analytical approach)

Voice, anti-slop, and output format are handled through task instructions, not identity. They do not count against the identity cap.

**Rationale:** Behavioral differentiation in LLMs comes primarily from what agents are responding to, not from self-description. A 500-token rival argument produces more differentiation than 500 tokens of personality elaboration. However, identity cannot be zero -- in blind proposals it is the only differentiator. 800 tokens is sufficient for meaningful behavioral shaping without consuming space needed for substance.

### DECIDED: Instrument V1 Before Tuning V2

The eviction order ships as the architecture. But the specific caps (800 tokens identity, 500 tokens decisions) and the summarization thresholds are initial values to be validated through instrumentation. The first V2 deliverable after blind proposals includes:

- Token counting per category on real V1 sessions
- Logging of actual context composition at each round
- Morning Brief quality comparison under simulated degradation levels

Caps are adjusted based on data. The eviction *order* is not expected to change; the *thresholds* at which each tier triggers are tuning parameters.

**Rationale:** The Critic's core objection -- that both percentage and profile proposals were assigning values to unmeasured quantities -- is valid. The eviction order does not require measurement to ship (it is a logical priority, not an empirical one), but the specific numbers do require validation. Instrument, then tune.

## Rules

1. **The eviction order is deterministic and hardcoded.** No runtime negotiation of priorities. PromptBuilder applies the order mechanically.
2. **Never cut task instructions.** An agent that doesn't know what to do produces garbage regardless of how much context it has.
3. **Never hard-truncate conversation history mid-thought.** Always summarize to the next tier before evicting. FIFO truncation destroys reasoning threads.
4. **Version all summaries.** Raw transcripts are retained on disk. Summaries stored in prompt context must be reproducible from the raw source for debugging.
5. **Identity cap is per-agent, not per-session.** 800 tokens each, regardless of team size. A 7-agent team uses 5600 tokens on identity. This is acceptable.
6. **Decision summaries are append-only and compact.** One line per decision. The decisions ledger is the source; the prompt gets a compressed extract.
7. **Reserve 5% of the context window as overflow buffer.** Never allocate proactively. This absorbs estimation errors in token counting.
8. **Validate the eviction order by reading Morning Briefs, not by counting tokens.** The quality metric is user-visible output, not engineering metrics. If a Morning Brief degrades under a specific cut, the order is wrong regardless of what the token numbers say.
<!-- complete -->
