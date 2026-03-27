# How does the Morning Brief get generated?

*Generated: 2026-03-25 12:23 | Question 1 | 171s | Mode: compete*

## Decisions

1. **Rolling synthesis is the architecture.** The Morning Brief is regenerated after each question completes, not generated once at session end. Each synthesis call receives `previous_brief + current question's extracted fields`. The brief at session end is the Morning Brief — there is no separate final pass.

2. **Do not feed design docs into the brief generator.** Design docs are human-readable output artifacts, not inputs. The brief generator consumes structured extracted fields only: extracted decisions, extracted open questions, and the sharpest critic objection (one sentence). This bounds input to approximately 100 tokens per question regardless of session length.

3. **The brief has four required sections, in this order:**
   - `## What Got Built` — one line per question, anchors the user's memory
   - `## Still In Play` — unresolved tensions the agents flagged
   - `## Watch Out` — sharpest critic objection, verbatim, one sentence, per question
   - `## Your Move` — questions only a human can answer; primary value, read-this-if-nothing-else

4. **Each section has a hard word budget enforced in the prompt, not by token limits.** Token caps truncate mid-sentence and produce briefs that look complete but aren't. The prompt specifies: `What Got Built`: one sentence per question. `Still In Play`: max 4 bullets. `Watch Out`: one sentence per question, verbatim from the critique. `Your Move`: max 3 bullets, one sentence each.

5. **The synthesis prompt contract:**

   ```
   You are updating a running Morning Brief for a human who has 5 minutes tomorrow.
   
   Inputs:
   - Previous brief (may be empty on first call)
   - New question summary:
       Decisions: [extracted decisions]
       Open questions: [extracted open questions]
       Sharpest objection: [one sentence from critique round]
   
   Output exactly these four sections, no others:
   
   ## What Got Built
   [one line per question answered so far, including this one]
   
   ## Still In Play
   [max 4 bullets — active tensions not yet resolved]
   
   ## Watch Out
   [one line per question — the sharpest critic objection, verbatim]
   
   ## Your Move
   [max 3 bullets — decisions that require a human; one sentence each]
   
   Rules:
   - If a bullet appeared in "Your Move" or "Watch Out" in the previous brief, carry it forward unless this question explicitly resolves it.
   - Cut anything a smart PM already knows.
   - Do not summarize what the agents said. State what is true and what is at risk.
   ```

6. **Continuity is enforced by the prompt rule, not the architecture.** The rule "carry forward unless explicitly superseded" prevents compounding loss across the rolling chain without requiring a `## Preserved Decisions` section or architectural preservation mechanism. The prompt is the anti-corruption layer.

7. **The fallback uses a separate file.** If the synthesis call fails, write raw extracted decisions and open questions to `brief_fallback.md`, never to `brief.md`. The reason: a hybrid narrative-plus-list document in `brief.md` corrupts the input contract for the next synthesis call. The fallback file is labeled with `## FALLBACK: Synthesis Failed` so the user knows what they are reading. The main `brief.md` is left at its last successful state.

8. **The execution sequence per question:**
   ```
   1. Run propose → critique → evaluate rounds
   2. Extract: decisions, open questions, sharpest objection
   3. Write design_doc.md to disk (full prose, for human review)
   4. Call synthesize(previous_brief, extracted_fields) → new_brief
   5. If step 4 succeeds: overwrite brief.md
   6. If step 4 fails: write to brief_fallback.md; leave brief.md unchanged
   ```

9. **`brief_history/` is deferred to V2.** Synthesis drift is a real risk but unverified in practice. Add timestamped brief snapshots when a user actually asks for them.

---

## Open Questions

- **Sharpest objection extraction:** Who extracts "the sharpest critic objection" from the critique round — a dedicated extraction call, a regex heuristic, or a field the evaluate round is asked to produce? This needs a mechanism, not just a field name.
- **First-call behavior:** On the first question, `previous_brief` is empty. The prompt should handle this gracefully (omit `## What Got Built` if there is only one entry, or always include it). Specify which.
- **Fallback trigger:** Is the fallback triggered only on API failure, or also on malformed output (e.g., missing required sections)? A validation step after step 4 that checks for the four section headers would catch structural failures before they corrupt the chain.
<!-- complete -->
