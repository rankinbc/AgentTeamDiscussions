# Morning Brief: 2026-03-26_1218_10-question-session

*Generated: 2026-03-26 12:53*

# Overnight Design Session Summary: V2 Planning

The session covered **10 open questions** about the V2 evolution of the discussion engine, producing **70+ decisions**. Here's what was decided:

---

## Critical Path & Scope (Q1, Q10)

The team converged on a tight minimum-viable V2:

1. **Round-type prompt differentiation** is the highest-priority change — proposals, critiques, and evaluations get different prompts via PromptBuilder modifications
2. **Blind proposals** ship as a real PromptBuilder change (not just a prompt instruction)
3. **Overnight completion report** is the third minimum-viable deliverable
4. **Prompt output snapshots** are the prerequisite for all V2 validation

Explicitly **not** minimum-viable: tiered summarization, BIT system, personality transition. The phase system comes second; stale detection requires phases; anti-sycophancy is treated as validation, not architecture.

## Build Strategy (Q2)

**Incremental, not parallel.** PromptBuilder is the migration entry point. Every V2 change ships through feature delivery — the migration pattern emerges from the work, not from upfront design. Every change is measured against output quality. BIT system and key takeaways layer on independently.

## Context Window Management (Q3)

- **Priority-queue eviction** with a hardcoded eviction order (last-cut to first-cut), not percentage budgets
- **Agent identity hard-capped at 800 tokens** per agent
- **Tiered summarization** for conversation history
- Round type determines available budget
- **Instrument V1 first** before tuning V2

## Feature Flags (Q4)

- Only **two session-level flags**, living in `session.json` and checked in PromptBuilder
- Ego simulation and graduated resistance are **team YAML config**, not flags
- Anti-coordination scoring, tiered summarization, and all mechanical changes ship **always-on**
- Flags are per-session, never mid-session
- Validate the 800-token cap before shipping

## Validation & Testing (Q5, Q6)

**No automated quality scoring.** The validation framework is:

- **Paired human comparison** — run V1 and V2 on the same topic, human judges which surfaced better perspectives
- **Five paired runs** before declaring success or failure
- **Measurement infrastructure is a spreadsheet**
- No LLM-as-judge, no embedding metrics, no divergence scoring, no formal experimental design at N<20

Testing is **two layers only**: mechanical tests (prompt assembly, template correctness) and human evaluation. No middle layer. Contrarianism detection is a human judgment call.

## CLI vs SDK (Q7)

**SDK migration ships last**, after all V2 prompt features are validated on the CLI subprocess model. Token measurement uses character-based heuristics with safety margins. The 800-token cap is validated offline. Context eviction uses padded character estimates. V1's retry mechanism is sufficient for V2 validation. No partial SDK extraction.

## Personality System (Q8)

A **swap test** is the mandatory gate: can a human blindly identify which agent wrote which response? If personality is decorative, write BITs fresh without migration. If load-bearing, use sequential single-agent compression. V1 YAML files are preserved as rollback. This work **does not block the critical path**. Round structure and positional context are acknowledged as potentially dominant factors over personality.

## Overnight Operations (Q9)

- **Sequential execution, halt-on-failure** — no parallelism, no skip-and-advance
- Retry with **exponential backoff + jitter**, capped at 120 seconds
- **Session duration cap** in `defaults.yaml`
- A **human-readable completion report** is the only new artifact
- No watchdog process, no heartbeat, no runtime quality validation, no new monitoring infrastructure

---

## Key Themes

- **Ruthless minimalism**: The session repeatedly rejected complexity (automated scoring, SDK migration, monitoring infrastructure, A/B testing) in favor of the simplest thing that could work
- **Human judgment over automation**: Quality is evaluated by humans reading output, not by metrics
- **PromptBuilder is the seam**: Nearly all V2 changes flow through prompt assembly
- **Measure before optimizing**: Instrument V1, snapshot prompts, run paired comparisons — then decide what to tune
<!-- complete -->
