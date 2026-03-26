# Transcript: What V2 features should be behind feature flags vs always-on?

*Generated: 2026-03-26 12:32*

## Round: PROPOSE

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

## Round: CRITIQUE

### The Adversarial Critic (adversarial reviewer)

Both proposals share a fatal assumption: that you can distinguish "well-understood improvements" from "experimental mechanisms" before shipping them into real sessions. Blind proposals are "well-understood"? Based on what evidence? You have zero production data. The decision to ship blind proposals without a flag assumes the current round structure survives contact with agents that can't see each other's work. What happens when three agents independently propose the same architecture and synthesis produces a document that reads like one person talking to themselves? That's not a hypothetical -- it's the most likely outcome, and neither proposal accounts for it.

The Flow Orchestrator wants three flags. The Cognitive Architect wants four. Nobody is asking the harder question: **what is the rollback plan when an unflagged feature breaks a session mid-run?** You can't un-blind proposals in round two after round one already ran blind. You can't retroactively apply eviction priorities to a context window that already overflowed. The asymmetry between "flag it" and "ship it" isn't about confidence -- it's about reversibility. Every irreversible change needs a flag regardless of how "well-understood" it seems.

The Cognitive Architect's "behavioral coupling" criterion sounds principled but is untestable. How do you measure coupling between agent behaviors before you've observed them interact under the new system? You're building a categorization framework on top of data you don't have.

And the 800-token agent identity cap everyone accepted? That's your first-to-break component. Nobody's verified that any current agent definition actually fits in 800 tokens after prompt assembly. If they don't, your entire eviction order is theoretical.

## Position Summary
I advocate for flagging every V2 behavioral change -- including blind proposals -- because reversibility matters more than confidence, and you have no production data to justify confidence in anything. I reject the shared assumption that some features are "well-understood improvements" when the system has never run with any of them. The principle: if you can't undo it mid-session, flag it.

### The Systems Pragmatist (infrastructure realist)

The Adversarial Critic is right that reversibility matters, but wrong about the solution. Flagging everything sounds disciplined until you realize what it actually costs: every flag doubles your test matrix. Three flags = eight configurations. Five flags = thirty-two. You don't have the session volume to validate even one configuration properly, let alone thirty-two. "Flag everything" is complexity cosplaying as caution.

Here's what actually breaks first: **the synthesis step under blind proposals.** Not because agents converge (that's manageable), but because they diverge into incompatible framing. Three agents blind-proposing on auth design will use different terminology, different decomposition boundaries, different implicit assumptions about scope. Your synthesis prompt now has to reconcile three documents that don't share a vocabulary. The current synthesis was tuned for proposals that already reference each other. Nobody's addressed this.

The 800-token cap concern is real but misdiagnosed. The failure isn't "agent definitions don't fit" -- you'll discover that in five minutes of testing. The failure is that 800 tokens forces every agent into the same density of persona specification, which flattens the difference between a tightly-defined specialist and a broadly-scoped generalist. Your agent diversity -- the thing generating discussion value -- gets compressed into uniform blandness.

On flags specifically: the Critic wants mid-session rollback. That's architecturally incoherent. Sessions are append-only by design. The useful boundary is per-session, not mid-session. You pick your configuration at session start and live with it. That's not a limitation, that's the only sane contract.

## Position Summary
I advocate for per-session configuration of blind proposals and graduated resistance only, because those are the two features that change synthesis input structure, which is the actual blast radius. I reject both "flag everything" and "flag only experiments" -- the criterion should be whether a feature changes what the synthesis step receives, not whether we feel confident about it. Flag what breaks downstream; ship what's contained.

## Round: EVALUATE

### The Product Oracle (user advocate)

**The Pragmatist wins. Flag what changes synthesis input.**

Here's what the user actually experiences: the Morning Brief. Work backward from there. The synthesis step is the last transform before the user reads anything. If a feature changes what synthesis receives, a miscalibration corrupts the output the user paid for. If a feature changes agent behavior but synthesis still gets the same shape of input, the worst case is a mediocre round — not a corrupted deliverable.

**Blind proposals change synthesis input structure.** Agents no longer build on each other. Synthesis receives independent positions instead of a conversation. That's a different document shape. Flag it.

**Graduated resistance changes synthesis input.** If agents are pushing back harder, synthesis receives more contentious, less converged material. The Morning Brief shifts from "here's what we agreed" to "here's what we fought about." The user notices. Flag it.

**Ego simulation does NOT change synthesis input shape.** It changes how agents weight their own prior positions. Synthesis still receives proposals and critiques in the same format. Ship it always-on or don't ship it. A flag adds configuration surface for something the user will never toggle.

**Anti-coordination scoring is instrumentation.** It measures; it doesn't alter. Always-on.

**Tiered summarization is context management.** It changes what agents see, not what synthesis receives. The user doesn't experience "oh, summarization was too aggressive." They experience "the agents seemed less informed." That's a tuning problem, not a kill-switch problem. Always-on.

The Critic's "flag everything" approach sounds safe but actually creates a worse product: a wall of configuration that a solo builder must understand before running a session. That's not safety — that's friction disguised as caution.

Two flags. Both justified by synthesis blast radius. Done.

## Position Summary
I advocate for exactly two feature flags — blind proposals and graduated resistance — because those are the only features that change what the synthesis step receives, which is the last gate before the user's Morning Brief. I reject both the "flag everything" approach (which creates configuration burden without protecting user experience) and the "flag experiments only" framing (which uses developer confidence rather than user impact as the criterion). The right test is simple: if this breaks, does the Morning Brief get worse — or does a round just get weaker?

### The Context Surgeon (context efficiency evaluator)

**The Pragmatist's criterion is correct, but everyone missed the token cost of the flags themselves.**

Every feature flag adds context overhead: conditional branching in PromptBuilder, flag state serialized in session.json, and — critically — explanatory tokens in prompts when behavior shifts. "You are operating in blind proposal mode" costs tokens every round, for every agent. Multiply that across a 7-agent, 3-round session and a boolean becomes 21 prompt injections.

The Oracle's synthesis-blast-radius test is the right filter. But the Oracle hand-waves ego simulation as "ship always-on or don't ship it." That's not an analysis — that's punting. Ego simulation changes how agents weight prior positions, which changes the *content distribution* of what synthesis receives. Not the shape. The distinction matters. Shape changes (blind proposals) break synthesis parsing assumptions. Content changes (ego simulation) shift quality gradients. The first needs a kill switch. The second needs tuning knobs in agent YAML, not a session-level flag.

The Critic's "flag everything" fails on information theory grounds. More flags means more configuration state, which means more context tokens burned on explaining current mode to agents. You're spending context budget on meta-information about behavior instead of on the actual discussion. That's a direct tax on output quality — the thing you're supposedly protecting.

**Graduated resistance** belongs in team YAML as intensity bounds per mode, not as a session boolean. The Cognitive Architect was right on that specific point and the Oracle missed it.

Two session flags: blind proposals and tiered summarization. Graduated resistance and ego simulation are agent-level tuning, not session-level switches.

## Position Summary
I advocate for two session-level flags (blind proposals, tiered summarization) with graduated resistance and ego simulation handled as agent/team YAML configuration rather than session flags, because session flags cost context tokens on every prompt injection across every agent in every round. I reject the "flag everything" approach as a context budget tax that actively degrades the output quality it claims to protect. The criterion isn't just blast radius — it's blast radius weighed against the per-prompt token cost of carrying the flag.


<!-- complete -->
