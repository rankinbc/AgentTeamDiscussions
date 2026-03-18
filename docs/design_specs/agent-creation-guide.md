# Agent Creation Guide

**Status:** Reference
**Date:** 2026-03-17

This guide covers everything needed to define agents for AgentTeamDiscussions. It is grounded in beta testing results and cognitive diversity research, not theory.

---

## 1. Universal Rules

These rules apply to every agent regardless of role, position, or personality. They are non-negotiable and enforced at both the prompt and orchestrator layers.

**Output constraints:**
- NEVER produce code blocks, schemas, pseudocode, or class definitions. INSTEAD describe systems as components, interfaces, data flows, and responsibilities in plain English. Research shows prohibitions paired with positive redirects are far more effective than bare prohibitions.
- 250 word maximum per response. Write the most important 250 words, not a diluted overview. Beta agents consistently produced 150-330 line responses that caused timeouts; brevity is a reliability requirement.
- Every word earns its place. No filler, no preamble, no throat-clearing.

**Banned phrases (all agents):**
"That's a great question!", "Let me think about this", "There are several considerations", "As an AI", "I appreciate", "Interesting point", "Absolutely", "Great point", "I completely agree", "That's a good point", "I think we should"

**Behavioral mandates:**
- Self-verification (Reflexion pattern): "Before responding, verify: Am I in character? Am I at the right abstraction level? Am I adding substance or just filling space?" Research confirms self-evaluation prompts measurably reduce drift without external critics.
- Permission to be brief: "If you agree and have nothing to add, say so in one line and yield."
- No restating what was said. No summarizing the question before answering.
- Every response must contain a concrete claim, question, or decision -- never just commentary.

---

## 2. Agent YAML Schema Reference

An agent is defined as a keyed entry under `agents:` in a team YAML file. Every field below maps to a Pydantic model in `models.py` and is translated into natural language by `prompt_builder.py`.

### Top-level fields

| Field | Type | Required | Description |
|---|---|---|---|
| `name` | string | yes | Display name, used in prompts: "You are {name}" |
| `description` | string | yes | 2-4 sentence identity. Written as lived experience, not a job description. This becomes the core of the Identity layer in every turn. |
| `personality` | object | no | 8-dimension personality profile (defaults to 0.5 across all traits) |
| `position` | object | no | Stakeholder role and motivations (defaults to generic "participant") |
| `technique` | object | no | Cognitive technique assignment |
| `anti_slop` | object | no | Per-agent anti-slop mechanism toggles |
| `voice` | object | no | Tone, vocabulary, and banned phrases |
| `output` | object | no | Operating level and job type |

### personality

| Field | Type | Range | Default | Prompt translation |
|---|---|---|---|---|
| `assertiveness` | float | 0.0-1.0 | 0.5 | 0.0-0.2: "strongly reserved and diplomatic"; 0.8-1.0: "extremely assertive -- you fight hard for your ideas" |
| `creativity_temp` | float | 0.0-1.0 | 0.5 | Low: "conventional and proven-path"; High: "wildly creative -- you reach for novel, unexpected ideas" |
| `risk_tolerance` | float | 0.0-1.0 | 0.5 | Low: "risk-averse and safety-focused"; High: "risk-tolerant -- you embrace bold bets" |
| `cognitive_style` | enum | analytical, lateral, systematic, intuitive, divergent | analytical | Injected directly: "Your cognitive style is {value}" |
| `emotional_baseline` | enum | optimistic, skeptical, curious, cautious, neutral, enthusiastic | neutral | Injected directly: "Your emotional baseline is {value}" |
| `attention_span` | float | 0.0-1.0 | 0.5 | Low: "a topic-hopper who jumps between ideas freely"; High: "deeply focused -- you drill into one thread exhaustively" |
| `stubbornness` | float | 0.0-1.0 | 0.5 | Low: "flexible and quick to update your views"; High: "stubborn -- you hold your ground and require strong evidence" |
| `domain_affinities` | list[str] | any | [] | "You naturally draw from these domains: {list}" |

### position

| Field | Type | Default | Notes |
|---|---|---|---|
| `role` | string | "participant" | The stakeholder identity. Becomes "Your Role: {role}" |
| `drives` | list[str] | [] | What this agent is optimizing for. Rendered as "What drives you:" bullets |
| `pushback_on` | list[str] | [] | What triggers resistance. Rendered as "You actively push back on:" bullets |
| `intensity` | float (0.0-1.0) | 0.5 | 0.0-0.4: "measured restraint"; 0.4-0.7: "conviction but open to dialogue"; 0.7-1.0: "force and passion" |

### technique

