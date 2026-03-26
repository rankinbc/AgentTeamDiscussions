# Concurrency and scaling: what does reliable overnight operation look like?

*Generated: 2026-03-26 12:49 | Q9 | 195s | Mode: compete*

## Decisions

### DECIDED: Sequential Execution With Halt-on-Failure Is the Complete Overnight Model

One Claude CLI call at a time. No parallelism. The session is logically sequential — rounds depend on previous rounds, synthesis depends on all rounds. Parallelizing calls multiplies failure modes and rate-limit exposure without reducing wall-clock time for the parts that matter. Sequential execution makes every failure predictable and every retry safe.

When a Claude call fails after exhausting retries, the engine halts. It does not skip the agent, does not advance to the next round, does not attempt the next question. It writes current state to `session.json` and exits with a non-zero code. The operator gets two states: complete or stopped. No ambiguity.

**Rationale:** The Pragmatist and Oracle converged on this as the only model that preserves output trustworthiness. Skip-and-advance (proposed by the Orchestrator) was rejected by every evaluator because a session with silent holes is worse than a crash — it makes the Morning Brief untrustworthy, which destroys the system's primary value. The Architect's sequential model was correct; the Orchestrator's graceful degradation was the wrong optimization target.

### DECIDED: Retry With Exponential Backoff and Jitter, Capped at 120 Seconds

ClaudeRunner's existing retry mechanism gains exponential backoff: 3s, 9s, 27s, capped at 120s, with random jitter of +/-30% on each interval. Three consecutive failures on the same call trigger the halt described above. This is a modification to existing retry behavior, not a new subsystem.

**Rationale:** Consensus across all agents. The existing retry mechanism is the right place for this logic. The specific intervals (3s base, 120s cap, 3 attempts) were proposed by the Architect and unchallenged. Jitter prevents thundering-herd patterns if multiple sessions ever run concurrently.

### DECIDED: No External Watchdog Process, No Heartbeat File

No bash wrapper loop. No heartbeat file. No second process monitoring the first. The engine is its own watchdog through its existing timeout mechanism. If the engine process dies (OOM, machine restart, power loss), `--resume` with completion markers handles recovery. The operator either runs `--resume` manually or sets a cron entry that calls `--resume` periodically — the engine exits immediately if the session is already complete.

**Rationale:** The Orchestrator correctly identified that the Architect's heartbeat file and bash wrapper are redundant with completion markers that already exist. The Pragmatist reinforced this: adding a monitoring artifact that competes with an existing recovery mechanism creates confusion about which is authoritative. Completion markers are the heartbeat. `--resume` is the restart mechanism. Both already exist.

### DECIDED: Session Duration Cap in defaults.yaml

A `maxSessionDurationMinutes` setting in `config/defaults.yaml`. When exceeded, the engine writes current state and exits cleanly. This prevents runaway sessions from burning unlimited API budget overnight. The default should be generous (480 minutes / 8 hours) — this is a safety net, not a throttle.

**Rationale:** Proposed by the Orchestrator, unchallenged by any evaluator. The only scenario none of the other mechanisms cover is a session that technically progresses but takes far longer than expected. A wall-clock cap is the simplest prevention.

### DECIDED: Human-Readable Completion Report Is the Only New Artifact

When a session ends (whether complete or halted), SessionRunner writes a structured completion report covering: which questions completed, which question was in progress when halted (if applicable), wall-clock duration per question, total session duration, any retry events with timestamps, and final status. This is appended to or written alongside the existing session output — not a separate monitoring system.

**Rationale:** The Pragmatist identified this as the only overnight operational question that matters: "How does the operator know what happened when they check in the morning?" The Oracle confirmed that the operator's morning experience is the correct design target. A completion report gives the operator immediate triage capability without reading transcripts or parsing logs.

### DECIDED: No Runtime Quality Validation

No LLM-as-judge between rounds. No automated quality scoring of agent responses. No response length checks, coherence scoring, or degradation detection at runtime. The Critic correctly identified quality degradation as the primary overnight risk — Claude producing increasingly generic responses during sustained multi-hour sessions. However, runtime quality validation would require calling Claude to judge Claude, which degrades under the same conditions it monitors. Prior decisions (Q5, Q6) explicitly prohibit LLM-as-judge and automated quality scoring.

Quality degradation is accepted as an unmitigable V2 risk. The mitigation is the existing paired human comparison framework: if overnight output reads worse, the operator catches it during review and re-runs. The retry cost is one night of compute, not data loss.

**Rationale:** The Critic raised a real risk. The Surgeon and Pragmatist both concluded it is unmitigable within V2's decided constraints. Building quality validation that violates prior decisions to catch a problem whose blast radius is "rerun tomorrow" is not a justified trade.

### DECIDED: No Skip-and-Advance Behavior

The engine never silently drops an agent response, skips a round, or advances past a failed question. Every question either completes fully or the session halts. A Morning Brief generated from a session with holes would appear complete while missing potentially critical perspectives. Once an operator discovers a silent skip, they lose trust in every future session's completeness. The system's value depends on the operator believing the output covers what it claims to cover.

**Rationale:** This was the sharpest point of disagreement. The Orchestrator proposed skip-and-advance as graceful degradation. Every subsequent evaluator rejected it. The Oracle's framing was decisive: skip-and-advance poisons the well — it turns the Morning Brief from a trusted artifact into something that requires manual completeness verification.

### DECIDED: No New Monitoring Infrastructure

No dashboards, metrics services, health check endpoints, or structured logging frameworks for overnight operation. Errors are logged to the existing output mechanisms. The completion report (decided above) is the monitoring story. The live SSE dashboard exists for interactive use and is irrelevant to overnight batch operation.

**Rationale:** Consensus. The Architect proposed a `session_errors.log` file, which is reasonable but unnecessary given the completion report captures the same information in a more useful format. The system is a batch job processing design questions — engineer for diagnosability after the fact, not real-time observation.

---

## Summary

Reliable overnight operation requires exactly three additions to V1: exponential backoff on retries, a session duration cap, and a completion report. The engine runs sequentially, halts on failure, and resumes via the existing `--resume` mechanism. No external watchdogs, no skip logic, no quality validation, no monitoring services. The operator's morning experience is binary: either a complete Morning Brief is waiting, or a completion report explains where the session stopped and why.
<!-- complete -->
