# What is the current agent system capable of?

*Generated: 2026-03-26 11:26 | Q2 | 202s | Mode: compete*

## Decisions

### D1: Speaking order rotation is a V1 fix

Rotate agent speaking order across rounds within each question. Round 1 order A-B-C-D-E becomes Round 2 order C-D-E-A-B (or randomized). The current sequential execution in RoundRunner creates systematic anchoring bias where later speakers in every round absorb earlier speakers' framing. This is a mechanical asymmetry that costs minimal code and has outsized impact on output diversity. Implement before any layer model changes.

### D2: The six-layer agent model is an authoring model, not a runtime model

The six layers (personality, position, technique, anti-slop, voice, output format) compress to three runtime layers in PromptBuilder (identity, situation, task). This is not a defect. The six-layer structure serves YAML authors organizing agent definitions. The three-layer structure is what reaches the LLM. Treat them as separate concerns: author-facing schema vs runtime prompt architecture. Do not conflate "layers in YAML" with "independent levers on output."

### D3: Context accumulation dominates agent identity by Round 2

Agent identity layers occupy roughly 800 tokens. By Round 2, accumulated transcript occupies 4,000-10,000 tokens. Agent identity signal drops to 7-15% of the prompt and continues shrinking. This means no prompt-layer redesign (personality-based or cognitive-strategy-based) will meaningfully improve differentiation unless transcript management is addressed first. The differentiation problem is a context budget problem.

### D4: Audit transcript content before redesigning agent layers

Before any changes to the agent model (personality dimensions, cognitive strategies, or new layers), audit what actually fills agent prompts at each round. Measure: transcript token count per round, compression or truncation method applied, ratio of identity tokens to context tokens, and whether agents produce distinguishably different outputs in Round 1 vs Round 3. Without this data, layer redesign optimizes the wrong variable.

### D5: Add per-agent contribution visibility to session output

The Morning Brief compresses all agent contributions into consensus, making it impossible to assess whether agent differentiation is working. Add a contribution attribution section to session output that surfaces what each agent uniquely contributed. This serves two purposes: it gives the user a reason to trust multi-agent sessions over single-agent queries, and it provides the diagnostic data needed to evaluate whether layer changes improve output quality.

### D6: Defer personality-to-cognitive-strategy migration

The proposal to replace personality dimensions with cognitive strategy dimensions (inversion thinking, constraint-first reasoning, analogical reasoning) is directionally sound but premature. Two blockers: (1) no evidence that personality-based differentiation has failed, only suspicion; (2) Scriban templates support additive composition only, and cognitive strategies interact multiplicatively. A prompt compiler would be needed to express strategy combinations cleanly, which is a V2 concern. Revisit after D4 audit data exists.

### D7: Anti-slop layer has marginal effect and should not expand

Instructions like "don't use buzzwords" fight base model tendencies with minimal token budget. The anti-slop layer is unlikely to produce measurable output improvement. Do not invest in expanding it. If slop reduction matters, address it in synthesis post-processing rather than per-agent prompt engineering.

---

## Design Rules

### Agent Prompt Budget

- Agent identity layers (personality + position + technique + voice) must remain under 1,000 tokens total.
- If identity layers exceed 15% of the total prompt at any round, the system is misconfigured. Treat this as a warning threshold.
- Transcript content included in subsequent rounds is the primary context consumer. Any truncation or summarization strategy applied to transcripts has more impact on output quality than any agent layer change.

### Round Execution

- Speaking order must rotate or randomize across rounds within a single question. No agent should occupy the same position in consecutive rounds.
- The first speaker in any round has no prior-round context from that round's peers. The last speaker sees all peers' responses. This asymmetry is inherent to sequential execution and must be offset by rotation, not eliminated.

### Layer Model Boundaries

- YAML authors use six layers to organize agent definitions. This is a schema concern.
- PromptBuilder compresses to three runtime layers. This is a prompt engineering concern.
- Changes to the authoring schema do not require changes to the runtime architecture, and vice versa.
- Mode overlays modify the task layer per-round. They are functional when they restructure what the agent is asked to do (e.g., "argue against the strongest prior proposal"). They are cosmetic when they add adjectives (e.g., "be more competitive").

### Output Visibility

- Session output must include per-agent contribution markers that survive into user-facing artifacts (Morning Brief or summary).
- The user must be able to answer: "What did agent X uniquely contribute that no other agent said?" If this question is unanswerable from the output, the multi-agent system is not demonstrating its value.

### Measurement Before Redesign

- No changes to the agent layer model without before/after comparison data from at least one full session.
- The null baseline is a single Claude call with the same question and context but no agent persona. If multi-agent output is not measurably better than this baseline, the layer model is not the problem to solve.

---

## Gaps Identified

| Gap | Severity | Resolution Path |
|-----|----------|----------------|
| No transcript size audit exists | High | Instrument PromptBuilder to log token counts per layer per round |
| No null-baseline comparison (single Claude vs multi-agent) | High | Run parallel sessions and compare output quality |
| Speaking order is static across rounds | Medium | Rotate in RoundRunner before next session run |
| Morning Brief erases agent attribution | Medium | Add contribution tagging to synthesis prompts |
| No per-round differentiation metric | Medium | Define and measure after transcript audit |
| Scriban cannot compose cognitive strategies multiplicatively | Low | Architectural constraint; revisit if cognitive strategy migration proceeds |
| Anti-slop layer effectiveness is unmeasured | Low | Deprioritize; do not expand |
<!-- complete -->
