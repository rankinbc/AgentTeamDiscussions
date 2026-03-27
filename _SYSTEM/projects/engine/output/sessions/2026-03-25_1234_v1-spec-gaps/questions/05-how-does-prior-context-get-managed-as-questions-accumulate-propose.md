### The Cognitive Architect (creativity engine designer)

The 6000-char truncation is a blunt instrument solving the wrong problem. Truncating raw design docs is like summarizing a conversation by cutting off the last speaker mid-sentence — you preserve volume, not signal.

Here's the actual problem: **prior context serves one function** — preventing question N from contradicting or re-litigating what question N-3 already resolved. It is not a reference library. Agents don't need the full reasoning chain; they need the binding constraints.

**My proposal: sliding window of 3, verbatim.**

Pass the three most recent design docs forward, unmodified. Archive everything older. No summarization.

Why not summarization? Because summarization adds a lossy LLM call to every question transition, compounds errors across 10 questions, and solves a problem that doesn't exist at the scale we're building for. A 10-question session has at most 3 docs in the window — roughly 1,800 words of prior context. That's well within budget without any compression.

Why 3, not 2 or 5? Three captures the local coherence arc — setup, elaboration, consequence — without carrying stale early-session constraints that no longer bind. The first two questions are often framing questions whose decisions are already embedded in the decisions.json artifact. The window doesn't need to reach them; the decisions list does.

The fragment log already solves the long-range coherence problem. Prior docs solve short-range elaboration continuity. These are different jobs. Don't conflate them.

**Sliding window of 3, no summarization, decisions.json for long-range binding.** That's the architecture.

### The Flow Orchestrator (mechanical flow designer)

This is already decided. Sliding window of 3, verbatim, earlier docs archived. The Cognitive Architect is proposing the conclusion we landed on two questions ago. We are covering old ground.

The unresolved operational question is the assembly sequence, not the policy.

**Concrete sequence for question N context assembly:**

1. Session start: question IDs registered in order.
2. Question N begins: collect the three most recent *written* design docs by slot position — including tombstones.
3. Pass those three docs as prior context. No filtering, no modification.

The tombstone case is the only decision point here. A tombstone occupies a slot in the chain. If questions 5, 6, and 7 are in the window and question 6 tombstoned, does the window skip it and pull question 4? **No.** Tombstones stay in the chain. The tombstone's one-sentence content explicitly signals the gap. Skipping it silently re-introduces the invisible-failure problem we already solved at the session level.

So: window is the last 3 slots by position, tombstones included, no exceptions.

**What this resolves:** Prior docs pass tombstones forward as context-chain entries. Downstream agents see the gap explicitly rather than inferring from missing reasoning.

**What remains open:** The exact format the window docs are injected into the propose prompt — whether they're labeled by question ID, separated by headers, or appended raw. That's a prompt template detail, not an architecture decision, but it needs to be specified before implementation.


<!-- complete -->
