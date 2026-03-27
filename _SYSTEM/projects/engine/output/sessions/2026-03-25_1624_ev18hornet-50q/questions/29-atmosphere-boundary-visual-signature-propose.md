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


<!-- complete -->
