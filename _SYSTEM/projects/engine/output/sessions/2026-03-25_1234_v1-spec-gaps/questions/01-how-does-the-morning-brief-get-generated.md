# How does the Morning Brief get generated?

*Generated: 2026-03-25 12:36 | Question 1 | 169s | Mode: compete*

## Decisions

1. **Fragment-first architecture.** The Morning Brief is assembled from a fragment log, not from raw design docs. Design docs remain on disk as archival artifacts; the brief is navigation, not content.

2. **Incremental fragment accumulation, single synthesis call.** Fragments are extracted after each question resolves. The brief is generated once, at session end, from the complete fragment log. This is not an "incremental brief" — it is a final synthesis over a structured log.

3. **Fragment extraction runs async after each design doc is written.** It does not block the next question's context assembly. Q2 can begin as soon as Q1's design doc is on disk; fragment extraction for Q1 runs concurrently.

4. **Fragment schema uses output-aligned names:**
   ```json
   {
     "question_id": "str",
     "decision": "one sentence — what was resolved",
     "needs_your_call": "one sentence — the tension that required human judgment",
     "blocker": "one sentence or empty string — a tagged risk that was not dismissed"
   }
   ```
   Fields are hard-limited to one sentence each. Ten questions yields ~800 tokens of fragments total.

5. **Blocker extraction uses tagged convention, not an extra LLM call.** The critique round prompt template instructs critics to prefix risk flags with `BLOCKER:` or `RISK:`. Fragment extraction regex-scans critic output for these prefixes and copies matching sentences into the `blocker` field. If no tags appear, the field is empty. Empty is valid signal.

6. **The synthesis prompt receives exactly three inputs:** the fragment log, the output format template, and the word limit. No design docs, no raw transcripts, no decisions.json redundancy (decisions are already in the fragment log).

7. **Output sections use decision-gate framing, not process framing:**
   - `## Ready to Build` — decisions with enough confidence to act on
   - `## Needs Your Call` — tensions the agents could not resolve; require human judgment
   - `## Don't Start Yet` — all blockers, one line each; omitted if none

8. **One config field:** `brief_word_limit`, default 300.

---

## Synthesis Prompt (normative)

```
You are writing a handoff document for a human reading over coffee.
They need to know what is unblocked, what requires their judgment,
and what must not start yet. Do not summarize the discussion process.

Input:
<fragments>
{{ fragment_log }}
</fragments>

Output format (strict):
## Ready to Build
[One line per resolved decision. Only include if confidence is clear.]

## Needs Your Call
[One line per unresolved tension. These require human judgment to proceed.]

## Don't Start Yet
[One line per blocker. Omit this section entirely if no blockers exist.]

Word limit: {{ brief_word_limit }}. Be specific. Skip filler.
```

---

## Input Assembly Rules

- **Context problem:** Resolved structurally. The synthesis call never receives design docs. Total input budget is approximately 1,150 tokens (800 fragments + 200 system prompt + 150 format template). No chunking or summarization of summaries is required.
- **Fragment log format:** Append-only `.jsonl` file written to the session folder after each question. Each line is one JSON fragment object.
- **Decisions.json:** Not passed to the synthesis call. Decisions are already captured in the fragment log's `decision` field. `decisions.json` remains a separate machine-readable artifact for downstream tooling.

---

## Fallback Behavior

If the synthesis LLM call fails (timeout, API error, or rate limit), the session writes `morning_brief.md` by concatenating structured fragment data directly — no LLM required:

- All non-empty `decision` fields → `## Ready to Build`
- All non-empty `needs_your_call` fields → `## Needs Your Call`
- All non-empty `blocker` fields → `## Don't Start Yet` (section omitted if all are empty)

The fallback output is readable and uses the same section framing as the synthesized brief. The session never exits without a `morning_brief.md`.

---

## What Remains Unspecified

- The exact prompt template for the per-question fragment extractor (one LLM call per question; inputs are `transcript.md` and `design_doc.md` for that question; output is the four-field JSON fragment).
- Retry policy for the synthesis call before falling back (recommend: two retries with 30-second backoff, then fallback).
- Whether the fragment extractor itself has a fallback (if it fails, write an empty fragment with `question_id` populated so the question is represented in the log).
<!-- complete -->
