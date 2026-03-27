### The Adversarial Critic (adversarial reviewer)

**The brief-as-forward-chain has a structural compression problem nobody has quantified.**

The brief has hard word budgets: one sentence per question for What Got Built, max 4 bullets for Still In Play. By Q8, you've run 7 questions. You potentially have 20+ decisions and 15+ open questions. The brief fits ~4 open questions. The rest are silently dropped.

That's not managed compression. That's arbitrary lossy pruning by the synthesis model, with no audit trail and no guarantee the right 4 survived.

**Three specific failure modes:**

1. **Silent eviction.** "Carry forward unless explicitly superseded" is a prompt rule, not a mechanism. An open question not mentioned in Q5 or Q6 doesn't get explicitly superseded — it just falls off the brief. By Q8, it's gone. The implementer has no way to detect this.

2. **Rationale stripping.** The brief carries *what* was decided, not *why*. By Q8, a question that touches a Q2 decision will have no access to the reasoning that produced it. The one-sentence format enforces this loss. Later questions will re-debate closed ground without knowing it's closed.

3. **Synthesis drift accumulates.** Each brief write is an LLM call. Each call introduces small distortions. Seven sequential synthesis passes means Q8's brief may not accurately represent what Q1-Q3 actually concluded. There's no ground-truth check against decisions.json.

**The unstated assumption here:** that the brief's word budget is sufficient to carry all relevant context forward. It isn't. Someone needs to specify the eviction policy explicitly, or acknowledge what Q8 will be working with is a lossy shadow of the session.

### The Systems Pragmatist (infrastructure realist)

**The Adversarial Critic is right. And decisions.json already solves it.**

The brief-as-forward-chain has the right instinct — bounded, structured — but wrong implementation for agent context. The brief is optimized for human readability. The word budget that makes it a good Morning Brief makes it a bad context injection mechanism.

Here's what's already on disk after each question: `decisions.json` with structured decisions and open questions, already extracted, already bounded per-question. By Q8, that's a flat list of every decision the session has produced — not a synthesis model's prioritized subset.

**The fix is to use the right artifact for the right consumer:**
- Brief → human reader (Morning Brief function, unchanged)
- decisions.json → agent context for discussion rounds (replace the brief in steps 1–3)

The brief synthesis still runs. Still produces the Morning Brief. But discussion round inputs get `current_question + all_decisions_so_far + all_open_questions_so_far` from decisions.json — not the brief.

**Why this works:** decisions.json grows linearly with decisions made, not with questions asked. A 10-question session with disciplined extraction might produce 25 decisions total. At ~15 words each, that's ~375 words — well within any context budget. No eviction. No synthesis drift. No silent lossy pruning by an LLM that doesn't know what Q8 will need.

**One real concern:** extraction quality gates everything. If extraction degrades, decisions.json accumulates garbage and later questions drift anyway. But that failure is detectable — it's structural, not silent. That's the property you want.

The eviction policy question the Adversarial Critic raised is answered: don't evict. Carry everything. The data is small enough.


<!-- complete -->
