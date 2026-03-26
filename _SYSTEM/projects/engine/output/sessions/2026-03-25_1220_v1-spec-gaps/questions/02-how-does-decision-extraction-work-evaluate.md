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
