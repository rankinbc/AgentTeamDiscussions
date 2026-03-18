# Transcript: How does decision extraction work?

*Generated: 2026-03-18 03:51*

## Round: PROPOSE

### The Cognitive Architect (creativity engine designer)

# How Does Decision Extraction Work?

## The Core Insight

Don't ask the extractor to *find* decisions. Ask it to **classify every imperative statement** in the design doc. The failure mode isn't missing decisions -- it's the extractor hallucinating confidence levels it can't ground. So the prompt forces grounding by requiring textual evidence.

## Schema: `decisions.json`

```json
[{
  "id": "q3-d1",
  "decision": "Use WebSocket transport, not polling",
  "commitment": "firm | recommendation | suggestion",
  "confidence": "high | medium | low",
  "resolution_status": "resolved | partially_resolved | unresolved",
  "supporting_evidence": "Direct quote from synthesis showing consensus",
  "dissent": "Direct quote from critic round, or null",
  "source_round": "q3"
}]
```

The `commitment` field is the key discriminator. The prompt defines it structurally:

- **Firm**: Synthesis uses declarative language ("we will", "the system uses") with no hedging
- **Recommendation**: Synthesis endorses but qualifies ("should", "preferred approach")
- **Suggestion**: Mentioned as viable, not endorsed ("could", "worth exploring", "one option")

## Extraction Prompt (condensed)

> Read the design doc. For every statement that prescribes a choice, extract it. Quote the exact sentence that justifies commitment level. Quote any unresolved dissent from the critic. If you cannot find a supporting quote, set confidence to `low`.

The quote requirement is the garbage detector. When the extractor fabricates evidence, the quote won't exist in the source doc. The orchestrator runs a **literal substring match** of `supporting_evidence` against the design doc. Any extraction where the quote doesn't match gets flagged `confidence: low` automatically, regardless of what the LLM claimed.

No retry loop. No second call. Just demotion. The Morning Brief handles low-confidence items as risk flags, which is exactly where uncertain extractions belong.

### The Flow Orchestrator (mechanical flow designer)

# How does decision extraction work?

## Decisions

### Extraction is a single CLI call with JSON output

One `claude -p` call per question. Input: the design doc markdown. Output: JSON to stdout, validated, written to `decisions.json`. No intermediate files.

### Schema

```json
{
  "question": "string",
  "decisions": [
    {
      "id": "q1-d1",
      "statement": "string",
      "status": "decided | recommended | noted",
      "confidence": "high | medium | low",
      "critique_resolution": "resolved | partially_resolved | unresolved",
      "dissent": "string | null"
    }
  ],
  "open_questions": [
    {
      "id": "q1-oq1",
      "statement": "string",
      "blocking": true
    }
  ]
}
```

That's the whole schema. No nested objects, no metadata beyond what the Morning Brief consumes downstream.

### Status distinction comes from the prompt, not post-processing

The extraction prompt defines the three categories by their linguistic markers:

- **decided**: "We will", "The system does", definitive present/future tense with no qualifiers
- **recommended**: "Should", "the best approach is", conditional or advisory language
- **noted**: "Worth considering", "one option is", exploratory or deferred language

The extractor classifies. It doesn't invent. If the design doc is ambiguous, the status is `noted` and confidence is `low`. Conservative default.

### Garbage handling: JSON parse check, then field validation

Two gates:
1. `json.loads()` succeeds. If not, retry once with a "return valid JSON" nudge appended. If second attempt fails, write a stub `decisions.json` with zero decisions and log the failure.
2. Required fields present and values within allowed enums. Strip any decision missing required fields. Don't fail the session over one malformed entry.

No retry loops beyond the single retry. Two failures means the design doc was unparseable. Flag it; move on. The Morning Brief will note the gap.

## Round: CRITIQUE

### The Systems Pragmatist (infrastructure realist)

# Critique: Decision Extraction

Both proposals converge on the right core: single CLI call, three-tier commitment classification, conservative defaults. Good. Here's what breaks.

## The Quote Verification is Fragile

Cognitive Architect's substring match against the design doc sounds elegant. In practice, LLMs paraphrase. They'll return "We should use WebSocket transport" when the doc says "WebSocket transport is the recommended approach." Substring match fails. You've just demoted a perfectly valid extraction to low confidence because the LLM did what LLMs do -- restate things slightly differently.

**Fix:** Drop literal substring matching. The quote requirement in the prompt is still useful as a grounding constraint -- it forces the model to look before it classifies. But the verification step should be "quote field is non-empty and non-trivial," not "quote exists verbatim in source." Save yourself the false positives.

## Schema Disagreement Needs Resolution

One proposal bundles `open_questions` inside the same JSON. The other implies separate files. The Morning Brief doc says the brief receives `decisions.json` AND `open_questions.json` separately. Match that contract. Two files. One extraction call can produce both, but they ship as separate artifacts.

## The Single Retry is Correct

One retry on JSON parse failure, then stub and move on. No exponential backoff, no three-strike systems. At V1 scale, a failed extraction on one of ten questions is a minor gap, not a crisis. The Morning Brief notes it. The human reads the design doc directly. Done.

