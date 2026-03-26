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


<!-- complete -->
