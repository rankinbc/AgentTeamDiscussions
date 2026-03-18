# How do we make the evaluation feedback loop reliable?

*Generated: 2026-03-18 04:04 | Question 7 | 123s | Mode: compete*

## Decisions

### D1: One Dimension Per Evaluation Call

Each scoring dimension is evaluated in its own separate `claude -p` invocation. The prompt contains the artifact being scored, one dimension name with its definition, a 1-5 rubric with behavioral anchors, and an instruction to output a single integer score with one sentence of justification.

A multi-dimension prompt is an open-ended generation task that invites the model to reinterpret the scoring structure. A single-dimension prompt is a classification task. These are cognitively different operations for the LLM. The model picks from a rubric instead of inventing one.

Cost is 8-10 CLI calls per evaluation instead of 1. Each call carries minimal context: one artifact (fixed), one dimension definition (~50 tokens), one rubric (~100 tokens), one instruction (~30 tokens). No accumulated state across calls. This is the cheapest prompt pattern in the system.

### D2: Dimensions and Rubrics Live in a Static YAML File

`eval_dimensions.yaml` defines every scoring dimension. Each entry contains: dimension name, one-sentence definition, and five behavioral anchors (one per score level). The evaluator loads this file, iterates over its entries, and injects each into a single-dimension prompt.

Adding a dimension means adding a YAML block. Removing one means deleting it. Scores are always keyed to registered dimension names because no other names exist in any prompt. The LLM never chooses dimension names, defines rubrics, or structures output format.

Rubric anchors must include concrete failure indicators for low scores, not only success indicators for high ones. "Score 1: the design doc contains no extractable decisions" is testable. "Score 1: poor quality" is not. Without low-end anchors, score distributions compress into the 3-5 range and lose discriminating power.

### D3: Scores Are Extracted by Regex, Not by Parsing Prose

The prompt instructs the LLM to emit each score on a line matching the pattern `SCORE: {1-5}`. The evaluator extracts the integer with a regex match. Anything that does not match the pattern is treated as a failed evaluation, not reinterpreted.

If the regex match fails, the call is retried up to 2 times. After 2 failed retries, the dimension score is recorded as `null` with a logged reason. No infinite retry loops. No heuristic reinterpretation of malformed output. Null scores surface in the Morning Brief as "could not evaluate" rather than silently disappearing.

### D4: Rubric Versioning Is a Hard Gate

The rubric file carries a version string. Every session's evaluation output records which rubric version produced the scores. The orchestrator refuses to programmatically compare or diff scores produced under different rubric versions. A version mismatch is a blocking condition for any cross-session comparison logic, not a logged warning.

Rubric anchors are natural language interpreted by an LLM. The model's interpretation of anchor text can shift across Claude versions and prompt changes. Scores are comparable within a session and across sessions using the same rubric version. Cross-version comparability is not a V1 goal.

### D5: Evaluation Gates Human Attention, Not Automated Reruns

For V1, evaluation produces a morning report that helps the user triage which design docs are sharp, which are weak, and which questions deserve a rerun. It does not gate automated rerun loops or closed-loop optimization.

This means directional accuracy within a single session is sufficient. Scores need to correctly rank five design docs against each other today. Cross-month reproducibility, dimension independence testing, and calibration data collection are V2 concerns.

Automated gating ("score below 3, rerun the question") requires reliability guarantees that depend on calibration data the project does not yet have. Building automated gating before collecting that data means building on assumptions. Build the morning report. Measure score stability across sessions. Decide on automated gating when the data exists.

### D6: Evaluation Produces Suggested Follow-ups

After scoring all dimensions for a session's design docs, the evaluator generates `suggested_followups.md`. This artifact maps low-scoring dimensions back to the question topics that produced them and proposes follow-up questions for the next session.

A design doc that scores low on Decision Clarity signals a follow-up question targeting that gap. This is the feedback loop that compounds across sessions: evaluation informs the next session's question list, not just the current session's quality report.

The mapping is mechanical: for each dimension score below a configurable threshold (default: 3), emit the question topic and the dimension name as a suggested follow-up target. The user edits this list before the next run. No automated queue insertion.

### D7: Self-Evaluation Bias Is a Documented Limitation

When the same model that produced an artifact also scores it, expect inflated scores. This is a known LLM self-evaluation bias. For V1, this is documented as a limitation in the session output metadata. The scores remain useful for relative ranking within a session (all artifacts share the same bias) but not for absolute quality claims.

For V2, mitigation options include using a different model for evaluation calls, adjusting temperature, or introducing a calibration step against human-scored reference artifacts.

---

## Resolved Open Questions

**Topic tag vocabulary** (from Q5): Use free-form tags. A fixed vocabulary requires a classification step that would itself need evaluation, creating a recursive problem. Free-form tags cost nothing, serve human scanning of the ledger, and can be retroactively normalized if a fixed vocabulary proves necessary later.

## Remaining Open Questions

- **Extraction loss rate** (from Q5): What percentage of meaningful constraints survive extraction into the ledger? Not addressed by evaluation design. Requires manual comparison of beta transcripts against ledger output.
- **Supersession clarity** (from Q5): Whether agents reliably infer that later decisions supersede earlier ones from chronological order alone. Unaffected by evaluation design. Monitor in practice; add "SUPERSEDES Q{n}" tags if inference proves unreliable.
- **Dimension independence**: Single-dimension evaluation assumes dimensions are independent. "Decision Clarity" and "Constraint Specificity" are correlated. Whether context deprivation (scoring one at a time) produces different numbers than context contamination (scoring all at once) is an empirical question. For V1, accept the tradeoff. If score patterns look anomalous, test multi-dimension prompts as a comparison in V2.
- **Structured output compliance rate**: The reliability of `claude -p` producing the expected `SCORE: {1-5}` format without system prompt enforcement has not been measured. The 2-retry cap with null fallback handles failures, but if the failure rate exceeds ~20%, the prompt format or model configuration needs adjustment. Measure compliance rate in the first real session and adjust.