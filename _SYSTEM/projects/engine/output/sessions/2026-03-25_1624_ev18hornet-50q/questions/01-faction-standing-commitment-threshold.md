# Faction Standing Commitment Threshold

*Generated: 2026-03-25 16:27 | Question 1 | 166s | Mode: ev18hornet*

## Decisions

**Commitment NPC Unlock Condition:** Standing ≥ 60 AND completed_faction_mission_count ≥ 1

**Commitment NPC Location:** The Bar (On-Foot layer, dirtside)

**Standing Display:** Standing tooltip surfaces the first time player standing with any faction crosses 40, naming the system before it gates content

---

## Faction Standing — Commitment NPC Design

### Trigger Condition

The commitment NPC becomes available when both of the following are true simultaneously:

- Player faction standing ≥ 60 (on a 0–100 scale)
- Player has completed at least one mission in the faction's mission string (boolean flag: `faction_mission_completed = true`)

Both conditions must be satisfied. Neither alone is sufficient.

**Standing is a precondition. Mission completion is the intent signal.**

Standing accumulates through trade, travel, and passive behavior. It reflects exposure and reputation, not deliberate choice. Mission completion is a discrete player action — the player accepted a flagged mission, flew it, and returned. That act is unambiguous. The commitment NPC responds to the combination: you have standing *and* you have chosen to do work for this faction.

### Why This Number

60 is the threshold where faction standing has moved past neutral drift and into active relationship. Below 60, the player's standing could be an artifact of trade routes or proximity. At 60, combined with at least one completed mission, the standing reflects a player who has engaged with the faction as a faction — not just as a background variable.

80+ would make the NPC redundant: at that standing, the relationship is already defined. The NPC would feel like paperwork on an already-decided outcome.

40 or lower would make the NPC premature: the player hasn't yet experienced the systems the commitment is asking them to deepen.

65 (Max's proposal) and 55 (Ren's proposal) were both reasonable but lacked a second condition anchor. The mission completion flag is what makes 60 defensible — the number alone is not the mechanism.

### What Is Not the Trigger

- **Settlement tier** — a player can have deep faction relationship without building high. Tier gates content in the Settlement system; it should not gate relationship content in the Faction system.
- **Raid repelled count** — a combat statistic that does not yet exist in the data model. Authorizing this condition would authorize a new statistics system as a prerequisite to M5. That prerequisite is not scoped.
- **Standing alone** — two players at standing 60 may have radically different relationships with the faction. One farmed trade routes; one flew escort missions. The mission completion flag distinguishes them at the code layer.
- **Atmospheric intercept** — ruled out on feel (mid-flight unknown contacts read as threats to new and experienced players alike) and on build scope (mid-flight NPC broadcast is a new mechanic not required by any other system). Every consequential NPC conversation in the EV lineage happens in a bar or spaceport. This one does too.

### Location

The commitment NPC is encountered in the Bar, accessed through the On-Foot layer.

The Bar is the established site for consequential conversations. Players learn early that the Bar is where missions begin, rumors surface, and relationships deepen. Delivering the commitment offer here uses a learned pattern rather than introducing a new one at the highest-stakes narrative moment in the faction arc.

Dirtside delivery also closes a loop: the player has been flying faction airspace, building in faction territory, completing faction missions — and now they walk into a bar and someone who has been watching them is there. That sequence is legible without explanation.

### Standing Tooltip

The first time player standing with any faction crosses 40 (in either direction), a tooltip surfaces that names the standing system, shows the current value, and briefly describes what standing affects (mission availability, equipment access, faction raid behavior toward settlements).

This is a one-time trigger per faction, not a recurring interrupt. Its purpose is to ensure that when the commitment NPC appears at standing 60, the player has already been introduced to the system governing it. Without this surface, the threshold is invisible and the NPC appears to fire randomly.

### Data Requirements for M5

The following must be queryable at trigger-check time:

| Field | Type | Notes |
|---|---|---|
| `faction_standing[faction_id]` | integer 0–100 | Already required by faction system |
| `faction_mission_completed[faction_id]` | boolean | Required for mission string progression; not new |

No new data model entries are required. `raid_repelled_count` is explicitly out of scope for this trigger.

### Trigger Check Pseudocode

```
func commitment_npc_available(faction_id) -> bool:
    return (
        faction_standing[faction_id] >= 60
        and faction_mission_completed[faction_id] == true
    )
```

This check runs when the player enters the Bar in a location associated with the faction. If true, the commitment NPC is present and interactable. If false, the NPC is absent — no placeholder, no hint, no partial state.

### Settlement and Raid Interactions

Settlement tier and raid history inform the *meaning* of the commitment conversation (a player with a Colony has more to defend than one with a Claim Stake) but do not modify the trigger condition. These variables are available as context for writing the commitment NPC's dialogue — they should be read by the content system, not by the unlock check.
<!-- complete -->
