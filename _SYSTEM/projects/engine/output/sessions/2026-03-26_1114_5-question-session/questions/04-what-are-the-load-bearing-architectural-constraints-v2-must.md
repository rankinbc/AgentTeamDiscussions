# What are the load-bearing architectural constraints V2 must work within?

*Generated: 2026-03-26 11:34 | Q4 | 270s | Mode: compete*

## Decisions

### D1: Measure the three mechanical constraints before designing V2 features

The Pragmatist's framework won consensus: payload size limits per Claude CLI call, wall-clock latency per session, and synthesis input quality are the three constraints that produce actionable numbers. All V2 feature proposals must be evaluated against measured values for these three, not estimated from code reading.

**Rationale:** Static code analysis (Flow Orchestrator) and pure observation (Critic) both fail to produce causal maps. The Architect's selective context proposal and the Flow Orchestrator's code-seam mapping are useful hypotheses but remain untestable without baseline measurements. Decision D3 from Q3 ("measurement before mechanism") already established this ordering constraint; this decision operationalizes it.

### D2: The Claude CLI subprocess boundary is the true flexibility ceiling

Every architectural change is filtered through stateless text-in, text-out subprocess calls. There is no conversation continuity between rounds — each round rebuilds full context from scratch. This means context management is not a feature but the cost model itself. V2 features that increase per-turn payload size have an unmeasured hard ceiling.

**Rationale:** Neither the Flow Orchestrator nor the Cognitive Architect examined this boundary directly. The Critic identified it; the Pragmatist explained why it matters mechanically. Until payload ceilings are measured, any V2 feature adding context (memory, cross-question references, accumulated history) is priced at unknown cost.

### D3: Code-seam rigidity is real but magnitude is unknown

The Flow Orchestrator correctly identified three structurally rigid points: the synchronous linear pipeline (SessionRunner through ClaudeRunner), hardcoded prompt assembly in BuildAgentPayload, and coupled round iteration with synthesis in DiscussionEngine. These are accurate inventory. However, "expensive" has no baseline — a BuildAgentPayload refactor may be days or weeks, and static analysis cannot distinguish.

**Rationale:** The Pragmatist's correction is accurate: knowing BuildAgentPayload is a chokepoint says nothing about magnitude. The Critic's challenge ("expensive compared to what?") remains unanswered. This inventory is useful for V2 planning but not sufficient for prioritization.

### D4: Context homogenization is an unproven hypothesis, not a confirmed constraint

The Cognitive Architect's thesis — that selective context exposure is the gating constraint for V2 — assumes agents would behave differently with different context. Q2-D3 established that context accumulation dominates identity by Round 2, but no evidence demonstrates that filtering context would restore differentiation. This is a testable hypothesis, not an architectural constraint.

**Rationale:** The Oracle and Surgeon both flagged this: proposing selective context exposure without first demonstrating that homogenization degrades output quality is solving an unmeasured problem. The idea has architectural merit but belongs in a hypothesis queue, not a constraint map.

### D5: Synthesis quality is the user-facing constraint that binds all others

Synthesis is a single LLM call over concatenated text. The quality ceiling of session output is determined by one Claude invocation digesting everything upstream. Payload size, agent differentiation, round structure, and context management all funnel through this single point. If synthesis cannot distinguish signal from noise, upstream sophistication is wasted.

**Rationale:** The Oracle correctly identified that synthesis quality is the only constraint the user directly experiences through the Morning Brief. The Pragmatist correctly identified it as mechanically measurable. Both perspectives converge: measure synthesis input quality first because it is simultaneously the user-facing bottleneck and the architectural funnel.

### D6: Round structure rigidity is a latency multiplier, not an architectural wall

The round structure (TeamMode dictionary iterated in insertion order) enforces sequential, synchronous agent execution. This is correctly identified as rigid, but the cost is primarily wall-clock time, not architectural impossibility. Five agents times three rounds times Claude response time equals session duration. Adaptive rounds, parallel execution, or early stopping require changes to DiscussionEngine's iteration logic, which is contained.

**Rationale:** The Flow Orchestrator overstated the cost of changing round structure. The Pragmatist reframed it as a latency problem with a linear multiplier, which is more precise and more actionable.

---

## Confirmed Constraint Map

### Rigid (structurally load-bearing)

| Constraint | What it blocks | Measurement needed |
|---|---|---|
| Claude CLI is stateless | Every round rebuilds full context; no conversation continuity | Max payload size before truncation or degradation |
| Pipeline is synchronous and serial | No parallel agent execution, no mid-round intervention | Wall-clock time per session at current and projected agent/round counts |
| Synthesis is a single LLM call | Output quality ceiling is one invocation over concatenated input | Synthesis input token count vs output quality correlation |

### Semi-rigid (contained refactor, not rearchitecture)

| Constraint | What it blocks | Estimated scope |
|---|---|---|
| BuildAgentPayload is hardcoded | Per-agent or per-round context customization | Method refactor, not architecture change |
| DiscussionEngine couples rounds and synthesis | Independent synthesis strategies per question | Extract synthesis to separate component |
| Round structure is a static dictionary | Adaptive rounds, conditional branching, early stopping | Iteration logic change in DiscussionEngine |

### Flexible (cheap to extend)

| Seam | What it enables |
|---|---|
| IClaudeRunner interface | Backend swaps, logging, retry policies, latency injection |
| IAgentLoader + team YAML | New agents, teams, modes without code changes |
| SessionPersistence (static utilities) | Format changes without touching orchestration |

### Unproven (hypothesis, not constraint)

| Hypothesis | Test required |
|---|---|
| Context homogenization degrades output quality | Compare brief quality from sessions with full vs filtered agent context |
| Selective context exposure restores agent differentiation | Run controlled sessions with per-agent context filtering |
| IClaudeRunner's raw text return blocks structured output features | Assess whether downstream parsing is sufficient vs requiring interface changes |

---

## V2 Planning Rules

1. **No feature enters the V2 list without a measured constraint it addresses.** Instrument payload size, session latency, and synthesis input quality first.
2. **Features touching BuildAgentPayload or DiscussionEngine iteration are medium-cost, not high-cost.** Plan accordingly — these are contained refactors.
3. **Features requiring parallel execution or agent-to-agent messaging are high-cost.** They break the synchronous pipeline assumption.
4. **The context homogenization hypothesis must be tested before any feature depends on it.** Run a controlled experiment comparing filtered vs full context before committing to selective exposure.
5. **Synthesis quality is the priority measurement.** If synthesis is the bottleneck, upstream features (better prompts, more rounds, adaptive structure) produce no user-visible improvement until synthesis improves.
6. **Wall-clock latency has a user tolerance ceiling.** Measure current session duration and establish the maximum acceptable duration before adding features that increase round or agent count.
<!-- complete -->
