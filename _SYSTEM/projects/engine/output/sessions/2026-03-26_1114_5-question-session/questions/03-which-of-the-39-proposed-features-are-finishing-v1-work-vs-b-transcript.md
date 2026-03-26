# Transcript: Which of the 39 proposed features are finishing V1 work vs building genuinely new systems?

*Generated: 2026-03-26 11:29*

## Round: PROPOSE

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

## Round: CRITIQUE

### The Adversarial Critic (adversarial reviewer)

Both proposals share a dangerous assumption: that you can cleanly classify 39 features at all. Neither has actually enumerated them. They're arguing about taxonomy for a list nobody has pinned down. That's architecture theater.

**The enumeration problem.** Where are these 39 features? If they came from a brainstorming session or brief, features bleed into each other. "Speaking order rotation" — is that one feature or three? (Random, round-robin, weighted.) "Per-agent contribution visibility" — output formatting change or new metrics pipeline? Until someone defines feature boundaries with enough precision to estimate, any classification scheme is premature optimization of a vague list.

**The dependency depth model breaks immediately.** Cognitive Architect says instrumentation must precede mechanisms. Fine in theory. In practice, what counts as "instrumentation"? Logging agent token counts is trivial. Measuring whether agent identity persists across rounds requires defining identity metrics that don't exist yet. You can't instrument what you can't define, and you can't define it without building experimental mechanisms first. The dependency is circular, not linear.

**The state machine criterion is honest but insufficient.** Flow Orchestrator's test — does it need new state machines? — gives you a binary that's easy to apply but tells you nothing about effort, risk, or value. A feature requiring zero new state machines can still take weeks if it touches prompt assembly across all round types.

**What actually fails first:** someone builds three "instrumentation" features, discovers they measure the wrong things, and the mechanism features built on top produce garbage data that looks authoritative.

**The real question nobody is asking:** which five features, if built wrong, make the other 34 worthless?

## Position Summary
I advocate stopping the classification debate and instead identifying the five highest-risk features whose failure would cascade across the roadmap. I reject both the dependency-depth taxonomy and the state-machine binary as classification schemes applied to an unnumbered, poorly-bounded feature list. Until someone enumerates concrete features with defined boundaries, arguing about how to sort them is optimizing a spreadsheet with no rows.

### The Systems Pragmatist (infrastructure realist)

The Critic is right that nobody has enumerated the list. But the Critic's own proposal — "find the five highest-risk features" — has the same problem. You can't identify cascade risks in an unnumbered list either. So we're three proposals deep and zero people closer to a concrete artifact.

**The circular dependency is real but solvable.** The Critic claims you can't instrument identity persistence without building mechanisms first. Wrong. You can instrument *proximate signals* right now: token-level overlap between agent responses across rounds, semantic similarity scores, prompt-template token ratios versus context-window ratios. These are crude. They're also measurable today with zero new subsystems. The question isn't whether perfect instrumentation precedes mechanisms — it's whether *any* signal beats zero signal. It does. D3 already told us context accumulation dominates identity by Round 2. Someone observed that. Formalize the observation into a metric, ship it, then build on it.

**What both proposals and the Critic miss: the V1/new distinction is a scope control mechanism, not a taxonomy.** The question isn't philosophical. It's operational. If a feature touches only files that exist today and requires no new interfaces, it ships faster and breaks less. If it requires new abstractions, it needs design review. That's the only distinction that matters for sequencing.

**The actual blast radius question:** the decided items already identify the first failure point. Atomic writes for session.json is a V1 blocker. If that ships broken, every session after the first crash produces corrupt state. That's not one of five risky features — it's the single feature that gates everything else.

Stop debating classification. Enumerate the list. Tag each item: existing-file-only or new-interface-required. Ship the first category while designing the second.

## Position Summary
I advocate a mechanical triage — existing-file-only versus new-interface-required — applied to a concrete enumerated list, not abstract taxonomy debates. I reject both the dependency-depth model and the cascade-risk approach as premature when nobody has written down what the 39 features actually are. Ship crude instrumentation now using proximate signals from existing observations, then iterate.

