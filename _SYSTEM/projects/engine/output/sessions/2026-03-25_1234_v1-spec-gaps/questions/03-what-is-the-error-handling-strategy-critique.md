### The Adversarial Critic (adversarial reviewer)

## The Happy Path Assumptions Buried in This Question

Before anyone proposes a strategy, name what's being glossed over.

**"Failures are guaranteed" is underselling it.** At 70+ calls with network timeouts, rate limits, context length overflows, and malformed JSON, you're not designing for occasional failures — you're designing for cascading failures. Question 6 fails, its fragment is missing, question 7's context chain is now broken, questions 8-10 are reasoning from a gap. The retry policy doesn't fix this. The fragment stub doesn't fix this. The *design doc chaining* is the silent assumption nobody has stress-tested.

**Five problems to resolve before proposing retry counts:**

1. **Context chain poisoning.** Failed question = missing design doc = subsequent questions receive incomplete context. Does the session continue with a known gap, or does it attempt to patch? "Skip and continue" assumes downstream questions are independent. They're not — that's the whole point of chaining.

2. **Partial transcript saves.** "Save the partial transcript" sounds safe. What triggers the save? If propose fails mid-write, is the file corrupt, empty, or truncated? Who reads a corrupt file and what happens to them?

3. **Morning Brief omission vs. notation.** Stub fragment says "not completed." But the Brief synthesis prompt receives this stub alongside real fragments. Does the synthesizer hallucinate a resolution for the gap, or faithfully report it? That behavior is unspecified.

4. **Rate limit vs. transient failure.** Identical retry policy for both is wrong. Rate limits require backoff. Transient failures don't.

5. **What "synthesis fails" actually means.** Timeout? Malformed output? Wrong schema? Each has a different correct response. Treating them identically is lazy.

Propose with those constraints in frame.

### The Systems Pragmatist (infrastructure realist)

## The Critic is Right. The Orchestrator is Wrong on One Point.

The Adversarial Critic named the actual failure mode: **context chain poisoning**. Everything else in this discussion is downstream of that. Retry policy, stub fragments, partial transcripts — none of it matters if question 7 is reasoning from a gap and producing confident-sounding garbage that makes it into the Morning Brief.

**Resolve this first:** prior design docs chain forward as context. That's decided. A skipped question produces a stub fragment but **no design doc**. The next question's context assembly silently has a hole. The synthesizer doesn't know the hole exists. The output looks complete. That's the blast radius: not one failed question — potentially every subsequent question.

**Concrete fix:** When a question fails after retries, write a minimal tombstone design doc. Not a stub — a doc that explicitly states: "Question N was not resolved due to [failure type]. The following downstream questions should be treated as lacking this context." One sentence. Enough for subsequent questions to know the chain is broken.

**On the Orchestrator's cut:** I agree with removing "Not Completed" as a fourth Brief section. But the reason isn't simplicity — it's that the tombstone design doc already communicates the failure to downstream questions. The Brief then honestly says "Needs Your Call" because it genuinely does.

**The one thing still unresolved:** rate limit vs. transient failure handling. The Critic is right that identical retry policy is wrong. Rate limits need exponential backoff with jitter. Transient failures retry immediately. This is a two-line config distinction; don't skip it.


<!-- complete -->
