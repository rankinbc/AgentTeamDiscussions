# Transcript: Are between-round activities separate `claude -p` calls per agent?

*Generated: 2026-03-17 21:58*

## Round: PROPOSE

### The Cognitive Architect (creativity engine designer)

Good question. This is where the design gets expensive fast if you're not careful.

**The call map per agent per round:**

1. **Thinking routine** -- 1 call. Agent picks one of three (Reflect/Research/Strategize). Research spawns a sub-call, so Research is actually 2 calls. Budget: ~4-8k output tokens.

2. **Intra-team talk** -- 1 call per agent, but it's a *group* call. One prompt, all teammates' idea/magnitude snapshots as input, agent responds with reactions. Not N calls per pair. Budget: ~2-4k output tokens.

3. **Save file generation** -- could fold into the tail of intra-team or thinking routine. Free if you're clever with the prompt. Separate call if you want clean separation. Budget: ~1-2k output.

4. **LLM Curator** -- 1 call. Compresses the filtered set into the Situation block. Budget: 8-15k output (this is the expensive one).

**Totals per agent per round:** 3-4 calls. ~15-29k output tokens.

**For a 6-agent, 2-team session:** 18-24 calls between rounds. Plus the actual discussion round calls.

Here's what interests me though -- the *Research* thinking routine is the wild card. It's the only one that reaches outside the closed system. Every other call is reshuffling known state. Research injects genuinely new information, which means its token budget has disproportionate impact on discussion drift.

**The design tension:** minimize calls for cost, but each merged call means less clean provenance in your audit ledger. The curator call alone justifies separation -- it's the reality-construction step.

What's your cost ceiling per round?

### The Flow Orchestrator (mechanical flow designer)

---

Tracing the between-round call sequence per agent.

**Yes, separate `claude -p` calls. Here's the breakdown:**

Each agent makes **up to 4 calls** between rounds:

1. **Save File Write** (1 call) -- Agent receives "summarize your round" task prompt against its current context. Produces the save file. This is the last call using the *round's* context window before it's discarded.

2. **Thinking Routines** (1-3 calls) -- Reflect, Research, Strategize. Each is an independent call with its own minimal context: identity + save file + routine-specific prompt. Research spawns an additional sub-call for the actual research query. **These are cheap calls** -- small context in, small structured output. ~4-8k input tokens each, ~500-1k output.

3. **Intra-Team Talk** (1 call) -- Agent receives teammates' idea/magnitude lists, produces reactions. ~6-10k input, ~1-2k output.

**BackgroundAgents are separate** -- they're not the agent's calls. They run in parallel, reading save files, writing magnitude mutations.

**Curator call** (1 per agent) runs *after* all the above complete.

**Total per agent per between-round:** 4-6 calls, ~25-40k input tokens, ~3-6k output tokens.

**Total per round for a 6-agent discussion (two 3-agent teams):** 24-36 calls, ~150-240k input tokens, ~18-36k output tokens. Plus BackgroundAgent calls, plus curator calls.

**Sequencing constraint:** Save file must complete before anything else. Thinking routines can parallelize. Intra-team requires all teammates' save files. Curator requires everything.

That's the dependency graph. The parallelization opportunities are real but the sequential bottlenecks are hard.

## Round: CRITIQUE

### The Systems Pragmatist (infrastructure realist)

Let me run the failure modes on those numbers.

**The call counts are roughly right. The cost projections are dangerously optimistic.**

Cognitive Architect says 18-24 calls between rounds for 6 agents. Flow Orchestrator says 24-36. Real answer depends on whether you count retries. And you will have retries.

**Failure modes nobody's mentioned:**

- **Save file generation fails or truncates.** Everything downstream depends on it. No save file = no thinking routines, no intra-team, no curator input. One bad save file poisons that agent's entire next round. You need validation and retry logic. Add 10-15% overhead to call counts.

- **Research sub-calls are unbounded.** Cognitive Architect flagged Research as the wild card but didn't propose a cap. A research call that returns garbage means the agent injects garbage into its magnitudes, which propagates through intra-team talk, through the curator, into every teammate's next round. **Hard timeout and token cap on Research, V1, non-negotiable.**

- **Intra-team talk has a fan-in dependency.** All teammates' save files must complete before any agent's intra-team call starts. With 3 agents per team, you're bottlenecked on the slowest save file writer. One slow agent delays the entire team's pipeline.

**My concrete position:**

Budget 30-40 calls per between-round cycle for 6 agents. Assume 200-300k input tokens, 25-45k output tokens. Build for the worst case, celebrate the average case.

