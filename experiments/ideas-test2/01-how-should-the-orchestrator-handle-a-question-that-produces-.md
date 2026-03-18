# How should the orchestrator handle a question that produces contradictory proposals?

*Generated: 2026-03-18 06:00 | Question 1 | 131s | Mode: ideas*

## Decisions

### Core Rule: Present Both, Never Merge

When two proposers generate fundamentally incompatible designs, the synthesizer never merges them. Merging destroys the information that made each proposal valuable and produces satisficing compromises. The system's value is clarity of disagreement, not resolution of it.

The synthesizer presents both proposals verbatim and names the divergence point. The Morning Brief becomes a decision document, not a consensus document.

### Synthesis Step Behavior

The synthesizer performs exactly three operations on contradictory proposals:

1. **Present both proposals verbatim.** No editorial smoothing, no narrative bridging, no partial merging. The full text of each proposal appears in the session output.

2. **Name the fork in one sentence.** Not "they disagree about architecture" but the specific design assumption where they diverge. Example: "Proposal A assumes the user configures teams per-run; Proposal B assumes teams are persistent across sessions." This sentence is the most valuable artifact the synthesis step produces.

3. **Flag the minority position.** Whichever proposal the agents converged toward less gets an explicit marker. The system structurally resists gravitational pull toward the comfortable option.

No scoring matrices. No similarity thresholds. No confidence calibration. These require measurement capabilities the system does not have in V1 and would produce false precision.

### Fork Cap

A maximum of **3 unresolved forks** per session reach the Morning Brief. This is the mechanism that prevents the brief from becoming a decision backlog.

When more than 3 forks accumulate during a session:

- The synthesizer selects the 3 highest-stakes forks based on how central the divergence is to the original idea seed.
- Remaining forks collapse to a one-line note: "Also diverged on [topic] -- defaulted to [majority/first-proposed] position."
- Collapsed fork details remain in the full session transcript for review if the user wants them.

The fork cap is a single integer in the session configuration YAML. Default: 3.

### No Parallel Tracks

Contradictory proposals are **not** carried forward as parallel threads into subsequent phases. The critique and evaluate rounds process only the synthesis output, not two separate proposal histories.

Rationale: every parallel track doubles downstream token cost. In a system where context windows are the binding constraint and phases run through stateless subprocess calls requiring history reconstruction, parallel tracks are unaffordable. A well-written fork description is 50-100 tokens. Two full parallel threads through remaining phases costs thousands. The fork description has higher information density by an order of magnitude.

### What Moves Forward After Synthesis

When proposals contradict, the synthesis step produces a single output artifact containing:

- Both proposals presented verbatim (for the session record and Morning Brief)
- The one-sentence fork description
- The minority flag
- A designation of which proposal subsequent phases should treat as the working direction

The working direction is chosen by alignment with the original idea seed. The synthesizer picks one track and records what it dropped. Downstream phases (critique, evaluate) operate on the selected track only. The dropped track exists in the synthesis artifact for human review but does not consume further context budget.

### Fork Record Format

Each fork produces a compact record stored in the session's `decisions.json`:

```
{
  "type": "fork",
  "topic": "one-sentence description of the divergence point",
  "selected": "A or B",
  "selected_rationale": "one sentence on why this track was chosen",
  "dropped_insight": "what the rejected track uniquely offered, under 50 words",
  "surfaced_to_brief": true/false
}
```

Fork records are the structured residue of contradictions. They are cheap to store, cheap to surface, and give the human the decision and the alternative without requiring them to re-read full proposals.

### When Proposals Are Not Actually Contradictory

If two proposals share the same core design and differ only in implementation details, they are not contradictory. The synthesizer treats them as complementary and produces a single unified output incorporating elements of both.

The synthesizer does not compute structural similarity metrics. It applies a simple heuristic: if you can describe both proposals' approach in the same sentence, they are not contradictory. If describing them requires "either X or Y," they are.

No numeric threshold (80% or otherwise) is used. Freeform text similarity has no reliable metric, and an LLM judging "are these really different" will drift toward "yes" because that is the more interesting answer. The heuristic stays qualitative.

### Morning Brief Integration

The Morning Brief includes a **Forks** section after the main synthesis content. This section contains:

- Each surfaced fork's one-sentence description
- Which direction was selected for downstream processing
- What the dropped track offered
- A clear label: "Your call -- details in session log"

The forks section appears only when forks exist. When all proposals aligned, the section is omitted. The brief never pads with "no contradictions found" filler.

### What This Design Explicitly Defers

The following capabilities are excluded from V1. They may be revisited after the base system proves that overnight runs produce contradictions worth preserving:

- **Confidence scoring.** No reliable signal exists for calibration. Agent agreement is the metric the anti-slop mechanisms suppress, making it unusable as a confidence input.
- **Similarity detection thresholds.** No reliable metric for structural similarity between freeform text proposals.
- **Contradiction classification taxonomies.** The system does not categorize types of contradiction. It names them and moves on.
- **User-tunable scoring dimensions.** Feasibility, novelty, and alignment scores sound clean but require judgment the synthesizer cannot reliably provide at this stage.

### Summary of Synthesizer Rules

1. Are the proposals genuinely incompatible? If no, unify them normally.
2. If yes, present both verbatim in the synthesis output.
3. Write one sentence naming the exact divergence point.
4. Flag the minority position.
5. Pick the stronger track for downstream processing based on idea seed alignment.
6. Write a fork record (under 150 tokens) capturing what was dropped and why.
7. If fewer than 3 forks have been surfaced this session, surface this one to the Morning Brief.
8. If 3 forks are already surfaced, collapse this one with a one-line note and default to the selected direction.
9. Downstream phases receive only the selected track. The fork record and both original proposals live in the session log.