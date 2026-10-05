1. **The convergence trigger will fire on exhaustion or on regex noise, and the engine cannot tell which.** The cadence doc's own open question admits that consolidation from agreement and consolidation from exhaustion look identical to the counters. The disambiguator (concession rate) rests on ~80% regex coverage, and `claude -p` footer compliance is unproven. At 3 AM the Brainstorm to Refine transition triggers on a counter nobody can audit, and the failure is silent: a phase that advanced too early looks like a normal run.

2. **The convergence counters assume continuous turns, but the engine has fixed rounds and 3-sentence Position Summaries.** Between rounds agents see only summaries, so "position count declined by 2+ over 7 turns" is measured on a transcript where agents cannot see most of what was said. N=7 with 3 agents per round makes a "check" land mid-round. The thresholds were designed for a 25-turn live conversation (the cadence doc), not for the engine that exists.

3. **Nothing exists to tune the thresholds.** The cadence doc says its parameters "can only be answered by running sessions". The engine has 17 sessions, no real ledger before today, and an Evaluator whose scores nothing reads. Every threshold is a guess, there is no feedback loop, and one developer running sessions occasionally will never accumulate the data. Expect hand-edited YAML thresholds, then abandonment.

4. **Four phases times per-phase configuration (personality weighting, bench rotation, technique categories, Weaver briefings, exit gates) is the seven-background-agents mistake again.** phase-dynamics.md lists about nine settings per phase, plus a transition ritual involving a BackgroundAgent and recalculated magnitudes. The roadmap prices this at 2-3 days. Nothing in the engine supports bench rotation or magnitudes. Scope will balloon and the half-built version will be undebuggable.

5. **The roadmap's own critical path says phases are invisible infrastructure and blind proposals work without them.** If blind proposals ship first, the existing propose, critique, evaluate round modes already are the phases. The failure mode is building a transition engine when a fixed round count per phase would answer the question.

6. **Exit gates in phase-dynamics.md ("50+ Ideas", "all major Ideas challenged", "Builder confirms implementable") need entities the engine does not have.** Ideas, Decisions with provenance and a Builder confirmation are not in the code. Those gates cannot be evaluated without extra LLM judge calls, which the cadence doc claims it avoids (2 calls per session).

**Undecided, only the author can answer:**
- Is the goal better design docs, or an autonomous overnight system? That determines whether round-count triggers are enough.
- What is the fallback if convergence never fires: a hard cap on rounds?
- Who owns the boundary between moderator input and auto-transition, given that there is no moderator channel yet?
- Is the ledger's DECIDED/CONTESTED/OPEN output intended to be the convergence signal instead of regex counters?
