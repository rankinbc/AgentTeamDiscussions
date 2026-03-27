# Transcript: How does decision extraction work?

*Generated: 2026-03-25 12:25*

## Round: PROPOSE

### The Cognitive Architect (creativity engine designer)

## Decision Extraction: One Call, Epistemic Markers, Fail-Empty

**The core insight:** LLMs signal commitment level through modal verbs. "We will use X" is categorically different from "We should consider X" or "X might work." The extractor should detect these epistemic markers, not infer intent from position or emphasis.

**The extraction prompt:**

```
Read the design doc below. Extract every decision, recommendation, and suggestion.

Classify each by commitment level:
- FIRM: "will", "decided", "we are using", past tense conclusions
- WORKING: "should", "recommend", active voice without hedge
- TENTATIVE: "might", "could", "worth considering", "one option"

Return JSON only. No explanation.
```

**Schema:**

```json
{
  "decisions": [
    {
      "id": "q1_d1",
      "question_index": 1,
      "text": "one sentence, present tense",
      "commitment": "firm | working | tentative",
      "evidence": "verbatim phrase that triggered classification",
      "extracted_at": "ISO timestamp"
    }
  ]
}
```

**Why `evidence` matters:** It's the anti-hallucination anchor. If the extractor can't quote the source, the classification is suspect. Downstream reviewers can audit it.

**Garbage handling:** Validate that the response is parseable JSON with at least one item. On failure — malformed JSON, empty array when design doc is non-empty, or missing required fields — write `decisions_fallback_{n}.json` and log the raw response. Never write partial data to `decisions.json`. This also resolves the open question on fallback trigger scope: structural validation catches garbage before it corrupts the chain.

**Bonus:** This same call extracts the sharpest objection — add one field: `"sharpest_objection": "verbatim sentence"`. One extraction call handles both open questions from Q1.

### The Flow Orchestrator (mechanical flow designer)

## Agree on one call. Cut the three tiers. Fix the sequencing.

**What the Cognitive Architect gets right:** Single extraction call that also captures `sharpest_objection` — that's the right move. Resolves both Q1 open questions in one shot. The evidence field is a legitimate audit anchor, not gold-plating.

**Cut the commitment tiers.** Firm / working / tentative sounds useful but trace who consumes it. The brief generator gets `decisions` as input — does it treat tentative items differently? If not, we're extracting three categories and using one. Ship one tier: it's a decision or it isn't. If the extractor is uncertain, it should omit, not classify.

**Sequencing problem.** The decided execution order is: `evaluate → extract fields → write design_doc.md → synthesize`. The Cognitive Architect's prompt says "read the design doc below" — but design_doc isn't written yet at extraction time. The extraction source is the **evaluate round output**, not design_doc. This needs to be explicit in the prompt and in the sequence spec.

**Minimum schema:**

```json
{
  "decisions": [{"text": "...", "evidence": "..."}],
  "open_questions": ["..."],
  "sharpest_objection": "..."
}
```

Drop `id`, `question_index`, `commitment`, `extracted_at`. Session folder provides timestamp. Downstream can index by array position if needed.

**Fallback trigger** resolves to: API failure OR invalid JSON OR missing required top-level keys. Write `extraction_fallback_{n}.json`. Never write partial data. This is consistent with the synthesis fallback pattern already decided.

## Round: CRITIQUE

### The Adversarial Critic (adversarial reviewer)

## The extraction source is still unresolved. Everything else is premature.

The Flow Orchestrator says extract from the **evaluate round output**. The question asks about extracting from **design_doc.md** — "free-form markdown from an LLM synthesis call." These are different documents. Pick one and commit, because the prompt, the schema, and the garbage-handling all depend on which artifact you're parsing.

**Problem 1: Binary classification doesn't survive LLM output.** "It's a decision or it isn't" collapses the moment the evaluate round produces "we lean toward X" or "the group preferred Y but noted Z." The extractor will hedge. You've moved the classification problem into the extraction prompt and pretended it disappeared.

**Problem 2: No actual prompt.** We have a schema and a fallback rule. We do not have a prompt. The question asks what prompt extracts decisions. That is the hard part. Proposing a JSON schema without the prompt is skipping the work.

**Problem 3: Garbage fallback is incomplete.** Write `extraction_fallback_{n}.json` — then what? Synthesis still runs. Does it run with empty inputs? Does it skip? Does it halt the session? The fallback file is where data goes to die if nothing downstream consumes it. Specify the recovery path or the fallback is decoration.

