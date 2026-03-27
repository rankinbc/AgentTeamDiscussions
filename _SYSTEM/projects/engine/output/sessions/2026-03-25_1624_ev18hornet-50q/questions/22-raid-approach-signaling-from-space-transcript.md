# Transcript: Raid Approach Signaling from Space

*Generated: 2026-03-25 17:44*

## Round: PROPOSE

### Max (atmospheric flight advocate)

The question sounds like a UI problem — icon, timer, threat bracket — but it's actually a pull problem. If the signal reads as "raid incoming, wait to see if your stuff survives," we've built a spectator system. The atmospheric layer stays empty and the settlement feels like a progress bar someone else is attacking.

The real question is: does the signal make the player *want to dive*?

For a new player who has never flown an atmospheric raid defense, the inter-layer threat model only becomes legible the moment they commit to descent and see their own settlement from 500 meters. That's the SimCopter payoff — it's also the first time the stakes are felt rather than read off a HUD. Until they've done that once, no amount of approach-time accuracy makes the threat model land.

So what I want the group to resolve isn't "how many seconds of warning" — it's whether the approach signal is designed to pull players into the atmospheric layer or to manage anxiety about it from a safe distance.

Specific questions I'd put on the table:

**One:** Does the approach signal resolve entirely in the galaxy layer, or does it require atmospheric entry to get precise information? Vagueness that rewards descent is a design tool, not a deficiency.

**Two:** What is the minimum signal that creates urgency without giving players a reason to hover in space and wait?

**Three:** Does the first-raid protection flag interact with the signal — or does a new player see the full threat model before they've had a clean descent?

That's where I'd start.

### Ren (emergence systems theorist)

Max has correctly identified the pull problem. I want to add the systems dimension.

The risk isn't just that the signal becomes a spectator mechanic — it's that a purpose-built approach signal is authored content masquerading as emergent information. If we ship a discrete "raid incoming" notification, we've created a scripted event at exactly the point where the faction standing system should be doing that work.

Consider what information already exists: patrol density responds to standing band. A player who has been tracking standing has been watching patrol behavior change. The raid isn't a surprise arrival — it's a standing consequence that the galaxy layer has been telegraphing through patrol geometry the entire time. The approach "signal" should be the patrol state becoming unambiguous, not a new notification system.

This answers Max's second question differently: the minimum signal is *no new system*. Hostile band patrol density, already decided as an M8 atmospheric texture problem, is the raid warning. The player who has been reading patrol behavior knows. The player who hasn't will learn at cost — which is the correct emergence mechanic.

On the first-raid protection flag: it should interact. A player who hasn't had clean atmospheric view hasn't built the mental model that makes approach signals meaningful. The protection window isn't just preventing unfair loss — it's preventing the signal from firing before the player can interpret it. Showing the full threat model to someone who has never seen their settlement from altitude teaches nothing.

Max's vagueness point stands. Descent should be the information-gathering act, not an alternative to it.

## Round: CRITIQUE

### Vera (EV systems historian)

The discussion is treating this as a notification design problem. It isn't. It's a visibility problem — and EV solved it without notifications.

In EV Nova, you didn't need a raid warning system because the 2D system map showed you what was there. Fleet composition visible at a glance. Hostile ships in your system weren't announced — they were *present*, readable, on the same plane as everything else. The threat was diegetic. The map was the signal.

What's being proposed here is an approach warning because the atmospheric layer hides settlement state from the galaxy map. That's the real issue. The three-layer architecture creates an information gap that didn't exist in EV, and both Max and Ren are designing around the symptom rather than naming the cause.

Before any signal architecture is specified, I'd want the group to answer: what does the galaxy map *show* when your settlement is under raid threat? If the answer is "nothing without a purpose-built warning," then the EV heritage has already been compromised at the architecture level, and no signal design recovers it.

Ren's patrol density solution inherits the same problem — patrol behavior is atmospheric layer information. A player on the galaxy map can't read atmospheric patrol density. The signal that should be doing the work isn't accessible from the layer the player is in.

The first question isn't how to warn players. It's whether the galaxy map surface can make settlement threat *visible* in the same way EV made system threat visible — before we design anything that substitutes for that visibility.

### Nadia (new-player experience advocate)

Vera's diagnosis is right and it's the one I'd been waiting for someone to name. The information gap isn't a notification problem — it's an architecture problem. And it surfaces a new-player journey issue none of the proposals fully address.

Here's what concerns me: even if the galaxy map *shows* raid threat diegetically, a new player doesn't yet know what they're looking at. They haven't seen their settlement from 500 meters. They don't have the mental model that makes "three hostile signatures near your planet" feel like urgency rather than ambient noise. The signal can be perfectly visible and completely unreadable.

Max's pull problem is real, but the solution isn't signal timing — it's that the *first* raid defense needs to be the moment that teaches the whole system. The player descends, sees their buildings, watches a raid vector approach, and suddenly every subsequent signal becomes legible in retrospect. That's the teaching moment you can't skip.

Which means Ren's "no new system" answer is correct for players who've had their first clean descent. But for players who haven't, we need to ask: what pulls them *into* the layer before they understand why it matters?

My flag: if the first-raid protection window suppresses the signal entirely, new players may never be *invited* to descend and build that mental model. The protection window should suppress *damage*, not the approach signal itself. Let them see the threat. Let them choose to respond. The first dive should feel earned, not accidental.

## Round: EVALUATE

### Soren (solo dev scope warden)

The discussion has four speakers and zero build estimates. Before this group designs a signal architecture, it needs to know what already exists on the galaxy map that's free to repurpose.

Vera's diagnosis is correct but her question isn't scoped. "Can the galaxy map show settlement threat diegetically?" has three possible answers with very different build costs:

**A.** Faction ship presence near your planet is already visible on the galaxy map as part of the base layer — repurpose it. Cost: authoring a visual read state, maybe two days.

**B.** Faction ship presence exists in simulation but isn't surfaced on the map — add a read path and icon state. Cost: one to three days depending on data proximity.

**C.** Faction ship presence near your planet isn't modeled at all until atmospheric entry — this is a new system. Cost: unknown, but it's not a notification problem anymore.

That answer gates everything else in this discussion. Ren's "no new system" argument only holds if option A is true. Max's pull problem is only a design question if the baseline signal exists and we're tuning it. Nadia's new-player concern is only actionable if we know what the player actually sees before descent.

My agenda proposal: answer the galaxy map question first. What does the layer currently show, and what does it cost to make threat legible there? Then we can talk about pull mechanics, protection window behavior, and first-raid teaching moments — in that order, not before.

What's already on the map?

<!-- complete -->
