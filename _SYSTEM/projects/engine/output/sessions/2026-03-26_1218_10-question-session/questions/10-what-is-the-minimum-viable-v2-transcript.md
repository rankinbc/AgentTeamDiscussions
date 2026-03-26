# Transcript: What is the minimum viable V2?

*Generated: 2026-03-26 12:53*

## Round: PROPOSE

### The Cognitive Architect (creativity engine designer)

# The Three That Matter

The minimum viable V2 is exactly one structural change and two support mechanisms. Everything else is optimization.

**1. Blind Proposals — the only feature that changes the physics of discussion.**

Anchoring bias isn't a minor effect in LLM group dynamics. It's the dominant force. When Agent B reads Agent A's proposal before writing, you don't get two perspectives — you get Agent A's perspective with Agent B's vocabulary painted over it. Every creativity researcher from Osborn to Paulus confirms this: production blocking and anchoring destroy ideational diversity in groups. Blind proposals don't improve discussions. They make real discussions *possible* for the first time. Everything else is tuning a broken instrument.

**2. Tiered Summarization — because blind proposals are worthless if critique rounds can't hold context.**

You gain nothing from diverse proposals if the critique round receives truncated fragments. Tiered summarization isn't a nice-to-have — it's the structural prerequisite for proposals to *survive* into later rounds intact enough to matter. The eviction order is already decided. Ship it.

**3. Round-Type Prompt Differentiation — because "critique this" and "propose solutions" require different cognitive modes.**

Right now, round type is a label. It should be a behavioral lever. Propose rounds need expansive, generative framing. Critique rounds need adversarial, gap-finding framing. Evaluate rounds need integrative, trade-off framing. Three prompt templates, not seven personality novels. This is where the 800-token identity cap actually helps — less personality theater, more cognitive mode-switching.

Everything else — BITs, phase system, stale detection — layers on top. These three make the instrument play in tune.

## Position Summary
I advocate shipping blind proposals, tiered summarization, and round-type prompt differentiation as the minimum coherent V2 — three mechanisms that attack the three biggest failure modes (anchoring, context loss, and mode-indifferent prompting). I reject including the BIT system or personality transition in the minimum viable set because the swap test hasn't even determined whether personality is load-bearing yet. You fix the structural physics of discussion first; you decorate the agents later.

### The Flow Orchestrator (mechanical flow designer)

# The Architect Is Almost Right — But Misordered

Blind proposals are correct as #1. No argument. The sequencing change is mechanical: PromptBuilder withholds prior responses during propose rounds. One conditional. Done.

But #2 and #3 are wrong.

**Tiered summarization is not #2. It's maintenance.** The eviction order is decided. The summarization triggers on round boundaries. This is plumbing that ships alongside blind proposals because it's the same code path — PromptBuilder assembling context. Calling it a separate feature inflates the count. It's part of shipping #1 correctly.

**Round-type prompt differentiation is real, but it's #2, not #3.** Three prompt templates keyed to round type. The round runner already knows what round it's in. PromptBuilder already assembles prompts per-agent-per-round. You add a `round_type` template selector. This is the second-highest-impact change because it's the only thing that tells the LLM *what cognitive operation to perform* instead of letting it default to "write something smart."

**#3 is the completion report for overnight runs.** Not glamorous. Not architectural. But the question asks what makes overnight runs "noticeably better." Right now a failed overnight run produces a crash log. A successful one produces output files you have to read individually. One structured report — what ran, what completed, wall-clock time, any retries — is the difference between "overnight runs work" and "overnight runs are usable." Already decided as the only new artifact. Ship it.

Three features. Two touch PromptBuilder. One touches SessionRunner. No new subsystems.

## Position Summary
I advocate blind proposals (with tiered summarization as inherent implementation detail, not separate feature), round-type prompt templates, and the overnight completion report — because these are the three changes that touch the fewest components while addressing the three actual failure modes: anchoring, mode-indifferent prompting, and blind overnight operation. I reject counting tiered summarization separately because it inflates the feature count to hide that the real #3 slot is the unglamorous operational report that makes overnight runs actually usable.

