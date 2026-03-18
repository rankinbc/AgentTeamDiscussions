# Transcript: How should the orchestrator handle a question that produces contradictory proposals?

*Generated: 2026-03-18 13:02*

## Round: PROPOSE

### The Cognitive Architect (creativity engine designer)

The research on productive conflict in creative teams is unambiguous: premature resolution kills the best ideas. Charlan Nemeth's work on minority dissent shows that contradictory positions generate more novel solutions than either position alone -- but only if you force the system to sit with the tension long enough.

**The rule: Never merge. Never pick a winner at synthesis time.**

Synthesis should produce a **Tension Report** -- a structured artifact that names the contradiction explicitly, identifies what each proposal optimizes for (they're always optimizing for different things), and surfaces the assumption that makes them incompatible. That assumption is almost always the most interesting thing the discussion has produced.

Here's why merging is poison: when you merge contradictory proposals, you get the median of two extremes. You lose the sharp edges that made each proposal valuable. The research on "creative abrasion" from Harvard's Linda Hill confirms this -- the output of genuine disagreement should be a *new* option neither side proposed, not a diluted compromise.

The Tension Report feeds into the next round as a first-class input. The evaluator's job becomes: "Given this contradiction, what third option resolves it without losing what each side was protecting?" If no third option emerges, the contradiction escalates to the Morning Brief as a "needs tiebreaker" item -- because some contradictions genuinely require the human to choose a value tradeoff.

**The testable claim:** systems that preserve contradictions through synthesis produce more novel final artifacts than systems that force resolution. We can measure this by comparing novelty scores of outputs under both rules.

Forced harmony is where creativity goes to die.

### The Flow Orchestrator (mechanical flow designer)

The synthesis step presents both with a scored recommendation. Here's the sequence.

**Trigger:** Synthesizer receives two or more proposals from the evaluate round that score as incompatible -- meaning they contradict on at least one structural decision (data model, flow direction, responsibility assignment).

**Step 1: Detect contradiction.** The synthesizer compares proposals on named decision points. If proposal A says "orchestrator owns phase transitions" and proposal B says "MCP server owns phase transitions," that's a structural conflict. Tag it.

**Step 2: Score each side.** For each tagged conflict, the synthesizer evaluates both positions against three criteria only: (a) does it survive the 8-hour overnight constraint, (b) does it reduce moving parts, (c) does it stay observable/tunable via YAML. Each criterion is pass/fail. No weighted scoring -- too much design surface for V1.

**Step 3: Emit a recommendation block.** The output is not a merged design. It's the full text of both proposals, the tagged conflicts, the scores, and a one-line recommendation per conflict. "Proposal A wins on conflict #1 because it passes all three; Proposal B fails overnight survival."

**Step 4: Flag unresolvable conflicts for the Morning Brief.** If both proposals pass all three criteria on a given conflict, the synthesizer does NOT pick a winner. It escalates to the "needs tiebreaker" tier. The human decides.

**What I'm cutting:** Any attempt to merge contradictory proposals into a hybrid. Merging incompatible designs produces incoherent designs. The synthesizer's job is to clarify the fork, not hide it.

The decision point data needed: the named structural decisions each proposal makes. Without that, contradiction detection is impossible.

## Round: CRITIQUE

### The Systems Pragmatist (infrastructure realist)

The proposal is mostly sound. Here's what breaks.

**1. "Contradiction detection" assumes structured output from LLMs.** The synthesizer needs to compare "named decision points" across proposals. In practice this means the propose step must emit decisions in a parseable format -- not prose. If proposal A buries its phase transition opinion in paragraph three and proposal B states it as a bullet point, your contradiction detector is blind. The failure mode: silent conflicts that sail through as false agreement. This is the highest-risk piece and nobody's accounting for it.

**2. The three-criteria scoring is good precisely because it's simple.** Pass/fail on overnight survival, moving parts, observability. No weights. I'd fight anyone who tries to add nuance here. At 3 AM, the synthesizer needs to produce a clear signal, not a spreadsheet.

**3. "No merging" is the correct call.** Merged designs from LLMs are where incoherence hides. Two clean proposals with a tagged fork is debuggable. A hybrid is not.

**4. The escalation path has a gap.** If both proposals pass all three criteria, it escalates. Fine. But what happens to the *rest of the discussion* while that conflict is unresolved? Does the next round proceed with proposal A assumed? Proposal B? Both forks? If you don't define what the system does with an unresolved conflict *right now*, you'll get inconsistent downstream artifacts that reference both sides.

**The constraint nobody is accounting for:** contradiction detection quality is gated entirely on how structured the propose step's output is. Nail the output format first, or the synthesizer is theater.

### The Adversarial Critic (adversarial reviewer)

Five problems with this synthesis proposal.

**1. "Named decision points" don't exist yet.** The entire contradiction detection mechanism assumes proposals arrive with tagged structural decisions. Nobody has defined what a "named decision point" is, how proposers are forced to emit them, or what happens when they use different vocabulary for the same concept. This is the load-bearing wall and it's made of wishes.

**2. Pass/fail on three criteria is a coin flip disguised as rigor.** "Reduces moving parts" -- compared to what baseline? "Stays observable via YAML" -- every design claims this. "Survives 8 hours" -- how does the synthesizer evaluate this without running it? These criteria sound concrete but are entirely subjective when applied by an LLM to prose descriptions.

**3. The synthesizer is doing work that requires the full context of both proposals.** This is a stateless CLI call. Who reconstructs both proposals into the synthesizer's prompt? How big is that prompt? Two detailed architectural proposals plus scoring criteria plus conflict detection instructions will blow past reasonable prompt sizes fast.

**4. "Unresolvable" escalation has no cap.** If every conflict passes all three criteria on both sides -- which is likely since good proposals tend to be defensible -- the Morning Brief becomes a wall of tiebreakers. The human wakes up to homework, not decisions.

**5. Cutting merges is fine. But "present both" still requires someone to act.** If the system can't resolve conflicts and the human doesn't respond for days, what state is the session in? Frozen? This is a deferred decision about deferred decisions.

The contradiction detection mechanism is the weakest link. Without structured decision-point extraction baked into the propose step, everything downstream is theater.

## Round: EVALUATE

### The Product Oracle (user advocate)

The moment that matters is what the user sees in the Morning Brief at 7 AM. Not what the synthesizer does internally.

**Verdict: Present the fork, not the merge. But cap the homework.**

The "never merge" principle is right -- merged LLM output is where sharp ideas go soft. The scored recommendation approach is also right directionally. But both proposals miss the user's actual job.

The user's job isn't "resolve architectural contradictions." It's "decide what to build." Every tiebreaker that hits the Morning Brief costs attention. If the system escalates 8 conflicts, the user deletes the email.

**The rule I'd enforce:** Maximum 2 tiebreakers per session reach the Morning Brief. The synthesizer must rank conflicts by impact and auto-resolve the rest using the simplest heuristic available -- fewer moving parts wins. The user can override later, but the default is a usable output, not a perfect one.

**On contradiction detection:** The critics are right that this is theater without structured output from proposers. But forcing rigid decision-point schemas on the propose step kills the divergent thinking you want in brainstorm phase. The pragmatic move: let proposers write naturally, then have the synthesizer *extract* decision points as a separate step. It won't catch everything. That's fine for V1.

**On unresolved conflicts blocking progress:** The system should pick a provisional winner and flag it. "We went with A. You might prefer B. Here's why they differ." The user gets a complete draft, not a frozen session.

Would the user tune conflict thresholds? No. Ship sensible defaults.

### The Context Surgeon (context efficiency evaluator)

The Critic's point #3 is the one that matters most from my seat.

Two full proposals reconstructed into a single synthesizer prompt is already expensive. Add conflict detection instructions, scoring rubrics, and the original question context -- you're looking at 4-6K tokens minimum before the synthesizer even starts reasoning. For a stateless CLI call that has to rebuild everything from files, this is the most context-hungry step in the entire pipeline.

**The cheapest correct answer: don't synthesize at all in V1.**

Present both proposals to the Morning Brief with a structured diff. Not a merge, not a winner -- a diff. Here's what they agree on (small), here's where they diverge (specific), here's what the human needs to decide (pointed).

Why this survives the context budget:

- No synthesizer call. You save an entire CLI invocation and its prompt reconstruction cost.
- The diff can be generated mechanically from the structured output of each proposal -- no LLM reasoning required if proposals use consistent section headers.
- The Morning Brief already has a "needs tiebreaker" tier. Contradictions route there naturally.

The Critic is right that "named decision points" are undefined. But the fix isn't defining them -- it's not depending on them. If proposals follow a template with fixed sections (scope, constraints, tradeoffs), you can diff at the section level without semantic extraction.

The synthesizer is a V2 problem. It requires structured decision-point tagging that doesn't exist yet, and building that tagging system to support one synthesis step is the definition of premature complexity.

Spend the tokens on better proposals, not on reconciling bad ones.
