# How do we handle the personality system transition?

*Generated: 2026-03-26 12:46 | Q8 | 203s | Mode: compete*

## Decisions

### DECIDED: Swap Test Is the Mandatory Gate Before Any Personality Transition Work

No compression, instrumentation, or migration work begins until a two-run swap test demonstrates that agent personality layers produce user-detectable differences in session output. The swap test exchanges the identity stacks of two agents (cognitive_architect and adversarial_critic), runs the same brief, and compares Morning Brief output. If the user cannot identify which brief used swapped agents without being told, personality is decorative and transition planning is deprioritized.

**Rationale:** All proposed transition strategies assume personality layers are load-bearing. The swap test is the cheapest possible experiment to validate that assumption. Two brief runs versus weeks of compression or instrumentation work on a potentially decorative system component.

### DECIDED: The Detection Threshold Is Blind Identification

The swap test passes (personality is decorative) if the user reads two Morning Briefs and cannot identify which one used swapped agent identities without being told. No scoring rubric, no LLM-as-judge. Binary human judgment: "Can you tell which is which?"

**Rationale:** The product is the Morning Brief. If swapped personalities produce indistinguishable output to the person reading it, the distinction has no user-facing value regardless of what automated metrics might detect.

### DECIDED: If Personality Is Decorative, Write BITs Fresh Without Migration

If the swap test demonstrates personality layers do not produce user-detectable output differences, skip the entire transition problem. Write BIT-based agent definitions from scratch optimized for evaluation criteria and behavioral constraints. No need to preserve V1 identity layers, no compression exercise, no A/B testing.

**Rationale:** You cannot "lose the good parts" of a system component that produces no measurable effect. Fresh BIT authoring focused on what agents optimize for is simpler and more honest than compressing narrative that was not doing work.

### DECIDED: If Personality Is Load-Bearing, Use Sequential Single-Agent Compression

If the swap test demonstrates personality layers do produce user-detectable output differences, compress agents one at a time using paired comparison after each. Start with the agent whose V1 output is most distinctive. Each compression informs the next.

**Rationale:** Sequential compression provides seven failure-detection points instead of one. The cost is six extra brief runs, which is trivial compared to discovering all seven agents degraded simultaneously with no signal about which compression failed.

### DECIDED: V1 Agent YAML Files Are Preserved as Rollback, Not Deleted

Regardless of transition path, V1 agent definition YAML files are retained in a `data/agents/v1-archive/` directory. Rollback is a file swap, not a reconstruction.

**Rationale:** Agent definitions are small YAML files. Storage cost is zero. Reconstruction cost from memory is nonzero and error-prone.

### DECIDED: No A/B Testing of Personality Systems

Agent personality comparison uses the already-decided paired human comparison framework (five paired runs, human judgment). No runtime A/B testing, no automated divergence scoring, no split-traffic experiments.

**Rationale:** A/B testing personality systems at N=5 cannot distinguish signal from stochastic LLM variance. The decided validation framework already covers this use case. Adding A/B infrastructure is engineering effort that produces noise, not data.

### DECIDED: Personality Transition Does Not Block the Critical Path

The swap test and any resulting transition work are independent of blind proposals, which ship first per prior decisions. Personality transition is scheduled after blind proposals are validated and shipping.

**Rationale:** Blind proposals have known, direct impact on session output quality. Personality transition has unproven impact. Engineering attention goes to proven value first.

### DECIDED: Round Structure and Positional Context Are Acknowledged as Potentially Dominant Factors

The swap test implicitly tests whether round mechanics (speaking order, phase structure, prior-response context) dominate personality in determining agent output character. If swapped identities produce identical output, positional pressure is the primary driver and future investment shifts to round mechanics over personality engineering.

**Rationale:** The system has two candidate explanations for agent behavioral differentiation: personality prompts and positional mechanics. The swap test distinguishes between them at near-zero cost. Whichever wins should receive the engineering investment.

---

## Execution Sequence

1. **Run swap test.** Exchange cognitive_architect and adversarial_critic identity stacks. Run one existing brief through both configurations. Present both Morning Briefs to user for blind identification.

2. **Branch on result.**
   - User cannot distinguish: personality is decorative. Write BIT definitions fresh. Archive V1 YAML. No migration needed.
   - User can distinguish: personality is load-bearing. Proceed to sequential compression starting with the most distinctive agent.

3. **If sequential compression:** compress one agent to BIT format, run paired comparison against the same brief, confirm Morning Brief quality holds. Repeat for each agent. Stop and investigate if any compression degrades output.

4. **Archive V1 definitions** in `data/agents/v1-archive/` regardless of path taken.

---

## What Was Rejected

| Proposal | Reason for Rejection |
|---|---|
| Bulk extract-and-replace of all agents simultaneously | No feedback mechanism to identify which compression failed if output degrades. Seven simultaneous changes with one detection point. |
| Pre-instrumentation of V1 identity layers | Requires the same experimental rigor (independent layer variation, N>20) that was already declared impractical. Replaces one unmeasured intervention with another. |
| A/B testing old vs new agent definitions | Cannot distinguish personality effects from stochastic variance at achievable sample sizes. Produces noise, not signal. |
| Gradual migration with mixed V1/V2 agents | Introduces confounding interactions between old and new formats. Validates nothing because the baseline shifts with each change. |
| Automated quality scoring of personality effects | Already decided: no LLM-as-judge, no embedding metrics, no automated quality scoring. Human judgment is the validation mechanism. |

---

## Open Questions Deferred

- **Which specific BIT format to use** is deferred until after the swap test determines whether BITs replace decorative or load-bearing personality layers. The format requirements differ significantly between those cases.
- **Whether the 800-token agent identity cap applies to BIT definitions** is deferred. BITs may be dramatically shorter (25-50 tokens per agent), making the cap irrelevant, or they may require structured metadata that approaches the cap.
- **How ego simulation and graduated resistance interact with BIT-based identities** is deferred until BIT format is defined. These are team YAML configuration per prior decisions, but their expression may change if personality layers are restructured.
<!-- complete -->
