# Engineering robust multi-agent LLM discussion systems

Multi-agent LLM systems that produce project specifications face eight interlocking engineering challenges — from keeping agents at the right abstraction level to synthesizing their outputs without overwhelming context windows. This report distills current best practices (2024–2026) from academic research, framework architectures (AutoGen, CrewAI, LangGraph, MetaGPT, ChatDev), and practitioner experience into actionable patterns for a system using Claude CLI subprocess calls with YAML-configured agent personas.

The core insight across all research: **structured constraints beat free-form conversation**. Systems that enforce typed outputs, explicit cross-references, and phase-gated workflows consistently outperform unconstrained multi-agent chat. The second key finding is that multi-agent debate doesn't automatically improve quality — careful design of role differentiation, communication topology, and synthesis architecture matters far more than adding more agents or rounds.

---

## Keeping agents at the design altitude

The most common failure in spec-generation systems is agents dropping from architecture-level thinking into code and implementation details. Anthropic's own engineering team uses the term **"right altitude"** to describe the Goldilocks zone between brittle hardcoded logic and vague high-level guidance. Controlling altitude requires layered prompt engineering across four dimensions.

**Role framing** is the first and most effective layer. Position the agent as a CTO or enterprise architect reviewing decisions, not a developer implementing them. Research on role prompting consistently shows that explicit professional identity shifts communication style and abstraction level. The prompt "You are a senior enterprise architect evaluating system design decisions, not implementing them" fundamentally changes output character compared to a generic assistant prompt.

**Negative constraints with positive alternatives** form the second layer. Explicit prohibitions work best when paired with what the agent *should* do instead. A constraint block like "Do NOT write code, pseudocode, or SQL. Do NOT specify function signatures or class names. INSTEAD describe systems as components, interfaces, data flows, and responsibilities" creates a clear boundary. XML-tagged constraint sections are particularly effective with Claude, as the model uses tags as strong structural signals.

**Output templates** naturally preclude implementation detail by defining fields that only accept design-level content. An XML template with fields for `<responsibility>`, `<interfaces>`, `<data_flows>`, and `<constraints>` leaves no structural slot for code snippets. This is more reliable than prohibitions alone because it channels the model's generation toward the desired abstraction level rather than relying on it to inhibit unwanted behavior.

**Vocabulary-level constraints** restrict the agent's working terminology. Establishing an explicit vocabulary of design terms (components, modules, contracts, trade-offs, responsibilities) while prohibiting implementation vocabulary (functions, classes, variables, SQL) acts as a persistent altitude anchor. Martin Fowler's work on LLMs and abstractions reinforces that LLMs are most valuable as brainstorming partners at the design stage when you resist letting them generate core implementation.

A self-evaluation guardrail completes the system: instruct the agent to verify before responding whether it has accidentally dropped into implementation details, and to zoom back out if so.

---

## Making each agent genuinely different

Role differentiation is where most multi-agent systems fail silently. Without strong behavioral specialization, three agents produce three politely agreeable essays that converge on the same ideas — eliminating the diversity that justifies a multi-agent approach in the first place.

CrewAI's **role-goal-backstory framework** provides the strongest foundation. Each agent needs three distinct identity components: a role (job function), a goal (singular objective that creates tension with other agents' goals), and a backstory (experiential context that shapes judgment). The Cognitive Architect's goal might be "design systems that remain coherent and evolvable at scale," while the Systems Pragmatist's goal is "identify the simplest implementation that ships on time" — these goals naturally create productive tension without requiring explicit instructions to disagree.

**The agreement tax** is the most powerful technique for preventing convergent groupthink. Force agents to justify every agreement by identifying at least one weakness in the position they're endorsing, stating what specific evidence convinced them, and explaining what would need to be true for them to disagree. This creates genuine friction that surfaces different perspectives rather than allowing agents to default to polite consensus.

Making a skeptic agent actually challenge ideas requires several reinforcing techniques. First, **run Round 1 in parallel with no shared context** — this forces independent reasoning before cross-agent visibility, preventing anchoring on the first response. Second, give the skeptic agent an explicit mandate to challenge: "You are skeptical of other agents' reasoning by default. Only agree when forced to by evidence." Third, define emotional triggers in the persona — the Systems Pragmatist might be "allergic to over-engineering" and triggered by scope creep, unfounded optimism, and gold-plating.