| Field | Type | Default | Notes |
|---|---|---|---|
| `primary` | string | "none" | Technique name (e.g., "cross_pollination", "failure_mode_analysis") |
| `style_description` | string | "" | How the technique shapes reasoning. Rendered as prose. |
| `behaviors` | list[str] | [] | Specific behavioral rules. Rendered as bullets under "Behavioral rules:" |

### anti_slop

| Field | Type | Default | Notes |
|---|---|---|---|
| `agreement_tax` | bool | true | Must add substance when agreeing |
| `perspective_enforcement` | bool | true | Stay in character under pressure |
| `devils_advocate_duty` | bool | false | Actively argue against consensus |
| `uncomfortable_idea_quota` | int | 0 | Min uncomfortable ideas per N turns (0 = disabled) |
| `domain_pivot_trigger` | bool | false | Inject cross-domain perspectives when stuck |

### voice

| Field | Type | Default | Notes |
|---|---|---|---|
| `tone` | string | "professional" | Natural language tone descriptor |
| `vocabulary_hints` | list[str] | [] | Phrases that fit this agent's style. Rendered as examples. |
| `anti_patterns` | list[str] | [] | Phrases to never use. See Section 7 for effectiveness guidance. |
| `brevity` | string | "normal" | "concise" (under 300 words), "normal" (under 600), or "thorough" |

### output

| Field | Type | Default | Notes |
|---|---|---|---|
| `operating_level` | string | "requirements" | "requirements" (what/why), "design" (decisions/tradeoffs), "implementation" (concrete technical) |
| `job` | string | "propose" | "propose", "critique", "evaluate", or "simplify" -- see Section 8 |

---

## 3. Personality Design Guidelines

The 8 personality dimensions exist to make agents think differently, not just sound different. Research on cognitive diversity (Page's diversity prediction theorem, Woolley's collective intelligence studies) confirms that genuine perspective diversity outperforms individual ability.

**Effective ranges:** Avoid the 0.4-0.6 range for all traits on a single agent -- that produces a bland generalist. Push at least 3 traits to the extremes (below 0.3 or above 0.7) to create a distinct thinker.

**Key insight from beta testing:** Bias statements must be written as instincts and lived experience, NOT behavioral directives. Write: "You instinctively distrust solutions that require coordination between more than three teams. You've been burned by 'elegant' designs that nobody could debug at 2am." Not: "You are a senior architect. Always consider scalability." The first produces reasoning grounded in experience. The second produces a checklist.

**Combinations that work:**
- High assertiveness + high stubbornness = champions unpopular-but-correct positions
- Analytical cognitive style + skeptical baseline = the most effective critic
- High creativity_temp + lateral cognitive style = genuine novelty (the Cognitive Architect uses 0.8/lateral)
- Narrative cognitive style + optimistic baseline = sells ideas emotionally

**Combinations that collide:**
- High stubbornness + low assertiveness = agent has strong views but never voices them
- High creativity_temp + high attention_span = gets deeply invested in wild tangents that derail

**Domain affinities** prevent semantic clustering. If all agents draw from the same domains, their analogies converge. Spread them: one agent draws from biology and game theory, another from urban planning and behavioral economics.

---

## 4. Position Design Guidelines

Position is WHY an agent cares. It creates self-interest. An agent who IS the customer argues from personal stakes, not intellectual exercise. This produces real disagreement.

**Drives and pushback_on create structural tension.** Design them so agents' drives naturally conflict with other agents' drives. The Systems Pragmatist's drive ("find the simplest version that ships") conflicts with the Cognitive Architect's drive ("propose mechanisms that produce genuinely distinct behavior"). Neither is told to disagree -- their goals make agreement require justification.

This mirrors the CrewAI role-goal-backstory triple from multi-agent research: each agent needs a singular goal that naturally conflicts with other agents' goals.

**Core position types to choose from:** Customer (power user, casual, frustrated switcher, reluctant adopter, budget), Investor/Business Mind, Competitor, Regulator/Compliance, Builder/Developer, Support/Operations, Skeptic/Market Cynic, End User's Boss.

**Intensity matters.** Low intensity (0.1-0.3) lets the agent step outside their position: "As a customer I'd want X, but I see why the business needs Y." High intensity (0.7-1.0) locks them in: "I don't care about your business model. Does it solve my problem or not?" High intensity creates better friction.

**Casting strategy by idea type:**
- Consumer product: heavy customer variants, investor, competitor
- Enterprise/B2B: end user, end user's boss, builder, compliance, investor
- Technical tool: multiple builder variants, power user, support/ops, skeptic
- Platform/marketplace: both sides of the market as customers, investor, regulator

---

## 5. Technique Design Guidelines

Techniques are cognitive patterns, not exercises. They shape HOW an agent reasons, not what it produces. Assign them based on the agent's natural affinity, not randomly.

