# Should V2 be built as incremental upgrades to V1 or as a parallel rewrite?

*Generated: 2026-03-26 12:25 | Q2 | 192s | Mode: compete*

## Decisions

### DECIDED: Prompt Output Snapshots Are the Non-Negotiable First Deliverable

Before any structural work begins, capture known-good prompt output for every existing mode (compete, counter, lean, ideas, ideas_compete, bigsmall, angles, default). These snapshots serve two purposes: regression oracle for detecting prompt degradation, and product baseline for measuring whether V2 changes improve Morning Brief quality. Days of effort, not weeks.

### DECIDED: PromptBuilder Is the Migration Entry Point, Not the Round Loop

The round loop is sequential and predictable. The actual coupling hotspot is PromptBuilder's context assembly, which already touches agent config, session state, round history, and role overlays simultaneously. Every V2 feature -- blind proposals, phase gates, stale detection -- ultimately manifests as a change to what agents see in their prompts. Start where value flows.

### DECIDED: Blind Proposals Ship Through PromptBuilder Modification First

Blind proposals require withholding prior round context during the proposal phase. This can be achieved by modifying PromptBuilder's context assembly without restructuring the round loop. Ship this as the first V2 change, measured against Morning Brief quality. If output improves, V2's core thesis is validated. If it doesn't, you've learned something critical before committing to larger structural changes.

### DECIDED: The Migration Pattern Emerges From Feature Delivery, Not Upfront Design

No strangler fig interface extraction. No state machine formalization. No parallel rewrite. These are premature commitments without empirical evidence of actual coupling boundaries. As features ship through PromptBuilder modification, the natural abstraction boundary will reveal itself. The round loop abstraction (IDiscussionPipeline or equivalent) may still be the right pattern, but it is earned through evidence, not assumed through architectural aesthetics.

### DECIDED: Every V2 Change Is Measured Against Output Quality

The Morning Brief and design docs are the product. The migration strategy that wins is the one where output quality improves fastest. Prompt output snapshots provide the diff target. Each feature ships only when it demonstrably improves or maintains output quality against known-good baselines. Internal architectural elegance is not a success metric.

### DECIDED: BIT System and Key Takeaways Layer On Top Independently

These features do not require round loop restructuring or PromptBuilder changes that interfere with blind proposals or phase gates. They can be built whenever capacity allows, in any order, without coordination with the core migration path.

---

## Migration Sequence

1. **Prompt snapshots** -- Capture full prompt output for all modes across both teams. Establish Morning Brief quality baseline.
2. **Blind proposals via PromptBuilder** -- Modify context assembly to withhold prior round output during proposal phase. Measure output quality diff.
3. **Manifest versioning** -- Co-deliver with blind proposals as previously decided. Not a blocker but a mandatory companion.
4. **Phase system** -- If blind proposals required PromptBuilder branching that strains the current structure, extract the round loop abstraction at this point. If PromptBuilder handled it cleanly, continue with targeted modification.
5. **Stale detection** -- Requires phases. Ships after phase system stabilizes.
6. **BIT system / key takeaways** -- Independent. Ship whenever.

---

## Rules

- No V2 feature ships without prompt output snapshot coverage for all affected modes.
- No architectural scaffolding ships without a feature that immediately uses it.
- PromptBuilder modifications must be validated against prompt snapshots before merge. If a change alters prompts for modes it shouldn't affect, the blast radius is too large.
- If PromptBuilder develops more than two levels of mode-conditional branching for V2 features, that is the empirical signal to extract a pipeline abstraction. Not before.
- Anti-sycophancy remains a validation concern, not an architectural one. It is enforced through prompt content, not system structure.

---

## Risks and Mitigations

| Risk | Mitigation |
|---|---|
| PromptBuilder becomes a god object under successive V2 modifications | The two-branch threshold rule triggers extraction before complexity compounds |
| Prompt snapshots become stale as features ship | Snapshots update with each feature merge; old snapshots are archived, not deleted |
| Blind proposals degrade output quality for some modes | Per-mode snapshot comparison catches regression before merge; roll back if quality drops |
| Multiple V2 features in flight create interference patterns in PromptBuilder | One PromptBuilder-touching feature at a time. BIT and key takeaways (non-PromptBuilder) can parallel |

---

## What Was Rejected

- **Strangler fig pattern as starting point.** Correct intuition about the round loop being the spine, but premature without evidence that PromptBuilder modification fails first. May be adopted later if empirically justified.
- **State machine formalization before interface extraction.** Useful analysis tool but formalizing states across seven modes risks locking in a unification that may not exist. Let the abstraction emerge.
- **Parallel rewrite.** Eliminates the feedback signal needed to evaluate whether structural changes improve discussion quality. The system that preaches iterating against real output cannot rewrite in isolation.
- **Pure incremental patching.** Four overlapping mutations to the most coupled component is not four small changes. It is an interference pattern. The snapshot baseline and single-feature-at-a-time rule prevent this from becoming death by a thousand conditionals.
<!-- complete -->
