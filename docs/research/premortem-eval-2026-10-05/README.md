# Step 1: does a persona team beat a single call? (pre-mortem, V2 roadmap)

**Date:** 2026-10-05 · **Question:** before investing in the plugin, does a team of persona critics produce a better
pre-mortem than one strong model call given the same material?

**Answer: no — not on this evidence.** The team did not clear the bar set in advance (win ≥3 of 5 subjects).
It won 1 subject outright, lost 2, and split 2, at roughly 4× the calls. Both arms found substantially the same
failures. The useful output of this experiment is the findings themselves, summarised at the bottom.

> Want to judge blind yourself first? Read `sN-*/blind/opus/X.md` and `Y.md` for any subject, pick one, then check
> `KEY.json`. Don't open `single.md`, `team.md` or `results.json` until you have.

## Setup

| | Arm A — single call | Arm B — persona team |
|---|---|---|
| Who | 1 × Opus, told to attack from engineering, failure/ops, user and solo-dev-scope angles | 3 × Sonnet personas (Adversarial Critic, Systems Pragmatist, Product Oracle), independent, then 1 × Sonnet synthesizer (reporter only, no own findings) |
| Input | identical packet per subject: subject, verified engine-facts sheet, 2–4 source docs | same |
| Output | What breaks / Undecided / Questions for you, ≤ 700 words | same format and cap |
| Calls | 1 | 4 |

**Subjects** — the four open questions in `docs/v2/ROADMAP.md`, plus the critical path itself:

1. `s1-phase-triggers` — how should phase transitions be triggered?
2. `s2-eval-feedback` — how does evaluation feed back into agent behavior?
3. `s3-moderator-vs-phases` — boundary between moderator input and phase auto-transitions?
4. `s4-research-integration` — how do research results enter context assembly?
5. `s5-critical-path` — is the V2 build order right?

**Judging** — outputs shuffled to X/Y by script (`scripts/blind.py`, seed fixed), one identifying phrase scrubbed
from s1. Two judges per subject, Opus and Sonnet, each with its own random order, told to check claims against the
packet and not to reward length. Rubric: per finding valid / non-obvious / actionable; unique catches; sharpness of
the question sections; overall verdict.

## Results

| Subject | Opus judge | Sonnet judge | Outcome |
|---|---|---|---|
| s1 phase triggers | single (low) | team (low) | split |
| s2 eval feedback | team (medium) | team (low) | **team** |
| s3 moderator vs phases | single (medium) | single (medium) | **single** |
| s4 research integration | single (low) | team (low) | split |
| s5 critical path | single (low) | single (low) | **single** |

| Totals over 10 judgments | Single | Team |
|---|---|---|
| Verdicts won | 6 | 4 |
| Valid + non-obvious + actionable findings | 51 | 56 |
| Unique catches (valid, non-obvious, only in that report) | 21 | 23 |
| Invalid findings | 1 | 1 |
| Question-section sharpness (sum of 1–5) | 41 | 39 |

7 of 10 verdicts were low confidence. Judges repeatedly wrote that the two reports "converge on the same core" and
"overlap heavily"; the margin came down to one or two unique catches either way.

**Each judge leaned toward its own model.** The Opus judge picked the Opus-written single report in 4 of 5 subjects;
the Sonnet judge picked the Sonnet-written team report in 3 of 5. That is the pattern self-preference bias produces,
and it means the 6–4 verdict split mostly cancels out. Read the split as a tie.

## What this means

1. **The method doesn't change the conclusions.** Given the same packet, three personas plus a synthesizer and one
   instructed Opus call surfaced the same top 3–5 failures in every subject. The value came from the packet — the
   verified engine-facts sheet and the right source docs — not from the debate.
2. **The team finds slightly more, not better.** +5 findings and +2 unique catches over 10 judgments is within noise
   at n=5, and it costs 4× the calls (here ~250k vs ~62k subagent tokens per subject, most of it fixed per-call
   harness overhead; the team's calls were on cheaper Sonnet, so the dollar gap is smaller than 4×).
3. **Each arm catches a few things the other misses.** ~2 unique catches per report on each side. If coverage matters
   more than cost, the untested cheaper alternative is several independent single calls, not personas.
4. **Gate result:** per the plan, don't build `/premortem` as a multi-agent command. Keep the persona files as prompt
   material (the "angles" line in the single-call prompt is effectively the personas compressed).

## Caveats

- n = 5 subjects, all from this repo's own V2 docs, several of which are chat transcripts rather than specs.
- Judges are LLMs and each favored its own model's output (see Results). A human blind read is the tiebreaker that
  matters; the blind pairs are here for that.
- Arms differ in both method and model (Opus vs Sonnet personas) — a deliberate cost-matched comparison, not a pure
  method test.
- s4's team report was 24% longer than its single report (747 vs 604 words); the judges split on it anyway.
- Both arms read the same engine-facts sheet, written by the experimenter. Errors in it would be shared.

## What the roadmap pre-mortem actually found (both arms agree)

These showed up independently in both reports and are the real deliverable:

1. **The V2 specs target an engine that doesn't exist.** The moderator spec edits `live_conversation.py`
   (Python, GIL); the cadence/convergence design assumes a continuous live conversation; the research engine plugs into
   `context-assembly-template.md` rather than the running `RoundRunner`. Steps 3–6 of the critical path carry design
   work nobody budgeted. (s1, s3, s4, s5)
2. **Measure before you change behavior.** The Evaluator's scores are never read; no session before 2026-10-05 had a
   real ledger, so there is no baseline. Every critical-path step ships a behavior change with no way to tell if it
   helped. Build the measurement first, or at least an A/B on blind proposals. (s2, s5)
3. **Phase exit gates can't be computed, so "automatic transitions" become round counts with a label.** "50+ Ideas",
   "all major Ideas challenged" need entities the engine lacks; convergence can't be told apart from exhaustion. Start
   with round-count transitions and say so. (s1, s3, s5)
4. **The round boundary eats everything.** Between rounds agents see only 3-sentence Position Summaries, so research
   findings and moderator directives vanish at the first boundary unless they get a protected context section. (s3, s4)
5. **Blind proposals may already be mostly true.** Proposers already see only summaries of earlier rounds; the
   roadmap's "highest user value" item may change little that the user reads. Define what "suppress prior context"
   removes (ledger? prior-doc headings?) before building it. (s5)
6. **Evaluation feedback would optimize for the judge, not for friction.** An LLM judge rewards coherent, agreeing
   docs — the opposite of what the personas exist for — and scores can't be attributed to a persona. Feedback should
   tell you which persona to hand-edit, not edit it automatically. (s2)

## Files

```
README.md                this report
KEY.json                 X/Y -> arm mapping per subject and judge
results.json             unblinded scores
scripts/build.py         builds packets and prompts
scripts/blind.py         scrubs, shuffles, writes judge prompts
sN-*/inputs/             packet + exact prompts each arm received
sN-*/single.md           arm A output
sN-*/critic-{1,2,3}.md   arm B critics (1 adversarial, 2 pragmatist, 3 oracle)
sN-*/team.md             arm B synthesis
sN-*/blind/{opus,sonnet}/X.md, Y.md, judgment.md
```