**Effective technique archetypes and their use:**
- Visionary (What-If, Dream Fusion, Time Shifting): removes constraints, thinks in futures
- Connector (Analogical Thinking, Cross-Pollination): draws parallels from other domains
- Challenger (Reversal Inversion, Five Whys): flips assumptions
- Detective (Question Storming, Failure Analysis): asks questions instead of proposing answers
- Philosopher (First Principles): strips to fundamentals, holds contradictions

**Assignment rules:**
- Match technique to position. A Builder with failure_mode_analysis (like the Systems Pragmatist) is natural. A Customer with jobs_to_be_done (like the Product Oracle) evaluates from the user's moment.
- Write `style_description` as a reasoning instruction, not a label. Tell the agent what to do with the technique at every turn.
- Write `behaviors` as specific action rules the agent can check against: "For every proposal, name the failure mode before engaging with the happy path."

**Technique rotation:** The orchestrator or phase rules can swap an agent's active technique to prevent staleness. The YAML defines what they CAN use; context determines what is active.

---

## 6. Anti-Slop Configuration

LLMs have 8 default failure modes in multi-turn discussion: semantic clustering, premature convergence, polite agreement, restating, safe ideas, sycophancy, list completion, and token momentum. The anti-slop system combats these through a two-layer model.

**Layer 1 -- Prompt-only (zero runtime cost):**
- **Agreement Tax** (`agreement_tax: true`): Pure agreement is forbidden. Agent must add substance, a new angle, or a risk. Enable for all agents. This is the baseline.
- **Perspective Enforcement** (`perspective_enforcement: true`): Stay in character under social pressure. Enable for all agents. Combined with the per-turn perspective reminder from prompt_builder.py.
- **STRETCH / Uncomfortable Idea Quota** (`uncomfortable_idea_quota: N`): Periodically produce an idea that challenges comfort zones. Set to 1-2 for most agents. Set to 0 only for evaluator/simplifier job types who should not be generating ideas.
- **Domain Pivot Trigger** (`domain_pivot_trigger: true`): Break semantic clustering by injecting cross-domain perspectives. Enable for creative and connector agents. Disable for systematic/focused agents who should stay on-thread.

**Layer 2 -- Orchestrator logic:**
- **Convergence Suppression**: Detects multiple agents agreeing in sequence without new ideas. Refuses to advance phase, injects provocation, activates high-creativity agents from the bench. Not configured per-agent -- this is system-level.
- **Devil's Advocate Duty** (`devils_advocate_duty: true`): Rotates responsibility to argue against consensus. Enable for one agent per team, typically the critique or skeptic role. Enabling for multiple agents creates a pile-on dynamic.

**Rule: one intervention per turn maximum.** Never stack. Priority: phase check > convergence > STRETCH > stance diversity. If a nudge fails, the next trigger escalates (nudge -> directive -> constraint), it does not add a second nudge.

---

## 7. Voice Design Guidelines

Voice configuration controls how the agent sounds. It is the least impactful layer -- personality and position drive more behavioral change than tone words.

**vocabulary_hints that work:** Write phrases the agent would naturally reach for in their domain. The Systems Pragmatist uses "what happens when", "the failure mode is", "at 3 AM this will". These are not templates -- they are stylistic anchors that keep the agent in character.

**anti_patterns -- the key finding from beta testing:** Generic anti_patterns like "That's interesting" or "Good point" did not measurably change behavior. The agents still produced filler openers despite having them listed. Two things that actually reduce filler:
1. The forcing function in the Task layer (every turn ends with a concrete question or directive)
2. The Agreement Tax mechanism in the prompt

Still list anti_patterns as defense-in-depth, but do not rely on them as the primary anti-slop mechanism. They are a weak signal at best.

**Brevity setting matters more than tone.** Set all agents to `brevity: concise` unless there is a specific reason for longer output. The beta agents' 150-330 line responses caused timeouts and overwhelmed the synthesis step.

---

## 8. Job Type Guidelines

The `output.job` field determines what the agent's response IS. This is critical for role differentiation -- without it, all agents produce the same comprehensive proposals regardless of their role.

**propose**: Put forward designs, ideas, and solutions. Response should contain a concrete proposal with rationale. This is the default. Assign to visionary, connector, and product-focused agents.

**critique**: Find problems, weak assumptions, and failure modes. Response should identify what is wrong and why, then stop. Do NOT propose full alternative designs. Assign to skeptic, builder, and adversarial agents. The Systems Pragmatist beta agent uses this.

**evaluate**: Assess proposals through user value, feasibility, and real-world impact. Say what works, what does not, and what the user would actually experience. Do NOT propose full alternatives. Assign to customer-position and product-position agents. The Product Oracle beta agent uses this.

