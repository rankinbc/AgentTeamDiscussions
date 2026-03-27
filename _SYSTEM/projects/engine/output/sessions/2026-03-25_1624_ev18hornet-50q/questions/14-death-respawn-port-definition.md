# Death Respawn Port Definition

*Generated: 2026-03-25 17:12 | Question 14 | 183s | Mode: ev18hornet*

## Decisions

**Respawn model is last-docked, not nearest navigable friendly.** The respawn anchor is the port the player most recently successfully docked at, where "successfully" requires standing ≥ Engaged (≥ 40) with the owning faction at the time of landing. This is a single field written on landing. It introduces no routing-topology dependency, no graph traversal, no live contested-boundary read. "Nearest navigable friendly" is explicitly rejected — it is an invisible algorithm with weeks of infrastructure cost that EV deliberately avoided.

**"Friendly" is not a new flag.** Port accessibility for respawn purposes reads from the existing standing band system. A port owned by a faction toward which the player holds Hostile standing is inaccessible for docking and therefore ineligible as a respawn anchor. No separate friendly-flag field is introduced for the death flow. Engaged/Degraded/Hostile bands do this work.

**Landing at the player's own settlement pad counts as docking.** Touching down on a player-owned settlement landing pad writes the last-docked anchor identically to landing at a faction port. This preserves Max's scenario: if the player's last landing was at their own pad before the raid that killed them, they wake up there, in atmosphere, with a flight path home already established. The SimCopter payoff — seeing the damage from altitude on approach — is delivered by the spawn point itself, not by a separate approach-vector mechanic.

**Starting port is a hardcoded fallback anchor, always accessible regardless of standing.** On first death, or on any death where the last-docked anchor cannot be resolved, the player respawns at the starting port. This port is exempt from standing checks as a new-player contract. It is not a standing-system exception — it is a constant that the standing system does not touch. One named config constant.

**Contested systems and faction-owned ports with bad standing are handled by the docking write, not the respawn read.** A player with Hostile standing toward Confederation cannot dock at a Confederation port while alive, so a Confederation port can never be their last-docked anchor. No special respawn-time standing check is required for the contested-system edge case. The exclusion happens upstream at landing, not downstream at death.

---

## Open Questions

**Pad destruction and anchor invalidation — two paths, not yet chosen.** If a settlement pad degrades or is destroyed through raid damage, does it remain a valid respawn anchor?

- *Option A:* Degraded pad remains dockable and valid as a respawn anchor regardless of damage state. No fallback chain required. Landing pad functional state does not affect the anchor field. Simplest implementation.
- *Option B:* A pad below a defined damage threshold is invalid as a respawn anchor. Requires a fallback chain: next most recent valid anchor, then starting port. Adds a fallback lookup and a pad-state read at respawn time.

Option B has real build cost. The fallback chain must be scoped explicitly before Option B is chosen. The question gates whether tier regression interacts with the respawn system at all. **Not resolved in this discussion.**

**How deep does tier regression cut pad functionality?** Soren's closing question is unanswered. If a Colony regresses to Outpost, does the landing pad survive intact, degrade to a lower-capacity state, or disappear? The answer determines whether Option A and Option B above produce different outcomes in practice. Pad functionality at each regression tier is not yet specified. **Blocking for Option B scope estimate.**

**Degraded-pad docking write.** If a pad is in degraded state but still physically present (Option A), does landing on it still write the last-docked anchor? Implied yes under Option A, but not explicitly confirmed. Requires confirmation before M7 builds the pad damage model.

**Standing check direction at respawn time.** Under last-docked, standing is checked at docking time (write). Whether standing is also re-checked at respawn time — if standing has fallen since last docking — is not addressed. If a player docked at a Confederation port while Engaged, then fell to Hostile before dying, does the last-docked anchor remain valid? The simpler rule is: anchor is set at docking and not re-evaluated at respawn. The stricter rule re-checks standing at respawn and triggers fallback if standing has since degraded. Which rule ships is not decided. **Must be resolved before death-flow implementation begins.**

---

## Carried Open Questions (Unaffected by This Discussion)

- Per-faction rivalry heat values — config architecture must support per-faction overrides from day one; no authored values
- Defection multiplier post-commitment — whether `FACTION_STANDING_LOSS_MULTIPLIER` increases after commitment NPC trigger
- Hostile floor numeric value — named config constant required; value deferred pending M5 playtest data
- Authored Hostile recovery trigger form — deferred pending Hostile band frequency playtest data
- Mission pool sparsity definition in Degraded band — probability filter, reduced count, or mission type subset unspecified
- Commitment NPC dialogue content and content system — exact dialogue and settlement tier/raid history variable read path not designed
- Standing floor behavior post-commitment with allied faction — undefined for M5
- Standing tooltip direction — fires at crossing 40 upward only or in both directions; threshold decided, direction open
- Joint action delta magnitude for co-op — full or fractional standing consequence per participating player; must resolve before M8 mission resolution ships
- Standing change cause attribution for co-op — notification surface deferred to M8
- Contested airspace spawn geometry for split-commitment co-op — deferred to M8
- Passive decay milestone — requires M5 event-only playtest data
- Refusal-tracking attribution rule — deliberate decline vs. absence vs. never reached a faction Bar
- `DECAY_FLOOR` numeric value — named config constant required above `HOSTILE_THRESHOLD`; value deferred
- Hull capture standing delta magnitude per faction — named config constants required; numeric values deferred
- Relative magnitude of hull capture versus mission failure standing consequence
- Comms intercept string content per faction — content design out of scope
- Patrol vector modifier numeric values — named config constants required; values deferred
- Bribe path design — deferred pending Bar rumor/informant surface and deferred-state store
- Salvage flag path design — deferred pending faction-specific grievance tracking
- M6 scope capacity — full committed scope list required to place galaxy-layer formation AI and threat-aware hold state
- Build cost of threat-aware hold state — gates M6 vs. M7 placement
- Escort hold visual treatment — circular orbit, stationary hover, or trailing vector; UX decision required before M6 ships layer-transition contract
- Mechanical resolution when raid spawns during escort hold — escort engagement rules, destruction possibility, player surface state unspecified
- Terrain avoidance timing — deferred to M8 alongside full atmospheric follow
- `SETTLEMENT_REGRESSION_THRESHOLD` numeric value — deferred pending M7 building type count and structural damage accumulation rates
- Building type count at Settlement, Colony, and City tiers — required inputs for M8 regression asset estimate
- Tier regression milestone placement — M7 stat-only vs. M8 geometry change
- Assault-scale split-vector spawn bearing offsets for M7 solo — named config constants required
- First-raid protection window co-op edge case — both players or only triggering player
- Defense emplacement milestone placement — blocking for scope estimates including the emplacement
- Power-emplacement dependency raid AI query path architecture — not yet specified
- Power node degraded state visual signal at 500 meters in flat-poly — must resolve before degraded model is built
- Tier regression rebuild cost mechanism — resource reduction, time reduction, or step-count reduction; must be named config constant before implementation
- Which in-world surface carries the rebuild gate explanation at moment of regression — comms intercept or Bar cold dialogue
- Scaffolding third geometry state asset estimate — per-building-type day count required before group can approve
<!-- complete -->
