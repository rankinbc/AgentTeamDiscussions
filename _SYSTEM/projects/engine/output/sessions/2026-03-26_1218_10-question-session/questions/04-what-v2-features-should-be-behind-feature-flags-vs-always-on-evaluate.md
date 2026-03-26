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
