# Transcript: Tier Regression Rebuild Path

*Generated: 2026-03-25 17:08*

## Round: PROPOSE

### Max (atmospheric flight advocate)

Here's what I want on the table before we answer the economics question.

Tier regression is the SimCopter payoff inverted — you bank over your settlement and see it *smaller* than you left it. That's the knife-in-the-gut moment the whole atmospheric layer is built to deliver. The rebuild arc is the recovery from that moment. What the player sees from 500 meters during that recovery IS the experience. So the rebuild path question isn't primarily an economy question — it's a **flight-view question**.

Two things I need the group to address:

**1. Does the rebuild path have visible intermediate states?**
If regression snaps geometry from intact → degraded and rebuild snaps it back, the aerial view is binary. But if partial reconstruction has its own geometry state — scaffolding, a half-built power node — then the player *watches their settlement come back* from altitude across multiple sessions. That's the Cities: Skylines pull. That's earned investment. The asset cost is real but I think it's the right cost.

**2. Does the faster recovery path route through the atmospheric layer?**
If recovery missions exist and they're dirtside Bar pickups only, we've made atmospheric flight optional to the rebuild arc. Wrong. Recovery should pull the player *up and out* — escort a supply run, intercept a patrol, do something that requires actually flying. The atmospheric layer needs to own the recovery feel, not just the destruction feel.

The economic question — same cost vs. reduced cost — I can live with either answer. But the path needs to *look* like something from altitude.

### Ren (emergence systems theorist)

Max is right that the rebuild arc needs to be readable from altitude — but I want to push the systems interaction dimension of what he's describing.

The partial geometry state (scaffolding, half-built power node) isn't just aesthetic payoff. It's an **information surface the raid system should read**. A settlement mid-rebuild has a different vulnerability profile than a fully intact one — power node down means emplacements offline means specific vectors are undefended. If the assault raid AI does a live structural pass before selecting spawn bearings, partial reconstruction creates a natural window where the faction that raided you has a read on your weakest vector. You're not just rebuilding against a timer, you're rebuilding against an adversary that can see your scaffolding from the same altitude you can.

That's not a scripted event. That's the raid composition system and the building state system interacting to create pressure the designer didn't author.

On the economic question: reduced cost with a standing gate is systemically richer than flat same-cost. It creates a tension between economic speed (rebuild is cheaper, act now) and political readiness (can't tier back up without the standing). Those two rates — how fast you can rebuild economically versus how fast standing recovers through missions — are orthogonal clocks. Players will naturally feel the gap between them without anyone explaining it.

Max's atmospheric recovery point stands. If supply escort missions are the standing-recovery vehicle, and standing is the advancement gate, then the atmospheric layer owns the rebuild arc mechanically, not just visually. That chain closes correctly.

## Round: CRITIQUE

### Vera (EV systems historian)

Two proposals are on the table. One introduces a third geometry state. The other re-opens a decision this group already closed.

On the third geometry state: the existing decision is two states per building — intact and degraded. Max is proposing scaffolding as a distinct partial-construction state. That's three states per building type, six assets at Outpost tier becomes nine, and the visual language you're adding has to be legible at 500 meters in flat-poly alongside the existing two. That's not an aesthetic note — that's an asset scope question that needs to be named before the group can say yes to it. EV didn't have partial construction states. You had credits, you bought the outpost upgrade, you had it or you didn't. The legibility was binary. If you're departing from that, say so explicitly.

On Ren's structural-pass proposal: assault raid AI querying live building states before selecting spawn vectors is the power-emplacement dependency problem. This was decided in Q12 — "rational targeting in assault-scale raids...is a weeks-level build item." The decision log says it "does not ship in M7." Ren is proposing it again without naming it. I want that identified before it gets absorbed into the rebuild-path discussion as though it's new.

The core question — same cost versus reduced cost with a standing gate — is answerable without either of those additions. What does reduced cost actually mean mechanically? Is it a time discount, a resource discount, or a mission requirement waiver? The answer changes what "faster" actually buys the player.

Name the mechanism. Then we can evaluate it.

### Nadia (new-player experience advocate)

Vera's question is the right one, but I want to surface a new-player trap before we answer it.

The standing gate on recovery creates a potential double-punishment loop: standing drops → raid fires → tier regresses → need standing to advance again → standing recovery requires missions → missions require understanding a faction system the player may have only just discovered caused the raid. That's four layers of causality a player who just watched their settlement shrink has to trace backwards. If the tooltip and Bar dialogue don't close that loop explicitly, new players will read it as broken, not systemic.

So: reduced cost yes, but only if the recovery path is **self-explaining at the moment of regression**. Not in a tutorial panel. In the world. The comms intercept string and the Bar cold dialogue both fire around the standing-drop event — one of those surfaces should name the rebuild gate directly. "Your standing with [Faction] is what's blocking reconstruction, not your credits."

On Max's atmospheric recovery pull: this is correct design and I'd push further. If supply escort missions are the standing-recovery vehicle, make that legible from the moment of regression. The player surfaces from underground to find their tier changed. They should be pulled *up* immediately — an escort request queued at the Bar, a mission that requires flying. The destruction is dirtside. The rebuilding should feel like it lives in the sky.

On partial geometry states: scaffolding reads as "in progress" to anyone, no EV knowledge required. That's the right legibility signal. The asset cost is real but Vera's the one to scope it, not me.

## Round: EVALUATE

### Soren (solo dev scope warden)

Three items before the economic question gets any airtime.

**The third geometry state is a scope multiplier, not an aesthetic choice.**
Outpost tier: 3 building types × 2 states = 6 assets. Add scaffolding: 3 × 3 = 9. That ratio holds at every tier above Outpost. We don't know Settlement, Colony, or City building counts yet — that's an open question — but whatever that number is, Max's proposal multiplies it by 1.5. In flat-poly, a scaffolding state isn't a color swap. It's a distinct mesh. Call it 2–4 days per building type for the scaffolding variant, minimum. At Outpost alone that's 6–12 days of asset work on top of the intact/degraded pass. Before it goes on the table as a yes, it needs a day count attached to it.

**Ren's structural-pass proposal is Q12's closed decision, restated.**
"Assault raid AI querying live building states before selecting spawn bearings" is exactly what Q12 called "a weeks-level build item" and placed out of M7. Naming it as emergence doesn't change the build cost. It's back on the table without a flag. I'm flagging it.

**The economic question is answerable without either addition.**
Reduced cost with a standing gate is mechanically richer than same cost. The two orthogonal clocks Ren describes — economic rebuild rate vs. standing recovery rate — create pressure that doesn't require authoring. That's correct. The mechanism needs naming: is the discount a resource reduction, a time reduction, or a step-count reduction in the tier advancement sequence?

Name the mechanism. Asset scope and AI scope are separate conversations that need separate estimates before they're decided.

<!-- complete -->
