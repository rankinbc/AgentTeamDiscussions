The disagreement spine is the missing step dressed up as a design. Step 1 is: who builds it, and what is the trigger? The Cognitive Architect says "engine-maintained" and "extracted, not smoothed." Extraction requires something to read every response, decide which claims contradict, and quote them. That is an LLM call, or a heuristic nobody has described. When it misidentifies a contradiction, or misses one, the sequence has no fallback. This is "the engine handles it" hand-waving, and it adds a whole new pipeline stage per round.

Smallest version that answers the question:

Step 1: before each agent's turn, the engine assembles the prompt from the question, the decided items, and the previous round's responses in full.
Step 2: the trigger for truncation is a measured size check on the assembled prompt against a configured budget (the existing defaults.yaml limits).
Step 3: when under budget, nothing is cut. Full history is the default, because most discussions never hit the limit.
Step 4: when over budget, drop the oldest whole rounds first, never partial responses. Question and decided items are never dropped.
Step 5: dropped rounds stay on disk in the transcript, so nothing is lost for synthesis.

The data flowing here is only prompt size and round order. No new component, no new state, no new LLM call.

The spine is a deferral candidate. The proposed experiment is sound, but run it only after the sliding window is observed to lose dissent in real sessions. Building the spine first optimizes a failure nobody has measured. Complexity is a cost, so justify the spine with evidence before it ships.

## Position Summary
I advocate full history by default with a size-triggered, oldest-whole-round-first window, keeping the question and decided items always. I reject the disagreement spine for now, and any summarization stage, because each adds an undefined extraction step with no fallback. Defer both until measurement shows the plain window loses dissent.
<!-- complete -->
