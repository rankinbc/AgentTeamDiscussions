# Is the researcher/organizer split the right pipeline architecture?

*Generated: 2026-03-26 18:47 | Q2 | 221s | Mode: compete*

## Decisions

### 1. The Organizer Agent Is Eliminated

The two-role researcher/organizer pipeline is replaced. The organizer model fails on two independent grounds: it inverts cognitive load (least-contextualized agent makes highest-judgment decisions), and its whole-structure visibility is a context-budget catastrophe that scales with hierarchy size. At wave 5+ an organizer must load the full hierarchy plus all new raw files simultaneously — that is O(n) context consumption, not a feature.

### 2. Researchers Own Their Metadata

Every researcher output carries three required tags:

- **Proposed path** — the full hierarchy path the researcher believes the file belongs at (e.g., `systems/combat/action_combat/damage_formulas`)
- **Depth level** — numeric (0 = overview prose, 3+ = exact tables/formulas)
- **Provenance class** — one of: `ROM_VERIFIED`, `COMMUNITY_VERIFIED`, `GUIDE_SOURCED`, `INFERRED`, `OBSERVED`

Tag quality is a researcher responsibility, not a downstream concern. Researchers are closest to the data they found; they carry the context to tag it correctly.

### 3. Routing Is Deterministic and Path-Local

A deterministic router places files mechanically based on proposed path tags. No agent judgment is involved in routing. The router requires only three things: the proposed path, the hierarchy path rules, and the immediate neighborhood of the target node. This keeps routing decisions O(1) context, not O(n).

### 4. New Hierarchy Nodes Require an Explicit Approval Gate

When a researcher proposes a path that does not yet exist in the hierarchy, the router does not create the node automatically, drop the file, or queue it silently. It emits a **path proposal record** and halts placement of that file.

Path proposal records are first-class artifacts. They contain: the proposed path, the researcher who proposed it, the raw file awaiting placement, and a brief rationale. A human reviews and approves or redirects before the next wave proceeds. This is the single judgment gate in the pipeline. The organizer role, if it survives at all, shrinks to this one decision point — not a trailing agent reviewing all placements.

### 5. Conflicts Are First-Class File Artifacts

When two files resolve to the same leaf path with different provenance classes, the router automatically emits a **conflict record** rather than overwriting. It does not resolve. Conflict records contain:

- Both conflicting claims, verbatim
- Provenance class of each
- Source agent for each
- The path both resolved to
- Resolution status: `UNRESOLVED`

For read operations, highest provenance class wins. The lower-provenance version is preserved in the conflict record, not discarded.

Conflict records accumulate in a designated `_conflicts/` folder at the relevant hierarchy level. They do not disappear passively. Resolution requires explicit human action: either marking one claim authoritative and archiving the other, or flagging for follow-up research in the next wave proposal.

### 6. Failures Are User-Visible by Design

The organizer model fails silently: a mis-slotted finding propagates into the Morning Brief as confident synthesis built on misplaced data. The pipeline defined here fails visibly: unresolved path proposals and conflict records are explicit artifacts the user sees and acts on.

A Morning Brief generated from a hierarchy containing unresolved conflict records must surface those records by count and location. The user is never reading synthesis that conceals live contradictions.

### 7. Implementation Is Wave-Gated

This architecture is not fully built before wave 2 runs. The sequencing is:

- **Now:** Implement researcher metadata tagging (proposed path, depth, provenance). Run two full research waves using human review for all placements.
- **After wave 2:** Observe which actual failure manifests — tag quality degradation, path proposal volume, conflict accumulation rate, or hierarchy instability. Build the minimum router machinery to address the observed failure.
- **Do not build** conflict detection automation, path-proposal queuing, or routing logic before wave 2 produces empirical data.

The context scaling problem is predictable and should inform architecture direction now. The specific failure thresholds are not predictable and should not be engineered against before they appear.

### 8. What Is Not Decided Here

- Whether path proposals require synchronous human approval or can batch between waves
- Tooling for conflict record management (manual file editing vs. CLI vs. dashboard)
- Whether the Conflict Registrar concept (CA's proposal) warrants its own agent at high conflict volumes — deferred to post-wave-2 evaluation
- Retention policy for resolved conflict records
<!-- complete -->
