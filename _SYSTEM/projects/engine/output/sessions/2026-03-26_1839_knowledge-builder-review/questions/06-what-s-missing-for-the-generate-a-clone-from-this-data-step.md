# What's missing for the "generate a clone from this data" step?

*Generated: 2026-03-26 19:02 | Q6 | 228s | Mode: compete*

## Decisions

### 1. The Target Artifact Must Be Defined Before Any Schema Work Proceeds

The entire discussion of what metadata is "missing" is undefined without first specifying what the generation agent is producing. The target is a modern reimplementation — Python, C++, or a game framework such as pygame or Godot — not 6502 assembly or ROM output. This collapses arguments about zero-page memory topology and NES hardware register layout as per-game knowledge base concerns; those belong in a shared platform context document available to the agent, not replicated inside game_specs. This decision is a precondition. Any schema additions that do not reference a concrete target artifact are premature.

### 2. A Behavioral Assertion Format Is the Primary Missing Artifact

The generation gap is not an information problem and not solely a capability problem. It is a validation loop problem. An agent given complete mechanics documentation can produce plausible-wrong output that is indistinguishable from correct output without a verification signal. The knowledge base being complete makes this worse, not better — confidence in completeness masks undetectable divergence.

The missing artifact is a machine-checkable behavioral assertion format: known-input / expected-output pairs that allow generated code to be tested against documented behavior. These assertions are derived from the existing knowledge base but are a separate artifact class. They are not unit tests in the programming sense — they are behavioral contracts expressed at the level of game mechanics.

Format requirements:
- Each assertion targets a named system at a specified depth level
- Assertions specify: precondition state, triggering input or event, expected output state or observable result
- Assertions carry provenance tags using the existing tier system (ROM_VERIFIED assertions are high-confidence; INFERRED assertions flag uncertainty)
- UNKNOWN-tagged mechanics produce no assertions; they produce assertion gaps, which are explicit and machine-readable

Assertion files live alongside the system files they cover, following existing path conventions.

### 3. Player-Observable Fidelity Criteria Are the Anchor Layer Above Assertions

Behavioral assertions are internal metrics. Without grounding them in what a player would recognize as faithful, generated code can pass all assertions and still feel wrong. Player-observable fidelity criteria are the layer above assertions: human-readable behavioral benchmarks expressed as what a tester running the original game would check.

These criteria are not test scripts. They are written in natural language, indexed to named systems, and describe the observable outcome a player experiences — not the internal state an assertion checks. Examples: "dying in combat returns the player to the last town entrance, not the world map"; "the magic timer depletes at the same apparent rate during boss encounters as during field encounters."

Fidelity criteria are the source from which assertions are derived. The authoring order is: fidelity criteria first, assertions second. This grounds the entire generation-verification loop in user-visible behavior rather than internal implementation metrics.

Fidelity criteria files live at the system README level (Level 1 in the hierarchy), not at leaf level.

### 4. A Per-Game Frame-Loop Execution Order Manifest Is Required

The behavioral knowledge base documents outcomes. It does not document when systems execute relative to each other within a frame. Getting execution order wrong produces games that match all documented mechanics but feel wrong — damage checks running before or after position updates, death state checks occurring in the wrong sequence, animation state diverging from game state.

A frame-loop execution order manifest is required per game. It specifies:
- Which systems tick each frame
- The sequence in which they execute
- Any conditional execution (systems that only tick on certain game states)
- The frame boundary and update model (fixed timestep, the NES-equivalent loop structure)

This manifest is not derivable from behavioral descriptions. It is a distinct artifact. It lives at the root of game_specs as a peer to the top-level README.

### 5. A System Dependency Graph Is Required

Code generation requires knowing which systems read from and write to which other systems' state. This is not derivable from individual system documentation. It must be explicit.

The dependency graph specifies read/write relationships between systems at the named-system level (not sub-system level). It does not need to be a formal graph format — a structured list of "System A reads: [x, y]; writes: [z]" per system is sufficient. This is maintained in the same machine-readable manifest introduced in the Q4 decision (the per-game machine-readable manifest).

The dependency graph is not a full state machine topology. State topology at the level of explicit states and transitions is derivable from precise behavioral descriptions and is not a required separate artifact at this stage.

### 6. NES Platform Constants Are a Shared Document, Not Per-Game Data

Asset interface constants (sprite dimensions, palette constraints, tile sizes, OAM layout) and platform approximation targets (60.1 fps fixed timestep, input polling model, pixel-perfect collision model) are NES-wide, not per-game. These do not belong in game_specs. They belong in a shared platform context document that is provided to generation agents as part of their context, not replicated per game.

Per-game asset data that does vary — mapper type, CHR-ROM bank count, specific palette assignments, animation frame counts for named sprites — does belong in game_specs under asset system documentation.

### 7. The Generation-Validation Loop Architecture

With the above artifacts in place, the generation-validation loop is:

1. Generation agent receives: behavioral knowledge base (existing hierarchy), frame-loop execution manifest, system dependency graph, platform context document, behavioral assertions for covered systems
2. Agent generates code for a named system or set of systems
3. Assertion runner checks generated code against behavioral assertions
4. Assertion gaps (from UNKNOWN-tagged mechanics) surface as explicit warnings, not silent passes
5. Player-observable fidelity criteria are the human review layer above automated assertion passes — a generation pass is incomplete until a human tester has confirmed fidelity criteria are met for the target systems

This loop is iterative. Assertion failures feed back into generation. Fidelity criteria failures feed back into either generation or knowledge base research (if the failure reveals a gap in documentation).

### 8. What Is Not Decided Here

- The specific format or schema for behavioral assertions (deferred to implementation)
- The tooling for running assertions against generated code (deferred)
- Whether assertions are authored by humans, derived automatically from knowledge base content, or generated by a separate agent pass (open question)
- How assertion coverage is tracked relative to knowledge base completeness
- The process for promoting INFERRED assertions to ROM_VERIFIED status
- Cross-game reuse of assertions for mechanics that appear in multiple games (deferred to scale)
<!-- complete -->
