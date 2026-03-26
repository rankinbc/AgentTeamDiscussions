### The Cognitive Architect (creativity engine designer)

**Rolling synthesis, not end-of-night batch.**

Here's why this matters behaviorally: a brief generated after 10 questions must compress everything simultaneously. That's a lossy single-pass. Instead, treat the Morning Brief as a *living document* — regenerate it after each question completes, feeding `previous_brief + new_design_doc` as input. Context stays bounded. Each update is small and precise.

**The prompt contract:**

```
You are synthesizing overnight AI design work for a human who has 5 minutes.
Input: running brief so far + one new design doc
Output format:
  ## What Got Decided (bullet per question, one line each)
  ## Live Debates (unresolved tensions, tagged by question)
  ## Risk Flags (surfaced from critique rounds — must cite the critic's objection)
  ## What Needs Your Input (open questions the agents couldn't resolve)
Keep it brutal. Cut anything a smart PM already knows.
```

**Risk flag surfacing:** During critique rounds, the orchestrator tags any critique that scores above threshold as a `risk_flag: true` in the transcript metadata. The brief prompt explicitly pulls these — not as a summary of the full critique, but as the *sharpest objection* verbatim, one sentence.

**Context overflow:** Rolling synthesis solves this structurally. The brief never sees raw docs — only the previous brief (stable ~500 tokens) plus one new doc (~800 tokens). Ten questions = ten small calls, not one massive one.

**Fallback:** If synthesis fails, concatenate each doc's `## Decisions` section. Mechanical but readable. No brief is worse than a crashed session.

The incremental approach also gives you crash recovery for free — the brief survives mid-session failures.

### The Flow Orchestrator (mechanical flow designer)

Rolling synthesis is correct. Agree on all structural points. But there's a precision gap in the risk flag mechanism that needs closing before this is buildable.

**The ambiguity:** "critique scores above threshold" — what score? The 3-round structure doesn't produce a critique score. If we're adding a scoring pass to tag critiques, that's a new operation that needs to be designed. If we're not, the threshold is undefined.

**Simpler path:** Drop the metadata tagging entirely. Include the full critique text in the design doc under a `## Critiques` section. The brief prompt already says "Risk Flags must cite the critic's objection" — let the synthesis call find the sharpest one. One fewer moving part, same output.

**The exact sequence I'd commit to:**

```
for each question:
  1. run propose → critique → evaluate rounds
  2. write design_doc to disk (includes ## Critiques verbatim)
  3. call synthesize(previous_brief, design_doc) → new_brief
  4. overwrite brief.md on disk
  5. if step 3 fails → fallback: append design_doc.decisions to brief.md
```

Step 5 is the only branch. Everything else is linear.

**One addition:** The brief should also write to a `brief_history/` subfolder with a timestamp, so you can audit drift across the night. One extra file write, zero logic change.

The Cognitive Architect's prompt contract is good. I'd add one constraint: output token cap of 600. Briefs that grow unbounded aren't briefs.

The rolling approach also means the brief is readable mid-session — useful if you wake up early.


<!-- complete -->
