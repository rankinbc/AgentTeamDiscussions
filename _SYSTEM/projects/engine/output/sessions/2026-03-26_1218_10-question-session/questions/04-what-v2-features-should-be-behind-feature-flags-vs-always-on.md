# What V2 features should be behind feature flags vs always-on?

*Generated: 2026-03-26 12:32 | Q4 | 209s | Mode: compete*

## Decisions

### DECIDED: Two Session-Level Feature Flags Only

Blind proposals and graduated resistance are the two V2 features that require session-level feature flags. All other V2 features ship always-on or are configured at the agent/team YAML level.

The deciding criterion is **synthesis blast radius**: does the feature change the shape or contentiousness of what the synthesis step receives? If a miscalibration corrupts synthesis input, it corrupts the Morning Brief — the artifact the user actually reads. That is the only failure mode that justifies a kill switch.

- **Blind proposals** change synthesis input structure. Agents no longer build on each other's work, so synthesis receives independent positions instead of a threaded conversation. That is a different document shape requiring different synthesis behavior. Flag it.
- **Graduated resistance** changes synthesis input contentiousness. Agents pushing back harder produce less-converged material. The Morning Brief shifts from consensus summary to conflict summary. The user notices. Flag it.

### DECIDED: Feature Flags Live in session.json, Checked in PromptBuilder

The flag mechanism is a `features` map in `session.json`, read at session start, checked in `PromptBuilder` during prompt assembly. One location. Not scattered across the codebase.

```yaml
features:
  blind_proposals: true
  graduated_resistance: false
```

If a key is absent, the feature is off. No defaults file, no inheritance, no overrides. Two booleans. Two code paths in PromptBuilder. That is the entire flag surface.

Do not build a feature flag framework. Do not add flag toggle UI. Do not support mid-session flag changes. Sessions are append-only — you pick configuration at session start and live with it.

### DECIDED: Ego Simulation and Graduated Resistance Intensity Are Team YAML Configuration, Not Session Flags

Ego simulation changes content distribution (how agents weight their own prior positions) but does not change synthesis input shape. It is a behavioral tuning concern, not a kill-switch concern.

Graduated resistance, while flagged at the session level for on/off control, requires intensity bounds defined in team YAML per mode. A boolean is not sufficient — the team definition must specify how aggressively resistance escalates.

Both belong in `data/teams/*.yaml` as mode-level configuration:

```yaml
modes:
  compete:
    ego_weight: 0.6        # how much agents favor own prior positions
    resistance_ceiling: 3   # max escalation level for graduated resistance
```

This keeps behavioral tuning where behavioral definitions live and avoids burning context tokens on session-level meta-instructions that must be injected into every agent prompt every round.

### DECIDED: Anti-Coordination Scoring Ships Always-On as Instrumentation

Anti-coordination scoring is measurement. It analyzes outputs after rounds complete. As long as it does not feed back into agent prompts, it has zero impact on discussion flow or synthesis input. It belongs in the same category as prompt output snapshots: instrumentation that runs silently.

If anti-coordination scoring ever feeds back into prompts (influencing agent behavior based on scores), it must be promoted to a session-level flag at that time. Read-only measurement does not need a kill switch.

### DECIDED: Tiered Summarization Ships Always-On

Tiered summarization changes what agents see (compressed history vs. full history) but does not change what synthesis receives. The failure mode is "agents seem less informed in later rounds," which is a tuning problem addressed by adjusting summarization thresholds in `config/defaults.yaml` — not a kill-switch problem.

Flagging it would add a third boolean that costs context tokens on every prompt injection (explaining to agents whether they are seeing full or summarized history) while protecting against a failure the user experiences as mild quality degradation, not output corruption.

### DECIDED: All Mechanical V2 Changes Ship Without Flags

The following are always-on with no flag surface:

| Feature | Rationale |
|---|---|
| Manifest versioning | Bookkeeping. No behavioral impact. |
| Priority-queue eviction with hardcoded order | Deterministic. No calibration needed. |
| Agent identity 800-token cap | A constraint, not a behavior. Validate during development that current agents fit. |
| Prompt output snapshots | Instrumentation. Zero impact on discussion flow. |
| Context budget by round type | Mechanical allocation. No agent behavior change. |

### DECIDED: Flags Are Per-Session, Never Mid-Session

Mid-session rollback is architecturally incoherent with append-only session design. You cannot un-blind proposals after round one ran blind. You cannot retroactively change eviction priorities after context already overflowed.

The contract: features are set at session creation, recorded in `session.json`, and immutable for the session lifetime. If a session produces poor output, you run a new session with different flags. You do not patch a running session.

### DECIDED: Validate 800-Token Agent Cap Before Shipping

The 800-token agent identity cap was accepted in prior decisions but has not been validated against current agent definitions after prompt assembly. Before shipping any V2 feature, measure actual token counts for all agents post-PromptBuilder assembly. If agents exceed the cap, the entire eviction order is theoretical.

This is a development task, not a flag decision — but it blocks confident deployment of the eviction system.

---

## Design Rationale

The discussion surfaced four competing criteria for flag decisions:

1. **Developer confidence** (Flow Orchestrator): flag what feels experimental. Rejected — confidence without production data is guesswork.
2. **Behavioral coupling** (Cognitive Architect): flag what creates inter-agent feedback dynamics. Principled but untestable before observation.
3. **Reversibility** (Adversarial Critic): flag everything irreversible. Rejected — creates combinatorial test burden (2^n configurations) and configuration friction that degrades the product.
4. **Synthesis blast radius** (Systems Pragmatist / Product Oracle): flag what changes synthesis input. Adopted — it is testable, user-outcome-anchored, and produces a minimal flag surface.

The Context Surgeon's contribution refined the decision by identifying that flags themselves have a cost: every flag injects explanatory tokens into every agent prompt in every round. Minimizing flags is not just about simplicity — it is about preserving context budget for actual discussion content rather than meta-instructions about behavioral mode.

The final design splits behavioral configuration into two layers:
- **Session-level flags** (2 total) for features that change synthesis input shape or contentiousness
- **Team YAML configuration** for features that tune agent behavior within the existing synthesis contract

This avoids both the "flag everything" tax and the "ship and pray" risk, while keeping the configuration surface that a solo builder must understand to exactly two choices per session.
<!-- complete -->
