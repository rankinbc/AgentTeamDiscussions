### The Cognitive Architect (creativity engine designer)

## Error Handling: Layer-Aware Blast Radius

The key insight is that failure modes have different blast radii. One retry policy for 70 calls is wrong. The policy should match what each layer is worth.

**Three failure layers, three policies:**

**Round failures (propose/critique/evaluate):** These are the session's core value. One retry with 15-second backoff. If retry fails, write a tombstone entry to the transcript — `[ROUND FAILED: propose, question 6]` — and skip that question entirely. Do not attempt extraction or synthesis on partial round output. The tombstone is the record.

**Extraction failures:** Already decided — degrade gracefully (empty arrays, log raw output). No retry. The extraction call is cheap enough that a second attempt on malformed JSON rarely recovers.

**Synthesis failures:** Already decided — `brief_fallback.md`, never corrupt `brief.md`. Design doc still writes. Session continues from last valid brief state.

**Transcript writes are incremental, per round, not per question.** If the session dies at question 6, rounds 1–5 and completed rounds of question 6 are already on disk. Nothing is lost. This is the most important single implementation decision here.

**Morning Brief on failed questions:** Include a one-line tombstone in `## Still In Play` — *"Question 6 failed before extraction — [topic] is unresolved."* The chain needs to know the gap exists or downstream synthesis halts confabulate an answer.

**First-call behavior resolution:** When `previous_brief` is empty, omit `## What Got Built` entirely. Including it with zero content produces structural noise.

### The Flow Orchestrator (mechanical flow designer)

## Agreed on Layers. One Sequence to Pin Down.

The three-layer policy is correct. I won't re-argue it. What's missing is the exact state machine for "skip question" — because "skip" is ambiguous until you trace what does and doesn't run.

**Exact sequence on round failure (post-retry):**

1. Write tombstone line to transcript: `[ROUND FAILED: propose, Q6]`
2. **Stop.** No extraction call. No design doc write. No synthesis call.
3. Append tombstone to `## Still In Play` in current `brief.md` via direct file append — **not** a synthesis call.
4. Increment question counter. Continue to Q7.

That last point matters: the tombstone brief update is a file write, not an LLM call. Calling the synthesizer on a failed question is backwards — you'd be feeding it incomplete data to produce a brief update that should be a static string. The tombstone text is deterministic. Write it directly.

**Retry scope:** Retry applies to the specific failing round call only. If `propose` fails and retries successfully, `critique` runs normally. Don't re-run completed rounds.

**First-call behavior:** Agree — omit `## What Got Built` when `previous_brief` is empty. Mark this **DECIDED**.

**One flag:** The proposal says "write tombstone to transcript per round" but also "skip that question entirely." If `propose` succeeds and `critique` fails, the propose output is already on disk. The tombstone should name the failing round specifically — `[ROUND FAILED: critique, Q6]` — so the partial record is interpretable.


<!-- complete -->
