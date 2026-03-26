### The Cognitive Architect (creativity engine designer)

The knowledge base documents *behavior*. Code generation requires *contracts*.

These are not the same thing, and the gap between them is the entire problem.

"Enemy deals 3 damage on contact" is a behavioral fact. A code-generating agent also needs: What is the entity model? What is the collision detection approach? What is the frame timing contract? When is this damage check valid vs. ignored (invincibility frames, death state, cutscenes)? These aren't more facts about the mechanics — they're a different *representation layer* entirely.

What's missing is a **System Contract Layer** sitting between the behavioral knowledge base and code generation. Four components:

**1. State Machine Topology** — Every system needs explicit states, valid transitions, and guards. "Combat" as described tells you outcomes. It doesn't tell you the state graph the game is actually running.

**2. Execution Order Manifest** — Which systems update in which order per frame. NES games have hard-coded execution sequences baked into the ROM loop. This isn't mechanics — it's architecture. Getting it wrong produces games that look right but *feel* wrong.

**3. Asset Interface Contracts** — Dimensions, anchor points, palette indices, animation frame counts. The knowledge base references assets as semantic objects. Code needs them as typed interfaces.

**4. Platform Approximation Target** — NES timing, input latency, and "feel" characteristics are not discrete values — they're emergent from hardware constraints. An agent needs explicit targets: fixed timestep value, input polling model, pixel-perfect collision vs. radius.

The hierarchy is excellent for comprehension. It is not sufficient for generation. We need a thin machine-readable contract layer derived from it.

## Position Summary
I advocate for a System Contract Layer — a machine-readable schema derived from behavioral specs that defines state topology, execution order, asset interfaces, and platform targets. I reject the premise that more complete mechanics documentation closes this gap, because the gap is representational, not factual. Behavioral knowledge and implementation contracts are different artifacts serving different consumers, and conflating them produces a knowledge base that humans can read but agents cannot execute.

### The Flow Orchestrator (mechanical flow designer)

The Cognitive Architect is right that behavioral knowledge ≠ implementation contracts. But the proposed four-component layer over-solves.

Two of the four items are already handled or trivially resolved:

**Asset Interface Contracts** — for NES clones, these are constants. Sprite dimensions, palette constraints, tile sizes: one shared NES-platform-constants file covers every game. This isn't a knowledge base gap, it's a lookup table.

**Platform Approximation Target** — same. NES runs at 60.1 fps, has specific input polling timing, uses pixel-perfect collision. These don't vary per game. One constants document, referenced once, done.

What's actually missing is exactly two things:

**1. Frame loop execution order.** Which systems tick, in which sequence, on which conditions. This is the real unresolved gap. "Combat deals damage on contact" tells you nothing about whether the damage check runs before or after position update, before or after animation state, before or after death check. Getting this wrong produces games that *look* right and *feel* wrong — the Architect named this correctly. This needs to be explicit per-game data.

**2. System dependency graph.** Not full state topology — just which systems read from which other systems' state. This tells a code generator what can parallelize and what must sequence.

State machine topology as a full artifact is premature. A code-generating agent can derive states from behavioral descriptions if the descriptions are precise. We don't need a separate state graph if the behavioral layer is doing its job.

Propose the minimum: execution order manifest + dependency edges. Everything else is either derivable or a shared constant.

## Position Summary
I advocate for exactly two additions to the knowledge base: a per-game frame-loop execution order manifest and a system dependency graph indicating read/write relationships between systems. I reject the full four-component System Contract Layer as containing two items (asset contracts, platform targets) that are NES-wide constants, not per-game gaps. The remaining gap is real but narrow — execution sequencing and system coupling — and adding more structure than that creates maintenance burden without closing the actual generation bottleneck.


<!-- complete -->
