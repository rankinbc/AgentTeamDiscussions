### Max (atmospheric flight advocate)

The 500-meter figure has been haunting this design for several discussions now — it keeps appearing as the legibility threshold for degraded building states. That number is doing double duty as an implicit design constraint, and we should name that before we pick a range.

Here's what I want the group to actually solve: **the atmospheric layer needs three distinct feel-states on descent, not just an entry point and a floor.** That's the Hornet DNA. High altitude is the overview moment — SimCopter payoff, your settlement laid out below you, scale legible. Mid altitude is where intercepts happen — patrol geometry, threat reading, that specific Hornet sensation of something converging on your six. Low altitude is where banking over terrain earns its keep — below the ridgelines, below building height, pure kinesthetic.

The minimum altitude range question is really asking: how much vertical space do those three states require?

My stake in the ground before we hear from others: **the floor cannot be above building height.** If you can't drop below your own shelter roofline on a low pass, the SimCopter payoff is a postcard, not a place. And the intercept zone — the contested middle — needs enough depth that a player can react and maneuver, not just fly through it.

Concrete question I want answered today: what is the **entry altitude** and what is the **minimum deck**, expressed as actual numbers, with enough separation that all three feel-states have room to breathe?

That's the agenda. Let's scope the column before we scope the floor.

### Ren (emergence systems theorist)

Max's three-band framing is right, but I want to restate it as a systems problem rather than a feel problem — because the altitude column is where faction standing materializes as spatial pressure.

The intercept zone isn't just where patrols appear. It's where `RAID_HARASSMENT_THRESHOLD` and `RAID_ASSAULT_THRESHOLD` express as geometry. A player with Degraded standing should feel that difference in the column, not just read it in a tooltip. If the intercept band is too thin, the standing system works in isolation — the numbers change but the airspace doesn't.

We have one decided anchor: the atmospheric entry point is already the escort hold altitude. That's the top of the column. It's also the chokepoint where raid intercept vectors converge. Everything else derives from that.

The 500m figure keeps appearing as the degraded-building legibility threshold. If that's the floor of the high-altitude overview band, it's also the ceiling of the intercept zone. That compresses the intercept band unless entry is set significantly higher — I'd argue entry needs to be at least 3–4x the legibility threshold or the intercept zone has no reaction depth.

Concrete stake: entry altitude should be no lower than **2000m** game-units (or equivalent in Godot world-space). Floor at **below building roofline** as Max says. That gives the intercept band from ~100m to ~1500m — enough vertical space for converging patrol geometry to register as a direction before it becomes a collision.

The numbers aren't arbitrary. They're sized by the standing system's need to express spatially.


<!-- complete -->
