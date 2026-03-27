### Vera (EV systems historian)

Before accepting Ren and Max's framing, I need to flag what EV actually did — because neither "nearest" nor "friendly" appears in the original mechanic.

EV used **last docked**. Not nearest. Not navigable-nearest. The planet you most recently touched down on. That's where you woke up.

The design implication is significant: in EV, *where you choose to land is a strategic decision*. Players landing at a faction port they're pushing standing with aren't just picking up missions — they're setting their respawn anchor. The choice carries weight you feel later. Landing frequency and landing location become meaningful in a way that "nearest navigable friendly" erases.

"Nearest" imports a complexity that EV avoided deliberately. It also introduces a read-path dependency — routing topology, contested boundary state, live port availability — that last-docked doesn't require.

Max's destroyed-pad scenario is emotionally correct but mechanically inverted if we use last-docked. You respawn at the last port you successfully landed at *before* the raid that killed you. That's probably your own pad, pre-damage. You wake up, you fly home, you see what happened. The SimCopter payoff is still there — it's the *approach vector* that delivers it, not the spawn point.

My proposal: define respawn as last-docked, where "docked" requires standing ≥ Engaged at that port. This keeps the standing read. It keeps the strategic weight of landing choices. It eliminates the routing-topology dependency entirely.

Destroyed ports become a forward-session problem, not a respawn-definition problem. Scope accordingly.

### Nadia (new-player experience advocate)

Vera's last-docked framing is the right call, and I want to name *why* from a player experience perspective: legibility.

"Nearest navigable friendly" is an invisible algorithm. When a new player wakes up at a distant port, they don't know why. They don't know what the system weighed, what topology it traversed, what standing values it read. It just *happens to them*. That's the worst kind of system — consequential but unreadable.

Last-docked is a mirror. The player remembers landing there. The logic is traceable to a choice they made. When they wake up, they can reconstruct the story without a tooltip.

Max's emotional beat — flying home to see the damage — survives completely under last-docked. Vera's right that it's the approach vector doing the work, not the spawn point. You still see the settlement from altitude. The SimCopter moment is intact.

One gap nobody addressed: **first death before meaningful docking**. A new player dies in their first skirmish, having only ever touched down at the starting port. Last-docked works fine — they wake up at origin. But that starting port needs to be guaranteed Engaged-accessible by definition, or first death could produce a confusing null state. Starting port should be hardcoded as always-accessible regardless of standing. That's a new-player contract, not a standing-system exception.

Support Vera's proposal. Last-docked, standing ≥ Engaged required, starting port as fallback anchor. Eliminates routing dependency, preserves strategic weight, and is legible to someone who just died for the first time.


<!-- complete -->
