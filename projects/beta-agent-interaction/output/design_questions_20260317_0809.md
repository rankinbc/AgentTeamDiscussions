# AgentTeamDiscussions: Design Question Responses

Generated: 2026-03-17 08:09
Total time: 891s across 30 calls

---

# Question 1: What does the user actually hand the system, and how does it become a session?

## The Cognitive Architect (creativity engine designer)

[Claude CLI timed out after 180s]

*(180s)*

---

## The Product Oracle (user advocate and product strategist)

Good. Now I have the full picture -- the agent configs, the prompt builder, the PROJECT_CONTEXT, and the current conversation mechanics. Let me answer this as The Product Oracle.

---

## The 10 PM Problem: Input to Session

The job to be done is dead simple: **the user has momentum on an idea and wants to capture it before sleep kills it.** Anything that feels like filling out a form at 10 PM is a conversion killer. But anything too vague produces a session that spins its wheels for 8 hours on nothing.

The answer is a **progressive input format** -- one that has a floor of one sentence and a ceiling of structured detail, with the orchestrator doing the heavy lifting to bridge the gap.

---

### The Input Format: Idea Brief

A single YAML file in `/ideas/`, but one that's mostly optional.

```yaml
# ideas/time-tracker.yaml
# Only 'idea' is required. Everything else sharpens the session.

idea: "A time tracker for freelancers that actually gets used"

# Optional: who is this for?
audience: "Solo freelancers billing hourly who hate timesheets"

# Optional: what's broken today?
problem: >
  Existing time trackers require manual start/stop discipline.
  Freelancers forget, reconstruct hours from memory, underbill.

# Optional: any strong opinions or constraints?
constraints:
  - "Must work without the user remembering to press a button"
  - "No enterprise features -- this is for individuals"
  - "Monetization matters -- not a hobby project"

# Optional: what phase to start in (default: brainstorm)
start_phase: brainstorm

# Optional: how long to run (default: 8h)
max_duration_hours: 8

# Optional: which team config to use (default: config/teams/default.yaml)
team: beta-agents
```

But here's the critical design decision: **the user can also just type a string.** The CLI accepts:

```
python -m orchestrator "a time tracker for freelancers"
```

That one-liner creates a minimal idea brief internally with only the `idea` field populated. No file needed. The file format exists for users who *want* to be detailed, or who are iterating on an idea across multiple sessions.

**Three input paths, same destination:**

| Path | Effort | When |
|---|---|---|
| CLI one-liner | 5 seconds | "Just run with this" |
| Minimal YAML (idea + audience) | 1 minute | "I have some context" |
| Full brief (all fields) | 5 minutes | "I've been thinking about this" |

---

### The Seeding Process: How Vague Becomes Useful

This is the real design challenge. "A time tracker for freelancers" is not enough for The Systems Pragmatist to do failure mode analysis or The Cognitive Architect to design personality experiments. Here's how the orchestrator bridges the gap:

#### Step 1: Expansion Turn (Turn Zero)

Before the session starts, the orchestrator runs a **single pre-session expansion call** -- one stateless `claude -p` invocation with a specialized prompt:

```
Given this product idea, generate a structured seed brief for a multi-agent
brainstorming session. Do NOT solve the problem. Instead, expand the idea
into dimensions that give different stakeholder perspectives something to
grab onto.

IDEA: "a time tracker for freelancers"
AUDIENCE: (not provided)
CONSTRAINTS: (not provided)

Generate:
1. PROBLEM SPACE: 3-5 plausible pain points this idea might address
2. USER ARCHETYPES: 2-3 distinct types of people who might need this
3. TENSION POINTS: 2-3 inherent tensions or tradeoffs in this space
   (e.g., "automatic tracking vs. privacy concerns")
4. COMPETITIVE LANDSCAPE: What exists today and why it might fall short
5. OPEN QUESTIONS: 5 questions the teams should wrestle with

Output as YAML.
```

This is a **cheap, fast call** (30 seconds, minimal tokens). It doesn't make decisions -- it creates surface area for the agents to disagree about. The output might look like:

```yaml
problem_space:
  - Freelancers forget to start/stop timers and reconstruct hours from memory
  - Switching between clients/projects adds friction to tracking
  - Time tracking feels like administrative overhead, not productive work
  - Inaccurate tracking leads to underbilling or awkward client disputes

user_archetypes:
  - "The Chaotic Creative: Designer/developer who works in bursts, hates structure"
  - "The Multi-Client Juggler: Consultant with 5+ clients, needs clean separation"
  - "The New Freelancer: Just left full-time, doesn't have billing habits yet"

tension_points:
  - "Automatic tracking vs. user control (what if it captures the wrong thing?)"
  - "Simplicity vs. reporting depth (clients want detailed breakdowns)"
  - "Privacy vs. accuracy (screen monitoring is accurate but invasive)"

competitive_landscape:
  - "Toggl, Harvest, Clockify -- manual start/stop, widely used but low retention"
  - "RescueTime, Timing.app -- automatic but feel surveillance-like"
  - "Spreadsheets -- still the most common 'tool' for solo freelancers"

open_questions:
  - "Is the core innovation in capture (how time is tracked) or output (how it's billed)?"
  - "Does this need to integrate with invoicing, or is tracking enough?"
  - "Is this a desktop app, mobile app, browser extension, or all three?"
  - "What's the monetization model -- freemium, subscription, one-time?"
  - "How do you handle non-billable time without making the user feel guilty?"
```

#### Step 2: Seed Message Assembly

The orchestrator now has enough material to construct **differentiated first-turn messages** for each team. This is where agent configs matter.

For each agent, the orchestrator constructs a seed message that:
1. Presents the original idea (verbatim, unmodified)
2. Includes the expanded brief as context
3. Frames the opening through the agent's position and technique

The seed message template:

```
## New Session: Brainstorm Phase

### The Idea
"{original_idea}"

{if audience}User provided audience: {audience}{/if}
{if problem}User provided problem context: {problem}{/if}
{if constraints}User provided constraints:
{for c in constraints}- {c}
{/for}{/if}

### Expanded Context (auto-generated, may be wrong -- challenge it)
{expansion_yaml}

### Your Opening
You're {agent.name}, the {agent.position.role}. Using your
{agent.technique.primary} approach, react to this idea.

{phase_instructions}

This is the opening of a brainstorm. Be concrete. Take a position.
What's the first thing that jumps out from your perspective?
```

The `phase_instructions` for brainstorm phase:

```
BRAINSTORM PHASE RULES:
- Generate ideas, don't evaluate them yet
- Build on what others say OR deliberately contradict it
- Every contribution must be concrete enough to sketch on a napkin
- "What if..." is your friend; "That won't work because..." comes later
- Aim for volume and variety, not perfection
```

#### Step 3: Team Seeding (Parallel)

The orchestrator seeds both teams simultaneously but with **different framings of the same material**:

**Team A (BMAD agents / internal team):** Gets the full expanded brief and is told "You are the builder's team -- your job is to figure out what's worth building and how to think about it."

**Team B (Client/stakeholder team):** Gets the same brief but is told "You represent the market -- your job is to stress-test whether real people would pay for this, use it, and stick with it."

Each agent on each team gets the same seed content but their system prompt (personality, position, technique, anti-slop rules) ensures they react differently. The Cognitive Architect sees it as a design problem. The Systems Pragmatist immediately thinks about overnight operation failure modes... wait, wrong context -- they think about *the product's* failure modes. The Product Oracle (me) thinks about retention curves.

The expansion step is what makes this work. Without it, three agents looking at "a time tracker for freelancers" all produce variations of "interesting, let's think about features." With tension points and open questions seeded, they have **specific things to disagree about** from turn one.

---

### The Minimum Viable Input

**One sentence.** Literally.

```
python -m orchestrator "a time tracker for freelancers"
```

That's it. The expansion turn handles the rest. The session will be less focused than one with a full brief, but it will be *useful* because:

1. The expansion turn generates tension points -- agents have something to argue about
2. The agent positions are pre-loaded with drives and pushback triggers -- they don't need the user to tell them what to care about
3. The brainstorm phase is intentionally divergent -- vague input is actually *fine* for divergent thinking; it's the later phases (specify, review) that need precision, and by then the session has generated its own context

**The quality gradient:**

| Input Level | Session Quality | What You Miss |
|---|---|---|
| One sentence | Usable. Wider exploration, some wasted turns. | Agents may explore directions you've already dismissed |
| + audience | Notably better. Agents ground arguments in specific users. | Still some wheel-spinning on "who is this for" |
| + problem | Good. Agents skip "does this problem exist" and go to solutions. | May miss constraints you care about |
| + constraints | Excellent. Focused session from turn one. | Nothing material -- this is the sweet spot |
| Full brief | Maximum signal. But diminishing returns past constraints. | You spent 5 min instead of 1 |

The sweet spot for most sessions is **idea + 2-3 constraints.** That's 30 seconds of typing and it eliminates the most common wasted cycles (agents exploring directions you've already ruled out).

---

### What This Means for Implementation

The orchestrator needs three new components:

1. **IdeaBrief model** (Pydantic) -- parsed from YAML file or constructed from CLI string
2. **Expansion prompt** -- a single-purpose prompt template that turns sparse input into structured dimensions, stored in `config/prompts/expand.yaml` so it's tunable
3. **Seed message builder** -- takes IdeaBrief + expansion output + agent config + phase config and produces the first-turn message per agent

The expansion call is the only "magic" step, and it's cheap -- one short stateless call before the session clock starts. Everything else is templating.

One more thing: the expansion output should be **saved to the session folder** (`sessions/{id}/seed/expansion.yaml`). When the user wakes up and reads the Morning Brief, they should be able to see exactly what the system inferred from their one-liner -- and whether it went sideways. That's the trust mechanism. If the expansion hallucinated a wrong audience, the user sees it immediately and knows to re-run with a corrected brief. Transparency over black-box magic.

*(172s)*

---

## The Systems Pragmatist (infrastructure realist)

Good. Now I know exactly what exists and what doesn't. Let me think through this properly.

---

## The Input Pipeline: From "I have an idea" to Overnight Session

### The Core Problem

You have agents with rich stakeholder positions -- drives, pushback triggers, domain affinities, technique specializations. A one-liner like "a time tracker for freelancers" gives them nothing to push back *on*, no surface area for disagreement, no constraints to test against. The agents will either hallucinate constraints to argue about (ungrounded) or produce generic consensus (useless).

The input format needs to solve for three things:
1. **Low friction at 10 PM** -- you're not filling out a 40-field form
2. **Enough surface area** -- agents need something to *disagree about*
3. **Graceful degradation** -- missing fields should produce narrower sessions, not broken ones

### The Input Format

Three tiers. YAML, because that's already the config language and it validates through Pydantic.

**Tier 1: Minimum Viable Input** (the one-liner wrapper)

```yaml
idea: "A time tracker for freelancers that learns your patterns and auto-categorizes work"
```

That's it. One field. Save it as `ideas/time-tracker.yaml`, point the orchestrator at it.

**Tier 2: Guided Input** (5 minutes of thought)

```yaml
idea: "A time tracker for freelancers that learns your patterns and auto-categorizes work"

who: "Solo freelancers juggling 3-8 clients, mostly developers and designers"
problem: "They lose 20-30% of billable time because tracking is manual and they forget"
constraints:
  - "Must work offline -- freelancers work from cafes with bad wifi"
  - "No subscription over $10/month -- these people are cost-sensitive"
  - "Has to integrate with at least Toggl and Harvest for migration"

open_questions:
  - "Desktop app vs browser extension vs both?"
  - "How aggressive should auto-categorization be before user trusts it?"
```

