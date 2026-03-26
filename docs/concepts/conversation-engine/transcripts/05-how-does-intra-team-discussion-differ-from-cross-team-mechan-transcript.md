# Transcript: How does intra-team discussion differ from cross-team mechanically?

*Generated: 2026-03-17 21:46*

## Round: PROPOSE

### The Cognitive Architect (creativity engine designer)

---

Different animal entirely. Here's the mechanical split:

**Cross-team** is the main event. Formal turns, committed to transcript, mediated through MCP channels. Agents speak *as their team's voice* to the other team. Full context assembly pipeline. Every utterance is permanent record.

**Intra-team** is the huddle between rounds. Step 3 of the 7-step pipeline, after BackgroundAgents mutate state but before thinking routines fire. Mechanically:

- **No transcript.** Intra-team talk doesn't append to the session transcript. It's a processing step, not a speech act. The *effects* persist (magnitude changes), the conversation doesn't.
- **Simplified context.** Agents see: their own save file, teammates' save files (ideas + stances + magnitudes only), and a short "what just happened" summary. No curator call -- too expensive for what's essentially a magnitude-adjustment pass.
- **Direct magnitude writes.** When Agent A pitches an idea and teammate B finds it compelling, B's copy of that idea gets a magnitude bump. Bad pitch? Magnitude drop. This is the entire feedback mechanism -- no decisions, no artifacts, no formal structure.
- **Prompt format is different.** Cross-team Task: "Respond to Team X's position on Y." Intra-team Task: "Your teammates hold these positions. What resonates? What's wrong? Adjust your priorities."

**Feed-forward path:** Updated magnitudes flow into Step 4 (thinking routines), which means agents reflect and strategize on *post-huddle* priorities, not pre-huddle ones. The huddle reshapes what they care about before they decide what to say.

One LLM call per agent. Cheap pass, high leverage.

### The Flow Orchestrator (mechanical flow designer)

Two distinct flows. Let me trace them.

**Cross-team discussion** is the main round loop. Full context assembly pipeline. Agents speak into `roundTranscript[]`, which is append-only mid-round. Each turn gets the curated Situation block built from Discussion state. This is the expensive path -- full identity, situation, task prompt per turn.

**Intra-team talk** runs in the between-round pipeline, step 3 of 7 (after Save, after BackgroundAgents, before ThinkingRoutines). Mechanically different in three ways:

1. **Scope.** Cross-team sees the curated Discussion state. Intra-team sees only teammates' save files -- their ideas, stances, magnitudes. No opponent state. No transcript. Much smaller context window.

2. **Output.** Cross-team appends to `roundTranscript[]` and indirectly shifts magnitudes through what gets said. Intra-team writes directly to magnitude values. Teammate endorses your idea? Magnitude goes up. Teammate challenges it? Magnitude goes down. No transcript produced -- just state mutations.

3. **Budget.** Cross-team burns turns against the phase cap. Intra-team gets a fixed, small token budget (open item -- exact number unset). It's a single LLM call per agent, not a multi-turn conversation. "Here are your teammates' positions. What shifts for you?"

**Feedback path:** Intra-team magnitude changes flow into the deterministic filter (step 5), which flows into curator emphasis (step 6), which shapes the Situation block for round-open. An idea boosted by teammates ranks higher. An idea no teammate endorsed drops toward archival threshold.

The critical ordering: BackgroundAgents mutate first, then intra-team reacts to the already-mutated state. This is deliberate -- angels act, then teammates process the new reality.

## Round: CRITIQUE

### The Systems Pragmatist (infrastructure realist)

Two proposals saying the same thing. Let me stress-test what they're glossing over.

**What's actually different mechanically:**

- **Context assembly:** Cross-team runs the full 6-step pipeline (filter, curate, assemble). Intra-team skips all of it. You hand each agent their save file plus teammates' save files. No curator call. This is the right call -- but it means intra-team has zero protection against context bloat if team size grows. Six agents times save files is fine. Twelve agents and you're burning context on teammate state alone.

- **Output contract:** Cross-team produces natural language appended to transcript. Intra-team produces structured magnitude deltas. This needs a schema. "Magnitude goes up" is hand-waving. The LLM response needs to return something parseable -- idea ID, direction, amount -- or you're doing another LLM call to interpret freeform text. Nobody's specified this format.

- **Failure mode nobody mentioned:** What happens when Agent A bumps an idea's magnitude during intra-team, then their thinking routine (step 4) drops it back down? You've got two consecutive steps fighting over the same values with no conflict resolution. The ordering says "intra-team feeds thinking routines," but thinking routines don't know *why* a magnitude changed. Teammate endorsement and random drift look identical in the save file.

