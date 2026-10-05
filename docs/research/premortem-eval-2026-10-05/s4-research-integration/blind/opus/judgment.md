# Judgment: s4 research integration (X vs Y)

## Step 1. Item labels

### Report X
| # | Finding | Valid | Non-obvious | Actionable | Notes |
|---|---|---|---|---|---|
| 1 | Findings get trimmed or crowd out the discussion (4k vs ~10k ceilings, research in neither protected list, ~24k worst case) | VALID | NON-OBVIOUS | ACTIONABLE | The 24k figure is inferred from 6 agents x 2 calls x 2k. The packet implies six voices, so it holds up. |
| 2 | Findings vanish at round boundary (3-sentence summaries); "cached per session" conflicts with stateless `claude -p`; ROI signal reads ~0 | VALID | NON-OBVIOUS | ACTIONABLE | Good catch that the cache claim has nowhere to live. |
| 3 | Unverified findings harden into DECIDED ledger lines with no provenance | VALID | NON-OBVIOUS | ACTIONABLE | |
| 4 | Trigger is unbuilt; footer compliance test not run; "skip and log" makes parse failure, timeout, hallucinated citation and a real "no" look the same | VALID | NON-OBVIOUS | ACTIONABLE | The point that these failure modes look the same is a distinct insight. |
| 5 | Cost/scope numbers come from a panel transcript, not measurement; integration is explicitly excluded; what a "research call" is stays undefined | VALID | NON-OBVIOUS | ACTIONABLE | |
| 6 | Findings in the propose round anchor speakers and undermine blind proposals | VALID | NON-OBVIOUS | ACTIONABLE | A reasonable inference from the ROADMAP's priorities. |
| 7 | Built before the base it needs; no way to tell if it helped | VALID | OBVIOUS | ACTIONABLE | The author wrote the critical path. The "did it help" point is fairly generic. |

### Report Y
| # | Finding | Valid | Non-obvious | Actionable | Notes |
|---|---|---|---|---|---|
| 1 | Research targets context-assembly-template.md (4k, takeaways, tombstones, signals footer), which the running engine does not implement. The real engine has different sections and a ~10k trimmer, and neither has a research slot. | VALID | NON-OBVIOUS | ACTIONABLE | This is the highest-leverage reframe in either report: it shows which spec the integration has to target. |
| 2 | Research budget (~24k) vs context budget cannot both hold; unprotected means paid but unseen, protected means it displaces history | VALID | NON-OBVIOUS | ACTIONABLE | "Trimmer cuts them first" overstates what the packet says about trim order. Otherwise it matches X1. |
| 3 | Nothing triggers research: no footer parsing, no research field in the template footer, compliance test pending, thinking-routine templates blocking | VALID | NON-OBVIOUS | ACTIONABLE | "Engine parses no footer" and "templates do not exist" are inferred, not stated in the packet. The core claim holds. |
| 4 | Round structure wipes findings before peers see them; ROI signal unmeasurable | VALID | NON-OBVIOUS | ACTIONABLE | Same as X2, without the stateless-cache point. |
| 5 | Wrong research hardens into DECIDED; uncited and impossible to audit or expire | VALID | NON-OBVIOUS | ACTIONABLE | Same as X3. |
| 6 | Integration design has no owner: scope-controls excludes it, the file is a chat transcript, and the ROADMAP files research-findings context management under Vision while calling Research Engine V2 | VALID | NON-OBVIOUS | ACTIONABLE | The V2-vs-Vision split is a small but real catch. |
| 7 | Nobody could tell whether research helped (no grounding dimension, scores feed back into nothing) | VALID | OBVIOUS | ACTIONABLE | The packet does not list the Evaluator's dimensions, so "no grounding dimension" is unverified. |

## Step 2. Unique catches (valid and non-obvious, in only one report)

X:
- X6: research in the propose round anchors speakers and works against blind proposals.
- X4 (the part only X has): "skip and log" makes hallucinated, timed-out, unparsed and genuinely negative results look the same.

Y:
- Y1: the integration target (context-assembly-template.md) is not the engine that actually runs. X only touches this indirectly, through "which ceiling, 4k or 10k".
- Y6 (the part only Y has): the ROADMAP places research-findings context management under Vision while Research Engine is V2.

(Y's Undecided section also has two sharp items X lacks: the time-limit contradiction between research-engine.md and scope-controls, and web-tool permission inside a `claude -p` subprocess. They are not counted above because they are not "What breaks" items.)

## Step 3. Undecided / Questions sharpness

- X: **3/5.** The Undecided list is solid and specific: placement, ceiling, timing, ledger marking, and evidence vs participant. The Questions lean generic or leading ("should blind proposals ship first as the ROADMAP says", "is there a baseline").
- Y: **4/5.** The Undecided list includes contradictions grounded in the packet (time limits) and a real implementation blocker (tool permission in `claude -p`). The Questions include "Is the template still the target, or is the current engine the baseline?", "research as brief preparation instead of mid-turn?" and "live web access in unattended sessions?". Only this author can answer these, and the answers change the design.

## Step 4. Verdict

**Y, low confidence.** The two reports overlap heavily on the budget, round-boundary, DECIDED-hardening and trigger findings, and both are free of outright invalid claims. Y leads with the most consequential reframe: the spec the research engine would plug into is not the running engine. Y's questions also force the decisions that matter next. X has two real unique catches (blind-proposal anchoring and the "skip and log" failure modes looking the same), which keeps this close.

{"x_valid_nonobvious_actionable": 6, "y_valid_nonobvious_actionable": 6, "x_invalid": 0, "y_invalid": 0, "x_unique": 2, "y_unique": 2, "x_questions": 3, "y_questions": 4, "verdict": "Y", "confidence": "low"}