Research from PersonaGym (2024) reveals that **model size and capability do not directly correlate with persona adherence** — a well-prompted smaller model can maintain character more consistently than a poorly-prompted larger one. The key techniques for consistency across multiple stateless calls are character sheets with core traits, speech patterns, and decision frameworks that get injected into every call, plus self-verification instructions asking "Does this response align with my established values? Would my persona say this, or am I defaulting to generic AI assistant behavior?"

Output type differentiation reinforces behavioral differentiation. The Cognitive Architect should produce component diagrams and trade-off analyses. The Systems Pragmatist should produce risk assessments and simplification recommendations. The Product Oracle should produce user impact analyses and prioritization frameworks. When each agent has a structurally different output format, behavioral convergence becomes physically impossible.

---

## Making agents aware of each other

Inter-agent awareness in a stateless subprocess architecture requires explicit context injection — agents cannot "remember" what other agents said unless the orchestrator tells them. Research identifies three communication topologies with distinct tradeoffs.

The **shared blackboard pattern**, revived from classical AI's Hearsay-II system and formalized for LLMs in the LbMAS framework (2025), provides central shared memory with public and private spaces. For subprocess-based systems, this translates to a JSON file on disk that each agent subprocess reads as context and writes contributions back to. The orchestrator updates the blackboard between calls. Experimental results show **13–57% improvement** over master-slave communication paradigms.

For a 3-agent spec discussion, the most effective pattern is the **Multi-Agent Debate (MAD) protocol**: independent generation in Round 1 (parallelizable), then iterative rounds where agents review others' responses and refine their own, followed by synthesis. The critical implementation detail for stateless CLI agents is prompt assembly — each call receives the system prompt, shared project state, other agents' outputs (explicitly labeled by agent name and round), and the task instruction for this round.

**Structured output formats dramatically improve cross-referencing quality.** JSON-based representations produce **40% better** summarization performance than plain text. A consistent schema across all agents should include proposals (with IDs for reference), explicit agreements and disagreements (with target IDs), and open questions. When the Systems Pragmatist can write `"disagrees_with": {"id": "P1", "agent": "architect", "reason": "microservices add operational complexity our 3-person team cannot support"}`, the cross-referencing becomes precise rather than vague.

XML context injection is particularly effective with Claude:

```xml
<agent_context>
  <previous_agent name="architect" round="1">
    <proposal id="P1">Event-driven architecture with message queue</proposal>
  </previous_agent>
  <previous_agent name="pragmatist" round="1">
    <critique target="P1">Message queues add operational overhead</critique>
  </previous_agent>
</agent_context>
<your_task>Respond to and build upon the above proposals from your Product Oracle perspective.</your_task>
```

Google's Agent Development Kit introduces a useful principle: **"Separate storage from presentation."** Store the full history durably, but compile a minimal, relevant working context for each LLM call. Each agent sees only what it needs, reducing noise and keeping responses focused.

---

## Maintaining memory across stateless calls

Each subprocess call to Claude CLI starts with zero state, making memory management the orchestrator's responsibility. The naive approach of sending full conversation history fails through cost spiraling, signal degradation from the "lost in the middle" effect, and physical context limits.

The most effective architecture uses a **multi-tier context window**. Tier 1 (full fidelity) retains the last 3–5 turns verbatim. Tier 2 (compressed) extracts key decisions and facts from turns 6–15. Tier 3 (summary) condenses all older content into a rolling summary paragraph. Research from the University of Washington NLP group found that **12-message windows** (6 exchanges) provide optimal balance for task-oriented dialogue.

**Rolling summary with anchoring** is the recommended summarization approach. Rather than regenerating the entire summary each round (which scales O(n) per turn), the Factory.ai pattern maintains a persistent summary that gets incrementally updated: only the newly dropped content span is summarized and merged. This keeps summarization cost at O(1) per turn while preserving continuity.