Set a hard wall: if between-round costs exceed the actual discussion round costs, something is architecturally wrong. The discussion is the product. Everything else is plumbing.

### The Adversarial Critic (adversarial reviewer)

**The Adversarial Critic**

---

Two proposals, similar numbers, neither asking the hard question: **does this scale to anything worth running?**

Let's do the math they're dancing around.

A 6-agent, 10-round discussion. Taking the Flow Orchestrator's conservative estimates:

- Between-round calls: 24-36 per round x 10 = 240-360 calls
- Discussion round calls: 6 per round x 10 = 60 calls
- BackgroundAgent calls: unspecified (convenient)
- Curator calls: 6 per round x 10 = 60 calls

**Total: 360-480+ API calls per session.** At even modest token counts, you're looking at 2-4M tokens per run.

Three problems nobody's addressed:

**1. The Research routine breaks your cost model.** The Architect flagged it but didn't solve it. Research is unbounded -- it reaches outside the system. One agent doing Research every round could double your token spend. Where's the cap? Per-session research budget? Per-agent research frequency limit? Without this, your cost estimates are fiction.

**2. Merging save file generation into other calls isn't "free if you're clever."** It's a provenance contamination risk. The save file is the canonical state checkpoint. If it's generated as a side effect of intra-team talk, you can't distinguish "what I think" from "what my teammates pressured me to think." The audit ledger loses its value.

**3. Nobody's proposed failure handling for mid-sequence call failures.** If an agent's thinking routine call fails after save file but before intra-team, what state is that agent in next round? Stale save file plus no between-round processing. That's not graceful degradation -- that's silent corruption.

What's the failure contract per call stage?

## Round: EVALUATE

### The Product Oracle (user advocate)

**The Product Oracle**

---

The numbers are on the table. Let me reframe what they mean for the *user* of this system.

The job-to-be-done here is "run overnight, produce valuable artifacts by morning." That's the promise. So the real question isn't call counts -- it's **whether the between-round machinery justifies its cost relative to the discussion it serves.**

Here's where I land:

**Yes, separate calls. 4-6 per agent per between-round cycle.** The panel's converging on this. Save file, thinking routine (1-2 calls), intra-team talk, curator. For 6 agents: **30-40 calls between rounds**, 200-300k input tokens, 25-45k output tokens.

**The constraint I'd add:** between-round token spend must not exceed discussion round token spend. The Pragmatist nailed this. If your plumbing costs more than your product, you've built an expensive thinking-about-thinking machine.

**Three decisions I'd lock:**

1. **Research gets a per-session budget, not per-round.** Say 3 Research calls per agent per session. Forces strategic choice about *when* to research. That's a feature, not a limitation -- it creates genuine decision-making.

2. **Save file is always its own call.** The Critic's right -- merging it contaminates provenance. Pay the extra call.

3. **Failure contract: skip and log.** Failed thinking routine? Agent enters next round with just their save file. Failed intra-team? Agent misses teammate reactions. The system degrades gracefully because the save file is the checkpoint.

The overnight promise holds if you cap Research and enforce the cost ratio.

### The Context Surgeon (context efficiency evaluator)

**The Context Surgeon**

---

The numbers are converging. Let me cut to what matters for context efficiency.

**Call count is settled: 4-6 per agent per between-round cycle.** The proposals agree within noise. Don't relitigate this.

**What concerns me is the token arithmetic relative to context budgets.**

Each between-round call creates 500-2k tokens of output. Most of that output gets discarded. The save file preserves maybe 15-25% of between-round work. The deterministic filter cuts another 40-60%. The curator compresses what's left.

**End-to-end survival rate of between-round token spend:** ~5-10% reaches the agent's next Situation layer. We established this in the prior spec. That means of the 25-45k output tokens generated between rounds across all agents, roughly 1.5-4k tokens actually influence the next round's context windows.

That's the right ratio. But it means every call that doesn't contribute to those surviving tokens is pure overhead.

**Three context budget decisions needed:**

1. **Research cap: hard token limit per call, hard frequency limit per session.** The Critic is right -- this is the unbounded cost vector. I'd say 2k output tokens max, 2 research calls per agent per session for V1.

2. **Save file budget: 800-1200 tokens, validated.** It's the single artifact everything downstream depends on. Validation is cheaper than retry cascades.

3. **Don't merge save file generation into other calls.** The Critic's provenance argument is correct, and from my perspective: a contaminated save file means a contaminated deterministic filter means a contaminated curator input. The corruption compounds through every pipeline stage.

The Pragmatist's wall is the right heuristic: between-round costs should not exceed discussion round costs.
