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
