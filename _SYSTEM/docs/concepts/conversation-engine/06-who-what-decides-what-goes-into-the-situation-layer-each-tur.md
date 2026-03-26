# Who/what decides what goes into the Situation layer each turn?

*Generated: 2026-03-17 21:49 | Question 6 | 188s*

The spec is ready to write. Here's what I synthesized from all six panel voices:

---

**Spec: Situation Layer Pipeline** -- reconciled into one authoritative design document.

**The pipeline (full consensus, no dissent on structure):**

Three stages, one LLM call per agent per round.

1. **Deterministic Filter (zero LLM cost)** -- pulls from four sources: agent's save file, teammate save files (ideas+magnitudes only), Discussion state (magnitude-ranked activeIdeas, stances, decisions, phase), and magnitude delta flags. Cuts ideas below persona-dependent archival threshold, stances on dead ideas, decisions older than 2 rounds unless referenced by active ideas. Output: ~12-18k tokens of candidate material, 40-60% smaller than raw state. Key nuance: two agents on the same team get different filtered sets because thresholds are persona-dependent. Same discussion, different realities, before the LLM touches it.

2. **Single LLM Curator Call** -- compresses filtered set into narrative Situation block (8-15k tokens). Clusters stances into tension pairs, weights by magnitude, surfaces delta flags, applies phase-appropriate framing (brainstorm = breadth, specify = convergence). Can inject valuable randomness by noticing connections nobody made explicit. **Hard constraint added (Pragmatist's demand):** curator must not invent connections absent from the filtered set. Creative interpretation yes, fabrication no.

3. **Assembly** -- Identity (~2k static) + Situation (curator output) + Task (~1-2k phase prompt). Agent sees only this. ~80k+ remaining for thinking and response.

**The agent never sees:** raw magnitudes, other agents' save files, BackgroundAgent actions, audit ledger, transcript, curator reasoning, magnitude source tags.

**Key governance decisions locked down:**

- **Curator prompt versioning required** (Critic's demand) -- it's the god prompt hiding behind a utility function label. Three words changed = every agent's reality changes.
- **Drop logging required** (Oracle's addition) -- log what the curator dropped, not just what it produced. The story the curator didn't tell is where bugs live.
- **Full observability chain required** (Critic + Pragmatist) -- log magnitude-ranked list, filtered set, curator output, Task prompt, and what the agent actually discussed. Only way to diff recommendations vs. behavior.

**Compression ratio variance acknowledged** (Surgeon's flag) -- early rounds get nearly lossless context, late rounds get lossy summaries. Curator behavior is not constant across rounds. No V1 mitigation beyond the deterministic filter; V2 candidates include candidate set caps or progressive summarization.

**Nine open items tracked:** archival threshold values, delta flag threshold (three specs and counting), decision retention window, curator token budget enforcement, curator prompt versioning scheme, drop logging format, late-round fidelity degradation, curator emphasis measurement, and consensus detection.

---

Shall I save the file? It's targeted at `output/spec_situation_layer_pipeline.md`.