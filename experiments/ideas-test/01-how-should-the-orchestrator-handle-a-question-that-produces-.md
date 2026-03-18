# How should the orchestrator handle a question that produces contradictory proposals?

*Generated: 2026-03-18 05:56 | Question 1 | 138s | Mode: ideas*

## Decisions

### DR-001: Handling Contradictory Proposals in Synthesis

**Status:** Accepted
**Context:** When two proposers generate fundamentally incompatible designs, the synthesis step needs a deterministic rule for producing actionable output.

---

## Rule: Dual-Output Synthesis with Structural Promotion

The synthesizer always produces two artifacts. A structural validation pass determines which one is the primary output. The user always receives a recommendation.

---

## Behavior

### 1. Critique Round: Flag Incompatibilities Early

During the critique round, each critic's prompt includes a `compatibility_flags` field requiring a structured list of conflicting assumptions between the two proposals.

Format:

```yaml
compatibility_flags:
  - assumption_a: "System should eagerly load all data at startup"
    assumption_b: "System should lazy-load data on demand"
    domain: "data access pattern"
  - assumption_a: "Single deployment unit"
    assumption_b: "Independent service boundaries"
    domain: "deployment architecture"
```

This surfaces structural tension before scoring begins, where numerical evaluation would obscure it.

### 2. Synthesizer: Always Produce Both Outputs

The synthesizer receives both proposals, all critiques (including compatibility flags), and evaluation scores. It produces exactly two artifacts every time, regardless of whether conflicts were flagged:

- **`recommendation.md`** -- Best-effort unified design. The synthesizer's honest attempt at merging both proposals into a coherent whole. Always present. Always leads.
- **`decision_record.md`** -- Two-option fork documenting the tension. Each option includes:
  - The assumption it rests on
  - What it optimizes for
  - What it sacrifices
  - Conditions under which you would pick it

### 3. Structural Validation: Mechanical Confidence Scoring

A post-synthesis validation pass inspects the merged `recommendation.md` for weasel indicators -- language that signals unresolved tension rather than genuine synthesis:

**Weasel patterns** (substring and regex matching):
- "depending on requirements"
- "could also"
- "if requirements dictate"
- "alternatively"
- "either X or Y"
- Conditional architecture statements ("if scale demands," "should latency require")

**Scoring rule:**
- Count weasel indicator occurrences in the recommendation
- **0-2 occurrences:** `confidence: high` -- the merge is coherent
- **3+ occurrences:** `confidence: low` -- the merge is masking unresolved tension

### 4. Output Assembly: Recommend First, Hedge Second

The session output folder receives:

| Confidence | Primary Output | Supporting Output |
|---|---|---|
| `high` | `recommendation.md` | `decision_record.md` (archived, not promoted) |
| `low` | `recommendation.md` with confidence banner | `decision_record.md` (promoted as companion) |

The `recommendation.md` header includes:

```markdown
## Recommendation
**Confidence:** high | low
**Compatibility flags found:** N
**Weasel indicators detected:** N
```

When confidence is low, the recommendation file includes a notice:

```
> This recommendation contains unresolved design tensions.
> See decision_record.md for a structured comparison of the competing approaches.
```

---

## Design Principles Behind This Rule

### Always recommend, never punt

A decision record alone is homework. The user opened a session with a question and deserves an answer. Even when the system is uncertain, it leads with its best attempt and flags the uncertainty honestly.

### Detection is mechanical, not judgmental

LLMs are conflict-averse. Asking a stateless subprocess "are these compatible?" produces false compatibility. Instead, compatibility is surfaced through structured fields in the critique round and validated through pattern-matching in post-synthesis. The LLM's role is generation, not adjudication.

### No separate "bridge" step

If a higher-order reframing exists that dissolves the contradiction, the merge attempt finds it naturally. Adding a distinct bridge phase under token pressure produces exactly the mushy compromises this rule exists to prevent.

### Score proximity is not a compatibility signal

Two proposals can score identically and be perfectly mergeable, or score far apart and rest on the same assumptions. Compatibility flags on conflicting assumptions are the correct detection mechanism.

---

## Prompt Engineering Requirements

### Critique round addition

Append to each critic's system prompt:

```
After scoring, list any assumptions in Proposal A that directly
conflict with assumptions in Proposal B. Use the compatibility_flags
YAML format. If no conflicts exist, return an empty list.
```

### Synthesizer prompt structure

```
You will receive two proposals and their critiques.

1. Produce a unified recommendation that resolves or integrates both
   designs. Do not hedge. Make choices. If one proposal's approach is
   clearly stronger for a given concern, adopt it.

2. Separately, produce a decision record treating the two proposals
   as competing options. For each option, state: the core assumption,
   what it optimizes, what it sacrifices, and when you would choose it.

Output both as separate markdown documents.
```

### Adversarial prompting for conflict aversion

The synthesizer prompt must include:

```
Do not soften contradictions. If the proposals disagree on a
fundamental assumption, say so directly. Do not use phrases like
"both approaches have merit" without immediately stating which
one you are adopting and why.
```

---

## Failure Modes and Mitigations

| Failure Mode | Mitigation |
|---|---|
| Synthesizer always claims compatibility | Adversarial prompting + structural weasel detection catches false merges |
| Synthesizer always claims incompatibility | Compatibility flags from critique round provide ground truth; if critics found zero conflicts, low confidence is suspicious |
| Decision record becomes an escape hatch for lazy synthesis | Decision record is always secondary; the system forces a merge attempt first |
| Weasel threshold is miscalibrated | Threshold of 3 is a starting point; tune after reviewing 5-10 session outputs |
| Recommendation is incoherent but passes weasel check | Future improvement: add a coherence validation agent; V1 accepts this risk |

---

## Implementation Scope for V1

- Add `compatibility_flags` field to critique round prompt templates
- Modify synthesizer prompt to always produce dual output
- Add post-synthesis weasel detection (string matching, not LLM-based)
- Add confidence field to recommendation header
- Write both artifacts to session output folder with appropriate naming

No changes to the 3-round structure. No additional rounds or subprocess calls. This is prompt engineering and output formatting, not architecture.