## Round: CRITIQUE

### The Adversarial Critic (adversarial reviewer)

Both proposals agree blind proposals are the #1 priority. That's the assumption I want to break.

Blind proposals solve anchoring — agents won't parrot the first speaker. But anchoring is only a problem if agents are actually producing differentiated perspectives in the first place. If you run V1 right now with randomized speaking order (no code changes, just shuffle the agent list), do proposals meaningfully diverge? Nobody has tested this. You're building architectural machinery to solve a problem that might be mostly prompt-addressable with a single instruction line: "Do not reference or build upon other agents' positions."

If the anchoring problem is 80% prompt-solvable, blind proposals become an expensive structural change that delivers marginal improvement over a one-line prompt edit — while introducing real complexity: you now need a merge point where isolated proposals get recombined, you need to handle the cold-start problem where critique rounds reference proposals that were generated without shared context, and you've fundamentally changed the information flow that every downstream round depends on.

Second problem: both proposals treat "overnight runs" as the usage pattern to optimize for. But overnight runs with halt-on-failure and no skip-and-advance means a single Claude CLI timeout at 2 AM kills the entire session. Your minimum viable V2 optimizes for a mode where the most likely outcome is a partial failure with no recovery. The completion report tells you it died — it doesn't prevent the death.

Third: round-type prompt differentiation assumes you know what good critique prompts versus good proposal prompts look like. Where's the evidence? You're shipping prompt templates validated by exactly zero paired comparisons against the current undifferentiated prompts.

## Position Summary
I advocate that blind proposals need a zero-cost anchoring baseline (prompt-only mitigation tested first) before any structural implementation, because the architectural cost is only justified if prompt-level fixes demonstrably fail. I reject both proposals' implicit assumption that the three biggest failure modes are correctly identified, since neither references any systematic analysis of actual V1 session failures. The minimum viable V2 might be "instrument V1 properly" — which was already decided and then buried under feature enthusiasm.

### The Systems Pragmatist (infrastructure realist)

The Critic is right that blind proposals need a baseline test, but wrong about the conclusion. The prompt-only mitigation ("don't reference others") fails because you can't enforce it — Claude will pattern-match against conversational context whether you instruct it not to or not. The fix isn't a prompt line; it's information isolation. That said, the Critic correctly identifies that nobody has measured actual divergence in V1 output. You're all arguing about solutions to a problem sized by intuition.

Here's what actually breaks first: tiered summarization. Both proposals either include it or assume it's trivial. It's not. You're asking an LLM to compress prior rounds into summaries that preserve the specific technical nuances agents need to critique effectively. Lossy compression of argument structure is the entire problem this project exists to solve. Summarization that strips the wrong detail produces agents arguing past each other — which looks like divergence but is actually information destruction. And you have zero feedback mechanism to detect when summarization has corrupted the discussion state.

The Orchestrator's overnight completion report is the only proposal grounded in operational reality. But it's a band-aid on the actual problem: halt-on-failure with no recovery means your expected overnight output is zero for any session longer than ~4 questions, given Claude CLI's observed timeout rate. The report tells you where it died. That's a log file, not a feature.

Round-type prompt differentiation is the lowest-risk, highest-information change. Different prompts for propose/critique/evaluate are testable in isolation, require minimal structural changes, and produce artifacts you can directly compare against V1.

## Position Summary
I advocate round-type prompt differentiation as the only V2 change with a favorable cost-to-information ratio, paired with the Critic's zero-cost anchoring baseline test before committing to blind proposals. I reject tiered summarization as a minimum-viable inclusion because lossy compression of argument structure is an unsolved problem that will silently degrade discussion quality with no detection mechanism. Ship what you can measure; instrument what you can't.

## Round: EVALUATE

### The Product Oracle (user advocate)