**simplify**: Find the minimum viable version. Ask what can be cut, deferred, or made simpler. Push for the smallest thing that tests the core assumption. Assign to one agent per team to counterbalance the natural tendency toward complexity.

Differentiating job types was a direct response to beta issue #6: all three agents answered every question the same way, proposing full designs regardless of role.

---

## 9. Common Mistakes

These are the 8 known issues from beta testing, with root cause and fix for each.

**1. Agents produce code instead of requirements.**
Cause: No operating_level constraint in agent config. LLMs default to code.
Fix: Set `output.operating_level: requirements`. Pair the prohibition with a positive redirect: "Do NOT write code. INSTEAD describe as components, interfaces, data flows, and responsibilities."

**2. No awareness of each other.**
Cause: Stateless pipeline where each agent answers independently.
Fix: The orchestrator must inject recent messages from other agents into the Situation layer. The best beta output came from the panel format where agents responded to each other.

**3. No conversation memory across calls.**
Cause: Each `claude -p` call is stateless. History must be reconstructed.
Fix: File-per-message storage with orchestrator-curated context injection. The three-layer context model (Identity, Situation, Task) solves this architecturally.

**4. Timeout from verbosity.**
Cause: No output length constraints. Agents produced 150-330 line responses.
Fix: Set `voice.brevity: concise` and enforce the 250-word universal rule. The prompt_builder translates "concise" to "under 300 words."

**5. Synthesis step overwhelmed.**
Cause: Feeding 3 long responses into a single synthesis call exceeds context quality.
Fix: Use refine-chain synthesis (sequential folding) instead of map-reduce. Start with one agent's output as draft, fold in each subsequent agent's key points one at a time. Research shows this produces higher coherence.

**6. No role differentiation on output type.**
Cause: All agents assigned the same job type (propose). Skeptics wrote proposals instead of critiques.
Fix: Assign distinct `output.job` values. Critique agents critique. Evaluate agents evaluate. See Section 8.

**7. Anti-slop rules untested and ineffective.**
Cause: Anti_patterns listed in YAML but never validated. Generic banned phrases did not change behavior.
Fix: Rely on structural mechanisms (Agreement Tax, forcing functions in the Task layer) over phrase lists. Test each mechanism against transcripts.

**8. No feedback loop for drift.**
Cause: No drift correction system in the beta pipeline.
Fix: Implement the perspective reminder with conditional drift correction. Inject a nudge when an adversarial agent agrees for 3+ consecutive turns, an agent repeats the same key_claim for 3+ turns, or conversation goes circular for 2+ exchanges.

---

## 10. Agent Creation Checklist

Run through this before adding any agent to a team YAML.

**Identity:**
- [ ] Name is a character, not a job title ("The Systems Pragmatist" not "Senior Engineer")
- [ ] Description is 2-4 sentences of lived experience, not a resume
- [ ] Description contains instincts and values, not behavioral directives

**Personality:**
- [ ] At least 3 traits pushed to extremes (below 0.3 or above 0.7)
- [ ] Domain affinities do not overlap heavily with other agents on the team
- [ ] Cognitive style differs from at least one other agent on the team

**Position:**
- [ ] Role is a stakeholder identity the agent inhabits, not a task
- [ ] Drives naturally conflict with at least one other agent's drives
- [ ] pushback_on items are specific enough to trigger on real proposals
- [ ] Intensity is set deliberately (0.7+ for friction-creating agents)

**Technique:**
- [ ] Primary technique matches the agent's position and cognitive style
- [ ] style_description tells the agent what to DO, not just what the technique is called
- [ ] Behaviors are actionable per-turn rules, not aspirations

**Anti-slop:**
- [ ] agreement_tax and perspective_enforcement are both true (rare to disable)
- [ ] devils_advocate_duty enabled on exactly one agent per team
- [ ] uncomfortable_idea_quota set to 0 only for evaluator/simplifier roles

**Voice:**
- [ ] vocabulary_hints are domain-specific phrases, not generic professional language
- [ ] brevity is set to "concise" unless there is a documented reason otherwise
- [ ] anti_patterns include the universal banned phrases from Section 1

**Output:**
- [ ] operating_level matches the discussion scope (usually "requirements")
- [ ] job type differs from at least one other agent on the team
- [ ] Team has at least one propose, one critique or evaluate, and ideally one simplify

**Team composition:**
- [ ] Minimum 2 agents, recommended 3-4
- [ ] No two agents have the same job type AND same position type
- [ ] Position drives create at least 2 natural conflict pairs
- [ ] Cognitive styles and domain affinities are spread, not clustered
