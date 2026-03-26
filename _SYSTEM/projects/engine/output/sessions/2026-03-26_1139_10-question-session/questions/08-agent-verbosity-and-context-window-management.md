# Agent verbosity and context window management.

*Generated: 2026-03-26 12:10 | Q8 | 209s | Mode: compete*

## Decisions

### Primary Decision: Log Total Assembled Prompt Size Per ClaudeRunner Invocation

**Status:** DECIDED

Add a single instrumentation point: before each `ClaudeRunner` subprocess call, log the total character/token count of the assembled prompt string. This is the sole V2 change for context window management.

**Rationale:** The discussion converged decisively on one insight — the system currently has zero visibility into the actual constraint that matters. The context window limit is not a per-response verbosity problem; it is a prompt assembly size problem. Every agent call is a fresh subprocess invocation with a fully constructed prompt. There is no persistent context window being managed across turns. The failure mode is not "agents talk too much" but "PromptBuilder assembles a prompt that approaches or exceeds the model's context window, and nobody knows."

One number per invocation — total assembled prompt size — captures the critical signal with zero runtime cost, zero new dependencies, and zero user-facing complexity.

**Evidence from this session:** The Context Surgeon observed that the decisions block fed into this session's own prompts contained every prior question duplicated verbatim, inflating context by roughly 40%. This is not a hypothetical risk. Structural waste in prompt assembly is already present and unmeasured.

**Implementation scope:**
- Log the byte/character length of the final prompt string in `ClaudeRunner` before the subprocess call
- Write to the existing session output logging path
- No new config. No new flags. No new subsystems.

### Secondary Decision: Role-Selective Context Curation Is Rejected

**Status:** REJECTED

The Cognitive Architect proposed filtering what each agent receives based on their cognitive function — a fourth layer in `PromptBuilder` that curates context per agent role. This was rejected on three independent grounds:

1. **Premature.** No data exists showing that context volume degrades output. The Q2 decision to instrument before allocating has not been fulfilled. Building a filtering system before a measurement system inverts the correct order.

2. **Undebuggable.** Filtering creates information asymmetry bugs that are invisible in output. An agent responding to a conversation it partially didn't see produces phantom disagreements that trace back to a dropped paragraph in the curation layer. Debugging this failure class is significantly harder than debugging verbosity.

3. **Architecturally misframed.** In a subprocess-per-call architecture, there is no live context window to filter. Each invocation gets a fully assembled prompt. "Curation" is just prompt engineering with an additional abstraction layer and a new failure surface. It would hide structural bloat (like duplicate decision blocks) instead of exposing it.

If instrumentation data eventually confirms that context volume is degrading output, filtering may be revisited — but as a prompt engineering refinement, not a runtime subsystem.

### Tertiary Decision: Output-Only Logging Is Insufficient

**Status:** DECIDED (scope clarification)

Logging response token counts (what agents produce) was proposed by the Flow Orchestrator as consistent with the Q2 instrumentation commitment. The Critic and Pragmatist identified the gap: the critical failure mode is silent input truncation, not output verbosity. What the model receives determines quality; what it produces is a symptom.

Output token counts may be added alongside input measurement if cheap to capture, but they are not the primary diagnostic signal. The assembled prompt size is.

---

## Design Rules

### What Gets Logged

For every `ClaudeRunner` invocation:
- Total assembled prompt size (characters and estimated tokens)
- Agent key and round identifier
- Timestamp

This data writes to the session output directory alongside existing session artifacts.

### What Does Not Change

- The 250-word soft limit remains advisory. No hard token limits are introduced.
- No CLI flags for token control in V2.
- No SDK migration. The subprocess model (`claude -p`) is retained.
- No per-agent context filtering. No fourth `PromptBuilder` layer.
- No runtime intervention or dynamic truncation.

### What This Enables

Once assembled prompt sizes are visible across sessions:
- Identify which questions, rounds, or agent counts push prompts toward the context ceiling
- Detect structural waste in prompt assembly (duplicate blocks, verbose formatting, unnecessary context repetition)
- Establish a baseline for "normal" vs "at risk" prompt sizes per invocation type
- Make evidence-based decisions about whether intervention is needed and what shape it should take

### The Instrumentation Gate

This question is reopened only when data shows one of:
- Assembled prompts routinely exceed 80% of the model's context window
- Output quality (measured via evaluation scores) correlates negatively with prompt size
- Specific agents or round positions consistently produce degraded responses traceable to context pressure

Until one of these conditions is met, no filtering, curation, or enforcement mechanism is designed or built.

---

## Rejected Alternatives

| Alternative | Proposed By | Rejection Reason |
|---|---|---|
| Role-selective context curation | Cognitive Architect | Premature, undebuggable, architecturally misframed for subprocess model |
| Hard token limits via CLI flags | Original question | Blunt instrument that degrades output quality; treats volume as the problem instead of signal-to-noise |
| SDK migration for token control | Original question | No evidence the subprocess model is the bottleneck; migration cost unjustified without data |
| Per-agent context filtering by personality | Original question | Subset of curation proposal; same objections apply |
| Output-only token logging | Flow Orchestrator | Misses the critical failure mode (input truncation); necessary but not sufficient |
| Input and output token decomposition | Adversarial Critic | Correct in spirit but over-scoped for V2; assembled prompt size captures the primary signal |

---

## Consistency With Prior Decisions

This decision is a direct continuation of the Q2 commitment to "Instrument Before Allocating" and the Q5 commitment to "Instrument Output Quality Post-Hoc." It fulfills the measurement prerequisite that multiple prior questions deferred to. It does not conflict with any prior decision.

The Context Surgeon's observation about duplicate decision blocks in this session's own prompts validates the Q7 tertiary decision that "Context Hygiene Is the Highest-Leverage Anti-Convergence Intervention Available Today." Measuring prompt assembly size is the first step toward context hygiene — you cannot clean what you cannot see.
<!-- complete -->
