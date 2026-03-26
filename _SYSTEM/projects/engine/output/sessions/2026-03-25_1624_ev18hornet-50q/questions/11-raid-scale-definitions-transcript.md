# Transcript: Raid Scale Definitions

*Generated: 2026-03-25 17:00*

## Round: PROPOSE

### Max (atmospheric flight advocate)

Okay, before we get into ship counts and damage caps — I want to reframe why these definitions matter *to me specifically*.

Raid scale is not a balance question. It's a **visual drama question.** The SimCopter payoff — the thing that makes this game different from every 2D top-down colony builder — is banking over your settlement from altitude and *seeing what you built.* Raids are the threat that makes that view mean something.

So here's the framing I want us to hold while we define these tiers:

**Harassment-scale** should be something you can handle solo from the cockpit. You enter atmosphere, you see two or three bogeys inbound, and the engagement is a dogfight with stakes — a building takes a hit, maybe two. You feel competent. You feel like Hornet. Your settlement survives with a scar.

**Assault-scale** should make you break a sweat. Multiple attack vectors. You can't intercept everything. Some buildings *will* take damage. The question from altitude is triage: which wave do you chase, what do you sacrifice? That's the SimCopter payoff under pressure — watching your City take damage while you decide.

Tier regression is where it gets spicy. If a Settlement can actually drop back to Outpost from sustained assault, that moment needs to be *visible from altitude.* Not just a stat. A physical change in the geometry you're flying over.

So: what does assault-scale look like from 500 meters up? That's my agenda question before we lock ship counts.

### Ren (emergence systems theorist)

Max's framing is right but incomplete. Visual drama is the *output*. The input is what generates raids the designer didn't author.

Here's what I want to protect: **raid scale should be a function of standing depth, not a authored category.** If harassment and assault are fixed tiers we spawn deliberately, we've scripted the thing that should emerge. The emergence chain is: faction standing depth → raid composition algorithm → what you see from altitude. The designer shouldn't be choosing "harassment today" — the standing system should be generating it.

Concrete proposal: raid ship count scales continuously with standing value in the Hostile band. At the floor boundary you get 2–3 ships (Max's dogfight). At standing zero you get 6–8 with split attack vectors. No discrete tiers, just a count formula reading from `standing_value`. That means every settlement under different standing histories looks different from altitude — situations the designer never authored.

Building damage cap: I'd resist per-tier damage caps entirely. Damage accumulates, and tier regression happens when accumulated damage crosses a structural threshold. That threshold is emergent from *what you didn't intercept*, not a designer decision. Tier regression becomes visible from altitude because geometry changes — that's Max's payoff, but it fires from player choices, not authored set pieces.

The one flag: if we define assault-scale as a *spawn category* rather than a *standing readout*, we've broken the emergence chain. Faction standing → raid composition must be a continuous read, not a lookup table with three rows.

What does the standing-to-count formula look like? That's the actual blocking question.

## Round: CRITIQUE

### Vera (EV systems historian)

**Vera**

Both proposals have a source problem. Let me place them against what we know worked.

EV Nova's raids weren't continuous standing readouts. They were authored fleet compositions tied to specific standing thresholds — *because the player needed to recognize the raid type before committing to an intercept vector.* Ren's continuous formula is elegant on paper and unreadable in a cockpit. A player at 500 meters doesn't experience "standing 23 maps to 4.7 ships." They experience: *I can handle this* or *I cannot handle this.* That's a binary read, made in two seconds, based on visible fleet geometry. Continuous scaling destroys the read.

Max's discrete tiers are historically correct but he's conflated two separate questions. Raid scale and tier regression eligibility are not the same system. EV never gated planetary tier on raid outcome — it gated story progression on mission completion. If we tie tier regression to damage accumulation from raids, we've created a slow-drain mechanic that punishes players for not being online. That's not EV. That's an MMO.

The actual blocking question isn't the count formula. It's this: **what is the minimum visible fleet geometry that communicates "you are outmatched" from altitude?**

In 2D that's trivial — count the dots. In 3D atmospheric at 500 meters, spread matters more than count. Three ships on converging vectors reads as an assault. Six ships in a loose column reads manageable.

Before we define ship count ceilings, we need to decide what fleet geometry the player is reading. Everything else follows from that.

### Nadia (new-player experience advocate)

**Nadia**

Vera's geometry question is the right one, and I want to push it one layer further: the geometry doesn't just need to communicate *threat level* — it needs to communicate *what to do next*. A new player at 500 meters has maybe three seconds before they're committed to an intercept vector. If the read fails, they fly the wrong direction, lose a building, and don't understand why. That's not a skill failure. That's a feedback failure.

So I'll endorse two discrete compositions over Ren's continuous formula — but not because of EV precedent. Because **Ren's formula is invisible**. Standing 23 → 4.7 ships is a spreadsheet. Two converging bogeys versus four split-vector attackers is a *feeling*. Players learn feelings. They don't learn formulas.

Where Ren is right: the *threshold* for which composition spawns should be standing-driven, not authored-per-session. Harassment below a certain standing depth, assault below a lower one. The designer never picks "harassment today" — the standing system generates it. That's the emergence chain intact, just discretized at the output layer instead of the input layer.

One flag nobody's raised: **first-raid legibility**. The very first raid a new player sees sets the template for everything that follows. If it arrives before they understand what their settlement looks like from altitude — before they've had a clean SimCopter moment — it reads as punishment, not drama.

Is there a first-raid protection window? That's blocking for me before ship counts matter at all.

## Round: EVALUATE

### Soren (solo dev scope warden)

**Soren**

Before ship counts: there's a scope bomb embedded in Max's framing that nobody's named.

"Tier regression needs to be *visible from altitude* — a physical change in the geometry you're flying over."

That's not a standing system question. That's a settlement geometry question. If a Settlement can visually revert to Outpost state, every building type needs at least two geometry states — erected and degraded — and the transition needs to be legible from 500 meters in flat-poly. Multiply that by however many building types ship at M7. That asset work can easily double the settlement art pass.

I'll flag it and set it aside, because it may be worth it. But it needs a cost acknowledgment before M8 scope estimation is meaningful.

On the actual blocking question — I'll take Nadia's position plus one constraint.

Two discrete compositions is the right call. Not for EV precedent reasons. For testability reasons. A continuous formula gives you infinite raid states to balance, none of which you can reliably reproduce during testing. Two compositions — harassment, assault — give you two test cases. You can verify each in isolation, tune each independently, and know exactly what you shipped.

The standing threshold that determines which spawns is a config value. Two numbers. Tunable from playtest data.

What I need defined before offline raid logic is scoped:

1. Does tier regression from raid damage ship in M5, M7, or M8?
2. How many building types exist at M7 settlement tier, and do they have degraded states?

Everything else follows from those two answers.

<!-- complete -->