For multi-round spec discussions, a structured **decisions ledger** should be maintained separately from conversation history. This JSON object tracks decided items (with agreement attribution and round number), items under active discussion (with each agent's position), and open questions. The ledger gets injected as high-priority context in every agent call, separate from the conversation summary, because it represents the persistent "project state" that must survive all levels of compression.

JetBrains Research (December 2025) found that **observation masking** — selectively hiding verbose outputs from older turns while preserving the agent's reasoning and decisions — matched LLM summarization in cost savings and problem-solving ability with simpler implementation. For a spec discussion system, this means retaining each agent's key proposals and critiques while dropping the surrounding explanatory text.

The recommended per-round context assembly for a 3-agent system allocates roughly **5,200 tokens per agent call**: ~500 for the system prompt, ~500 for the project state/decisions ledger, ~1,000 for the rolling summary of older rounds, ~3,000 for full context from the previous round (all 3 agents), and ~200 for the current task instruction. This budget scales linearly with round count only through the rolling summary component, which grows slowly by design.

---

## Controlling output length without losing substance

Verbose agent responses cause two failures in automated systems: timeouts on subprocess calls and context overflow when responses feed into subsequent rounds. Controlling length requires combining prompt-based instructions with hard technical limits.

The `max_tokens` parameter is a **hard bound that truncates, not a conciseness instruction** — it cuts output off rather than making it denser. Effective length control pairs max_tokens as a safety net with prompt-based instructions for quality conciseness. The recommended approach from Statsig (2025) is to set a target length in the prompt and back it up with strict max_tokens.

**Anti-slop patterns** eliminate the filler that inflates agent outputs. Hamel Husain's widely-cited guidelines distill this to: make every sentence information-dense, shorter words are better, fewer words are better, cut transitional fluff ("Understanding X helps you Y"), remove setup phrases ("It's worth noting that"), and trust the reader's intelligence. For the system prompt, a direct instruction like "No corporate jargon. No flowery language. No filler phrases. Start with your strongest point" reportedly eliminates the majority of generic padding.

**Structured output templates naturally constrain length** more reliably than word count instructions alone. An XML template with defined fields and item limits (e.g., "max 3 risks, max 2 open questions, rationale in 2–3 sentences") produces consistently sized outputs because the structure itself defines the content boundaries. JSON schemas with `maxItems` and `maxLength` constraints offer similar structural enforcement.

Additional techniques for automated systems include lowering temperature to **0.3–0.5** (more focused, potentially shorter outputs), using stop sequences to terminate at natural breakpoints, and pre-filling the assistant response opening to bypass conversational preamble. An explicit framing like "CRITICAL: This response will be processed by an automated system. No conversational preamble. No meta-commentary. Begin directly with content" prevents the padding that Claude naturally adds in conversational contexts.

---

## Synthesis architectures beyond naive concatenation

The "collect all agent responses then synthesize in one call" pattern breaks when three agents each produce 4,000 tokens — the synthesizer must process 12,000+ tokens of input, often producing degraded output due to the "lost in the middle" effect. Three alternative architectures scale better.

**The Refine Chain** starts with one agent's output as the initial draft, then sequentially folds in each subsequent agent's output. The synthesizer processes the current draft (~2,000 tokens) plus one new agent's key points (~1,000 tokens) at each step. This produces **higher coherence** than map-reduce because each refinement step builds on an integrated document. LangChain's RefineChain implementation adds a key instruction: "Only incorporate content from the additional input if it adds useful information; otherwise return the current draft unchanged."

**Map-Reduce** independently processes each agent's output (extracting key points, compressing, or evaluating), then combines the mapped results. The LLM×MapReduce framework (ACL 2025) adds confidence scores to each chunk's output, allowing the reduce step to resolve inter-chunk conflicts. For a 3-agent system, the map phase extracts structured data from each agent's free-text response, and the reduce phase merges these structured artifacts.

**Hierarchical tournament synthesis** works best when scaling beyond 3 agents: pairwise comparisons eliminate weaker positions, then surviving positions are synthesized. Research on pairwise reward models with knockout tournaments shows this consistently outperforms majority voting and absolute scoring.

For the specific 3-agent spec system, the **recommended hybrid approach** runs four phases. Phase 1: parallel generation (3 calls). Phase 2: extract and align — for structured JSON outputs, this can be done by orchestrator code with no LLM call. Phase 3: incremental refinement (2 sequential calls, each folding in one agent's contributions). Phase 4: optional validation pass back to each agent for sign-off. This totals 5 LLM calls, each processing 3–4K tokens, rather than 4 calls with one processing 15K tokens.

Google Research's **Chain-of-Agents** (NeurIPS 2024) demonstrates that sequential agent processing with progressive context building outperforms RAG and full-context baselines by **up to 10%**, even comparing 8K-token CoA windows against 200K full-context baselines. The progressive refinement pattern inherently manages context better than parallel-then-aggregate approaches.

---

## Testing whether your prompt rules actually work

Prompt engineering for multi-agent systems is meaningless without validation that behavioral rules actually change agent behavior. The evaluation landscape has matured significantly, with layered approaches combining deterministic checks, LLM-as-judge scoring, and human calibration.

**Promptfoo** is the leading open-source tool for test-driven prompt engineering. Its YAML-based test configs support `llm-rubric` assertions that use an LLM to evaluate semantic properties — ideal for testing whether an agent maintains its persona. It integrates into CI/CD via GitHub Actions, posting results as PR comments and blocking merges when success rates drop below thresholds. For multi-agent systems, define test suites per agent that evaluate role-specific behaviors.

**DeepEval** provides a dedicated `RoleAdherenceMetric` that iterates over each assistant turn and uses an LLM to evaluate whether content adheres to the specified role. The score equals the ratio of role-adherent turns to total turns — a direct, quantifiable measure of persona consistency. This is the most turnkey solution for the specific problem of testing agent character maintenance.

For testing the agreement tax, create an **LLM-judge rubric** that scores constructive disagreement on a 1–5 scale: 5 for identifying specific flaws and proposing alternatives, 3 for agreeing while noting one limitation, 1 for full agreement without unique perspective. Run this evaluation across a corpus of test scenarios and track the distribution. If most responses score 1–2, the agreement tax prompt isn't working.

The recommended **layered evaluation approach** combines three levels. Layer 1: deterministic checks — JSON schema validation, token count limits, regex matching against banned phrases (anti-slop patterns). Layer 2: LLM-as-judge — rubric-based scoring for abstraction level adherence, role consistency, cross-referencing quality, and constructive disagreement rate. Layer 3: human review — calibration samples to verify that automated metrics correlate with actual quality. Research shows strong LLM judges achieve **80–90% agreement** with human evaluators, comparable to inter-annotator agreement between humans, but known biases (verbosity preference, position bias) require calibration.

Build regression test suites with 20–50 representative scenarios per agent covering core use cases, edge cases, and known failure modes. Version control prompts alongside test configs, set minimum pass rates as quality gates, and run nightly regression against all agents to catch model-update-induced behavioral shifts.

---

## Detecting and correcting drift in real time

Agent drift — progressive degradation of behavior across interactions — manifests as semantic drift (deviation from original intent), coordination drift (breakdown in multi-agent consensus), and behavioral drift (emergence of unintended shortcuts). Research from Rath (2026) shows that **semantic drift appears in roughly 50% of multi-agent workflows by 600 interactions**, making detection and correction essential for production systems.

**Shannon entropy provides the fastest slop detection** — character-level entropy distinguishes meaningful content from filler at 10x the speed of LLM-as-judge approaches with zero API cost. Professional prose maintains entropy consistently above 4.5, while AI slop ("I apologize for the confusion…") drops below 3.2. A threshold of 3.5 acts as a reality lock: outputs below this entropy trigger automatic regeneration.

The **Antislop framework** (ICLR 2026) takes a more systematic approach, using automated profiling to compare model overuse patterns against human baselines. Some slop patterns appear over **1,000x more frequently** in LLM output than in human text. The framework's backtracking-based suppression scans generated text for banned patterns, backtracks to the pattern's first token, reduces its probability, and resamples — achieving 90% slop reduction while maintaining task performance.

For the 3-agent system, implement a **quality gate between rounds** with a four-stage validation pipeline. First, regex check against the anti-slop phrase list. Second, Shannon entropy check with the 3.5 threshold. Third, word count verification against per-agent limits. Fourth, LLM-judge evaluation of role adherence (more expensive, run selectively or on a sampling basis). Failed outputs trigger regeneration with specific feedback: "Your previous response was rejected because [reason]. Regenerate with these corrections."

**Cap retries at three attempts** — beyond this, escalate to human review or fall back to a simpler prompt. Use progressive constraint tightening: the first retry adds a gentle nudge, the second adds explicit constraints, the third uses few-shot examples of desired output. For severe drift detected via the Agent Stability Index composite metric, the nuclear option is a context reset: clear accumulated context and reinitialize from baseline prompts.

Self-reflection prompts embedded in system prompts ("Before responding, verify: Does this response reflect my assigned role? Am I at the correct abstraction level? Am I genuinely adding perspective or just agreeing?") act as a lightweight continuous guardrail. The Reflexion pattern formalizes this: generate → self-evaluate → produce verbal reinforcement signal → regenerate if needed. This creates an iterative self-improvement loop without external critic agents.

---

## What the frameworks teach us about architecture

Five major multi-agent frameworks offer distinct architectural patterns transferable to a spec-generation system.

**MetaGPT's structured artifacts pattern** is the most directly relevant. Instead of free-form chat, MetaGPT requires agents to produce structured deliverables (PRDs, design documents, API specs) at each phase. This dramatically reduces hallucination cascading because downstream agents parse structured inputs rather than interpreting free text. Its publish-subscribe message pool, where agents publish outputs and subscribe to relevant content by type rather than engaging in direct conversation, is more efficient than group chat for complex workflows.

**LangGraph's typed shared state with reducers** solves the concurrent update problem. A defined `TypedDict` state schema specifies exactly which fields flow between agents. Reducer functions control how multiple agents' updates merge — append to lists, overwrite scalars, or custom logic. For a subprocess-based system, this translates to a JSON state file with merge rules enforced by the orchestrator. LangGraph's built-in checkpointing supports resuming long discussions and "time-travel" debugging.

**CrewAI's role-goal-backstory triple** produces measurably more focused agent behavior than bare system prompts. The framework also offers dual orchestration: autonomous crews for adaptive collaboration and deterministic flows for phase-gated processes. Its memory system spans short-term, long-term, entity, and contextual layers shared across agents — a useful reference architecture even if implementing from scratch.

**ChatDev's communicative dehallucination** is a simple technique with outsized impact: prompt agents to request clarification and specific details before producing outputs. This single pattern significantly reduces hallucination in generated content. ChatDev's phase-based chat chain — where the full process decomposes into focused pairwise interactions between specific agent pairs — prevents the scope creep common in open group discussions.

**AutoGen's conversation-as-programming** model treats agent interactions as a flexible control flow that adapts based on content, with pluggable auto-reply functions and termination conditions. Its v0.4 actor model decouples message delivery from handling, improving modularity.

Recent research on **Mixture-of-Agents** (MoA) reveals that LLMs generate better responses when presented with outputs from other models, even less capable ones — a phenomenon called "collaborativeness." Critically, 2025 follow-up research found that **Self-MoA (same model, different prompts) outperforms mixed-model MoA**, validating the approach of using multiple Claude instances with different role prompts rather than mixing different LLM providers. The MAD literature cautions that multi-agent debate does not reliably outperform single-agent strategies without careful tuning of agent personas, round counts, and aggregation — simple debate isn't automatically better.

---

## Conclusion: an integrated architecture for spec generation

The research converges on an architecture that layers several patterns. Define agents with CrewAI-style role-goal-backstory triples and MetaGPT-style structured output schemas, not just system prompts. Use a shared blackboard (JSON state file) with a decisions ledger tracking agreements, disagreements, and open questions separately from conversation content. Implement multi-tier context management with full-fidelity recent rounds, compressed older rounds, and a rolling summary, targeting roughly 5,200 tokens of context per agent call.

Run discussions in phases (requirements → architecture → review → consolidation) rather than open-ended group chat. Within each phase, use parallel-then-critique rounds: independent generation first (preventing anchoring), then cross-referencing with mandatory agreement taxes. Gate every agent output through a fast validation pipeline (regex + entropy + length check) before it enters the shared state, with LLM-judge evaluation on a sampling basis. Synthesize using the refine chain pattern rather than naive concatenation.

The most underappreciated insight from the literature is that **the orchestrator's design matters more than the agents' prompts**. How context is assembled, when agents see each other's work, what validation gates exist between rounds, and how synthesis scales — these architectural decisions determine system quality more than any individual prompt optimization. Build the evaluation infrastructure first (promptfoo test suites, entropy-based slop detection, role adherence metrics), then iterate on prompts with confidence that changes produce measurable improvements.