# Transcript: Hostile vs. Friendly Atmosphere Signal

*Generated: 2026-03-25 18:21*

## Round: PROPOSE

### Max (atmospheric flight advocate)

The signal problem is real, but I want to name the trap before we design into it: **if we solve this too well, we make the atmosphere optional.**

Right now the open question from Q22 — galaxy map option A/B/C for non-starting systems — is technically unresolved. But the more interesting question underneath it is: *what should the player NOT be able to know from space?*

The static ring from Q29 gives spatial confirmation — inside/outside, threshold marked. That's correct and ships cheap. But a ring that color-shifts by faction standing is a different thing: it's a dashboard. It lets you orbit at safe altitude reading threat state without committing your hull to the approach vector. That's not Hornet. That's Kerbal mission planner.

My position: **the approach is the information.** You dive, you read the intercept geometry, you feel whether the patrol spacing is loose or tight. That's the kinesthetic standing readout we decided on back in Q10 — modified patrol approach vectors as atmospheric tell. The galaxy layer should show *that something is there.* How hostile? Go find out.

The specific open question I want to set: does the galaxy map signal for non-starting systems need to be faction-identified, or is faction-neutral threat presence (ships on map, no affiliation shown) the correct fidelity ceiling? Because faction-identified from orbit is Option B+ work, and it might be solving a problem that the dive itself already solves better.

What does the descent *feel like* when you're flying into hostile space versus friendly? That's where I want to land.

### Ren (emergence systems theorist)

Max is right about the trap, but I want to sharpen the systems framing.

The issue isn't information quantity — it's information *source*. There are two possible architectures here:

**Architecture A:** The galaxy map reads atmosphere and reports faction state to the player. Standing system and galaxy signal are parallel outputs. They work independently.

**Architecture B:** The player's standing ledger IS the galaxy signal. You know your Confederation standing is 28. You know that system is Confederation. You know what you're flying into. The approach confirms what your choices already told you.

Architecture B is where cross-layer interaction actually lives. Your faction history — accumulated across The Bar, missions, hull captures, combat — becomes your atmospheric intelligence. The standing system doesn't just produce raids; it produces *knowledge*. That's the chain we want: past choices → standing → approach read → intercept geometry → dirtside consequences.

Architecture A breaks that chain. If the map tells you faction ownership independent of your standing, you're reading a HUD, not your history. The approach becomes confirmation of information you already had for free.

For non-starting systems: faction-neutral ship presence on the map is the correct ceiling. Max is right that faction-identified from orbit is solving a problem the dive solves better. But the reason it's correct isn't aesthetic — it's that faction identification from orbit would let players route around their standing history instead of confronting it.

One flag: this only works if the standing UI is readable. Players need to be able to cross-reference "my Confederation standing is X" against "I'm approaching a Confederation system." If that cross-reference requires menu diving, the elegant architecture becomes an obscure one.

## Round: CRITIQUE

### Vera (EV systems historian)

EV Nova solved this without a signal layer at all. You knew a system was hostile because you'd been there, talked to people, read the mission text, and watched your standing bar move. The galaxy map showed ship presence. That was sufficient — not because players had complete information, but because the cost of being wrong was recoverable.

The trap both Max and Ren are circling isn't signal fidelity. It's **the standing tooltip carrying load it wasn't designed for.**

Look at what's been decided: the tooltip fires once per faction at 40 crossing. It names the system, shows the value, describes what standing affects. That's the cross-reference surface Ren identifies as necessary. Players who've been running Confederation missions know their Confederation standing is degraded — they've seen it move. The approaching-Confederation-system read is already in their head if the standing UI does its job.

The Q22 galaxy map question for non-starting systems is therefore answerable from prior decisions: **faction ship presence on the map (Option A or B depending on system) is the correct ceiling, and faction identification from orbit is unnecessary overhead** — not because it's aesthetically wrong but because it duplicates information the standing ledger already contains for any player who's engaged the faction.

The flag I want placed: if a player has *never interacted* with a faction, their standing is at default (50, presumably), they have no tooltip history with that faction, and they approach an unknown system. What does faction-neutral ship presence on the map actually tell them?

That's the new player onboarding gap. That's where the design problem actually lives.

### Nadia (new-player experience advocate)

Vera just named my problem exactly, and I want to push on it harder.

The elegant architecture — standing ledger as atmospheric intelligence — is beautiful for hour 20. For session one, it's invisible. A player approaching their second system has: default standing (wherever that starts), zero tooltip history with any faction they haven't touched yet, and "ships on map" as their only signal. That's not information. That's a dot.

The standing-as-intelligence chain only works if players **know they have a standing ledger that's worth reading.** The tooltip at 40 is the trigger that makes standing visible — but 40 requires prior faction engagement to reach. A player who flies cautiously, farms trade routes, avoids The Bar, can approach contested systems with standings that have silently been moving for sessions without ever crossing a tooltip threshold.

This is the scenario I'm flagging: **standing as intelligence assumes players are already inside the feedback loop.** The first dive into an unfamiliar system is often *before* the loop closes.

What would help: The Bar does work here that we're not fully crediting. If Bar contacts in Confederation space routinely name other systems — "Confederation patrols have been heavy in [system]," "Raiders have been hitting [system] transports" — that's diegetic faction identification that builds the mental model before the dive. It's not a map signal. It's the rumor surface doing onboarding.

The galaxy map ceiling stays at faction-neutral. But The Bar needs to close the gap Vera identified, or first-dive players are navigating blind.

## Round: EVALUATE

### Soren (solo dev scope warden)

Before we close Q22 on non-starting systems, I want to name what Nadia just proposed and make sure everyone heard it clearly: **Bar rumors as faction-identification onboarding surface.**

That's not a tweak to the comms intercept string. That's a rumor system with dynamic faction-state awareness, authored per-system, surfaced through Bar NPC dialogue. That's a content pipeline and a system. Nobody has estimated it. It's being floated as the solution to a UX gap *while* the galaxy map question is still open, which means we're about to design three overlapping solutions to the same problem.

The agenda question I want held before we proceed:

**What is the minimal information that closes the new-player gap Nadia identified — and what does building it actually cost?**

The options on the table right now, with rough cost:
- Static ship presence on galaxy map (Option A/B): 0–3 days depending on data proximity. Already in scope discussion.
- Standing UI readability improvement (Ren's cross-reference surface): unknown. Nobody has specified what the standing UI looks like or whether it's built yet.
- Bar rumors with system-specific faction content: 2–6 weeks of authored content plus system architecture. Not scoped. Not assigned a milestone.

Nadia's Bar solution might be correct. It's also potentially the most expensive thing proposed in this discussion.

The onboarding gap is real. The answer "Bar closes it" doesn't close the gap — it moves the problem to a build item we haven't acknowledged.

What does the standing UI currently look like, and is it readable without menu diving?

<!-- complete -->
