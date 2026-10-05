1. **The convergence trigger reads signals the engine does not produce, so it never fires or fires on noise.** The cadence spec (orchestrator-event-cadence.md) depends on a per-turn `---signals---` footer with stance, changed and key_claim fields, a position tracker and a concession log. Engine facts say none of that exists: agents emit only a 3-sentence Position Summary, and rounds are fixed. The unstated assumption is that footer compliance will be high. Nobody has said what happens when `claude -p` personas ignore the footer, and the regex fallback is estimated at about 80% for concessions, which was never measured on any of the 17 sessions.

2. **Convergence cannot be told apart from exhaustion, and the spec admits it.** The Cognitive Architect's flag in the cadence doc: position count falling because agents found something compelling looks identical to falling because they gave up. The rescue is a "concession precedes convergence" ordering that is explicitly unvalidated. Sycophantic LLM agents concede constantly, so concession rate will read as healthy convergence while the discussion is actually collapsing into agreement. Phases then advance on false convergence.

3. **Every threshold is a guess that cannot be tuned.** N=7, 10%, 5 turns and 2+ position drop are "starting values", yet a session has fixed short rounds (propose, critique, evaluate). With so few turns per question, a 7-turn window may never close. One solo developer runs sessions occasionally, so there is no data to tune against. The thresholds will be left at their guesses, then abandoned.

4. **The engine's architecture contradicts per-turn orchestration.** Agents see only earlier rounds' Position Summaries, and a budget enforcer trims unprotected context at about 10k tokens. A phase transition that injects a briefing, changes communication mode and rotates the bench has no place to live. Nothing says which context sections are protected, so the new phase briefing could be silently trimmed.

5. **The phase doc's exit gates contradict the convergence trigger.** phase-dynamics.md gates Brainstorm on "50+ Ideas", Refine on "all ideas challenged", and Specify on a Builder confirmation. Those are content-count and judgment gates. None maps to the cadence table's counters. Two incompatible trigger designs exist in the repo, and the roadmap question treats them as one.

6. **The ledger the phases would chain on has never worked.** The synthesis template was not rendered until 2026-10-05, so no real DECIDED/CONTESTED/OPEN ledger exists. Phase handoff and takeaway extraction would be built on an unproven foundation.

7. **Scope is mis-sized.** The roadmap says 2-3 days for a Phase System that also needs blind proposals, takeaways and moderator input. The roadmap itself says blind proposals work without phases. This is the likeliest form of abandonment: half-built infrastructure with no visible user value.

**Undecided, author only:**
- Does a phase mean a fixed round list per question, or a state that spans questions?
- Who wins when the moderator and the auto-transition disagree?
- What is the cheapest trigger you would accept being wrong: round count with a manual override?
- Will you read any Evaluator score to tune thresholds? Currently nothing does.
