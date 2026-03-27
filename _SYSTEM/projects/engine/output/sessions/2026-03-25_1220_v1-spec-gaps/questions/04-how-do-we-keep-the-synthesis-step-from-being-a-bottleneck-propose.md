### The Cognitive Architect (creativity engine designer)

The framing is slightly wrong, and fixing it resolves most of the problem.

**The synthesis bottleneck is in the design doc write, not the brief generation.** The brief is already protected — it consumes only extracted structured fields plus prior brief. That's lean by design. The real 9000-word problem is the design doc step, where all three round outputs get passed to produce the per-question artifact.

**My proposal: The evaluate round is the compression point. Use it.**

The evaluate round already reads propose and critique and produces a synthesized assessment. Passing all three rounds to the design doc writer is redundant — you're asking for synthesis of a document that already contains synthesis. The evaluate output *is* the natural compression boundary.

**Concrete mechanism:**
- Design doc writer receives: evaluate round output + extracted fields (decisions, open questions, sharpest objection)
- Propose and critique round outputs go to transcript only
- This cuts input to the design doc call from ~9000 words to ~2000-3000 words

**Why this holds:**
- Evaluate was explicitly designed to judge and integrate the prior rounds — it's not a summary, it's a synthesis
- Extracted fields capture the three most forward-relevant signals
- No information loss for the brief chain (brief never touched propose/critique directly)
- Design doc quality may *improve* — less noise from redundant competing proposals

**On the retry question:** Accept degraded output over no output, but degraded means "evaluate output forwarded as design doc verbatim" — not a blank file. The evaluate round already exists on disk. Use it.

Two-pass outline-then-fill adds latency without addressing the root cause. Fix the input size first.

### The Flow Orchestrator (mechanical flow designer)

The Cognitive Architect's diagnosis is correct. I'll confirm the sequence implication and flag the one remaining decision point.

**Confirmed routing:**
1. Propose round → transcript only
2. Critique round → transcript only  
3. Evaluate round → transcript + design doc input
4. Extract fields from evaluate output → structured fields
5. Design doc write: `evaluate_output + extracted_fields` → `design_doc_{n}.md`
6. Synthesize: `extracted_fields + previous_brief` → `brief.md`

Steps 5 and 6 already have separate, bounded inputs. The bottleneck was never architectural — it was an uncontrolled input to step 5. Constraining step 5 to evaluate output alone fixes it without adding any new moving parts.

**One decision still open:** What is the size bound on evaluate output? If evaluate output itself grows unbounded (agents are verbose; no truncation exists today), step 5 inherits the same problem one round later. The fix is a hard word truncation on evaluate output before it enters step 5 — not a retry policy, not a two-pass approach. One truncation threshold, applied at the boundary.

**On "accept degraded output":** The Cognitive Architect proposes forwarding evaluate output verbatim as the design doc on failure. I'd sharpen the trigger: this fallback activates only on step 5 API failure or timeout, not on output quality. The verbatim evaluate output is already a valid artifact — it's on disk, it's structured, it's forward-usable. Name it `design_doc_{n}_fallback.md` to match the existing fallback convention.

No chunking. No two-pass. Fix the input boundary and set one truncation limit.


<!-- complete -->
