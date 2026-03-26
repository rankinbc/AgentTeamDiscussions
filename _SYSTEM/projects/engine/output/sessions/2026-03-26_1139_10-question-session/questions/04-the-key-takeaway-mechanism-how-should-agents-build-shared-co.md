# The Key Takeaway mechanism: how should agents build shared conclusions during a discussion?

*Generated: 2026-03-26 11:54 | Q4 | 240s | Mode: compete*

## Decisions

### Primary Decision: Do Not Build a Key Takeaway Mechanism

**Status:** Rejected as premature. No convergence detection, voting, or mid-discussion scoring protocol should be built.

**Rationale:** The discussion reached unanimous convergence (ironically) that the proposed mechanism solves an unvalidated problem. No evidence was presented that the current synthesis step drops meaningful conclusions. Building infrastructure to detect consensus before proving consensus is being lost is waste.

**What this means:**
- No 0-10 voting protocol added to discussion rounds.
- No mid-discussion takeaway proposals injected into agent prompts.
- No between-round convergence detection passes.
- The current flow (propose, critique, evaluate, synthesize) remains unchanged.

### Secondary Decision: Audit Existing Output Before Revisiting

**Status:** Accepted as the prerequisite gate for any future work in this area.

**Rationale:** The system already produces session transcripts, design docs, decisions ledgers, and Morning Briefs. If conclusions are being dropped, that evidence exists in the output directory today. Building detection infrastructure without first examining existing output is solving backwards.

**Validation method:** Run a single LLM extraction call against 5 existing session transcripts. Extract candidate conclusions from round responses. Compare against what appeared in the final design doc and Morning Brief. If coverage exceeds 80%, this feature is confirmed unnecessary. If coverage is below 80%, the specific failure patterns dictate what to build.

### Tertiary Decision: If Evidence Demands Action, Fix Synthesis -- Not Discussion

**Status:** Conditional. Only applies if the audit reveals dropped conclusions.

**Rationale:** Mid-discussion mechanisms (voting, scoring, takeaway proposals) are categorically wrong for stateless LLM agents. They pollute context windows, manufacture false consensus through anchoring, and degrade the authentic disagreement that makes multi-agent discussion valuable. If conclusions are being lost, the failure is in the synthesis step that reads round output, not in the rounds themselves.

**If action is needed, the cheapest valid approach:** A single between-round LLM call that takes all agent responses as input and outputs two lists -- convergent claims and divergent claims. These lists feed forward as descriptive context ("the group appears to be converging on X"), not prescriptive conclusions. Agents can challenge detected convergence in subsequent rounds. This is instrumentation, not mechanism.

---

## Behavioral Rules

### What the system must not do

1. **No in-conversation voting or scoring.** Agents must never be asked to rate, score, or vote on proposed conclusions during a discussion. This creates performative consensus -- LLMs pattern-match toward agreement when prompt structure rewards it.

2. **No consensus injection into agent context.** Agents must not receive "the group has decided X" or "takeaway scored 8/10" as authoritative input. Any convergence signal fed to agents must be framed as observation ("multiple responses referenced X"), not conclusion.

3. **No blocking operations between rounds.** Discussion flow must not pause for validation loops, agent confirmation of detected convergence, or scoring ceremonies. Latency in multi-round discussion compounds -- each blocking step multiplies across agents and rounds.

4. **No embedding infrastructure or similarity pipelines.** Semantic similarity scoring, threshold tuning, and pairwise comparison matrices are premature optimization for a system that has not yet demonstrated a convergence detection need. If detection is eventually needed, a single LLM summarization call is sufficient.

### What the system should do

1. **Preserve the current synthesis step as the sole convergence mechanism.** Synthesis already reads all round output and produces design docs. This is where conclusions are captured. If it's inadequate, improve its prompt -- don't add upstream machinery.

2. **Prioritize inter-question state propagation over intra-round convergence.** The real state management gap is across questions in multi-question sessions, where a conclusion from Q1 should constrain Q4 discussion but doesn't. The decisions ledger partially addresses this, but its injection into agent prompts needs examination before building new mechanisms.

3. **Treat any future convergence detection as instrumentation, not product.** If built, extraction results should be logged and compared against synthesis output to measure their marginal value. If synthesis already captures what extraction finds, the feature is waste and should be removed.

---

## Key Insights From Discussion

**The observer problem.** Any between-round summarizer is effectively an unaccountable agent injected into the conversation. It decides what "converged" without being contestable by discussion participants. This is acceptable only if its output is treated as input to synthesis, never as authoritative conclusion.

**Context pollution.** Every byte of voting state, takeaway proposals, or consensus artifacts injected into agent prompts displaces tokens that could carry domain expertise, conversation history, or agent personality. For token-constrained agents, convergence detection directly competes with discussion quality.

**False confidence compounds.** A wrong convergence signal ("the group agrees on X" when they don't) propagates through subsequent rounds and into synthesis. Agents anchor to it. Synthesis treats it as ground truth. The final design doc contains manufactured consensus that no agent actually held. This is worse than missing a genuine conclusion.

**Surface-level extraction fails in both directions.** Agents using different words for the same idea register as divergence. Agents using the same words with different meanings register as convergence. Without agent confirmation, machine-extracted consensus has an uncharacterized error rate that could exceed the error rate of simply letting synthesis do its job.

---

## Decision Gate

This topic reopens only when the following condition is met:

**Evidence from existing sessions shows synthesis is dropping conclusions.** Specifically: an audit of 5+ session transcripts demonstrates that claims reinforced by 3+ agents in round output do not appear in the corresponding design doc or Morning Brief, at a rate exceeding 20% of identified convergent claims.

Until that evidence exists, this mechanism remains shelved.
<!-- complete -->
