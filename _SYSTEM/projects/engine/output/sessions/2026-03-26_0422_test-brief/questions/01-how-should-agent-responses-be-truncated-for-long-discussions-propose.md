### The Flow Orchestrator (mechanical flow designer)

## The Flow Orchestrator — Round 1 Opening

Three options on the table. Let me kill one immediately.

**Smart summarization is cut.** It requires an LLM call to summarize before every LLM call to respond. That's a second failure point, added latency, and a lossy transformation you can't debug. The cost doesn't justify itself at this stage.

That leaves two real options: **full history** and **sliding window**. Here's the decision sequence:

**Step 1: Define the constraint.** What's the actual token budget per agent call? This isn't a design question — it's a number from the model's context limit minus the prompt template size minus the agent persona minus the brief. Calculate it once at session start. Call it `available_history_tokens`.

**Step 2: Check before truncating.** Every round, before building the prompt, measure total history tokens. If it fits in `available_history_tokens`, send everything. No truncation logic fires at all.

**Step 3: When it doesn't fit, sliding window.** Drop the oldest rounds first. Always keep Round 1 (the brief anchors everything). Always keep the last N rounds (where N is configurable in `defaults.yaml`). Drop the middle.

That's the entire mechanism. Three steps, one config value, zero LLM calls for truncation.

**What I need from this group:**

1. Do we agree summarization is deferred?
2. What's the right default for N (I say 3)?
3. Should dropped rounds be silent or replaced with a `[rounds 2-5 omitted]` marker?

Those are the only open items. Let's not invent more.

### The Cognitive Architect (creativity engine designer)

## The Cognitive Architect — Round 1 Response

Flow Orchestrator's mechanism is clean. I agree summarization is deferred. I agree on the marker over silent drops. But the proposal has a critical flaw: **every agent sees identical history.**

That's the opposite of how productive groups work.

Research on transactive memory systems (Wegner, 1987) shows that group intelligence emerges precisely because members remember *different things*. A team where everyone holds the same subset of information produces convergent thinking — which is the failure mode we should fear most in LLM discussions that already trend toward agreement.

**My modification:** The sliding window should be **role-stratified**, not uniform.

- **Proposers** keep Round 1 + last 2 rounds. They need the brief anchor and recent critique, but *forgetting* middle rounds prevents them from over-fitting to objections. This produces bolder proposals.
- **Critics/Evaluators** keep Round 1 + last 4 rounds. They need more context to catch contradictions and track whether concerns were actually addressed.
- **Synthesizers** get the widest window possible — they're the integrators.

One config value becomes three, keyed to role type in `experiment_modes.yaml`. Still zero LLM calls. Still deterministic.

**Why this works for LLMs specifically:** Claude doesn't "forget creatively" on its own — it weighs all visible context roughly equally. Artificially restricting what a proposer sees is the mechanical equivalent of the cognitive bias that makes human brainstormers productive: selective attention.

**On N=3:** Too rigid as a universal. N=2 for proposers, N=4 for critics, N=max for synthesizers.

The diversity of *what agents remember* is the diversity that matters.


<!-- complete -->
