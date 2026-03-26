# What is the right testing strategy for a system where correctness is subjective?

*Generated: 2026-03-26 12:39 | Q6 | 199s | Mode: compete*

## Decisions

### DECIDED: Two-Layer Testing Strategy — Mechanical and Human, No Middle Layer

The testing strategy splits cleanly into two layers with no automated quality proxy between them. Mechanical tests verify that the engine assembles prompts correctly and respects hard constraints. Quality assessment uses the already-decided paired human comparison framework. There is no structural prompt analysis layer, no LLM-as-judge, no embedding diversity metrics, and no automated divergence scoring.

### DECIDED: Mechanical Tests Cover V2 Prompt Assembly, Not Prompt Effectiveness

Mechanical tests verify that PromptBuilder produces correct output given known inputs. "Correct" means structurally compliant with the spec — not "likely to produce good discussion." The distinction matters: a test asserting that blind-round prompts exclude prior responses is a mechanical correctness check. A test asserting that prompts "contain conflict-forcing language" is an encoded hypothesis about what makes discussions work, and those hypotheses change faster than the test suite. Do not encode quality hypotheses as automated assertions.

### DECIDED: Specific Mechanical Test Targets for V2

The following properties are mechanically testable and must be covered:

- **Blind proposal exclusion.** During blind rounds, rendered prompts must not contain prior agent responses for the current question.
- **Agent identity token cap.** No agent identity block exceeds 800 tokens after rendering.
- **Template selection by round type.** Each round type resolves to the correct Scriban template.
- **Feature flag gating.** When a session-level flag is off, the corresponding prompt sections are absent. When on, they are present.
- **Eviction order.** When context exceeds budget, content is evicted in the hardcoded priority order (last-cut to first-cut).
- **Token utilization.** Rendered prompts allocate at least 70% of available budget to novel content for the current round, not restated context from prior rounds or duplicate decision blocks.
- **No duplicate context blocks.** PromptBuilder must not include the same content (decisions, prior responses, identity blocks) more than once in a single rendered prompt.

### DECIDED: All Quality Validation Uses Paired Human Comparison

Output quality — whether a discussion produced genuine intellectual friction, whether agents avoided sycophancy, whether the Morning Brief surfaced perspectives the user wouldn't have found alone — is assessed exclusively through the paired human comparison framework already decided in Q5. The evaluation question remains: "Did V2 surface a perspective V1 missed?" Five paired runs before declaring success or failure. Measurement infrastructure is a spreadsheet.

### DECIDED: No Temporal Regression Detection in V2

Detecting when previously-effective prompts stop working (due to model version changes or behavioral drift) requires a stable baseline and statistical power that do not exist at N < 20. Temporal regression detection is a real concern but is not actionable at current scale. Revisit after twenty completed sessions provide enough data to define a baseline.

### DECIDED: No Structural Prompt Content Assertions Beyond Template Correctness

Tests must not assert the presence of specific rhetorical patterns, constraint language, or "friction-inducing" phrasing in rendered prompts. These assertions encode assumptions about what makes prompts effective — assumptions that change with every iteration on output quality. Template correctness (the right template rendered with the right variables) is testable. Prompt design effectiveness is not. The feedback loop for prompt design is the human reading the Morning Brief, not a test suite.

### DECIDED: No LLM-as-Judge, No Embedding Metrics, No Automated Quality Scoring

This reaffirms and extends existing decisions. LLM-as-judge introduces its own subjectivity and a runtime dependency. Embedding diversity metrics require infrastructure with no clear threshold for "enough diversity." Both contradict the decision against automated divergence scoring. The only automated signal is anti-coordination scoring, which ships always-on as instrumentation, not as a quality gate.

---

## Rationale

The core tension in this discussion was where to draw the line between mechanical testing and quality judgment. Three positions emerged:

1. **Clean binary** (Flow Orchestrator): mechanical tests for assembly, human comparison for quality, nothing between.
2. **Structural middle layer** (Cognitive Architect): test whether prompts contain the preconditions for divergent output — conflict language, position-forcing requirements, cross-agent tension.
3. **Temporal regression** (Adversarial Critic): track prompt-to-output coupling over time to detect when effective prompts stop working.

The structural middle layer failed because it encodes hypotheses about prompt effectiveness as test assertions. Those hypotheses are the builder's mental model of what works, which evolves with every session. Tests that encode yesterday's assumptions become maintenance burden without improving output. The feedback loop for "is this prompt design working" is already covered by paired human comparison.

Temporal regression failed on feasibility. It requires statistical power (stable baselines, sufficient N) that does not exist and will not exist in V2's timeframe. The concern is legitimate and should be revisited at N > 20.

The clean binary won with two sharpening additions from the Context Surgeon: token utilization assertions and duplicate context detection. These are mechanical properties with clear pass/fail thresholds that directly impact output quality without attempting to measure it.

---

## Validation Sequence

1. Write mechanical tests for the seven targets listed above.
2. Ship blind proposals with those tests green.
3. Run five paired V1/V2 sessions using the human comparison framework.
4. Record results in the spreadsheet.
5. After twenty sessions, revisit whether temporal regression detection is warranted.

---

## What Counts as "Better"

Unchanged from Q5 decisions. A human reads two Morning Briefs (V1 and V2, same topic) and answers: "Did V2 surface a perspective V1 missed?" The thirty-second read of the Morning Brief is a better quality signal than any automated proxy at this scale.

---

## When to Revisit

- **After 20 completed sessions:** Sufficient data may exist to define output baselines and consider regression detection.
- **After a Claude model version change:** If output quality shifts noticeably, the mechanical test suite will not catch it. The human comparison framework will. Run a paired session immediately after any model update.
- **If the team grows beyond one builder:** A second person reading Morning Briefs changes the calculus on what "subjective" means. Inter-rater reliability becomes relevant. Still not automated — but worth tracking agreement rates in the spreadsheet.
<!-- complete -->
