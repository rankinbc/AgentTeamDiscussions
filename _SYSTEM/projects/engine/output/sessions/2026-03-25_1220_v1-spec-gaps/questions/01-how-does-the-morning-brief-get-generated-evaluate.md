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