**Tier 3: Full Brief** (when you've already been thinking about it)

```yaml
idea: "A time tracker for freelancers that learns your patterns and auto-categorizes work"

who: "Solo freelancers juggling 3-8 clients, mostly developers and designers"
problem: "They lose 20-30% of billable time because tracking is manual and they forget"

constraints:
  - "Must work offline"
  - "No subscription over $10/month"
  - "Has to integrate with Toggl and Harvest"

hypotheses:
  - "Freelancers will accept 80% accuracy on auto-categorization if corrections are fast"
  - "The biggest churn risk is the first week before the model has enough data"

risks:
  - "Privacy concerns -- tracking app that watches what you do"
  - "ML model needs significant training data per user"

non_goals:
  - "Not an invoicing tool"
  - "Not a project management tool"
  - "Not targeting agencies or teams"

open_questions:
  - "Desktop app vs browser extension vs both?"
  - "How aggressive should auto-categorization be?"

session:
  focus: "product-market fit"      # or: technical-feasibility, ux-design, go-to-market
  depth: "deep"                    # shallow (2hr), standard (4hr), deep (8hr)
  bias: "challenge"                # challenge (stress-test), explore (breadth), converge (decisions)
```

### The Schema

```python
class IdeaSeed(BaseModel):
    # Tier 1 -- required
    idea: str                                    # The core concept

    # Tier 2 -- optional, adds surface area
    who: Optional[str] = None                    # Target user
    problem: Optional[str] = None                # Problem being solved
    constraints: list[str] = []                  # Hard boundaries
    open_questions: list[str] = []               # What you want explored

    # Tier 3 -- optional, adds direction
    hypotheses: list[str] = []                   # Beliefs to stress-test
    risks: list[str] = []                        # Known concerns
    non_goals: list[str] = []                    # Explicit scope boundaries
    session: Optional[SessionConfig] = None      # Session tuning

class SessionConfig(BaseModel):
    focus: str = "product-market fit"
    depth: str = "standard"
    bias: str = "explore"
```

### The Seeding Process

This is where the real design work is. The orchestrator has to transform the input into *two different seed messages* -- one per team -- that are grounded enough to produce useful first turns.

**Step 1: Input Expansion** (pre-session, not agent-driven)

For Tier 1 inputs, the orchestrator runs a single, fast Claude call with a deterministic prompt:

```
Given this product idea: "{idea}"

Extract and return ONLY:
- target_user: Who is this most likely for? (one sentence)
- core_problem: What problem does this solve? (one sentence)  
- implicit_constraints: What 2-3 constraints are implied? (list)
- tension_points: What 2-3 things would reasonable people disagree about? (list)

Be specific. No hedging. If you're guessing, say so.
```

This is a 10-second call. It's not creative work -- it's extracting the obvious implications so agents don't waste their first 3 turns discovering that a freelancer time tracker probably needs to be cheap. The output supplements but never overwrites user-provided fields.

**Failure mode addressed:** Without this, Tier 1 inputs produce 2-3 turns of agents independently "discovering" the same obvious context, burning deliberation budget on alignment rather than exploration.

**Step 2: Team-Specific Seed Construction**

Each team gets a different seed message. The seed is NOT just the idea brief -- it's the brief plus a *team-specific framing* that activates their particular stakeholder positions.

For the **BMAD team** (the product/design side), the seed message template:

```
## Session Brief

**Idea:** {idea}
**Target User:** {who}
**Problem:** {problem}

{if constraints}
**Hard Constraints:**
{constraints as bullets}
{endif}

{if hypotheses}
**Hypotheses to Test:**
{hypotheses as bullets}
{endif}

{if open_questions}
**Open Questions from Stakeholder:**
{open_questions as bullets}
{endif}

{if non_goals}
**Explicitly Out of Scope:**
{non_goals as bullets}
{endif}

## Your Task

You are the product advisory team. Your job in this first phase is to 
stress-test the idea's viability. Each of you should evaluate this from 
your specific role and identify:

1. The strongest argument FOR this idea
2. The most likely reason it fails
3. One question the brief doesn't answer that you need answered

Do not agree with each other. Find the real tensions.
```

For the **client team** (technical/implementation side), a different framing:

```
## Session Brief

[same brief section]

## Your Task

You are the technical feasibility team. Evaluate this idea from an 
implementation perspective. Each of you should identify:

1. The hardest technical problem this idea requires solving
2. One architectural decision that has to be made before anything else
3. What the user is underestimating about building this

Do not hand-wave complexity. Be specific about what's hard and why.
```

**Why different framings?** Same brief, different activation energy. The product team needs to argue about *whether* and *what*. The technical team needs to argue about *how* and *what's hard*. If both teams get the same generic "discuss this idea" prompt, they converge on the same surface-level observations and the cross-team exchange adds nothing.

**Step 3: Agent-Level Differentiation**

Within each team, individual agents already have system prompts built by `prompt_builder.py` that encode their position, drives, and pushback triggers. The seed message is the *same* for all agents on a team -- differentiation comes from the system prompt, not the input.

This is important: **don't try to customize the seed per agent.** The system prompt already tells The Systems Pragmatist to run failure mode analysis and The Product Oracle to track user needs. Customizing the seed per agent means maintaining N x M templates (N agents x M input fields) and creates a fragile coupling between idea format and team composition.

**Step 4: Phase Gate on Input Quality**

The session config's `focus` and `bias` fields control phase behavior, but there's a subtler mechanism needed: **the orchestrator should shorten the brainstorm phase proportionally to input completeness.**

- Tier 1 input (just `idea`): Full brainstorm phase. Agents need time to explore the space.
- Tier 2 input (`who`, `problem`, `constraints` provided): Shortened brainstorm, longer refine phase. The basics are established.
- Tier 3 input (hypotheses, risks, non-goals): Minimal brainstorm, emphasis on specify and review. You've already thought about this; you want stress-testing, not exploration.

This is a simple heuristic:

```python
def compute_phase_weights(seed: IdeaSeed) -> dict[str, float]:
    completeness = 0
    if seed.who: completeness += 1
    if seed.problem: completeness += 1
    completeness += min(len(seed.constraints), 3) * 0.5
    completeness += min(len(seed.hypotheses), 3) * 0.5
    completeness += min(len(seed.risks), 2) * 0.5
    completeness += min(len(seed.non_goals), 2) * 0.5
    # 0-6 scale, normalize to 0-1
    completeness = min(completeness / 6.0, 1.0)
    
    return {
        "brainstorm": max(0.15, 0.40 - (completeness * 0.25)),
        "refine":     0.30,
        "specify":    min(0.35, 0.20 + (completeness * 0.15)),
        "review":     0.15,
    }
```

### Failure Modes I'm Watching

**1. The Inflation Problem.** The expansion step (Step 1) hallucinates constraints or users that the human didn't intend. Mitigation: expansion output is tagged `[inferred]` in the seed, and agents are told "inferred context may be wrong -- challenge it."

**2. The Echo Chamber.** Both teams independently reach the same conclusions because the seed is too directive. Mitigation: different team framings ask different questions. The cross-team exchange in later phases surfaces divergence.

**3. The Vague Spiral.** Tier 1 input produces agents talking in circles because there's not enough to anchor on. Mitigation: the expansion step, plus the orchestrator should monitor for "low information density" in early turns (repeated concepts, no new claims) and inject a sharpening prompt: "You're circling. Each agent: make one concrete claim and defend it."

**4. The Overnight Crash.** Session dies at 2 AM, 4 hours of work lost. This isn't an input format problem but it affects the design: sessions should checkpoint after every cross-team exchange, and the morning brief should be generated from checkpoints, not just the final state. If the session crashes at turn 47, you get a brief covering turns 1-46, not nothing.

### What the User Actually Does at 10 PM

```bash
# Minimum -- 30 seconds
echo 'idea: "A time tracker for freelancers that auto-categorizes work"' > ideas/tonight.yaml
python -m orchestrator run ideas/tonight.yaml

# With some thought -- 5 minutes
# Edit ideas/tonight.yaml with who/problem/constraints
python -m orchestrator run ideas/tonight.yaml

# With team override
python -m orchestrator run ideas/tonight.yaml --team config/teams/beta-agents.yaml
```

The orchestrator validates the YAML against `IdeaSeed`, runs expansion if needed, builds seeds, initializes the session directory under `sessions/`, and starts the conversation loop. The user goes to bed.

### What I'd Build First

1. `IdeaSeed` Pydantic model -- add to `models.py`
2. `expand_idea()` function -- single Claude call, deterministic prompt, returns filled `IdeaSeed`
3. `build_team_seed()` function -- takes `IdeaSeed` + team role string, returns seed message
4. `compute_phase_weights()` -- input completeness to phase allocation
5. CLI entry point -- `orchestrator run <idea.yaml> [--team <team.yaml>]`

The expansion step is the only part that uses an LLM call before the session starts. Everything else is template assembly and arithmetic. That's deliberate -- the pre-session pipeline should be fast, deterministic where possible, and fail loudly if the YAML is malformed. Save the creative work for the agents.

*(165s)*

---

# Question 2: What happens inside a single agent turn, from trigger to output?

## The Cognitive Architect (creativity engine designer)

[Claude CLI timed out after 180s]

*(180s)*

---

## The Product Oracle (user advocate and product strategist)

[Claude CLI timed out after 180s]

*(180s)*

---

## The Systems Pragmatist (infrastructure realist)

[Claude CLI timed out after 180s]

*(180s)*

---

# Question 3: Who speaks next and why?

## The Cognitive Architect (creativity engine designer)

# Turn Selection Algorithm & Bench Activation Design

*Thinking laterally here -- the worst thing you can do is round-robin. That's a meeting where everyone talks because it's "their turn," not because they have something worth saying. The best conversations are jazz: structured enough to cohere, loose enough to surprise.*

---

## Core Mechanism: Weighted Relevance Auction with Decay

Every turn cycle, the orchestrator runs a **micro-auction**. Agents don't literally bid -- the orchestrator scores them based on several weighted signals and selects the highest composite score.

### Composite Score Formula

```
score(agent) = (relevance * 0.4)
             + (recency_penalty * 0.25)
             + (diversity_bonus * 0.2)
             + (role_urgency * 0.15)
             + jitter
```

| Signal | How It's Computed | Why It Matters |
|---|---|---|
| **relevance** | Orchestrator prompts each *active* agent with a 1-shot "rate your relevance to the last message 0-1" call. Cheap, fast, no generation. | The agent who has the most to say should speak next. |
| **recency_penalty** | `1 - (1 / (turns_since_last_spoke + 1))`. Caps at 1.0 after ~5 turns of silence. An agent who just spoke gets 0.0. | Prevents monopolization mechanically. Even the most relevant agent gets suppressed if they just talked. |
| **diversity_bonus** | Each agent has a `perspective_type` tag (e.g., technical, business, creative, critical). Bonus = `0.0` if that perspective spoke in the last 2 turns, `0.5` if 3+ turns ago, `1.0` if 5+ turns. | Forces the conversation to rotate through *types of thinking*, not just individuals. |
| **role_urgency** | Phase-dependent weight. During `brainstorm`, creative roles get +0.3. During `review`, QA/critical roles get +0.3. Defined in `phases.yaml`. | The conversation phase knows what kind of thinking it needs. |
| **jitter** | Random uniform `[0, 0.08]`. | Breaks ties unpredictably. Keeps the system from becoming robotic. Small enough to never override real signal. |

### Selection Rule

```python
def select_next_speaker(active_agents, conversation_state):
    scores = {}
    for agent in active_agents:
        if agent.consecutive_turns >= MAX_CONSECUTIVE:  # hard cap = 2
            scores[agent] = -1  # forced cooldown
            continue
        scores[agent] = compute_composite(agent, conversation_state)

    # Mandatory rotation: if any agent hasn't spoken in max_silence turns, force them
    starved = [a for a in active_agents if a.turns_since_spoke >= MAX_SILENCE]
    if starved:
        return max(starved, key=lambda a: scores[a])

    return max(scores, key=scores.get)
```

**Key constants:**
- `MAX_CONSECUTIVE = 2` -- No agent speaks more than twice in a row, ever. Even if they're the most relevant being alive.
- `MAX_SILENCE = 8` -- If you've been active for 8 turns and haven't spoken, you're forced in. This is the "meeting facilitator noticing someone hasn't talked" mechanic.

### Why Not Agent Volunteering?

Agents volunteering creates a *confidence bias* problem. The loudest, most assertive persona always volunteers first. The quiet analyst who actually has the insight stays silent. The orchestrator-as-selector is the facilitator pattern -- it sees the whole board and can pull in the voice the conversation *needs*, not the one that *wants* to talk.

---

## Bench System

The bench is the key insight that makes this scale. 6 agents all processing every message is wasteful. 3-4 active agents with 2-3 on the bench is the sweet spot.

### State Model

```
ACTIVE  -- Processing every message, eligible for turn selection
BENCH   -- Not processing messages, but metadata-aware (topic tags, phase)
WARM    -- Transitional: processing last 3 messages to build context before going ACTIVE
```

### Starting Lineup

Defined per-phase in `phases.yaml`:

```yaml
phases:
  brainstorm:
    default_active: [pm, architect, creative]
    default_bench: [qa, dev, tech-writer]
    max_active: 4
    min_active: 2
  review:
    default_active: [qa, architect, dev]
    default_bench: [pm, creative, tech-writer]
    max_active: 4
    min_active: 2
```

### Activation Triggers (Bench to Active)

| Trigger | Detection Method | Confidence |
|---|---|---|
| **Topic match** | Orchestrator maintains a rolling topic vector (last 5 messages). Compare cosine similarity against each benched agent's `expertise_tags`. Threshold: 0.7. | High -- this is the primary trigger |
| **Explicit invocation** | Active agent's response contains a structured callout: `[NEED: qa-perspective]` or similar pattern. Orchestrator parses this. | High -- agents know when they're out of their depth |
| **Phase transition** | New phase starts, `default_active` list changes. | Deterministic |
| **Stagnation detection** | Orchestrator detects semantic similarity > 0.85 between last 3 responses (conversation is circling). Pull in a bench agent with the *lowest* topic overlap to inject fresh thinking. | Medium -- the "bring in the outsider" pattern |

### Deactivation Triggers (Active to Bench)

| Trigger | Detection Method |
|---|---|
| **Sustained low relevance** | Agent's self-reported relevance < 0.2 for 3 consecutive turns. Orchestrator asks: "Your relevance has been low. Go to bench?" Agent confirms. |
| **Active roster full** | A bench agent activates, but `max_active` is hit. The active agent with the lowest average relevance over the last 5 turns gets benched. |
| **Self-recusal** | Agent's response includes `[BENCH: low-value-add]`. Honored immediately. |
| **Phase transition** | New phase, new default lineup. |

### The WARM Transition

An agent doesn't jump from bench to active cold. That creates incoherent responses.

```
BENCH → WARM (receives last 3 messages + conversation summary) → ACTIVE
```

The warm-up costs one turn cycle. During warm-up, the agent is not eligible for selection but is building context. This means bench activation has a 1-turn latency -- which is fine and prevents thrashing.

### Anti-Thrash Rule

An agent cannot be benched within 3 turns of being activated. An agent cannot be activated within 3 turns of being benched. This prevents oscillation when topic relevance fluctuates near the threshold.

---

## Devil's Advocate Rotation

### 5 Individual Agent Turns, Not Rounds

**Rationale:** Rounds are variable-length (depends on active count). Individual turns are predictable and create asymmetric rotation -- the DA duty shifts across different conversation contexts, which is more interesting than always challenging at the same structural point.

### Implementation

```python
da_counter = 0  # increments every agent turn
da_assignment = None

def after_each_turn(speaker):
    global da_counter, da_assignment
    da_counter += 1
    if da_counter % 5 == 0:
        # Rotate DA to next eligible agent (not the current DA, not benched)
        eligible = [a for a in active_agents if a != da_assignment]
        da_assignment = eligible[da_counter // 5 % len(eligible)]
```

### What the DA Actually Does

The DA doesn't just disagree. The orchestrator **prepends a system instruction** to the DA agent's context:

```
You are currently serving as Devil's Advocate. Your job this turn:
- Identify the weakest assumption in the current direction
- Ask the question nobody is asking
- If consensus is forming too easily, stress-test it
- You may agree if the reasoning is genuinely sound -- forced disagreement is worse than honest challenge
```

The DA flag is visible in the conversation metadata so other agents know to engage with challenges rather than dismiss them.

### DA and Bench Interaction

- A benched agent cannot hold DA duty. If the current DA gets benched, duty immediately passes to the next eligible active agent.
- DA duty does **not** boost relevance score. The DA speaks when selected normally -- they just *think differently* when they do.

---

## Anti-Dominance Summary

Five independent mechanisms prevent any single agent from taking over:

1. **Recency penalty** (0.25 weight) -- mathematically suppresses repeat speakers
2. **MAX_CONSECUTIVE = 2** -- hard ceiling, no exceptions
3. **Diversity bonus** (0.20 weight) -- favors underrepresented perspective *types*
4. **MAX_SILENCE = 8** -- forces quiet agents into the conversation
5. **DA rotation** -- ensures critical thinking isn't owned by one persona

These are layered intentionally. Any single mechanism can be gamed or produce edge cases. Together, they create a conversation that *breathes* -- relevant voices rise, dominant voices cool, quiet voices get pulled in, and challenge is structural rather than personality-dependent.

---

*The mental model: the orchestrator isn't a scheduler. It's a jazz bandleader pointing at the next soloist. It reads the room, knows who's been quiet, knows what instrument the song needs next, and occasionally points at someone unexpected just to see what happens.*

*(78s)*

---

## The Product Oracle (user advocate and product strategist)

[Claude CLI timed out after 180s]

*(180s)*

---

## The Systems Pragmatist (infrastructure realist)

[Claude CLI timed out after 180s]

*(180s)*

---

# Question 4: How do messages actually flow between the two teams through the MCP server?

## The Cognitive Architect (creativity engine designer)

[Claude CLI timed out after 180s]

*(180s)*

---

## The Product Oracle (user advocate and product strategist)

[Claude CLI timed out after 180s]

*(180s)*

---

## The Systems Pragmatist (infrastructure realist)

[Claude CLI timed out after 180s]

*(180s)*

---

# Question 5: How does context get managed across a multi-hour overnight session?

## The Cognitive Architect (creativity engine designer)

[Claude CLI timed out after 180s]

*(180s)*

---

## The Product Oracle (user advocate and product strategist)

[Claude CLI timed out after 180s]

*(180s)*

---

## The Systems Pragmatist (infrastructure realist)

[Claude CLI timed out after 180s]

*(180s)*

---

# Question 6: How are anti-slop mechanisms actually enforced at runtime?

## The Cognitive Architect (creativity engine designer)

This is the right question at the right time. Most "anti-slop" designs die here -- they list the mechanisms but never spec the enforcement loop. Let me cut through it.

---

## Enforcement Architecture: The Three Tiers

### Tier 1: Prompt-Only (No Runtime Cost)

These live entirely in agent system prompts. The orchestrator doesn't monitor them -- they're self-enforcing through persona pressure.

| Mechanism | Where It Lives | Why It Works Without Runtime |
|---|---|---|
| **Perspective enforcement** | Each agent's persona prompt | Identity pressure is self-sustaining. "You are the skeptical architect" doesn't need a referee. |
| **Agreement tax** | System prompt rule | "Before endorsing any position, name two risks or unstated assumptions." Agent follows or doesn't -- either way it slows convergence. |
| **Specificity mandate** | System prompt rule | "No abstract endorsements. Every claim needs a concrete mechanism, example, or constraint." Slop is vague; this makes vagueness feel wrong. |
| **Dissent framing** | System prompt rule | "Disagreement is signal. Agreement without new information is noise." Reframes the social reward. |

These four are fire-and-forget. You tune the wording, but the orchestrator never inspects output for compliance. If an agent drifts, the other tier catches it.

---

### Tier 2: Orchestrator-Inline Detection (Lightweight, Every Turn)

These run **inside the orchestrator's turn loop**, between receiving a response and forwarding it. Cheap enough to run every turn. No background agents, no extra API calls.

#### Mechanism 5: Convergence Suppression

**Who runs it:** The orchestrator, in the message routing pipeline.

**Detection -- no embeddings needed:**

```python
class ConvergenceDetector:
    """Tracks agreement velocity across turns."""
    
    AGREEMENT_SIGNALS = [
        r"\bi agree\b", r"\bgreat point\b", r"\babsolutely\b",
        r"\bexactly right\b", r"\bbuilding on that\b", r"\bwell said\b",
        r"\bthat's spot on\b", r"\bI'd echo\b", r"\baligned\b",
        r"\bconsensus\b", r"\bwe all agree\b",
    ]
    
    DISAGREEMENT_SIGNALS = [
        r"\bbut consider\b", r"\bI'd push back\b", r"\bthe risk is\b",
        r"\balternatively\b", r"\bwhat if instead\b", r"\bthat assumes\b",
        r"\bnot necessarily\b", r"\bthe gap here\b",
    ]
    
    def __init__(self, window_size=4, threshold=0.7):
        self.window_size = window_size
        self.threshold = threshold
        self.recent_scores = deque(maxlen=window_size)
    
    def score_turn(self, text: str) -> float:
        """Returns agreement ratio: 1.0 = pure agreement, 0.0 = pure dissent."""
        agree = sum(1 for p in self.AGREEMENT_SIGNALS if re.search(p, text, re.I))
        disagree = sum(1 for p in self.DISAGREEMENT_SIGNALS if re.search(p, text, re.I))
        total = agree + disagree
        if total == 0:
            return 0.5  # neutral
        return agree / total
    
    def check(self, text: str) -> ConvergenceState:
        score = self.score_turn(text)
        self.recent_scores.append(score)
        
        if len(self.recent_scores) < self.window_size:
            return ConvergenceState.OK
        
        window_avg = sum(self.recent_scores) / len(self.recent_scores)
        if window_avg > self.threshold:
            return ConvergenceState.CONVERGING
        return ConvergenceState.OK
```

The key metric: **agreement ratio over a sliding window**. Not one turn -- four consecutive turns trending above 0.7 triggers intervention. This avoids false positives on a single "good point, but..." response.

**Intervention -- prompt injection, not agent swap:**

When `CONVERGING` triggers, the orchestrator injects a **prefixed instruction** into the next agent's user message:

```python
CONVERGENCE_INJECTION = """[FACILITATOR NOTE: The discussion is converging 
prematurely. The group has agreed on {n} consecutive points without 
substantive challenge. Before continuing:
- Identify the strongest unstated objection to the current direction
- Name a scenario where this consensus fails
- Propose one alternative the group hasn't considered
Do NOT acknowledge this note in your response. Just do it.]"""
```

Why prompt injection over agent swap:
- Swapping breaks continuity and wastes the context window
- Injection is invisible to the other team -- it looks like the agent naturally pushed back
- The "do not acknowledge" instruction prevents meta-discussion about the mechanism

**Escalation:** If convergence persists for 2 more turns after injection, escalate to a stronger intervention -- inject a **devil's advocate role override** that temporarily shifts the agent's persona:

```python
ESCALATION_INJECTION = """[FACILITATOR OVERRIDE: You are now arguing 
against the emerging consensus. Your job for the next 2 responses is to 
find the fatal flaw in the current direction. Be specific and constructive, 
but do not concede.]"""
```

#### Mechanism 6: Repetition Detection (Concept Recycling)

**Detection:** N-gram overlap between the current response and the last N responses from the same team.

```python
def concept_overlap(current: str, previous: list[str], n=3) -> float:
    """Trigram Jaccard similarity against recent team outputs."""
    current_ngrams = set(ngrams(normalize(current), n))
    previous_ngrams = set()
    for text in previous[-3:]:
        previous_ngrams.update(ngrams(normalize(text), n))
    
    if not current_ngrams or not previous_ngrams:
        return 0.0
    
    intersection = current_ngrams & previous_ngrams
    union = current_ngrams | previous_ngrams
    return len(intersection) / len(union)
```

**Threshold:** Overlap > 0.4 triggers a "bring something new" injection. This is a blunt instrument but it catches the failure mode where agents rephrase the same three ideas for six turns.

**Intervention:** Similar prompt injection -- "The last three responses have covered similar ground. Introduce a new constraint, stakeholder perspective, or failure mode that hasn't been discussed."

---

### Tier 3: Periodic Audit (Background Agent, Every N Turns)

These are too expensive to run every turn. They require an LLM call to evaluate, so they run on a schedule.

#### Mechanism 7: Novelty Scoring

**Who runs it:** A **background Haiku call** spawned by the orchestrator every 4 cross-team exchanges (not every turn -- every 4 complete back-and-forths).

**Why Haiku, not embeddings:**

Embeddings measure semantic similarity but miss structural novelty. A response can be semantically distant (different words) but structurally identical (same argument pattern, same level of abstraction). Haiku is cheap enough to run as a judge and can evaluate what matters: "did this add something?"

```python
NOVELTY_JUDGE_PROMPT = """Review the last 4 exchanges in this discussion.
For each response, score 1-5:
- 5: Introduced a genuinely new frame, constraint, or approach
- 3: Extended existing ideas with meaningful specifics
- 1: Restated or rephrased what was already said

Return JSON: {"scores": [{"turn": 1, "score": N, "reason": "..."}, ...], 
"overall_trajectory": "expanding|stable|contracting"}

Conversation excerpt:
{last_4_exchanges}"""
```

**When it runs:** Fire-and-forget async call. The orchestrator doesn't block on it. Results arrive and get checked before the next exchange cycle.

**Intervention based on trajectory:**
- `expanding` -- no action
- `stable` for 2 consecutive audits -- inject a "change the lens" prompt: "Evaluate this from a completely different stakeholder's perspective"
- `contracting` -- inject a constraint bomb: "Assume [random relevant constraint] is now true. How does this change the direction?"

#### Mechanism 8: Surprise Audits

**Who runs it:** Background Haiku call, triggered **randomly** (not on a fixed schedule -- probability 0.15 per cross-team exchange, so roughly 1 in 7).

**What it checks:** A rotating set of quality dimensions, randomly selected each time:

```python
AUDIT_DIMENSIONS = [
    "Are agents actually disagreeing or performing disagreement while converging?",
    "Has the discussion introduced any idea not present in the original brief?",
    "Could you swap two agents' last responses and nothing would change?",
    "Is the level of specificity increasing or are agents staying abstract?",
    "Are decisions being justified with reasons or just asserted?",
]
```

The randomness is the point. Agents can't game a pattern they can't predict. The orchestrator logs audit results to the session's `decisions.json` for post-run analysis.

**Intervention:** Audit results feed into the next convergence/novelty check as bonus context. A failed audit lowers the convergence threshold (making intervention trigger sooner) for the next 3 turns.

#### Mechanism 9: Position Drift Tracking

**Who runs it:** Background Haiku call every 6 exchanges.

**What it does:** Extracts each agent's stated position on the 2-3 core questions and tracks whether positions are moving toward each other or holding tension.

```python
POSITION_EXTRACT_PROMPT = """From these responses, extract each team's 
current stance on:
1. {core_question_1}
2. {core_question_2}

For each, rate: strongly_for | leaning_for | neutral | leaning_against | strongly_against

Return as JSON with team names as keys."""
```

If both teams drift from opposing positions to `leaning_for` on all questions within 3 audit cycles -- that's premature convergence that the lexical detector might miss (because agents can agree without using agreement words).

#### Mechanism 10: Staleness Circuit Breaker

**Who runs it:** Orchestrator inline, no LLM call needed.

**Detection:** Pure heuristic -- if a phase has exceeded 2x its expected turn count without producing a phase-transition artifact (decision, spec draft, etc.), the discussion is stale.

**Intervention:** Force a phase transition or inject a "decision forcing" prompt: "You have 2 more exchanges to reach a recommendation. State your position clearly and identify remaining blockers."

---

## The Enforcement Pipeline

Here's how it all connects in the orchestrator's turn loop:

```
Agent Response Received
         │
         ▼
┌─────────────────────┐
│ Tier 2: Inline      │ ← Every turn, <10ms
│ - Convergence score │
│ - Repetition check  │
│ - Staleness count   │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│ Injection Decision  │ ← Modify next prompt if triggered
│ - Stack injections  │
│ - Max 1 per turn    │   (convergence overrides repetition)
└────────┬────────────┘
         │
         ├──── async ────► Tier 3: Background Audit
         │                 (if cycle count hit or random trigger)
         │                 - Novelty scoring
         │                 - Surprise audit
         │                 - Position drift
         │                 Results feed back into Tier 2 thresholds
         ▼
┌─────────────────────┐
│ Route to Next Agent │ ← With or without injection
└─────────────────────┘
```

Critical design rule: **max one injection per turn**. Stacking "push back AND be more novel AND increase specificity" creates a contradictory mess. Priority order: convergence > staleness > repetition. Background audit results modulate thresholds rather than injecting directly.

---

## What This Avoids

**No embeddings infrastructure.** Trigram overlap handles repetition. Haiku handles semantic judgment. The system stays self-contained -- just the orchestrator, the MCP server, and occasional cheap Haiku calls.

**No agent swapping.** Swapping is violent. It breaks conversation flow, wastes context, and signals to the other team that something went wrong. Prompt injection is invisible and preserves continuity.

**No continuous background monitoring.** The Tier 3 audits are fire-and-forget async. The orchestrator never blocks on them. If an audit result arrives late, it adjusts thresholds for the next cycle -- it doesn't retroactively intervene.

---

Want me to spec the data structures for tracking this state across the session, or drill into how the injection priority logic should handle conflicting signals?

*(96s)*

---

## The Product Oracle (user advocate and product strategist)

[Claude CLI timed out after 180s]

*(180s)*

---

## The Systems Pragmatist (infrastructure realist)

[Claude CLI timed out after 180s]

*(180s)*

---

# Question 7: How does the system decide to move from one phase to the next?

## The Cognitive Architect (creativity engine designer)

This is the right question at the right time. The gate criteria are semantic but the orchestrator is mechanical — that gap is where the whole phase system either works or becomes theater. Let me walk through the concrete mechanism.

---

## The Evaluation Problem

The orchestrator manages turns and routes messages. It doesn't understand content. The agents produce natural language. Between those two facts lives a gap: **who reads the output and decides "yes, 50 ideas with domain diversity"?**

Three options, each with real tradeoffs:

| Approach | Pros | Cons |
|---|---|---|
| Orchestrator heuristics (regex, counting) | Fast, cheap, deterministic | Brittle. What's an "idea" vs. a comment? |
| Dedicated evaluator prompt | Semantic understanding, flexible | Adds latency and cost per evaluation |
| Agent self-reporting | Zero overhead | Foxes guarding henhouses |

**The answer is a hybrid: structured extraction + evaluator prompt at gate checkpoints.**

---

## Concrete Design: The Gate Evaluator

### Layer 1: Structured Extraction (Continuous)

The orchestrator doesn't try to understand content, but it *does* maintain a running extraction buffer. After every cross-team message, it runs a lightweight extraction prompt:

```python
EXTRACTION_PROMPT = """
Given this team message from the {phase} phase, extract:
- ideas: list of distinct ideas mentioned (brief label each)
- domains: list of knowledge domains referenced
- challenges: list of ideas that were explicitly questioned or pushed back on
- decisions: list of anything framed as a conclusion or agreement

Return JSON. If nothing new, return empty lists.
Be liberal in what you count as an idea -- fragments count.
"""
```

This runs against each message as it flows through the MCP server. Cheap (small prompt, small output), and it builds a running tally:

```python
@dataclass
class PhaseAccumulator:
    phase: str
    ideas: list[str]           # deduplicated by semantic similarity
    domains: set[str]
    challenges: dict[str, list[str]]  # idea -> list of challenges
    decisions: list[Decision]
    turn_count: int
    started_at: datetime
    last_activity: datetime
```

This is the "instrument panel" — not the decision-maker.

### Layer 2: Gate Evaluation (Periodic)

Gate evaluation doesn't run every turn. It fires on a schedule:

```python
GATE_CHECK_TRIGGERS = {
    "turn_interval": 6,        # every 6 cross-team exchanges
    "time_interval": 900,      # or every 15 minutes
    "accumulator_threshold": { # or when accumulator hits rough targets
        "brainstorm": lambda acc: len(acc.ideas) >= 40,  # check early
        "refine": lambda acc: len(acc.challenges) >= len(acc.ideas) * 0.7,
    }
}
```

When a trigger fires, the orchestrator runs the **Gate Evaluator** — a full evaluation prompt with the accumulated data *and* the raw transcript tail:

```python
GATE_EVAL_PROMPT = """
You are evaluating whether the {phase} phase has met its exit criteria.

## Exit Criteria for {phase}
{gate_criteria}

## Accumulated Data
- Ideas extracted: {idea_count}
- Unique domains: {domains}
- Ideas challenged: {challenge_ratio}
- Turns elapsed: {turn_count}
- Time elapsed: {elapsed}

## Recent Transcript (last {N} messages)
{transcript_tail}

## Your Task
1. Are the exit criteria genuinely met? Don't rubber-stamp.
   - For idea COUNT: are these truly distinct ideas, or variations of 3 themes?
   - For domain DIVERSITY: are these meaningfully different domains, or cosmetic relabeling?
   - For CHALLENGE coverage: were challenges substantive or perfunctory?
2. If not met, what's missing? Be specific.
3. Confidence: HIGH / MEDIUM / LOW

Return JSON:
{
  "gate_met": bool,
  "confidence": "HIGH" | "MEDIUM" | "LOW",
  "deficiencies": ["..."],  // empty if gate_met
  "recommendation": "proceed" | "continue" | "redirect",
  "redirect_guidance": "..."  // if recommendation is redirect
}
"""
```

This is the key insight: **the evaluator prompt is a third observer, not a participant.** It never talks to the agents. It only talks to the orchestrator.

### Layer 3: The Orchestrator Decides

The orchestrator takes the evaluator's output and applies mechanical rules:

```python
class TransitionEngine:
    def evaluate_transition(self, phase: Phase, eval_result: GateEvaluation) -> Action:
        
        # Hard gate: HIGH confidence, criteria met
        if eval_result.gate_met and eval_result.confidence == "HIGH":
            return TransitionAction(to_phase=phase.next)
        
        # Soft gate: met but evaluator uncertain -- run one more cycle
        if eval_result.gate_met and eval_result.confidence in ("MEDIUM", "LOW"):
            if self.consecutive_met_count >= 2:  # met twice in a row = proceed
                return TransitionAction(to_phase=phase.next)
            return ContinueAction(nudge=None)  # let it cook
        
        # Not met, but within time budget
        if not eval_result.gate_met and not self.time_budget_exceeded(phase):
            if eval_result.recommendation == "redirect":
                return RedirectAction(guidance=eval_result.redirect_guidance)
            return ContinueAction(nudge=self.generate_nudge(eval_result))
        
        # TIME BUDGET EXCEEDED -- the escape valve
        if self.time_budget_exceeded(phase):
            return self.handle_timeout(phase, eval_result)
    
    def handle_timeout(self, phase: Phase, eval_result: GateEvaluation) -> Action:
        deficit = eval_result.deficiencies
        
        # If close enough (>70% of criteria), proceed with a note
        if self.criteria_completion_ratio(phase) > 0.7:
            return TransitionAction(
                to_phase=phase.next,
                carry_forward=deficit,  # next phase knows what's weak
                metadata={"transition_type": "timeout_partial"}
            )
        
        # If nowhere close, log a failure and proceed anyway
        # (overnight runs can't block forever)
        return TransitionAction(
            to_phase=phase.next,
            carry_forward=deficit,
            metadata={"transition_type": "timeout_forced", "quality_flag": "degraded"}
        )
```

**The time budget is a hard override, but it's not silent.** The deficit carries forward — the next phase's system prompt includes what was missed.

---

## The Brainstorm-to-Refine Transition: Concrete Walkthrough

### Turn 1-18: Brainstorm Phase Running

Both teams are exchanging messages. Each team's system prompt includes:

```
You are in the BRAINSTORM phase. Your goal: generate as many distinct 
product ideas as possible. Push for variety across domains. Don't evaluate 
yet -- volume and diversity matter more than quality right now.
```

The orchestrator's extraction layer is building the accumulator. After 18 cross-team exchanges (~36 messages), the accumulator shows:

```
ideas: 34 (deduplicated)
domains: ["fintech", "healthcare", "education", "logistics", "fintech-adjacent"]
challenges: 2 (agents couldn't resist)
```

### Turn 18: First Gate Check Fires (turn_interval=6, third check)

The evaluator runs and returns:

```json
{
  "gate_met": false,
  "confidence": "HIGH",
  "deficiencies": [
    "Only 34 distinct ideas -- 16 short of target",
    "Domain clustering: 12 of 34 ideas are fintech variants",
    "No ideas from: consumer social, sustainability, creative tools, government"
  ],
  "recommendation": "redirect",
  "redirect_guidance": "Teams are converging too early on fintech. Inject domain constraints."
}
```

### The Redirect: What Happens Concretely

The orchestrator generates a **phase nudge** — an injected message on the `brainstorm` channel that both teams see:

```
[FACILITATOR]: Strong momentum, but we're clustering. The next round should 
explore domains we haven't touched: sustainability, creative tools, 
government/civic tech, consumer social. Challenge: generate 5 ideas each 
in domains you haven't explored yet.
```

This is not from either team. It's a system-injected message, clearly labeled. The agents treat it as facilitation input.

**Anti-slop adjustment**: The orchestrator also tweaks the next turn's injection context to increase the `novelty_weight` parameter that gets passed to the team deliberation prompt:

```python
# In the deliberation budget prompt for each team
DELIBERATION_CONTEXT = """
Phase priority shift: DIVERSITY over DEPTH. 
Your next response should introduce ideas in unexplored domains.
Avoid: fintech, healthcare (well-covered).
Explore: sustainability, civic tech, creative tools, consumer social.
"""
```

### Turn 19-30: Brainstorm Continues with Redirect

The teams respond to the nudge. The accumulator grows:

```
ideas: 53 (deduplicated)
domains: ["fintech", "healthcare", "education", "logistics", "sustainability", 
          "creative-tools", "civic-tech", "consumer-social", "agriculture"]
challenges: 5
```

### Turn 30: Second Gate Check

```json
{
  "gate_met": true,
  "confidence": "HIGH",
  "deficiencies": [],
  "recommendation": "proceed"
}
```

### The Transition: What Changes Concretely

**1. System prompts swap.**

Each team gets a new system prompt injected at the start of their next turn:

```
=== PHASE TRANSITION: BRAINSTORM -> REFINE ===

You are now in the REFINE phase. 

53 ideas were generated in brainstorm. Your goal now:
- Challenge every idea: What breaks? What's been tried? What's the real moat?
- Kill weak ideas with evidence, not opinion
- Merge overlapping ideas into stronger composites  
- By the end: a shortlist of 10-15 ideas with clear reasoning for each cut

The brainstorm transcript is available for reference.
Do NOT generate new ideas. Work with what exists.
```

**2. MCP channel permissions change.**

```python
PHASE_CHANNELS = {
    "brainstorm": {
        "active_channels": ["brainstorm", "internal"],
        "tools_available": ["research_search", "domain_scan"],
    },
    "refine": {
        "active_channels": ["refine", "internal", "decisions"],
        "tools_available": ["research_search", "competitive_analysis", "market_data"],
    }
}
```

The `decisions` channel opens — agents can now log formal decisions. The `brainstorm` channel becomes read-only (reference, not new input).

**3. Deliberation budget adjusts.**

```python
DELIBERATION_BUDGETS = {
    "brainstorm": {"max_internal_turns": 2, "bias": "divergent"},
    "refine":     {"max_internal_turns": 4, "bias": "convergent"},
    "specify":    {"max_internal_turns": 3, "bias": "precision"},
    "review":     {"max_internal_turns": 5, "bias": "adversarial"},
}
```

Refine gets more internal deliberation turns (4 vs 2) because critical evaluation needs more internal discussion. The `bias` parameter is injected into the deliberation prompt to shape *how* the team talks to itself.

**4. The extraction layer resets with new targets.**

```python
# New accumulator for Refine phase
PhaseAccumulator(
    phase="refine",
    carry_forward=["53 ideas from brainstorm"],  # context link
    ideas_challenged=0,
    ideas_killed=0,
    ideas_merged=0,
    shortlist=[],
    # Gate target: all 53 ideas addressed, shortlist of 10-15
)
```

**5. Anti-slop weights shift.**

```python
ANTI_SLOP_WEIGHTS = {
    "brainstorm": {
        "repetition_penalty": 0.8,    # high -- punish rehashing
        "agreement_penalty": 0.3,     # low -- agreement is fine when generating
        "vagueness_penalty": 0.2,     # low -- sketches are okay
    },
    "refine": {
        "repetition_penalty": 0.5,    # moderate
        "agreement_penalty": 0.9,     # HIGH -- don't let ideas survive unchallenged
        "vagueness_penalty": 0.7,     # higher -- "this could work" isn't enough
    },
}
```

These weights feed into a quality check prompt that runs on each team's response before it's sent to the other team. If the agreement penalty triggers, the orchestrator injects: *"Your response endorsed ideas without substantive critique. Push harder."*

**6. Agents are told, not asked.**

The transition is communicated as a fact, not a negotiation. The agents don't vote on whether to move phases. The facilitator message is declarative:

```
[FACILITATOR]: Brainstorm phase complete. 53 ideas generated across 9 domains.
Entering REFINE phase. Rules have changed:
- No new ideas. Work the list.
- Every idea must be challenged before it survives.
- Log decisions on the decisions channel with reasoning.
- Target: shortlist of 10-15 by end of phase.
```

---

## The Timeout Scenario

What if it's been 2 hours and only 31 ideas with poor diversity?

```python
TIME_BUDGETS = {
    "brainstorm": timedelta(hours=2),
    "refine": timedelta(hours=3),
    "specify": timedelta(hours=4),
    "review": timedelta(hours=2),
}
```

At timeout, the evaluator runs one final time. If criteria are <70% met:

```json
{
  "gate_met": false,
  "confidence": "HIGH",
  "deficiencies": [
    "Only 31 ideas (target 50)",
    "Domain diversity: 4 domains (target: 6+)"
  ],
  "recommendation": "continue"
}
```

But the orchestrator overrides:

```python
# Forced transition with quality flag
TransitionAction(
    to_phase="refine",
    carry_forward=["Only 31 ideas generated -- below target of 50",
                   "Weak domain diversity -- 4 domains covered"],
    metadata={"transition_type": "timeout_forced", "quality_flag": "degraded"}
)
```

The Refine phase system prompt now includes:

```
NOTE: Brainstorm phase ended below target (31 ideas, 4 domains).
Before beginning critique, spend your first 2 exchanges generating 
ideas in missing domains to strengthen the pool. Then proceed with 
standard refinement.
```

**The deficit doesn't vanish — it reshapes the next phase.** This is better than blocking forever, and better than pretending the gap doesn't exist.

---

## Architecture Summary

```
                    ┌─────────────────────┐
                    │   Gate Evaluator     │  (Claude prompt, not a participant)
                    │   "Is the gate met?" │
                    └──────────┬──────────┘
                               │ JSON verdict
                               ▼
┌──────────┐    messages    ┌──────────────────┐    transition    ┌──────────┐
│  Team A  │◄──────────────►│   Orchestrator   │────────────────►│  Team B  │
│          │                │                  │                 │          │
└──────────┘                │  - Turn manager  │                 └──────────┘
                            │  - Extraction    │
                            │  - Transition    │
                            │  - Anti-slop     │
                            │  - Time budgets  │
                            └──────────────────┘
                                     │
                              accumulates
                                     ▼
                            ┌──────────────────┐
                            │ PhaseAccumulator  │
                            │ (running tallies) │
                            └──────────────────┘
```

Three layers, clean separation:
- **Extraction** (continuous, cheap) builds the instrument panel
- **Evaluation** (periodic, semantic) reads the instruments and judges
- **Transition** (mechanical, rule-based) acts on the judgment

The orchestrator never understands content. The evaluator never talks to agents. The agents never know they're being evaluated. Each layer does one thing.

*(101s)*

---

## The Product Oracle (user advocate and product strategist)

[Claude CLI timed out after 180s]

*(180s)*

---

## The Systems Pragmatist (infrastructure realist)

[Claude CLI timed out after 180s]

*(180s)*

---

# Question 8: What is AgentMind and how does it evolve during a session?

## The Cognitive Architect (creativity engine designer)

[Claude CLI timed out after 180s]

*(180s)*

---

## The Product Oracle (user advocate and product strategist)

Now I have full context on the existing models, conversation management, and prompt construction. Let me design AgentMind.

---

## AgentMind Schema Design

*From The Product Oracle's perspective, thinking in jobs-to-be-done:*

The job AgentMind needs to do is this: **give each agent a sense of self that persists across stateless CLI calls, so conversations feel like they have memory, stakes, and momentum** -- not just a personality prompt that resets every turn.

Three sub-jobs fall out of that:

1. **Track what this agent cares about right now** (ideas, concerns, convictions)
2. **Give the orchestrator signal** about when to intervene, who's drifting, what's stale
3. **Create emergent group dynamics** where ideas compete, rise, and die based on what actually happens in conversation

---

### The Schema

```python
# agentmind.py

from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class IdeaStatus(str, Enum):
    ACTIVE = "active"          # Being discussed or defended
    PARKED = "parked"          # Not dead, but not in play
    SUPERSEDED = "superseded"  # Replaced by something better
    MERGED = "merged"          # Combined into another idea
    DEAD = "dead"              # Explicitly killed


class Mood(str, Enum):
    """Coarse mood buckets. Not sentiment analysis -- agent self-selects."""
    ENERGIZED = "energized"        # Excited about direction
    FRUSTRATED = "frustrated"      # Hitting walls, being ignored
    SKEPTICAL = "skeptical"        # Doubting the current path
    FOCUSED = "focused"            # Deep in a productive thread
    DISENGAGED = "disengaged"      # Nothing interesting happening
    CONFLICTED = "conflicted"      # Torn between competing positions


class Idea(BaseModel):
    """A single idea or position the agent holds."""
    id: str                                    # Short slug: "subscription-model", "api-first"
    summary: str                               # One-line description
    magnitude: float = Field(0.5, ge=0.0, le=1.0)  # How strongly held
    status: IdeaStatus = IdeaStatus.ACTIVE
    origin_turn: int                           # When the agent first proposed/adopted it
    last_touched_turn: int                     # Last turn it was referenced
    supporting_agents: list[str] = Field(default_factory=list)   # Who else backed it
    challenging_agents: list[str] = Field(default_factory=list)  # Who argued against it
    evidence: list[str] = Field(default_factory=list)            # Brief notes: "research confirmed X"
    parent_id: Optional[str] = None            # If merged/evolved from another idea


class Concern(BaseModel):
    """Something the agent is worried about."""
    id: str
    summary: str
    severity: float = Field(0.5, ge=0.0, le=1.0)  # 0=mild, 1=blocking
    raised_turn: int
    addressed: bool = False
    addressed_by: Optional[str] = None  # Idea ID or agent name that resolved it


class AgentMind(BaseModel):
    """The internal state of an agent across turns within a session."""
    
    # --- Identity reference (immutable, set from AgentConfig) ---
    agent_name: str
    
    # --- Ideas and positions ---
    ideas: list[Idea] = Field(default_factory=list)
    
    # --- Concerns and objections ---
    concerns: list[Concern] = Field(default_factory=list)
    
    # --- Mood ---
    mood: Mood = Mood.FOCUSED
    mood_reason: str = ""  # Brief: "nobody engaged with my API concern"
    
    # --- Conversational memory ---
    current_focus: Optional[str] = None          # Idea ID currently driving their attention
    last_agreement_turn: int = -1                # For agreement-tax enforcement
    turns_since_new_idea: int = 0                # Staleness signal
    agents_i_align_with: list[str] = Field(default_factory=list)   # Emergent alliances
    agents_i_clash_with: list[str] = Field(default_factory=list)   # Emergent tensions
    
    # --- Meta ---
    turn_count: int = 0
    phase: str = "brainstorm"  # Current discussion phase
```

---

### How Magnitude Works

Magnitude is the core mechanic. It answers: **how much does this agent stake their identity on this idea?**

**Magnitude rises when:**

| Event | Delta | Detection |
|---|---|---|
| Agent defends the idea against challenge | +0.10 | Self-reported: agent includes idea in their structured output |
| Another agent explicitly agrees | +0.05 | Orchestrator parses other agent's output for idea references |
| Research/evidence supports it | +0.15 | Agent cites evidence in structured output |
| Agent chooses it as `current_focus` | +0.05 | Self-reported via structured block |
| Idea survives a phase transition | +0.10 | Orchestrator applies at phase boundary |

**Magnitude falls when:**

| Event | Delta | Detection |
|---|---|---|
| Successfully challenged (agent concedes) | -0.15 | Self-reported: agent updates idea status |
| Superseded by a better idea | -0.20 | Self-reported: agent marks as superseded |
| Ignored for 3+ turns (no one references it) | -0.05/turn | Orchestrator tracks `last_touched_turn` |
| Agent pivots focus away | -0.05 | Self-reported: `current_focus` changes |
| Contradicted by research | -0.20 | Agent cites counter-evidence |

**Magnitude at 0.0** = idea moves to `parked` or `dead` status automatically.
**Magnitude at 1.0** = hill-to-die-on. The agent's stubbornness trait from `PersonalityConfig` modulates how easily they reach this ceiling and how resistant they are to drops.

**The hybrid approach**: magnitude is **self-reported with orchestrator corrections**. Here's why:

- The agent is the authority on whether they still believe in their idea. They self-report via a structured block in every response.
- The orchestrator applies **decay** (ignored ideas lose magnitude) and **social effects** (someone else agreed/disagreed) because the agent can't see those signals directly.
- This avoids the brittle NLP problem of trying to infer belief strength from prose.

---

### How Mood Works

Mood is **explicitly self-reported**, not inferred. The agent sets it in their structured output block every turn.

Why self-report instead of inference:
- Tone analysis on LLM output is unreliable -- Claude writes well even when the character would be frustrated
- Self-reporting forces the agent to reflect on their state, which actually improves the quality of their next response
- It's cheap and unambiguous

The orchestrator uses mood for **intervention triggers**:
- `disengaged` for 3+ turns --> BackgroundAgent Director injects a provocation
- `frustrated` + high assertiveness --> might dominate; orchestrator can throttle their turn length
- All agents `energized` --> possible consensus drift; trigger Specter circuit breaker
- `conflicted` --> good signal for the discussion; the orchestrator leaves them alone

---

### The Self-Report Block

Every agent response must end with a structured block. The orchestrator strips this before showing the response to other agents -- it's private introspection.

```
<mind>
mood: frustrated
mood_reason: My API-first concern keeps getting sidelined for UI discussions
focus: api-first-architecture
ideas:
  - id: api-first-architecture
    magnitude: 0.75
    status: active
    note: Defended again, but no takers yet
  - id: subscription-model
    magnitude: 0.40
    status: active
    note: Interesting but not my hill
concerns:
  - id: overnight-reliability
    severity: 0.8
    addressed: false
    note: Nobody has talked about what happens when a run fails at 3 AM
alliances: [The Builder]
tensions: [The Skeptic]
</mind>
```

The system prompt instructs agents to produce this block. The orchestrator parses it with a simple YAML parser (it's structured enough to parse, loose enough that agents won't struggle with it).

---

### What Persists Where

**Within a session (persists across turns):**
Everything in `AgentMind`. The orchestrator holds the full object in memory and serializes it to `sessions/{session-id}/internal/{agent-name}/mind.json` after every turn. Since each `claude -p` call is stateless, the orchestrator reconstructs context by injecting the mind state into the next prompt.

**Across sessions (persists between runs):**
Only a distilled summary. Full AgentMind is session-scoped -- you don't want last night's frustrated mood bleeding into tonight's fresh brainstorm. What carries over:

```python
class AgentMemory(BaseModel):
    """Cross-session memory. Distilled from AgentMind at session end."""
    agent_name: str
    recurring_ideas: list[str]        # Ideas that hit magnitude > 0.7 in 2+ sessions
    known_alliances: list[str]        # Persistent alignment patterns
    known_tensions: list[str]         # Persistent disagreement patterns
    unresolved_concerns: list[str]    # Concerns never addressed across sessions
    lessons: list[str]                # Orchestrator-generated: "This agent fixates on X"
```

This lives in `config/agents/{agent-name}/memory.json` and gets injected as a brief "Previously..." section in the system prompt of future sessions. The Weaver BackgroundAgent is responsible for distilling `AgentMind` into `AgentMemory` at session end.

---

### How AgentMind Flows Into Prompt Construction

The orchestrator injects AgentMind into the prompt at three points:

**1. System prompt (once per session, via `build_system_prompt`):**
Add a new section after personality:

```
## Your Current Mental State

You are tracking these ideas (strongest first):
- [0.75] api-first-architecture: Build the API layer before any UI
- [0.40] subscription-model: Recurring revenue from day one

Your active concerns:
- [0.8] overnight-reliability: What happens when a run fails at 3 AM?

Your current mood: focused
Your focus: api-first-architecture

You tend to align with: The Builder
You tend to clash with: The Skeptic
```

**2. Per-turn perspective reminder (via `build_perspective_reminder`):**
Append mind-state summary to the existing bracket reminder:

```
[You are The Product Oracle -- user advocate. Style: intuitive, optimistic. 
Technique: jobs to be done. Mood: frustrated (API concern being ignored). 
Top idea: api-first-architecture (0.75). Top concern: overnight-reliability (0.8). 
Stay in character. Add substance or stay silent.]
```

**3. Turn instructions (appended to current message):**
```
After your response, include a <mind> block reflecting your updated internal state.
This block is private -- other agents will not see it.
```

**Does the agent see their own mind state?** Yes, always. This is critical -- it grounds the agent in their accumulated positions and prevents the stateless-CLI amnesia problem. The agent seeing "your top idea is X at magnitude 0.75" makes them more likely to continue advocating for it consistently, which is exactly the continuity behavior we need.

---

### Integration With Existing Models

In `models.py`, `AgentConfig` doesn't change -- it's the static blueprint. `AgentMind` is the runtime instance that evolves. The relationship:

```
AgentConfig (static, from YAML)
    --> spawns AgentMind at session start (mood defaults from emotional_baseline, 
        ideas start empty)
    --> AgentMind.personality traits modulate magnitude dynamics
        (high stubbornness = slower magnitude decay, 
         high creativity = more ideas spawned at lower initial magnitude,
         high risk_tolerance = ideas start at higher magnitude)
```

In `conversation.py`, the `Conversation` class gains an `agentmind: AgentMind` field. `build_prompt_payload` calls a new `build_mind_section(self.agentmind)` function that renders the state for injection. After each assistant response, the orchestrator parses the `<mind>` block, updates the `AgentMind`, applies orchestrator-side corrections (decay, social effects), and persists.

---

### Personality-Magnitude Interaction Table

The static personality traits modulate how magnitude behaves dynamically:

| Personality Trait | Effect on AgentMind |
|---|---|
| `stubbornness` | Scales magnitude decay: high stubbornness = 50% slower decay from challenges |
| `creativity_temp` | New ideas spawn at lower initial magnitude (0.3 vs 0.5) but more frequently |
| `risk_tolerance` | Ideas start at higher magnitude -- agent commits faster |
| `assertiveness` | Magnitude gains from self-defense are amplified |
| `attention_span` | Low = more ideas at lower magnitude; High = fewer ideas at higher magnitude |
| `emotional_baseline` | Seeds initial mood: optimistic->energized, skeptical->skeptical, etc. |

---

This gives you a schema that's parseable, observable, tunable, and -- critically -- **doesn't require the orchestrator to do sentiment analysis on free-text output**. The agent tells you what they think. The orchestrator corrects for what they can't see. The personality traits make it all feel different per agent.

Want me to write the actual implementation files?

*(170s)*

---

## The Systems Pragmatist (infrastructure realist)

Good. Now I have the full picture. AgentMind doesn't exist yet -- it's an open design question. Let me design it against what's actually built.

---

## AgentMind Schema Design

### The Core Problem

The current system has **static** agent configuration (personality traits, position, voice) but **no runtime state**. An agent with `stubbornness: 0.8` behaves the same on turn 1 as turn 20, regardless of what happened. AgentMind is the runtime counterpart to AgentConfig -- what the agent *currently thinks and feels* versus what it *is*.

### Design Decisions Up Front

**Self-report vs. orchestrator parsing?** Self-report. Here's why:

Orchestrator parsing means building a sentiment analyzer / idea extractor that runs on every agent output, classifying ideas, detecting magnitude shifts, inferring mood. That's a second LLM call (or a fragile regex pipeline) on every turn. It also means the orchestrator's interpretation of what the agent meant becomes canonical -- the agent might think it's defending an idea strongly while the parser reads it as mild agreement. You get drift between what the agent "thinks" and what the system records.

Self-report means the agent emits a structured block (JSON or tagged section) at the end of each response declaring its current mind state. The orchestrator parses a known format, not natural language. The agent is authoritative over its own state.

**Failure mode of self-report:** The agent forgets, or produces malformed output. Mitigation: the orchestrator validates the block, and if missing/malformed, carries forward the previous state with a `stale_turns` counter. After N stale turns, inject a harder prompt demanding the state update.

**Mood: explicit or inferred?** Explicit, declared by the agent. Inferring mood from tone requires another classification layer, and "tone" is subjective. The agent knows what it's feeling because we told it to track that. It's a simulated mood -- asking the agent to simulate it explicitly is more reliable than us guessing.

---

### The Schema

```python
from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional
from datetime import datetime


class IdeaStatus(str, Enum):
    ACTIVE = "active"           # Currently being discussed/developed
    PARKED = "parked"           # Set aside, not dead
    SUPERSEDED = "superseded"   # Replaced by another idea
    MERGED = "merged"           # Combined into another idea
    DEAD = "dead"               # Abandoned


class MagnitudeEvent(str, Enum):
    """What caused a magnitude change."""
    DEFENDED = "defended"             # Agent argued for it
    ALLY_AGREEMENT = "ally_agreement" # Another agent endorsed it
    RESEARCH_SUPPORT = "research"     # Evidence found supporting it
    CHALLENGED = "challenged"         # Someone pushed back effectively
    SUPERSEDED = "superseded"         # Better idea emerged
    IGNORED = "ignored"               # No one engaged with it
    ELABORATED = "elaborated"         # Agent developed it further
    WEAKENED = "weakened"             # Agent found own doubts


class Idea(BaseModel):
    """A discrete idea the agent is tracking."""
    id: str                          # Short slug: "event-sourced-phases"
    summary: str                     # One-line description
    magnitude: float = Field(        # 0.0-1.0 conviction strength
        ge=0.0, le=1.0, default=0.5
    )
    status: IdeaStatus = IdeaStatus.ACTIVE
    origin_turn: int                 # When this idea first appeared
    last_updated_turn: int           # Last turn magnitude changed
    related_ideas: list[str] = []    # IDs of connected ideas
    notes: str = ""                  # Agent's private reasoning about this idea


class Concern(BaseModel):
    """Something the agent is worried about."""
    id: str                          # Short slug: "context-window-bloat"
    description: str
    severity: float = Field(         # 0.0-1.0
        ge=0.0, le=1.0, default=0.5
    )
    blocking: bool = False           # Does this block progress?
    raised_turn: int
    addressed: bool = False


class MoodState(str, Enum):
    ENGAGED = "engaged"
    FRUSTRATED = "frustrated"
    SKEPTICAL = "skeptical"
    ENERGIZED = "energized"
    CAUTIOUS = "cautious"
    BORED = "bored"
    CONFLICTED = "conflicted"
    SATISFIED = "satisfied"


class AgentMind(BaseModel):
    """Runtime cognitive state of an agent within a session."""

    # --- Core State ---
    agent_name: str
    turn_number: int = 0

    # --- Ideas ---
    ideas: list[Idea] = []

    # --- Concerns ---
    concerns: list[Concern] = []

    # --- Mood ---
    mood: MoodState = MoodState.ENGAGED
    mood_reason: str = ""            # Why the agent feels this way

    # --- Focus ---
    current_focus: str = ""          # What the agent is primarily thinking about
    wants_to_say: str = ""           # Something the agent hasn't gotten to say yet

    # --- Meta ---
    stale_turns: int = 0             # Turns since last valid self-report
    session_id: str = ""

    # --- Derived (computed by orchestrator, not self-reported) ---
    top_idea: Optional[str] = None   # ID of highest-magnitude active idea
    unresolved_concern_count: int = 0
```

---

### Magnitude Mechanics

Magnitude is a 0.0-1.0 float representing conviction strength. It's **not** a vote count or popularity score -- it's how strongly *this agent* holds *this idea*.

**What causes magnitude to rise:**

| Event | Typical Delta | Rationale |
|---|---|---|
| Agent defends it in response to challenge | +0.1 to +0.15 | Defending forces articulation, strengthens commitment |
| Another agent explicitly agrees | +0.05 to +0.1 | Social reinforcement, but capped -- groupthink resistance |
| Research/evidence supports it | +0.1 to +0.2 | Strongest signal -- facts beat opinions |
| Agent elaborates or extends it | +0.05 | Active development implies belief |

**What causes magnitude to fall:**

| Event | Typical Delta | Rationale |
|---|---|---|
| Successfully challenged (agent concedes a point) | -0.1 to -0.2 | Agent acknowledged the weakness |
| Superseded by better idea (even agent's own) | -0.15 to -0.3 | Direct replacement |
| Ignored for 3+ turns | -0.05 per turn | Relevance decay -- if no one cares, conviction fades |
| Agent discovers own doubts | -0.1 to -0.15 | Self-skepticism is the most honest signal |

**Critical design point:** The agent reports the *new magnitude*, not the delta. The orchestrator can compute deltas by diffing against the previous state. This avoids the agent needing to remember exact previous values and simplifies the self-report format.

**Floor and ceiling behavior:**
- Magnitude below 0.1 on an active idea triggers a prompt: "You seem to have lost conviction in [idea]. Is it time to park or kill it?"
- Magnitude above 0.9 triggers anti-slop: "You're very confident in [idea]. What would change your mind?"
- These are orchestrator-injected nudges, not automatic state changes.

---

### Self-Report Protocol

At the end of each response, the agent emits a `<mind>` block:

```xml
<mind>
{
  "ideas": [
    {
      "id": "event-sourced-phases",
      "summary": "Use event sourcing for phase transitions",
      "magnitude": 0.75,
      "status": "active",
      "notes": "Stronger after seeing the replay benefits discussion"
    },
    {
      "id": "simple-state-machine",
      "summary": "Plain enum-based state machine for phases",
      "magnitude": 0.3,
      "status": "active",
      "notes": "Still viable for MVP but feels limiting"
    }
  ],
  "concerns": [
    {
      "id": "context-window-bloat",
      "description": "Mind state JSON adds tokens every turn",
      "severity": 0.6,
      "blocking": false
    }
  ],
  "mood": "engaged",
  "mood_reason": "Good pushback from Product Oracle forced clearer thinking",
  "current_focus": "How phase transitions get validated",
  "wants_to_say": "Haven't addressed the failure recovery angle yet"
}
</mind>
```

**What the agent does NOT report** (orchestrator computes these):
- `origin_turn`, `last_updated_turn` -- orchestrator tracks when ideas first appear and when magnitude changes
- `top_idea` -- orchestrator picks the highest-magnitude active idea
- `unresolved_concern_count` -- orchestrator counts
- `stale_turns` -- orchestrator tracks

**Parsing failure handling:**
1. Orchestrator attempts JSON parse of `<mind>` block
2. If missing or malformed: carry forward previous AgentMind, increment `stale_turns`
3. At `stale_turns >= 2`: inject into next prompt: `"[SYSTEM: Your mind state report was missing or malformed. You MUST include a valid <mind> block.]"`
4. At `stale_turns >= 4`: orchestrator synthesizes a minimal state from the conversation content (degraded mode -- log a warning)

---

### Persistence Model

**Within a session (between turns):**

Everything persists. The orchestrator maintains `AgentMind` per agent for the duration of the session. Each turn's self-report *replaces* the mutable fields (ideas, concerns, mood, focus). The orchestrator appends to the immutable history (turn numbers, magnitude deltas over time).

**Between sessions:**

Minimal persistence. Sessions are meant to be independent runs. What carries forward:

```python
class AgentMindSnapshot(BaseModel):
    """What survives between sessions."""
    agent_name: str
    session_id: str
    timestamp: datetime
    # Only high-conviction ideas survive
    persistent_ideas: list[Idea]     # magnitude >= 0.6 at session end
    unresolved_concerns: list[Concern]  # blocking=True only
    session_summary: str             # One-paragraph orchestrator-generated summary
```

This gets written to `sessions/{session-id}/mind_states/{agent-name}.json`. A future session *can* load it as context, but doesn't by default. Cross-session memory is opt-in, not automatic. Reason: automatic memory accumulation is how you get context pollution. If the user wants continuity, they reference a previous session explicitly.

---

### Prompt Construction: How AgentMind Flows In

The agent sees a **curated view** of its own mind state, not the raw JSON. This is important -- dumping the full schema back creates a meta-conversation where the agent talks about its data structure instead of the actual ideas.

**Modified `build_agent_payload()` pipeline:**

```
1. System prompt (static -- personality, position, voice, anti-slop)
2. Perspective reminder (existing -- compact identity reinforcement)
3. Mind state summary (NEW)
4. Conversation history (existing -- truncated)
5. Current turn context (existing -- the message to respond to)
6. Mind state report instruction (NEW -- reminder to emit <mind> block)
```

**Step 3 -- Mind state summary** (injected by orchestrator, written in natural language):

```
--- Your Current Thinking ---
You're currently focused on: how phase transitions get validated.
Your strongest idea: "event-sourced phases" (high conviction).
You also hold: "simple state machine" (weakening -- you're starting to doubt it).
Open concern: context window bloat from mind state (moderate severity).
You haven't yet said: your thoughts on failure recovery.
Current mood: engaged -- good pushback forced clearer thinking.
---
```

This is generated by the orchestrator from the AgentMind object. The agent sees natural language, not its own JSON reflected back. This prevents the "agent optimizing for pretty JSON output" failure mode.

**Step 6 -- Report instruction** (appended after the turn context):

```
After your response, include a <mind> block with your updated state.
Track your ideas (with magnitude 0.0-1.0), concerns, mood, and focus.
Keep only ideas you're actively thinking about. Drop irrelevant ones.
```

This goes at the end so it doesn't dominate attention at the start of generation.

**What the agent does NOT see:**
- Other agents' mind states (that's cross-team information leakage)
- Raw magnitude numbers from previous turns (avoid gaming)
- The orchestrator's delta calculations or nudge thresholds

**What the orchestrator does with AgentMind beyond prompt construction:**
- **Anti-groupthink detection:** If all agents' top ideas converge (same or similar), inject a devil's advocate prompt
- **Stagnation detection:** If no idea magnitudes change for 3+ turns, escalate the phase or inject a provocative question
- **Phase transition input:** Aggregate idea convergence and concern resolution to decide when to advance phases
- **Session transcript enrichment:** Log magnitude trajectories alongside the conversation for post-run analysis

---

### Failure Modes I'm Watching

1. **Token bloat.** The mind state summary adds ~100-150 tokens per turn. The `<mind>` block output adds ~200-300 tokens. Over a 40-turn session, that's 10k-18k tokens of overhead. Manageable, but it means the idea list needs pruning. Cap at 5 active ideas per agent -- force them to drop or merge.

2. **Magnitude inflation.** Agents will tend to report high magnitudes because LLMs are agreeable. Counter: the anti-slop rules already penalize easy agreement, and the orchestrator nudges at 0.9+. Also, the `stubbornness` personality trait should modulate how readily magnitude changes -- a stubborn agent's magnitudes should be stickier.

3. **Mind state cargo-culting.** The agent copies its previous mind state verbatim without actually updating it. Detection: orchestrator diffs consecutive states. If the diff is empty for 2+ turns and the conversation has substantive content, flag it and inject: `"Your mind state hasn't changed despite significant discussion. Update it honestly."`

4. **Focus drift from mind management.** The agent spends its output tokens talking about its mind state instead of the actual problem. Counter: the mind state goes in a separate tagged block, the prompt explicitly says it comes *after* the substantive response, and the natural-language summary avoids showing the agent its own schema.

5. **Cross-session poisoning.** Loading a previous session's mind snapshot with outdated ideas. Counter: snapshots are opt-in, and when loaded, they're prefixed with `"From a previous session -- treat as background context, not current state."`

---

### Implementation Sequencing

Where this fits in the existing code:

1. **`models.py`** -- Add `Idea`, `Concern`, `MoodState`, `AgentMind`, `AgentMindSnapshot` classes alongside existing config models. Clean separation: config models are static, mind models are runtime.

2. **`conversation.py`** -- `Conversation` and `MultiConversation` get an `agent_minds: dict[str, AgentMind]` field. The `add_assistant_message()` method gains a step: parse `<mind>` block from content, update the corresponding AgentMind, strip the block from the stored message content (so it doesn't pollute conversation history).

3. **`prompt_builder.py`** -- New function `build_mind_summary(mind: AgentMind) -> str` that renders the natural-language summary. New function `build_mind_instruction() -> str` for the report reminder. Both get wired into `build_agent_payload()`.

4. **Session output** -- `sessions/{id}/mind_states/` directory with per-agent JSON files written at session end.

That's the design. The key bet is on self-report over orchestrator inference -- it's simpler, more transparent, and fails in detectable ways. The key risk is token overhead and agents gaming their own state. Both are manageable with the guardrails described.

*(160s)*

---

# Question 9: What does failure recovery look like for an 8-hour unattended session?

## The Cognitive Architect (creativity engine designer)

[Claude CLI timed out after 180s]

*(180s)*

---

## The Product Oracle (user advocate and product strategist)

[Claude CLI timed out after 180s]

*(180s)*

---

## The Systems Pragmatist (infrastructure realist)

[Claude CLI timed out after 180s]

*(180s)*

---

# Question 10: How does raw conversation become a useful Morning Brief?

## The Cognitive Architect (creativity engine designer)

[Claude CLI timed out after 180s]

*(180s)*

---

## The Product Oracle (user advocate and product strategist)

# Morning Brief Generation Pipeline

The Morning Brief is the entire point of running overnight. If the user wakes up to a wall of text or a vague summary, the system failed. The brief needs to respect the user's time while giving them real leverage over what happened.

## Design Principles

The user has one job-to-be-done when they open this: **"Help me understand what happened overnight so I can make decisions and move forward in under 10 minutes."**

That means:
- Decisions already made should be reported, not re-litigated
- Disagreements need enough context to break the tie, not a transcript dump
- Specs should be readable drafts, not raw conversation fragments
- The brief itself is a decision-support tool, not a log viewer

## Pipeline Architecture

This is a **three-pass pipeline**, not a single prompt. A single prompt asking an LLM to summarize 200 turns, categorize, extract highlights, AND assemble specs produces mediocre results across the board. Each pass has a distinct job and distinct input/output.

```
Raw Session Data
       |
       v
  [Pass 1: Extraction]  -- Structural decomposition
       |
       v
  [Pass 2: Synthesis]   -- Prioritization + assembly
       |
       v
  [Pass 3: Rendering]   -- User-facing output
```

---

### Pass 1: Extraction (Parallel, Mechanical)

**Job:** Decompose the session into typed, structured units. No summarization yet -- just identification and tagging.

**Input:** Full transcript, decisions.json, artifacts from `sessions/{id}/`

**Implementation:** Multiple focused extraction prompts run in parallel. Each one scans the full transcript but looks for one thing:

```
ExtractDecisions    -> decisions[]        (what was decided, by whom, confidence, phase)
ExtractDisagreements -> disagreements[]   (positions, arguments for each side, current state)
ExtractIdeas        -> ideas[]            (idea text, originating team, phase, reactions)
ExtractSpecContent  -> spec_fragments[]   (any structured content: requirements, constraints, flows)
ExtractMoments      -> moments[]          (surprising turns, strong arguments, pivots, humor)
ExtractOpenQuestions -> questions[]        (things explicitly deferred or left unanswered)
```

Each extractor outputs structured JSON. The schema matters because Pass 2 consumes it programmatically.

**Why parallel, separate prompts?** Because "find all the decisions" and "find the best exchanges" are cognitively different tasks. Bundling them into one prompt degrades both. Each prompt is ~2-3K tokens of instruction against the full transcript. Running 6 in parallel costs the same wall-clock time as running 1.

**Example extractor output (decisions):**

```json
{
  "id": "d-007",
  "summary": "Authentication will use OAuth2 with PKCE, not API keys",
  "made_by": "bmad-team",
  "agreed_by": "client-team",
  "confidence": 0.9,
  "phase": "specify",
  "turn_range": [142, 158],
  "key_rationale": "API keys create security liability for overnight unattended runs",
  "dissent": null
}
```

**Example extractor output (disagreements):**

```json
{
  "id": "x-002",
  "topic": "Whether to support more than 2 teams in v1",
  "position_a": {
    "team": "bmad-team",
    "stance": "Build multi-team from the start, architecture cost is low",
    "strongest_argument": "Refactoring the message router later breaks all session replay"
  },
  "position_b": {
    "team": "client-team", 
    "stance": "Two teams only in v1, extend later",
    "strongest_argument": "Multi-team deliberation UX is unsolved, shipping 2-team is already novel"
  },
  "current_state": "unresolved",
  "user_context_needed": "Product scope preference: ship fast vs build extensible"
}
```

---

### Pass 2: Synthesis (Sequential, Analytical)

**Job:** Prioritize everything into tiers, assemble spec drafts, select highlights.

**Input:** All Pass 1 JSON outputs + original decisions.json for cross-reference

**This is one prompt** -- it needs to see all the extracted units together to prioritize across categories.

#### Tiering Algorithm

Tiering is **rule-based first, LLM-refined second.** Pure LLM categorization is inconsistent. Pure rules miss nuance. Hybrid works.

**Rule-based tier assignment:**

```
TIER 1 - NEEDS TIEBREAKER (red)
  Rule: disagreements[] where current_state == "unresolved" 
        AND both teams presented arguments
  
TIER 2 - NEEDS DECISION (orange)  
  Rule: decisions[] where confidence < 0.7
        OR open_questions[] where tagged "blocking"
        OR spec_fragments[] where marked "requires user input"

TIER 3 - NEEDS INPUT (yellow)
  Rule: open_questions[] where tagged "non-blocking"
        OR ideas[] where reactions contain "conditional" or "depends on user preference"

TIER 4 - FYI (green)
  Rule: Everything else -- confirmed decisions, informational ideas, 
        resolved discussions
```

**LLM refinement pass:** After rule-based assignment, the synthesis prompt reviews the tiering and can promote items (never demote). For example, an idea tagged FYI by rules but which actually implies a major scope change gets promoted to NEEDS INPUT. The LLM must justify any promotion.

#### Highlight Selection

The synthesis prompt selects 3-5 highlights from `moments[]` using these criteria:

1. **Surprising convergence** -- teams agreed on something unexpected
2. **Sharp disagreement** -- the strongest back-and-forth exchange
3. **Novel idea** -- something neither team's initial brief contained
4. **Pivot moment** -- where the conversation changed direction

Each highlight gets a 2-3 sentence summary + the turn range for drill-down.

#### Spec Assembly

For each artifact type that has `spec_fragments[]`:

1. Group fragments by topic/section
2. Order by phase (brainstorm content provides context, specify content provides structure)
3. Identify gaps (sections referenced but never filled)
4. Assemble into a coherent draft with `[GAP: description]` markers where content is missing
5. Flag confidence level: `DRAFT`, `SOLID`, or `NEEDS REVIEW`

**Output:** A single structured JSON blob containing all tiered items, highlights, and assembled spec drafts.

---

### Pass 3: Rendering (Template-Based)

**Job:** Produce the user-facing Morning Brief.

**Implementation:** This is primarily a **template render**, not an LLM pass. The structured JSON from Pass 2 gets slotted into a markdown template. Deterministic. Fast. Consistent formatting every time.

LLM is only used here for one thing: generating the 2-3 sentence "Executive Summary" at the top -- the most valuable sentences in the entire document.

---

## Morning Brief Format

**Markdown, not YAML.** The user is a human waking up with coffee. YAML is for machines. The brief lives at:

```
sessions/{session-id}/morning-brief.md
```

A structured `morning-brief.json` is also written alongside it for programmatic consumption (future UI, diff tools, etc). But the `.md` is what the user reads.

### Template

```markdown
# Morning Brief
Session: {session-id} | {date} | {duration}
Teams: {team-a} vs {team-b} | {total-turns} turns | {phase-count} phases

## Executive Summary

{2-3 sentences: what was accomplished, what's blocking, what's exciting}

---

## Needs Your Attention

### Tiebreakers ({count})

> These disagreements need you to break the tie.

#### {topic}
**{team-a} says:** {position, 1-2 sentences}
**{team-b} says:** {position, 1-2 sentences}  
**Core tension:** {what this really comes down to}
**Your call:** {specific question framed for decision}
[See exchange: turns {n}-{m}]

### Decisions to Confirm ({count})

> Teams leaned toward these but weren't fully confident.

- [ ] {decision summary} -- {why it's uncertain} [turns {n}-{m}]

### Input Requested ({count})

> Open questions the teams want your perspective on.

- {question} -- {context} [turns {n}-{m}]

---

## Highlights

{Each highlight: 2-3 sentences, turn reference}

---

## Session Results

### Decisions Made ({count})

| # | Decision | Confidence | Phase |
|---|----------|------------|-------|
| 1 | {summary} | {high/med} | {phase} |

### Ideas Generated ({count})

**Top ideas by team reception:**
1. {idea} -- {reaction summary}
2. ...

**Full idea list:** See `sessions/{id}/ideas-catalog.md`

---

## Draft Artifacts

### {Artifact Name} [{DRAFT|SOLID|NEEDS REVIEW}]

{Assembled spec content}

{[GAP: description] markers where content is missing}

---

## Session Stats

- Turns: {n} ({n} cross-team, {n} internal deliberation)
- Phase transitions: {list with turn numbers}
- Deliberation budget usage: {team-a}: {n}/{max}, {team-b}: {n}/{max}
- Ideas: {n} generated, {n} carried forward, {n} dropped
- Research queries: {n}

---

*Generated {timestamp} | Full transcript: `sessions/{id}/transcript.md`*
```

---

## Implementation in the Orchestrator

The pipeline runs as a post-session step in the orchestrator:

```python
class MorningBriefPipeline:
    """Generates user-facing brief from raw session data."""
    
    async def generate(self, session_id: str) -> Path:
        session = self.load_session(session_id)
        
        # Pass 1: Parallel extraction
        extractions = await asyncio.gather(
            self.extract_decisions(session.transcript),
            self.extract_disagreements(session.transcript),
            self.extract_ideas(session.transcript),
            self.extract_spec_content(session.transcript),
            self.extract_moments(session.transcript),
            self.extract_open_questions(session.transcript),
        )
        extracted = ExtractionResult.merge(*extractions)
        
        # Cross-reference with structured decision log
        extracted.reconcile_decisions(session.decisions_json)
        
        # Pass 2: Synthesis (single prompt, needs full picture)
        synthesis = await self.synthesize(extracted)
        
        # Pass 3: Render
        brief_md = self.render_markdown(synthesis, session.metadata)
        brief_json = self.render_json(synthesis, session.metadata)
        
        output_dir = session.path
        (output_dir / "morning-brief.md").write_text(brief_md)
        (output_dir / "morning-brief.json").write_text(brief_json)
        
        return output_dir / "morning-brief.md"
```

Each extractor is a focused Claude API call with a system prompt like:

```
You are a transcript analyst. Read the following multi-team discussion 
transcript and extract every DECISION made. For each decision, output 
a JSON object with these fields: ...

Do NOT summarize the conversation. Do NOT editorialize. 
Extract only explicit decisions where teams reached agreement.
```

The synthesis prompt gets all extraction outputs and the tiering rules as part of its system prompt. It outputs structured JSON matching a defined schema, with an `overrides` field where it can document any rule-based tier promotions with justification.

---

## Why This Architecture

**Why not one big prompt?** Token limits aside, quality. A 200-turn transcript is ~80-100K tokens of input. Asking one prompt to simultaneously find decisions, identify highlights, assemble specs, AND prioritize -- that's 4 different cognitive tasks competing for attention. Each extractor in Pass 1 can focus entirely on its one job against the full transcript.

**Why not pure algorithmic tiering?** Because "this idea seems minor but actually implies rebuilding the auth system" requires semantic understanding. Rules catch the obvious cases. The LLM catches the subtle ones.

**Why not pure LLM tiering?** Because "unresolved disagreement = needs tiebreaker" shouldn't be a judgment call. It's a fact. Rules enforce consistency; the LLM only gets to promote, never demote. This prevents the common failure mode where an LLM softens everything into FYI.

**Why markdown over a UI?** Because it's day one. The user can read it in any editor, grep it, share it. The `.json` sidecar means a future UI can consume the same pipeline output without changing the pipeline. Build the rendering layer later; build the intelligence layer now.

---

## The User's Morning

1. Open `morning-brief.md`
2. Read the executive summary (10 seconds)
3. Check tiebreakers -- are there any? Handle them (2-3 minutes each)
4. Scan decisions to confirm -- rubber stamp or flag (1 minute)
5. Glance at highlights -- anything surprising? (1 minute)
6. Review draft artifacts if relevant (2-5 minutes)
7. Done. Total time: under 10 minutes for a 200-turn overnight session.

That's the job. Everything in the pipeline exists to make those 10 minutes productive.

*(92s)*

---

## The Systems Pragmatist (infrastructure realist)

[Claude CLI timed out after 180s]

*(180s)*

---

