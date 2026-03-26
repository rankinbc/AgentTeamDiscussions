# Transcript: Graduated resistance: how should discussion intensity change over time?

*Generated: 2026-03-26 12:16*

## Round: PROPOSE

### The Cognitive Architect (creativity engine designer)

The martial arts metaphor is seductive and wrong. Randori works because human bodies have injury thresholds — you literally cannot start at full intensity without breaking people. LLMs have no such constraint. The graduated resistance model imports a biological limitation and repackages it as a design principle.

Here's what actually matters: **premature convergence kills discussions, not premature criticism.** The research on group creativity (Nemeth, 2018; Charlan Nemeth's work on authentic dissent) shows that early, genuine disagreement produces better final outputs than "safe" brainstorming followed by late-stage critique. The Osborn brainstorming model — defer judgment, then evaluate — has been empirically demolished for decades. Groups that argue from the start generate more ideas *and* better ideas than groups that play nice first.

**My design: Constant Resistance, Rotating Frame.**

Every round runs at full intellectual intensity. What changes is not the *force* but the *lens*. Round 1: agents attack the problem space (what's missing from the framing?). Round 2: agents attack each other's proposals (what breaks under pressure?). Round 3: agents attack their own positions (what am I wrong about?). The resistance never dips — the target rotates.

This requires zero runtime detection, zero dynamic adjustment, zero orchestrator intervention. It's implementable entirely through round-specific prompt overlays, which the existing `role_overlays.yaml` already supports. The mode definition in team YAML specifies which overlay each round gets. Ship it with what exists.

Different agents at different resistance levels simultaneously? Absolutely not. That's a coordination nightmare that produces incoherent discussions. Uniform frame, diverse perspectives — that's where real cognitive diversity lives.

## Position Summary
I advocate constant full-intensity resistance with rotating analytical frames per round, implemented entirely through existing prompt overlays. I reject graduated resistance as a misapplication of biological constraints to a system that has none. The empirical creativity research is unambiguous: authentic early disagreement outperforms deferred judgment, and our architecture already has every mechanism needed to deliver this.

### The Flow Orchestrator (mechanical flow designer)

The Cognitive Architect is half right and drawing the wrong conclusion from it.

Yes, graduated resistance imports a biological metaphor we don't need. Agreed — cut it. But "constant full intensity with rotating frame" is just graduated resistance wearing a trench coat. You're still changing what agents do each round. You're still sequencing lighter work (attack the problem space) before heavier work (attack each other). You've relabeled the gradient and called it flat.

Here's my actual concern: **what state does the orchestrator need to manage?** Right now: round name, agent list, overlay key. That's it. The Cognitive Architect's proposal preserves this — good. But let me trace the message lifecycle to show why even *his* version has unnecessary moving parts.

Three rotating frames means three distinct overlay configurations. Each requires a different prompt template injection. The orchestrator must track which frame applies to which round index. This is manageable but **it's not nothing** — it's a mapping table the mode definition must encode and the orchestrator must interpret.

**My counter-design: one frame, one overlay, zero rotation.**

Every round uses the same behavioral overlay. The only thing that changes between rounds is what other agents said — which changes naturally because responses accumulate. The system already provides escalating context by construction. Round 2 agents see Round 1 output. Round 3 agents see Rounds 1-2. **Context accumulation IS the intensity gradient.** We get graduated resistance for free without encoding it anywhere.

No frame rotation. No per-round overlay mapping. No orchestrator logic beyond "run the next round." The mode definition shrinks to: agent list, round count, single overlay.

## Position Summary
I advocate a single uniform overlay per mode with zero per-round variation, because context accumulation between rounds already provides natural escalation without any orchestrator mechanism. I reject both explicit graduated resistance and rotating frames as unnecessary complexity — they encode in configuration what the system already produces structurally. Every piece of round-differentiation logic is a piece that must be maintained, debugged, and explained, and the current architecture already delivers the effect for free.

## Round: CRITIQUE

### The Adversarial Critic (adversarial reviewer)

Both proposals share a dangerous assumption: that we can determine the right resistance strategy *before we have data on what's actually failing in discussions*. One claims constant high intensity is optimal. The other claims the system already handles it. Neither has evidence. Both are arguing from first principles about a system that exists and produces measurable output.

**Where the Cognitive Architect breaks:** "Empirical creativity research" on human groups doesn't transfer to LLM agents running on stateless subprocess calls. These aren't humans building psychological safety. Each invocation is a fresh context window with a prompt overlay. The claim that "authentic early disagreement outperforms deferred judgment" assumes agents that remember being disagreed with and adjust. Ours don't. They read a transcript and respond to a prompt. The mechanism of action doesn't exist here.

**Where the Flow Orchestrator breaks:** "Context accumulation provides natural escalation" is a testable claim that hasn't been tested. It's equally plausible that context accumulation produces convergence, not escalation — agents reading three rounds of discussion trend toward consensus, not harder critique. The assertion that round-differentiation is "unnecessary complexity" assumes the current output quality is acceptable. We don't know that either.

**The shared blind spot:** Both treat resistance level as a system-design question when it's an empirical question. We already decided (Q2, Q6, Q8) to instrument before optimizing. Why is this question exempt?

**The actual first-to-break component:** Any resistance architecture chosen without output-quality data. We'll tune something we can't measure, then argue about whether the tuning worked.

## Position Summary
I advocate deferring any resistance architecture decision until instrumentation from Q2/Q8 exists to measure whether discussion quality actually degrades in ways that resistance changes would fix. I reject both constant-intensity and natural-escalation as unfounded claims about LLM behavior that neither proposal can substantiate. The decisions we already made on Q2, Q5, Q6, and Q8 all follow the same principle — instrument first, optimize second — and breaking that principle here would be inconsistent.

### The Systems Pragmatist (infrastructure realist)

The Adversarial Critic is right on the core point and I won't waste words restating it. Instrument first. But I'll push further on something the Critic glossed over.

**The Orchestrator's "free escalation" claim has a specific failure mode.** Context accumulation in stateless subprocess calls doesn't produce escalation — it produces *anchoring*. Each agent reads the growing transcript and the most prominent positions become attractors. I've seen this pattern in every LLM-chain system I've worked with: more context means more convergence, not more friction. The Orchestrator's model predicts the opposite of what actually happens. This isn't theoretical — it's the default behavior of instruction-following models reading prior conversation.

**The Architect's rotating-frames proposal has an operational problem nobody mentioned.** Per-round overlay variation means the prompt template layer now has round-number-dependent logic. That's a coupling between `RoundRunner` and `PromptBuilder` that doesn't currently exist. When it breaks — and template logic always breaks — the blast radius hits every mode in every team. For a feature whose benefit is undemonstrated.

**What I'll add to the Critic's position:** "Defer until instrumentation exists" is correct but incomplete. We need to define *what measurement would trigger action*. Specifically: if instrumentation shows agent responses in rounds 2-3 have >X% semantic similarity to round 1 positions, that's evidence of the convergence problem. If it doesn't show that, this entire question is moot. Without that gate, "defer" becomes "forget."

The one thing all three prior speakers agree on — that the current system produces *some* useful output — is actually untested. We're debating optimization of a system whose baseline we haven't measured.

## Position Summary
I advocate the Critic's defer-until-instrumented position with an explicit measurement gate: semantic similarity between rounds as the trigger metric. I reject both the Architect's rotating frames (creates template-layer coupling with undemonstrated benefit) and the Orchestrator's natural escalation claim (context accumulation produces anchoring, not friction). Ship the Q2/Q8 instrumentation, define the convergence threshold, and revisit only if the data shows a problem.

## Round: EVALUATE

### The Product Oracle (user advocate)

## The Product Oracle — Evaluate Round

The user runs a session. They read the Morning Brief the next morning. **Does graduated resistance change what they read?**

No. Not today, not with evidence, not even theoretically.

Here's the user's job-to-be-done: "Give me a design document that surfaces perspectives I wouldn't have found alone." The Morning Brief is the delivery mechanism. Everything upstream exists to make that document better.

The Architect wants constant full-intensity resistance through rotating frames. The Orchestrator wants zero configuration and trusts context accumulation. The Critic and Pragmatist say defer until instrumentation exists. **The Critic wins, and it's not close.**

The Architect's proposal adds template complexity for an effect no user will perceive. Rotating analytical frames per round means more overlay configuration, more debugging surface, more things to explain in docs — all producing a Morning Brief that reads identically to one without them. I've seen this pattern a hundred times: internal sophistication that optimizes for mechanism elegance while the user experience stays flat.

The Orchestrator's "natural escalation" claim is elegant but unverified. The Pragmatist correctly flags that context accumulation might produce anchoring, not friction. We don't know. And that's exactly the point.

**We already decided this pattern six times.** Q2: instrument first. Q5: fixed rounds, no runtime detection. Q6: defer until data. Q8: log before optimizing. Breaking the pattern here would mean resistance architecture gets special treatment over every other open question — and it's the one with the *least* user-visible impact.

Ship the Q2/Q8 instrumentation. Define semantic similarity between rounds as the convergence metric. Revisit only when data shows the Morning Brief is losing perspective diversity.

## Position Summary
I advocate deferring resistance architecture until Q2/Q8 instrumentation reveals whether discussion quality actually degrades in ways resistance changes would fix. I reject both constant-intensity resistance and natural-escalation claims as internal mechanism debates with zero demonstrated impact on what the user reads in the Morning Brief. The six prior decisions established instrument-first as our design principle, and resistance architecture has the weakest case of any question for breaking that principle.

### The Context Surgeon (context efficiency evaluator)

## The Context Surgeon — Evaluate Round

Before I evaluate the proposals: **this brief's context payload is exhibit A for the Critic's position.** The decisions section is duplicated verbatim — Q1 through Q9 appears twice, burning tokens on identical content. If we can't keep our own discussion context clean, we have no business adding per-round overlay complexity to agent prompts.

Now the substance. Four agents converged on defer, one wants rotating frames. The Architect lost in the critique round and the Oracle buried the remains. The Orchestrator's "natural escalation" is a hypothesis dressed as architecture — the Pragmatist's anchoring counterpoint stands unrebutted.

The Critic's position wins because **graduated resistance is a context budget question masquerading as a design question.** Every overlay variation, every rotating frame, every per-round behavioral modifier consumes tokens in the assembled prompt. The Q8 decision already committed us to logging prompt size per invocation. Until that data exists, any resistance architecture is blind allocation — spending context budget on mechanism without knowing the balance.

The Oracle's framing is correct but incomplete. It's not just that the user won't perceive the difference in the Morning Brief. It's that resistance overlays *compete directly* with conversation history for context space. Adding rotating analytical frames means either truncating prior-round content earlier or hitting token limits sooner. That's a measurable tradeoff we cannot evaluate without Q2/Q8 instrumentation.

The Architect's rotating frames proposal fails on its own terms: it claims to optimize discussion quality while consuming the very resource — context window — that discussion quality depends on.

## Position Summary
I advocate deferring resistance architecture until Q2/Q8 instrumentation quantifies prompt assembly costs, because resistance overlays compete with conversation history for finite context budget. I reject rotating analytical frames as a mechanism that consumes the resource it claims to optimize. Ship the logging, measure the budget, then decide what you can afford to spend on friction.


<!-- complete -->
