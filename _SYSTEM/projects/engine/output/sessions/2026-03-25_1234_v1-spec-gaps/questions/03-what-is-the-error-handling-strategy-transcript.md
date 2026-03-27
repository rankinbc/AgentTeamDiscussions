# Transcript: What is the error handling strategy?

*Generated: 2026-03-25 12:42*

## Round: PROPOSE

### The Cognitive Architect (creativity engine designer)

## Error Handling: Triage-First, Never Dark

The core principle: **every call failure produces a artifact, never a void.**

### Retry Policy (resolves open question)
Two retries, exponential backoff: 30s then 90s. After three failures, the call is dead. This applies uniformly to all LLM calls — discussion rounds, extraction, synthesis.

### Round-Level Failure
If critique or evaluate fails (after retries), the session **advances anyway**. The design doc is assembled from whatever rounds completed. A question with only a propose round produces a thin doc — but that doc is still written to disk with a `partial: true` flag in its header. Partial is not nothing.

### Question-Level Failure
If propose fails (nothing to build on), skip to question 7. But write a stub file: `q6_failed.md` containing the question text and failure log. This preserves the chain numbering for prior-doc context assembly — downstream questions see a gap, not a renumbering.

### Fragment Fallback (resolves open question)
If extraction fails, generate a deterministic stub fragment: `question_id` from the session, `decision` = "Discussion did not complete," `needs_your_call` = the question title verbatim, `blocker` = empty. This costs no LLM call and guarantees the Morning Brief has an entry for every question.

### Morning Brief Treatment
Failed questions surface under a fourth section: **"Not Completed"** — separate from "Don't Start Yet." The distinction matters: blockers are intellectual, failures are operational. Don't conflate them.

### Synthesis Failure
Already decided: deterministic fallback from fragments. No additional handling needed.

### The Flow Orchestrator (mechanical flow designer)

## Mostly Agree — One Cut, One Sequence Question

**Retry policy: accept.** 30s/90s backoff, three strikes dead. Uniform across all LLM calls is cleaner than per-call policies. No objection.

**Fragment stub fallback: accept.** Deterministic, zero cost, guarantees brief coverage. This resolves the open question cleanly.

**Cut the fourth Morning Brief section.** "Not Completed" as a distinct section adds complexity to the synthesis prompt, the fallback template, and the user's reading model — for an edge case. Failed questions already need human attention. Put them in "Needs Your Call" with an explicit `(session failure)` label. The user gets the same information, the synthesis prompt stays three sections, and the fallback path doesn't branch. The distinction between intellectual blockers and operational failures is real, but it doesn't require a new section to communicate.

**Cut `partial: true` in the doc header.** Nothing reads it in V1. If no downstream consumer acts on that flag, it's documentation noise. The stub file for a fully-failed question is sufficient; a partial doc is just a doc.

**Sequence question on question-level skip:** when propose fails after retries, what is the exact trigger that advances the session? Is it timeout expiry, exception catch, or explicit failure state? "Skip to question 7" is the right behavior — I just want the state machine to be explicit: `QUESTION_FAILED` is a terminal state for that question, not a recoverable one, and the session loop checks for it before incrementing.

The rest holds.

## Round: CRITIQUE

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

## Round: EVALUATE

### The Context Surgeon (context efficiency evaluator)

## Agenda: Error Handling Strategy

The prior discussion already resolved the most important question without naming it: **the blast radius is context chain corruption, not call failure**. The tombstone design doc proposal handles it. I'm adopting it. Move on.

Here's what actually needs decisions:

**1. Retry taxonomy (two retries is insufficient specification)**
Rate limits and transient failures require different handlers. This isn't preference — it's correctness. Proposed:
- Transient (timeout, 5xx): 2 retries, 5s fixed backoff
- Rate limit (429): 2 retries, exponential backoff with jitter, respect `retry-after` header if present
- That's the full policy. One config block, two keys.

**2. Partial round failure within a question**
If propose succeeds, critique fails: save the partial transcript, write a tombstone design doc, skip extraction, continue. The transcript is evidence; never discard it.

**3. Fragment fallback on combined call failure**
This is the open question from Q2. Proposed: if the combined extraction call fails after retries, write a sentinel fragment with `question_id`, `decision: "[extraction failed]"`, `needs_your_call: null`, `blocker: null`. The synthesizer sees it, omits it from Ready to Build, and surfaced it in Needs Your Call. Session never exits without the Brief.

**4. Synthesis failure with all rounds succeeded**
Fallback is already decided — direct fragment concatenation into three-section framing. No new decision needed.

**What I want from critics:** challenge the tombstone doc. Is one sentence enough? Is it too much? That's the only live design risk here.

### The Product Oracle (user advocate)

## The Morning Brief Is the Error Report

Everything proposed so far optimizes for session continuity. That's right. But I want to name the user's actual job here: **they read the Morning Brief and decide whether to act on it**. Error handling succeeds when the Brief is honest and actionable, not when it's technically complete.

**On tombstone docs: yes, one sentence is enough.** The user never reads tombstone docs directly — the synthesizer does. One sentence gives the chain enough signal. More than that is infrastructure theater.

**On the sentinel fragment: adopt Cognitive Architect's version, not the null fields.** Context Surgeon's `needs_your_call: null` is a gap the synthesizer may silently drop. The Architect's version — `needs_your_call` = question title verbatim — guarantees the user sees what failed. The question title *is* the call to action. Don't discard it.

**Cut the fourth Brief section. Full stop.** "Not Completed" as a category asks the user to care about operational failures before their coffee. They don't. "Needs Your Call" with a `(session error)` label is sufficient signal. One reading model, always.

**On retry taxonomy: the two-line distinction is correct and mandatory.** Rate limit vs. transient failure is not over-engineering — it's preventing a retry storm that makes a rate limit worse. But keep it two config keys, not a framework.

**The one thing nobody said:** if more than half the questions fail, don't produce the Brief. Produce a single-line error file instead. A Brief assembled from five tombstones isn't a Brief — it's noise dressed as output.

<!-- complete -->
