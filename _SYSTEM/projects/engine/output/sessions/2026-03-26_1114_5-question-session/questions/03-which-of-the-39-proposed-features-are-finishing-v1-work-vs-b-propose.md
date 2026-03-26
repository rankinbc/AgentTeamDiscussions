### The Cognitive Architect (creativity engine designer)

The wrong way to categorize these 39 features is "V1 completion vs. new systems." That binary hides the actual risk: features that *look* like V1 polish but secretly require architectural commitments you can't undo.

I propose a three-tier classification based on **dependency depth**:

**Tier 1 - Wiring** (no new abstractions needed): Speaking order rotation, atomic writes, per-agent contribution visibility, ledger quarantine surfacing. These connect existing pieces. Ship them. Maybe 8-10 features land here.

**Tier 2 - Instrumentation** (new observation, no new control): Transcript auditing, context window consumption tracking, behavioral distinctiveness metrics, round-over-round identity decay measurement. These features *watch* the system. They're prerequisites for everything else because D4 says "audit before redesigning." Probably 10-12 features. This is where teams get sloppy - they skip instrumentation and jump to mechanisms they can't evaluate.

**Tier 3 - Mechanisms** (new control loops): Stigmergic coordination, dynamic context budgeting, personality-to-cognitive-strategy migration, adaptive round structures. These create feedback loops that change system behavior. Every one requires its own evaluation criteria *before* you build it, or you'll never know if it works. The remaining 15-20 features.

The critical insight from creativity research: **you cannot design differentiation mechanisms without first measuring current differentiation.** D3 tells us context accumulation dominates identity by Round 2. Until instrumentation proves *where* identity collapses and *how much*, every Tier 3 feature is speculative architecture.

The 39 features aren't a backlog to prioritize. They're a dependency graph where Tier 2 unlocks Tier 3.

## Position Summary
I advocate classifying features by dependency depth (wiring, instrumentation, mechanisms) rather than V1-vs-new, because the real constraint is that mechanism features cannot be evaluated without instrumentation features built first. I reject treating this as a flat prioritization exercise. The decided finding that context accumulation dominates identity by Round 2 means building differentiation mechanisms before measuring differentiation is architectural gambling.

### The Flow Orchestrator (mechanical flow designer)

The Cognitive Architect's three-tier model is elegant but adds a layer of abstraction we don't need. "Dependency depth" is just another way of saying "do the simple things first" — which is obvious. The tier labels don't change what ships when.

Here's what actually matters: **can you draw the state transition diagram or not?**

Features where the state machine already exists and you're filling gaps — those are V1 completion. Speaking order rotation: the round runner already iterates agents, you're changing the iterator. Atomic writes: SessionPersistence already writes, you're wrapping it. Ledger quarantine: DecisionsLedger already appends, you're adding a filter. These features have known entry states, known exit states, and no new event types.

Features requiring **new event types or new state machines** — those are new systems. Stigmergic coordination needs a shared artifact store that nothing currently reads or writes. Dynamic context budgeting needs a measurement-before-prompt loop that doesn't exist in PromptBuilder's current three-layer assembly. Adaptive round structures need DiscussionEngine to accept round definitions at runtime instead of reading them once from team YAML.

I agree instrumentation matters, but I reject calling it a separate tier. Transcript auditing is V1 completion — you're reading output files that already exist. Context window tracking is a new system — you need token counting infrastructure that doesn't exist anywhere in ClaudeRunner today.

The Cognitive Architect says Tier 2 "unlocks" Tier 3. That's true for maybe three features. Most Tier 3 features have design constraints you can identify now without metrics. Don't build a dependency graph where a checklist works.

## Position Summary
I advocate classifying features by whether they require new state machines and event types (new systems) versus filling gaps in existing ones (V1 completion). I reject the three-tier model as unnecessary abstraction that conflates a real dependency (measurement before mechanism) with a general organizing principle. The codebase's current control flow — not an abstract dependency depth — is the only honest scoping criterion.


<!-- complete -->
