# What is the critical path for V2?

*Generated: 2026-03-26 12:22 | Q1 | 208s | Mode: compete*

## Decisions

### Critical Path for V2

The critical path is a near-linear chain driven by user-visible value, not architectural purity.

```
Manifest v2 ─┬─ Blind Proposals ──→ Phases ──→ Stale Detection ──→ Anti-Sycophancy
              │
              └─ Key Takeaways (co-ships with blind proposals)

BIT System ────── Independent track, no dependencies
```

**Build order:**

1. **Blind proposals + manifest versioning + key takeaways** (first delivery)
2. **Phase system** (second delivery)
3. **Stale detection** (third delivery)
4. **Anti-sycophancy detection** (fourth delivery, validates blind proposals worked)
5. **BIT system** (parallel track, any time)

---

### 1. Blind Proposals Ship First

Blind proposals is the highest-value, lowest-risk V2 feature. It changes what the user reads in the Morning Brief on day one: agent positions become genuinely independent instead of anchored to whoever spoke first.

**Why not phases first:** Phases are internal plumbing. They produce zero perceptible change to session output. Blind proposals does not require phases -- it requires round position awareness in `RoundRunner`, not session-level state transitions. Building phases first delays the quality improvement users can feel.

**Scope of change:** Blind proposals touches `RoundRunner` (suppress prior responses for first round), `PromptBuilder` (context injection toggle), transcript generation (marking which responses were blind vs. revealed), and the SSE dashboard (buffered reveal). The Critic correctly identified this as distributed cost across four-plus boundaries -- but distributed cost is still small cost when each boundary change is a few lines.

**Key takeaways co-ships** because it is a formatting change to synthesis extraction and is the output improvement users explicitly requested. Natural extraction points exist at round boundaries today; phases make this cleaner later but are not required now.

### 2. Manifest Versioning Is Mandatory Co-Delivery, Not a Blocker

Every V2 feature adds state to `session.json`: blind/revealed flags, phase markers, staleness scores. The current `"version": 1` manifest has no migration strategy.

**Resolution:** Ship manifest versioning alongside blind proposals as hygiene, not as its own workstream. Add a version field, write a migration function that defaults missing fields, and move on. This is a PR, not a project.

### 3. Phase System Comes Second

Phases are a label on groups of rounds with different prompt templates and context accumulation rules. The current `RoundRunner` already sequences rounds; phases add a `PhaseContext` object passed to `PromptBuilder` plus transition validation.

**What phases are not:** A complex state machine. The session flow is linear -- for each question, run phase sequence, within each phase run rounds. There is one decision point: "is this phase complete?" Everything else is iteration with a label.

**What phases enable:** Phase-specific prompt injection, cleaner blind proposal boundaries, semantic anchors for stale detection, natural extraction points for key takeaways, and measurable BIT dimension behavior across propose vs. challenge.

**Why second, not first:** Phases make blind proposals cleaner but don't make them possible. Building phases before validating that blind proposals improves output quality is premature infrastructure.

### 4. Stale Detection Requires Phases

Stale detection compares content across phase transitions to identify repetition vs. progress. Without phase semantics, staleness measurement has no anchor for what kind of staleness is being measured -- repeating the same position in a proposal round means something different than repeating it in a convergence round.

**Dependency:** Phase system must exist before stale detection can distinguish meaningful repetition from structural repetition.

### 5. Anti-Sycophancy Is Validation, Not Architecture

Anti-sycophancy detection measures whether blind proposals actually changed agreement patterns. It compares independent positions (from blind propose) to post-discussion positions (after reveal and critique) and flags suspicious convergence.

**Why last:** You cannot calibrate sycophancy detection without data from blind proposals. Building the measurement before the intervention is backwards. If blind proposals ships and agreement patterns don't change, the problem is product design, not detection tooling. Ship blind proposals, collect data, then build detection against real baselines.

**Cut option:** If V2 scope needs trimming, anti-sycophancy detection is the first feature to defer to V3. Blind proposals and adversarial role overlays are the mechanism; detection is optional instrumentation.

### 6. BIT System Is Independent

The BIT system (personality dimensions, behavioral trait configuration) has no structural dependency on any other V2 feature. It can be built in parallel at any time.

**Phase interaction:** BIT gains measurable value after phases exist -- you can observe whether a trait dimension actually changes agent behavior across propose vs. challenge phases. But this is an enhancement to BIT analysis, not a build dependency.

---

## Rejected Positions

**Phases-first (Cognitive Architect):** Rejected. Conflated round-level mechanics (blind proposals) with session-level structure (phases). Blind proposals is a round runner change, not a session architecture change. Inflating phases into a prerequisite for everything delays the feature that changes output quality.

**Cut anti-sycophancy entirely (Flow Orchestrator):** Partially accepted. Anti-sycophancy is deferred to last in the chain and is the first candidate for V3 deferral, but not pre-emptively cut. The measurement has value once blind proposals provides a baseline.

**Schema evolution as blocker (Adversarial Critic):** Rejected as a blocker, accepted as hygiene. Manifest versioning ships alongside blind proposals, not before it. It is a solved problem that does not warrant its own workstream.

---

## Risk Register

| Risk | Mitigation |
|---|---|
| Prompt budget exhaustion when V2 features compose in the same round | Audit token ceiling before second feature ships. Blind proposals actually reduces propose-round prompt size (no prior responses). Monitor truncation behavior in `defaults.yaml` limits. |
| Evaluator doesn't know what agents could see when | Blind/revealed metadata in transcript and session manifest. Evaluator prompt includes visibility context per round. |
| SSE dashboard assumes streaming responses as they arrive | Buffered reveal mode for blind rounds. Dashboard shows "agents thinking..." until all blind responses complete, then reveals simultaneously. |
| Second feature fights first feature's state shape in session.json | Manifest versioning co-ships with blind proposals. All V2 state additions use optional fields with defaults. |
<!-- complete -->
