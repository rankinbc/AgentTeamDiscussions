# Morning Brief: 2026-03-26_1139_10-question-session

*Generated: 2026-03-26 12:17*

# Overnight Design Session Summary

## Overview

The session covered **10 open questions** about the AgentTeamDiscussions engine architecture. A strong theme emerged across nearly all decisions: **instrument first, build later**. The team consistently rejected speculative architecture in favor of gathering real data before committing to structural changes.

---

## Key Decisions by Topic

### Q1: BIT System (Beliefs, Instincts, Traits) vs Current 6-Layer Agent Model
**Decision:** Run a controlled bake-off before committing to either architecture. No immediate change — the current system stays until a head-to-head comparison produces evidence.

### Q2: Token Budget Allocation (Agent State vs Conversation History)
**Decision:** Instrument before allocating. Ship instrumentation as a logging change (low-risk), and only if data shows token pressure, start with simple solutions. No preemptive budget partitioning.

### Q3: Blind Proposal Rounds (Agent Independence Before Interaction)
**Decision:** Two-phase visibility with deterministic rotation. Agents propose blind in the first phase, then interact. Ship diversity instrumentation alongside the structure, and surface diversity as a user-visible signal.

### Q4: Key Takeaway Mechanism (Shared Context During Discussion)
**Decision:** Do NOT build a Key Takeaway mechanism. Audit existing output first. If evidence later demands action, fix the synthesis step — not the discussion structure itself.

### Q5: Stale Detection and Orchestrator Intervention
**Decision:** Fixed round counts per mode, no runtime stagnation detection. Instrument output quality post-hoc instead. If revisited later, start with early termination rather than mid-discussion intervention.

### Q6: Phase Separation (Brainstorm / Refine / Specify / Review)
**Decision:** Defer phase separation until instrumentation data exists. Preserve the "constraint gradient" concept as a design note for future reference. Define a clear instrumentation gate that would reopen this question.

### Q7: Anti-Sycophancy Architecture
**Decision:** The Q3 blind-round structure IS the complete anti-sycophancy mechanism — no additional architecture needed. Context hygiene (managing what agents see) is the highest-leverage anti-convergence tool available today. Log a context-length diversity hypothesis for the Q1 bake-off.

### Q8: Agent Verbosity and Context Window Management
**Decision:** Log total assembled prompt size per ClaudeRunner invocation. Role-selective context curation is rejected. Output-only logging is insufficient — input prompt sizes must also be tracked.

### Q9: Morning Brief and Session Output Format
**Decision:** Single structured-prompt synthesis with no verification pass. No dropped-thread detection. Defer structured decision records and reading instrumentation.

### Q10: Graduated Resistance (Discussion Intensity Over Rounds)
**Decision:** Defer resistance architecture until instrumentation data exists. Define semantic similarity between rounds as the convergence gate metric. Rotating analytical frames and "natural escalation" are rejected as unsubstantiated.

---

## Themes

1. **Instrument, don't architect** — Questions 2, 5, 6, 8, and 10 all concluded with "add logging/measurement first, decide later." The team is clearly resisting speculative complexity.

2. **Blind rounds as structural safeguard** — Q3's two-phase visibility design does double duty: it drives idea diversity (Q3) AND serves as the anti-sycophancy mechanism (Q7). Two problems, one solution.

3. **Synthesis over discussion complexity** — Q4 and Q9 both push quality improvements downstream to the synthesis/output stage rather than adding mechanisms to the discussion rounds themselves.

4. **Evidence gates** — Multiple decisions explicitly define what data would trigger revisiting the question, preventing indefinite deferral.

## Immediate Action Items

- **Ship prompt-size logging** per ClaudeRunner invocation (Q2, Q8)
- **Implement two-phase blind rounds** with deterministic rotation (Q3)
- **Add diversity instrumentation** alongside the blind round structure (Q3, Q7)
- **Design and run the BIT vs 6-layer bake-off** (Q1)
- **No new mechanisms to build:** Key Takeaways, stale detection, phase separation, graduated resistance, and dropped-thread detection are all explicitly deferred or rejected.
<!-- complete -->
