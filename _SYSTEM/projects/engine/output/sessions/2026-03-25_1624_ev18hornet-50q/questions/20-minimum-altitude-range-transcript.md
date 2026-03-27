# Transcript: Minimum Altitude Range

*Generated: 2026-03-25 17:36*

## Round: PROPOSE

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

## Round: CRITIQUE

### Vera (EV systems historian)

Before anyone commits numbers, I want to flag what's happening in these proposals: both Max and Ren are designing for the *full* atmospheric experience. Max wants three feel-states. Ren wants standing to express spatially across the entire column. Those are good instincts but they're M8 instincts dressed as M-current constraints.

EV's spatial legibility worked because it asked one question per moment: *is that ship hostile, neutral, or friendly?* The 2D top-down view answered that question with color and vector at a glance. No altitude band reasoning required.

The atmospheric layer is new. We do not yet know what the minimum viable column needs to deliver. Before specifying entry altitude and deck, the group should answer a prior question: **what is the atmospheric layer required to prove at the milestone where it ships?**

If the answer is "FA-18 Hornet flight feel over authored terrain," the column is sized by flight dynamics — bank angle, roll response, low-pass sensation. Those are testable with a 500m range or a 5000m range.

If the answer is "standing consequences express as spatial pressure," that's a faction system integration problem, not a flight model problem.

Committing entry altitude to 2000m before the Hornet Layer milestone has been played is the same mistake as specifying `HOSTILE_FLOOR` before M5 playtest data. The config constant approach was right for standing thresholds. It should be right here too.

My question for the group: **what does the atmospheric column need to prove at first ship, and is that requirement different from what it needs to sustain at M8?** Size the column for the former, not the latter.

### Nadia (new-player experience advocate)

Vera's structural point is correct — and I want to name *why* it matters for new players specifically.

A first-time atmospheric descent is the moment this game proves it's not just a galaxy map with extra steps. The player has been in space. Now they're going *somewhere*. That descent is the fantasy delivery — "I am landing on a planet I have a relationship with." If it doesn't feel like arrival, the whole three-layer premise collapses for them before they understand what they're even inside.

Max's three feel-states are real, but they're *discovered* states, not explained ones. A new player won't parse "this is the intercept band" — they'll just feel tension, or not. The column has to be deep enough that descent *takes time*, that the view transforms, that they pass through something. That's not a number. That's a pacing requirement.

Ren's standing-as-spatial-pressure argument is the right *eventual* design but Vera is right that wiring it to specific altitudes before playtest is premature.

The one concrete anchor I'd defend: **the deck must be below building roofline.** Not because of faction systems — because otherwise a new player who just built their first shelter cannot see their own shelter from *inside* their own settlement. The SimCopter moment doesn't happen if you're always looking *down at* your build like a map. You need to be able to fly *through* it.

That's not an M8 concern. That's session one.

Everything else — entry altitude, intercept band depth — size those after the Hornet Layer milestone tells us what the flight model actually wants.

## Round: EVALUATE

### Soren (solo dev scope warden)

The altitude range is a config constant. The systems that run at each altitude band are the build cost. The group is solving the wrong problem first.

Vera and Nadia are right on sequencing. But I want to add the build-cost framing they're missing.

Here's what actually costs time in the atmospheric column:

**Entry altitude:** one float. Costs nothing. Change it twelve times after playtest.

**Floor altitude:** same. One float.

**What costs time is the systems you wire to each band.** Patrol spawn logic at intercept altitude — that's a build item. Convergent approach vectors keyed to faction standing — build item. LOD transitions as altitude changes — build item depending on terrain complexity.

Vera's question ("what does the column need to prove at first ship?") is the scope sequencing question. My answer: **one thing.** At Hornet Layer, the column needs to prove the flight model is fun between two altitude bounds. That's it. No faction pressure. No standing reads. No three feel-states. Those come after you know the flight model earns its keep.

The one constraint I'll second from Nadia: **deck below roofline is a day-one build requirement**, not because of feel-states but because building height determines your terrain geometry, your collision surfaces, and your low-pass camera behavior. You cannot retrospectively lower the floor without touching those systems. That number needs to exist before the first building mesh is authored.

Everything else: config constants, sized after the Hornet Layer milestone plays.

Name the deck. Defer the rest.

<!-- complete -->
