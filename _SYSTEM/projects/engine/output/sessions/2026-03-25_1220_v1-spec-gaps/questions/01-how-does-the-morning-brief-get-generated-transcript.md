# Transcript: How does the Morning Brief get generated?

*Generated: 2026-03-25 12:23*

## Round: PROPOSE

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

## Round: CRITIQUE

### The Systems Pragmatist (infrastructure realist)

**The incremental vs. all-at-once question is already answered by the architecture.** If you're doing rolling synthesis after each question, the Morning Brief *is* the brief at session end. There's no separate final pass. Treat them as one thing or you're building two systems.

**The real failure modes:**

1. **Context overflow is the actual problem.** Ten design docs at 800 tokens each is 8K tokens of input before your prompt. Fine for now. At 20 questions with verbose outputs, you're over 16K just in docs. The rolling approach sidesteps this — you only ever pass `previous_brief + latest_design_doc`, not the full history. That's the winning argument for incremental, not "readable mid-session."

2. **Brief drift is undetectable.** If the synthesis call subtly drops a risk flag or misrepresents a decision across 10 rounds, you won't know until you read the final output. The `brief_history/` subfolder proposed in the last round is the only audit mechanism. That's load-bearing — don't treat it as optional.

3. **Fallback creates a different artifact.** The proposed fallback (append decisions to brief.md) produces a structured list, not a synthesized narrative. That's fine as a degradation mode, but label it — write `## FALLBACK: Synthesis Failed` so the user knows what they're reading.

**What needs designing right now:** The synthesis prompt. Specifically — what's the token budget for the output brief, and what sections are required? Without that contract, the rolling chain has no termination condition and the brief grows unbounded.

That's the blocking question. Everything else is implementation detail.

### The Adversarial Critic (adversarial reviewer)

**Three problems nobody has solved:**

**1. Synthesis compounds, not just drifts.** Rolling synthesis doesn't just *drift* — it permanently discards. If round 4's synthesis drops a risk flag from round 2, rounds 5–10 never see it. `brief_history/` lets you *detect* this after the fact. It doesn't prevent it. You need a mechanism that preserves high-confidence decisions across the chain, not just an audit log.

**2. The fallback poisons the chain.** If synthesis fails on round 6, you append raw decisions to `brief.md`. Round 7's synthesis call then receives a hybrid document — part narrative, part structured list — and synthesizes *that*. The fallback doesn't degrade gracefully; it corrupts the input contract for every subsequent call. The fix is a separate `brief_fallback.md` that the chain never reads from.

**3. "600 token cap" is unenforceable.** You can set `max_tokens=600` on the API call. The model will truncate mid-sentence. That's not a brief — that's a truncated brief that *looks* complete. The output contract needs a structured format (fixed sections, each with a word budget) that the prompt enforces, not the token limit.

**The Pragmatist is right that the synthesis prompt is blocking.** But the required sections aren't just a formatting question — they're the anti-corruption layer for the rolling chain. Without explicit sections like `## Preserved Decisions` and `## Active Risk Flags`, each synthesis call decides what's worth keeping. That's too much discretion.

Design the prompt sections first. Everything else follows.

## Round: EVALUATE

### The Product Oracle (user advocate)

**The brief has one job: tell the user what to do next morning.**

Not "what was decided." Not "what the agents debated." *What requires a human now.* Design the sections backward from that moment.

**The sections I'd commit to:**

```
## What Got Built  (one line per question — anchor for context)
## Still In Play   (unresolved tensions the agents flagged)
## Your Move       (questions only a human can answer)
## Watch Out       (sharpest critic objection, verbatim, per question)
```

That's it. Four sections. Each has a job. `Your Move` is the primary value — if a user reads nothing else, they read that.

**On the rolling vs. batch debate:** rolling wins, but for a product reason nobody named yet. If the session runs overnight and something goes wrong at question 7, the user wakes up to *something useful* — not nothing. That's not a crash recovery feature, that's basic respect for the user's time.

**The Adversarial Critic is right about compounding loss.** The fix isn't `## Preserved Decisions` (engineering framing) — it's a hard rule in the prompt: *"If a decision appeared in the previous brief, it must appear in this brief unless explicitly superseded."* The prompt enforces continuity, not the architecture.

**The fallback corruption problem is real and user-visible.** A hybrid narrative-plus-list brief is confusing to read. Separate file is correct.

**Flag for V1:** Skip `brief_history/`. Users won't audit synthesis drift on the first run. Add it in V2 when someone actually asks for it.

### The Context Surgeon (context efficiency evaluator)

**The input assembly question is the one nobody answered, and it's the most consequential.**

"What if 10 design docs exceed context?" has one correct answer: **don't feed design docs**. Design docs are human-readable prose. They're the *output* artifact, optimized for readability, not for being re-ingested. Feeding them back in is full history stuffing with extra formatting overhead.

What the brief generator actually needs per question:
- Extracted decisions (already structured)
- Extracted open questions (already structured)
- The sharpest critic objection (one sentence, not the full critique)

That's 3 structured fields per question. 10 questions × ~100 tokens each = ~1,000 tokens of input. Context problem solved.

**On rolling vs. all-at-once:** rolling wins on context budget grounds too, not just crash recovery. All-at-once scales with session length. Rolling is O(1) — each call sees previous brief + current question's extracted fields. The brief *is* the compression mechanism.

**The Product Oracle's four sections are correct.** I'd add one constraint: each section gets a hard word budget in the prompt (`Your Move: max 3 bullets, one sentence each`). Not because of token limits — because the prompt-enforced structure is what makes rolling synthesis lossless. A model that must fill exactly four sections with fixed budgets has no discretion about what to discard.

**The Adversarial Critic's `## Preserved Decisions` and the Product Oracle's continuity rule are the same fix in different clothes.** The prompt rule is simpler. Ship that.

`brief_history/` is V2. Separate fallback file is V1.

<!-- complete -->
