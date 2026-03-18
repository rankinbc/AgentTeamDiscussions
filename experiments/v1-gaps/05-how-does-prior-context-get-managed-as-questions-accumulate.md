# How does prior context get managed as questions accumulate?

*Generated: 2026-03-18 04:00 | Question 5 | 115s | Mode: compete*

## Decisions

### D1: Context Strategy is Append-Only Ledger Plus Previous Doc

Two layers of prior context enter each question's agent prompts:

1. **Decisions Ledger** — a single append-only file that accumulates extracted decisions and open questions from every completed question. Never edited, never truncated, never summarized.
2. **Previous Design Doc** — the full, uncompressed design doc from the immediately prior question only. Not a window of 2-3 docs. Not all prior docs truncated.

No other prior context enters the prompt. Full design docs from earlier questions remain in the session folder for human review but are not loaded into agent context.

### D2: Decisions Ledger Format

Each question appends a block to the ledger in this structure:

```
### Q{n}: {topic tag}
- DECIDED: {terse constraint statement}
- DECIDED: {terse constraint statement}
- OPEN: {unresolved question or tension}
```

Rules:
- Decisions are stated as constraints, not rationale. "Session output is append-only" not "We chose append-only because..."
- Each decision is one line, max 50 words.
- Open questions carry forward until a subsequent question resolves them, at which point the resolving question's block includes the decision.
- Topic tags are short labels (e.g., "context management", "agent invocation", "output format") that identify the domain of each question.
- Expected budget: 200-300 characters per question. At question 10, the full ledger is approximately 2000-2500 characters.

### D3: Ledger is Append-Only, No Graph Surgery

The ledger is never rewritten, reordered, or deduplicated. If Question 5 supersedes Question 2, Question 5's block contains the new decision. Question 2's entry remains. Agents seeing both will encounter the contradiction and must resolve in favor of the later decision.

This is deliberately less elegant than a maintained dependency graph. The tradeoff: occasional redundancy in exchange for mechanical reliability. An LLM performing merge operations on a structured document it previously generated is an untested dependency with silent failure modes. A corrupted dependency graph looks correct. A missing append-only entry is obviously missing.

The dependency graph ("Design Spine") is a documented V2 optimization, contingent on proving extraction reliability first.

### D4: Extraction Happens During Synthesis

The synthesizer agent — the same agent that produces the design doc after each question's discussion rounds — also produces the ledger entries for that question. This is not a separate post-processing step or a dedicated extraction prompt.

The synthesizer already reads all agent contributions and distills them into a design doc. Extracting terse decisions and open questions from its own synthesis is a natural extension of that task, not a new capability.

### D5: Extraction Validation

After each question, a lightweight validation check runs: scan the new design doc for references to constraints or decisions. Compare against the new ledger entries. If the design doc contains a decision not reflected in the ledger, flag it in the session log.

This is not a blocking gate. It is a diagnostic signal. The flag goes into the session output for human review and for future evaluator scoring. The purpose is to measure extraction loss rate empirically rather than assuming reliability.

### D6: Context Construction at Prompt Assembly

When assembling the prompt for question N's agents, context is constructed as:

1. The full decisions ledger (questions 1 through N-1)
2. The full design doc from question N-1
3. The current question text

Total context budget at question 8: approximately 4000 characters (2500 ledger + 1500 previous doc). Well under the 6000-character constraint from the beta system, with every token traceable to a source document.

### D7: Thematic Gaps Are Accepted in V1

When question 8 depends on question 3's design doc (not just its decisions), the decisions ledger carries the constraint but not the rationale. This is a known limitation. If the ledger entry is insufficient — if an agent needs to understand why a constraint exists to evaluate whether a new approach violates its spirit — the information is not in context.

This gap is accepted for V1 because:
- The frequency of cross-question thematic dependencies is unquantified.
- Adding selective retrieval of earlier docs introduces complexity (topic matching, relevance scoring) that is unjustified without data.
- The extraction validation mechanism (D5) will surface cases where this gap causes problems, providing the data needed to justify a V2 solution.

---

## Open Questions

- **Extraction loss rate**: What percentage of meaningful constraints survive extraction into the ledger? The beta transcripts from questions 1-5 should be run through this scheme manually to measure coverage before relying on it at scale.
- **Supersession clarity**: When a later decision supersedes an earlier one, agents must infer this from the ledger's chronological order. If this proves unreliable in practice, a lightweight "SUPERSEDES Q{n}" tag may be needed on ledger entries.
- **Topic tag vocabulary**: Whether topic tags should be drawn from a fixed vocabulary or free-form. Fixed tags enable future retrieval optimizations but add a classification step. Free-form is simpler but less structured.