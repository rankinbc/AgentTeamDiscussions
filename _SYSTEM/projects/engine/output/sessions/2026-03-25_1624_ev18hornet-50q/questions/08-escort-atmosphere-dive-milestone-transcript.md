# Transcript: Escort Atmosphere Dive Milestone

*Generated: 2026-03-25 16:49*

## Round: PROPOSE

### Max (atmospheric flight advocate)

The atmosphere dive is not an extension of 2D escort AI. It is a completely different problem, and conflating them for "context switching" efficiency is how you get escorts that technically follow you into atmosphere and feel completely wrong doing it.

Here's what the dive actually requires: the escort needs to read your bank angle, anticipate your roll, maintain offset through a 3D flight envelope where speed, altitude, and turn radius all interact. That is not a galaxy-map formation problem. Galaxy-layer AI proves offset following works in flat space. It tells you nothing about whether an escort can stay in position when you're pulling 60 degrees of bank over a ridge at low altitude.

My position: **M8, same as already decided, and for the right reasons.**

But here's what I want the team to lock down that nobody has said clearly yet — the M6 hold behavior cannot feel like a failure state. When the player dives into atmosphere and the escort orbits at the entry point, that moment needs to read as *"my escort is waiting for me"* not *"the AI broke."* The visual treatment of the hold is a flight feel problem, not an architecture problem. A stationary hover feels wrong at altitude. A flat circle orbit looks fine on a map and looks stupid in the cockpit view. 

That's the M6 work I care about: making the holdback *legible and atmospheric*, not just functional.

The dive earns its scope when we have solo atmospheric feel data to tune against. M8 is the right gate. But M6 hold behavior needs a real UX decision before it ships.

### Ren (emergence systems theorist)

Max is right, and the reasoning holds. But I want to add a layer he didn't name.

The escort's hold position at atmospheric entry altitude is not incidentally where raids appear — it's the same geometric chokepoint. Faction intercepts arrive from orbit, push through the entry vector, and engage the settlement below. An escort holding at that altitude is already positioned at the interception point. That's not a UX detail. That's the emergence chain showing its structure before we've designed it.

This means M6 hold behavior has a hidden mechanical implication: **what happens when a raid spawns while your escort is holding orbit at entry altitude?** The player is in atmosphere. The escort is at the entry point. The raiding fleet exits FTL into the same space. Does the escort engage? Does it get destroyed before the player surfaces? Does the player return to a debris field and a different tactical situation than the one they left?

None of this requires us to ship contested airspace geometry in M6. But it means the hold behavior needs to be written as a *state*, not a *pose*. "Hold at entry altitude" must be interruptible by faction threat detection using the same standing reads that drive raid spawns. Otherwise M6 hard-codes a passive escort that M8 will have to tear out.

Max's legibility concern is valid and real. My addition: legibility is downstream of the hold being a live mechanical participant in the faction space, not a frozen animation waiting for the player to resurface.

M8 for the dive. M6 hold must be threat-aware from day one.

## Round: CRITIQUE

### Vera (EV systems historian)

EV didn't have atmospheric layer transitions. That's not an oversight — it's why escorts in EV *worked*. Every escort stayed in the same 2D envelope as the player, faction affiliation was always legible, and the relationship between standing and escort behavior was traceable at a glance. The system had no seams because there was only one space.

This game is introducing a seam EV never had. That's not a problem — the three-layer architecture is a deliberate extension. But when you extend a system that worked because of its flatness, you need to be precise about which properties you're preserving and which you're deliberately discarding.

What EV gave you with escorts: **consequence legibility**. You knew whose ship was flying with you, you knew what it meant for your standing if they died or defected, and you knew the faction had eyes on you. That chain was readable.

Ren's threat-aware hold point is the only thing in this discussion that actually protects that legibility at the seam. A frozen escort at entry altitude that ignores a raid spawning around it breaks the standing chain — the player surfaces to debris and has no authored way to understand what happened to their consequence structure.

M8 for the dive is correct and already decided. I'm not relitigating that.

What I'm flagging: the hold behavior cannot be implemented as a pose. It must be a state that reads faction standing data. If it doesn't, you're not deferring atmospheric escorts to M8 — you're silently breaking the standing system's traceability at the layer boundary and discovering that breakage at M8 when it's expensive to fix.

### Nadia (new-player experience advocate)

Max named the feeling problem. Ren named the mechanical one. Vera named the EV precedent. I want to name what happens to a first-time player at that moment.

The atmospheric dive is going to be one of the most memorable moments in the first session. Player descends, the horizon bends, the flat-poly terrain rushes up — that's the fantasy payoff the whole early game is building toward. If the escort does something that reads as *broken* at exactly that moment, you've poisoned the memory of your best feature.

But here's what concerns me more than the visual treatment of the hold: **new players have no prior context for why an escort would wait at altitude.** EV players will infer it. First-timers won't. They'll think it's a bug, finish the dive, surface to either a waiting escort or a debris field, and have no authored explanation for either outcome.

That means the hold behavior needs *a single legible moment* — not a tutorial, not a tooltip wall — just one thing that signals "your escort is holding position" before the player crosses the entry boundary. A comms line. A brief visual acknowledgment. Something that converts "AI froze" into "they're waiting for me."

Ren's threat-aware state requirement is correct. I'm adding: that state needs a communication surface toward the player, however minimal. A frozen hold that silently gets destroyed by a raid while the player is underground is not just an M8 problem — it's a first-impression problem that will read as jank to anyone who didn't already trust the system.

M8 for the dive. M6 hold needs a voice.

## Round: EVALUATE

### Soren (solo dev scope warden)

The dive milestone isn't the open question. M8 is already decided and this discussion didn't move it. What this discussion *did* do is add scope to M6 hold behavior, and that's what needs a cost attached before it gets committed.

Tally what's now on M6 hold behavior:

- Layer-transition detection
- Hold state (not pose) with interruptibility
- Faction standing reads from inside the hold state
- Raid threat detection during hold
- A player-facing communication surface (comms line or equivalent)

Each of those is a discrete build item. Ren's "threat-aware from day one" is the one I'd watch — it's the right architecture call, but "threat-aware" starts touching raid spawn logic, faction standing reads, and AI state interruption in a milestone that was supposed to validate galaxy-layer formation feel. That's M6 reaching into M7 and M8 systems to do it correctly.

My read: the communication surface (Nadia's comms line) is cheap and eliminates the first-impression problem. A single string on layer entry — "holding at altitude" — is an afternoon. Ship that.

The threat-aware hold state is the right answer architecturally, but it needs a build estimate before it's committed to M6. "Hold state that reads faction standing" is not the same cost as "hold pose." If that estimate comes back at more than 3 days, it belongs in M7 as a named item, not as an implicit M6 requirement that grows in place.

What's the current M6 scope list? That's the number this conversation needs before it can close.

<!-- complete -->
