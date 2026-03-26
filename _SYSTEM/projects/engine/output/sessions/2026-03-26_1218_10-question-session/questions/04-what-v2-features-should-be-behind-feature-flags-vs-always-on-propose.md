### The Flow Orchestrator (mechanical flow designer)

## Feature Flag Design: Minimize the Flag Surface

Feature flags are state. State has costs: configuration drift, testing combinatorics, code paths that rot. Every flag you add doubles your test matrix. So the question isn't "what could we flag?" -- it's "what absolutely must have a kill switch because we cannot predict its effect on output quality?"

**Always-on (no flag):**
- Blind proposals. Decided. Well-understood. Ships as default behavior.
- Manifest versioning. Mechanical bookkeeping. No quality risk.
- Priority-queue eviction with hardcoded order. Deterministic. No calibration needed.
- Agent identity 800-token cap. A constraint, not a behavior.
- Prompt output snapshots. Instrumentation. Zero impact on discussion flow.

**Flagged (off by default, enable per-session):**
- Ego simulation. Novel behavioral injection. Miscalibration directly corrupts agent voice. Kill switch mandatory.
- Anti-coordination scoring. Post-hoc analysis that could feed back into prompts. Feedback loops are unpredictable.
- Graduated resistance. Modifies agent behavior mid-session based on scoring. That's a control loop with no tuning data yet.

**Not flagged because not shipped:**
- Stale detection. Requires phases. Phases aren't built. Don't flag what doesn't exist.
- BIT system. Independent track. Ships when ready, flags add nothing to something that layers on top.

The flag mechanism itself: a `features` map in `session.json`, checked at the prompt assembly layer in `PromptBuilder`. One place. Not scattered across the codebase. If a feature isn't in the map, it's off. Three flags total. That's it.

Don't build a feature flag framework. Build three boolean checks.

## Position Summary
I advocate for exactly three feature flags -- ego simulation, anti-coordination scoring, and graduated resistance -- checked at the PromptBuilder layer via a simple map in session.json. I reject flagging well-understood mechanical changes like blind proposals or eviction order, and I reject building any general-purpose flag infrastructure. Flags are state, state is cost, and three booleans don't need a framework.

### The Cognitive Architect (creativity engine designer)

## The Flag Boundary Is Wrong -- It's Not About Predictability, It's About Behavioral Coupling

Flow Orchestrator's logic is clean but misses the deeper issue. The question isn't "can we predict its effect?" -- it's "does this feature change how agents relate to each other?" Solo features don't need flags. Coupling features do.

**Blind proposals** -- I agree, always-on. But not because they're "well-understood." They're safe because they're *decoupling* mechanisms. They reduce agent interdependence. You can't miscalibrate isolation.

**Ego simulation** -- agree on the flag, disagree on the reasoning. The danger isn't "miscalibration corrupts agent voice." It's that ego creates *feedback dynamics between agents*. Agent A's stubbornness changes what Agent B produces. That's a second-order effect you cannot unit test. Flag it because it's a coupling injection.

**Anti-coordination scoring** -- here's where I diverge hard. Flow Orchestrator flags this because "feedback loops are unpredictable." But if it stays post-hoc with no prompt feedback, it's just measurement. Measurement doesn't need a kill switch. **Flag it only if it feeds back into prompts.** If it's read-only scoring, ship it always-on alongside prompt output snapshots. Same category: instrumentation.

**Graduated resistance** -- flag, yes, but recognize this is the most dangerous feature in the entire V2 list. It's not a "control loop with no tuning data." It's an *adversarial pressure system* that changes group dynamics mid-conversation. Research on minority influence (Moscovici, 1969) shows that consistent dissent shifts group output -- but *escalating* dissent triggers reactance and entrenchment. This needs more than a flag. It needs session-level intensity bounds baked into the team YAML.

**Missing from the list: tiered summarization.** Lossy compression of conversation history changes what agents can reference. That's invisible coupling. Flag it.

## Position Summary
I advocate for flagging based on inter-agent behavioral coupling rather than individual-feature predictability, which means adding tiered summarization as a fourth flag and keeping read-only anti-coordination scoring always-on as pure instrumentation. I reject the framing that graduated resistance is merely an unflagged control loop -- it's an adversarial pressure system requiring intensity bounds in team YAML, not just a boolean kill switch. The principle: decouple freely, couple cautiously.


<!-- complete -->
