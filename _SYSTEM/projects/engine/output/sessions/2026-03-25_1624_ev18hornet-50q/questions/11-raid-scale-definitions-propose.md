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


<!-- complete -->
