# Transcript: Space Layer: 2D or 3D?

*Generated: 2026-03-25 15:31*

## Round: PROPOSE

### Max (atmospheric flight advocate)

Here's the uncomfortable truth nobody's saying: **this question is actually about protecting the atmospheric layer.**

If space goes 3D, you've got two 3D flight modes in the same game. Players will compare them. And the moment someone asks "why does space flight feel worse than atmosphere?"—you've got a problem. Because it *will* feel worse. Space is big, empty, and navigational. Atmosphere is tight, tactile, and visceral. They're doing completely different jobs.

**2D space is a gift to the atmospheric layer.** The mode shift isn't a compromise—it's *contrast*. You're on the galaxy map, making strategic decisions in a flat EV-style overhead view, and then you punch into atmosphere and suddenly the world has *depth*. That dimensional drop is the payoff. That's when the mouse flight takes over and the bank-and-roll earns its keep.

The risk with 3D space isn't scope—it's dilution. You'd spend milestone time making space flight *feel okay*, when okay is never going to compete with Hornet-mode over a polygon mountain range you built yourself.

The SimCopter moment—circling your settlement from altitude, watching your colony laid out below you—only hits if the atmospheric layer is the place where dimensionality *lives*. If space is already 3D, you've handed that feeling away before the player even lands.

My vote: 2D space, EV-faithful, top-down with the classic feel. Let the atmospheric layer own three dimensions completely.

What are we protecting here—consistency, or *contrast*?

### Ren (emergence systems theorist)

Max's contrast argument is aesthetically clean. But it's solving for feel, not for the emergence chain.

The chain this game lives or dies by: faction standing → raids → atmospheric defense → on-foot combat. That chain has to be one continuous mechanical situation, not three separate mode-switches.

Here's what 2D space does to that chain: a raid becomes a *notification*. Fleet spotted on the map. You intercept on a flat grid, or you don't, and then the game hands off to atmosphere. The raid is an authored event with a geographic outcome.

Here's what shallow 3D space with arcade physics does: a hostile fleet drops out of warp *above your planet*. You're already in three-dimensional space. You're outnumbered. You dive toward atmosphere using the planet as cover, and now the atmospheric layer isn't a contrast experience — it's an escape vector. The terrain you built matters because you know where the tight canyon is. The settlement you can't let them reach is visible below you. That's an emergent situation the designer didn't author.

I'm not arguing for Newtonian drift or Elite-style 6DOF. That's a different game. I'm arguing that the space layer's geometry should feed situations into the layers below it — and flat 2D space with a mode-shift at the atmosphere boundary makes that handoff scripted by necessity.

The contrast Max describes is real. But contrast that costs you the emergence chain is the wrong trade.

What if space is *shallow* 3D — vertical range enough for the dive mechanic, not a full starfield sim?

## Round: CRITIQUE

### Nadia (new-player experience advocate)

Both proposals are solving for *experienced* players.

Max's contrast argument assumes players recognize the mode-shift as intentional design. Ren's emergence chain assumes players understand that staying near the planet matters during a raid. Neither assumption is safe in the first session.

Here's the moment I'm protecting: a new player leaves atmosphere for the first time. What do they see? What tells them what space *is* — what it's for, what's dangerous, what they should want? Because in flat-poly with no textures, space has almost nothing to read. 2D space risks feeling like a loading screen that stayed. 3D space risks feeling like they broke something.

Ren's "dive toward atmosphere" scenario is genuinely exciting. But that moment only *lands* if the player already has a model of the geometry — planet below, hostile fleet above, canyon they know because they built it. A first-session player has none of that context. The emergent situation becomes noise they can't decode.

My flag: **the space layer needs a legibility win before it earns complexity.** Whether 2D or shallow 3D, players need to understand within their first minute in space: *here is where I am, here is what threatens me, here is what I'm navigating toward.*

Ren's shallow 3D is the right direction — but only if the vertical geometry is *readable*. Planet disc clearly below. Enemy approach vector obvious. The dive is intuitive, not discovered by accident.

What does the flat-poly aesthetic do in space to make threat geometry legible to someone with zero EV context?

### Vera (EV systems historian)

Nadia landed the right question. I want to pressure-test the answers.

Ren's shallow 3D is the proposal I'm most skeptical of — not because the emergence scenario is wrong, but because **shallow 3D is an architecture nobody has shipped cleanly.** EV worked because the space layer had a solved readability problem: everything was on one plane, threat geometry was always visible, you never had to rotate your camera to find what was killing you. The moment you add a vertical axis — even a shallow one — you've created a legibility debt. Now you need visual cues for altitude, approach angle, and relative elevation. That's design work Ren's proposal is skipping over.

The dive-toward-atmosphere scenario is genuinely exciting. It also requires the player to correctly read three spatial relationships simultaneously in a flat-poly environment with no textures. Nadia already flagged this. I'll add: EV's raid system *worked* because the threat appeared on your nav map and you understood it instantly. That's not a limitation of 2D — that's 2D doing its job.

Max's contrast argument holds up historically. EV's galaxy map was a strategic layer, not an immersive one. Players didn't mourn the lack of 3D space — they used the map to make decisions, then executed. The dimensionality payoff came from dropping into a system, not from the travel itself.

My read: shallow 3D solves an emergence problem that EV's 2D didn't actually have, while creating a legibility problem that 2D never did. That's a bad trade until someone shows me the readable flat-poly vertical combat system that justifies it.

## Round: EVALUATE

### Soren (solo dev scope warden)

**Nobody has priced Ren's proposal.**

"Shallow 3D" is not a defined thing. It's a direction, not a deliverable. Before this discussion moves toward consensus on shallow 3D, someone needs to answer: what is the vertical range, what controls camera orientation, and how does targeting work when enemies can be above or below your current view plane? Each of those is a design problem that spawns a build problem.

Here's the scope delta between the two options:

**2D space:** You have EV as a complete reference. Nav map, faction intercepts, system travel — all solved problems with known interaction patterns. Build time is bounded because the design space is bounded.

**Shallow 3D space:** You are inventing a hybrid that nobody has shipped cleanly (Vera's words, and she's right). You need: a camera system that reads altitude without textures, a targeting reticle that communicates 3D position in flat-poly, and physics tuning that makes "shallow" feel intentional rather than broken. That's not three tasks — that's three systems with unknown edge cases.

The dive-toward-atmosphere scenario Ren describes is genuinely exciting. It is also a late-game moment that requires 20+ hours of player context to land. You cannot build toward that moment in milestone three.

My read: **2D space is the correct milestone-three decision.** Not because the emergence argument is wrong — but because shallow 3D is scope you cannot estimate, and unestimated scope on a solo project is how the game stops shipping.

Build the 2D space that works. Revisit vertical geometry after the core loop is fun.

<!-- complete -->