## Status Field Naming

Use `commitment`: `firm`, `recommendation`, `suggestion`. More precise than `status` or overloaded terms like "decided." The linguistic markers both proposals define are functionally identical -- pick one vocabulary and lock it.

### The Adversarial Critic (adversarial reviewer)

# Critique: Decision Extraction

Both proposals converge on the same core -- single CLI call, three-tier commitment classification, conservative failure handling. Good. But I have problems.

**The substring match is brittle theater.** Cognitive Architect's "literal substring match" verification sounds rigorous until you realize LLMs paraphrase constantly. The synthesis doc says "We'll use WebSocket transport for all real-time communication." The extractor quotes "Use WebSocket transport for all real-time communication." Substring match fails. You just demoted a perfectly valid, high-confidence decision to low. You'll drown in false-positive risk flags, training the human to ignore them -- the exact opposite of what risk flags exist for.

**Neither proposal defines the extraction boundary.** What counts as "the design doc"? The final synthesis only? The full transcript? The Morning Brief spec says extractions feed from design docs, but design docs contain the critic's voice too. If the extractor pulls a critic objection and classifies it as a decision, you've manufactured a contradictory decision set. The prompt needs an explicit instruction: extract only from the synthesis section, ignore critique passages.

**Open questions extraction is underspecified.** Flow Orchestrator includes `open_questions` in the schema but neither proposal explains the prompt logic for distinguishing an open question from a hedged recommendation. "We should consider X" -- is that `noted` or an open question? Both, apparently, depending on the extractor's mood.

**My recommendation:** Drop the substring match. Keep the quote requirement as a prompt discipline tool -- it forces the LLM to ground its work -- but validate structurally, not literally. Define the extraction scope explicitly. Specify open question criteria in the prompt.

## Round: EVALUATE

### The Product Oracle (user advocate)

# Evaluate: Decision Extraction

## The User Job

The human waking up to this brief has one job: **know which decisions to trust and which to interrogate.** Every schema field, every prompt clause exists to serve that sorting task. Anything that doesn't serve it is waste.

## What's Settled

Both proposals and both critics converge here:

- **Single CLI call per question.** No fragments, no accumulation.
- **Three-tier commitment** (`firm` / `recommendation` / `suggestion`) classified by linguistic markers in the synthesis. The prompt defines the markers; the extractor applies them.
- **One retry on JSON failure, then stub.** No retry loops. The Morning Brief notes the gap. The human reads the doc directly.
- **Two output files:** `decisions.json` and `open_questions.json`. Matches the Morning Brief contract.

## What Needs Deciding

**Drop the substring match.** Both critics are right -- paraphrasing kills it, and false demotions train humans to ignore risk flags. Keep the quote requirement in the prompt as grounding discipline. Validate that the field is non-empty and non-trivial. Nothing more.

**Scope the extraction explicitly.** The prompt must say: extract from the synthesis section only. Critic objections are context, not decisions. Without this boundary, you get contradictory decision sets.

**Define open question criteria.** An open question is something the discussion explicitly deferred or flagged as needing human input. A hedged recommendation is a `suggestion`. The prompt must distinguish: "we should consider X" is a suggestion; "this requires user input on Y" is an open question.

## Recommendation

Ship the schema with `commitment`, `confidence`, `resolution_status`, `supporting_evidence` (prompt-grounded, not literally verified), and `dissent`. That gives the Morning Brief everything it needs to sort trust from risk.

### The Context Surgeon (context efficiency evaluator)

# Evaluation: Decision Extraction

## What's Settled

Both proposals and both critics converge. Lock these:

**Single CLI call per question.** Design doc in, JSON out. One retry on parse failure, then stub and move on. No retry loops.

**Three-tier commitment classification** via linguistic markers in the prompt. The markers are identical across proposals. Use `commitment`: `firm`, `recommendation`, `suggestion` -- most precise vocabulary offered.

**Two output files.** `decisions.json` and `open_questions.json`. The Morning Brief contract already expects this. Don't bundle them.

**Conservative defaults.** Ambiguous language maps to `suggestion` + `low` confidence. Failed extractions produce stubs. The Morning Brief surfaces the gap.

## What Gets Cut

**Substring matching.** Both critics killed it for the same reason: LLMs paraphrase. You'll generate false demotions, training the human to ignore risk flags. The quote field stays in the prompt as a grounding discipline -- forces the model to cite before classifying -- but verification is structural only: non-empty, non-trivial quote string. Nothing more.

## What Needs Specifying

**Extraction boundary.** Neither proposal defined it. The extractor reads the synthesis section only, not critic passages. Without this, critic objections get classified as decisions. Contradictory output.

**Open question criteria.** Add explicit prompt language: an open question is something the discussion identified as unresolved and requiring future input. A hedged recommendation is a `suggestion`. If the synthesis says "this needs human judgment," it's an open question. If it says "one option is X," it's a suggestion. Prompt must distinguish these or the extractor won't.

## Schema (final)

Cognitive Architect's schema with `commitment` replacing `status`. Add `source_section` field pointing to the synthesis. Drop `supporting_evidence` as a verification mechanism; keep it as prompt discipline only.
