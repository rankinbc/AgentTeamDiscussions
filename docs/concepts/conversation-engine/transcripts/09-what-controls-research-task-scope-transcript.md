# Transcript: What controls research task scope?

*Generated: 2026-03-17 22:01*

## Round: PROPOSE

### The Cognitive Architect (creativity engine designer)

Interesting question, and the answer is: **all three, but they're not equal.**

**Output token cap is the primary lever.** 2k output cap per research call is already decided. That's your hard ceiling. The model stops generating, full stop. No negotiation, no overrun. This is the only constraint the API actually enforces mechanically.

**Time limit is the secondary lever.** Not wall-clock time -- *cost time*. A research call that burns 80k input tokens reading a massive context is expensive even if the output is tiny. So you need a input token budget too, probably 15-20k. This is where people get surprised: the expensive part of research isn't what the agent writes back, it's what you let it read.

**Scope framing is the interesting lever.** Here's where cross-pollination helps -- think about how academic grant proposals work. You don't control a researcher by setting a page limit on findings. You control them by **narrowing the question**. The thinking routine that triggers research should produce a *single focused query*, not "go learn about authentication." More like "what are the tradeoffs between JWT refresh tokens and sliding session windows for OAuth flows?"

The tighter the question, the less the token cap matters, because the model converges faster.

So the control stack is:

1. **Question specificity** -- strategic constraint (set by thinking routine)
2. **Input token budget** -- cost constraint (~15-20k)
3. **Output token cap** -- hard stop (2k, already decided)
4. **Call count cap** -- session constraint (2 per agent per session, already decided)

Word limits are just fuzzy token caps. Skip them. Tokens are the native unit -- use the native unit.

### The Flow Orchestrator (mechanical flow designer)

Three controls, layered. Each catches what the previous missed.

**1. Output token cap (hard).** 2k output tokens per research call. This is the primary constraint. The `claude -p` call gets `max_tokens=2048`. The model stops. No negotiation. This was decided in the between-round call spec -- research is the only unbounded cost vector, so it gets the tightest leash.

**2. Call count cap (session-level).** 2 research calls per agent per full session. Not per round -- per session. An agent that burns both in round 2 gets no more research for rounds 3-10. The Strategize routine should weigh this, but enforcement sits in the orchestrator, not the agent's judgment.

**3. Prompt scoping (soft).** The research call's system prompt constrains the question. The agent doesn't get to say "research everything about microservices." The thinking routine outputs a specific question. The orchestrator wraps it in a task prompt that says: answer this question, cite sources if available, stay within scope. Soft because the model can wander, but the output cap kills it before wandering costs real money.

**What's notably absent:** no time limit. The call takes as long as it takes within the output cap. Adding wall-clock timeouts to LLM calls creates partial-response failure modes that are worse than waiting. If latency becomes a problem, that's a model selection decision, not a scope control.

**The sequence matters.** Prompt scoping narrows the ask. Output cap bounds the answer. Call count bounds the lifetime. Miss any layer and research becomes the session's dominant cost.

Ten open items remain. Research scope isn't one of them anymore.

## Round: CRITIQUE

### The Systems Pragmatist (infrastructure realist)

**The Systems Pragmatist**

The prior two responses nailed the control stack. I'm not going to repeat it. Let me add what they're dancing around.

**The real scope control is the input budget, not the output cap.** Everyone fixates on the 2k output ceiling. Fine, that's your hard stop. But a research call that reads 60k tokens of context and writes 500 tokens back still costs you $0.15+ on the input side alone. Multiply by 12 agents times 2 calls and you've quietly doubled your session cost without tripping any output alarm.

Cap input tokens at 15-20k per research call. This is the constraint that actually controls spend.

**Prompt scoping is where this system lives or dies in practice.** The Architect's grant proposal analogy is correct. A well-scoped question makes the token caps irrelevant because the model converges in 800 tokens. A vague question hits the 2k wall mid-thought and you get a truncated answer that's worse than no answer -- the agent now has partial information it treats as complete.

So here's my failure mode concern: **what happens when the thinking routine produces a bad question?** The Strategize routine is itself an LLM call. It can generate "research distributed consensus algorithms" just as easily as a tight query. The output cap catches the cost. Nothing catches the quality.

