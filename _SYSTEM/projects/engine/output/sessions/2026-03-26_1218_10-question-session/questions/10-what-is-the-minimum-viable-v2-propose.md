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


<!-- complete -->
