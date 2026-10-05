## What breaks

1. **The convergence trigger was designed for an engine that does not exist, so building it meant building the whole orchestrator first.** orchestrator-event-cadence.md assumes free-flowing per-turn conversation, a `---signals---` footer, urgency-driven speaker order, and a position tracker. The real engine runs fixed rounds of sequential speakers, and between rounds agents see only 3-sentence Position Summaries (engine facts). The roadmap's "Phase System (2-3 days)" estimate quietly includes footer parsing, three-tier detection, counters and threshold checks. The estimate blew up and the feature was shelved half-built.

2. **The phase exit gates cannot be measured, so the triggers fell back to round counts with a phase label.** phase-dynamics.md gates on "50+ Ideas", "all major Ideas challenged or killed", "Builder confirms implementable" and an "agreement score". Those need Idea entities and magnitudes (listed as Vision scope in ROADMAP.md), bench rotation and a Weaver BackgroundAgent. None of these exist. Each gate ended up either judged by an LLM (the kind of per-turn LLM evaluation the cadence doc explicitly killed) or dropped.

3. **The counter fires on false convergence, so Brainstorm ends too early.** The cadence doc admits that a falling position count looks the same whether agents were persuaded or just worn out. LLM agents agree with each other readily, so concession events show up cheaply and the "nonzero concession rate + declining positions" rule trips. With N=7 and ~5 agents, a 3-round question gets about 2 checks, too coarse to separate narrowing from collapse.

4. **There was no data and no feedback loop to tune the thresholds.** Every threshold is "tune from first overnight run". But the project has 17 sessions, sessions run only occasionally, real ledgers have existed only since 2026-10-05, and nothing reads the Evaluator's scores back (engine facts). The thresholds stayed at their starting guesses, and every wrong transition cost a whole run with no way to fix it mid-session.

5. **"Phase" collides with existing structure, and the scope was never settled.** The engine already has modes (propose -> critique -> evaluate) inside each question, plus a decisions ledger that chains from one question to the next. It is unclear whether a phase spans a session, sits inside a question, or replaces modes. Building without deciding produced two overlapping state machines, and ledger entries ended up tagged inconsistently across phase boundaries.

6. **With no override, automatic transitions undermined trust.** ROADMAP.md lists "boundary between moderator input and auto-transitions" as open, and no moderator channel exists (engine facts). A solo user who sees a premature transition can only rerun the session. After a few bad runs, phases get turned off.

7. **Phase briefings get squeezed by the context budget.** The promoted summary and the phase-specific prompt add to an already crowded per-turn payload (persona, lens, overlay, brief, ledger, headings, open questions). The ~10k budget enforcer trims unprotected sections, so either the new phase framing or the existing context loses out silently.

## Undecided

- Unit of a phase: per session, per question, or a replacement for the existing mode/round structure.
- Which signals are actually available in the current engine (round-level Position Summaries, ledger DECIDED/CONTESTED/OPEN counts) versus signals that need new infrastructure (footer, per-turn tracker).
- Whether a minimum and maximum round count per phase wraps any adaptive trigger, and what happens when the maximum is hit without convergence.
- Whether exit gates are deterministic counts or LLM-judged, and if judged, how that squares with the cadence doc's ban on per-turn LLM evaluation.
- How transitions interact with moderator input (veto, force-advance, none).
- What counts as a phase transition "working", and which Evaluator dimension (if any) measures it.

## Questions for you

- Would you accept a fixed round-count schedule per phase for V2, with adaptive triggers deferred until enough sessions exist to tune them?
- Do you run sessions unattended (overnight) or watch them live, since that decides whether a manual override matters?
- Is the existing propose/critique/evaluate mode meant to become the phase system, or to keep running inside each phase?
- Would a premature Brainstorm cutoff or a Review that never ends be the worse failure for you?
- Does the blind-proposals feature need phases at all, or can phases wait until after it ships?
