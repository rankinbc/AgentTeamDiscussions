# What should V2 absolutely NOT try to change about V1?

*Generated: 2026-03-26 11:37 | Q5 | 205s | Mode: compete*

## Decisions

### D1: Freeze the Claude CLI subprocess boundary

The subprocess execution model is the single mechanism whose failure is unrecoverable. Every other component can be patched, migrated, or rewritten without user-visible impact. If the CLI integration breaks, nothing works. V2 must not replace, abstract over, or restructure how the engine invokes Claude CLI subprocesses.

**Confidence:** Unanimous. All five agents converged on this as load-bearing, and no agent challenged it.

### D2: Freeze the session output file structure

Users have existing sessions. The eval command, the UI, and human readers all depend on predictable output paths and file naming. Changing the output shape breaks accessibility of every prior session for zero user-facing benefit. The completion marker pattern, file naming conventions, and directory layout must remain stable.

**Confidence:** High. The Oracle and Pragmatist identified this as the second user-facing freeze. No agent argued for changing it.

### D3: Freeze the context budget priority order until measured

The prompt assembly pipeline is the token budget allocator. Round transcripts, prior decisions, agent identity layers, and round instructions compete for the same finite context window. The priority order — which categories of information survive truncation — is the invisible load-bearing wall. Changing it without measurement guarantees optimizing noise, because context homogenization (Q4-D4, flagged as unproven) may already be occurring silently.

This freeze is conditional: it holds until context utilization per agent call is measured. That measurement must come first, because if agents are hitting truncation limits, every other measurement captures truncated behavior, not agent behavior.

**Confidence:** Moderate-high. The Surgeon identified this as the mechanism the Architect was reaching for but misdiagnosed. The Architect's prompt-assembly freeze targeted the wrong layer (template syntax rather than priority order). The Critic correctly noted that freezing prompt assembly without measurement locks in unknown quality — the budget priority freeze is narrower and resolves that objection.

### D4: Do not freeze round execution sequence

The propose-critique-evaluate ordering is a mode-level concern, not an architectural wall. Mode definitions in team YAML already treat round structure as variable. Q2-D3 established that context accumulation dominates agent identity by Round 2, meaning the round labels may not be producing distinct cognitive phases. Protecting this sequence from experimentation would preserve a naming convention, not a mechanism.

V2 should experiment with round structure — different orderings, different group compositions — within the existing mode system.

**Confidence:** Moderate. The Orchestrator argued strongly for freezing; the Architect, Critic, and Oracle all rejected it. The existing mode system already treats rounds as configurable.

### D5: Do not freeze the manifest format or persistence mechanics with blanket protections

Session.json as single source of truth is good design, but granting it a blanket freeze is premature. The Orchestrator's "no new state stores" rule directly contradicts Q4-D1 (measure three constraints before designing V2), because measurement requires somewhere to write telemetry. Measurement infrastructure must be permitted.

The manifest format and persistence layer are candidates for instrumented experimentation, not preemptive protection. Their failure modes are recoverable — a persistence bug loses one session; a manifest bug breaks resume. Neither is catastrophic.

**Confidence:** Moderate. The Orchestrator wanted these frozen; the Critic and Pragmatist identified the contradiction with measurement-first principles. The Pragmatist's argument that failure costs are low and recoverable was not refuted.

### D6: Do not freeze the prompt template structure

The Architect argued for freezing PromptBuilder's template interface (identity, situation, task assembly order). The Critic and Pragmatist identified the hidden cost: if Q2-D3 is correct and context dominates by Round 2, the first experiment needed is whether different injection orders change that outcome. Freezing the template interface eliminates the cheapest experimental lever before running the experiment.

D3 above (freeze context budget priority order) captures the actual load-bearing concern the Architect identified, without locking template syntax or assembly mechanics.

**Confidence:** Moderate. The Architect's concern was valid but targeted the wrong layer. The Surgeon's reframing resolved the tension.

### D7: Measurement of context utilization is the first required measurement

Before any other V2 measurement (agent differentiation, synthesis quality, round effectiveness), measure context utilization per agent call. This determines whether agents are hitting truncation limits. If they are, all other measurements capture truncated behavior, not the mechanism under test. This is the prerequisite that validates every subsequent experiment.

**Confidence:** High. The Surgeon's argument was not challenged, and it follows directly from Q4-D1 (measure constraints first) and Q2-D3 (context accumulation dominates).

---

## Summary

V2 has exactly two permanent freezes, one conditional freeze, and a measurement prerequisite:

| Category | Mechanism | Status |
|----------|-----------|--------|
| Permanent freeze | Claude CLI subprocess boundary | Do not touch |
| Permanent freeze | Session output file structure | Do not touch |
| Conditional freeze | Context budget priority order | Frozen until context utilization is measured |
| Open for experimentation | Round execution sequence | Varies by mode, already designed to change |
| Open for experimentation | Manifest format, persistence mechanics | Measurable, recoverable failure modes |
| Open for experimentation | Prompt template structure | Cheapest experimental lever for agent differentiation |

The single ordering constraint carries forward from prior sessions: measurement before mechanism. The Orchestrator's and Architect's proposals both violated this by prescribing freezes on unmeasured mechanisms. The corrected position is that nothing earns freeze protection without measured evidence that it is both load-bearing and working correctly — except the two mechanisms where failure is unrecoverable or breaks user access to prior work.
<!-- complete -->
