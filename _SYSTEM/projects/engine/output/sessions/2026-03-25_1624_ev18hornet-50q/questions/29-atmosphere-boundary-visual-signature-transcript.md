# Transcript: Atmosphere Boundary Visual Signature

*Generated: 2026-03-25 18:16*

## Round: PROPOSE

### Max (atmospheric flight advocate)

The boundary has to *land* — not fade in, not shimmer into existence. If it reads as a gradient it reads as a loading state. We need a hard geometric event.

Here's the frame I want to hold: the atmosphere boundary is a **color discontinuity**, not a volume. The sky polygon — the dome — changes color state at the altitude threshold. Below the entry altitude, sky is planet-hue. Above it, space-black. That's a one-float swap on a mesh that already exists. No new systems. Crossing it reads as crossing something real because the geometry *snaps*.

But color alone doesn't give you a *surface*. You need shape. The move I keep coming back to is a **ring of angled flat panels at entry altitude** — a sparse orbital shell in the same flat-poly language as everything else. Not solid, not a wall. Think a crown of eight or twelve beveled slabs, faction-colored, slowly rotating. From space, it marks the chokepoint. From inside atmosphere on ascent, it's your altitude reference and your exit signal. It's the diegetic sky marker question from Q21 — and it answers it *without* inventing a new system if it's authored as geometry at the same altitude as `ATMOSPHERIC_ENTRY_ALTITUDE`.

The agenda I want to set: **decide the sky dome color-snap first** (one line of code, resolves today), then scope the ring geometry as a separate authoring question with a day estimate. Those are two different decisions and they shouldn't block each other.

What's the planet sky hue? That determines everything downstream.

### Ren (emergence systems theorist)

Max's separation of the two decisions is correct and I'll enforce it harder: **dome snap is an implementation detail, ring geometry is a systems question.**

The dome color-snap requires no discussion. One float, one state change at `ATMOSPHERIC_ENTRY_ALTITUDE`. The sky is planet-hue below, space-black above. Done. Decide the planet hue palette offline.

The ring is where I want to slow down, because Max's framing buries the load-bearing question. He proposes "faction-colored" panels. That phrase is doing significant work.

If the ring is **statically authored** with a faction color, it's a landmark. Useful, low cost.

If the ring **reads live faction standing or patrol density**, it becomes an information surface — and it sits at the same altitude as escort hold points, raid spawn intercept vectors, and the layer transition chokepoint we've been designing for six questions. That's not a landmark. That's the emergence chain made visible.

The system interaction I want flagged: a player with degraded Confederation standing descending through a Confederation-colored ring should read differently than a player in good standing. The ring at entry altitude is structurally the same chokepoint as every raid spawn we've decided. If the ring can carry faction pressure information — color shift, rotation rate, panel count — then it's doing what the galaxy map threat visibility question has been struggling with since Q22. It's Option A: no new system, authoring cost only.

Before scoping the ring geometry, we need to decide: **static authored color or live faction read?** That answer changes the build estimate significantly.

## Round: CRITIQUE

### Vera (EV systems historian)

The dome snap is not a discussion item. Decide the planet hue palette, write the float swap, ship it. I won't spend words on it.

The ring is where I want to apply pressure, and it's not the static-versus-live question Ren is centering. That's a build cost question. The prior question is: **what problem is the ring solving, and did EV have that problem?**

In EV Nova, you always knew whose territory you were entering. System ownership was legible on the galaxy map before you ever plotted a hyperspace jump. Faction patrol presence was visible. You read Confederation space from Rebel space because the *map* told you, not because there was a diegetic landmark at the hyperspace arrival point. The faction information surface was the 2D layer itself.

This project added a third layer. That layer created an information gap the original never had — the Q22 blocking question. The ring-with-live-faction-read is being proposed as a solution to that gap. But if it works, you haven't resolved Q22. You've just moved the information surface from the galaxy map *to a piece of geometry at entry altitude* and called it emergence.

That's not emergence. That's a HUD made of polygons.

My position: resolve Q22 first. If galaxy map threat visibility is Option A — faction ship presence already base-layer renderable — then the ring is a *redundant* signal and the authoring question is whether redundancy earns the build cost.

If Q22 is still open, the ring is load-bearing infrastructure wearing a cosmetic hat. Name it correctly before scoping it.

### Nadia (new-player experience advocate)

Vera's question — what problem is the ring solving — is the right one, but I want to push it one step further toward the player sitting at session one.

The dome snap is correct. Ship it. But a color change on a sky polygon doesn't read as *arrival* — it reads as a state change in the engine. New players won't think "I crossed a surface." They'll think the sky loaded differently. The snap needs a shape event to make it felt.

Here's where I diverge from both Max and Ren: the ring's value to a new player isn't faction information. It's **spatial confirmation**. The player just did something with their mouse and the world transformed. The ring — even static, even faction-colored as a pure authoring choice — says *you're inside now*. The geometry marks an inside and an outside. That's the first thing atmosphere needs to communicate, before standing, before threat, before anything EV-adjacent.

Vera's critique lands differently for me: "HUD made of polygons" is only a problem if the player is being deceived about what they're looking at. Flat-poly doesn't deceive. The ring isn't pretending to be clouds. It's geometry saying *here is a threshold*. That's honest in the aesthetic language this game speaks.

On the static-versus-live question: **static first, always**. A new player who doesn't yet understand faction standing cannot read a color shift as threat information. Teach them what the ring means before you make it say something conditional.

Resolve Q22. Then scope the ring against what Q22 leaves unsolved for first-session players.

## Round: EVALUATE

### Soren (solo dev scope warden)

The dome snap is free. Sky hue below entry altitude, space-black above, one float on a mesh that already exists. Costs an afternoon including the config constant. Ship it without further discussion.

The ring is where I need the group to slow down, because the build estimate depends entirely on which version of the ring we're scoping.

**Static ring, no faction read:** 8–12 flat panels at a single altitude, one authored color. Single mesh, no runtime queries. Call it 2–3 days including placement and the rotation behavior. Cheap enough that the question is whether it earns its place in the milestone, not whether it's affordable.

**Live faction read:** Now the ring needs to query standing at render time, branch on standing band, and express that difference legibly — color, rotation speed, panel count, something. That's a shader or material swap path that doesn't exist, a standing read in a geometry context that hasn't been wired, and per-faction authored states for every faction that operates in atmosphere. Minimum 1–2 weeks. And it puts visual state on a system whose config constants have no numeric values yet.

Before the ring earns scope in either form, Vera's sequencing question has to close: **is Q22 resolved or not?** The starting system decision from Q27 put Confederation patrol presence on the galaxy map as Option A. If that's confirmed, the ring is redundant information. If Q22 is still open for other systems, the ring is load-bearing infrastructure.

What's the current Q22 status? That's my agenda question.

<!-- complete -->