## The Product Oracle — Evaluate

The Critic landed the hardest punch in this discussion: **nobody has systematically analyzed actual V1 session failures.** Every proposal is prescribing treatment without diagnosis. That's a product sin.

But the Critic's conclusion — "instrument V1 properly" — is also a trap. Instrumentation is work that produces data for *developers*, not better output for *users*. Brian reads the Morning Brief. If V2 doesn't change what he reads there, V2 didn't ship.

Here's how I break the tie:

**Round-type prompt differentiation wins the #1 slot unanimously.** Every agent agrees. It's cheap, measurable, and directly changes what agents produce. Ship it.

**The Pragmatist is right about blind proposals needing a zero-cost test first.** Try prompt-only anchoring mitigation — "generate your position before reading others" as an instruction, not an architectural change. If that works, you saved weeks of PromptBuilder surgery. If it fails, you've earned the architectural version. This takes a day, not a sprint.

**The overnight completion report is the #3 feature, and the Orchestrator is right that everyone else ignored it.** Blind overnight operation without a human-readable completion report means Brian wakes up, opens a folder, and has to forensically reconstruct what happened. That's not a product. The completion report is the difference between "the system ran" and "the system is usable."

Tiered summarization is not ready. The Pragmatist's critique — lossy compression with no detection mechanism — is fatal for a minimum viable release. You can't ship silent quality degradation as a feature.

The BIT system and personality transition aren't in this conversation. The decisions already say so.

**My three: round-type prompts, prompt-level anchoring test (graduating to blind proposals only if it fails), overnight completion report.**

## Position Summary
I advocate round-type prompt differentiation, a zero-cost prompt-level anchoring test before committing to architectural blind proposals, and the overnight completion report — because these are the three changes that alter what the user actually experiences. I reject tiered summarization as a minimum-viable inclusion because shipping lossy compression without a quality detection mechanism means silently degrading the Morning Brief, which is the entire product. The Pragmatist and Critic earned the agenda this round; the architects were building before diagnosing.

### The Context Surgeon (context efficiency evaluator)

## The Code Surgeon — Evaluate

The Oracle's synthesis is almost right but contains one critical flaw: **the "zero-cost anchoring test" is not zero-cost.**

"Generate your position before reading others" as a prompt instruction doesn't test anchoring mitigation — it tests whether Claude follows instructions while simultaneously receiving contradictory context. The agent still *sees* prior responses in the conversation history. You're asking the LLM to ignore what's in its context window via an instruction. That's the prompt engineering equivalent of telling someone "don't think about elephants." Every study on LLM prompt sensitivity says positional context dominates instructions.

The Pragmatist and Critic want a cheap test. Fine. But the actually cheap test is **running one session where propose-round agents literally don't receive prior responses** — which is a PromptBuilder change of maybe 30 lines. That *is* the blind proposal implementation. There's no meaningful intermediate step between "agents see everything" and "agents don't see prior proposals." The prompt-only version is theater.

**Round-type prompt differentiation: unanimous, ship it.** No argument.

**Blind proposals: skip the fake test, ship the real thing.** The PromptBuilder change is small. The Architect and Orchestrator were right about the mechanism; the Critic was right about needing justification; but the proposed "test" doesn't actually test the hypothesis.

**Overnight completion report: the Orchestrator earned this.** Nobody else even mentioned overnight usability. It's trivial to build and transforms the user experience.

Tiered summarization: the Pragmatist killed it. Agree completely.

## Position Summary
I advocate round-type prompt differentiation, actual blind proposals (not the prompt-instruction theater version), and the overnight completion report — because the "zero-cost test" doesn't test the hypothesis it claims to test, while the real PromptBuilder change is small enough to not need a preliminary gate. I reject tiered summarization as minimum-viable and reject the prompt-only anchoring test as methodologically unsound — telling an LLM to ignore context it can see is not a controlled test of whether removing that context changes behavior.


<!-- complete -->