V1 mitigation: log the research question alongside the result. When research calls consistently hit the 2k ceiling, that's your signal the question generator is broken, not that the cap is too low.

Don't add word limits. They're token caps with worse precision.

### The Adversarial Critic (adversarial reviewer)

Both proposals converge on the same three-layer stack. That's suspicious. When two designers agree this fast, they're usually both wrong about the same thing, or they're both right about the obvious parts and blind to the same gap.

The gap: **neither addresses input token budget as a first-class control.**

The Architect mentioned it -- "15-20k input tokens" -- then buried it under "scope framing" like it's a minor detail. The Orchestrator skipped it entirely. But input tokens are where the real cost lives. A research call that reads 80k of context and writes 500 tokens of output costs more than one that reads 10k and writes 2k. Your output cap is controlling the cheap side of the equation.

Second problem: **prompt scoping is not a control, it's a hope.** Calling it "soft" is generous. You're asking an LLM to stay focused. The entire project exists because LLMs don't stay focused without mechanical constraints. Every other system in this design uses numeric levers -- magnitudes, thresholds, token budgets. Research scope gets... a well-worded prompt? That's the one place you decided to trust the model?

What's actually needed:

1. **Output cap** -- 2k, decided, fine
2. **Input cap** -- not decided, not optional. Pick a number.
3. **Call count** -- 2/session, decided, fine
4. **Question validation** -- the orchestrator should reject research queries that fail a specificity check before the call fires. Not "soft scoping." A gate.

Prompt scoping without a gate is a suggestion box. You need a bouncer.

## Round: EVALUATE

### The Product Oracle (user advocate)

**The Product Oracle**

The users of this system -- the people reviewing session output at 7am -- don't care how you constrain research. They care whether research *improved the conversation*. Work backward from that.

The job-to-be-done for research is: **bring back one insight the team didn't have, scoped tightly enough to act on.** Every control should serve that job.

The panel's converging on the right stack. Let me reframe it through the lens of what matters to the person reading the transcript:

**The question is the product.** A great research question produces a useful answer in 400 tokens. A bad one produces noise at 2k. The thinking routine that generates the question is doing the real scope control -- everything else is damage mitigation. Invest your design energy here.

**Input budget is the hidden cost lever.** The Critic and Pragmatist are right to push this. Cap it at 15-20k. Users won't see this number, but they'll feel it when sessions cost 3x what they expected.

**The four-layer stack, ordered by impact on user value:**

1. Question specificity (quality gate -- highest leverage)
2. Input token cap (~15-20k -- cost control)
3. Output token cap (2k -- hard stop)
4. Call count (2/session -- lifetime budget)

**One addition nobody's made:** log whether the agent *used* the research result. If research findings don't surface in the next round's discussion, the question was wrong, the curator dropped it, or both. That's your quality signal. Not whether you stayed under 2k -- whether the investment paid off.

### The Context Surgeon (context efficiency evaluator)

**The Context Surgeon**

The control stack is settled. Four layers, three mechanical, one aspirational. Let me assess what this costs the context budget and what's still leaking.

**What's decided:**
- Output cap: 2k tokens (hard, API-enforced)
- Input cap: 15-20k tokens (consensus but not formally locked -- the Critic is right to flag this)
- Call count: 2 per agent per session (decided in prior spec)
- Prompt scoping: everyone agrees it matters, nobody agrees on enforcement

**Context budget impact:** Each research call consumes 15-20k input + 2k output. Two calls per agent, six agents = 204-264k tokens per session on research alone. That's 3-4% of the projected 6.4M session budget. Manageable, but only because the caps hold.

**What I'm flagging:** The Critic's "question validation gate" idea sounds clean but adds another LLM call to judge the question before the research call fires. That's 12 additional calls per session if every agent researches. The cure costs more than the disease. Log the questions, review the truncation rate, fix the prompt that generates bad questions. Cheaper, same outcome.

**The real unresolved item:** Input cap needs a number committed, not a range. 15k or 20k -- pick one. A 5k variance across 12 calls is 60k tokens of budget uncertainty. That's an entire agent's discussion context.

**Decision status:** Three of four layers are mechanical and locked. Prompt scoping remains the soft spot. Don't add a gate. Tighten the thinking routine prompt that generates the question. Control the source, not the output.
