### The Product Oracle (user advocate)

# EVALUATE — The Product Oracle

**Verdict: The Systems Pragmatist wins. The Cognitive Architect's middle layer is intellectually elegant but solves a problem the user never asked about.**

Work backward from the Morning Brief. The user reads it and either thinks "this surfaced something I wouldn't have considered alone" or doesn't. That judgment takes thirty seconds. No structural prompt assertion, no temporal regression detector, no embedding metric will ever replace that thirty-second read.

The Pragmatist's position survives because it respects what's already been decided: paired human comparison is the validation framework, measurement infrastructure is a spreadsheet, five paired runs before declaring anything. Mechanical tests protect the plumbing — blind exclusion works, token caps hold, templates resolve correctly. Everything else is the human's call.

The Cognitive Architect wants to test whether prompts contain "structural preconditions for genuine divergence." That sounds rigorous until you ask: who defines those preconditions? The answer is the builder, iterating on output quality, which is exactly what paired comparison already covers. You'd be writing tests to encode hypotheses about what makes prompts work — hypotheses that change every time you read a Morning Brief and think "that agent was too agreeable." Those tests become maintenance burden that encodes yesterday's assumptions.

The Adversarial Critic's temporal regression point is real but premature at N < 20 runs. You can't detect drift without a baseline, and you don't have a baseline yet.

**Ship mechanical tests for mechanical things. Read the Morning Brief for everything else. Revisit when you've done twenty runs and actually have data.**

## Position Summary
I advocate the Pragmatist's minimal mechanical testing focused on V2 prompt assembly correctness, with all quality validation deferred to the already-decided paired human comparison framework. I reject the structural middle layer because it encodes unfalsifiable hypotheses about what makes prompts effective, creating maintenance burden without improving user-perceived output. The user's thirty-second read of the Morning Brief is a better quality signal than any automated proxy we could build at this scale.

### The Context Surgeon (context efficiency evaluator)

# EVALUATE — The Context Surgeon

**Verdict: The Pragmatist wins. But everyone is ignoring the elephant: this very discussion is exhibit A of the problem it's debating.**

Look at the context stuffed into this prompt. The "What's Already Decided" section appears *twice* — identical content, verbatim duplicated. The "Prior Design Docs" repeats a subset of those same decisions a *third* time. That's roughly 800 tokens of pure waste in a system supposedly concerned with context window management.

The Pragmatist is right that mechanical tests on prompt assembly are the only defensible automated layer. But I'll sharpen the point: the *first* mechanical test should verify that PromptBuilder doesn't stuff duplicate context into agent prompts. Because if the engine's own session briefs look like this prompt — redundant blocks, human-readable headers burning tokens, decisions repeated for emphasis rather than information — then no amount of quality framework matters. The agents are reading padding instead of substance.

The Cognitive Architect's "structural preconditions" idea fails for the reason the Oracle identified, but also for a simpler one: it's untestable without a ground truth corpus you don't have and won't have at N=5.

The Critic's temporal regression point would matter if you had stable inputs. You don't. Every brief is different. You're comparing apples to oranges and calling it drift detection.

One addition to the Pragmatist's list: test token utilization. Assert that rendered prompts use >70% of available budget on *novel* content per round, not restated context. That's mechanical, measurable, and directly impacts the quality everyone else is hand-waving about.

## Position Summary
I advocate the Pragmatist's minimal mechanical testing plus one addition: token utilization assertions that verify prompts maximize novel content over restated context. I reject the structural middle layer and temporal regression detection as requiring statistical foundations this project lacks. The highest-leverage mechanical test you can write today is ensuring your engine doesn't waste context budget the way this very prompt does.


<!-- complete -->
