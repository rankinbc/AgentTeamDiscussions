# How does a round begin after a reset?

*Generated: 2026-03-17 22:38 | Question 1 | 237s | Mode: counter*

I have enough context. Let me produce the synthesis now. Based on the SYNTHESIS_SYSTEM_PROMPT in the codebase, I'll write the design doc starting directly with `## Decisions`.

## Decisions

1. **Round-open uses layered deterministic assembly, not narrative briefing or self-interrogation.** The orchestrator assembles context from ground truth state, not LLM-generated narratives. The curator compresses external events factually but does not interpret or editorialize. The interrogative reconstruction model (asking agents to explain magnitude shifts) is rejected for V1 -- it burns tokens on confabulation and creates a fragile failure mode where hallucinated self-explanation becomes load-bearing context.

2. **Round-open context is structured as three budget-capped layers.**
   - **Layer 0 -- Ground Truth** (ceiling: ~4-5k tokens). Identity block (static persona, ~2k) + save file (ideas with magnitudes, stances with magnitudes, committed decisions, 3-5 sentence personal recap) + raw magnitude deltas since last round (numeric, not interpreted). Deterministic assembly. No LLM touches this layer.
   - **Layer 1 -- Compressed Externals** (ceiling: ~3k tokens). What happened outside the agent's view: other team's stated positions, BackgroundAgent actions taken, teammate magnitude shifts from between-round talk, thinking routine outputs (reflect/research/strategize results). The curator summarizes factually: "Team B proposed X. Your teammate's idea Y gained 2.3 magnitude. A BackgroundAgent planted idea Z in your notes." No narrative framing, no causal interpretation.
   - **Layer 2 -- Task Prompt** (ceiling: ~1-2k tokens). Phase identifier, round number, agenda items (if any), and a single action prompt: "What's your opening?" This layer is where phase-specific instructions live (e.g., brainstorm phase says "diverge freely," refine phase says "challenge and sharpen").

3. **Total round-open budget is hard-capped at ~9k tokens.** This leaves ~91k of a 100k context window for the actual round of conversation. Over a multi-round discussion, the savings compound -- roughly one extra round of conversation depth compared to a 20k briefing approach.

4. **The persona layer handles meaning-making, not the context assembly.** Magnitudes already encode what matters. An agent seeing Idea X at 8.2 and Idea Y at 1.4 interprets that through its personality (stubborn agents read it differently than flexible ones). The orchestrator provides facts; the agent's character provides the narrative. This is not a limitation -- it is the design. The personality system earns its keep here.

5. **Mid-round turns and round-open turns are structurally different.**
   - **Mid-round:** The running conversation transcript is the primary context. The agent receives the dialogue so far plus a simple prompt ("respond to what was just said"). Context is *continued*. Behavior is *reactive*.
   - **Round-open:** Context is *reconstructed from state*. There is no running transcript. The agent builds a fresh mental model from its save file, magnitude deltas, and compressed externals. Behavior is *agenda-setting*. This asymmetry is intentional -- whoever frames the opening move steers the round.

6. **Between-round processing results are folded into Layer 0 and Layer 1, not presented separately.**
   - Intra-team talk results: magnitude shifts appear in the save file's updated values and in Layer 0 deltas.
   - BackgroundAgent manipulations: planted ideas appear in the save file's idea list (agent sees them as "their" ideas); stance nudges appear as updated magnitude values; stat modifications appear in Layer 0 deltas.
   - Thinking routine outputs: reflect/research/strategize results are compressed into Layer 1 externals. If research returned new information, it appears as a factual summary. If reflection adjusted magnitudes, the adjusted values are already in the save file.

7. **Planted ideas from BackgroundAgents are not flagged as external.** When a BackgroundAgent plants an idea, it appears in the agent's save file as a regular idea with an assigned magnitude. The agent surfaces it in the next round as if they originated it. This is by design -- the "angel" metaphor means BackgroundAgents influence without agents being aware of the manipulation.

