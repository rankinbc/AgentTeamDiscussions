1. **The user never sees a phase, so the whole trigger debate ships invisible infrastructure.** The roadmap itself says blind proposals change what the user reads and phases are "invisible infrastructure." Three months on, the phase system exists, the Morning Brief reads the same, and the retention question is answered: nobody would notice if it were removed. The 2-3 day estimate hid weeks of tuning for zero user-perceived gain.

2. **Convergence-based triggers fire on signals the engine cannot produce.** The cadence spec relies on `---signals---` footers (stance, changed, key_claim), concession rate and position count. The engine facts say nothing like that exists. Agents see only 3-sentence Position Summaries between rounds. The spec's own open question admits that exhaustion and genuine agreement look identical to the counter. From the user's perspective, a "convergence" transition that is really fatigue gives a confident Specify doc built on a false consensus.

3. **Round-count and convergence are the wrong axes, because sessions are fixed-round modes.** Each question already runs propose, critique, evaluate, then one synthesis. Phases layered on top either duplicate modes under new names or fight them. The moment that matters is when the user opens the Brief and cannot tell why the agents moved from Refine to Specify. Designs where the user cannot understand why agents said what they said are exactly what I reject.

4. **Phase exit gates are unmeasurable, so tuning becomes a config burden.** Gates like "50+ ideas, domain diversity threshold, disagreement queue below threshold, agreement score above threshold" need entity tracking (Ideas, magnitudes, a Disagreement queue) that is Vision scope. A solo builder's first-run YAML would hold a dozen thresholds. Would the user tune this or ignore it? They ignore it, and defaults silently decide everything.

5. **Nothing feeds back, so the choice cannot be learned.** The Evaluator scores are never read, and the ledger only began rendering 2026-10-05. With 17 sessions and none having a real ledger, there is no evidence for any trigger. The team will pick one by taste and never know whether it helped.

6. **Time-based is the option that fails first, and it is cheap to dismiss.** Every turn is a `claude -p` subprocess with variable latency, so wall-clock transitions cut rounds off mid-thought and make runs non-reproducible. Rule it out now.

**Undecided, author-only questions:**
- Is the phase system for the user's reading experience or for agent behavior? That decides everything else.
- Should the moderator or the user be able to override a transition? The roadmap's own open question on moderator input versus auto-transitions is unanswered.
- What is the one change in the Morning Brief that proves phases worked?
- Will you accept a fixed phase-per-round-count as v1, and commit to revisiting after reading real ledgers?
