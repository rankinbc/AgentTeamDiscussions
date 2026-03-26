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


<!-- complete -->