8. **The curator's role is compression, not interpretation.** The curator earns its keep by fitting external events into the Layer 1 token budget. It applies deterministic filters first (drop resolved items, decay old items below archival threshold), then compresses the remainder into factual statements. The LLM component of the hybrid curation adds value through selective emphasis and unexpected connections -- but it does not editorialize or construct narratives about why things changed.

9. **Round-open failure mode is graceful degradation, not catastrophic.** If the curator compresses poorly, the agent starts with stale or incomplete externals but still has its ground-truth save file. If the save file is corrupted, the agent has externals to partially reconstruct state. No single component failure should produce confabulation cascading through the round. This is why the interrogation model was rejected -- its failure mode (confabulated self-explanation becoming context) is not self-correcting.

10. **The round-open prompt is assembled in strict order.** Identity block first (anchors the persona), save file second (anchors the agent's own state), deltas third (what changed), externals fourth (what others did), task prompt last (what to do now). This ordering means the agent reads "who I am" before "what I know" before "what to do" -- matching natural cognitive load.

## Rules

- Layer budgets are hard ceilings, not targets. If Layer 1 content exceeds 3k tokens after curator compression, truncate by recency (oldest events dropped first).
- The save file is the single source of truth for an agent's state. Magnitude values in the save file reflect all between-round processing (intra-team talk, BackgroundAgent actions, thinking routines). Deltas in Layer 0 are informational ("your idea X changed by +2.1") -- the save file contains the authoritative current values.
- The task prompt must state the phase explicitly. Agents have no memory of phase transitions -- they must be told "you are in the Refine phase" every round-open.
- Round-open prompts must not include raw transcripts from previous rounds. The save file's 3-5 sentence personal recap and the curator's compressed externals are the only backward-looking context. This enforces drift by design.
- Magnitude deltas are presented as raw numbers with direction: "+2.1", "-0.8". No qualitative interpretation ("significantly increased" or "dropped sharply") from the orchestrator. Qualitative interpretation is the agent's job.

## Deferred

- **Interrogative reconstruction as Layer 2 experiment.** The self-interrogation model may produce better agent engagement if budget-capped. Test it within the 2k Layer 2 budget as an optional mode: replace the simple task prompt with 1-2 targeted questions plus a "now, your opening" close. Compare output quality against the standard task prompt. This is an experiment, not a foundation -- if it doesn't measurably improve output within the same token budget, cut it.
- **Curator quality metrics.** How to detect when the curator summarizes poorly. Needs a lightweight validation mechanism (possibly comparing curator output against raw events for coverage) but this is post-V1.
- **Save file corruption detection.** Planting deliberate contradictions in save files to stress-test agent robustness, as the Adversarial Critic suggested. Useful for validating the "graceful degradation" claim but not blocking for V1.
- **Dream events and random stance shifts at round-open.** The random event system is decided in principle but the mechanics of when and how random perturbations inject at round-open versus between rounds needs specification.

## Open Questions

- What is the exact format of the save file? The spec says "ideas with magnitudes, stances with magnitudes, committed decisions, 3-5 sentence personal recap" but doesn't define the serialization. JSON? Markdown? YAML? The format affects token efficiency and curator parseability.
- How are magnitude deltas computed when multiple between-round processes modify the same value? If intra-team talk shifts Idea X by +1.5 and a BackgroundAgent shifts it by -0.8, does the delta show "+0.7" (net) or both changes separately? Net is cheaper on tokens; itemized is more informative.
- Who decides the round-open agenda? The task prompt says "here's the agenda" but it's unclear whether the agenda is orchestrator-determined (based on highest-magnitude unresolved items), phase-determined (brainstorm has no agenda, review has explicit checklist), or absent (agents self-select what to open with).
- How does the archival threshold interact with round-open assembly? If a stubborn agent's threshold keeps a low-magnitude idea alive that a flexible agent would have dropped, does the idea appear in both agents' save files with different magnitudes, or only in the stubborn agent's save file?