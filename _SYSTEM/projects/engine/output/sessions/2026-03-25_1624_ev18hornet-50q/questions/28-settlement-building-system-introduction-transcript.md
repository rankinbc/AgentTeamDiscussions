# Transcript: Settlement Building System Introduction

*Generated: 2026-03-25 18:12*

## Round: PROPOSE

### Ren (emergence systems theorist)

The discovery method question is actually a question about when the emergence chain becomes live.

Building isn't interesting in isolation. It becomes interesting the moment a faction has a reason to care about what you built. That means the discovery method has a dependency: the player needs *something* to provoke standing movement before the settlement has tactical weight. If they build before standing has moved, they're constructing in a vacuum — no faction pressure, no reason to understand what defense means.

So the question I'd put to the group is this: **what's the minimum precondition for building to read as a consequential choice rather than a tutorial step?**

Three candidate answers, ordered by emergence quality:

**Option A — Open from session one, no gate.** Maximum agency. Risk: player builds before understanding what they're building against. The structure exists but the threat chain is silent.

**Option B — Triggered by first landing on a claimable world.** Landing is already a meaningful act (respawn anchor write, docking event). Piggyback building availability onto the same event. No authored tutorial, just affordance.

**Option C — Mission-gated.** Scripted. Predictable. Caps agency to manage onboarding legibility. This is the anti-pattern.

My read: Option B uses an event the system already tracks. The claim stake becomes available when the player executes a behavior that demonstrates they've committed to a location — landing. No new tutorial scaffolding. Faction standing starts moving from session one through Confederation missions, so by the time the player claims a world, the pressure chain is already warming.

What does the starting-system geography decision (Q27) tell us about when first landing on a claimable world happens relative to first standing movement?

### Max (atmospheric flight advocate)

Ren's right that Option C is the anti-pattern, and Option B is cleaner than Option A — but I want to push on *why* landing is the right trigger, because I think the atmospheric layer answer is actually more specific than "landing demonstrates commitment."

The SimCopter payoff — flying over your own build at altitude and recognizing it — only works if the player has something worth recognizing. A Claim Stake with one shelter reads as debris from above. The geometry needs *enough* to be legible at 500 meters before the aerial view becomes the reward it's supposed to be.

So here's the lateral angle: the building affordance opening on landing isn't just about commitment signal to the faction system. It's about *priming the player to look down*. The first descent to claim a world is the exact moment you want the player developing the vertical mental model — sky above, terrain below, their future settlement in between. If building unlocks at that moment, the player is immediately thinking about what they're creating *as something they'll see from the air*.

That's not tutorial scaffolding. That's the game teaching itself through the right sensory channel at the right time.

Option B, but with one addition: the Claim Stake placement should have a vertical confirmation view — a brief hover moment at mid-altitude showing the player the terrain they're claiming. Not a cutscene. Just a system-enforced altitude hold before ground access. Two seconds. Enough to establish the vertical relationship before they're dirtside.

The building system should feel like it was born from above.

## Round: CRITIQUE

### Vera (EV systems historian)

Max's altitude hold is tutorial scaffolding wearing an emergence costume. Flag it.

In EV Nova, the game never enforced a teaching moment. You landed, the port menu appeared, and the affordances were either there or they weren't. The system was legible because it was *simple enough to be self-explanatory on first contact*, not because the game paused your controls to make sure you looked at it correctly. A "system-enforced altitude hold" is two seconds of removed player agency plus a new AI state that must be implemented. That's Option C with better marketing.

More important: both Ren and Max are treating "building in a vacuum" as a problem to be solved by delay. EV's actual solution was different. The game let you do things before you understood them, and the consequences taught you. You could hire escorts before you understood faction standing. You could trade goods before you understood which routes were profitable. The system waited. The feedback arrived when your choices collided with the world.

Option A carries a real risk — the player builds without threat context — but the mitigation isn't a trigger condition. It's the Q27 decision already made: Confederation missions are available from session one, standing moves immediately, and the tooltip fires at 40. The pressure chain is already teaching the player that actions have faction consequences before they've built anything.

The question I want answered before we pick a trigger: does Claim Stake placement require dirtside access, or does the player designate the site from the air? That answer determines whether landing is the *right* event or just a *convenient* one.

### Nadia (new-player experience advocate)

Vera's question is the right one, and I want to sharpen why.

Option A only works if the affordance is actually *findable*. "Open from session one" and "discoverable by a new player" are not the same thing. If Claim Stake placement lives in a menu that requires knowing to look for it, it's not a feature — it's a secret that rewards players who already understand EV. That's the version of Option A I'd flag.

Vera's EV framing is correct about *consequences teaching you*, but EV's affordances were visible in the port menu. The player didn't have to discover that missions existed — the interface offered them. The building system needs equivalent surface. Where does it appear? If it appears in the landing port interface, Option A works cleanly. If it requires separate discovery, it needs a signal.

Max's altitude hold fails not because the vertical teaching moment is wrong — it's actually the right instinct — but because enforcing it removes agency. The right answer is that the *landing sequence itself* should create that view naturally through approach geometry, not through a locked camera state.

On Vera's actual question: if Claim Stake can be designated from the air, the trigger should be atmospheric descent with terrain visible, not ground contact. That's a stronger emergence moment than landing — the player chooses the location *while experiencing the vertical relationship* that will define the SimCopter payoff later.

But I want the group to confirm: does the flat-poly Claim Stake read as "yours" or as "environment" at first placement? Because if the aesthetic doesn't signal ownership at the moment of claiming, the whole chain goes invisible regardless of trigger.

## Round: EVALUATE

### Soren (solo dev scope warden)

Before the group debates trigger conditions, there's a prior question that actually gates the build cost estimate: **where does the building action live in the UI?**

Option A, B, and C are trigger conditions. None of them cost much to implement as triggers. A boolean check on session start, a flag set on landing, a mission completion state — these are all cheap. The trigger is not where the build time lives.

The build time lives in the **placement interface itself**. Two distinct implementations are on the table and nobody has named them:

**Path 1 — Landing port menu item.** Player lands, port interface appears, Claim Stake is a selectable option. Dirtside. Approximately same complexity as buying cargo. Low build cost.

**Path 2 — In-world placement tool.** Player designates a site via 3D interaction — either from the air or on foot. Requires: placement preview mesh, terrain validity check, confirmation state, anchor write. Non-trivial. Estimate 1–2 weeks solo to do it without bugs.

Nadia's "designation from air while experiencing vertical relationship" and Max's altitude hold both assume Path 2 exists. If Path 2 isn't built, those suggestions are scope additions, not trigger options.

One more flag: Vera's EV framing is correct — landing port menu is the EV-native pattern. It's also the cheapest one. If the group is tempted toward aerial designation because it *feels* more elegant, that feeling costs 1–2 weeks.

Confirm the interface path before the trigger debate. Everything downstream depends on it.

<!-- complete -->
