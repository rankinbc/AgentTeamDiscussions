# V1 Orchestrator Spec Gaps

An adversarial review of the V1 orchestrator spec found 13 issues. These are the top 7 that need design decisions before implementation.

## What's Already Decided

- V1 is a single-team, single-phase discussion system (no MCP, no two-team, no BackgroundAgents, no magnitude)
- Agents are configured via YAML and invoked as stateless `claude -p` CLI calls
- Structured 3-round discussions: propose -> critique -> evaluate -> synthesize
- Session output goes to a timestamped folder with design docs, transcripts, decisions, and a Morning Brief
- The beta experiment system (run_discussion.py) has the working orchestration loop
- Each question produces: a design doc, a transcript, extracted decisions, and extracted open questions
- Prior design docs chain forward as context for subsequent questions
- The evaluator (evaluate_experiment.py) scores output on behavioral and quality dimensions

## Open Questions

1. **How does the Morning Brief get generated?** The Morning Brief is the only artifact the user actually reads. It needs a specific prompt, input strategy (what if 10 design docs exceed context?), output format, and a way to surface risk flags from critic rounds. Design the prompt, the input assembly, and the fallback if the call fails. Consider: should the brief be generated incrementally (after each question) or all-at-once at the end?

2. **How does decision extraction work?** Design docs are free-form markdown from an LLM synthesis call. We need to extract structured decisions with confidence scores into decisions.json. What prompt extracts decisions? What schema does decisions.json follow? How does the extractor distinguish a firm decision from a recommendation from a suggestion? What happens when the extractor produces garbage?

3. **What is the error handling strategy?** A 10-question session makes 70+ LLM calls. Failures are guaranteed. Design the failure strategy: what gets retried, what gets skipped, what gets saved on partial failure. If question 6 of 10 fails, do we skip it and continue? Do we save the partial transcript? What does the Morning Brief say about failed questions? What if synthesis fails but all rounds succeeded?

4. **How do we keep the synthesis step from being a bottleneck?** The synthesis call receives all agent responses (potentially 9000+ words) plus prior context and must produce a coherent design doc. In beta, this is the slowest and most failure-prone step. How do we make it more reliable? Options: chunk the input, use a two-pass approach (outline then fill), add a retry with simplified input on failure, or accept degraded output over no output.

5. **How does prior context get managed as questions accumulate?** By question 8 of 10, there are 7 prior design docs. The beta system truncates to 6000 chars. What is the right strategy? Summarize prior docs into a compressed context? Keep only decisions and open questions? Use a sliding window? The answer affects whether later questions build coherently on earlier ones or drift.

6. **What does session recovery look like?** If the process crashes at question 5 of 10, what state is on disk? Can the user restart and pick up at question 6? What file marks progress? What does the Morning Brief say about incomplete sessions? Design the checkpoint strategy.

7. **How do we make the evaluation feedback loop reliable?** The evaluator currently lets the LLM invent its own scoring dimensions instead of using the specified ones. Scores are not comparable across runs. How do we fix this so the iterate-and-improve loop actually works? Should we post-process LLM responses to extract scores by expected dimension names? Use a different evaluation approach entirely?
