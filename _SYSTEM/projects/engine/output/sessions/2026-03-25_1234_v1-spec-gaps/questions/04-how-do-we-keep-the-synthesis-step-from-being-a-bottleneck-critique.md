### The Adversarial Critic (adversarial reviewer)

**Five problems. Starting with the one that invalidates the framing.**

**1. The question was never answered.** The Orchestrator declared the 9000-word problem solved, then closed process bookkeeping items. The actual question — how do we make synthesis *reliable* — got zero treatment. Retry policy is not a reliability strategy. It's a recovery strategy. These are not the same thing.

**2. The sync point is "the orchestrator handles it" with extra words.** "Await all extraction_task futures before synthesis" is a requirement, not a design. What tracks those futures? What happens if one was never launched because the extraction task threw before registration? What's the timeout on the sync wait itself? This is a hole dressed as a gate.

**3. Deterministic fallback breaks on empty blockers.** Concatenating fragment fields into three-section framing when `blocker` is legitimately empty string produces either a blank "Don't Start Yet" section or requires conditional logic. That conditional logic is not specified. "Direct concatenation" is not deterministic if the schema has optional-by-convention fields.

**4. `min_success_fraction` boundary is undefined.** "More than half fail" — does 50% trigger abort or not? On a 2-question session, one failure is exactly 0.5. The edge case is the common case in short sessions. Needs `>` vs `>=` specified.

**5. No timeout per synthesis attempt.** Retry count means nothing if individual attempts can hang indefinitely. What's the per-call timeout before a retry fires?

Close the gaps or they ship as assumptions.

### The Systems Pragmatist (infrastructure realist)

The Critic landed five hits. Three of them are real blockers. Two are implementation details.

**Real blockers:**

The sync point gap is the worst one. "Await all futures" assumes all futures were registered. An extraction task that throws before registration is invisible to the sync gate — synthesis fires, reads a partial log, and produces output that looks complete but isn't. The fix is simple: track question slots by ID at session start, not by task registration. If a slot has no fragment at sync time, write the sentinel *at the gate*, not at extraction time. The gate then has a complete log by construction.

The deterministic fallback with empty blockers is a latent bug. "Don't Start Yet" must be omitted if no blockers exist — that's already decided. The fallback path needs the same conditional. One line of code, but it has to be in the spec or it ships wrong.

Per-call timeout on synthesis is non-negotiable. Without it, retry count is theater. 60 seconds per attempt is a reasonable default. Add `synthesis_call_timeout_seconds` to the config block alongside the retry keys.

**Implementation details, not blockers:**

`min_success_fraction` boundary: specify `>` not `>=`. One failure on a 2-question session is 0.5, which should not abort. The brief with one sentinel fragment is more useful than no brief.

The "reliability vs. recovery" framing from the Critic is correct but the conclusion is wrong for V1. Structural reliability (chunking, two-pass) adds complexity before we have evidence the fragment budget actually fails. We have one data point: beta was slow. Slow is not the same as unreliable at 1150 tokens. Fix the three gaps, ship it, measure.


<!-- complete -->