**Problem 4: Evidence fields hallucinate.** An LLM asked to quote evidence from its own output will confabulate plausible-sounding citations. If evidence is an audit anchor, it needs to be a verbatim substring match, not a generated summary.

Resolve the source. Then write the prompt.

### The Systems Pragmatist (infrastructure realist)

## The Adversarial Critic is right on source. The Orchestrator is right on sequence. Resolve the conflict, then commit.

**The source question is already answered by the decided execution sequence.** Extract from the **evaluate round output**. Design docs haven't been written yet at extraction time. The question's framing ("free-form markdown from an LLM synthesis call") describes a document that doesn't exist yet when extraction runs. That's not a debate — it's a sequencing fact.

**Drop confidence scores entirely.** The question asks for them; I'm saying they're a trap. LLM-generated confidence is uncalibrated noise. You'll get `0.8` on a hedge and `0.9` on a hallucination. If you want to distinguish firm decisions from soft ones, make the extraction prompt do binary classification: output the decision or omit it. If it's hedged enough that the extractor can't commit, it's an open question, not a decision.

**The Adversarial Critic's evidence hallucination point stands.** Drop the evidence field. If you want an audit anchor, log the entire evaluate round output alongside decisions.json. That's a file copy, not an LLM extraction task.

**Garbage recovery path:** If extraction fails (API error, invalid JSON, missing required keys), write `extraction_fallback_{n}.txt` with raw evaluate output, set `decisions = []` and `open_questions = []` for synthesis inputs, and continue. Synthesis runs with empty inputs and produces a degraded brief. Session doesn't halt. Log the failure in `session.log`. This is consistent with the synthesis fallback pattern.

**Minimum viable prompt:** "From the agent evaluation below, extract firm decisions as JSON. A firm decision is a statement the group concluded, not proposed. If uncertain, omit."

## Round: EVALUATE

### The Product Oracle (user advocate)

## The User Never Reads decisions.json

Step back: who is extraction *for*? The Morning Brief. That's the artifact a human reads. Decisions.json is a pipeline artifact. Its quality only matters if it degrades what the user sees tomorrow morning.

That reframe resolves most of the debate.

**On source:** The Systems Pragmatist is correct. The decided execution sequence settles this. Extract from the evaluate round output. Not design_doc — that hasn't been written yet. Close this.

**On classification tiers:** Cut them. The Flow Orchestrator and Systems Pragmatist agree: binary or omit. If the extractor can't commit, it's an open question, not a decision. Firm decisions and open questions are the two buckets that map to the brief's sections. A third "tentative" category maps to nothing and produces maintenance burden.

**On evidence fields:** Drop them. Log the full evaluate output as a sidecar file. That's one file copy, not an LLM confabulation task.

**Minimum schema:**
```json
{
  "decisions": ["..."],
  "open_questions": ["..."],
  "sharpest_objection": "..."
}
```

**On garbage recovery:** Continue with empty inputs. Degraded brief is better than halted session. The user wakes up to *something*. Log the failure visibly in session.log.

**The prompt that matters:**
> "From the agent evaluation below, extract firm decisions as JSON. A firm decision is a conclusion the group reached, not proposed. If uncertain, omit. Also extract unresolved questions and the single sharpest objection raised."

That's it. One call. No tiers. No evidence fields. Ship it.

### The Context Surgeon (context efficiency evaluator)

## This Is Converged. Mark It and Move Forward.

The group has reached consensus on every axis. My job here is to close the loop on what this resolves and flag the one thing nobody named explicitly.

**The open question from Q1 is answered.** "Sharpest objection extraction mechanism" was listed as unresolved. The Product Oracle's prompt resolves it: one extraction call, one field, sourced from evaluate round output. No dedicated second call. No regex. It's in the schema as `sharpest_objection`. Close that open question.

**The schema is correct. Validate it against its consumer.** The synthesis prompt contract (already decided) takes: extracted decisions, extracted open questions, sharpest objection. The proposed schema maps exactly to those three inputs. No impedance mismatch. This is the right test — schema validity is fitness for its downstream consumer, not internal elegance.

**Token budget check on the schema.** Three string fields per question. Decisions array at ~15 words each, open questions similar, objection one sentence. This stays well under the ~100 token per question bound established in prior decisions. The schema is budget-compliant.

**One thing to nail in the prompt: scope.** "The group concluded" is doing heavy lifting. Add: "from this question's discussion only — do not infer from prior context." Extractors confabulate across context boundaries. The evaluate round output is the only valid source window.

Everything else is settled. The minimum prompt, binary classification, evidence-field drop, garbage recovery path — all converged. Write the decision and move.

<!-- complete -->
