## What breaks

1. **A convergence trigger fires on signals the engine does not produce, so it never fires or fires on noise.** The cadence spec (orchestrator-event-cadence.md) needs a per-turn `---signals---` footer (stance, changed, key_claim), a position tracker and a concession log. The engine only emits a 3-sentence Position Summary, and `claude -p` footer compliance is unproven. The ~80% regex fallback for concessions has never been measured on any of the 17 sessions.

2. **Convergence cannot be told apart from exhaustion, so phases advance on false consensus.** The cadence doc admits that positions falling because agents were persuaded looks identical to positions falling because they gave up. The "concession precedes convergence" rescue is unvalidated, and sycophantic agents concede constantly. A premature transition looks like a normal run, so the failure is silent and the resulting Specify doc rests on consensus that was never real.

3. **The thresholds were designed for a live conversation, not for this engine's fixed rounds.** N=7 turns, 10%, a 2+ position drop and 5 turns are "starting values" for a roughly 25-turn live discussion. The engine runs short fixed rounds (propose, critique, evaluate) with 3 agents per round. A window can land mid-round or never close, and between rounds agents see only summaries.

4. **Nothing exists to tune thresholds, so the guesses become permanent.** The cadence doc says its parameters can only be answered by running sessions. The engine has 17 sessions and no real ledger before 2026-10-05, and the Evaluator's scores are read by nothing. One developer running sessions occasionally will leave hand-edited YAML defaults in place and then abandon the feature.

5. **The exit gates in phase-dynamics.md need entities the engine lacks and contradict the cadence counters.** "50+ Ideas", "all major Ideas challenged", "disagreement queue below threshold" and "Builder confirms implementable" need Ideas, a disagreement queue, magnitudes and provenance, which are Vision scope. They would need extra LLM judge calls, while the cadence doc claims 2 calls per session. The repo holds two incompatible trigger designs, and the roadmap question treats them as one.

6. **Phase configuration balloons and has nowhere to live in the current context assembly.** Phase-dynamics lists about nine settings per phase (communication mode, bench rotation, technique categories, muse activity and more). The roadmap prices the whole system at 2-3 days. A phase briefing injected mid-session may be silently trimmed, because the ~10k-token budget enforcer trims unprotected sections and the plan does not say which sections are protected.

7. **The phase system ships as invisible infrastructure and duplicates existing round modes.** The roadmap itself says blind proposals change what the user reads and work without phases. The propose, critique, evaluate modes already behave like phases. Phases layered on top either duplicate those modes under new names or conflict with them, and the user cannot see why agents moved from one phase to the next.

8. **The decisions ledger that phase handoff would chain on has never worked.** The synthesis template was not rendered until 2026-10-05, so no session produced a real DECIDED/CONTESTED/OPEN ledger. Takeaway extraction at phase boundaries would be built on unproven output.

9. **Time-based triggers are the worst option.** Every turn is a `claude -p` subprocess with variable latency, so wall-clock transitions cut rounds off mid-thought and make runs non-reproducible. This should be ruled out now. The real choice, though, is between round-count and convergence, and round-count is the only one the current engine can support.

## Undecided

- Whether a phase is a fixed round list within a question or a state that spans questions.
- Which trigger is the v1 default, and whether round-count with a manual override is acceptable.
- A hard cap on rounds if convergence never fires.
- Whether the moderator or the user wins when they disagree with an auto-transition (no moderator channel exists yet).
- Whether the DECIDED/CONTESTED/OPEN ledger replaces the regex counters as the convergence signal.
- Whether Evaluator scores will ever be read back to tune thresholds.
- Whether phases are meant to improve the reading experience or agent behavior.

## Questions for you

- Is the goal better design docs, or an autonomous overnight system that decides when to move on?
- Will you accept fixed round counts per phase as v1 and revisit after reading real ledgers?
- What single visible change in the output would prove that phases worked?
- Do the existing propose, critique, evaluate modes already count as phases for your purposes?
- Do you want the Ideas, magnitudes and Builder-confirmation gates in v1, or only counters the engine can compute today?