## Round: EVALUATE

### The Product Oracle (user advocate)

The Critic is right and everyone else is wrong. We're sorting an empty spreadsheet.

**What the user sees today:** They run a session, get a Morning Brief, and read design docs. That's the entire product surface. Every feature proposal only matters if it changes what appears in those outputs or how reliably they appear.

The dependency-depth taxonomy, the state-machine binary, the cascade-risk model — none of these answer the question the user is actually asking: *"Will my next Morning Brief be better?"*

Here's what I'd do instead, and it's closer to the Critic's position than anyone else's:

**Step 1: Enumerate the 39 features.** Actually write them down. With boundaries. The Pragmatist is correct that nobody has done this yet, but wrong to propose a triage method before the list exists.

**Step 2: For each feature, answer one question:** Does this change what the user reads in the Morning Brief or design docs? Yes/no. That's the split that matters — not V1-vs-new, not dependency depth, not state machine topology.

**Step 3: Within the "yes" pile, order by:** Can we measure the improvement? If we can't tell whether the feature worked by reading output, it's not ready to build. This respects the decided finding — measurement before mechanism — without inventing a three-tier taxonomy to say it.

The Architect's dependency model is intellectually honest but adds a layer of abstraction between "what should we build" and "what does the user get." The Orchestrator's state-machine lens is engineering-accurate but user-blind. The Pragmatist's file-boundary heuristic is practical but optimizes for developer convenience, not user value.

Ship the list. Score it against output quality. Build what scores highest.

## Position Summary
I advocate enumerating all 39 features and scoring each by whether it visibly improves what the user reads in the Morning Brief or design docs, because that's the only classification that connects engineering work to user value. I reject all three proposed taxonomies — dependency depth, state-machine boundaries, and cascade risk — as internal organizing schemes that don't answer whether the user's experience improves. The Critic correctly identified that we're debating how to sort a list nobody has written, and until that list exists with concrete boundaries, every classification framework is premature abstraction.

### The Context Surgeon (context efficiency evaluator)

The Oracle and Critic converged on the right answer: enumerate before classifying. But the Oracle made a mistake the Critic avoided — proposing a scoring method ("does it change what the user reads?") before the list exists. That's the same premature abstraction everyone else committed, just wearing user-empathy clothing.

Here's what I see that nobody's said yet: **this entire discussion is a context waste problem.**

The 39 features live somewhere — a doc, a backlog, someone's head. Every round spent debating classification schemes without surfacing that list burns tokens arguing about a function signature nobody's defined. The Architect, Orchestrator, and Pragmatist each proposed sort algorithms for an empty array. The Critic correctly called `sort([])` pointless. The Oracle then proposed a *better* sort algorithm for the same empty array.

The V1-vs-new distinction in the original question is actually answerable mechanically: grep the codebase for stubs, TODOs, and partial implementations. That's the V1 pile. Everything else is new. No taxonomy needed. No scoring framework. No dependency depth analysis. **The codebase already contains the answer.**

The Pragmatist's "existing-file-only vs new-interface-required" heuristic is the closest to this, but they buried it under a process proposal instead of just doing it. The Architect's dependency model has one valid insight — measurement before mechanism — but that's already a decided finding, not a new contribution.

Stop debating. Enumerate from the codebase. The classification falls out mechanically.

## Position Summary
I advocate extracting the feature list mechanically from the codebase (stubs, TODOs, partial implementations = V1; everything else = new) because the repository already contains the V1-vs-new classification implicitly. I reject all five proposed frameworks — dependency depth, state-machine boundaries, cascade risk, user-output scoring, and file-boundary triage — as unnecessary abstraction layers over an answer that's already encoded in the code. The decided finding "measurement before mechanism" is the only ordering principle needed once the mechanical enumeration exists.


<!-- complete -->
