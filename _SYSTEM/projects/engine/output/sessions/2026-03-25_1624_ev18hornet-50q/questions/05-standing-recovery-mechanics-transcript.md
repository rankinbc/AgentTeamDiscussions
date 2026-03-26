# Transcript: Standing Recovery Mechanics

*Generated: 2026-03-25 16:39*

## Round: PROPOSE

### Ren (emergence systems theorist)

Recovery is a design question with teeth, because it determines whether degraded standing is a reversible cost or a permanent branch.

**The core tension:** If recovery is cheap and standing-agnostic, then standing loss has no narrative weight — it's just a resource drain. If recovery is impossible, then the system punishes early experimentation and caps the player's ability to change direction. Neither extreme produces emergence.

**What I want to surface for this round:**

Recovery mechanics need to be consistent with how settlement tier regression works. If a settlement can regress and be rebuilt, standing should follow the same logic — painful, costly, but not a death sentence. The interesting design question is *what the cost structure reveals about the faction*.

My position: recovery should be **mission-gated primarily**, with credits as a secondary cost attached to those missions — not a standalone payment. Here's why: a faction that lets you buy your way back into standing is a faction that treats you as a resource. A faction that requires you to *prove something* has ideology. That asymmetry creates faction identity through mechanics, not lore text.

The emergent consequence worth examining: if standing recovery requires faction missions, and those missions have standing costs with rival factions, then recovery from one relationship *structurally damages* another. Players who degrade standing through passive negligence face a genuinely different recovery geometry than players who actively antagonized a faction.

**Questions for this round:**
1. Is recovery gated on standing floor, or available at any positive value?
2. Do recovery missions exist as a distinct mission type, or do they draw from the same mission pool?
3. Does recovery cost anything with rival factions?

### Max (atmospheric flight advocate)

Ren's got the logic right and I won't fight it. Mission-gated recovery with credits attached creates faction identity through mechanics — that's the right call.

But here's what nobody's said yet: **standing recovery has an atmospheric signature, and that signature is the feedback loop players will actually feel.**

Degraded standing doesn't just mean fewer missions available in The Bar. It means your airspace gets hotter. More faction patrols. Hostile intercept vectors tightening over your settlement. When you're coming in from orbit and your settlement is ringed by Confederation patrol geometry, you *know* you've burned something. You don't need a tooltip — you feel it through the stick.

Recovery inverts that. As you complete faction missions and standing climbs, your airspace clears. The visual and kinesthetic reward for repairing a faction relationship is seeing fewer hostiles between you and home. That's the SimCopter payoff operating through standing mechanics — you built something, you damaged your relationship with the people watching it, and you can see the consequences from altitude.

This connects directly to Ren's question 3: yes, recovery costs standing with rivals, and **that cost shows in rival patrol density over your settlement**. Two players committed to opposing factions at M8 get genuinely contested airspace — different faction patrols coming from different vectors. That's the M8 two-spawn-axis geometry finding its design reason.

Standing floor for recovery access? I'd say available at any positive value. If you can land dirtside safely, you can attempt recovery. The cost is the missions, not the gate.

## Round: CRITIQUE

### Vera (EV systems historian)

**[PROPOSE - Vera (EV systems historian)]**

Both positions are directionally correct on mission-gating. Neither has asked the EV-critical question: **what does the floor actually mean?**

In Nova, standing wasn't a continuous gradient with smooth recovery available everywhere. Below certain thresholds, factions wouldn't let you dock. That's not a mission gate — it's a physical access gate. You couldn't begin recovery missions because you couldn't land to take them. The floor had teeth.

This game has The Bar as the mission acquisition layer. If degraded standing means the faction's Bar contacts won't speak to you, recovery missions don't exist in the UI — there's nothing to take. Max's "available at any positive value" proposal collapses that distinction. Positive standing doesn't mean relationship intact. It means you haven't fully antagonized them yet. Those are different states.

I'd separate standing into three behavioral bands:
- **Engaged** (above ~40): missions available, normal NPC behavior
- **Degraded** (below 40, above some floor): faction contacts cold, recovery missions sparse or absent, airspace hotter
- **Hostile** (below floor): faction shoots on sight, no docking, recovery requires an intermediary or a specific authored string — not just grinding missions

Max's patrol density feedback is compelling but it's M8 geometry. Don't let the visual design of atmospheric consequences drive the M5 standing logic.

**My question for this round:** Does the hostile floor exist, and if so, is recovery from it player-initiated or does it require a specific authored trigger to unlock the recovery path?

### Nadia (new-player experience advocate)

**[PROPOSE - Nadia (new-player experience advocate)]**

Vera's three-band model is the right structure. My concern is the Degraded band, not the Hostile floor.

The Hostile floor is legible. Faction shoots on sight — players understand they've crossed a line even without knowing why. The consequence is immediate, physical, and unmistakable. That band can require an authored unlock because the player *knows* something broke.

The Degraded band is where new players get quietly punished without feedback. Bar contacts going cold, missions becoming sparse — these are invisible to someone who doesn't have a prior session's mission density to compare against. They'll think the content dried up, not that they degraded a relationship. That's systems-legibility failure happening below the threshold where the standing tooltip even fires.

My proposal: the standing tooltip should fire **downward through 40**, not just upward. Specifically, it should read differently — not "here's what standing affects" but "your standing with [Faction] is slipping — this is what's starting to close." That one-time downward trigger is the signal that makes the Degraded band legible before it becomes the Hostile floor.

For recovery access: I agree with Vera that "any positive value" is too loose. But the gate shouldn't be invisible. If a Bar contact won't offer recovery missions below a certain value, there needs to be a single cold line of dialogue telling the player what's happening: *"Come back when we're on better terms."* Not a UI tooltip. A person in a bar saying something true.

Recovery should be hard. It shouldn't be silent.

## Round: EVALUATE

### Soren (solo dev scope warden)

**[PROPOSE — Soren (scope estimator)]**

Before this round adds another design layer, I want to sequence what's actually being decided versus what's being designed.

Vera's three-band model is the right frame. The question is what each band *costs to implement*, because the bands aren't equal:

**Engaged → Degraded** is a read against a threshold. One conditional. Already implied by the 40-threshold tooltip work. Build cost: negligible.

**Degraded band behavior** — Bar contacts cold, missions sparse — requires NPC state reads against faction standing. Every NPC contact that changes behavior based on standing is a separate implementation point. "Sparse" missions means a filter pass on the mission pool. This is real work. Not enormous, but not free.

**Hostile floor recovery** — Vera's intermediary or authored string — is content work that has no ceiling. "An authored trigger to unlock the recovery path" is a quest. That's M6 or later, not M5.

My recommendation for M5 scope:

1. Implement the three bands as standing thresholds only — no behavioral differences in M5 beyond what's already decided (tooltip, commitment NPC, patrol density is M8)
2. Nadia's cold dialogue line is the right call and it's one string per faction contact — that's manageable if it's a single state, not a branching tree
3. Recovery mechanics in M5 = mission-gated, drawing from existing pool, no separate authored recovery type. Distinct recovery missions are content scope that belongs post-playtest.

The downward tooltip is the only open question I'd close today. Everything else is M6+ until the core loop has run.

<!-- complete -->
