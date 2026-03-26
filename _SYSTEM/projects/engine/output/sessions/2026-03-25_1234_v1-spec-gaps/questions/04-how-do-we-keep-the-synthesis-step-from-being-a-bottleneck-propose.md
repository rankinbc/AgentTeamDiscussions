### The Cognitive Architect (creativity engine designer)

**The bottleneck is semantic density, not word count.**

9000 words of agent transcript contains roughly 400 words of actual signal — distinct positions, key objections, pivots. The rest is elaboration, hedging, and re-statement. Passing the full transcript to synthesis asks the LLM to do compression *and* synthesis simultaneously. That's why it fails.

**My proposal: per-agent position extraction, inline.**

After each agent speaks in the critique and evaluate rounds, extract a one-paragraph "position summary" as part of the round mechanics — not a separate call, just a structured field appended to the agent's turn output. By the time synthesis fires, you already have 6-7 position summaries (~150 words each, ~1000 words total) instead of raw transcript.

The synthesizer receives: position summaries + fragment log (already decided) + the question. Not the transcript. The transcript remains in the session folder as the archival record; synthesis never touches it.

This isn't chunking. Chunking preserves noise in smaller buckets. Position extraction preserves *stance* — which is what the design doc actually needs to arbitrate between.

**Why this produces better output, not just more reliable output:** synthesis reasoning over "Architect proposed X for reason Y, Critic challenged on Z" is structurally superior to synthesis reasoning over 1500 words of back-and-forth. The compression is lossy on prose but lossless on the decision surface.

**Retry policy for synthesis:** 2 retries, 30-second backoff, then deterministic concatenation of position summaries into the three-section framing. This resolves that open question — and deterministic fallback on position summaries is meaningfully better than fallback on raw fragments.

**Threshold for majority-failure abort:** config key `min_success_fraction`, default `0.5`. Hardcoding is fragile for sessions with different question counts.

### The Flow Orchestrator (mechanical flow designer)

**The 9000-word problem is already solved. We decided it two questions ago.**

Synthesis receives the fragment log, not the transcript. That's ~1150 tokens total — already decided, already budgeted. Per-agent position extraction is redundant complexity added on top of a decision that already constrains the input. I'm rejecting it.

The actual open questions here are operational, not architectural. Let me close them.

**Retry policy for synthesis:** 2 retries, 30-second backoff, then deterministic concatenation of fragment fields into three-section framing. This matches the extraction call policy for consistency and resolves the open question. No new decision surface.

**Majority-failure threshold:** Config key `min_success_fraction`, default `0.5`. Agreed with the Architect on this one — hardcoding fails silently on 3-question sessions where one failure hits 33% and on 10-question sessions where four failures hit 40%. A config key costs nothing.

**One sequencing flag:** The synthesis call must not fire until all fragment extraction calls have completed or timed out — including sentinel writes for failed extractions. If synthesis fires while fragments are still pending, it reads a partial log. The session loop needs an explicit sync point here before invoking synthesis. This is not "the orchestrator handles it" — it's a concrete gate: all `extraction_task` futures must be awaited before synthesis begins.

The Architect's proposal adds 12 modified agent calls to solve a token budget problem that the fragment log already solved. That's the wrong direction.


<!-- complete -->
