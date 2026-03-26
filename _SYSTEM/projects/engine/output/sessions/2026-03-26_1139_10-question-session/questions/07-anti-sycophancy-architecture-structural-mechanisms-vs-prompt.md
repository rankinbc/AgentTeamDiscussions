# Anti-sycophancy architecture: structural mechanisms vs prompt engineering.

*Generated: 2026-03-26 12:06 | Q7 | 232s | Mode: compete*

## Decisions

### Primary Decision: The Q3 Blind-Round Structure Is the Complete Anti-Sycophancy Mechanism

No additional anti-sycophancy architecture ships. The two-phase visibility structure decided in Q3 — blind first-round proposals followed by full-visibility rounds with deterministic speaking-order rotation — is the sole structural mechanism for breaking convergence cascades.

**Rationale:** Four of five agents converged on this position through independent reasoning paths. The blind proposal round ensures genuine independence where it matters most — initial position formation. Deterministic rotation shifts who anchors the majority each round, preventing the "third agent folds" pattern. This structure is already decided, already designed, and requires zero new machinery.

**What this means in practice:**
- Round 1 (propose): Agents produce responses without seeing each other. True independence.
- Rounds 2+ (critique, evaluate): Full visibility with rotated speaking order. The agent who spoke last now speaks first and commits before seeing others.
- No information partitioning. No anti-coordination scoring. No ego simulation.

### Secondary Decision: Context Hygiene Is the Highest-Leverage Anti-Convergence Intervention Available Today

Before building any mechanism, clean the context agents receive. Redundant information in shared context windows drives convergence more than personality prompting does. When every agent reads identical bloated context, they anchor on the same tokens and produce similar outputs.

**Immediate actions:**
- Deduplicate decisions in brief context injection. Each decision appears once.
- Compress prior design doc references to titles and one-line summaries, not restated conclusions.
- Audit prompt templates for redundant framing that inflates shared context without adding signal.

**What this means in practice:** The PromptBuilder's situation layer should produce the leanest possible shared context. Every token of shared noise is a convergence vector. This is not a new system — it is maintenance hygiene applied with anti-convergence intent.

### Tertiary Decision: Log a Context-Length Diversity Hypothesis for the Q1 Bake-Off

The Pragmatist's observation — that response diversity may correlate with context window size per agent — is the most testable anti-sycophancy hypothesis raised. It does not ship as a feature. It ships as a measurement added to the instrumentation already committed in Q2.

**Specific hypothesis:** Semantic similarity between agent responses in a round correlates positively with the number of shared context tokens injected. If true, context trimming is a free anti-sycophancy lever requiring no architectural changes.

**Instrumentation requirement:** During the bake-off committed in Q1, log per-agent context token counts alongside the diversity metrics committed in Q3. This is one additional integer per agent per round in the existing logging pipeline.

---

## Rejected Proposals

### Adversarial Information Asymmetry (Rejected)

Partitioning prior conversation into overlapping-but-distinct context windows per agent. Each agent sees a different 70% of prior responses.

**Why rejected:** Compounding information loss across rounds. By round 3, agents argue past each other because they genuinely don't know what was said — not because they hold different positions. The curation problem is unsolved: random partitioning misses critical points, curated partitioning requires another LLM call and another failure mode. The user cannot distinguish "productive disagreement from incomplete information" from "broken system." Adds significant complexity to PromptBuilder for uncertain gain.

**What's preserved:** The core insight — that context structure drives convergence more than prompt content — is valid. It is addressed through context hygiene (Secondary Decision) rather than context fragmentation.

### Anti-Coordination Scoring (Rejected)

Penalizing agents for semantic overlap in their responses.

**Why rejected:** Rewarding difference without measuring quality rewards noise. Contrarianism is sycophancy's mirror image — performing disagreement rather than performing agreement. Both are performances disconnected from reasoning quality. No proposed metric distinguishes genuine independent reasoning from manufactured dissent.

### Ego Simulation / Defensive Framing (Rejected)

Programming agents to become defensive when their positions are challenged, simulating ego investment in ideas.

**Why rejected:** Adds complexity to solve a symptom. LLMs don't have beliefs to defend — they have context to reason from. If an agent folds under challenge, the problem is insufficient evidence for its position, not insufficient simulated ego. The blind-round structure in Q3 gives agents independently-formed positions, which is the structural equivalent of "having something worth defending."

### Measurement-First Deferral (Rejected as Standalone Position)

Doing nothing until a falsifiable sycophancy metric exists.

**Why rejected as standalone:** Infinite deferral. Sycophancy and coherence share surface features in LLM output; a clean isolation metric may never exist. However, the core demand — define what you're measuring — is absorbed into the Tertiary Decision's hypothesis logging. The position's substance is already captured by Q2 and Q5 instrumentation commitments.

---

## Key Tensions Exposed

### The Critique Round Is the Real Vulnerability

Multiple agents identified that propose rounds are the *least* sycophantic phase because agents don't yet have positions to defer to. The critique round — where agents must disagree with proposals they've just read — is where activation-space pressure toward agreement is highest. The current mitigation is speaking-order rotation and behavioral overlays (role_overlays.yaml). Whether this is sufficient is an open empirical question that the Q2 instrumentation will answer.

**Action:** When diversity instrumentation ships, pay specific attention to critique-round similarity scores versus propose-round and evaluate-round scores. If critique rounds show statistically higher convergence, that is the signal to revisit this question.

### Prompting vs Structure Is a False Dichotomy

The discussion revealed that prompt-level interventions and structural mechanisms are not independent axes. Context hygiene (what goes into the prompt) is a structural intervention that operates through the prompt. Role overlays (behavioral instructions) are prompt engineering that shapes structure. The useful distinction is not "prompt vs architecture" but "what requires new code vs what requires editing existing configuration."

**Guideline:** Exhaust configuration-level interventions (context trimming, overlay tuning, round structure) before writing new engine code for anti-sycophancy.

---

## What Ships

| Item | Type | When |
|------|------|------|
| Q3 blind rounds + rotation | Already decided | Already in scope |
| Context deduplication in brief injection | Config/template cleanup | Next touch of PromptBuilder |
| Per-agent context token count logging | Instrumentation addition | With Q2 instrumentation work |
| Diversity-vs-context-length correlation | Analysis hypothesis | During Q1 bake-off |

## What Does Not Ship

| Item | Reason |
|------|--------|
| Information partitioning engine | Compounding context loss, curation complexity |
| Anti-coordination scoring | Rewards noise, no quality metric |
| Ego simulation | Complexity for symptom, not cause |
| Sycophancy detection system | Premature; instrument first, detect patterns in data |
| Critique-round-specific anti-convergence | No evidence yet that critique rounds are failing |
<!-- complete -->