**Feed-forward is clean in theory, fragile in practice.** The magnitude changes propagate through filter and curator into the next round's Situation block. But without provenance on magnitude changes, debugging "why did the system fixate on this idea" becomes archaeology.

Specify the output schema. Tag magnitude sources. Or accept you can't diagnose bad sessions.

### The Adversarial Critic (adversarial reviewer)

Two proposals saying the same thing in different words. Let me poke the gaps they're both glossing over.

**What's actually settled:** One LLM call per agent, no transcript, direct magnitude writes, simplified context (teammate save files only), runs at step 3 before thinking routines. Fine. I don't dispute the shape.

**What's not settled and nobody's admitting it:**

**Magnitude write rules are undefined.** "Teammate finds it compelling, magnitude goes up." By how much? Who resolves conflicts? If Agent A boosts Idea X by +0.3 and Agent B drops it by -0.2, is that additive? Averaged? Last-write-wins? This isn't a detail -- it's the entire mechanism. Without defined write semantics, you have a race condition masquerading as a feature.

**"No transcript" creates a debugging black hole.** Both proposals hand-wave this. If intra-team talk produces only magnitude deltas with no record of *why*, you cannot diagnose bad sessions. An idea's magnitude spikes between rounds and you have zero audit trail. At minimum you need structured logs: agent, idea ID, delta, one-sentence rationale. Not a transcript -- a ledger.

**The "simplified context" assumption is untested.** Teammate save files include ideas, stances, magnitudes. For a 6-agent team that's 5 save files. How big? If each is 500 tokens, that's 2500 tokens of teammate state plus the agent's own. Manageable. But nobody's confirmed save file size budgets yet.

The mechanism is right. The specification is incomplete. Don't ship it without write semantics and audit logging.

## Round: EVALUATE

### The Product Oracle (user advocate)

The panel's converging on the mechanism. Let me reframe it through the lens of what the *user* of this system actually needs.

**The job-to-be-done split is clean.** Cross-team talk is *performance* -- agents advocating positions for the record. Intra-team talk is *sensemaking* -- agents privately calibrating what matters before they go back on stage. Different jobs, different mechanics. That's correct.

**What I'd add:** The Pragmatist and Critic are right that magnitude write semantics and audit logging aren't optional. But frame it as a product question: *can an operator understand why a session produced what it produced?* Without a structured ledger (agent, idea, delta, one-line reason), the answer is no. That's not a debugging luxury -- it's the difference between a tool you trust and a black box you abandon after three confusing runs.

**The feed-forward path is the real product magic.** Teammates validate or challenge your ideas *before* you reflect and strategize. That means agents walk into the next round with socially-tested priorities, not just individual hunches. This is what makes multi-agent better than single-agent -- the huddle creates emergent consensus without anyone explicitly negotiating.

**One concern nobody raised:** intra-team talk with no transcript means operators can't learn what makes good teams good. V1 is fine with just the ledger. But flag this -- structured intra-team logs become the training data for understanding which team compositions produce better outcomes.

The mechanism works. Specify the write semantics, add the ledger, ship it.

### The Context Surgeon (context efficiency evaluator)

The mechanism is converged. I'm here for the context budget implications.

**Cross-team context cost per turn:** ~25-30k tokens (2k identity + 8-15k curated situation + 1-2k task + response). Full pipeline. Expensive by design.

**Intra-team context cost per call:** ~4-6k tokens (agent's own save file ~500t + 5 teammate save files ~2500t + task prompt ~500t + response). No curator call. No identity block beyond what's in the save file. This is 80% cheaper per agent-call than a cross-team turn.

That's the real difference. Not the philosophical distinction between "speech act" and "processing step" -- the token economics.

**My concern is the Pragmatist's output schema point.** If intra-team returns freeform text that needs parsing, you either constrain the response format (structured JSON -- magnitude deltas with rationale) or you burn a second LLM call interpreting it. The second call doubles intra-team cost and kills its budget advantage. Structured output is non-negotiable.

**The Critic's audit ledger solves two problems at once.** Structured response format (agent, idea\_id, delta, one-line rationale) gives you both parseable output AND the debugging trail. One schema, two wins. Tiny token footprint for logging.

**Feed-forward is context-efficient by accident.** Magnitude changes propagate through the deterministic filter before the curator ever runs. Changed magnitudes shift ranking, ranking shifts curator emphasis, curator shifts situation block. No extra LLM calls to "process" intra-team results. The existing pipeline absorbs them for free.

Tag magnitude sources. The Pragmatist is right -- without provenance, you're burning future debugging tokens reconstructing what happened.
