# The BIT System (Beliefs, Instincts, Traits) vs the current 6-layer agent model.

*Generated: 2026-03-26 11:42 | Q1 | 204s | Mode: compete*

## Decisions

### Primary Decision: Run a Controlled Bake-Off Before Committing to Either Architecture

The team reached consensus that the theoretical debate between BITs and the 6-layer model has exhausted itself without producing testable claims. No participant successfully defended continued theoretical discussion over empirical testing.

**What was decided:**

- A structured bake-off will compare BITs-only identity against the current 6-layer system.
- The bake-off produces the evidence needed to commit to one architecture. No hybrid or incremental migration until results are in.

**What was rejected:**

- Wholesale replacement of the 6-layer model based on theoretical arguments alone (Cognitive Architect's initial position).
- Layering BITs on top of the existing system (original question's alternative). Hybrids obscure which mechanism does the work.
- Demanding formal failure proof before testing alternatives (Adversarial Critic's conservative stance). Agent tone convergence by round 3 is the observed failure mode that motivated this question.

---

## Bake-Off Protocol

### Test Design

| Parameter | Value |
|-----------|-------|
| Configurations | 2: current 6-layer system vs BITs-only replacement |
| Sessions per config | 3 minimum |
| Same brief/topic | Yes, identical inputs across both configs |
| Same team composition | Yes, same agent roles |
| Scoring | Blind (evaluator does not know which config produced which output) |
| Time budget | 48 hours maximum |

### BITs-Only Test Configuration

Each agent identity is reduced to:

- **3 BITs** (Beliefs, Instincts, Traits), each structured as:
  - `conviction`: A stated belief the agent holds.
  - `because`: The causal reasoning behind the conviction.
  - `triggers_when`: The discussion conditions that activate this belief.
- **1 voice constraint block**: Sentence length range, jargon policy, hedging tolerance, and output format rules.

No personality layer. No position layer. No technique layer. No anti-slop layer. The test must isolate motivation-driven identity cleanly.

### Current System Test Configuration

Run with the existing 6-layer agent model unchanged. No modifications, no BIT additions.

### Prompt Architecture for BITs Version

Two segments only, loaded in order:

1. **Motivation block**: The 3 BITs, rendered as structured prompt content. Placed first so the model anchors on identity before processing conversation context.
2. **Task constraint block**: Output format, length limits, voice rules. Placed second to frame the response shape.

This follows the Orchestrator's observation that prompt ordering determines attention allocation, while testing the Architect's claim that BITs alone are sufficient.

### Evaluation Criteria

Score each session's Morning Brief and design documents on one primary metric:

**"Did this output surface a perspective the evaluator would not have reached alone?"**

For each question's design doc and the overall Morning Brief, mark individual insights as:

- **Novel**: A perspective, framing, or tradeoff the evaluator had not considered.
- **Expected**: A perspective the evaluator would have reached independently.
- **Redundant**: A perspective that repeats another agent's point without adding value.

Count novel insights per session. Compare totals across configurations.

### Blind Scoring Protocol

To mitigate confirmation bias from a single evaluator who designed the system:

- Strip agent names and configuration identifiers from outputs before scoring.
- Score all 6 sessions in randomized order in a single sitting.
- Record scores before unblinding which configuration produced which session.

### What the Bake-Off Resolves

| If BITs-only wins | If current system wins | If no significant difference |
|---|---|---|
| Replace the 6-layer model with BITs + voice constraints. Proceed to calibrate BIT count per agent empirically. | Keep the 6-layer model. Investigate convergence fix within the existing architecture (likely a task-framing change, not an identity change). | The identity model is not the bottleneck. Investigate round structure, synthesis prompts, or conversation context management instead. |

---

## Open Questions Surfaced But Not Resolved

These emerged during discussion and remain unanswered. The bake-off may inform some of them.

1. **Optimal BIT count**: The Architect asserts 3. The Orchestrator argues the number should be empirical. The bake-off tests 3; if BITs win, subsequent experiments should test 2 and 4.

2. **Context dilution**: The Critic raised that BIT influence decays as conversation context grows. Neither proposal addressed how identity signal persists across rounds. If BITs win the bake-off, measure whether novel-insight count degrades in later rounds compared to earlier rounds.

3. **Convergence is a task-framing problem, not an identity problem**: The Pragmatist argued that the propose/critique/evaluate round structure already forces divergent behavior and identity just seasons it. If neither configuration wins the bake-off, this hypothesis becomes the next investigation target.

4. **Token budget arithmetic**: No participant calculated the actual token cost of each approach or the identity-to-conversation ratio at round 3 vs round 5. This should be measured during the bake-off as secondary data.

---

## Consensus Map

| Participant | Final Position | Agreed On |
|---|---|---|
| Cognitive Architect | Replace 6-layer with BITs entirely | BITs as mechanism; bake-off as process (implicitly, by not objecting in evaluate round) |
| Flow Orchestrator | Two-segment prompt, empirical BIT count | BITs as mechanism; prompt ordering matters; measurement over theory |
| Adversarial Critic | Prove failure before replacing | Identified real risks (context dilution, circular measurement, cooperative base model) that inform bake-off design |
| Systems Pragmatist | 48-hour bake-off, blind scoring | Bake-off process; token budget awareness; pragmatic timeline |
| Product Oracle | Bake-off scored on user-perceived insight | User value as the metric; stop debating, start testing |
| Context Surgeon | Bake-off with clean variable isolation and blind scoring | BITs-only vs current (no hybrid); blind protocol to control for evaluator bias |

**The group converged on**: Run the bake-off. Test BITs-only against current. Score blind on novel insights. Let evidence decide.

**The group did not converge on**: Whether BITs are inherently superior (Architect and Orchestrator say yes; Critic says unproven; Pragmatist says irrelevant until tested).
<!-- complete -->
