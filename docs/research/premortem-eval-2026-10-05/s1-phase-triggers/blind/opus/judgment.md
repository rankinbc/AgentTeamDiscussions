# Judgment: s1-phase-triggers (X vs Y)

## Step 1. Item labels

### Report X
1. Convergence trigger assumes an orchestrator that doesn't exist; 2-3 day estimate hides footer/tracker/counters. VALID / NON-OBVIOUS / ACTIONABLE. The packet supports it: the cadence doc assumes per-turn free flow, footer and urgency, while the engine runs fixed rounds.
2. Exit gates need Idea entities, magnitudes, bench rotation and a Weaver that don't exist (Vision scope), so they get LLM-judged or dropped. VALID / NON-OBVIOUS / ACTIONABLE. The tension with the "killed" list is slightly stretched, because what the cadence doc killed was per-turn LLM evaluation, not evaluation at phase boundaries.
3. False convergence ends Brainstorm early; N=7 gives about 2 checks per 3-round question. VALID / OBVIOUS / ACTIONABLE. The persuasion-versus-exhaustion ambiguity is already written down in the author's own cadence doc. "~5 agents" is an assumption the packet doesn't state.
4. No data and no feedback loop to tune thresholds (17 sessions, ledger only real since 2026-10-05, Evaluator scores unread). VALID / NON-OBVIOUS / ACTIONABLE. It argues for deferring adaptive triggers.
5. "Phase" collides with existing modes and the question-chained ledger, and the unit of a phase is unsettled, giving two overlapping state machines and inconsistent ledger tagging. VALID / NON-OBVIOUS / ACTIONABLE.
6. No override, so premature transitions erode trust and phases get turned off. VALID / OBVIOUS / ACTIONABLE. The roadmap already lists the moderator-versus-auto-transition boundary as an open question.
7. Phase briefing gets squeezed by the ~10k budget enforcer. VALID / NON-OBVIOUS / ACTIONABLE. The fix is to protect the phase section.

X: 5 valid+non-obvious+actionable, 0 invalid.

### Report Y
1. Convergence trigger needs a footer, tracker and concession log the engine doesn't produce; `claude -p` footer compliance and the 80% regex figure are unmeasured. VALID / NON-OBVIOUS / ACTIONABLE.
2. Convergence can't be told apart from exhaustion, so false consensus is silent. VALID / OBVIOUS / ACTIONABLE. It restates the cadence doc's own open question. The "silent failure" angle adds a little.
3. Thresholds were sized for a ~25-turn live discussion, not short fixed rounds, so windows land mid-round or never close. VALID / NON-OBVIOUS / ACTIONABLE. "3 agents per round" is not stated in the packet (minor unsupported detail).
4. Nothing exists to tune thresholds, so the guesses become permanent. VALID / NON-OBVIOUS / ACTIONABLE. Same finding as X4.
5. Exit gates need Vision-scope entities, and those gates plus the cadence counters form two incompatible trigger designs that the roadmap treats as one. The gates' judge calls also contradict the 2-calls-per-session budget. VALID / NON-OBVIOUS / ACTIONABLE.
6. About nine settings per phase against a 2-3 day price, and the briefing may be trimmed by the budget enforcer. VALID / NON-OBVIOUS / ACTIONABLE. It overlaps X1 and X7.
7. Phases are invisible infrastructure and duplicate the propose/critique/evaluate modes. VALID / NON-OBVIOUS / ACTIONABLE. The "invisible" half is the roadmap's own insight. The duplication half overlaps X5.
8. The decisions ledger that phase handoff depends on "has never worked". VALID, though overstated: it was fixed on 2026-10-05, and only its output is unproven. OBVIOUS, because the author just fixed it. Weakly actionable.
9. Time-based triggers are the worst option because `claude -p` latency is variable. VALID / OBVIOUS / ACTIONABLE. Ruling it out is cheap but self-evident.

Y: 6 valid+non-obvious+actionable, 0 invalid. Three items (2, 8, 9) are mostly padding.

## Step 2. Unique catches (VALID + NON-OBVIOUS, in one report only)
- X only: ledger entries tagged inconsistently across phase boundaries, and a phase as a second state machine alongside modes (X5's ledger angle). Count: 1.
- Y only: (a) the repo holds two incompatible trigger designs (phase-dynamics gates vs cadence counters), and the gates break the 2-LLM-call budget (Y5); (b) `claude -p` footer compliance and regex coverage have never been measured on the existing 17 sessions (Y1). Count: 2.

## Step 3. Undecided / Questions sharpness
- X: 4. "Unattended overnight vs watched live" decides whether an override matters, and "premature Brainstorm cutoff vs never-ending Review" is a real preference only the author can state. The question about blind proposals and phases is partly answered by the roadmap already. The Undecided list is concrete and well scoped (available vs new signals, min/max rounds wrapper).
- Y: 4. "Better design docs vs autonomous overnight system" and "what single visible change proves phases worked" are sharp. "Ideas/magnitudes gates in v1?" is a good scoping question. A couple of Undecided items are generic (whether Evaluator scores will be read back).

## Step 4. Verdict
X, low confidence. The two reports converge on the same core: build round-count first, adaptive triggers can't be tuned, and the gates need missing entities. Y has slightly more distinct valid catches, notably the two incompatible trigger designs. X, though, carries less padding, and its top items (the hidden orchestrator cost, the phase/mode/ledger unit collision, the protected budget section) are the ones the author would act on first. Y spends three of its nine items on things the author already knows (persuasion vs exhaustion, the ledger just fixed, time-based being bad).

{"x_valid_nonobvious_actionable": 5, "y_valid_nonobvious_actionable": 6, "x_invalid": 0, "y_invalid": 0, "x_unique": 1, "y_unique": 2, "x_questions": 4, "y_questions": 4, "verdict": "X", "confidence": "low"}
