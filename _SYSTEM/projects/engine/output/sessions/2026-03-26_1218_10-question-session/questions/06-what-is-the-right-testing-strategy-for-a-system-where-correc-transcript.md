# Transcript: What is the right testing strategy for a system where correctness is subjective?

*Generated: 2026-03-26 12:39*

## Round: PROPOSE

### The Flow Orchestrator (mechanical flow designer)

Split the problem at the seam that's already there: mechanical correctness vs. output quality. These are different testing problems with different strategies. Stop conflating them.

**Mechanical tests (deterministic, automated):**
- Config loads and validates without error
- Prompt assembly produces expected output given known inputs
- Session state transitions follow legal sequences
- Crash recovery restores to last completion marker
- Feature flags gate the correct code paths
- Token budgets stay within hard caps
- Eviction order matches the hardcoded priority queue

These are standard unit/integration tests. Write them. No controversy here.

**Output quality tests (subjective, human):**
Already decided. Paired human comparison, five runs, spreadsheet. That IS the testing strategy for subjective quality. Adding LLM-as-judge or embedding metrics contradicts the decisions against automated divergence scoring and runtime instrumentation.

**The gap people will want to fill but shouldn't:**
There's a tempting middle layer — "did the prompt contain the right sections," "did blind mode actually withhold prior responses." These are mechanical checks disguised as quality checks. Test the prompt assembly output directly. If `PromptBuilder` produces a prompt without a prior-response block during blind rounds, that's a unit test. Don't dress it up as quality validation.

**What I'd cut from this conversation entirely:**
LLM-as-judge. It adds a dependency, introduces its own subjectivity, and we decided against automated scoring. Embedding diversity metrics — same problem, more infrastructure, no clear threshold for "enough diversity."

The testing strategy is already decided. The question is whether we write the mechanical tests thoroughly enough.

## Position Summary
I advocate splitting testing cleanly into mechanical (automated unit/integration) and quality (the already-decided paired human comparison), with no middle layer. I reject LLM-as-judge, embedding metrics, and any automated quality scoring because they contradict existing decisions and add infrastructure we explicitly chose not to build. The real risk isn't missing a clever testing technique — it's writing too few mechanical tests and then blaming output quality when the prompt assembly was simply wrong.

### The Cognitive Architect (creativity engine designer)

Flow Orchestrator's split is clean. Too clean. The mechanical/subjective binary obscures the most important testing surface: **whether the prompts are structurally designed to produce friction in the first place.**

You can't test whether a discussion produced genuine intellectual friction — agreed. But you absolutely can test whether the prompt *set up the conditions* for friction, and that's mechanical. This isn't prompt assembly correctness (did the template render). It's prompt design validation: does the blind-round prompt actually forbid hedging language? Does the critique prompt force agents to name a specific claim they reject? Does the identity block contain a position that *conflicts* with at least one other agent's position on the team?

Creativity research is unambiguous here: divergent output requires **structural conflict in the inputs**. Charlan Nemeth's work on authentic dissent shows groups produce better solutions when disagreement is *built into the starting conditions*, not left to emerge. Testing the starting conditions is mechanical. Testing the output is subjective. Flow Orchestrator collapses both into "just test prompt assembly," which misses that a perfectly assembled prompt can be structurally toothless.

Concretely: write tests that parse the rendered prompt and assert the presence of constraint language, position-taking requirements, and cross-agent tension points. These aren't quality tests. They're structural tests on the *design* of the intervention, not measurement of its effect.

I agree LLM-as-judge and embedding metrics are out — the decisions are clear. But "write more mechanical tests" is insufficient guidance without specifying *what properties* the mechanical tests should assert.

## Position Summary
I advocate testing prompt design properties — structural conflict, constraint language, position-forcing requirements — as mechanical assertions on rendered prompts, not output quality. I reject the clean mechanical/subjective binary because it ignores the testable middle layer: whether prompts contain the structural preconditions that creativity research identifies as necessary for genuine divergence. The gap isn't test quantity — it's that nobody has specified what the mechanical tests should actually verify about prompt content.

## Round: CRITIQUE

### The Adversarial Critic (adversarial reviewer)

Both proposals share a dangerous assumption: that you can meaningfully test prompt structure without testing what it produces. The Cognitive Architect's "testable middle layer" sounds rigorous — assert that prompts contain conflict-forcing language, position requirements, constraint patterns. But this is cargo cult testing. You're verifying the presence of incantations, not their efficacy.

Here's the failure scenario: You write 50 assertions confirming every prompt contains "challenge the previous response" and "argue from your unique position." Tests pass. Output is still sycophantic garbage because the *combination* of instructions, context length, and model behavior produces convergence regardless of what structural tokens you injected. You've built a green test suite that proves nothing.

The Flow Orchestrator's clean binary is equally fragile. "Mechanical tests for assembly, human comparison for quality" assumes assembly correctness and output quality are independent variables. They aren't. A prompt that assembles correctly per spec can systematically produce worse discussions than one with a "bug" that accidentally creates productive tension. Your mechanical tests become a false floor — everything passes, output degrades, and you can't trace why because your test boundary explicitly excludes the connection between the two.

The unstated assumption both share: that prompt content is *stable enough* to assert against. Claude's behavior shifts across versions. A structural assertion valid today — "contains adversarial framing" — means nothing when the model's response to that framing changes. You're testing the letter, not the envelope.

Five paired runs won't surface this. You need regression detection *across time*, which neither proposal addresses.

## Position Summary
I advocate treating prompt-to-output coupling as the primary test target rather than testing prompts and outputs in isolation. I reject both the clean mechanical/subjective binary and the structural middle layer because both assume prompt content predicts output behavior, which is unfalsifiable without the output. The real gap is temporal regression detection — knowing when previously-effective prompts stop working — which neither proposal even acknowledges.

### The Systems Pragmatist (infrastructure realist)

The Adversarial Critic is right that prompt-to-output coupling matters, but wrong about the prescription. "Temporal regression detection" sounds great until you ask: detection against what baseline? You need stable output to detect drift. But you've already decided output quality is subjective and measured by human comparison at N<20. You can't build regression detection on a foundation of five paired runs and a spreadsheet. The math doesn't work. You're proposing infrastructure that requires statistical power you explicitly chose not to invest in.

Here's what actually breaks first: nothing gets tested at all.

Every proposal here is debating the *shape* of the test suite while ignoring that this is a side project with YAML configs, Scriban templates, and subprocess calls to `claude -p`. The blast radius of a prompt assembly bug is one wasted session — maybe 20 minutes of compute. The blast radius of spending two weeks building a "structural assertion framework" for prompt content is two weeks of not shipping blind proposals.

The Cognitive Architect wants to assert prompts contain conflict-forcing language. Fine — write three tests. Not fifty. Assert the blind proposal round excludes prior responses. Assert agent identity stays under 800 tokens. Assert round-type selects the correct template. That's your mechanical floor. Everything else is quality, and you already decided that's human judgment over paired runs.

The dangerous shared assumption isn't about prompt stability or testing boundaries. It's that this system needs a sophisticated testing strategy at all. You have 78 tests covering config and persistence. You need maybe 10 more covering V2 prompt assembly. The rest is the spreadsheet you already committed to.

## Position Summary
I advocate minimal, targeted mechanical tests on V2 prompt assembly (blind exclusion, token caps, template selection) with everything else deferred to the already-decided paired human comparison. I reject both the structural middle layer and temporal regression detection as overengineering that assumes scale and statistical power this project doesn't have. The real risk is analysis paralysis about testing strategy delaying the features that actually need validating.

## Round: EVALUATE

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
