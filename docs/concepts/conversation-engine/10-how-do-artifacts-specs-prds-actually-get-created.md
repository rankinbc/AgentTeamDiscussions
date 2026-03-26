# How do artifacts (specs, PRDs) actually get created?

*Generated: 2026-03-17 22:05 | Question 10 | 202s*

The file is ready to write -- I need permission to save to the output directory. Could you approve the file write to `output/spec_artifact_creation.md`?

Here's what the synthesized spec covers -- 14 sections distilled from all six panel voices across three rounds:

**Core decision: Dedicated `claude -p` calls, phase-triggered, single drafter with team critique.**

1. **Core Decision** -- Artifacts are created via separate calls, not inline during discussion. Lossy discussion and lossless artifacts don't mix.

2. **Trigger** -- The phase engine triggers artifact creation, not individual agents. Agents can propose transitions but the phase engine confirms against defined criteria.

3. **Convergence Definition (Provisional)** -- Cross-team magnitude agreement above threshold 6. Disagreements are annotated, not suppressed. Formal definition deferred to phase engine spec (blocking dependency).

4. **Drafting Model** -- Single designated agent per artifact type (PM drafts PRDs, architect drafts specs). Multi-drafter synthesis rejected on token math grounds. Other agents quality-check through in-round critique.

5. **Drafting Call Specification** -- Fifth call type alongside Save/Think/Talk/Curate. Input: decision log, relevant stances, artifact template. Explicitly excluded: full transcript, raw magnitudes, other agents' save files.

6. **Review and Revision Loop** -- Cap at 2 revisions. Force-accept with annotated dissent on third attempt. Each revision costs 30-50k input tokens.

7. **Artifact Feedback** -- 500-token summary enters curator pipeline. Full artifact available via MCP tool call. Prevents situation block inflation.

8. **Finalization** -- Accepted artifacts write to session output with traceability, dissent annotations, and metadata.

9. **Cost Summary** -- 360-600k tokens worst case for 4 artifacts (6-10% of session budget). Hard constraint: artifact spend must not exceed one discussion round's spend.

10. **Failure Contract** -- Skip and log at every stage. No silent corruption. Consistent with system-wide policy.

11. **Observability** -- Six logging points from trigger through finalization.

12. **What Agents Never See** -- Consistent with prior specs (no raw magnitudes, no other save files, no BackgroundAgent actions).

13. **Open Items** -- 10 items, 4 blocking (convergence metric, artifact templates, curator prompt versioning, thinking routine templates).

14. **Design Rationale** -- Why dedicated calls, why single drafter, why 2 revisions not 3, why summary not full artifact, why phase-triggered not agent-triggered.