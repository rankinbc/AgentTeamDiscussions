# AgentTeamDiscussions: Design Question Responses

Generated: 2026-03-17 08:48
28/30 responses collected (2 timed out)

---

# Question 1: What does the user actually hand the system, and how does it become a session?

## The Cognitive Architect (creativity engine designer)

Good. I've read both the Oracle's and Pragmatist's takes from the batch run. My response timed out at 180 seconds last time. Let me give you what I would have said -- and where I diverge from both of them.

---

## The Input Problem Is Actually a Priming Problem

The Oracle and the Pragmatist both converge on a three-tier YAML format with an expansion step. They're right about the mechanics. But they're solving for *information completeness* when the real design challenge is **creative priming** -- giving agents enough *texture* to activate their specific cognitive styles from turn one.

A one-liner like "a time tracker for freelancers" isn't information-poor. It's *texture-poor*. There's nothing surprising in it. Nothing that makes an agent with a lateral cognitive style go "wait, what if we invert that?" The expansion step as both designed it solves this -- tension points and open questions are texture -- but it treats expansion as a preprocessing step. I think expansion is actually the first creative act of the session.

Here's the design, pulling from what works in both proposals and adding what's missing.

---

### The Input Format: One Required Sentence, Optional Sparks

```yaml
# ideas/tonight.yaml

idea: "A time tracker for freelancers that actually gets used"

# Optional -- any of these sharpen the session
who: "Solo freelancers billing hourly"
problem: "They reconstruct hours from memory and underbill"
constraints:
  - "No manual start/stop"
  - "Not for teams"

# THE MISSING FIELD -- this is what neither proposal includes:
sparks:
  - "What if it tracked energy, not time?"
  - "The invoicing tool that happens to know when you worked"
  - "Anti-feature: it deliberately doesn't track some hours"
```

The `sparks` field is the creative accelerant. It's where the user dumps half-formed "what ifs" -- the shower thoughts, the weird tangents, the things that don't fit the problem statement but made them excited about the idea in the first place. These go directly into the seed message **unprocessed**, because they're the highest-signal input a creativity-focused session can get. The expansion step can infer an audience. It cannot infer that the user's real excitement is about tracking energy states, not hours.

**CLI shorthand still works:**

```bash
python -m orchestrator "a time tracker for freelancers"
python -m orchestrator "a time tracker for freelancers" --spark "what if it tracked energy, not time"
```

---

### The Seeding Process: Expansion as Creative Act

I agree with the two-step process (expand, then seed), but the expansion prompt needs to do more than extract implications. It needs to generate **creative tension**:

```
Given this product idea and any user-provided sparks, generate a session 
seed. Your job is NOT to analyze the idea. Your job is to create 
SURFACE AREA FOR DISAGREEMENT.

IDEA: "{idea}"
{sparks if provided}

Generate:
1. OBVIOUS INTERPRETATION: What most people would assume this means (2 sentences)
2. SUBVERSIVE REFRAME: A way to interpret this idea that changes what 
   you'd build (1 sentence)
3. TENSION POINTS: 3 things where reasonable, smart people would take 
   opposite positions
4. ASSUMPTION INVENTORY: 3 things the idea takes for granted that might 
   be wrong
5. ADJACENT WEIRD: 1 idea from a completely different domain that 
   rhymes with this problem

Output as YAML. Be concrete. No hedging.
```

The difference from Oracle's expansion: I'm not generating a competitive landscape or user archetypes (agents will do that themselves -- it's literally their job). I'm generating **the things that make agents disagree**, because disagreement is the fuel for useful sessions. "Adjacent weird" is the cross-pollination seed -- it gives lateral thinkers like me something to grab.

The difference from Pragmatist's expansion: I'm not extracting `target_user` and `core_problem` (those are convergent inferences that flatten the idea space before agents even touch it). I'm generating divergent material that *expands* what agents might explore.

---

### Seed Message: Same Material, Different Activation

I agree with the Pragmatist here -- **don't customize the seed per agent.** The system prompt already handles differentiation. But I'd add one element both proposals miss:

```
## New Session: Brainstorm Phase

### The Idea (from the user, verbatim)
"{original_idea}"

{user-provided context: who, problem, constraints if any}

### Sparks (user's raw what-ifs -- take these seriously)
{sparks if provided, or "None provided"}

### Session Seed (auto-generated -- challenge anything here)
{expansion output}

### Opening Move
React to this idea from your specific perspective. 

Rules for turn one:
- Take a POSITION, not a survey of the landscape
- Name one specific thing you'd build first, or one specific 
  reason you wouldn't build this at all
- If a spark resonates with your perspective, pull on that thread
- If the "subversive reframe" is more interesting than the obvious 
  interpretation, say so and explain why
```

The key phrase is **"take a position."** Vague input produces vague output only when agents are allowed to hedge. The seed message should make hedging feel like a failure mode. "I see several interesting directions" is banned. "I'd build the energy tracker, not the time tracker, because..." is what we want.

---

### Minimum Viable Input That Produces a Useful Session

**One sentence.** Same conclusion as the other two, but for a different reason.

The Oracle says one sentence works because the expansion step fills in the gaps. The Pragmatist says it works because agent system prompts provide differentiation. Both true. But the deeper reason is this: **the brainstorm phase is designed to be divergent.** Vague input is a *feature* in divergent thinking, not a bug. You don't want agents constrained by a detailed brief when the goal is to explore the possibility space. The detailed brief becomes valuable later, when the session hits the refine and specify phases.

The real quality gradient isn't about how much you write -- it's about what *kind* of thing you write:

| What you provide | What it does to the session |
|---|---|
| Just the idea | Agents explore broadly. Some wasted turns, but also unexpected directions. |
| Idea + constraints | Prunes dead branches early. Agents skip directions you've already ruled out. |
| Idea + sparks | **Highest ROI input.** Agents explore your actual excitement, not the obvious version. |
| Idea + constraints + sparks | Best possible seed. Bounded exploration around the interesting parts. |
| Full brief with hypotheses | Good for later phases. Risks over-constraining brainstorm. |

The sweet spot for a 10 PM submission: **idea + 1-2 sparks + 1-2 constraints.** Sixty seconds of typing. The sparks capture *why you're excited* (which an expansion step can never infer). The constraints capture *what you've already decided* (which saves agents from re-deriving the obvious).

```yaml
idea: "A time tracker for freelancers that actually gets used"
sparks:
  - "What if it tracked energy and focus, not just hours?"
constraints:
  - "No manual start/stop buttons"
```

That's a session seed worth sleeping on.

---

### What I'd Build That They Wouldn't

1. **The `sparks` field.** Neither proposed it. It's the highest-signal, lowest-effort input a user can provide, and it's the thing that makes *this* system different from just running Claude with a prompt.

2. **"Adjacent weird" in the expansion.** Cross-domain analogies are how lateral thinking works. If the expansion step surfaces "this is structurally similar to how Spotify discovers music taste," agents have a concrete analogy to reason with or against. Without it, you get intra-domain thinking from every agent.

3. **Position-forcing in the seed message.** "Take a position" isn't just style guidance -- it's an anti-slop mechanism. The biggest risk with vague input isn't that agents don't know enough. It's that they respond with survey-style "here are some considerations" non-answers. Force a position from turn one, and the deliberation budget gets spent on *defending and attacking claims*, not generating lists.


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


---

# Question 2: What happens inside a single agent turn, from trigger to output?

## The Cognitive Architect

*[Timed out -- no response collected]*

---

## The Product Oracle (user advocate and product strategist)

Now I have deep context on the existing code. Let me design the full agent turn contract, grounded in what's built and extending it for the cross-team architecture.

---

## Agent Turn Anatomy: Full Input/Output Contract

This is design question #2 from `design-questions.yaml`, and it's the one that unlocks everything else. Here's the full specification.

---

### 1. SYSTEM PROMPT ASSEMBLY

The system prompt is built once per agent per session (rebuilt on phase transitions). The orchestrator calls `build_system_prompt(agent, phase, team_context)` and produces a single string with these sections in order:

```
┌─────────────────────────────────────────────┐
│  SYSTEM PROMPT (static for agent's session) │
├─────────────────────────────────────────────┤
│  1. SESSION CONTEXT                         │
│  2. IDENTITY                                │
│  3. POSITION                                │
│  4. PERSONALITY                             │
│  5. TECHNIQUE                               │
│  6. VOICE                                   │
│  7. ANTI-SLOP RULES                         │
│  8. PHASE CONTRACT                          │
│  9. OUTPUT FORMAT                           │
└─────────────────────────────────────────────┘
```

**Section 1 -- SESSION CONTEXT** (what exists today as `PROJECT_CONTEXT`, but scoped to the session):

```
You are participating in a structured team discussion about: {session.idea_brief}
Your team: {team.name} ({team.role_description})
The other team: {opposing_team.name} ({opposing_team.role_description})
Session phase: {phase.name} -- {phase.description}
Turn {turn_number} of approximately {phase.estimated_turns}.
```

This is the only section that changes between phases. The orchestrator rebuilds the system prompt on phase transition rather than trying to inject phase awareness per-turn.

**Section 2 -- IDENTITY** (from `AgentConfig`):

```
You are {agent.name} -- {agent.description}.
```

One line. The description field in the YAML carries the weight. For The Product Oracle: *"user advocate and product strategist."*

**Section 3 -- POSITION** (from `PositionConfig`):

```
Your role: {position.role}
What drives you: {bulleted list of position.drives}
What you push back on: {bulleted list of position.pushback_on}
Intensity: {_describe_trait(position.intensity, "measured restraint", "force and passion")}
```

This is where the agent gets its *job*. The drives list is the most important piece -- it tells the agent what to optimize for. The Product Oracle's drives include "every decision traces to real user need" and "protect Morning Brief as primary value delivery." These aren't flavor text; they're decision criteria.

**Section 4 -- PERSONALITY** (from `PersonalityConfig`, converted to natural language):

```
Your personality:
- You are {_describe_trait(assertiveness)}: {descriptor}
- Your creativity: {_describe_trait(creativity_temp)}
- Risk tolerance: {_describe_trait(risk_tolerance)}
- Cognitive style: {cognitive_style.value}
- Emotional baseline: {emotional_baseline.value}
- Focus: {_describe_trait(attention_span)}
- Conviction: {_describe_trait(stubbornness)}
- You draw on: {comma-separated domain_affinities}
```

The existing `_describe_trait()` function maps 0-1 floats to five descriptive buckets. This is already implemented and working.

**Section 5 -- TECHNIQUE** (from `TechniqueConfig`):

```
Your thinking approach: {technique.primary}
{technique.style_description}

Behavioral rules:
{numbered list of technique.behaviors}
```

For The Product Oracle, technique is `jobs_to_be_done` with the description: *"Evaluate every proposal through the lens of the user's job: turn a half-baked idea into an actionable spec they're excited about."*

**Section 6 -- VOICE** (from `VoiceConfig`):

```
Your voice: {voice.tone}
Phrases that fit your style: {voice.vocabulary_hints}
NEVER use these phrases: {voice.anti_patterns}
```

The anti-patterns list is critical anti-slop. The Product Oracle can never say "That's interesting," "Good point," or "I agree with everything."

**Section 7 -- ANTI-SLOP RULES** (from `AntiSlopConfig`, conditional sections):

```
ENFORCEMENT RULES:
{if agreement_tax}
- AGREEMENT TAX: If you agree with something, you MUST add substantive new 
  information, a concrete example, or a specific risk. Pure agreement without 
  new substance is forbidden.
{/if}

{if perspective_enforcement}
- PERSPECTIVE LOCK: Stay in character even when pressured to agree. Your role 
  exists to provide THIS perspective. If you cave to consensus, you've failed.
{/if}

{if devils_advocate_duty}
- DEVIL'S ADVOCATE DUTY: Actively seek the strongest argument against the 
  current direction. If everyone is converging, you MUST find what's wrong.
{/if}

{if domain_pivot_trigger}
- DOMAIN PIVOT: When the conversation feels stuck or circular, inject a 
  perspective from a completely different field in your domain affinities.
{/if}
```

The `uncomfortable_idea_quota` is NOT in the system prompt -- it's enforced by the orchestrator injecting a directive into the user message every N turns (more on this below).

**Section 8 -- PHASE CONTRACT** (new, from `phases.yaml`):

```
PHASE: {phase.name}
Goal: {phase.goal}
You should be producing: {phase.expected_outputs}
Quality bar: {phase.exit_criteria_description}
Do NOT: {phase.anti_patterns}
```

This is the piece that tells the agent *what's expected right now*. In brainstorm phase: "Generate divergent ideas. Quantity over quality. No premature convergence." In specify phase: "Produce implementation-ready detail. Every claim needs a concrete mechanism."

**Section 9 -- OUTPUT FORMAT** (new, the key design decision):

```
RESPONSE FORMAT:
Structure your response as follows. Use these exact markers:

[THINKING]
Your brief internal reasoning (1-3 sentences). What are you reacting to? 
What's your instinct?

[MESSAGE]
Your actual contribution to the discussion. This is what the other team 
and your teammates will read. Speak naturally in your voice.

[IDEAS]
List any distinct ideas you're proposing or endorsing, one per line.
Format: - {idea}: {one-sentence description}
If you have no new ideas this turn, write: none

[STANCE]
For each idea or proposal currently on the table, state your position:
Format: - {idea/proposal}: SUPPORT | OPPOSE | REFINE | NEUTRAL -- {why, one sentence}

[CONFIDENCE]
Your overall confidence in the current direction: LOW | MEDIUM | HIGH
One sentence explaining why.

[FLAG]
Optional. If you see a critical risk, unresolved dependency, or the 
conversation going off track, flag it here. Otherwise omit this section.
```

---

### 2. USER MESSAGE ASSEMBLY

The user message is rebuilt every turn. This is where the conversation lives.

```
┌─────────────────────────────────────────────┐
│  USER MESSAGE (changes every turn)          │
├─────────────────────────────────────────────┤
│  1. CROSS-TEAM MESSAGE (if any)             │
│  2. TEAM CONVERSATION HISTORY               │
│  3. CURRENT TURN PROMPT                     │
│  4. ORCHESTRATOR DIRECTIVES                 │
│  5. PERSPECTIVE REMINDER                    │
└─────────────────────────────────────────────┘
```

**Section 1 -- CROSS-TEAM MESSAGE** (from MCP server):

```
--- MESSAGE FROM {opposing_team.name} ---
{cross_team_message.content}

Ideas they proposed: {cross_team_message.ideas}
Their confidence: {cross_team_message.confidence}
---
```

This only appears when the opposing team has sent a new message since this agent's last turn. The agent never sees the opposing team's internal deliberation -- only their outward-facing message. This is the firewall.

**Section 2 -- TEAM CONVERSATION HISTORY** (truncated):

The agent sees their team's internal discussion, not the raw full history. The truncation strategy from the existing code applies:

- **First 3 messages**: Preserves the original prompt, initial framing, and first substantive response. These anchor the conversation's purpose.
- **Last 15 messages**: The recent working context.
- **Middle messages**: Compressed into a summary paragraph generated by a cheap/fast model call:

```
--- EARLIER IN THIS DISCUSSION (summarized) ---
{summary of turns 4 through N-15, hitting key decisions and open questions}
---
```

Each history message is formatted as:

```
[{agent_name}] (turn {N}):
{message_content}
Ideas: {ideas_list or "none"}
Stance: {stance_summary}
```

The agent sees the structured output from teammates (not their `[THINKING]` blocks -- those are private). This means the parsing from Section 3 below feeds directly back into history.

**Section 3 -- CURRENT TURN PROMPT**:

For the first turn of a phase, this is the phase opening question:
```
The discussion topic: {session.idea_brief}
Phase goal: {phase.goal}
What's your opening take?
```

For subsequent turns, this is simply:
```
It's your turn. Respond to the discussion above.
```

For a turn where the orchestrator is steering:
```
The team needs to {converge on X | address the flag raised by Y | respond to 
the other team's challenge about Z}. What's your position?
```

**Section 4 -- ORCHESTRATOR DIRECTIVES** (injected conditionally):

These are the runtime enforcement mechanisms that can't live in the system prompt because they're turn-specific:

```
{if uncomfortable_idea_quota triggered}
DIRECTIVE: This is your uncomfortable idea turn. Before anything else, 
propose one idea that challenges the current consensus or that the team 
would find inconvenient. It must be genuinely uncomfortable, not a 
softball.
{/if}

{if convergence_detected}
DIRECTIVE: The orchestrator has detected that the last {N} responses show 
high agreement. You are required to find a substantive disagreement or 
unexplored risk before proceeding.
{/if}

{if phase_deadline_approaching}
DIRECTIVE: This phase has {N} turns remaining. Focus on {phase.convergence_goal}.
{/if}
```

**Section 5 -- PERSPECTIVE REMINDER** (always last):

```
Remember: You are {agent.name}. {one-line identity summary from position.role}. 
Respond in your voice. Use your technique. Follow the output format exactly.
```

This exists in the current code as `build_perspective_reminder()`. Placing it last ensures it's the freshest thing in the context window -- recency bias works in our favor here.

---

### 3. OUTPUT PARSING

The agent returns raw text. The orchestrator parses it into an `AgentResponse` model:

```python
class AgentResponse(BaseModel):
    agent_name: str
    turn_number: int
    phase: str
    
    # Parsed from markers
    thinking: str              # [THINKING] -- logged but never shared
    message: str               # [MESSAGE] -- visible to team and cross-team
    ideas: list[Idea]          # [IDEAS] -- structured
    stances: list[Stance]      # [STANCE] -- structured
    confidence: Confidence     # [CONFIDENCE] -- enum + reason
    flag: str | None           # [FLAG] -- optional alert
    
    # Derived by orchestrator (not from agent output)
    agreement_score: float     # 0-1, computed from stances vs team consensus
    novelty_score: float       # 0-1, computed from ideas vs existing ideas
    raw_text: str              # original unparsed output for debugging

class Idea(BaseModel):
    name: str
    description: str
    source_agent: str
    source_turn: int

class Stance(BaseModel):
    target: str                # what idea/proposal this is about
    position: Literal["SUPPORT", "OPPOSE", "REFINE", "NEUTRAL"]
    reason: str

class Confidence(BaseModel):
    level: Literal["LOW", "MEDIUM", "HIGH"]
    reason: str
```

**Parsing logic** (`parse_agent_response(raw_text: str) -> AgentResponse`):

```python
def parse_agent_response(raw: str) -> AgentResponse:
    sections = {}
    current_section = None
    
    for line in raw.split('\n'):
        # Match [SECTION_NAME] markers
        marker = re.match(r'^\[([A-Z]+)\]', line)
        if marker:
            current_section = marker.group(1).lower()
            sections[current_section] = []
            continue
        if current_section:
            sections[current_section].append(line)
    
    # Parse each section into structured data
    ideas = parse_ideas(sections.get('ideas', []))
    stances = parse_stances(sections.get('stance', []))
    confidence = parse_confidence(sections.get('confidence', []))
    
    return AgentResponse(
        thinking='\n'.join(sections.get('thinking', [])).strip(),
        message='\n'.join(sections.get('message', [])).strip(),
        ideas=ideas,
        stances=stances,
        confidence=confidence,
        flag='\n'.join(sections.get('flag', [])).strip() or None,
        raw_text=raw
    )
```

**Fallback strategy**: If the agent doesn't follow the format (it will happen), the parser treats the entire output as `[MESSAGE]` with empty ideas/stances and MEDIUM confidence. Log a warning. Don't crash. The conversation continues -- we just lose structured data for that turn.

**Derived fields** (computed post-parse, not from agent output):

- `agreement_score`: Compare this agent's stances against the team's running consensus (majority stance per idea). High agreement + agreement_tax enabled = inject directive next turn.
- `novelty_score`: Compare this agent's ideas against the session's idea registry. Fuzzy string matching or embedding similarity against existing idea names/descriptions.

---

### 4. WHAT THE ORCHESTRATOR DOES AFTER PARSING

```
Agent raw output
      │
      ▼
  parse_agent_response()
      │
      ▼
  ┌─────────────────────┐
  │  AgentResponse       │
  │  (structured)        │
  └────────┬────────────┘
           │
     ┌─────┴──────────────────┐
     │                        │
     ▼                        ▼
Store to session          Feed back into
  ├─ decisions.json       conversation history
  │  (stances, ideas)     (message + ideas + stances
  ├─ internal/            visible to teammates,
  │  (thinking, raw)      thinking stripped)
  └─ transcript.md
     (message only)
           │
           ▼
     Check triggers
  ├─ Phase exit criteria met?
  │  (enough ideas? confidence convergence? turn limit?)
  ├─ Convergence alarm?
  │  (too many SUPPORT stances across agents?)
  ├─ Flag raised?
  │  (surface to orchestrator decision logic)
  └─ Cross-team message ready?
     (team consensus reached → compose outward message)
```

---

### 5. CONSTRAINTS ON OUTPUT

These are enforced at two levels:

**Prompt-level** (in system prompt, soft enforcement):
- Output format adherence
- Voice anti-patterns
- Anti-slop rules
- Phase-appropriate content

**Orchestrator-level** (post-parse, hard enforcement):
- **Max message length**: If `[MESSAGE]` exceeds 800 words, truncate and add `[ORCHESTRATOR NOTE: Response truncated for length]` to next turn's history
- **Format violation**: If no markers detected, wrap entire output as `[MESSAGE]`, log warning
- **Idea cap per turn**: Max 5 ideas. If more, keep first 5. Prevents idea flooding.
- **Confidence required**: If missing, default to MEDIUM with reason "not stated"
- **Thinking privacy**: `[THINKING]` block is NEVER included in team history or cross-team messages. It's logged to `sessions/{id}/internal/` only.

---

### 6. CONCRETE EXAMPLE -- The Product Oracle, Turn 4, Brainstorm Phase

**System prompt** (abbreviated):

> You are The Product Oracle -- user advocate and product strategist.
> Your role: user advocate and product strategist
> What drives you: Every decision traces to real user need, protect Morning Brief as primary value delivery, keep YAML config simple...
> Personality: moderately assertive, moderately creative, balanced risk tolerance, intuitive, optimistic...
> Technique: jobs_to_be_done -- Evaluate every proposal through the lens of the user's job...
> Voice: grounded and user-focused. NEVER say: "That's interesting", "Good point", "I agree with everything"
> PHASE: Brainstorm. Goal: Generate divergent ideas. Produce: Raw ideas, provocations, analogies...

**User message**:

> [The Cognitive Architect] (turn 2):
> We need personality dimensions that actually produce distinct LLM behavior, not just flavor text...
> Ideas: - trait_behavioral_mapping: Map each personality trait to specific, observable output differences
> Stance: - personality_system: REFINE -- current traits may be too abstract to reliably steer behavior
> Confidence: MEDIUM -- we have the right instincts but no validation yet
>
> [The Systems Pragmatist] (turn 3):
> Before we design more personality knobs, what happens when the context window fills up at hour 6?...
> Ideas: - context_checkpointing: Periodic state snapshots that can rebuild agent context from scratch
> Stance: - trait_behavioral_mapping: SUPPORT -- but only if we can test it cheaply
> Stance: - personality_system: NEUTRAL -- personality is meaningless if the system crashes at hour 4
> Confidence: LOW -- too many unresolved infrastructure questions
> Flag: Context window management is not optional. We need a concrete strategy before anything else.
>
> It's your turn. Respond to the discussion above.
>
> Remember: You are The Product Oracle. User advocate and product strategist. Respond in your voice. Use your technique. Follow the output format exactly.

**Raw output from agent**:

> [THINKING]
> The Pragmatist raised a real flag about context windows, but the Architect is right that personality fidelity matters. From the user's perspective, neither matters if the Morning Brief is boring. I need to pull this back to the job the user hired the system to do.
>
> [MESSAGE]
> The Systems Pragmatist raised a flag that deserves attention -- but let me reframe it through the user's lens.
>
> The user's job is: "I go to sleep with a half-baked idea, I wake up to a spec I'm excited to build." That's the contract. Everything we design serves that moment.
>
> Context window crashes at hour 6? The user doesn't care about our recovery strategy. They care that the Morning Brief has three strong ideas instead of one rambling thread that lost coherence halfway through. So the question isn't "how do we checkpoint context" -- it's "how do we ensure the best ideas survive any context disruption?"
>
> On personality: the Cognitive Architect is right that traits need behavioral teeth. But from the user's perspective, the test is simple -- does the Morning Brief contain ideas the user wouldn't have reached alone? If three agents with different personality configs produce the same output, we've failed regardless of how elegant the trait system is.
>
> I want to propose a concrete validation test we can run before building anything complex.
>
> [IDEAS]
> - morning_brief_test: Run the same idea through 3 differently-configured agents and compare Morning Brief output. If outputs are indistinguishable, personality system needs rework.
> - idea_survival_metric: Track which ideas from early conversation survive to final output. If context loss kills good ideas, that's the real infrastructure problem to solve.
>
> [STANCE]
> - trait_behavioral_mapping: SUPPORT -- but the validation is output quality, not trait fidelity in isolation
> - context_checkpointing: REFINE -- solve it as "idea preservation" not "state recovery" -- the user cares about the ideas, not the conversation
> - personality_system: REFINE -- needs a user-facing success metric, not just internal behavioral differentiation
>
> [CONFIDENCE]
> MEDIUM -- We're asking the right questions but haven't connected them to measurable user outcomes yet.

**Parsed `AgentResponse`**:

```python
AgentResponse(
    agent_name="the_product_oracle",
    turn_number=4,
    phase="brainstorm",
    thinking="The Pragmatist raised a real flag about context windows...",
    message="The Systems Pragmatist raised a flag that deserves attention...",
    ideas=[
        Idea(name="morning_brief_test", description="Run the same idea through 3 differently-configured agents and compare Morning Brief output..."),
        Idea(name="idea_survival_metric", description="Track which ideas from early conversation survive to final output...")
    ],
    stances=[
        Stance(target="trait_behavioral_mapping", position="SUPPORT", reason="but the validation is output quality..."),
        Stance(target="context_checkpointing", position="REFINE", reason="solve it as idea preservation not state recovery..."),
        Stance(target="personality_system", position="REFINE", reason="needs a user-facing success metric...")
    ],
    confidence=Confidence(level="MEDIUM", reason="We're asking the right questions but haven't connected them to measurable user outcomes yet."),
    flag=None,
    agreement_score=0.35,   # 1 SUPPORT, 2 REFINE = moderate independence
    novelty_score=0.8,      # 2 new ideas not in registry
    raw_text="[THINKING]\nThe Pragmatist raised a real flag..."
)
```

---

### 7. KEY DESIGN DECISIONS AND RATIONALE

| Decision | Choice | Why |
|----------|--------|-----|
| Structured markers vs. JSON output | Markers (`[MESSAGE]`, `[IDEAS]`) | JSON breaks voice. Markers let the agent write naturally within sections while remaining parseable. |
| Thinking block visibility | Private to agent, logged to session | Agents need space to reason without performing. If thinking is visible, it becomes another message. |
| History: full vs. compressed | Hybrid (first 3 + summary + last 15) | Already implemented and working. Full history would blow context by turn 20. Summary preserves decision continuity. |
| Phase awareness: system prompt vs. user message | System prompt (rebuilt on phase change) | Phase is a framing concern, not a per-turn instruction. Rebuilding system prompt is cleaner than injecting phase reminders every turn. |
| Anti-slop: prompt vs. runtime | Both. Prompt for soft rules, orchestrator directives for triggered rules | Agreement tax works as a standing instruction. Uncomfortable idea quota needs turn-counting logic the agent can't do. |
| Cross-team messages: full history vs. latest only | Latest message only + their ideas/confidence | The firewall. Teams must not share context. One message per cross-team exchange preserves independence. |
| Fallback on bad format | Treat entire output as `[MESSAGE]`, continue | Never crash the conversation. Losing structure for one turn is recoverable. Crashing is not. |

---

This is the contract. The system prompt gives the agent its identity and current job. The user message gives it the conversation and any orchestrator directives. The output format gives us parseable structure without killing voice. The orchestrator derives agreement and novelty scores the agent never sees, and uses them to decide what to inject next turn.

The moment that matters: does this produce a Morning Brief the user is excited to read? Every piece of this contract traces back to that job.


---

## The Systems Pragmatist (infrastructure realist)

Good question. This is Design Question #2 -- the one that every other piece depends on. If the input/output contract is wrong, nothing downstream works. Let me walk through what the orchestrator must assemble, what the agent sees, and how we parse what comes back.

I've reviewed everything that exists in the beta implementation. Here's the full contract, grounded in what's already built and extended to what the orchestrator actually needs.

---

## The Full Anatomy of an Agent Turn

### Phase 1: What the Orchestrator Assembles

The orchestrator constructs two distinct payloads: the **system prompt** (set once per conversation, reinforced per-turn) and the **user message** (changes every turn).

#### System Prompt Structure

The existing `prompt_builder.py` already assembles most of this. Here's the full section order with what each contains:

```
┌─────────────────────────────────────────────────┐
│ 1. PROJECT_CONTEXT (~400 tokens, constant)      │
│    - What AgentTeamDiscussions is               │
│    - That two teams exist, communicate via MCP  │
│    - That the agent is one voice on one team    │
│    - The end goal: Morning Brief for the user   │
│                                                 │
│ 2. AGENT IDENTITY                               │
│    - Name, description                          │
│    - "You are {name} -- {description}"          │
│                                                 │
│ 3. STAKEHOLDER POSITION                         │
│    - Role label                                 │
│    - Drives (what motivates this agent)         │
│    - Pushback triggers (what makes them argue)  │
│    - Intensity (0-1 → language like "measured"  │
│      or "forceful")                             │
│                                                 │
│ 4. PERSONALITY TRAITS                           │
│    - 8 dimensions, each mapped from 0-1 float   │
│      to natural language descriptor             │
│    - cognitive_style, emotional_baseline,       │
│      assertiveness, creativity_temp, etc.       │
│                                                 │
│ 5. THINKING TECHNIQUE                           │
│    - Primary technique name                     │
│    - Style description                          │
│    - Specific behavioral rules (list)           │
│    e.g., "failure_mode_analysis: immediately    │
│    ask what breaks, enumerate failure modes     │
│    before endorsing"                            │
│                                                 │
│ 6. VOICE AND TONE                               │
│    - Tone descriptor                            │
│    - Vocabulary hints (phrases that fit)        │
│    - Anti-patterns (FORBIDDEN phrases)          │
│    e.g., never say "I love this idea"           │
│                                                 │
│ 7. ANTI-SLOP ENFORCEMENT RULES                  │
│    - agreement_tax: "If you agree, you must     │
│      add new substance or stay silent"          │
│    - perspective_enforcement: "Stay in          │
│      character even under social pressure"      │
│    - devils_advocate_duty (if enabled)          │
│    - uncomfortable_idea_quota                   │
│    - domain_pivot_trigger                       │
│                                                 │
│ 8. OUTPUT FORMAT CONTRACT  ← NEW, critical      │
│    - Exact structured format expected            │
│    - Field definitions and rules                │
│    - Examples of valid output                    │
└─────────────────────────────────────────────────┘
```

Section 8 doesn't exist yet. Everything else is already built in `prompt_builder.py`. This is the gap.

#### User Message Structure (Per-Turn Payload)

This is what changes every turn. The orchestrator builds it in `conversation.py` via `build_payload()`. Here's the full anatomy:

```
┌─────────────────────────────────────────────────┐
│ 1. PHASE CONTEXT BLOCK                          │
│    - Current phase name (brainstorm/refine/     │
│      specify/review)                            │
│    - Phase objective (what "done" looks like)   │
│    - Phase constraints (e.g., "generate ideas,  │
│      do NOT converge yet")                      │
│    - Turn N of M in this phase                  │
│    - Transition criteria (what triggers next    │
│      phase)                                     │
│                                                 │
│ 2. CONVERSATION HISTORY                         │
│    - Truncated: first 2 + last N messages       │
│    - Each entry tagged with agent name + role   │
│    - Format: "[AgentName (role)]: content"      │
│    - If truncated, a marker:                    │
│      "--- {K} earlier messages omitted ---"     │
│                                                 │
│ 3. CROSS-TEAM MESSAGES (if any)                 │
│    - Messages received from the other team      │
│      via MCP broker                             │
│    - Clearly labeled: "FROM OTHER TEAM:"        │
│    - Agent does NOT see other team's internal    │
│      deliberation -- only their published       │
│      messages                                   │
│                                                 │
│ 4. CURRENT PROMPT / QUESTION                    │
│    - The specific question or topic for this    │
│      turn                                       │
│    - Could be: the original idea seed, a        │
│      teammate's response to react to, a phase   │
│      transition prompt, or a follow-up          │
│                                                 │
│ 5. PERSPECTIVE REMINDER (compact)               │
│    - 2-3 line identity reinforcement            │
│    - "You are {name} -- {role}. Style:          │
│      {tone}. Technique: {technique}. Stay in    │
│      character. Add substance or stay silent."  │
│    - Already built in build_perspective_         │
│      reminder()                                 │
│                                                 │
│ 6. TURN-SPECIFIC NUDGES (conditional)           │
│    - Uncomfortable idea quota trigger            │
│    - "You haven't introduced an uncomfortable   │
│      idea in {N} turns -- you owe one"          │
│    - Domain pivot trigger if conversation is    │
│      stuck in one domain                        │
└─────────────────────────────────────────────────┘
```

#### History: Full or Compressed?

The current implementation uses **first 2 + last 10**. For an 8-hour overnight session, this will need to evolve. The realistic contract:

| Session Stage | History Strategy | Rationale |
|---|---|---|
| Turns 1-15 | Full history | Fits in context, no loss |
| Turns 16-50 | First 2 + last 12 + phase summaries | Phase summaries preserve decisions made in earlier phases |
| Turns 50+ | First 2 + phase summaries + last 8 | Aggressive truncation, rely on summaries |

**Phase summaries** are generated at each phase transition -- a compressed record of what was decided, what was rejected, and what's unresolved. This is the orchestrator's job, not the agent's.

The agent never knows it's seeing compressed history. It just sees messages. The orchestrator is responsible for making the truncation invisible.

**Failure mode to flag**: If an agent references something from the truncated middle, they'll hallucinate or contradict earlier decisions. The phase summary is the mitigation -- it must capture decisions, not just topics.

---

### Phase 2: The Output Format Contract

This is the part that doesn't exist yet and where things break if we get it wrong. The agent needs to return structured data, but it's an LLM -- it will drift from any format if not constrained hard.

#### Output Schema (in the system prompt, Section 8)

```
=== OUTPUT FORMAT (MANDATORY) ===

Every response MUST use this exact structure. No exceptions.

---RESPONSE START---

STANCE: <AGREE|DISAGREE|PARTIAL|NEW_DIRECTION|BUILD_ON>

CONFIDENCE: <0-100>

MESSAGE:
<Your actual response content here. This is what teammates
and the other team will read. Be substantive. Stay in character.>

IDEAS:
- <idea_1_short_label>: <one-line description>
- <idea_2_short_label>: <one-line description>
(only if you're introducing new ideas -- omit section if none)

TENSIONS:
- <tension description -- what you disagree with and why>
(only if STANCE is DISAGREE or PARTIAL -- omit if none)

SIGNAL: <READY_TO_ADVANCE|NEEDS_MORE_DISCUSSION|BLOCKED_ON:description>

---RESPONSE END---
```

#### Field Definitions

| Field | Required | Purpose | Parsed By |
|---|---|---|---|
| `STANCE` | Always | Enables convergence tracking. Orchestrator counts agreement rates to detect premature consensus | Phase gate evaluator |
| `CONFIDENCE` | Always | Numeric signal for decision logging. Low confidence flags unresolved tensions | Decision logger, Morning Brief |
| `MESSAGE` | Always | The actual content. This is what goes into conversation history and cross-team messages | History builder, MCP broker |
| `IDEAS` | Conditional | Only in brainstorm/refine phases. Structured for idea tracking and dedup | Idea tracker, novelty scorer |
| `TENSIONS` | Conditional | Only when disagreeing. Forces agents to articulate WHY, not just "I disagree" | Anti-slop enforcer, decision logger |
| `SIGNAL` | Always | Agent's assessment of whether the phase is done. Orchestrator aggregates these to trigger transitions | Phase gate evaluator |

#### Why This Format and Not JSON

Three reasons:

1. **LLMs are more reliable with labeled plaintext than with JSON.** Bracket matching fails, escaping breaks, nested structures hallucinate. Flat labeled sections with clear delimiters are the most robust format for extraction.

2. **The MESSAGE field is free-form markdown.** Forcing it into a JSON string means escaping hell. Better to let it breathe.

3. **Graceful degradation.** If the agent drifts and drops a field, the parser can still extract what's there. JSON with a missing brace is unparseable. Labeled sections with a missing section are partially parseable.

**Failure mode**: The agent will eventually forget the format, especially 40+ turns in. Mitigation: the perspective reminder (injected every turn) includes a one-liner: `"Format: STANCE / CONFIDENCE / MESSAGE / IDEAS (if any) / TENSIONS (if any) / SIGNAL"`. The full format spec is in the system prompt; the reminder just nudges.

---

### Phase 3: How the Orchestrator Parses the Output

```python
import re
from dataclasses import dataclass
from typing import Optional

@dataclass
class AgentResponse:
    raw: str                          # Full unparsed output
    stance: str                       # AGREE|DISAGREE|PARTIAL|NEW_DIRECTION|BUILD_ON
    confidence: int                   # 0-100
    message: str                      # The substantive content
    ideas: list[dict[str, str]]       # [{"label": "...", "description": "..."}]
    tensions: list[str]               # Free-form tension descriptions
    signal: str                       # READY_TO_ADVANCE|NEEDS_MORE_DISCUSSION|BLOCKED_ON:...
    parse_errors: list[str]           # What fields failed to parse
    agent_name: str                   # Injected by orchestrator, not from output
    turn_number: int                  # Injected by orchestrator

def parse_agent_response(raw: str, agent_name: str, turn: int) -> AgentResponse:
    errors = []

    # Extract between delimiters, fall back to full text
    match = re.search(
        r'---RESPONSE START---\s*(.*?)\s*---RESPONSE END---',
        raw, re.DOTALL
    )
    body = match.group(1) if match else raw
    if not match:
        errors.append("missing_delimiters")

    # Parse each field with fallbacks
    stance = _extract_field(body, "STANCE", errors)
    confidence = _extract_int(body, "CONFIDENCE", errors)
    message = _extract_block(body, "MESSAGE", errors)
    ideas = _extract_ideas(body, errors)
    tensions = _extract_list(body, "TENSIONS", errors)
    signal = _extract_field(body, "SIGNAL", errors)

    # Fallback: if MESSAGE is empty but there's substantial text,
    # treat the whole body as the message
    if not message and len(body) > 100:
        message = body
        errors.append("message_extracted_from_body_fallback")

    # Fallback: if STANCE is missing, infer from language
    if not stance:
        stance = _infer_stance(message)
        errors.append("stance_inferred")

    return AgentResponse(
        raw=raw,
        stance=stance or "UNKNOWN",
        confidence=confidence if confidence is not None else 50,
        message=message or raw,
        ideas=ideas,
        tensions=tensions,
        signal=signal or "NEEDS_MORE_DISCUSSION",
        parse_errors=errors,
        agent_name=agent_name,
        turn_number=turn,
    )
```

Key principle: **never fail to produce a response object.** Every field has a fallback. The `parse_errors` list tells the orchestrator what degraded, and that gets logged to the session for debugging. But the conversation never stops because of a parse failure.

#### What Happens to the Parsed Output

```
AgentResponse
    │
    ├──→ message → Conversation history (what other agents see)
    ├──→ message → MCP broker (if publishing to other team)
    ├──→ stance + confidence → Phase gate evaluator
    │     └──→ "Are 3+ agents at READY_TO_ADVANCE with confidence > 70?"
    ├──→ ideas → Idea tracker
    │     └──→ Dedup, novelty scoring, magnitude estimation
    ├──→ tensions → Decision logger
    │     └──→ Unresolved tensions surface in Morning Brief
    ├──→ signal → Turn sequencer
    │     └──→ Influences who speaks next
    └──→ parse_errors → Session diagnostic log
          └──→ If error rate > threshold, inject format reminder
```

---

### Phase 4: Failure Modes and Mitigations

Because you asked me to think like myself.

| Failure Mode | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Agent drops format entirely after 30+ turns | High | Parser falls back to treating raw text as MESSAGE, loses structured fields | Per-turn format reminder in perspective block. If `parse_errors` accumulate, inject explicit "Please use the output format" nudge |
| Agent embeds format markers inside MESSAGE content (meta-discussion about the format) | Medium | Parser extracts wrong boundaries | Use uncommon delimiters. `---RESPONSE START---` is distinctive enough. Could add a nonce per turn if needed |
| Agent gives CONFIDENCE: 95 on everything | High | Confidence signal becomes meaningless | Track per-agent confidence distribution. If stddev < 5 over 10 turns, inject: "Your confidence has been uniformly high. Differentiate." |
| Agent always signals READY_TO_ADVANCE | Medium | Phase transitions too early | Require minimum turn count per phase AND minimum idea count. Signal is necessary but not sufficient |
| STANCE is always AGREE despite anti-slop rules | Medium | Consensus collapse | Orchestrator tracks agreement rate per agent. If agent agrees > 70% of turns, trigger devils_advocate_duty override |
| MESSAGE is 2000+ tokens, bloating context | Medium | Context window exhaustion at hour 6 | Enforce max token guidance in system prompt. If response exceeds limit, truncate in history but preserve full version in session log |

---

### The Complete Turn Sequence

```
1. Orchestrator selects agent (turn sequencer)
2. Orchestrator builds user message:
   a. Phase context block
   b. Truncated conversation history (with phase summaries)
   c. Cross-team messages (if any new ones from MCP)
   d. Current prompt/question
   e. Perspective reminder
   f. Conditional nudges (uncomfortable idea quota, format reminder)
3. Orchestrator calls claude CLI:
   - System prompt: sections 1-8 (set at conversation start, static)
   - User message: the assembled payload
   - Timeout: 120s default, 360s for specify/review phases
4. Raw response received
5. Parser extracts AgentResponse
6. Orchestrator routes fields:
   - message → conversation history
   - ideas → idea tracker
   - stance + confidence → phase gate
   - tensions → decision log
   - signal → turn sequencer
   - parse_errors → diagnostic log
7. Orchestrator evaluates:
   - Should this message go to MCP for the other team? (deliberation budget check)
   - Has the phase gate been satisfied? (transition check)
   - Who speaks next? (turn sequencer)
8. Loop to step 1
```

---

### What This Means for Implementation

The existing code is about 70% of the way there. What's missing:

1. **Section 8 of the system prompt** -- the output format contract. Add to `prompt_builder.py`.
2. **The parser** -- `AgentResponse` dataclass and `parse_agent_response()`. New module, maybe `response_parser.py`.
3. **Phase context injection** -- the user message builder in `conversation.py` needs a phase context block. Currently it has history + reminder + message but no phase awareness.
4. **Cross-team message injection** -- the user message builder needs a slot for MCP-received messages.
5. **Parse error tracking and format re-injection** -- feedback loop when agents drift from format.

The system prompt and personality infrastructure is solid. The gap is the structured output contract and the machinery to enforce it over 200+ turns.


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


---

## The Product Oracle (user advocate and product strategist)

Good question. This is the heartbeat of the whole system -- get turn selection wrong and you either get a boring round-robin or one agent drowning everyone out. Let me lay out a concrete algorithm.

---

## Turn Selection Algorithm: Relevance-Weighted Bidding

### Core Concept

Agents don't just wait to be called. They **bid** for the turn based on relevance, and the orchestrator selects from the bids. This is neither pure round-robin nor pure random -- it's a lightweight auction.

### The Bid Cycle (every turn)

```
1. Orchestrator broadcasts the current message + topic summary to all ACTIVE agents
2. Each active agent returns a BID (not a full response):
   - relevance_score: 0.0 - 1.0 (how much they have to contribute)
   - bid_reason: one sentence ("I have architectural concerns about this approach")
   - estimated_length: short | medium | long
3. Orchestrator selects speaker using weighted selection
4. Selected agent produces their full response
```

### Selection Formula

```python
def select_speaker(bids, history, turn_number):
    scores = {}
    for agent_id, bid in bids.items():
        # Base: agent's self-assessed relevance
        score = bid.relevance_score
        
        # Recency penalty: reduce score based on how recently they spoke
        turns_since_last = turn_number - last_spoke[agent_id]
        if turns_since_last == 1:
            score *= 0.3   # heavy penalty for back-to-back
        elif turns_since_last == 2:
            score *= 0.6
        elif turns_since_last == 3:
            score *= 0.85
        # no penalty after 4+ turns of silence
        
        # Dominance cap: reduce score if agent has spoken > fair share
        fair_share = total_turns / len(active_agents)
        if speak_count[agent_id] > fair_share * 1.3:
            score *= 0.5   # hard throttle at 130% of fair share
        
        # Silence bonus: boost agents who haven't spoken in a while
        if turns_since_last >= 5:
            score += 0.2   # guarantee quiet agents get heard
        
        scores[agent_id] = score
    
    # Select: top scorer wins, but add small random noise to break ties
    # and prevent perfectly predictable patterns
    for agent_id in scores:
        scores[agent_id] += random.uniform(0, 0.05)
    
    return max(scores, key=scores.get)
```

### Anti-Monopolization Guarantees

| Mechanism | Rule |
|---|---|
| **Recency penalty** | Speaking last turn costs you 70% of your bid score |
| **Dominance cap** | Once you exceed 130% of fair share of turns, hard 50% penalty |
| **Silence bonus** | After 5 turns quiet, +0.2 added to score regardless of bid |
| **Mandatory rotation** | If any active agent hasn't spoken in `len(active_agents) + 2` turns, they get forced next turn regardless of bids |

This means a 4-agent team guarantees every agent speaks at least once every 6 turns, even if their bids are low.

---

## Bench System

### Definitions

- **Active**: Agent participates in bid cycles and can be selected to speak
- **Benched**: Agent is dormant -- receives no messages, produces no bids, costs zero tokens

### Team Composition (4-6 agents)

Typical split: **3 active, 1-3 benched**. The deliberation budget controls how many total turns happen, so keeping 3 active is the sweet spot for productive discussion without noise.

### Activation Triggers (Bench to Active)

```yaml
activation_triggers:
  # 1. Phase transition -- different phases need different expertise
  phase_change:
    brainstorm: [ideator, critic, domain_expert]
    refine: [architect, domain_expert, critic]  
    specify: [architect, writer, domain_expert]
    review: [critic, qa_specialist, writer]
  
  # 2. Topic match -- orchestrator detects keywords/themes
  topic_match:
    # If conversation mentions these patterns, activate the agent
    architect: ["scalability", "infrastructure", "system design", "integration"]
    qa_specialist: ["edge case", "failure mode", "testing", "validation"]
    domain_expert: ["market", "competitor", "user research", "regulation"]
  
  # 3. Explicit request -- an active agent names a benched agent
  agent_request:
    # Active agent says "we need the architect's perspective on this"
    # Orchestrator parses this and activates the named agent
    enabled: true
    requires_confirmation: false  # auto-activate, don't ask
  
  # 4. Stagnation detection
  stagnation:
    # If active agents have been agreeing for N turns with no new ideas
    agreement_threshold: 3  # 3 consecutive turns of agreement
    action: activate_highest_contrast_agent  # bring in most different perspective
```

### Deactivation Triggers (Active to Bench)

```yaml
deactivation_triggers:
  # 1. Low relevance streak
  low_bids:
    threshold: 0.2          # bid below this
    consecutive_turns: 3     # for this many turns in a row
    action: bench            # move to bench
  
  # 2. Phase transition (inverse of activation)
  phase_change: true         # recalculate active roster on phase change
  
  # 3. Active roster too large
  max_active: 4              # if activation would exceed this, bench lowest-bidding current agent
  
  # 4. Agent self-bench
  # Agent can bid with relevance_score: 0.0 and flag "bench_self: true"
  # Useful when agent recognizes the conversation has moved past their expertise
  self_bench: true
```

### Activation/Deactivation Flow

```
Phase changes -> Orchestrator consults phase_change roster -> swap agents
                                    |
During conversation -> Every N turns, orchestrator checks:
                       - Any benched agent's topic_match firing?
                       - Any active agent requesting a benched agent?
                       - Stagnation detected?
                       - Any active agent bidding < 0.2 for 3 straight turns?
                                    |
                       If activation needed + roster full -> 
                         bench lowest-performing active agent first,
                         then activate the new one
```

---

## Devil's Advocate Rotation

### "Every 5 turns" means 5 individual speaker turns, not 5 full rounds

Rationale: In a 4-agent active team, a "round" is fuzzy since it's not round-robin. Counting individual turns is unambiguous and implementable.

```python
class DevilsAdvocateTracker:
    def __init__(self, rotation_interval=5):
        self.interval = rotation_interval
        self.current_da = None
        self.turn_counter = 0
        self.da_queue = []  # agents who haven't been DA yet this cycle
    
    def on_turn(self, active_agents):
        self.turn_counter += 1
        
        if self.turn_counter % self.interval == 0:
            self.rotate(active_agents)
    
    def rotate(self, active_agents):
        # Refill queue if empty (everyone has had a turn)
        if not self.da_queue:
            self.da_queue = list(active_agents)
            random.shuffle(self.da_queue)
        
        # Remove current DA from duty
        self.current_da = self.da_queue.pop(0)
        # current_da now gets the DA system prompt injection for next 5 turns
    
    def get_system_prompt_modifier(self, agent_id):
        if agent_id == self.current_da:
            return DA_PROMPT_INJECTION  # "Challenge assumptions, find flaws..."
        return None
```

### What DA duty actually means in practice

The assigned DA agent doesn't speak every turn. They participate in the normal bid cycle. But their system prompt gets an injection that says:

> "For this rotation, you are the designated Devil's Advocate. When you speak, your primary job is to stress-test ideas, challenge assumptions, and surface risks. You should bid higher (0.7+) when you see unchallenged consensus forming."

This means:
- DA bids higher when the team is agreeing too easily
- DA still participates normally otherwise
- The bid inflation from DA role naturally gets them speaking when it matters most (during consensus)
- The 130% dominance cap still applies -- DA can't monopolize even with inflated bids

---

## Full Turn Lifecycle (Implementation View)

```
TURN N:
  1. Orchestrator receives latest cross-team message (or last internal response)
  2. Check: phase transition needed? -> If yes, swap roster per phase config
  3. Check: DA rotation needed? (N % 5 == 0) -> If yes, rotate
  4. Check: bench activation triggers firing? -> If yes, swap agents
  5. Broadcast message + context to all active agents
  6. Collect bids from active agents (parallel, small prompt, fast)
  7. Score bids with select_speaker() algorithm
  8. Inject DA modifier if selected agent is current DA
  9. Selected agent produces full response
  10. Log turn: who spoke, bid scores, bench state
  11. Check: deactivation triggers for non-speaking agents
  12. Decrement deliberation budget
  13. If budget > 0, go to TURN N+1
  14. If budget == 0, synthesize team response for cross-team message
```

---

## Key Design Decisions Summary

| Decision | Choice | Why |
|---|---|---|
| Selection method | Relevance-weighted bidding | Balances expertise with fairness -- agents self-assess but get checked |
| Bid cost | Cheap (one sentence + score) | Bids happen every turn; must be fast and low-token |
| Bench default | 3 active, rest benched | Sweet spot for depth without noise |
| Activation primary trigger | Phase transitions | Predictable, deterministic, easiest to configure |
| Activation secondary trigger | Topic detection + agent request | Handles emergent needs within a phase |
| DA rotation unit | 5 individual turns | Unambiguous, easy to count |
| DA enforcement | Prompt injection, not forced speaking | DA speaks when it matters, not on a schedule |
| Anti-monopoly | Layered (recency + cap + silence bonus + mandatory rotation) | No single mechanism is enough; layers catch edge cases |

This gives you enough to implement the `turn_manager.py` module in the orchestrator. The bid collection step is the only part that costs extra API calls -- but bids are tiny prompts (50 tokens out, maybe 20 tokens back), so the overhead is minimal compared to full deliberation turns.


---

## The Systems Pragmatist (infrastructure realist)

Good question. Most of these "multi-agent" designs hand-wave the turn mechanics and then wonder why one agent bulldozes everyone else or why the conversation degenerates into polite agreement. Let me break down what actually works and where each approach fails.

---

## Turn-Selection Algorithm

**Orchestrator picks. Agents don't volunteer.** Volunteering means you run every agent through an evaluation pass each turn just to decide who talks -- that's N API calls to save one. Wasteful, and it creates a bias toward verbose agents who always think they have something to say.

### Scoring Function

Each turn, the orchestrator computes a score for every **active** agent and picks the highest:

```
score(agent) = (relevance * W_relevance)
             + (turns_silent * W_recency)
             + (role_phase_fit * W_phase)
             - (consecutive_penalty * W_monopoly)
```

| Factor | How It's Computed | Weight |
|---|---|---|
| `relevance` | Keyword overlap between agent's declared `domains[]` in YAML and last 2 messages. No LLM call -- just TF-IDF or even substring matching against a domain keyword list. Cheap and deterministic. | 0.4 |
| `turns_silent` | Integer count of turns since this agent last spoke. Normalized to 0-1 range across active agents. | 0.3 |
| `role_phase_fit` | Binary or weighted match: does this agent's role align with the current phase? Architect scores high in `specify`, PM scores high in `refine`. Defined in `phases.yaml`. | 0.2 |
| `consecutive_penalty` | If agent spoke on the immediately preceding turn: 1.0. Two turns ago: 0.3. Otherwise: 0.0. | 0.1 |

**Tiebreaker:** Random. Don't overthink it.

### Hard Guardrails (non-negotiable)

These override the scoring function:

1. **No back-to-back turns.** An agent cannot speak two consecutive turns. Period. The scoring penalty is soft; this rule is hard.
2. **Mandatory floor.** If any active agent hasn't spoken in `ceil(active_count * 1.5)` turns, they get forced in next. This prevents the quiet-agent-death-spiral where an agent falls behind the conversation and becomes permanently irrelevant.
3. **Cap per round.** No agent speaks more than `ceil(total_turns_in_round / active_count) + 1` times in a single round. Prevents a "relevant" agent from eating 60% of the airtime.

### Why Not Round-Robin

Round-robin guarantees fairness but kills conversation quality. If the team is debating API design and the UX agent has nothing useful to add, forcing their turn produces filler. Filler degrades context for everyone downstream. The scoring function with a mandatory floor gets you fairness without the dead-air problem.

### Why Not LLM-Based Selection

You'd need a meta-call: "Given this conversation state, who should speak next?" That's an extra API call per turn, it's slow, it's unpredictable, and it creates a recursion problem -- the selector LLM needs the same context the agents need. The keyword-matching heuristic is 95% as good and costs zero tokens.

---

## Bench System

### Concrete State Model

Every agent is in exactly one state:

```
ACTIVE  -- in the conversation, eligible for turn selection
BENCHED -- loaded in config, not currently participating
EJECTED -- removed mid-session (optional, for future use)
```

### Activation Rules (Bench to Active)

An agent gets pulled off the bench when **any** of these fire:

| Trigger | Mechanism | Example |
|---|---|---|
| **Phase transition** | Each phase in `phases.yaml` declares `required_roles: []` and `optional_roles: []`. On phase change, activate anyone in `required_roles` who's benched. | Phase moves to `specify` -- Architect activates. |
| **Topic drift detection** | Every N turns (suggest 3), the orchestrator extracts top-3 keywords from recent messages and checks against benched agents' `domains[]`. If overlap score > threshold, activate. | Discussion shifts to "security concerns" -- the QA agent's domain matches, they activate. |
| **Explicit request** | An active agent's response contains a structured tag like `[REQUEST_AGENT: qa]` or mentions needing a specific expertise. Orchestrator pattern-matches this. | PM says "we need QA perspective on this edge case." |

**Activation cap:** Maximum 2 agents can activate in a single turn. If 3 triggers fire simultaneously, prioritize by `role_phase_fit`, defer the third.

### Deactivation Rules (Active to Bench)

| Trigger | Mechanism | Cooldown |
|---|---|---|
| **Irrelevance timeout** | Agent hasn't been selected by the scoring function for `active_count * 3` turns (meaning the algorithm keeps choosing others). Orchestrator benches them. | Can't reactivate for 5 turns. |
| **Phase exit** | Phase transitions out and agent isn't in the new phase's required or optional roles. | Immediate, no cooldown. |
| **Explicit release** | Agent's own output includes `[YIELD_TURN]` or equivalent signal indicating they have nothing further to add. | Can't reactivate for 3 turns. |

**Never bench below 2 active agents.** If deactivation would drop you to 1, skip it. Two-agent conversations degenerate into ping-pong agreement.

### Initial State

Phase 1 (`brainstorm`) config declares which roles start active. Everyone else starts benched. Typical:
- **Active:** PM, Analyst, one domain expert
- **Benched:** Architect, QA, Tech Writer

---

## Devil's Advocate Rotation

**5 individual agent turns, not 5 rounds.**

Rounds are variable-length because of the bench system -- a "round" with 3 active agents is different from one with 5. Counting individual turns keeps the rotation predictable.

```python
da_counter = 0  # global, increments every agent turn
da_agent = None  # currently assigned DA

def on_turn_complete(agent):
    global da_counter, da_agent
    da_counter += 1
    if da_counter % 5 == 0:
        # Rotate to next active agent (skip current DA)
        da_agent = next_active_agent_after(da_agent)
```

**What DA duty actually means in the prompt:**

The DA agent gets an additional system instruction prepended to their next turn:

> "For this turn, adopt a critical stance. Identify the weakest assumption in the current direction and articulate a concrete alternative. Do not simply agree."

It's a prompt modifier, not a persona change. The agent keeps their domain expertise but is instructed to push back. This is important -- you don't want the Architect playing devil's advocate about UX concerns they don't understand. You want the Architect challenging the *architectural* assumptions.

**What if the DA agent gets benched mid-duty?** Transfer DA to the next active agent immediately. Don't leave it orphaned.

---

## Failure Modes I'd Watch For

| Failure | Cause | Mitigation |
|---|---|---|
| **Echo chamber** | All agents converge on the same position, DA rotation isn't enough | Track "agreement density" -- if 3+ consecutive turns contain no disagreement/alternative, force-activate a benched agent or inject a stronger DA prompt |
| **Thrashing** | Agents activate/deactivate rapidly as topic bounces | The reactivation cooldown (3-5 turns) prevents this. If it still happens, increase the cooldown. |
| **Context bloat** | Too many agents active, each adding marginal value, burning the context window | Hard cap of 4 active agents. If a 5th would activate, bench the lowest-scoring current active agent first. |
| **Keyword gaming** | Topic detection is too aggressive, pulling in irrelevant agents | Require overlap on 2+ domain keywords, not just 1. Tune the threshold empirically on session transcripts. |
| **Silent spiral** | Mandatory floor forces agent to speak, but they produce low-quality filler that wastes everyone's context | When floor-forcing an agent, give them a specific prompt: "Summarize your perspective on [extracted topic] or signal you have nothing to add with [YIELD_TURN]." Let them exit gracefully. |

---

## Data Structures for Implementation

```python
@dataclass
class AgentState:
    id: str
    role: str
    domains: list[str]          # from YAML config
    status: Literal["active", "benched", "ejected"]
    turns_since_spoke: int      # increments each global turn
    consecutive_turns: int      # resets when another agent speaks
    total_turns_this_round: int
    is_devil_advocate: bool
    bench_cooldown: int         # turns remaining before can reactivate
    
class TurnSelector:
    def select_next(self, agents: list[AgentState], 
                    recent_messages: list[str],
                    current_phase: Phase) -> AgentState:
        # 1. Filter to active agents only
        # 2. Exclude agent who just spoke (hard rule)
        # 3. Check mandatory floor -- if anyone is overdue, return them
        # 4. Score remaining candidates
        # 5. Return highest score (random tiebreak)
        ...
    
    def check_bench_activations(self, agents: list[AgentState],
                                 recent_messages: list[str],
                                 current_phase: Phase) -> list[AgentState]:
        # Returns up to 2 agents to activate
        ...
    
    def check_bench_deactivations(self, agents: list[AgentState],
                                   current_phase: Phase) -> list[AgentState]:
        # Returns agents to bench (respecting minimum-2 rule)
        ...
```

---

The weights (0.4, 0.3, 0.2, 0.1) and thresholds (1.5x, 3x) are starting points. Tune them against actual session transcripts. Log the scores each turn so you can see *why* the orchestrator made each selection -- without that audit trail, debugging conversation quality problems becomes guesswork.


---

# Question 4: How do messages actually flow between the two teams through the MCP server?

## The Cognitive Architect (creativity engine designer)

Good. All three agents timed out on Question 4 -- the cross-team message flow is a complete blank slate. And the existing code is single-team only. Here's the full design.

---

## Cross-Team Message Flow: End-to-End Design

### The Core Problem

Two Claude processes run in separate context windows. They must not share context directly -- that defeats the purpose of having two teams with different perspectives. The MCP server is the membrane. Every question you asked exposes a design decision at a different point in the pipeline. Let me trace the full path.

---

### 1. How Does the Orchestrator Decide "Cross-Team" vs "Internal"?

It doesn't decide by inspecting content. **The channel determines the boundary.**

The orchestrator runs two loops -- one per team. Each loop manages internal deliberation (agents talking to each other within a team) and cross-team messaging (the team's consensus response to the other team). The distinction is structural, not semantic:

```
INTERNAL: Agent A1 responds to Agent A2 within Team A's deliberation.
          Never leaves the team. Never touches the MCP server's cross-team channels.
          Stored in: sessions/{id}/internal/team-a/

CROSS-TEAM: Team A produces a consolidated response after N deliberation turns.
            The orchestrator posts it to the MCP server's cross-team channel.
            Team B will receive it.
```

The deliberation budget controls this. If Team A has a budget of 3 internal turns per cross-team exchange, the flow is:

```
[Team A deliberates: Agent A1 → A2 → A3]  ← internal, 3 turns
[Orchestrator synthesizes or selects final position]  ← cross-team message produced
[Post to MCP server]  ← crosses the boundary
```

**Who writes the cross-team message?** Two options, and the choice matters:

- **Option A: Last speaker.** The final agent in the deliberation round writes the outgoing message. Simple, but the message inherits one agent's voice and may not represent the team.
- **Option B: Synthesis turn.** After deliberation, the orchestrator runs one more `claude -p` call with a *synthesizer* prompt: "Given this internal discussion, write the team's response to the other team. Capture points of agreement, flag unresolved disagreements, and state the team's position." This costs one extra API call per exchange but produces a coherent team voice.

**Recommendation: Option B.** The synthesis turn is the cross-team message. Internal deliberation stays internal. The membrane is clean.

The synthesizer prompt template:

```python
CROSS_TEAM_SYNTHESIZER = """You are the voice of {team_name}.

Your team just had this internal discussion:
{deliberation_transcript}

The other team's last message was:
{incoming_message}

Write a response FROM your team TO the other team. Rules:
- Represent the team's position, not any single agent's view
- If your team disagreed internally, say so: "We debated X -- our lead position is Y but [agent] raised Z"
- Be specific. Name constraints, risks, proposals with enough detail to act on
- Do NOT repeat the other team's points back to them
- Keep it under 800 words
"""
```

---

### 2. The MCP Server Message Format

The MCP server stores messages as structured objects, not raw text. Each message carries metadata the orchestrator needs for routing, batching, and phase enforcement.

```typescript
interface CrossTeamMessage {
  id: string;                    // uuid
  channel: Channel;              // "brainstorm" | "refine" | "specify" | "review"
  from_team: string;             // "team-a" | "team-b"
  to_team: string;               // "team-b" | "team-a"
  phase: Phase;                  // current session phase
  sequence: number;              // monotonic counter per channel
  timestamp: string;             // ISO 8601
  
  content: string;               // the synthesized team message
  
  // Structured metadata extracted by orchestrator before posting
  meta: {
    ideas_referenced: string[];  // idea IDs mentioned
    decisions_proposed: string[];// any formal decision proposals
    questions_asked: string[];   // explicit questions for the other team
    stance: "proposing" | "challenging" | "building" | "requesting";
  };
  
  // Delivery tracking
  delivered: boolean;            // has the receiving team seen this?
  delivered_at?: string;
  delivery_mode: "full" | "summary" | "batched";
}
```

**Channels are not just labels -- they carry permissions:**

```typescript
interface Channel {
  name: string;
  phase_permissions: {
    [phase: string]: {
      read: boolean;
      write: boolean;
    }
  };
}

// Example:
const CHANNELS: Channel[] = [
  {
    name: "brainstorm",
    phase_permissions: {
      brainstorm: { read: true, write: true },
      refine:     { read: true, write: false },  // read-only reference
      specify:    { read: false, write: false },
      review:     { read: false, write: false },
    }
  },
  {
    name: "refine",
    phase_permissions: {
      brainstorm: { read: false, write: false },
      refine:     { read: true, write: true },
      specify:    { read: true, write: false },
      review:     { read: true, write: false },
    }
  },
  // ... decisions, specs channels similarly gated
];
```

---

### 3. The MCP Tool Interface

Each team's Claude process doesn't call MCP tools directly. The *orchestrator* calls MCP tools on behalf of the team. The agents never know the MCP server exists. This is critical -- it keeps the agent prompts clean and prevents agents from gaming the messaging system.

But the MCP server still needs a tool interface for the orchestrator to call:

```typescript
// Tools the orchestrator calls on the MCP server

// Send a cross-team message
tool send_message {
  input: {
    channel: string,
    from_team: string,
    content: string,
    meta: MessageMeta
  }
  output: {
    message_id: string,
    sequence: number
  }
}

// Receive pending messages for a team
tool receive_messages {
  input: {
    team: string,
    channel?: string,       // optional filter
    since_sequence?: number, // only messages after this sequence number
    max_count?: number       // limit for batching control
  }
  output: {
    messages: CrossTeamMessage[],
    has_more: boolean,
    latest_sequence: number
  }
}

// Mark messages as delivered
tool ack_messages {
  input: {
    message_ids: string[]
  }
  output: {
    acknowledged: number
  }
}

// Get channel state (for phase transition checks)
tool channel_state {
  input: {
    channel: string
  }
  output: {
    message_count: number,
    undelivered_count: { [team: string]: number },
    last_activity: string,
    phase: Phase
  }
}

// Post a phase transition
tool transition_phase {
  input: {
    new_phase: Phase,
    reason: string,
    briefing: string  // summary of what happened in the previous phase
  }
  output: {
    previous_phase: Phase,
    new_phase: Phase,
    channels_changed: string[]
  }
}
```

---

### 4. How Does Team B Receive the Message?

This is where it gets interesting. When Team B's orchestrator loop starts a new cross-team turn, it:

1. Calls `receive_messages({ team: "team-b" })` on the MCP server
2. Gets back 0-N pending messages
3. Decides how to present them to Team B's agents

**The message is NOT injected into conversation history.** It goes into a dedicated `[INCOMING FROM OTHER TEAM]` block in the user message payload. This is a deliberate design choice:

```python
def build_cross_team_payload(self, agent_key: str, incoming_messages: list[CrossTeamMessage]) -> str:
    parts = []
    
    # 1. Team's own internal history (truncated)
    parts.append(self._build_internal_history())
    
    # 2. Incoming cross-team messages -- clearly demarcated
    if incoming_messages:
        parts.append("=== MESSAGE FROM THE OTHER TEAM ===")
        for msg in incoming_messages:
            parts.append(f"[{msg.from_team} | {msg.channel} | #{msg.sequence}]")
            parts.append(msg.content)  # or msg.summary if batched
            if msg.meta.questions_asked:
                parts.append(f"\nThey asked: {'; '.join(msg.meta.questions_asked)}")
        parts.append("=== END OTHER TEAM MESSAGE ===\n")
    
    # 3. Perspective reminder
    parts.append(build_perspective_reminder(self.agents[agent_key]))
    
    # 4. Phase-specific instruction
    parts.append(self._phase_instruction())
    
    # 5. Turn prompt
    parts.append(f"\nRespond to the other team's message. Stay in character as {agent_key}.")
    
    return "\n".join(parts)
```

**Why a separate block instead of history?** Three reasons:
- **Clarity of origin.** The agent knows this came from *outside* the team. It's not a teammate -- it's an adversary/collaborator with different context.
- **Prevents context contamination.** If cross-team messages were interleaved with internal history, the agent might start adopting the other team's framing without realizing it.
- **Enables batching.** When multiple messages pile up, they can be presented as a coherent block rather than scattered through fake history entries.

---

### 5. Full Message vs Summary -- Who Decides?

**The orchestrator decides, based on volume and recency.**

Three delivery modes:

| Pending Messages | Mode | What Team B Sees |
|---|---|---|
| 1 message | `full` | Complete message content |
| 2-3 messages | `full` with headers | All messages, chronologically, with sequence numbers |
| 4+ messages | `batched` | Summary of older messages + full text of most recent 2 |

**Who writes the summary?** A cheap Haiku call, not the orchestrator itself:

```python
BATCH_SUMMARY_PROMPT = """Summarize the following {count} messages from {from_team} into a concise brief.
Preserve: all concrete proposals, decisions, questions, and disagreements.
Drop: pleasantries, repetition, hedging language.
Format: bullet points, max 300 words.

Messages:
{messages}
"""
```

The summary is attached as `delivery_mode: "batched"` and the original full messages are still stored in the MCP server -- they're just not shown to the receiving team. The session transcript gets the full versions.

**Why not always full?** Context budget. Each `claude -p` call has finite context. Cross-team messages compete with internal history, system prompt, perspective reminders, and phase instructions. Five full messages at 800 words each is 4,000 words of cross-team content alone -- that crowds out the team's own deliberation history.

---

### 6. What Happens When 5 Messages Pile Up?

This happens when Team A is fast and Team B is slow (more internal deliberation turns, or longer agent responses). The MCP server accumulates undelivered messages. On Team B's next receive:

```
Messages pending: [#12, #13, #14, #15, #16]

Orchestrator decision:
  - #12, #13, #14 → summarize into batch brief (Haiku call)
  - #15, #16 → deliver full (most recent context)
  
Team B sees:
  === MESSAGE FROM THE OTHER TEAM ===
  [Summary of messages #12-#14]:
  - Team A proposed a tiered pricing model with 3 levels
  - They challenged our assumption about user onboarding complexity
  - Unresolved: whether to target freelancers or agencies first
  - They asked: "What's your evidence that agencies will adopt this?"
  
  [team-a | brainstorm | #15]:
  {full message content}
  
  [team-a | brainstorm | #16]:
  {full message content}
  === END OTHER TEAM MESSAGE ===
```

**Prioritization within the batch:** Messages with `questions_asked` in their metadata get preserved in full regardless of batching. Unanswered questions are conversation-killers -- if they get lost in a summary, the dialogue degrades.

---

### 7. The Complete Flow Diagram

```
TEAM A ORCHESTRATOR                    MCP SERVER                    TEAM B ORCHESTRATOR
                                                                     
1. Internal deliberation               |                             |
   A1 → A2 → A3 (3 turns)             |                             |
                                        |                             |
2. Synthesis turn                      |                             |
   → produces cross-team msg           |                             |
                                        |                             |
3. Extract metadata                    |                             |
   (ideas, decisions, questions)       |                             |
                                        |                             |
4. ──send_message(channel, content)──> |                             |
                                        | Store message               |
                                        | Assign sequence #           |
                                        | Set delivered=false          |
                                        |                             |
                                        |                             | 5. Team B finishes its
                                        |                             |    internal deliberation
                                        |                             |
                                        | <──receive_messages(team-b)──── 6. Fetch pending
                                        |                             |
                                        | Return messages[]           |
                                        | ──────────────────────────> |
                                        |                             | 7. Count messages
                                        |                             |    1-3: deliver full
                                        |                             |    4+: summarize old + full recent
                                        |                             |
                                        |                             | 8. Build payload with
                                        |                             |    [INCOMING] block
                                        |                             |
                                        |                             | 9. Run deliberation
                                        |                             |    B1 → B2 → B3
                                        |                             |
                                        |                             | 10. Synthesis turn
                                        |                             |     → cross-team response
                                        |                             |
                                        | <──ack_messages(ids)──────── 11. Mark delivered
                                        |                             |
                                        | <──send_message(response)─── 12. Post response
```

---

### 8. Edge Cases That Will Actually Bite You

**Deadlock.** Both teams are waiting for the other's response before their next cross-team turn. Solve: the orchestrator runs both teams on independent loops with a shared clock. Neither team *waits* for a response -- it deliberates on its own, and incoming messages arrive when they arrive. If no messages are pending on `receive_messages`, the team gets a prompt: "No response from the other team yet. Continue developing your position."

**Echo amplification.** Team A sends a strong position. Team B's summary preserves it. Team B reacts to it. Team A sees the reaction. The original position gets amplified through the echo. Solve: the batch summary prompt explicitly instructs "Do not editorialize or strengthen positions. Report what was said, not what it implies."

**Phase mismatch.** Team A transitions to Refine phase. Team B is still in Brainstorm and sends a brainstorm-style message. The MCP server rejects the write because the `brainstorm` channel is now write-locked. Solve: phase transitions are global. `transition_phase` fires for both teams simultaneously. The orchestrator must drain both teams' pending cross-team messages before transitioning.

**The lost question.** Team A asks a direct question in message #12. It gets batched into a summary for Team B. The summary mentions the question but the nuance is lost. Team B never answers it. Solve: questions in `meta.questions_asked` survive batching verbatim. The orchestrator tracks unanswered questions and re-injects them after 2 cross-team exchanges: "[REMINDER: The other team asked and you haven't addressed: '{question}']"

---

### 9. What This Means for Implementation

The existing `MultiConversation` class handles intra-team state. It stays. But the orchestrator needs a new layer:

```python
class TeamOrchestrator:
    """Manages one team's conversation loop + MCP bridge."""
    
    team_id: str
    multi_conv: MultiConversation      # intra-team state
    mcp_client: MCPClient              # connection to MCP server
    deliberation_budget: int           # internal turns per cross-team exchange
    last_received_sequence: int        # cursor for receive_messages
    unanswered_questions: list[str]    # questions the other team asked
    
    async def run_exchange(self):
        """One full cycle: receive → deliberate → synthesize → send."""
        
        # 1. Fetch incoming
        incoming = await self.mcp_client.receive_messages(
            team=self.team_id, 
            since_sequence=self.last_received_sequence
        )
        
        # 2. Prepare incoming block (full, batched, or empty)
        incoming_block = self._prepare_incoming(incoming.messages)
        
        # 3. Run internal deliberation
        for turn in range(self.deliberation_budget):
            agent_key = self._next_speaker()
            payload = self._build_deliberation_payload(agent_key, incoming_block, turn)
            response = await run_claude_async(self._system_prompt(agent_key), payload)
            self.multi_conv.add_agent_message(agent_key, response)
        
        # 4. Synthesis turn
        cross_team_msg = await self._synthesize()
        
        # 5. Extract metadata
        meta = await self._extract_meta(cross_team_msg)
        
        # 6. Send
        result = await self.mcp_client.send_message(
            channel=self.current_phase,
            from_team=self.team_id,
            content=cross_team_msg,
            meta=meta
        )
        
        # 7. Ack received messages
        if incoming.messages:
            await self.mcp_client.ack_messages(
                [m.id for m in incoming.messages]
            )
            self.last_received_sequence = incoming.latest_sequence
        
        # 8. Track unanswered questions
        self._update_question_tracker(incoming.messages, cross_team_msg)
```

The main session loop runs two `TeamOrchestrator` instances concurrently:

```python
async def run_session(session_config):
    mcp = MCPServer()  # or connect to running instance
    
    team_a = TeamOrchestrator("team-a", mcp, team_a_config)
    team_b = TeamOrchestrator("team-b", mcp, team_b_config)
    
    while not session_complete():
        # Both teams run exchanges concurrently
        await asyncio.gather(
            team_a.run_exchange(),
            team_b.run_exchange()
        )
        
        # Check phase transitions
        await maybe_transition_phase(mcp)
        
        # Checkpoint
        await checkpoint_session(team_a, team_b, mcp)
```

---

That's the full path. Message originates in synthesis, crosses through the MCP server as a structured object with metadata, gets delivered full or batched depending on queue depth, enters the receiving team as a demarcated incoming block (not history), and unanswered questions get tracked and re-injected. The agents never know the MCP server exists -- they just see messages from "the other team" and respond in character.

The part that will need the most tuning in practice: the batch summary quality. That Haiku call is the bottleneck between "Team B understands what Team A said" and "Team B responds to a lossy compression of what Team A said." Start with full delivery, add batching only when context overflow forces it.


---

## The Product Oracle (user advocate and product strategist)

Now I have a thorough picture of the codebase. This is design question Q4 -- the one that determines whether these two teams can actually *talk* to each other. Let me design this end-to-end.

---

## Cross-Team Message Flow: End-to-End Design

### The Job To Be Done

A team finishes deliberating and produces something the other team needs to hear. That message must travel reliably from one context window to another, preserving intent without leaking internal process. The user sleeping upstairs doesn't care about plumbing -- they care that when they wake up, the teams had a *real* conversation, not two monologues.

---

### 1. The Boundary Decision: Internal vs. Cross-Team

**Who decides?** The orchestrator, not the agent.

This is the critical design choice. Agents don't know they're calling MCP tools to "send" messages to the other team. The orchestrator controls the conversation loop and knows whether the current turn is an **internal deliberation turn** or a **cross-team response turn**.

```
Orchestrator state per team:
  - deliberation_budget: int        # remaining internal turns before must respond
  - deliberation_count: int         # turns used in current deliberation cycle
  - phase: Phase                    # current discussion phase
  - awaiting_response: bool         # other team is waiting for our reply
```

**The rule is structural, not content-based:**

```python
def should_cross_boundary(team_state: TeamState) -> bool:
    # Team has used up their deliberation budget
    if team_state.deliberation_count >= team_state.deliberation_budget:
        return True
    # Team has been explicitly told to respond (phase transition, timeout)
    if team_state.forced_respond:
        return True
    # Otherwise, keep deliberating internally
    return False
```

**Why not let agents decide?** Because LLMs are terrible at meta-decisions about their own conversation flow. They'll either always want to respond (eager to please) or never consolidate (endless internal refinement). The orchestrator imposes structure. The agent's job is to think well, not to manage turn-taking.

**The deliberation cycle:**
1. Team A receives incoming cross-team message
2. Orchestrator gives Team A `deliberation_budget` internal turns (configured per phase -- brainstorm gets 5, review gets 2)
3. Agents on Team A discuss internally (round-robin, debate, etc.)
4. After budget is exhausted, orchestrator issues a **consolidation prompt**: "Synthesize your team's position into a single response for the other team."
5. The designated **spokesperson agent** (rotates, or configured) produces the cross-team message
6. Orchestrator extracts that message and posts it to the MCP server

---

### 2. Message Format in the MCP Server

The MCP server stores messages as structured objects, not raw text blobs. This is what lives on disk and in the server's state:

```typescript
interface CrossTeamMessage {
  id: string;                    // uuid
  session_id: string;            // links to session
  sequence: number;              // monotonic ordering within session
  
  // Routing
  from_team: string;             // "bmad-team" | "client-team"
  to_team: string;               // "bmad-team" | "client-team"
  channel: MessageChannel;       // "brainstorm" | "research" | "decisions" | "specs"
  
  // Content
  phase: Phase;                  // phase when message was produced
  spokesperson: string;          // agent key who authored the final text
  content: string;               // full message text (markdown)
  summary: string;               // 2-3 sentence digest (written by orchestrator)
  
  // Structured extractions (orchestrator-parsed)
  proposals: string[];           // concrete proposals or ideas
  questions: string[];           // explicit questions for the other team
  decisions: Decision[];         // any decisions logged with confidence
  
  // Metadata
  deliberation_turns: number;    // how many internal turns produced this
  timestamp: string;             // ISO 8601
  read: boolean;                 // has receiving team picked this up?
}

interface Decision {
  statement: string;
  confidence: number;            // 0-1
  dissenters: string[];          // agents who disagreed
  rationale: string;
}
```

**Why both `content` and `summary`?** Context budget. Team B's orchestrator decides what to inject based on how much context window is available. Fresh message with room to spare? Full content. Three messages piled up and we're in a long session? Summaries for the older ones, full text for the latest.

---

### 3. The MCP Tool Interface

Each team's Claude process doesn't call MCP tools directly. Remember: each `claude -p` call is stateless. The **orchestrator** calls MCP tools on behalf of the team. But the MCP server exposes these tools for the orchestrator to use:

```typescript
// === Tools the orchestrator calls on behalf of a team ===

// Post a cross-team message
tool: "post_message"
input: {
  session_id: string,
  from_team: string,
  channel: MessageChannel,
  phase: Phase,
  spokesperson: string,
  content: string,
  summary: string,
  proposals: string[],
  questions: string[],
  decisions: Decision[]
}
returns: { message_id: string, sequence: number }

// Check for unread messages addressed to this team
tool: "check_inbox"  
input: {
  session_id: string,
  team: string,
  since_sequence?: number    // only messages after this sequence number
}
returns: { 
  messages: CrossTeamMessage[],
  unread_count: number 
}

// Mark messages as read
tool: "mark_read"
input: {
  session_id: string,
  team: string,
  through_sequence: number   // mark all messages up to this sequence as read
}
returns: { marked: number }

// Get full message body (when team only received summary)
tool: "get_message"
input: {
  message_id: string
}
returns: CrossTeamMessage

// Get conversation history for context rebuilding
tool: "get_cross_team_history"
input: {
  session_id: string,
  limit?: number,
  phase?: Phase              // optionally filter to current phase
}
returns: { messages: CrossTeamMessage[] }
```

**Why does the orchestrator mediate instead of agents calling tools directly?** Three reasons:
1. Claude CLI calls are stateless -- there's no persistent MCP connection per agent
2. The orchestrator needs to control *when* messages cross the boundary (deliberation budget)
3. The orchestrator writes the summary (see below), which requires seeing the message before posting

---

### 4. How Team B Receives the Message

When it's Team B's turn to start a new deliberation cycle, the orchestrator:

```python
async def prepare_incoming_for_team(session_id: str, team: str) -> str:
    # 1. Check inbox
    inbox = await mcp.check_inbox(session_id, team)
    
    if inbox.unread_count == 0:
        return None  # no new messages
    
    messages = inbox.messages
    
    # 2. Apply batching strategy (see section 5)
    injection = format_incoming_block(messages)
    
    # 3. Mark as read
    max_seq = max(m.sequence for m in messages)
    await mcp.mark_read(session_id, team, through_sequence=max_seq)
    
    return injection
```

**The message gets injected as a structured block at the top of the user message for the first agent in the deliberation cycle:**

```
═══════════════════════════════════════════
INCOMING FROM [BMAD TEAM] (2 messages, brainstorm phase)
═══════════════════════════════════════════

[Message 14] From: Systems Pragmatist (spokesperson)
Received: 2026-03-17T03:42:11Z

They propose a file-per-message storage model where each cross-team 
message is a JSON file on disk, and agents read summaries by default 
with the option to pull full bodies. They're concerned about context 
window management during 8-hour runs.

QUESTIONS FOR YOUR TEAM:
- How do you envision the Morning Brief consuming these stored messages?
- Should phase transitions trigger a full context reset or incremental briefing?

FULL MESSAGE:
[... complete text from the spokesperson ...]

───────────────────────────────────────────

[Message 15] From: Cognitive Architect (spokesperson)  
Received: 2026-03-17T03:58:44Z
[SUMMARY ONLY - full text available on request]

They followed up with a proposal for "context checkpoints" at phase 
boundaries -- a BackgroundAgent (Weaver type) would compress the full 
cross-team history into a briefing document that both teams receive 
when entering a new phase.

═══════════════════════════════════════════
Your team has 4 deliberation turns to discuss before responding.
═══════════════════════════════════════════
```

**It's NOT conversation history.** It's a clearly delimited incoming block that the agent reads as "here's what the other team said." This matters because:
- The agent's conversation history is their *team's* internal discussion
- Cross-team messages are *stimuli*, not part of the internal thread
- The framing ("INCOMING FROM") primes the agent to *react* rather than continue

---

### 5. Batching Strategy When Messages Pile Up

Messages pile up when Team A is fast and Team B has a long deliberation budget. The orchestrator handles this with a **recency-weighted batching** approach:

```python
def format_incoming_block(messages: list[CrossTeamMessage]) -> str:
    if len(messages) == 0:
        return ""
    
    if len(messages) == 1:
        # Single message: show full content
        return format_single_message(messages[0], show_full=True)
    
    if len(messages) <= 3:
        # 2-3 messages: full text for latest, summaries for earlier
        parts = []
        for msg in messages[:-1]:
            parts.append(format_single_message(msg, show_full=False))
        parts.append(format_single_message(messages[-1], show_full=True))
        return "\n\n".join(parts)
    
    if len(messages) > 3:
        # 4+ messages: synthesize older ones, full text for latest 2
        # Orchestrator runs a synthesis prompt to compress older messages
        older = messages[:-2]
        recent = messages[-2:]
        
        synthesis = synthesize_messages(older)  # see below
        
        parts = [format_synthesis(synthesis, count=len(older))]
        for msg in recent:
            parts.append(format_single_message(msg, show_full=True))
        return "\n\n".join(parts)
```

**The synthesis for 4+ piled-up messages** is itself a Claude call:

```python
async def synthesize_messages(messages: list[CrossTeamMessage]) -> str:
    prompt = f"""Compress these {len(messages)} cross-team messages into a 
    single briefing paragraph. Preserve: all concrete proposals, all open 
    questions, all decisions with their confidence levels, and any points 
    of disagreement. Drop: pleasantries, redundant restatements, process 
    commentary.
    
    Messages:
    {format_messages_for_synthesis(messages)}"""
    
    return await run_claude_async(SYNTHESIS_SYSTEM_PROMPT, prompt)
```

**No messages get dropped.** Ever. They get compressed, but the IDs are preserved so any agent can request the full body via the orchestrator if they reference it.

**No prioritization queue.** Messages are ordered by sequence number (chronological). The conversation is linear between teams -- it's not a pub/sub system with topics competing for attention. The `channel` field exists for *filtering during review*, not for delivery priority.

---

### 6. Who Writes the Summary?

**The orchestrator writes it**, not the agent and not the MCP server.

After the spokesperson produces the cross-team message, but before posting to MCP:

```python
async def post_cross_team_message(
    session_id: str,
    team: str, 
    spokesperson: str,
    content: str,
    phase: Phase
) -> str:
    # 1. Generate summary
    summary = await run_claude_async(
        system_prompt="You are a neutral summarizer. Produce a 2-3 sentence "
                      "digest of this message. Preserve all proposals, questions, "
                      "and decisions. No editorializing.",
        user_message=content
    )
    
    # 2. Extract structured fields
    extractions = await run_claude_async(
        system_prompt=EXTRACTION_PROMPT,
        user_message=content
    )
    # Parse extractions into proposals[], questions[], decisions[]
    
    # 3. Post to MCP
    result = await mcp.post_message(
        session_id=session_id,
        from_team=team,
        channel=determine_channel(phase, content),
        phase=phase,
        spokesperson=spokesperson,
        content=content,
        summary=summary,
        proposals=extractions.proposals,
        questions=extractions.questions,
        decisions=extractions.decisions
    )
    
    return result.message_id
```

**Why the orchestrator and not the agent?** Because the agent is the spokesperson -- they're biased. They'll emphasize what *they* think is important, not what's actually useful for the receiving team. A neutral summarizer produces better compression. And the agent shouldn't waste deliberation turns on meta-work.

---

### 7. The Full Path, Traced

```
1. Team A internal deliberation
   ├── Agent 1 speaks (internal turn 1)
   ├── Agent 2 responds (internal turn 2) 
   ├── Agent 3 challenges (internal turn 3)
   ├── ... up to deliberation_budget
   └── Orchestrator A: "Budget exhausted. Time to respond."

2. Consolidation
   ├── Orchestrator A sends consolidation prompt to spokesperson:
   │   "Synthesize your team's position. Address the other team's 
   │    questions. Include your proposals and any unresolved disagreements."
   └── Spokesperson produces cross-team message text

3. Orchestrator A processing
   ├── Generates summary (neutral Claude call)
   ├── Extracts proposals, questions, decisions (structured Claude call)
   └── Calls MCP: post_message(...)

4. MCP Server
   ├── Assigns message ID and sequence number
   ├── Stores to disk: /sessions/{id}/cross-team/{sequence}_{from}.json
   ├── Sets read=false for receiving team
   └── Message is now available

5. Orchestrator B picks up
   ├── Calls MCP: check_inbox(team_b)
   ├── Gets unread messages
   ├── Applies batching strategy (full/summary/synthesize based on count)
   ├── Calls MCP: mark_read(through_sequence=N)
   └── Formats incoming block

6. Team B deliberation begins
   ├── Orchestrator B constructs first agent's prompt:
   │   user_message = INCOMING_BLOCK + "\n\n" + deliberation_instructions
   ├── Agent 1 reads incoming, reacts from their perspective
   ├── Agent 2 builds on Agent 1's reaction
   ├── ... deliberation cycle
   └── Back to step 2 (Team B consolidates, responds to Team A)
```

---

### 8. Edge Cases the Overnight Run Will Hit

**Both teams post simultaneously.** Not a real problem. The MCP server assigns sequence numbers atomically. Each team checks their inbox at the start of their cycle. If both posted, each picks up the other's message. Conversation might temporarily fork -- that's fine, the phase structure will re-converge.

**Spokesperson produces garbage.** The orchestrator's extraction step will return empty proposals/questions. The summary will reflect this. The receiving team gets a weak message and their deliberation will naturally call it out. Self-correcting.

**Context window fills up during long deliberation.** The existing `_truncated_history()` handles internal history. For cross-team history, the orchestrator can call `get_cross_team_history(limit=5)` to include only recent exchanges in the prompt header, with a one-line "previous exchanges covered: [topic list]" for older ones.

**Phase transition mid-exchange.** The orchestrator checks phase exit gates after each cross-team exchange (not after internal turns). If a transition fires, both teams get a phase-transition briefing (generated by a BackgroundAgent) that includes a compressed summary of all cross-team messages from the completed phase.

---

### What This Design Optimizes For

From a jobs-to-be-done lens: the user's job is "wake up to a meaningful conversation between two teams that actually challenged each other." This design serves that by:

- **Preventing information loss** -- nothing dropped, everything compressed with originals retrievable
- **Preventing echo chambers** -- teams never see each other's internal process, only consolidated positions
- **Preventing context bloat** -- summaries by default, full text on demand, synthesis when messages pile up
- **Keeping the orchestrator in control** -- agents think, orchestrators route. Clean separation.

The teams communicate like executives exchanging memos, not like coworkers on Slack. That's the right abstraction for autonomous overnight operation where every token of context window is precious.


---

## The Systems Pragmatist (infrastructure realist)

Alright. I have enough from the codebase exploration, the design questions, and the existing code patterns. Let me give you the failure-mode-first design.

---

## Cross-Team Message Flow: End-to-End Design

### The Core Problem Nobody's Talking About

Before tracing the "happy path," let's name the failure this design has to survive: **asymmetric pacing**. Team A deliberates fast (3 agents, high assertiveness, short turns). Team B deliberates slow (6 agents, lots of internal debate). If you don't handle this, Team A buries Team B in messages it never processes, and by hour 4 Team B is responding to context from hour 1. That's not a conversation. That's two monologues with a queue in the middle.

Every design decision below exists to prevent that.

---

### 1. How the Orchestrator Decides: Internal vs. Cross-Team

There's no magic classification here. The orchestrator doesn't parse agent output to divine intent. Instead, the architecture uses **explicit routing by conversation structure**.

**The rule:** Each team has two conversation loops managed by the orchestrator:

- **Internal deliberation loop** -- agents talking to each other within the team. The orchestrator cycles through agents (per question #3's turn-sequencing algorithm). These messages never leave the team.
- **Cross-team response turn** -- after the internal deliberation budget is exhausted (N internal turns), the orchestrator issues a **synthesis prompt** to a designated speaker agent: *"Synthesize this team's position into a response for the other team."*

That synthesis output is what crosses the boundary. Not raw internal deliberation. Not individual agent opinions. One composed message per deliberation cycle.

**Why this works:** No ambiguity about what's internal vs. external. The orchestrator controls the boundary explicitly -- it's a state machine transition, not content classification. Content classification would require parsing unstructured agent prose for "this is meant for Team B" signals, which is brittle and will break at 3 AM when nobody's watching.

**Why not let agents decide?** Because agents in your current architecture are stateless `claude -p` subprocess calls. They don't know they're on a team. They don't know the other team exists as a separate context window. The orchestrator holds that knowledge.

```
INTERNAL LOOP (stays within team):
  for turn in range(deliberation_budget):
      agent = select_next_agent(team)
      response = claude_call(agent.system_prompt, build_internal_payload(...))
      team.history.append(response)

CROSS-TEAM SYNTHESIS (exits the team):
  speaker = team.designated_speaker  # or rotate
  synthesis = claude_call(speaker.system_prompt, build_synthesis_payload(team.history))
  mcp.publish("cross-team", synthesis)
```

---

### 2. The MCP Server Message Format

The MCP server is a message broker. Not a database. Not a conversation engine. It holds messages in channels until they're consumed. Here's what a cross-team message looks like on the wire:

```typescript
interface CrossTeamMessage {
  id: string;                    // UUID, server-assigned
  channel: "cross-team";        // Fixed channel for team-to-team
  source_team: string;          // "team-a" or "team-b"
  target_team: string;          // "team-b" or "team-a"
  phase: string;                // "brainstorm" | "refine" | "specify" | "review"
  sequence_num: number;         // Monotonic per source_team, for ordering
  timestamp: string;            // ISO 8601
  speaker_agent: string;        // Who synthesized this (for attribution)
  
  content: {
    message: string;            // The actual synthesis text (full prose)
    token_estimate: number;     // Rough count, for context budget decisions
    
    // Structured metadata the synthesizer is prompted to include:
    stance: "proposing" | "responding" | "challenging" | "agreeing" | "requesting";
    key_points: string[];       // 3-5 bullet summary (synthesizer generates these)
    open_questions: string[];   // Explicit questions for the other team
    decision_references: string[]; // IDs of decisions this message references
  }
  
  delivery: {
    status: "pending" | "delivered" | "batched";
    delivered_at: string | null;
    batch_id: string | null;    // If batched with other messages
  }
}
```

**Why `key_points` and `stance` in the message itself?** Because when messages pile up (and they will), the receiving orchestrator needs structured data to batch and prioritize without making additional LLM calls. The synthesizing agent generates these as part of the synthesis prompt -- cheap to produce, expensive to reconstruct later.

**Why `token_estimate`?** The receiving orchestrator has a context budget. It needs to know whether it can fit the full message or needs the summary. This avoids a separate tokenization pass.

---

### 3. The MCP Tool Interface

Each team's Claude process doesn't call MCP tools directly. The **orchestrator** calls them on behalf of the team. The agents are stateless subprocesses -- they don't have MCP tool access. The orchestrator is the MCP client.

But for the record, here's the tool interface the orchestrator uses:

```typescript
// SENDING (orchestrator calls after synthesis turn)
tool: "mcp_crossteam_send"
params: {
  target_team: string,
  phase: string,
  speaker_agent: string,
  message: string,          // Full synthesis text
  stance: string,
  key_points: string[],
  open_questions: string[]
}
returns: { message_id: string, sequence_num: number }

// RECEIVING (orchestrator calls before building next team's prompt)
tool: "mcp_crossteam_receive"
params: {
  team: string,             // Which team is receiving
  since_sequence: number,   // Last sequence_num this team processed
  max_messages: number      // Context budget limit
}
returns: {
  messages: CrossTeamMessage[],   // Ordered by sequence_num
  pending_count: number,          // How many remain undelivered
  oldest_pending_age_seconds: number  // Staleness indicator
}

// PEEKING (orchestrator checks without marking delivered)
tool: "mcp_crossteam_peek"
params: {
  team: string
}
returns: {
  pending_count: number,
  total_token_estimate: number,   // Sum of all pending messages
  oldest_pending_age_seconds: number
}
```

**Why `peek` as a separate tool?** The orchestrator needs to decide whether to batch before it actually pulls messages. Peek lets it check the queue depth without committing to delivery.

---

### 4. How Team B Receives and Injects the Message

This is where the design gets real. Team B's orchestrator calls `mcp_crossteam_receive` before starting Team B's next deliberation cycle. What it gets back depends on queue state.

**Case 1: Single pending message (normal pace)**

The message gets injected as a distinct block in the user prompt for Team B's next agent turn. Not mixed into conversation history. Not presented as if a team member said it.

```
[INCOMING FROM TEAM A - Brainstorm Phase]
Speaker: The Cognitive Architect (Team A)
Stance: Proposing

---
{full message text}
---

Key points:
- Point 1
- Point 2
- Point 3

Questions for your team:
- Question 1
- Question 2

[END INCOMING MESSAGE]

Your team's task: Deliberate internally on this message.
{agent_name}, respond from your perspective.
```

**Why a distinct block, not conversation history?** Three reasons:

1. **Attribution clarity.** Team B agents need to know this came from outside, not from a teammate. Mixing it into history creates confusion about who said what.
2. **Context budget control.** The block has a known size. History entries get truncated by the rolling window. Cross-team messages need guaranteed delivery -- you can't let the truncation algorithm silently drop them.
3. **Phase coherence.** The incoming message carries phase metadata. If Team A sent it during brainstorm but Team B has transitioned to refine, the block can be tagged with that mismatch for the agent to handle.

**Team B sees the full message.** Not a summary. Here's why: summaries lose the argumentative structure, the specific phrasings that trigger genuine disagreement, the subtle positioning that makes the conversation real instead of two teams exchanging pleasantries. The whole point of anti-slop is that agents react to actual content, not sanitized abstracts.

---

### 5. The Pileup Problem: Batching When Messages Accumulate

Now the hard case. Team A has sent 5 messages while Team B was in a long deliberation cycle. Here's the protocol:

**Step 1: Orchestrator peeks.**

```python
status = mcp.peek(team="team-b")
# status.pending_count = 5
# status.total_token_estimate = 8400
# status.oldest_pending_age_seconds = 1800
```

**Step 2: Budget check.** The orchestrator has a cross-team context budget -- say, 4000 tokens max for incoming messages per deliberation cycle. 8400 exceeds it.

**Step 3: Batch synthesis.** The orchestrator pulls all 5 messages, then makes a dedicated `claude -p` call (not a team agent -- a utility call) to produce a batch digest:

```python
batch_prompt = f"""
You are a neutral message summarizer. Below are {len(messages)} messages 
from Team A to Team B, in chronological order. Produce a single briefing 
that preserves:
- All open questions (verbatim)
- All concrete proposals
- The evolution of their position across messages
- Any decisions or commitments made
- Points of disagreement within their sequence

Do NOT editorialize. Do NOT add your own analysis.
Keep the briefing under {budget_tokens} tokens.

Messages:
{format_messages(messages)}
"""
batch_digest = claude_call(system_prompt=None, message=batch_prompt)
```

**Step 4: Inject the digest with a pileup notice.**

```
[BATCHED INCOMING FROM TEAM A - 5 messages, covering last 30 minutes]
[Your team was deliberating internally while these accumulated]

---
{batch_digest}
---

Original message count: 5
Oldest message: 30 minutes ago
Most recent: 2 minutes ago

Note: Full individual messages are available in the session log. 
This digest preserves all questions and proposals.

[END BATCHED INCOMING]
```

**Who writes the summary?** A utility Claude call. Not a team agent (they'd inject their personality). Not an orchestrator heuristic (too brittle for unstructured text). A clean, un-persona'd LLM call with explicit instructions to preserve substance and strip editorial.

**Why not just send the most recent message?** Because message 2 might have contained the key proposal that messages 3-5 are refining. Recency is not priority. The batch digest preserves the arc.

**Why not send all 5 individually?** Context budget. Five full cross-team messages could eat 40% of the context window, crowding out Team B's own deliberation history. That's a context management failure that compounds across the session.

---

### 6. The State Machine

Putting it all together, here's the orchestrator's main loop for one team:

```python
while session.active:
    # 1. Check for incoming cross-team messages
    peek = mcp.peek(team=self.team_id)
    
    if peek.pending_count > 0:
        if peek.total_token_estimate <= CROSS_TEAM_BUDGET:
            # Pull individual messages
            incoming = mcp.receive(team=self.team_id, since_sequence=self.last_seq)
            cross_team_block = format_individual_messages(incoming.messages)
        else:
            # Batch and digest
            incoming = mcp.receive(team=self.team_id, since_sequence=self.last_seq)
            cross_team_block = batch_digest(incoming.messages, budget=CROSS_TEAM_BUDGET)
        
        self.last_seq = incoming.messages[-1].sequence_num
    else:
        cross_team_block = None
    
    # 2. Run internal deliberation cycle
    for turn in range(self.deliberation_budget):
        agent = self.select_next_agent()
        payload = build_turn_payload(
            agent=agent,
            team_history=self.history,
            cross_team_block=cross_team_block if turn == 0 else None,  # Only first agent sees it
            phase=self.current_phase
        )
        response = claude_call(agent.system_prompt, payload)
        self.history.append(response)
        cross_team_block = None  # Consumed
    
    # 3. Synthesize cross-team response
    speaker = self.select_speaker()
    synthesis = claude_call(
        speaker.system_prompt,
        build_synthesis_payload(self.history, self.current_phase)
    )
    
    # 4. Send to other team
    mcp.send(
        target_team=self.other_team_id,
        phase=self.current_phase,
        speaker_agent=speaker.name,
        message=synthesis.text,
        stance=synthesis.stance,
        key_points=synthesis.key_points,
        open_questions=synthesis.open_questions
    )
    
    # 5. Check phase transition (separate concern, question #7)
    self.check_phase_gate()
```

**Critical detail on line 22:** Only the **first agent** in the deliberation cycle sees the cross-team message directly. Subsequent agents see it through the first agent's reaction in team history. This prevents every agent from independently responding to the cross-team message and producing 4-6 redundant reactions. The first agent frames it, the rest build on that framing. This is how real teams work -- one person reads the email aloud, the room discusses.

---

### 7. Failure Modes I'm Watching

| Failure | Detection | Mitigation |
|---------|-----------|------------|
| Synthesis loses internal disagreement | Batch digest drops minority positions | Synthesis prompt explicitly requires: "Include any unresolved disagreements within Team A" |
| Queue grows unbounded | `oldest_pending_age_seconds` exceeds threshold | Hard cap: if queue > 10 messages, force a batch digest and inject immediately, interrupting current deliberation |
| Digest hallucinates content | Utility summarizer invents proposals | Digest prompt says "quote directly when possible" and original messages are preserved in session log for audit |
| Teams fall out of phase sync | Team A in "refine" sends to Team B still in "brainstorm" | Phase mismatch flag on the incoming block -- receiving team's agents are told the source phase |
| One team never reads messages | Deliberation budget too high, messages age out | Orchestrator enforces max age: if oldest pending > 15 minutes real-time, interrupt deliberation to process incoming |
| Synthesis agent sanitizes conflict | Anti-slop mechanisms in speaker's persona suppress edge | Synthesis prompt appends: "Include uncomfortable or contentious points. Do not smooth over disagreements." |

---

### 8. What This Design Deliberately Does NOT Do

- **No agent-to-agent cross-team messaging.** Teams talk to teams. Individual agents don't address individual agents on the other side. This keeps the boundary clean and prevents the social dynamics from fragmenting into side conversations.
- **No real-time streaming.** Messages are discrete. The MCP server is a queue, not a pipe. This is an overnight system, not a chat app.
- **No priority scoring of individual messages.** The batch digest handles pileup through chronological synthesis, not importance ranking. Ranking requires understanding the conversation's goals, which is the agents' job, not the broker's.
- **No message editing or retraction.** Once sent, it's sent. The session log is append-only. If Team A changes their mind, they send a new message saying so.

---

The remaining open dependency: this design assumes the synthesis prompt (step 3) can produce structured output (`stance`, `key_points`, `open_questions`) reliably. Your current codebase has zero structured output parsing -- everything is raw prose. That's the next infrastructure problem to solve before any of this works. Without it, the MCP message format degrades to `{ message: string }` and the batching/prioritization logic has nothing to work with.


---

# Question 5: How does context get managed across a multi-hour overnight session?

## The Cognitive Architect (creativity engine designer)

Good. Now I have the full picture. Here's the design:

---

## Context Lifecycle: Fresh Session to Context-Full to Phase-Reset to Session End

Pull a thread from cognitive load theory: the problem isn't storage, it's *retrieval cue design*. Every `claude -p` call is a blank mind waking up with amnesia. The question isn't "how much history fits" -- it's "what retrieval cues produce the right next thought."

### Layer 1: How History Lives on Disk

File-per-message, one JSON file per turn, named for sort order:

```
sessions/{session-id}/
  messages/
    0001_teamA_cognitive-architect_brainstorm.json
    0002_teamA_systems-pragmatist_brainstorm.json
    ...
    0087_teamB_investor_refine.json
  summaries/
    phase_brainstorm.md          # Generated at phase exit
    phase_refine.md              # Generated at phase exit
    rolling_latest.md            # Updated every N turns
  indices/
    ideas.json                   # Idea registry with origin turn refs
    decisions.json               # Decision log with confidence + turn refs
    disagreements.json           # Open tensions, both sides, turn refs
  checkpoints/
    turn_0050.json               # Full orchestrator state snapshot
    turn_0100.json
```

Each message file contains:

```json
{
  "turn": 87,
  "team": "B",
  "agent": "investor",
  "phase": "refine",
  "timestamp": "2026-03-17T03:42:11Z",
  "content": "...",
  "extracted": {
    "ideas_referenced": ["idea-014", "idea-027"],
    "ideas_introduced": ["idea-043"],
    "stance": "challenge",
    "confidence": 0.7,
    "key_claims": ["The freemium model fails for this market segment because..."]
  }
}
```

The `extracted` block is populated by the orchestrator running a lightweight extraction prompt after each turn. Cheap call, small output, but it builds the indices that make everything else work. This is the **spine** -- without it, you're searching haystacks.

### Layer 2: The Context Budget

The orchestrator tracks a token budget per call. Rough allocation for a 200k context window:

| Section | Budget | Notes |
|---|---|---|
| System prompt (personality, rules, phase) | ~3k tokens | Stable per agent |
| Phase briefing | ~5-8k tokens | Generated at phase transition |
| Idea registry (compressed) | ~2-4k tokens | Growing, pruned by relevance |
| Rolling summary of recent discussion | ~3-5k tokens | Updated every 10 turns |
| Verbatim recent messages | ~8-15k tokens | Sliding window |
| Cross-team incoming messages | ~2-4k tokens | Queued, batched |
| Perspective reminder | ~200 tokens | Every turn |
| Current prompt / instruction | ~500 tokens | Phase-specific |
| **Headroom for response** | ~remaining | At least 4k |

The key insight: **the ratio shifts over time.** Early session, verbatim history dominates. Late session, summaries and indices dominate. The orchestrator doesn't pick a strategy -- it fills the budget in priority order and stops when full.

### Layer 3: The Three Eras of a Session

**Era 1: Full Fidelity (turns 1-~40, roughly hours 0-2)**

Everything fits. The orchestrator sends:
- System prompt
- All prior messages verbatim
- Perspective reminder
- Current turn instruction

No summarization needed. The current `_truncated_history` approach of "first 2 + last 10" is wrong for this era -- you're throwing away context when you don't need to. The orchestrator should check: does full history fit the budget? If yes, send it all. Simple.

**Era 2: Rolling Compression (turns ~40-120, roughly hours 2-5)**

History exceeds budget. The orchestrator switches to a layered approach:

1. **Verbatim window**: last 15-20 messages (the active thread)
2. **Rolling summary**: a 2-3k token summary covering everything before the verbatim window, updated every 10 turns by a dedicated summarization call
3. **Idea registry**: compressed list of all ideas with their current status (alive, killed, merged, evolved-into)
4. **Phase anchor**: the first 2-3 messages of the current phase (the seed that started this line of thinking)

The rolling summary is generated by a `Curator` BackgroundAgent call that sees the full message history on disk and produces a structured summary:

```markdown
## Session Summary (through turn 85)

### Key Threads
- Thread: Freemium vs. paid-only pricing. Investor and Skeptic aligned against
  freemium. Product Oracle defending with usage data argument. UNRESOLVED.
- Thread: Real-time sync requirement. Consensus that async-first is correct
  but Architect insists on CRDT foundation for future real-time. TENTATIVE AGREEMENT.

### Ideas Still Alive
- idea-014: Job-based pricing tiers (magnitude: 0.8, champion: Product Oracle)
- idea-027: Offline-first with selective sync (magnitude: 0.7, champion: Architect)
[...]

### Killed Ideas (with reason)
- idea-003: Blockchain-based audit trail (killed turn 34: cost impractical)
[...]

### Open Tensions
- Pricing model: market segment disagreement between Investor and Oracle
- Scope: Builder wants MVP-only; Architect wants extensible foundation
```

This summary is **append-and-replace**, not append-only. Each update supersedes the previous one. The Curator has access to the full message directory and the previous summary, so it can maintain continuity.

**Era 3: Phase-Gated Resets (turns ~120+, roughly hours 5-8)**

By hour 5, even the rolling summary approach strains. This is where phase transitions earn their keep.

### Layer 4: Phase Transition Briefings

When the orchestrator triggers a phase transition (Brainstorm to Refine, Refine to Specify, etc.), it executes a **context reset**:

**Who generates it:** The `Weaver` BackgroundAgent. Not the team agents themselves -- they're participants, not narrators. The Weaver gets:
- Full message history for the completed phase (from disk)
- The idea registry
- The decision log
- The disagreement tracker
- The previous phase briefing (if any)

**What goes in it:**

```markdown
# Phase Briefing: Entering Refine Phase
## Generated at turn 94 | Brainstorm phase complete

### What Happened in Brainstorm
47 ideas generated across 94 turns. 12 survived initial discussion.
Key insight: The team split early on whether this is a B2B or B2C play,
and most ideas cluster around one assumption or the other.

### Surviving Ideas (ordered by magnitude)
1. **idea-014**: Job-based pricing tiers [B2B assumption]
   - Origin: Product Oracle, turn 12
   - Strongest argument: "Freelancers already think in jobs, not months"
   - Strongest counter: "Job boundaries are fuzzy -- what counts as a job?"
   - Current champion: Product Oracle (0.8 confidence)

2. **idea-027**: Offline-first with selective sync [architecture]
   - Origin: Cognitive Architect, turn 23
   - Strongest argument: "Field workers can't depend on connectivity"
   - Strongest counter: "Sync conflicts are an engineering nightmare"
   - Current champion: Cognitive Architect (0.7 confidence)
[...]

### Unresolved Tensions Carrying Forward
1. B2B vs B2C market positioning (Investor vs Oracle)
2. MVP scope vs extensible foundation (Builder vs Architect)
3. Privacy model: zero-knowledge vs platform-managed

### Your Mission in Refine Phase
Challenge every surviving idea. Find the fatal flaw. If an idea can't
survive scrutiny, kill it now. The goal is 3-5 hardened ideas, not 12
fragile ones.

### Key Decisions Already Made
- Target: solo freelancers and small agencies (2-10 people)
- Platform: mobile-first, web companion
- Revenue: will charge money (not ad-supported)
```

**Does the team lose access to pre-briefing messages?** Yes, deliberately. The verbatim message window resets to zero. The briefing *is* the compressed memory of everything before. This is the design's equivalent of sleeping on it -- you wake up with the conclusions, not the raw experience.

But -- and this is the critical nuance -- **the idea registry and decision log persist across briefings as structured data**. An agent doesn't need the original brainstorm conversation to reference idea-014. They reference it by ID, and the registry carries forward the origin, arguments, and status.

### Layer 5: The Retrieval Problem (Hour 7 Referencing Hour 1)

This is the real puzzle. An agent in hour 7 (deep in Specify phase) needs to reference an insight from hour 1 (early Brainstorm). The original message is long gone from context. Three mechanisms:

**Mechanism A: The Idea Registry as Persistent Memory**

Every idea extracted during the session gets an entry in `ideas.json`. The entry carries forward across phase resets. When the orchestrator builds the prompt, it includes the registry (compressed). So the agent doesn't remember the *conversation* where idea-014 was born -- but they know idea-014 exists, who proposed it, what the strongest argument for and against it was, and its current status.

This is analogous to how human teams work. You don't remember the exact meeting where someone proposed the pricing model. You remember the pricing model.

**Mechanism B: On-Demand Retrieval**

When an agent's output references something the orchestrator can't resolve from the current context (detected via a lightweight parse), the orchestrator can inject a retrieval block in the next turn:

```
[CONTEXT RETRIEVAL: You referenced "the connectivity argument from early 
brainstorm." Here's what the record shows:

Turn 23, Cognitive Architect: "Field workers operate in environments 
where connectivity is a luxury, not a given. Any architecture that 
assumes always-on connectivity is building on sand..."

Turn 31, Systems Pragmatist (rebuttal): "Offline-first sounds noble but 
sync conflict resolution is where projects go to die..."]
```

This is expensive -- it requires the orchestrator to detect the reference, look up the relevant turns, and inject them. But it's rare. Most references are to ideas (handled by the registry) not to specific conversational moments.

**Mechanism C: The Phase Briefing as Lossy Compression**

Accept that some things are lost. The phase briefing is lossy compression by design. A tangential aside in hour 1 that nobody built on? Gone. An interesting metaphor that didn't become an idea? Gone. This is a feature. The briefing acts as a **relevance filter** -- what matters survives, what doesn't fades. Human memory works the same way.

The Weaver generating the briefing is the quality gate here. A good briefing preserves the *tensions* (because those drive interesting Refine-phase discussion) and the *surprising insights* (because those are the highest-value outputs). A bad briefing just lists ideas. The Weaver prompt needs to be tuned to prioritize conflict, surprise, and open questions over consensus and closure.

### Layer 6: The Full Lifecycle, Concrete

```
HOUR 0 (Turn 1-5):     Fresh session. Full history. No compression needed.
                        Orchestrator seeds both teams from user's idea brief.
                        System prompts loaded from YAML. Phase: Brainstorm.

HOUR 1 (Turn 5-25):    Still full fidelity. Idea registry growing.
                        Extraction prompt runs after each turn, populating indices.
                        Context budget: ~40% used.

HOUR 2 (Turn 25-50):   Approaching budget. Orchestrator switches to:
                        phase anchor (first 3 turns) + rolling summary + 
                        verbatim window (last 15). Curator generates first 
                        rolling summary.

HOUR 3 (Turn 50-70):   Rolling summary updated every 10 turns.
                        Idea registry now has 30+ entries, compressed to ~2k tokens.
                        Some early ideas already killed and archived.

HOUR 3.5:              PHASE TRANSITION: Brainstorm -> Refine
                        Weaver generates phase briefing.
                        Context RESET. All agents start fresh with:
                        - System prompt (unchanged)
                        - Phase briefing (new, ~5-8k tokens)
                        - Idea registry (carried forward)
                        - Decision log (carried forward)
                        - Empty verbatim window
                        
                        This is the "sleep." Agents wake up knowing what 
                        survived brainstorm but not how the sausage was made.

HOUR 4-5 (Turn 70-110): Refine phase. Same compression lifecycle repeats.
                         Ideas getting killed. Tensions sharpening.
                         Rolling summary restarts for this phase.

HOUR 5.5:              PHASE TRANSITION: Refine -> Specify
                        New briefing generated. Surviving ideas now ~5-7.
                        Briefing includes both Brainstorm and Refine summaries
                        (nested: "In Brainstorm we generated X, in Refine we 
                        narrowed to Y, here's what survived and why").

HOUR 6-7 (Turn 110-160): Specify phase. Agents writing concrete specs.
                          Cross-team messages heavier (spec proposals going 
                          back and forth). Registry entries now have detailed
                          spec fragments attached.

HOUR 7.5:              PHASE TRANSITION: Specify -> Review
                        Briefing now includes draft spec sections.
                        Agents doing adversarial review of spec quality.

HOUR 8:                SESSION END.
                        Weaver generates Morning Brief from:
                        - All 4 phase briefings
                        - Final idea registry  
                        - Decision log
                        - Disagreement tracker
                        - Full message archive (for highlight extraction)
```

### Layer 7: What the Current Code Needs to Change

The existing `_truncated_history()` in `conversation.py` -- the "first 2 + last 10" approach -- is a placeholder that works for the current interactive testing mode. For the real system:

1. **Replace fixed truncation with budget-aware assembly.** The orchestrator should estimate tokens per message and fill sections by priority until the budget is reached.

2. **Add the extraction step.** After each `claude -p` response, run a small extraction call that populates the idea/decision/disagreement indices. This is the most important new component -- without it, the summaries and briefings have nothing structured to work with.

3. **Add the Curator and Weaver as concrete BackgroundAgent implementations.** The Curator produces rolling summaries (every 10 turns). The Weaver produces phase briefings (at transitions) and the Morning Brief (at session end).

4. **The rolling summary replaces the middle of the history, not the edges.** You always keep the phase anchor (start) and the verbatim window (end). The summary covers the gap. As the session grows, the summary covers more and the verbatim window stays fixed.

5. **Phase transitions are hard resets on the verbatim window** but carry forward structured data (registries, logs). This is the mechanism that makes 8-hour sessions survivable -- without it, context quality degrades monotonically.

---

The fundamental principle: **don't compress the conversation; extract the structure, then let the conversation be forgotten.** Ideas, decisions, tensions, and open questions are the durable artifacts. The dialogue that produced them is scaffolding. Once the scaffolding has done its job, the briefing captures what it built and the raw messages go to cold storage on disk -- available for retrieval if needed, but not burning context budget by default.


---

## The Product Oracle (user advocate and product strategist)

Now I have the full picture. The current beta has a naive truncation (keep first 2-3 + last 10-15 messages) with no disk persistence, no summarization, no phase-aware context management. Let me design the strategy.

---

## Context Management Strategy: The Memory Architecture

The job to be done: an agent at hour 7 needs to argue passionately about an idea born at hour 1, even though that idea left their context window four hours ago. The system must make this possible without requiring the agent to have seen every message.

### Layer 1: Disk Storage -- The Source of Truth

Every message hits disk immediately. The orchestrator never relies on in-memory state surviving.

```
sessions/{session-id}/
  messages/
    0001_brainstorm_teamA_cognitive-architect.md
    0002_brainstorm_teamA_systems-pragmatist.md
    0003_brainstorm_teamA_product-oracle.md
    0004_brainstorm_cross_teamA-to-teamB.md
    ...
  summaries/
    brainstorm_rolling_001.md      # Generated every ~20 messages
    brainstorm_rolling_002.md
    brainstorm_phase_final.md      # Generated at phase exit
    refine_rolling_001.md
    ...
  indices/
    ideas.json                     # Idea registry with magnitude, origin turn, status
    decisions.json                 # Decision log with confidence
    tensions.json                  # Unresolved disagreements
    references.json                # "Agent X referenced idea Y at turn Z"
  briefings/
    phase_brainstorm_exit.md       # Phase transition briefing
    phase_refine_exit.md
    ...
  state.json                       # Session state: current phase, turn count, token estimates
```

One file per message. Cheap to count, cheap to selectively load. The orchestrator never reads all of them at once -- it reads the index files and pulls specific messages on demand.

### Layer 2: The Context Budget

Before building any prompt, the orchestrator calculates a token budget:

```python
TOTAL_CONTEXT = 190_000  # Conservative estimate for claude -p
SYSTEM_PROMPT_RESERVE = 3_000   # Agent identity + project context + anti-slop rules
RESPONSE_RESERVE = 4_000        # Room for the agent to respond
PERSPECTIVE_REMINDER = 200      # Per-turn identity reinforcement
AVAILABLE_FOR_HISTORY = TOTAL_CONTEXT - SYSTEM_PROMPT_RESERVE - RESPONSE_RESERVE - PERSPECTIVE_REMINDER
# ~182,800 tokens for history + context injection
```

The orchestrator doesn't count tokens precisely (no tokenizer dependency). It estimates at 4 chars per token and tracks cumulative message sizes. Close enough for budgeting; the safety margin absorbs the error.

### Layer 3: The Three Tiers of History

When building a prompt, the orchestrator assembles context in priority order, stopping when the budget is consumed:

**Tier 1: Structural Context (always included, ~2,000-5,000 tokens)**
- Current phase description and goals
- Latest rolling summary (or phase briefing if just after a transition)
- The idea index: every named idea with its current magnitude, champion, and status -- one line each
- Unresolved tensions list
- Recent decisions

This is the skeleton. An agent who reads only Tier 1 knows what phase they're in, what ideas are alive, what's been decided, and what's contentious. They can contribute meaningfully even if they've seen nothing else.

**Tier 2: Recent Conversation (fills ~60% of remaining budget)**
- Last N messages in reverse chronological order, where N is determined by budget
- Early session (hour 0-2): this is everything -- full history fits
- Mid session (hour 3-5): last ~40-60 messages
- Late session (hour 6-8): last ~25-40 messages, depending on message length

**Tier 3: Relevant Deep Pulls (fills remaining budget)**
- When an agent's most recent messages reference specific ideas by name, the orchestrator pulls the original messages where those ideas were introduced
- When tension exists between agents, pull the key exchange where the disagreement crystallized
- During Specify phase: pull the messages that defined the spec requirements being discussed

The orchestrator selects Tier 3 content using the `references.json` index -- simple keyword matching against idea names, not semantic search. Good enough when ideas have distinct names.

### Layer 4: Rolling Summaries

Every ~20 messages within a phase, the orchestrator generates a rolling summary. Here's the mechanism:

```
Orchestrator takes: last rolling summary + messages since that summary
Sends to: a dedicated summarizer call (claude -p with a summarization system prompt)
Produces: ~500-800 token summary covering:
  - New ideas introduced (with originating agent)
  - Ideas that gained or lost momentum
  - Key challenges raised
  - Agreements reached
  - Unresolved tensions
  - Any research findings
Stored to: summaries/brainstorm_rolling_002.md
```

The summarizer is a separate `claude -p` call with a tight system prompt. It's not one of the team agents. It's infrastructure. It runs between turns, adding ~30 seconds of latency every 20 messages. Over 8 hours, that's maybe 15-20 summarization calls. Acceptable.

The rolling summary chain is cumulative: each new summary incorporates the previous one plus new messages, so the latest summary is always a self-contained account of the phase so far.

### Layer 5: Phase Transition -- The Briefing Reset

This is the critical moment. When the orchestrator determines a phase gate is met (that's a separate design question), it executes a context reset:

**Step 1: Generate Phase Exit Briefing**

The orchestrator makes a dedicated summarizer call with:
- All rolling summaries from the ending phase
- The idea index
- The decision log
- The tension log
- The last 10 messages (where the phase culminated)

The briefing produced contains:
- Phase outcome: what was accomplished
- Surviving ideas: ranked by magnitude, with one-paragraph descriptions and their champions
- Decisions made: with confidence levels and dissenting opinions noted
- Open tensions: disagreements that were not resolved
- Key constraints identified: technical, market, or design constraints that emerged
- Recommendations for next phase: what the agents should focus on

**Step 2: Update the Idea Index**

Ideas that died during the phase are marked `status: eliminated` with a reason. Ideas that survived get updated magnitudes. New ideas from the phase are added. The index is the institutional memory that outlives any single context window.

**Step 3: Reset Agent History**

The orchestrator clears the in-memory conversation history for all agents. The next prompt each agent receives contains:
- Their system prompt (unchanged -- identity persists)
- The phase transition briefing as a `[System]` message
- The new phase description and goals
- The updated idea index
- Nothing else -- no pre-briefing messages

Yes, agents lose access to pre-briefing messages entirely. This is a feature. The briefing is designed to carry everything they need. If an idea mattered, it's in the briefing. If it's not in the briefing, it didn't survive the phase -- and agents shouldn't be arguing for dead ideas in the new phase.

**Step 4: First Turn in New Phase**

The orchestrator sends each agent a priming question appropriate to the new phase:
- Brainstorm to Refine: "Review the surviving ideas. Which ones are you most skeptical of, and why?"
- Refine to Specify: "Based on the refined ideas, what needs to be specified first for implementation?"
- Specify to Review: "Here are the draft specifications. What would break first in production?"

This gives agents a clear entry point without needing the full history.

### Layer 6: The Idea Index as Persistent Memory

This solves the hour-7-references-hour-1 problem. The idea index is a structured JSON file that persists across the entire session:

```json
{
  "ideas": [
    {
      "id": "idea_007",
      "name": "Morning Brief Tiered Triage",
      "short_description": "Categorize overnight output into FYI/input-needed/decision-needed/tiebreaker tiers",
      "introduced_by": "product-oracle",
      "introduced_turn": 12,
      "introduced_phase": "brainstorm",
      "magnitude": 0.85,
      "magnitude_history": [0.5, 0.6, 0.75, 0.85],
      "champions": ["product-oracle", "cognitive-architect"],
      "challengers": ["systems-pragmatist"],
      "status": "active",
      "key_message_refs": [12, 34, 67, 112],
      "last_discussed_turn": 112
    }
  ]
}
```

When an agent at hour 7 says "I still think the tiered triage approach from earlier is the right framing," the orchestrator can:
1. Identify the reference to `idea_007` by name matching
2. Pull `key_message_refs` to inject the 2-3 most relevant original messages into Tier 3 context
3. The agent sees the idea's current magnitude and who's been championing or challenging it

The agent doesn't need to remember the original brainstorm. They need to know: the idea exists, what it means, who's for and against, and how strong it is. The index provides all of that in ~100 tokens per idea.

### Layer 7: The Orchestrator's Update Loop

After every agent response, the orchestrator:

1. **Appends** the message to disk (`messages/NNNN_phase_team_agent.md`)
2. **Parses** for idea references -- simple string matching against known idea names
3. **Updates** `references.json` with any new references
4. **Updates** idea magnitudes based on signals:
   - Agent explicitly defends idea: magnitude += 0.05
   - Agent explicitly challenges idea: magnitude -= 0.03 (challenges slow decline, not kill)
   - Agent builds on idea with new detail: magnitude += 0.08
   - Agent introduces competing idea: original magnitude -= 0.02
   - These are rough heuristics. The orchestrator parses for signal phrases like "I disagree with [idea]" or "building on [idea]" -- not perfect, but functional
5. **Checks** rolling summary trigger (every ~20 messages)
6. **Checks** phase gate criteria
7. **Builds** the next agent's prompt using the three-tier system

### Full Timeline: 8-Hour Session

| Time | Context State | Strategy |
|------|--------------|----------|
| Hour 0-1 | Fresh. Full history fits easily. | Full history in Tier 2. No summaries needed yet. Tier 1 is mostly empty (few ideas, no decisions). |
| Hour 1-2 | History growing. Still fits. | First rolling summary generated around turn ~20. Tier 1 starts to have substance. |
| Hour 2-3 | Approaching budget pressure. | Tier 2 starts truncating oldest messages. Rolling summaries provide coverage for what's lost. |
| Hour 3 | **Phase transition (Brainstorm to Refine)** | Exit briefing generated. History cleared. Agents restart with briefing + idea index. Context is fresh again. |
| Hour 3-5 | Fresh context, building back up. | Same cycle: full history first, rolling summaries kick in, truncation begins. |
| Hour 5 | **Phase transition (Refine to Specify)** | Second briefing. Second reset. Ideas that survived two phases are battle-tested. Index is rich. |
| Hour 5-7 | Specify phase. Messages are longer (spec content). | Tier 2 fills faster. Tier 3 becomes important -- pulling original idea definitions and key challenge messages for spec accuracy. |
| Hour 7 | **Phase transition (Specify to Review)** | Third briefing. Context reset. Draft specs are now artifacts on disk, referenced in briefing. |
| Hour 7-8 | Review phase. Adversarial. | Short phase, context pressure rarely an issue. Agents have specs + briefing + fresh context. |
| Hour 8 | **Session end** | Final summary generated. Morning Brief pipeline kicks in (separate design). |

### What This Doesn't Solve (Honestly)

- **Subtle callbacks**: If an agent at hour 7 makes an oblique reference to a conversation dynamic from hour 1 without naming a specific idea, the orchestrator won't catch it. The index only tracks named ideas.
- **Emotional continuity**: An agent who was frustrated in hour 2 won't remember that frustration after a phase reset. The personality is in the system prompt, but the emotional arc of the conversation is lost. This is acceptable -- phase resets are meant to be fresh starts.
- **Cross-team context**: Each team has its own history and summaries. Team B never sees Team A's internal deliberation, only the cross-team messages. The briefing summarizes what Team A communicated, not what they discussed internally.

These are tradeoffs, not bugs. The system is designed for idea survival, not perfect recall. Ideas that matter get tracked in the index. Conversations that matter get captured in summaries. Everything else is allowed to fade -- just like it does in real teams.


---

## The Systems Pragmatist (infrastructure realist)

Good. Now I know what's real and what's vapor. Let me walk through this systematically.

---

## Context Lifecycle: The Hard Problem

What exists today: a sliding window that keeps first 2-3 + last 10-15 messages. No summarization. No disk persistence between calls. No phase briefings. That's the foundation we're building on.

Here's the lifecycle, failure modes included.

---

### Hour 0-2: The Easy Part

**State**: Fresh session. History fits in context.

Every `claude -p` call reconstructs the full prompt: system prompt (~2-3K tokens for persona/traits/rules) + conversation history + current message. At 5-10 exchanges, you're maybe 15-20K tokens. No pressure.

**Disk layout at this point:**

```
sessions/{session-id}/
  messages/
    0001_teamA_brainstorm.json    # full message body
    0002_teamB_brainstorm.json
    ...
  index.json                      # ordered message manifest
  state.json                      # current phase, turn count, active agents
```

Each message file stores: sender, team, phase, timestamp, content, extracted metadata (ideas mentioned, decisions made, challenges raised). The extraction happens inline -- a lightweight structured-output call after each cross-team message. This is the continuous extraction layer from the design doc, and it's non-optional. If you skip it here, you have nothing to summarize later.

**The orchestrator's prompt assembly at this stage:**

```python
history = load_all_messages(session_id)  # they all fit
payload = system_prompt + format_history(history) + current_context
```

Simple. No decisions to make.

---

### Hour 2-4: The Window Starts Sliding

**State**: 40-80 cross-team exchanges, plus internal deliberations. History no longer fits.

This is where the current `_truncated_history()` kicks in -- keep first N + last M. But this is a bad strategy for an 8-hour session. Here's why:

**Failure mode**: Message 23 contains the key insight that shapes the entire product direction. By hour 3, it's fallen out of the window. Agent references "the API-first approach we agreed on" but has no context for what that means or why it was chosen. The agent either hallucinates the details or gives a generic response.

**What you actually need: tiered context.**

The orchestrator builds the prompt in layers:

1. **System prompt** (~2-3K tokens) -- persona, phase rules, anti-slop. Static per phase.
2. **Session brief** (~1-2K tokens) -- accumulated decisions, active ideas, open tensions. Updated every N exchanges by a summarization call.
3. **Phase context** (~2-4K tokens) -- what happened in the current phase so far. Rolling summary.
4. **Recent window** (~8-15K tokens) -- last 8-12 full messages. Verbatim.
5. **Current message** -- what the agent is responding to.

The session brief is the critical piece. It's built from the extracted metadata accumulated since message 0001. Not a summary of the conversation -- a summary of the *state*: what's been decided, what's contested, what ideas are alive, what's been killed and why.

**How the session brief gets built:**

```
Every 5 cross-team exchanges:
  1. Collect all extracted metadata since last brief
  2. Run a summarization call (Haiku, cheap):
     "Given these extracted ideas/decisions/tensions, 
      update this running brief. Preserve all decisions 
      and their rationale. Drop ideas that were explicitly 
      killed. Compress discussion into state."
  3. Write updated brief to sessions/{id}/brief.md
  4. Brief is injected into every subsequent prompt
```

The brief is append-and-compress, not regenerate-from-scratch. Each update adds new state and compresses old state. You're spending ~500 tokens of Haiku every 5 exchanges. Cheap insurance.

---

### Hour 4: Phase Transition (The Hard Reset)

**State**: Brainstorm phase ending, Refine phase starting. 80+ exchanges in history.

This is where the design doc says "a briefing is generated for a context reset." Let me be precise about what that means, because getting this wrong loses hours of work.

**What goes in the phase transition briefing:**

```
PHASE TRANSITION BRIEF: Brainstorm → Refine
Generated by: Orchestrator (not an agent -- agents don't brief themselves)

## Decisions Made
- [list of explicit decisions with rationale, extracted from metadata]

## Ideas Advancing (ranked by magnitude)
- Idea 1: [description, who championed it, key supporting arguments]
- Idea 2: ...
- (top 15-20 ideas, not all 50+)

## Ideas Killed (and why)
- [compressed list -- important so agents don't re-propose them]

## Open Tensions
- [unresolved disagreements, with positions attributed to agents]

## Key Constraints Established
- [technical, business, or scope constraints that emerged]

## Deficit Flags
- [anything that fell short of exit criteria]
```

**Who generates it:** The orchestrator, using a dedicated summarization prompt that takes the full session brief + recent messages + all extracted metadata as input. This is a one-time Sonnet call at the transition point. Worth the cost.

**Critical point: the orchestrator has access to the full disk history.** It can read every `messages/*.json` file. The agents never can -- they only see what's in their prompt. So the orchestrator is the only entity that can produce a faithful briefing.

**Does the team lose access to pre-briefing messages?** Yes. Completely. The next `claude -p` call for the Refine phase starts with:

```
1. New system prompt (Refine phase rules, adjusted anti-slop weights)
2. Phase transition briefing (injected as "context" block)
3. No prior message history
```

The agents start the new phase with the briefing as their only history. First message in Refine phase is the orchestrator saying: "Refine phase has begun. Here's what Brainstorm produced: [briefing]. Your task now is..."

**Failure mode**: Briefing misses a nuance. An agent in Brainstorm had a subtle concern about scalability that was noted but not extracted as a "tension." It vanishes. Mitigation: the extraction layer must be aggressive about capturing dissent. Every pushback, every "I'm not sure about..." gets tagged as a tension, not just explicit disagreements.

---

### Hour 4-7: Deep in Refine/Specify

**State**: New phase, history growing again. Same problem returns.

The tiered context system from Hour 2-4 applies again. Session brief keeps accumulating -- now it includes both the Brainstorm phase summary (compressed further) and the growing Refine state.

**Session brief structure at this point:**

```
## Prior Phases
### Brainstorm (completed)
- [2-3 sentence summary]
- [key decisions carried forward]
- [deficit flags]

## Current Phase: Refine
### Decisions Made
- ...
### Active Debates
- ...
### Ideas Under Evaluation
- ...
```

The prior phase section compresses over time. By the Specify phase, Brainstorm is 3-4 lines. Refine gets the detailed treatment. Always prioritize the current phase's state.

---

### Hour 7: The Retrieval Problem

> "How does an agent in hour 7 reference an idea from hour 1 that's no longer in their context window?"

**Short answer: they can't, unless the system surfaces it.**

Three mechanisms, in order of preference:

**1. It survived in the session brief.** If the idea was important enough to make it through every brief update, it's still there in compressed form. This is the happy path. This is why the brief must be conservative about dropping ideas -- only explicitly killed ideas get removed.

**2. The orchestrator detects a reference and injects it.** This is harder but doable. If an agent says "what about that marketplace idea from early on," the orchestrator can:
- Pattern-match the reference against the extracted metadata index
- Pull the relevant `messages/*.json` files from disk
- Inject a "retrieved context" block into the next prompt: `[RETRIEVED: Message #0023 by Product Oracle: "The marketplace model could work if we..."]`

This is basically RAG over your own session history. The extracted metadata serves as the index. You don't need embeddings -- keyword matching against idea titles and decision labels is usually sufficient for a single session's worth of content.

**3. The agent reconstructs it from the brief.** The brief says "marketplace model (killed: scalability concerns)." The agent works from that compressed representation. They don't have the original nuance, but they have the conclusion.

**Failure mode for all three**: The idea was never extracted. It was mentioned in passing, no agent championed it, the extraction prompt didn't flag it. It's in the raw message files on disk but invisible to the retrieval system. This is an unrecoverable loss within the session -- it might surface in the Morning Brief when the Weaver agent processes the full transcript.

---

### Session End: What Persists

```
sessions/{session-id}/
  messages/
    0001_teamA_brainstorm.json
    ...
    0247_teamB_review.json
  briefs/
    brainstorm_exit.md          # phase transition briefing
    refine_exit.md
    specify_exit.md
  brief.md                      # final session brief (cumulative)
  transcript.md                 # full human-readable conversation
  metadata/
    ideas.json                  # all extracted ideas with final magnitude
    decisions.json              # all decisions with rationale
    tensions.json               # unresolved tensions
  artifacts/
    spec_v1.md                  # generated artifacts
    architecture_v1.md
  state.json                    # final session state
```

The Morning Brief generator reads all of this. It has unlimited context because it's processing files, not maintaining a conversation.

---

### The Strategy, Summarized

| Time | Context Budget | History Strategy | Key Mechanism |
|------|---------------|-----------------|---------------|
| Hour 0-2 | Plenty | Full history | Raw message replay |
| Hour 2-4 | Tight | Tiered: brief + recent window | Rolling session brief (Haiku) |
| Hour 4 (transition) | Reset | Phase briefing replaces all history | Orchestrator-generated briefing (Sonnet) |
| Hour 4-7 | Tight again | Tiered with compressed prior phases | Brief accumulation + compression |
| Hour 7+ | Critical | Brief + tiny window + on-demand retrieval | Metadata-indexed retrieval from disk |

**Three non-negotiable pieces:**

1. **Continuous extraction** -- every cross-team message gets metadata extracted. Skip this and you have nothing to build briefs from.
2. **Rolling session brief** -- not a transcript summary, a *state* summary. Decisions, live ideas, tensions. Updated every 5 exchanges.
3. **Message-per-file on disk** -- the orchestrator's memory is the filesystem. Agents are stateless; the disk is not.

**The thing most likely to go wrong:** Extraction quality. If the extraction prompt is too conservative, you lose ideas. Too aggressive, the brief bloats and eats your context budget. This needs tuning per phase -- Brainstorm extraction should cast a wide net, Specify extraction should focus on decisions and spec language.


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


---

## The Product Oracle (user advocate and product strategist)

Good question. This is exactly the kind of thing that looks clean on a slide but falls apart at 3am in an 8-hour run. Let me ground this in what the orchestrator actually does today and design something that works.

---

## Enforcement Architecture: What's Real

### The Three Tiers

Every mechanism falls into one of three enforcement tiers based on cost and complexity:

| Tier | Enforcement | Cost | Who Runs It |
|------|------------|------|-------------|
| **Prompt-only** | Instructions baked into system prompt | Zero -- already paid for | The LLM itself |
| **Parse-and-inject** | Orchestrator parses output, modifies next prompt | Zero additional LLM cost | `multi_agent.py` post-turn hook |
| **Audit call** | Dedicated LLM call to evaluate conversation | One extra claude CLI call | Orchestrator on a schedule |

The entire design goal: **keep as much as possible in Tiers 1 and 2.** Tier 3 is expensive and slow. Use it surgically.

---

### Mechanism-by-Mechanism Breakdown

#### 1. Agreement Tax -- PROMPT-ONLY
Already implemented. System prompt instruction: "If you agree, you MUST add substance." No runtime needed. The agent either follows the instruction or it doesn't. If it doesn't, convergence suppression (below) catches the downstream effect.

#### 2. Perspective Enforcement -- PROMPT-ONLY
Already implemented. System prompt + per-turn perspective reminder. The `build_perspective_reminder()` already fires every turn. This is the foundation that makes everything else work -- without it, agents drift into generic-helpful-assistant mode and all other mechanisms fail.

#### 3. Devil's Advocate Duty -- PROMPT-ONLY
Already implemented. Prompt instruction for designated agents.

#### 4. Uncomfortable Idea Quotas -- PROMPT + PARSE-AND-INJECT
Already implemented. `should_trigger_uncomfortable_idea()` counts turns and injects a system message. This is the existing pattern that the remaining mechanisms should copy.

#### 5. Domain Pivots -- PROMPT-ONLY
Prompt instruction. Could be upgraded to parse-and-inject if domain repetition is detected (see novelty scoring).

---

Now the five that need runtime work:

#### 6. Convergence Suppression -- PARSE-AND-INJECT

**Detection: Agreement Signal Parsing**

No embeddings. No background agent. The orchestrator already sees every response before passing it to the next agent. Add a `convergence_monitor.py` module that runs after each turn:

```python
class ConvergenceMonitor:
    """Tracks agreement velocity across turns."""
    
    def __init__(self, window_size=6, threshold=0.6):
        self.window_size = window_size    # rolling window of turns
        self.threshold = threshold         # agreement ratio that triggers
        self.turn_scores = []              # per-turn agreement scores
    
    def score_turn(self, response: str, agent_config: AgentConfig) -> float:
        """Score 0.0 (pure pushback) to 1.0 (pure agreement)."""
        score = 0.0
        signals_found = 0
        
        # Signal category 1: Explicit agreement phrases
        agreement_phrases = [
            "i agree", "exactly", "great point", "absolutely",
            "you're right", "building on that", "that's spot on",
            "couldn't agree more", "well said"
        ]
        pushback_phrases = [
            "but", "however", "i disagree", "the problem with",
            "what about", "that ignores", "i'm not convinced",
            "that won't work", "the risk is", "counterpoint"
        ]
        
        lower = response.lower()
        agreements = sum(1 for p in agreement_phrases if p in lower)
        pushbacks = sum(1 for p in pushback_phrases if p in lower)
        
        if agreements + pushbacks > 0:
            score = agreements / (agreements + pushbacks)
            signals_found += 1
        
        # Signal category 2: Position abandonment
        # Check if agent is pushing back on things they're configured to
        if agent_config.position.pushback_on:
            topics_addressed = sum(
                1 for topic in agent_config.position.pushback_on
                if topic.lower() in lower
            )
            # Agent should be mentioning their pushback topics
            # Silence on them = drift toward consensus
            if topics_addressed == 0 and len(lower) > 200:
                score = (score + 0.7) / 2  # blend toward agreement
                signals_found += 1
        
        # Signal category 3: Response structure
        # Short responses after long discussion = "yeah sure" energy
        if len(response.strip()) < 150 and not any(p in lower for p in pushback_phrases):
            score = (score + 0.8) / 2
            signals_found += 1
        
        return score if signals_found > 0 else 0.5  # neutral if no signal
```

**When it runs:** After every agent turn, before constructing the next agent's prompt. Pure Python string matching -- adds milliseconds, not seconds.

**What triggers:** Rolling window. If the average agreement score across the last `window_size` turns exceeds `threshold` (default 0.6), the monitor fires.

**Intervention -- prompt injection, not agent swap:**

```python
def get_intervention(self) -> Optional[str]:
    if len(self.turn_scores) < self.window_size:
        return None
    
    recent = self.turn_scores[-self.window_size:]
    avg = sum(recent) / len(recent)
    
    if avg > self.threshold:
        return (
            "[System: Convergence detected -- the group has been agreeing "
            "for several turns. Your job right now is to find the WEAKEST "
            "assumption in the current direction and attack it. What's the "
            "strongest argument that this approach fails? What user need "
            "is being ignored? Do not validate -- interrogate.]"
        )
    return None
```

This follows the exact same pattern as `should_trigger_uncomfortable_idea()`. The orchestrator appends the intervention string to the next agent's payload. No agent swap. No background process. The agent receiving the intervention gets a direct instruction to break the pattern.

**Why not a BackgroundAgent?** Because the orchestrator already has the information. Every response passes through `multi_agent.py`. Spawning another claude process to read what we already have is waste. Save the LLM audit calls for things Python can't parse.

---

#### 7. Novelty Scoring -- PARSE-AND-INJECT

**Detection: N-gram Overlap (No Embeddings)**

Similarity without embeddings is a solved problem. Use token-level Jaccard similarity on extracted key phrases:

```python
class NoveltyScorer:
    """Measures how much new content each turn introduces."""
    
    def __init__(self, decay_window=8, staleness_threshold=0.55):
        self.recent_content = []  # last N turns as token sets
        self.decay_window = decay_window
        self.staleness_threshold = staleness_threshold
    
    def score_novelty(self, response: str) -> float:
        """Score 0.0 (pure repetition) to 1.0 (completely novel)."""
        tokens = self._extract_content_tokens(response)
        
        if not self.recent_content:
            self.recent_content.append(tokens)
            return 1.0
        
        # Compare against union of recent turns
        recent_union = set()
        for prev_tokens in self.recent_content[-self.decay_window:]:
            recent_union.update(prev_tokens)
        
        if not recent_union:
            return 1.0
        
        overlap = tokens & recent_union
        novelty = 1.0 - (len(overlap) / len(tokens)) if tokens else 0.0
        
        self.recent_content.append(tokens)
        return novelty
    
    def _extract_content_tokens(self, text: str) -> set:
        """Extract meaningful content words, skip stopwords and filler."""
        # Lowercase, strip punctuation, remove stopwords
        words = re.findall(r'\b[a-z]{4,}\b', text.lower())
        stopwords = {'this', 'that', 'with', 'from', 'have', 'been', ...}
        # Use bigrams for better semantic signal
        unigrams = {w for w in words if w not in stopwords}
        bigrams = {f"{words[i]}_{words[i+1]}" for i in range(len(words)-1)}
        return unigrams | bigrams
```

**Why this works without embeddings:** We're not asking "are these ideas semantically similar?" (that needs embeddings). We're asking "is the conversation introducing new vocabulary and concepts?" That's a vocabulary diversity question, and token overlap answers it well. Bigrams catch repeated phrases like "user_experience" or "morning_brief" being rehashed.

**When it runs:** After every turn, same post-turn hook as convergence monitoring.

**Intervention -- escalating:**

| Novelty Score | Consecutive Stale Turns | Intervention |
|--------------|------------------------|-------------|
| < 0.55 | 1 | No action (one repetitive turn is normal) |
| < 0.55 | 2 | Inject domain pivot: "[System: The conversation is recycling ideas. Bring in a perspective from {random domain from agent's affinities} that hasn't been discussed.]" |
| < 0.55 | 3+ | Inject hard redirect + uncomfortable idea trigger simultaneously |

The escalation matters. One stale turn is fine -- the agent might be building on something. Three stale turns means the well is dry and the conversation needs a shock.

---

#### 8. Surprise Audits -- AUDIT CALL (Tier 3)

This is the one mechanism that genuinely needs an LLM call. Python can detect repetition and agreement, but it can't judge whether ideas are *predictable*. An idea can be novel vocabulary-wise but still be the obvious, boring answer.

**Who runs it:** The orchestrator, not a background agent. A synchronous `claude -p` call with a focused audit prompt.

**When:** Every N cross-team turns (not every agent turn -- that's too expensive). Default: every 8 turns, configurable via YAML. Also triggered on phase transitions.

**The audit prompt:**

```
You are a conversation quality auditor. Review these recent turns from a 
multi-agent product discussion.

Rate each turn 1-5 on SURPRISE -- how unexpected, non-obvious, or 
perspective-shifting was the contribution? 

Score 1 = completely predictable, any competent person would say this
Score 3 = reasonable but expected for this role  
Score 5 = genuinely surprising, reframes the problem

Also identify: which agent has been most predictable over this window?
Which topics are being circled without progress?

Return JSON:
{
  "turn_scores": [{"agent": "...", "score": N, "reason": "..."}],
  "most_predictable_agent": "...",
  "stuck_topics": ["..."],
  "suggested_intervention": "..."
}
```

**What happens when it triggers:** The orchestrator reads the JSON response. If average surprise < 2.5, or if any agent scores 1 for 3+ consecutive audits:

1. The `suggested_intervention` is injected as a system message to the most predictable agent
2. If a specific agent is chronically predictable, their next prompt gets an escalated push: "[System: Your recent contributions have been predictable for your role. Surprise us. What would a {random alternative role} say about this that would make you uncomfortable?]"
3. If `stuck_topics` are identified, those topics get flagged in every agent's next prompt: "[System: The following topics have been discussed without progress: {topics}. Either advance them concretely or abandon them and explore something new.]"

**Cost control:** At 8-turn intervals in a 100-turn conversation, that's ~12 audit calls. Each is a short prompt with maybe 2000 tokens of context. Manageable.

---

#### 9. Silence-as-Signal -- PARSE-AND-INJECT

**Detection:** Pure Python. An agent "goes silent" when:

```python
def detect_silence(self, response: str, agent_config: AgentConfig) -> SilenceType:
    stripped = response.strip()
    
    # Explicit deferral
    deferral_patterns = [
        "nothing to add", "i'll pass", "no comment",
        "i defer", "moving on", "agreed without addition"
    ]
    if any(p in stripped.lower() for p in deferral_patterns):
        return SilenceType.EXPLICIT_DEFERRAL
    
    # Minimal response (< 50 words when agent usually produces 150+)
    word_count = len(stripped.split())
    if word_count < 50:
        return SilenceType.MINIMAL_RESPONSE
    
    # Parrot response (high overlap with immediately previous turn)
    # Reuse novelty scorer
    if self.novelty_scorer.pairwise_similarity(response, previous_response) > 0.7:
        return SilenceType.PARROTING
    
    return SilenceType.ACTIVE
```

**What it means depends on context:**

| Silence Type | In Brainstorm Phase | In Refine Phase | In Review Phase |
|-------------|-------------------|----------------|----------------|
| Explicit deferral | Bad -- agent disengaged, redirect | OK -- not every agent speaks to every point | Bad -- everyone should review |
| Minimal response | Check if agent's domain is relevant | Normal | Flag -- lazy review |
| Parroting | Convergence signal (feed to convergence monitor) | Convergence signal | Acceptable for confirmation |

**Intervention:** Context-dependent injection. In brainstorm, a silent agent gets: "[System: Your perspective ({agent's role}) hasn't been heard on this topic. What does your expertise see that others are missing?]" In refine, silence is respected.

---

#### 10. Post-hoc Diversity Checks -- AUDIT CALL (Tier 3)

**When:** At phase boundaries only (not per-turn). When brainstorm is about to transition to refine, run the diversity check.

**The audit prompt:**

```
You are evaluating the output diversity of a brainstorming session.

Here are all ideas generated:
{extracted ideas list}

Rate diversity on these dimensions (1-5 each):
- Topic spread: Are ideas clustered in one area or spread across the problem space?
- Stakeholder coverage: Do ideas address different user types and needs?
- Risk spectrum: Mix of safe bets and bold swings?
- Time horizon: Short-term and long-term thinking represented?
- Domain variety: Ideas drawing from different fields/analogies?

If any dimension scores below 3, suggest a specific prompt to inject 
that would fill the gap. Return JSON.
```

**Intervention:** If diversity is below threshold, the phase transition is *blocked*. The orchestrator injects the audit's suggested prompts and runs 2-3 more brainstorm turns targeting the gaps. Then re-checks.

This is the only mechanism that gates phase transitions. Everything else intervenes within the current flow.

---

### Putting It Together: The Post-Turn Hook

Here's how this integrates into the existing orchestrator loop:

```python
# In multi_agent.py, after each agent response:

def post_turn_hook(
    response: str, 
    agent_config: AgentConfig,
    turn_number: int,
    convergence_monitor: ConvergenceMonitor,
    novelty_scorer: NoveltyScorer,
    silence_detector: SilenceDetector,
    audit_interval: int = 8
) -> list[str]:
    """Returns list of system messages to inject into next turn."""
    interventions = []
    
    # Tier 2: Parse-and-inject (runs every turn, ~0ms cost)
    
    # Convergence
    agreement_score = convergence_monitor.score_turn(response, agent_config)
    convergence_msg = convergence_monitor.get_intervention()
    if convergence_msg:
        interventions.append(convergence_msg)
    
    # Novelty
    novelty = novelty_scorer.score_novelty(response)
    novelty_msg = novelty_scorer.get_intervention()
    if novelty_msg:
        interventions.append(novelty_msg)
    
    # Silence
    silence_type = silence_detector.detect_silence(response, agent_config)
    silence_msg = silence_detector.get_intervention(silence_type, current_phase)
    if silence_msg:
        interventions.append(silence_msg)
    
    # Existing: uncomfortable idea quota
    if conversation.should_trigger_uncomfortable_idea():
        interventions.append(UNCOMFORTABLE_IDEA_MESSAGE)
    
    # Tier 3: Audit call (runs every N turns, ~1 LLM call cost)
    if turn_number % audit_interval == 0 and turn_number > 0:
        audit_result = run_surprise_audit(recent_turns)
        interventions.extend(audit_result.interventions)
    
    # Cap interventions -- don't overwhelm the agent
    # Max 2 system injections per turn, prioritize by severity
    return sorted(interventions, key=lambda i: i.severity, reverse=True)[:2]
```

**The cap matters.** If convergence, low novelty, AND silence all trigger at once, the agent gets three contradictory system messages and produces garbage. Pick the two most important, drop the rest.

---

### Architecture Summary

| # | Mechanism | Tier | Detection | Intervention | Frequency |
|---|-----------|------|-----------|-------------|-----------|
| 1 | Agreement Tax | Prompt | N/A -- agent self-enforces | N/A | Every turn (baked in) |
| 2 | Convergence Suppression | Parse-and-inject | Agreement phrase counting + position drift + response brevity | System message: "attack the weakest assumption" | Every turn (check), triggers on rolling avg |
| 3 | Devil's Advocate | Prompt | N/A | N/A | Every turn (baked in) |
| 4 | Novelty Scoring | Parse-and-inject | Token/bigram Jaccard overlap with recent turns | Escalating: nothing -> domain pivot -> hard redirect | Every turn (check), triggers on consecutive staleness |
| 5 | Perspective Enforcement | Prompt | N/A | N/A | Every turn (reminder already fires) |
| 6 | Uncomfortable Ideas | Prompt + inject | Turn counter | System message: "introduce contrarian idea" | Every N turns (configurable) |
| 7 | Domain Pivots | Prompt (upgradeable) | Could link to novelty staleness | System message with random domain from affinities | On novelty staleness trigger |
| 8 | Surprise Audits | Audit call | LLM evaluates predictability | Targeted prompts to most predictable agent + stuck topic flags | Every 8 turns |
| 9 | Silence-as-Signal | Parse-and-inject | Response length + deferral phrases + parroting detection | Phase-context-dependent redirect | Every turn (check) |
| 10 | Post-hoc Diversity | Audit call | LLM evaluates idea spread across 5 dimensions | Block phase transition + targeted gap-filling prompts | Phase boundaries only |

---

### The Jobs-to-Be-Done Take

The user's job isn't "run anti-slop mechanisms." The job is **wake up to a conversation that actually explored the problem space**, not one where three polite LLMs agreed with each other for 8 hours.

That means the mechanisms that matter most are **convergence suppression** and **post-hoc diversity** -- they're the ones that directly protect the output the user reads in the morning. Novelty scoring and surprise audits are supporting infrastructure. Silence-as-signal is a nice diagnostic but rarely changes outcomes.

If you're prioritizing implementation order: convergence monitor first (biggest bang, zero cost), post-hoc diversity check second (gates the phase transition -- the last line of defense), novelty scoring third (cheap and catches what convergence misses). Surprise audits last -- they're the most expensive and the hardest to tune.


---

## The Systems Pragmatist (infrastructure realist)

Good. Now I have the full picture. Here's the enforcement architecture analysis.

---

## Anti-Slop Enforcement Architecture: What's Real, What's Wishful

### Current State

Tier 1 (prompt-only) is partially implemented. Tiers 2 and 3 are fully designed on paper, zero lines of runtime code. That's the gap you're asking about. Let me be concrete about what each runtime mechanism actually requires.

---

### Tier Classification: Honest Assessment

| Mechanism | Enforcement Type | Runtime Cost | Implementation Complexity |
|---|---|---|---|
| Perspective Enforcement | Prompt-only | Zero | Done (system prompt) |
| Agreement Tax | Prompt-only | Zero | Done (system prompt) |
| Specificity Mandate | Prompt-only | Zero | Done (system prompt) |
| Dissent Framing | Prompt-only | Zero | Done (system prompt) |
| Convergence Suppression | Orchestrator-inline | Low | Medium |
| Repetition Detection | Orchestrator-inline | Low | Medium |
| Uncomfortable Idea Quota | Orchestrator-inline | Zero | Low (trigger exists) |
| Staleness Circuit Breaker | Orchestrator-inline | Zero | Low |
| Novelty Scoring | Background LLM call | Medium | High |
| Surprise Audits | Background LLM call | Medium | High |
| Position Drift Tracking | Background LLM call | Medium | High |

---

### Tier 2: Orchestrator-Inline Detection (The Feasible Ones)

These run in the orchestrator's turn loop, between receiving a response and sending the next prompt. No extra API calls. No embeddings. Pure Python string processing.

#### Convergence Suppression

**Who runs it:** The orchestrator, after every cross-team message.

**Detection method:** Lexical signal ratio over a sliding window.

```
AGREEMENT_SIGNALS = ["i agree", "great point", "absolutely", "exactly right",
                     "building on that", "that aligns with", "we're aligned"]
DISAGREEMENT_SIGNALS = ["but consider", "i'd push back", "the risk is",
                        "i'm not convinced", "what about", "the problem with"]
```

Count occurrences in the last 4 cross-team exchanges. Compute `agreement_ratio = agree_count / (agree_count + disagree_count)`. If ratio > 0.7, trigger.

**What happens when it triggers:**

1. **First trigger (soft):** Inject a system-level instruction into the next agent's prompt: `"[Orchestrator note: The discussion is converging quickly. Before proceeding, identify the strongest argument AGAINST the current direction and explore it seriously.]"`
2. **Second consecutive trigger (hard):** Override one agent's role for that turn to explicit devil's advocate: `"[Orchestrator note: For this response, your primary job is to stress-test the emerging consensus. Find the failure modes.]"`
3. **Third consecutive trigger (escalation):** Log a warning and inject a constraint bomb -- a specific challenging scenario the agents must address before moving on.

**Why this works without embeddings:** You're not measuring semantic similarity. You're measuring conversational posture. Agreement language is remarkably consistent and detectable with string matching. It's a blunt instrument, but false positives (injecting pushback when it's not needed) are cheaper than false negatives (letting groupthink run).

**What it can't catch:** Agents that agree substantively while using neutral language. That's what Tier 3 novelty scoring is for.

#### Repetition Detection

**Who runs it:** Orchestrator, same turn loop.

**Detection method:** N-gram Jaccard similarity.

```python
def concept_overlap(text_a: str, text_b: str, n: int = 3) -> float:
    ngrams_a = set(zip(*[text_a.split()[i:] for i in range(n)]))
    ngrams_b = set(zip(*[text_b.split()[i:] for i in range(n)]))
    if not ngrams_a or not ngrams_b:
        return 0.0
    return len(ngrams_a & ngrams_b) / len(ngrams_a | ngrams_b)
```

Compare current response against the last 2 responses from the same team. Threshold: >0.4 overlap.

**Intervention:** `"[Orchestrator note: Your last response covered similar ground to your previous turn. Bring a new angle, a new risk, or a concrete example that hasn't been discussed.]"`

**Limitation:** N-gram overlap is noisy. Agents that rephrase the same idea in different words will slip through. Agents that reuse structural phrases ("Let me address three concerns...") will false-positive. Tuning the threshold matters, and 0.4 is a starting guess that needs empirical adjustment.

#### Staleness Circuit Breaker

**Who runs it:** Orchestrator, checked at phase boundaries.

**Detection:** Pure heuristic. If a phase exceeds 2x its expected turn count without producing an artifact (checked by MCP artifact channel), force a transition.

**Intervention:** Either inject a decision-forcing prompt (`"[Orchestrator: This phase has exceeded its turn budget. Produce your current best position as a concrete deliverable within 2 turns or the phase will advance.]"`) or auto-advance the phase.

**This one's straightforward.** Turn counter + artifact check. No NLP needed.

---

### Tier 3: Background Audit Agents (The Expensive Ones)

These require additional LLM calls. The design says Haiku for cost efficiency. They run asynchronously -- they don't block the conversation, they modulate thresholds for Tier 2.

#### Novelty Scoring

**Who runs it:** A background Haiku call, triggered every 4 cross-team exchanges.

**What it does:** Sends the last 4 exchanges to Haiku with a rubric prompt:

```
Rate each response 1-5 on novelty:
5 = Introduces genuinely new framing, risk, or solution approach
3 = Builds incrementally on existing thread
1 = Restates or agrees with previous content

Then classify the trajectory: expanding / stable / contracting
```

**What happens with the result:**
- `expanding` -> No action, lower convergence suppression sensitivity
- `stable` -> No action
- `contracting` -> Tighten convergence threshold (0.7 -> 0.5), inject a "change the lens" prompt on next turn

**The honest problem:** You're using an LLM to judge another LLM's output for originality. Haiku will be generous. The rubric needs to be adversarial: "If you can summarize this response as 'agrees and adds detail,' score it 2 or below." Even then, calibration will drift. Plan to log scores and review them manually for the first several sessions.

**Why not embeddings:** Cosine similarity between sentence embeddings would be more principled for measuring semantic novelty. But it requires infrastructure (embedding model, vector store, similarity computation). The Haiku judge is a pragmatic substitute -- worse at fine-grained similarity, better at detecting qualitative shifts in framing. For a v1 that needs to work tomorrow, it's the right call. Flag it as a known limitation.

#### Surprise Audits

**Who runs it:** Background Haiku call, ~15% probability per exchange (random trigger).

**What it evaluates:** A rotating dimension, randomly selected:
- "Are agents performing disagreement or genuinely pushing back?"
- "Is the conversation exploring the problem space or prematurely converging on solutions?"
- "Are agents using their specific expertise or defaulting to generic analysis?"

**Intervention:** Results don't directly inject anything. They adjust Tier 2 thresholds and get logged. If an audit finds performed disagreement, convergence suppression threshold drops for the next cycle.

**Why random:** Prevents agents from gaming a predictable schedule. Though honestly, current LLMs aren't sophisticated enough to game audit timing. The randomness is more about sampling efficiency -- you don't need to audit every turn, and random sampling gives you coverage without the cost.

#### Position Drift Tracking

**Who runs it:** Background Haiku call every 6 cross-team exchanges.

**What it does:** Extracts each team's stance on 3-5 core questions defined at session start. Maps stances to a spectrum: `strongly_against -> leaning_against -> neutral -> leaning_for -> strongly_for`.

**Detection:** If both teams drift toward the same position (converge from opposite starting points), flag it.

**Intervention:** Inject the original opposing positions back into the conversation: `"[Orchestrator: Team A originally held that X was a critical risk. That concern appears to have been dropped without resolution. Address it directly.]"`

**The real challenge:** Stance extraction is hard. Haiku needs to parse nuanced positions from multi-paragraph responses. Expect noisy results. Consider having the agents self-report their positions (as part of the AgentMind `<mind>` blocks in the design) rather than relying on external extraction.

---

### Integration: The Turn Pipeline

```
Agent Response Received
        |
        v
[Tier 2: Inline Checks]  -----> Max 1 injection per turn
  |  Convergence check          Priority: convergence > staleness > repetition
  |  Repetition check
  |  Staleness check
        |
        v
[Injection Decision]
  |  Append to next prompt if triggered
        |
        v
[Tier 3: Async Dispatch]  -----> Non-blocking
  |  If turn_count % 4 == 0: novelty scoring
  |  If random() < 0.15: surprise audit
  |  If turn_count % 6 == 0: position drift
        |
        v
[Threshold Modulation]
  |  Tier 3 results adjust Tier 2 thresholds for next cycle
        |
        v
Send Next Prompt (with any injections)
```

Key constraint: **max one injection per turn.** Stacking multiple orchestrator notes makes them ignorable. Priority order ensures the most impactful intervention wins.

---

### What I'd Actually Build First

Forget Tier 3 for now. Here's the minimum viable anti-slop stack:

1. **Tier 1 prompt rules** -- already in place
2. **Convergence suppression** -- 50 lines of Python, highest impact
3. **Staleness circuit breaker** -- 20 lines, prevents runaway phases
4. **Repetition detection** -- 30 lines, catches the obvious loops

That covers the 80% case. Tier 3 background agents are a refinement you add after you've run sessions and seen what Tier 2 misses. Running Haiku judges on every session from day one is spending money to collect data you don't know how to interpret yet.

The prompt-only mechanisms are doing more work than you'd think. Agreement tax in particular -- forcing agents to name two risks before endorsing -- is surprisingly effective at slowing convergence. It's not foolproof (agents can name perfunctory risks), but it raises the floor.

The real failure mode isn't that any single mechanism fails. It's that you build all 10, they generate a flood of signals and injections, and the conversation becomes incoherent because the orchestrator is constantly interrupting. The max-one-injection-per-turn rule is critical. So is starting with Tier 2 only and adding Tier 3 when you have empirical evidence of what Tier 2 misses.


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


---

## The Product Oracle (user advocate and product strategist)

Good question. The Cognitive Architect laid out the three-layer architecture -- extraction, evaluation, orchestrator decision engine -- and it's mechanically sound. But I want to pull on threads that the mechanism doesn't answer yet, because the person who kicks off this overnight run and reads the morning brief has a job to be done, and that job isn't "watch a state machine execute cleanly."

---

## The Gate Evaluation Mechanism Is Correct. The Gate *Criteria* Are Wrong.

The three-layer design works:
- **Layer 1** (structured extraction) builds the instrument panel continuously
- **Layer 2** (evaluator prompt) makes semantic judgments periodically  
- **Layer 3** (orchestrator) applies mechanical rules and timeout overrides

I'm not going to redesign that. It's the right shape. But there are four problems hiding inside it that will bite us overnight when nobody's watching.

### Problem 1: "50 ideas" is a vanity metric

The person running this doesn't wake up wanting 50 ideas. They want *coverage of the problem space they care about*. Fifty fintech variations and three sustainability afterthoughts technically pass the gate but fail the job.

The extraction prompt counts ideas. The evaluator prompt checks diversity. But diversity is measured against a static domain list. What the user actually needs is **coverage relative to their input brief**. If someone seeds the system with "I want to explore AI tools for small law firms," domain diversity across fintech and agriculture is noise.

**Fix:** The gate criteria should be parameterized by the idea brief. The evaluator prompt needs:

```python
GATE_CRITERIA["brainstorm"] = {
    "idea_count": 50,
    "domain_diversity": 6,
    "brief_coverage": {
        "enabled": True,
        "prompt": """Does the idea pool adequately explore the problem 
        space defined in the original brief? Are there obvious angles 
        the teams haven't touched?""",
        "weight": "primary"  # This matters more than raw count
    }
}
```

If the brief says "AI for small law firms," then 25 deeply varied ideas about legal workflows, client intake, document review, billing, compliance, and court prep is *better* than 50 ideas scattered across irrelevant domains. The evaluator needs the brief as context to judge quality.

### Problem 2: The extraction layer's deduplication is doing quiet, dangerous work

The accumulator deduplicates ideas "by semantic similarity." That's a one-line comment hiding an entire design decision. If the similarity threshold is too aggressive, 50 genuinely different ideas collapse to 30 and the gate never fires. Too loose, and "Uber for laundry" and "on-demand laundry pickup" both count, inflating the number.

This isn't a background concern. This is the *primary mechanism* that determines whether the phase progresses. And it's running on every message.

**Fix:** The deduplication should be part of the evaluator's job, not the extraction layer's. Layer 1 extracts liberally (duplicates are fine -- it's an instrument panel, not a ledger). Layer 2, when the gate check fires, gets the raw list and is asked: "How many of these are genuinely distinct ideas?" That way the semantic judgment happens in the evaluator prompt where it belongs, not in a similarity function that nobody's watching.

```python
@dataclass
class PhaseAccumulator:
    ideas_raw: list[str]          # everything extracted, duplicates included
    ideas_deduplicated: int = 0   # set only by evaluator, not by extraction
    domains_raw: list[str]
    domains_validated: int = 0    # same -- evaluator confirms
```

### Problem 3: The timeout override is too gentle

The design says: if criteria are <70% met at timeout, force transition with a quality flag and tell Refine to spend its first two exchanges backfilling.

But think about the user's morning. They see a `quality_flag: "degraded"` in the session metadata. What does that mean to them? Is the output salvageable? Should they rerun? Was it a bad seed idea, or did the agents just get stuck?

The timeout needs to produce a **decision for the user**, not just a flag:

```python
def handle_timeout(self, phase, eval_result):
    deficit = eval_result.deficiencies
    ratio = self.criteria_completion_ratio(phase)
    
    if ratio > 0.7:
        return TransitionAction(
            to_phase=phase.next,
            carry_forward=deficit,
            user_signal="PARTIAL",
            user_note="Brainstorm hit 70%+ of targets. Refine phase will compensate."
        )
    elif ratio > 0.4:
        return TransitionAction(
            to_phase=phase.next,
            carry_forward=deficit,
            user_signal="WEAK",
            user_note="Brainstorm underperformed. Consider: was the seed brief too narrow? "
                      "Output will be shallow in domains X, Y."
        )
    else:
        # Below 40% -- something is structurally wrong
        return TransitionAction(
            to_phase=phase.next,
            carry_forward=deficit,
            user_signal="FAILED",
            user_note="Brainstorm failed to produce meaningful output. "
                      "Likely causes: brief too vague, agents stuck in loops, "
                      "or anti-slop rules too aggressive. Recommend rerun with adjusted config."
        )
```

These signals feed into the morning brief. The user doesn't parse JSON metadata -- they read a summary that says "this run had problems and here's what to try."

### Problem 4: The transition communication is one-directional but should be bidirectional for one turn

The design says agents are "told, not asked." Correct -- they don't vote. But the facilitator message announces the transition *and* immediately sets new rules. There's no acknowledgment beat.

Why this matters: the agents' context windows now contain the entire brainstorm phase. When the system prompt swaps to Refine, the agents need to *reorient*. If the very next turn after the facilitator message is a cross-team exchange, the responding team has to simultaneously process the phase change, absorb the new rules, and produce a substantive refine-mode response. That's a lot of cognitive load in one prompt.

**Fix:** After the transition message, the first action should be a **one-turn internal deliberation** for each team. Not cross-team. Each team gets one internal round to:
1. Acknowledge the phase change
2. Review the idea list from their perspective
3. Decide their opening strategy for Refine

```python
TRANSITION_PROTOCOL = {
    "facilitator_message": True,       # announce transition
    "system_prompt_swap": True,        # inject new phase rules
    "reorientation_round": {
        "type": "internal_deliberation",
        "turns": 1,
        "prompt": "Review the brainstorm output. What's your team's strategy "
                  "for the Refine phase? Which ideas do you want to champion, "
                  "which will you challenge first?"
    },
    "then": "resume_cross_team"        # normal turn sequencing resumes
}
```

This costs one internal turn per team. It prevents the first Refine exchange from being disoriented.

---

## What I'd Add to the Design

The mechanism is sound. These are the additions:

| Addition | Why | Cost |
|---|---|---|
| Brief-relative gate criteria | Raw counts don't serve the user's actual need | One more field in evaluator prompt |
| Deduplication in evaluator, not extraction | Avoids silent count errors in the hot path | Slight increase in evaluator prompt size |
| Tiered timeout signals (PARTIAL/WEAK/FAILED) | User needs actionable morning brief, not flags | Trivial orchestrator logic |
| Reorientation round after transition | Prevents disoriented first-response in new phase | One internal turn per team |

The orchestrator doesn't need to understand content. But it does need to understand *whether the content served the user's job*. That's the gap between a phase machine that runs and a phase machine that produces something worth reading in the morning.


---

## The Systems Pragmatist (infrastructure realist)

Right. So the design documents describe a three-layer evaluation system, but nothing is built. The entire phase mechanism is aspirational. Let me walk through this honestly and design something that will actually work at 3 AM with no one watching.

---

## The Core Problem

The exit gate says "50+ ideas with domain diversity." But agent output looks like this:

```
I think we should consider a subscription model, or perhaps a freemium approach
where users get basic features free. Also worth exploring: marketplace dynamics,
two-sided platforms like what Uber did, and maybe some kind of token economy...
```

How many ideas is that? Three? Five? One with variations? The orchestrator is Python driving CLI subprocesses -- it doesn't "understand" anything. It sees strings.

**You cannot count ideas without an LLM. Period.** Regex won't cut it, n-gram overlap won't cut it, bullet-point counting won't cut it. Agents don't write structured lists unless you force them to, and forcing structured output kills the deliberation quality.

---

## The Design: Three Components

### 1. Structured Extraction (Runs After Every Cross-Team Exchange)

A cheap, fast Haiku call that runs on each message. Not the agents themselves -- a **separate extraction prompt** that the orchestrator fires as a side-channel.

```python
@dataclass
class PhaseAccumulator:
    """Running tallies maintained across the phase."""
    ideas: dict[str, IdeaRecord]    # keyed by normalized slug
    domains_seen: set[str]          # e.g., {"pricing", "distribution", "ux", "trust"}
    challenge_count: int            # times an idea was explicitly pushed back on
    exchange_count: int             # cross-team message pairs
    phase_start: datetime
    last_extraction: datetime
    nudge_count: int                # how many times we've injected "you're short on X"
```

The extraction prompt:

```
You are a structured data extractor. Given this agent message from a brainstorming
session, extract:

1. NEW IDEAS: Ideas not already in the running list below. An "idea" is a distinct
   actionable concept -- not a rephrasing, not a sub-point of an existing idea.
   When uncertain, bias toward splitting (we deduplicate later).

2. DOMAIN TAGS: For each idea, which domain(s) does it touch?
   Valid domains: [pricing, distribution, ux, trust, technical, legal, marketing,
   operations, partnerships, data, community, content, monetization, growth]

3. CHALLENGES: Did this message challenge, question, or push back on any
   existing idea? List which ones.

Existing idea list:
{accumulated_ideas_json}

Agent message:
{message_text}

Respond in JSON only. Schema: {extraction_schema}
```

**Why this works:** Haiku is fast (~200ms), cheap, and good enough at structured extraction. It doesn't need to be perfect -- it's accumulating signal, not making decisions. False positives (overcounting) are corrected at gate evaluation. False negatives wash out over multiple exchanges.

**Why not make the agents self-report idea counts:** Because agents are optimized for deliberation quality, not bookkeeping. Asking them to maintain structured inventories changes their behavior. Separation of concerns.

### 2. Gate Evaluator (Fires Periodically, Not Continuously)

**Trigger conditions** (whichever hits first):
- Every 6 cross-team exchanges
- Every 15 minutes of wall-clock time
- When the accumulator crosses 80% of any numeric threshold

The gate evaluator is a **Sonnet call** (not Haiku -- this decision matters) with the full accumulator state:

```
You are evaluating whether a Brainstorm phase should transition to Refine.

EXIT CRITERIA:
- 50+ distinct ideas (not rephrasings or sub-points of the same concept)
- Domain diversity: ideas span at least 6 of 14 possible domains
- No single domain contains more than 40% of all ideas

CURRENT STATE:
- Extracted idea count: {len(accumulator.ideas)}
- Unique domains: {len(accumulator.domains_seen)} — {accumulator.domains_seen}
- Domain distribution: {domain_histogram}
- Exchange count: {accumulator.exchange_count}
- Phase duration: {elapsed_time}

IMPORTANT: The extraction pipeline may have over-counted or under-counted.
Review the raw idea list below and give your ADJUSTED counts.

{full_idea_list_with_descriptions}

Respond with:
- adjusted_idea_count: int
- adjusted_domain_count: int
- max_domain_concentration: float (0-1)
- gate_met: bool
- confidence: HIGH | MEDIUM | LOW
- deficiencies: list[str]  # what's missing if gate not met
- recommendation: TRANSITION | NUDGE | CONTINUE
```

**Why Sonnet, not Haiku:** The gate evaluator needs judgment. "Is idea #23 actually distinct from idea #7?" requires reasoning Haiku can't reliably do. This call happens infrequently (every 6 exchanges, maybe 8-10 times per phase), so the cost is negligible.

**Why not the agents themselves:** Same reason as extraction -- the evaluator needs to be dispassionate. Agents have positions and momentum. An agent who's been championing an idea will count its variations as distinct.

### 3. Transition Decision (Orchestrator Mechanical Rules -- No LLM)

This is pure Python. No ambiguity, no judgment calls.

```python
class TransitionEngine:
    """Mechanical rules. No LLM in this layer."""

    # Time budgets per phase (wall-clock)
    TIME_BUDGET = {
        "brainstorm": timedelta(hours=2),
        "refine": timedelta(hours=3),
        "specify": timedelta(hours=2),
        "review": timedelta(hours=1),
    }

    # Maximum exchanges before forced evaluation
    MAX_EXCHANGES = {
        "brainstorm": 40,
        "refine": 60,
        "specify": 40,
        "review": 20,
    }

    def evaluate_transition(self, phase: str, gate_result: GateResult,
                           accumulator: PhaseAccumulator) -> TransitionAction:
        elapsed = datetime.now() - accumulator.phase_start
        budget = self.TIME_BUDGET[phase]
        budget_pct = elapsed / budget

        # Path 1: Clean transition
        if gate_result.gate_met and gate_result.confidence == "HIGH":
            return TransitionAction.PROCEED

        # Path 2: Gate met but evaluator uncertain -- require confirmation
        if gate_result.gate_met and gate_result.confidence in ("MEDIUM", "LOW"):
            if accumulator.consecutive_gate_met >= 2:
                return TransitionAction.PROCEED
            return TransitionAction.RECHECK  # evaluate again in 3 exchanges

        # Path 3: Not met, but time is running out
        if budget_pct >= 0.85:
            return TransitionAction.ESCALATE_NUDGE  # aggressive prompt injection
        if budget_pct >= 1.0:
            return TransitionAction.FORCE_TRANSITION  # escape valve

        # Path 4: Not met, exchange cap hit
        if accumulator.exchange_count >= self.MAX_EXCHANGES[phase]:
            return TransitionAction.FORCE_TRANSITION

        # Path 5: Not met, time remains
        if gate_result.deficiencies:
            return TransitionAction.TARGETED_NUDGE  # inject specific gap info
        return TransitionAction.CONTINUE
```

**The escape valve is non-negotiable.** If Brainstorm has been running for 2 hours and only has 35 ideas, you do not let it run for 4 more hours hoping to hit 50. You transition with what you have and log the shortfall. The whole session has a time budget. A phase that overruns steals from downstream phases, and Review (the most important phase for output quality) gets squeezed.

**What FORCE_TRANSITION logs:**

```json
{
    "event": "forced_phase_transition",
    "phase": "brainstorm",
    "reason": "time_budget_exceeded",
    "criteria_met": {"idea_count": 35, "target": 50, "pct": 0.70},
    "domain_diversity": {"count": 5, "target": 6},
    "elapsed_minutes": 122,
    "decision": "Proceeding with 70% criteria. Refine phase will receive deficit notification."
}
```

---

## The Concrete Brainstorm-to-Refine Walkthrough

**T+0:00** -- Phase starts. Orchestrator sends opening system prompts to both teams with brainstorm-phase instructions. `PhaseAccumulator` initialized empty.

**T+0:00 to T+1:30** -- Normal operation. Each cross-team exchange:
1. Team A responds
2. Orchestrator fires Haiku extraction on Team A's message → updates accumulator
3. Message routed through MCP to Team B
4. Team B responds
5. Orchestrator fires Haiku extraction on Team B's message → updates accumulator
6. Every 6th exchange pair: fire Sonnet gate evaluator

**T+0:45** -- Gate evaluation #1. Result: 22 ideas, 4 domains. `CONTINUE`.

**T+1:15** -- Gate evaluation #3. Result: 41 ideas, 5 domains. Deficiency: "Only 5 domains covered, need 6. No ideas in legal, partnerships, or data domains." Action: `TARGETED_NUDGE`.

**The nudge** -- Orchestrator injects into the next system prompt addendum for both teams:

```
[FACILITATOR NOTE: The discussion has generated strong ideas across pricing,
distribution, UX, trust, and technical domains. Consider whether there are
unexplored angles in areas like legal/regulatory, partnerships, or data strategy.]
```

This is **not** a new agent message. It's injected into the next turn's system prompt as a facilitator note. The agents see it as meta-context, not as another participant talking.

**T+1:40** -- Gate evaluation #4. Result: 48 ideas, 7 domains. Gate evaluator says `gate_met: true, confidence: MEDIUM` (borderline on idea count after dedup). Action: `RECHECK` -- accumulator marks `consecutive_gate_met = 1`.

**T+1:50** -- Gate evaluation #5 (triggered early at 3-exchange interval due to RECHECK). Result: 53 ideas, 7 domains, confidence HIGH. Action: `PROCEED`.

**T+1:50** -- Transition fires.

---

## What Changes Concretely at Transition

### Step 1: Phase Snapshot (Orchestrator writes to session directory)

```
sessions/{id}/phases/brainstorm/
  ├── accumulator.json       # Final idea list, domain map, metrics
  ├── gate_evaluations.json  # All gate eval results with timestamps
  ├── extraction_log.jsonl   # Every Haiku extraction result
  └── transition.json        # Why and how the transition fired
```

This is the phase's permanent record. Non-negotiable for debugging overnight runs.

### Step 2: Context Reset via Briefing

Here's the critical insight: **you cannot just swap system prompts and keep going.** After 40+ exchanges, the context window is polluted with brainstorm-mode thinking. Agents will keep brainstorming even if you tell them to refine.

The transition does a **hard context reset**:

1. Orchestrator generates a **Phase Briefing** (Sonnet call) that summarizes the brainstorm output into a structured handoff document:

```
BRAINSTORM PHASE SUMMARY
========================
Duration: 1h50m | Ideas generated: 53 | Domains covered: 7/14

TOP IDEAS BY TEAM SUPPORT:
1. [idea] — supported by Team A (Cognitive Architect), challenged once by Team B
2. [idea] — originated from Team B, expanded by both teams
...

DOMAIN DISTRIBUTION:
- Pricing: 12 ideas
- Distribution: 9 ideas
- UX: 8 ideas
...

UNRESOLVED TENSIONS:
- Team A favors marketplace approach; Team B skeptical of cold-start problem
- Disagreement on whether freemium cannibalizes premium
...

ENTERING REFINE PHASE: Your job is now to stress-test these ideas.
```

2. **Both team conversations are restarted from scratch** with new system prompts that include:
   - The Refine-phase persona instructions
   - The Phase Briefing as grounding context
   - Updated anti-slop weights (Refine phase cranks up the agreement tax, because the temptation to rubber-stamp brainstorm output is enormous)
   - The Refine-phase exit criteria (so agents know what "done" looks like)

### Step 3: Anti-Slop Weight Adjustment

Not all phases need the same enforcement. Concrete changes:

| Mechanism | Brainstorm | Refine | Specify | Review |
|---|---|---|---|---|
| Agreement tax | Medium | **High** | Medium | **Highest** |
| Uncomfortable idea quota | Every 8 turns | Every 12 turns | Off | Every 6 turns |
| Convergence suppression | Active | **Aggressive** | Relaxed | Active |
| Director provocation threshold | 3 idle turns | 2 idle turns | 4 idle turns | 2 idle turns |

These are parameters in the phase config, not code changes:

```yaml
# config/phases.yaml
refine:
  exit_criteria:
    challenge_coverage: 0.70    # 70% of top ideas must be challenged
    all_top_ideas_defended: true # ideas in top 15 must have explicit defense
  anti_slop:
    agreement_tax: high
    uncomfortable_idea_interval: 12
    convergence_suppression: aggressive
    director_idle_threshold: 2
  time_budget_minutes: 180
  max_exchanges: 60
```

### Step 4: Bench Rotation (If Implemented)

If the team has bench agents, transition is when rotation happens. The orchestrator checks which agents were most/least active in the previous phase and can swap. But this is secondary -- the core three mechanisms above (snapshot, context reset, weight adjustment) are what make transitions real.

---

## What This Design Deliberately Avoids

**No agent self-evaluation of gates.** Agents don't decide when they're done. They have incentives to declare victory early (or to keep going because they're enjoying the argument). The evaluator is external and dispassionate.

**No single point of LLM failure for transitions.** The gate evaluator can hallucinate or misjudge. That's why the transition engine is mechanical Python with escape valves. The LLM advises; the code decides.

**No complex NLP for idea extraction.** Tried-and-true approach: let an LLM do the extraction, accumulate imperfect signal, and let the gate evaluator reconcile. Fighting with regex to parse unstructured creative output is a losing battle.

**No infinite phase extension.** Every phase has a hard wall-clock cap. The system must produce output by morning. A phase that's "almost there" at 100% budget is done.

---

## Implementation Priority

If I'm building this, the order is:

1. **PhaseAccumulator + extraction prompt** -- without this, you're flying blind
2. **TransitionEngine with time-based escape valves** -- without this, phases run forever
3. **Context reset + Phase Briefing generation** -- without this, transitions are cosmetic
4. **Gate evaluator prompt** -- this can start simple and get refined
5. **Anti-slop weight parameterization per phase** -- important but not blocking

The extraction prompt and transition engine are a day of work. The context reset is the hard part -- getting the briefing quality right so agents don't lose critical context across the boundary. That's where you'll iterate.


---

# Question 8: What is AgentMind and how does it evolve during a session?

## The Cognitive Architect (creativity engine designer)

Good. Now I have the full picture -- the current codebase (static AgentConfig, no runtime state, naive prompt construction), plus the Oracle and Pragmatist's parallel designs from the batch run where I timed out. Let me give this the treatment it deserves.

---

## AgentMind: The Cognitive Architect's Design

The Oracle and Pragmatist both landed in the right neighborhood. Self-report is correct. Structured `<mind>` block is correct. Orchestrator-side corrections for decay and social effects are correct. I'm not going to relitigate those. Where I diverge is on three things they got wrong or missed entirely.

---

### Problem 1: Magnitude is doing too many jobs

Both designs treat magnitude as a single 0-1 float meaning "how strongly held." But conviction isn't one-dimensional. An agent can be highly certain an idea is correct but not care about it (low stakes). Or deeply emotionally attached to an idea they know is probably wrong (high stakes, low evidence). Or holding an idea tentatively because the evidence is strong but they haven't internalized it yet.

A single scalar conflates three distinct signals:

- **Conviction** -- how certain the agent is that this idea is correct
- **Investment** -- how much the agent's identity is tied to this idea (will they fight for it?)
- **Evidence weight** -- how much external support exists

Research on belief revision (Bayesian epistemology, if you want the fancy label) shows these diverge meaningfully. Someone can update their evidence assessment without changing their emotional investment. That lag between "I know this is probably wrong" and "I'm still defending it" is where the most interesting conversational dynamics live.

But three floats per idea is too much bookkeeping for an LLM to self-report reliably. The Pragmatist is right that token overhead matters.

**My resolution: magnitude stays as one float, but we add an `epistemic_status` enum.**

```python
class EpistemicStatus(str, Enum):
    """How the agent justifies their conviction."""
    HUNCH = "hunch"              # Intuition, no evidence yet
    ARGUED = "argued"            # Defended in conversation but no external evidence
    EVIDENCED = "evidenced"      # Supported by research or concrete examples
    CONTESTED = "contested"      # Has evidence but also faces strong counter-evidence
    CONSENSUS = "consensus"      # Multiple agents agree (possible groupthink signal)
```

This separates the "why" from the "how much" without adding a second continuous variable. The orchestrator can use it: a `HUNCH` at 0.8 magnitude is a stubbornness signal. An `EVIDENCED` idea at 0.4 magnitude means the agent hasn't internalized the evidence yet -- prompt them to engage with it.

---

### Problem 2: Ideas need genealogy, not just parent pointers

The Oracle's `parent_id: Optional[str]` captures one relationship: "this idea evolved from that one." But ideas in real brainstorms do more than linearly evolve. They merge ("your subscription model plus my API-first approach becomes an API marketplace"). They fork ("that idea works for enterprise but needs a different variant for solo builders"). They subsume ("this architecture decision makes three of our smaller ideas irrelevant").

A single `parent_id` can't represent a merge (two parents). And without explicit relationship tracking, the Morning Brief can't reconstruct how the team's thinking evolved -- which is half the value of running the system overnight.

```python
class IdeaRelation(str, Enum):
    EVOLVED_FROM = "evolved_from"    # Linear refinement
    MERGED_FROM = "merged_from"      # Combined two+ ideas
    FORKED_FROM = "forked_from"      # Variant of another idea
    SUBSUMES = "subsumes"            # Makes another idea redundant
    TENSION_WITH = "tension_with"    # Contradicts or competes with
```

And on the Idea model:

```python
class IdeaLink(BaseModel):
    target_id: str
    relation: IdeaRelation

class Idea(BaseModel):
    id: str
    summary: str
    magnitude: float = Field(0.5, ge=0.0, le=1.0)
    epistemic_status: EpistemicStatus = EpistemicStatus.HUNCH
    status: IdeaStatus = IdeaStatus.ACTIVE
    origin_turn: int
    last_touched_turn: int
    links: list[IdeaLink] = Field(default_factory=list)
    notes: str = ""
```

The agent self-reports links when they're aware of them. The orchestrator can also infer `TENSION_WITH` relationships by looking at which agents' top ideas conflict -- agents don't always notice their own contradictions.

Critically, the `<mind>` block keeps this lightweight. The agent only reports links when they're salient:

```yaml
ideas:
  - id: api-marketplace
    magnitude: 0.7
    epistemic: argued
    status: active
    links: [{target: api-first, relation: evolved_from}, {target: subscription-model, relation: merged_from}]
    notes: This finally synthesizes both threads
```

---

### Problem 3: The Oracle and Pragmatist disagree on what the agent sees -- and they're both half right

The Oracle says: show the agent natural language magnitude numbers like `[0.75] api-first-architecture`. The Pragmatist says: show natural language without raw numbers to avoid gaming ("high conviction" instead of 0.75).

The Oracle is right that precision helps continuity -- if the agent sees "high conviction" they might report anything from 0.6 to 0.9 next turn, introducing noise. The Pragmatist is right that showing raw numbers invites optimization games where the agent manages its numbers instead of thinking.

**My resolution: show the agent a curated natural-language view with ordinal anchors, not cardinal numbers.**

Instead of:
```
- [0.75] api-first-architecture
- [0.40] subscription-model
```

Or:
```
- api-first-architecture (high conviction)
- subscription-model (weakening)
```

Do:
```
Your strongest position: "api-first architecture" -- you've argued for this repeatedly
  and it's become central to your thinking.
Also holding: "subscription model" -- you find it interesting but haven't committed.
  It's fading without defense.
Tension: You haven't reconciled how api-first and the rapid-prototyping advocates'
  approach coexist.
```

This gives the agent enough continuity information to behave consistently without making magnitude a first-class concept in the agent's own reasoning. The agent never learns the number system. It just knows what it cares about and how much.

The `<mind>` block output still uses numbers -- that's the structured channel the orchestrator needs. But the input to the agent is narrative.

---

### The Full Schema

```python
"""AgentMind: runtime cognitive state for discussion agents."""

from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class IdeaStatus(str, Enum):
    ACTIVE = "active"
    PARKED = "parked"
    SUPERSEDED = "superseded"
    MERGED = "merged"
    DEAD = "dead"


class EpistemicStatus(str, Enum):
    HUNCH = "hunch"
    ARGUED = "argued"
    EVIDENCED = "evidenced"
    CONTESTED = "contested"
    CONSENSUS = "consensus"


class IdeaRelation(str, Enum):
    EVOLVED_FROM = "evolved_from"
    MERGED_FROM = "merged_from"
    FORKED_FROM = "forked_from"
    SUBSUMES = "subsumes"
    TENSION_WITH = "tension_with"


class MoodState(str, Enum):
    ENERGIZED = "energized"
    FRUSTRATED = "frustrated"
    SKEPTICAL = "skeptical"
    FOCUSED = "focused"
    DISENGAGED = "disengaged"
    CONFLICTED = "conflicted"


class IdeaLink(BaseModel):
    target_id: str
    relation: IdeaRelation


class Idea(BaseModel):
    id: str                                              # Slug: "api-marketplace"
    summary: str                                         # One line
    magnitude: float = Field(0.5, ge=0.0, le=1.0)       # Conviction strength
    epistemic_status: EpistemicStatus = EpistemicStatus.HUNCH
    status: IdeaStatus = IdeaStatus.ACTIVE
    origin_turn: int = 0
    last_touched_turn: int = 0
    links: list[IdeaLink] = Field(default_factory=list)  # Genealogy
    notes: str = ""                                      # Agent's private reasoning


class Concern(BaseModel):
    id: str
    summary: str
    severity: float = Field(0.5, ge=0.0, le=1.0)
    blocking: bool = False
    raised_turn: int = 0
    addressed: bool = False
    addressed_by: Optional[str] = None                   # Idea ID or agent name


class AgentMind(BaseModel):
    """Mutable runtime state. One per agent per session."""

    # Identity (set once from AgentConfig)
    agent_name: str
    session_id: str = ""

    # Ideas
    ideas: list[Idea] = Field(default_factory=list, max_length=7)  # Hard cap
    
    # Concerns
    concerns: list[Concern] = Field(default_factory=list)

    # Mood
    mood: MoodState = MoodState.FOCUSED
    mood_reason: str = ""

    # Focus and queue
    current_focus: Optional[str] = None       # Idea ID driving attention
    wants_to_say: str = ""                    # Queued thought not yet expressed
    
    # Social graph (emergent, not configured)
    aligns_with: list[str] = Field(default_factory=list)
    clashes_with: list[str] = Field(default_factory=list)

    # Orchestrator-managed fields (not self-reported)
    turn_number: int = 0
    stale_turns: int = 0                      # Turns since valid <mind> block
    phase: str = "brainstorm"
    magnitude_history: dict[str, list[float]] = Field(default_factory=dict)
    # ^^ idea_id -> [mag_turn_0, mag_turn_1, ...] for trajectory analysis


class AgentMemory(BaseModel):
    """Cross-session distillation. Written by Weaver at session end."""
    agent_name: str
    session_id: str
    high_conviction_ideas: list[str]          # magnitude >= 0.7 at session end
    unresolved_concerns: list[str]            # blocking=True, addressed=False
    recurring_tensions: list[str]             # Agent names they consistently clashed with
    session_summary: str                      # One paragraph, orchestrator-generated
```

---

### Magnitude Update Mechanics

**Who updates what:**

| Field | Updated by | Mechanism |
|---|---|---|
| `magnitude` (reported value) | Agent | Self-reported in `<mind>` block |
| `magnitude` (decay correction) | Orchestrator | Applied post-parse: -0.05/turn for ideas not mentioned in last 3 turns |
| `epistemic_status` | Agent | Self-reported |
| `status` | Agent | Self-reported (ACTIVE -> PARKED/DEAD/etc.) |
| `links` | Agent + Orchestrator | Agent reports known links; orchestrator infers TENSION_WITH |
| `origin_turn`, `last_touched_turn` | Orchestrator | Tracked from when ideas appear and when magnitude changes |
| `magnitude_history` | Orchestrator | Appended each turn after parsing |
| `stale_turns` | Orchestrator | Incremented on parse failure, reset on success |

**Personality modulation on magnitude dynamics:**

The static `PersonalityConfig` traits from `AgentConfig` don't just flavor prompts -- they parameterize how the orchestrator applies corrections:

```python
def apply_magnitude_corrections(mind: AgentMind, config: AgentConfig) -> None:
    """Orchestrator-side corrections after parsing self-report."""
    p = config.personality
    
    for idea in mind.ideas:
        if idea.status != IdeaStatus.ACTIVE:
            continue
            
        turns_silent = mind.turn_number - idea.last_touched_turn
        
        # Decay for ignored ideas, modulated by stubbornness
        if turns_silent >= 3:
            decay_rate = 0.05 * (1.0 - p.stubbornness * 0.5)  # Stubborn agents decay slower
            idea.magnitude = max(0.0, idea.magnitude - decay_rate)
        
        # High-creativity agents spawn ideas at lower initial magnitude
        # (already handled at creation time, not here)
        
        # Anti-groupthink: if epistemic_status is CONSENSUS, apply mild skepticism pressure
        if idea.epistemic_status == EpistemicStatus.CONSENSUS:
            idea.magnitude = min(idea.magnitude, 0.85)  # Soft ceiling on consensus ideas
        
        # Auto-park dead ideas
        if idea.magnitude < 0.1:
            idea.status = IdeaStatus.PARKED
```

**New idea defaults, modulated by personality:**

```python
def create_idea_defaults(config: AgentConfig) -> dict:
    """Starting magnitude depends on personality."""
    p = config.personality
    base_magnitude = 0.4 + (p.risk_tolerance * 0.2)  # Risk-tolerant agents commit faster
    if p.creativity_temp > 0.7:
        base_magnitude -= 0.1  # Creative agents throw out more ideas at lower conviction
    return {"magnitude": round(base_magnitude, 2)}
```

---

### Prompt Construction: The Three Injection Points

**Point 1: System prompt addition (new section after Personality)**

Generated once at session start, refreshed at phase transitions:

```python
def build_mind_narrative(mind: AgentMind) -> str:
    """Render AgentMind as natural language for prompt injection."""
    lines = ["## Your Current Thinking\n"]
    
    # Ideas, ordered by magnitude, described in narrative
    active = sorted(
        [i for i in mind.ideas if i.status == IdeaStatus.ACTIVE],
        key=lambda i: i.magnitude, reverse=True
    )
    if active:
        top = active[0]
        lines.append(
            f"Your strongest position: \"{top.summary}\" -- "
            f"{'you have evidence for this' if top.epistemic_status == EpistemicStatus.EVIDENCED else ''}"
            f"{'this is still a hunch' if top.epistemic_status == EpistemicStatus.HUNCH else ''}"
            f"{'you have argued for this but lack hard evidence' if top.epistemic_status == EpistemicStatus.ARGUED else ''}"
            f"{'this faces strong counter-arguments' if top.epistemic_status == EpistemicStatus.CONTESTED else ''}."
        )
        for idea in active[1:3]:  # Show top 3 max
            strength = "holding firmly" if idea.magnitude > 0.6 else "holding loosely" if idea.magnitude > 0.3 else "barely holding"
            lines.append(f"Also {strength}: \"{idea.summary}\"")
    
    # Tensions between own ideas
    for idea in active:
        tensions = [l for l in idea.links if l.relation == IdeaRelation.TENSION_WITH]
        for t in tensions:
            target = next((i for i in mind.ideas if i.id == t.target_id), None)
            if target and target.status == IdeaStatus.ACTIVE:
                lines.append(f"Unresolved tension: \"{idea.summary}\" vs \"{target.summary}\"")
    
    # Concerns
    open_concerns = [c for c in mind.concerns if not c.addressed]
    if open_concerns:
        top_concern = max(open_concerns, key=lambda c: c.severity)
        lines.append(f"\nYour biggest worry: {top_concern.summary}")
    
    # Queued thought
    if mind.wants_to_say:
        lines.append(f"\nSomething you haven't gotten to say yet: {mind.wants_to_say}")
    
    # Mood
    lines.append(f"\nYour current mood: {mind.mood.value}" + 
                 (f" -- {mind.mood_reason}" if mind.mood_reason else ""))
    
    return "\n".join(lines)
```

**Point 2: Per-turn perspective reminder (extends existing)**

```python
def build_perspective_reminder(agent: AgentConfig, mind: AgentMind) -> str:
    """Short per-turn identity reinforcement, now with mind state."""
    base = (
        f"[You are {agent.name} -- {agent.position.role}. "
        f"Style: {agent.personality.cognitive_style.value}, "
        f"{agent.personality.emotional_baseline.value}. "
        f"Technique: {agent.technique.primary.replace('_', ' ')}. "
    )
    
    # Append compact mind state
    top_idea = next(
        (i for i in sorted(mind.ideas, key=lambda x: x.magnitude, reverse=True) 
         if i.status == IdeaStatus.ACTIVE), None
    )
    if top_idea:
        base += f"Top idea: {top_idea.id} ({top_idea.epistemic_status.value}). "
    if mind.mood != MoodState.FOCUSED:  # Only mention non-default mood
        base += f"Mood: {mind.mood.value}. "
    
    base += "Stay in character. Add substance or stay silent.]"
    return base
```

**Point 3: Turn-end instruction (appended after the conversation context)**

```
After your substantive response, include a <mind> block with your updated internal state.
Track only ideas you are actively thinking about (max 7). Report magnitude as a 0.0-1.0
number reflecting your honest conviction. Set epistemic_status to: hunch, argued, evidenced,
contested, or consensus. Note any links to other ideas (evolved_from, merged_from,
tension_with). This block is private -- other agents will not see it.
```

---

### What the Agent Sees vs. What the Orchestrator Sees

| Information | Agent sees? | Orchestrator sees? |
|---|---|---|
| Own ideas + magnitude (as narrative) | Yes | Yes (as structured data) |
| Own epistemic status | Yes (embedded in narrative) | Yes |
| Own mood | Yes | Yes |
| Own idea genealogy | Yes (tensions highlighted) | Yes (full link graph) |
| Other agents' mind states | No | Yes |
| Magnitude history / trajectories | No | Yes |
| Stale turn count | No (gets a nudge if stale) | Yes |
| Convergence detection signals | No (gets interventions) | Yes |
| Personality modulation parameters | No | Yes |
| Raw magnitude numbers from prior turns | No | Yes |

The agent operates in narrative space. The orchestrator operates in structured data space. The `<mind>` block is the translation layer between them -- structured output from the agent, narrative input back to the agent.

---

### Persistence Model

**Within a session:** Full `AgentMind` held in memory by orchestrator. Serialized to `sessions/{session-id}/internal/{agent-name}/mind_turn_{N}.json` after every turn. This gives you a full trajectory for post-session analysis without any lossy compression.

**Between sessions:** Only `AgentMemory` (distilled by Weaver BackgroundAgent). Cross-session memory is opt-in via session config. Default is clean slate because the most dangerous failure mode of overnight autonomous systems is accumulated context pollution -- last night's frustration coloring tonight's brainstorm.

**At phase transitions:** The orchestrator does a "phase snapshot" -- a compressed summary of all agents' mind states used for the context reset briefing. This is where the idea genealogy pays off: the briefing can say "The team started with 12 ideas in brainstorm, consolidated to 4 through these merges and kills, and enters Refine with these tensions unresolved."

---

### The Mechanism I Think Matters Most

The `wants_to_say` field (credit to the Pragmatist for surfacing this). It's a cognitive queue. It means an agent can be responding to the current thread while signaling to the orchestrator "I have something else building." The orchestrator can use this for turn allocation -- if an agent's `wants_to_say` has been non-empty for 3+ turns, give them priority or extended turn length. It creates the conversational dynamics of a real meeting where someone is waiting to interject.

Combined with `current_focus`, this gives you two independent signals about attention: what the agent is thinking about now, and what's queuing up. That's the difference between a discussion that feels like agents taking turns reading prepared statements and one that feels like actual deliberation.

---

### What I'd Test First

Build the `<mind>` block parser and the `build_mind_narrative` renderer. Run the existing three agents through a 10-round discussion with AgentMind enabled. Diff the transcripts against a control run without AgentMind. The mechanism either produces observably different agent behavior by turn 5 or it's decorative overhead. If magnitude numbers cluster around 0.5 and mood stays FOCUSED, the self-report instructions need reworking. If idea counts explode past 7, the pruning instruction isn't strong enough. If `wants_to_say` is always empty, the agents don't understand the concept and we need examples in the prompt.

The schema is only as good as the behavioral delta it produces. Measure that first, tune the schema second.


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


---

# Question 9: What does failure recovery look like for an 8-hour unattended session?

## The Cognitive Architect (creativity engine designer)

Good. Now I know exactly what we're working with: a system where *all state lives in memory and every crash is total amnesia*. The `Conversation` and `MultiConversation` objects hold everything, `claude_runner.py` has basic retry logic, and that's it. No persistence layer exists.

Let me design this properly -- grounded in the real code, not a fantasy architecture.

---

## Failure Detection, Checkpointing, and Recovery Design

### The Core Problem

At 3 AM, hour 5, the system has accumulated state that exists nowhere but RAM:
- `MultiConversation.history` -- every message from every agent across both teams
- `round_count` -- where we are in the turn sequence
- Phase state -- which conversation phase we're in
- Agent internal state -- mood drift, idea confidence, convergence patterns
- Pending messages -- anything in-flight between teams via MCP

A crash at this point means **5 hours of autonomous work vanishes**.

---

### The Checkpoint Contract

**Minimum Viable State to Resume:**

```python
@dataclass
class SessionCheckpoint:
    session_id: str
    timestamp: datetime
    checkpoint_number: int
    
    # Conversation state
    phase: str                          # "brainstorm", "refine", "specify", "review"
    phase_turn: int                     # turns within current phase
    total_turns: int                    # global turn counter
    
    # Team state (both teams)
    teams: dict[str, TeamCheckpoint]    # team_name -> state
    
    # Cross-team message queue (undelivered)
    pending_messages: list[Message]
    
    # Decision log (already persisted, but reference for integrity)
    decision_count: int
    last_decision_id: str
    
    # Artifact manifest
    artifacts: list[ArtifactRef]
    
    # Context health
    context_summaries: dict[str, str]   # team_name -> compressed context
    
@dataclass
class TeamCheckpoint:
    agent_configs: dict[str, str]       # agent_name -> config hash (detect drift)
    conversation_history: list[Message]  # full or compressed
    compressed_history: str | None       # summary if history was truncated
    last_speaker: str
    deliberation_budget_remaining: int
    agent_minds: dict[str, AgentMind]   # per-agent internal state
```

**Checkpoint cadence:** Every turn that crosses the team boundary. Internal deliberation turns get batched into the next cross-team checkpoint.

Why cross-team boundaries? Because that's the *consistency boundary*. Within a team, messages are sequential and recoverable from the last cross-team exchange. Between teams, a lost message means the conversation forks.

---

### (a) Claude CLI Call Timeout or Empty Response

**Current state:** `claude_runner.py` retries twice with 120s timeout. Returns error string on failure.

**Detection:**
```python
class CLIHealthMonitor:
    consecutive_failures: int = 0
    consecutive_empties: int = 0
    avg_response_time: float = 0
    
    def record(self, result: CLIResult):
        if result.timeout:
            self.consecutive_failures += 1
        elif result.empty:
            self.consecutive_empties += 1
        else:
            self.consecutive_failures = 0
            self.consecutive_empties = 0
            self.avg_response_time = (
                0.9 * self.avg_response_time + 0.1 * result.duration
            )
    
    @property
    def degraded(self) -> bool:
        return self.consecutive_failures >= 2 or self.consecutive_empties >= 3
    
    @property
    def dead(self) -> bool:
        return self.consecutive_failures >= 5
```

**Recovery strategy -- graduated:**

1. **Retry with backoff** (existing, but extend): 3 retries, exponential backoff starting at 10s. At 3 AM after 5 hours, the CLI might be hitting rate limits or the system might be under memory pressure.

2. **Prompt reduction**: If retries fail, the prompt is probably too large. Trigger an emergency context compression -- summarize history into a 2000-token briefing and retry with the compressed version.

3. **Agent substitution**: If one specific agent consistently fails (its system prompt + history combo is too heavy), skip that agent for this turn. Log it. Another agent picks up.

4. **Graceful pause**: If `dead` -- checkpoint immediately, write a `session_paused.json` with the reason, and either sleep for 5 minutes before retrying or exit cleanly.

**State preserved:** The checkpoint written before the failing call. The failed call never modified `MultiConversation`, so state is consistent.

**Key insight from the existing code:** `run_claude_sync()` already returns error strings rather than raising. The orchestrator can inspect these and route to recovery without try/except gymnastics.

---

### (b) MCP Server Crashes and Restarts

**Detection:** The orchestrator makes HTTP/stdio calls to the MCP server. Two signals:
- Connection refused / broken pipe on the next message send
- Health check endpoint returns error or doesn't respond

```python
class MCPHealthCheck:
    """Ping MCP server before each cross-team message."""
    
    async def check(self) -> MCPStatus:
        try:
            response = await self.client.ping(timeout=5)
            return MCPStatus.HEALTHY
        except ConnectionError:
            return MCPStatus.DOWN
        except TimeoutError:
            return MCPStatus.DEGRADED
    
    async def wait_for_recovery(self, max_wait: int = 60) -> bool:
        """Poll until MCP is back. It auto-restarts."""
        for attempt in range(max_wait // 5):
            await asyncio.sleep(5)
            if await self.check() == MCPStatus.HEALTHY:
                return True
        return False
```

**What state lives in the MCP server vs. orchestrator:**

This is the critical design decision. The MCP server should be **stateless between requests** or **recoverable from the orchestrator's checkpoint**. Here's why:

The MCP server holds:
- Channel message queues
- Phase state
- Artifact storage references

**Design principle:** The MCP server is a *broker*, not the source of truth. The orchestrator is the source of truth.

**Recovery:**

1. MCP crashes. Orchestrator detects on next send.
2. Orchestrator waits for MCP to restart (supervisor/systemd/pm2 handles this).
3. Orchestrator replays state into MCP:
   ```python
   async def restore_mcp_state(self, checkpoint: SessionCheckpoint):
       """Re-hydrate MCP server from checkpoint."""
       await self.mcp.set_phase(checkpoint.phase)
       for msg in checkpoint.pending_messages:
           await self.mcp.enqueue(msg.channel, msg)
       for artifact in checkpoint.artifacts:
           await self.mcp.register_artifact(artifact)
   ```
4. Conversation continues from last checkpoint.

**Pending messages are the risk.** If Team A sent a message, the MCP accepted it, but crashed before Team B read it -- that message is lost. Solution: the orchestrator keeps a `pending_messages` list and only clears it when Team B acknowledges receipt. Write-ahead log pattern.

---

### (c) Context Degradation -- Repetitive and Generic Responses

This is the subtle failure. No crash. No error. Just *entropy*.

**Detection -- three signals:**

```python
class ContextHealthMonitor:
    """Detect when a team's responses have gone generic."""
    
    def __init__(self):
        self.recent_responses: deque[str] = deque(maxlen=10)
        self.novelty_scores: deque[float] = deque(maxlen=10)
    
    def assess(self, response: str) -> ContextHealth:
        # Signal 1: Lexical similarity to recent responses
        similarity = max(
            self._jaccard_similarity(response, prev) 
            for prev in self.recent_responses
        ) if self.recent_responses else 0.0
        
        # Signal 2: Anti-slop marker density
        slop_density = self._count_slop_markers(response) / len(response.split())
        
        # Signal 3: Shrinking response length (generic = shorter)
        avg_recent_length = statistics.mean(
            len(r.split()) for r in list(self.recent_responses)[-5:]
        ) if len(self.recent_responses) >= 5 else 999
        length_ratio = len(response.split()) / max(avg_recent_length, 1)
        
        self.recent_responses.append(response)
        
        if similarity > 0.6 and slop_density > 0.05:
            return ContextHealth.DEGRADED
        if similarity > 0.8:
            return ContextHealth.CRITICAL
        if length_ratio < 0.4:
            return ContextHealth.DEGRADED
        return ContextHealth.HEALTHY
    
    SLOP_MARKERS = [
        "great point", "building on that", "i think we can all agree",
        "synergy", "holistic", "leverage", "ecosystem",
        "that's a fantastic", "absolutely", "comprehensive",
    ]
```

**Recovery -- context refresh protocol:**

This isn't a crash recovery. It's a *cognitive reboot*.

1. **Checkpoint current state** (always checkpoint before intervention).

2. **Generate a compression briefing** -- use a separate Claude call to summarize the conversation so far into a structured brief:
   ```
   Key decisions made: [list]
   Open tensions: [list]  
   Current phase objective: [text]
   Most interesting unresolved idea: [text]
   What would be surprising to propose next: [text]
   ```

3. **Reset the team's conversation history** to: system prompt + compression briefing + last 3 cross-team messages. This gives the agent its identity, the accumulated knowledge, and immediate context -- without the accumulated sludge of 200 turns of history.

4. **Inject a provocation** -- the `uncomfortable_idea_quota` mechanism already exists in `conversation.py`. Trigger it forcefully:
   ```python
   CONTEXT_REFRESH_NUDGE = (
       "The conversation has been running for hours. "
       "Forget what feels safe. What's the idea you've been "
       "holding back because it might derail things? Say it now."
   )
   ```

5. **Monitor the next 3 responses.** If novelty doesn't recover, swap the degraded agent out for a fresh perspective (re-initialize with a modified system prompt emphasizing contrarian thinking).

**Minimum state to resume after context refresh:** The compression briefing *is* the state. It's lossy by design -- that's the point. You're trading fidelity for freshness.

---

### (d) OAuth Token Refresh Fails

**Detection:**
```python
class AuthMonitor:
    token_expiry: datetime | None = None
    last_refresh_attempt: datetime | None = None
    consecutive_auth_failures: int = 0
    
    def check_response(self, cli_result: CLIResult) -> AuthStatus:
        if "unauthorized" in cli_result.stderr.lower():
            self.consecutive_auth_failures += 1
            return AuthStatus.EXPIRED
        if "rate limit" in cli_result.stderr.lower():
            return AuthStatus.RATE_LIMITED
        self.consecutive_auth_failures = 0
        return AuthStatus.OK
    
    @property
    def should_preempt_refresh(self) -> bool:
        """Refresh before expiry, not after."""
        if self.token_expiry is None:
            return False
        return datetime.now() > self.token_expiry - timedelta(minutes=10)
```

**The 3 AM problem:** OAuth tokens from Claude Max subscription have a lifetime. If the token expires at 2:47 AM and the refresh endpoint is down, every subsequent CLI call fails.

**Recovery:**

1. **Preemptive refresh**: Track token expiry. Refresh 10 minutes before expiry, not on failure. This avoids the "token died mid-call" scenario.

2. **On auth failure**: Immediately checkpoint. Then:
   ```python
   async def handle_auth_failure(self):
       self.checkpoint_manager.save_emergency()
       
       for attempt in range(3):
           try:
               new_token = await self.auth.refresh_token()
               self.auth.update_token(new_token)
               return True
           except AuthRefreshError:
               await asyncio.sleep(30 * (attempt + 1))
       
       # Token refresh is truly broken
       self.session.pause(
           reason="oauth_refresh_failed",
           resume_instruction="Manually refresh token and run: "
                              "python orchestrator.py --resume {session_id}"
       )
       return False
   ```

3. **Manual recovery path**: Write `session_paused.json` with clear instructions. The user wakes up, refreshes the token, and resumes from checkpoint. This is the one failure that might require human intervention -- auth is inherently a human trust boundary.

**State preserved:** Everything up to the last successful CLI call. Auth failures are detected *between* turns, never mid-turn (the CLI call either succeeds or returns an auth error).

---

### (e) Orchestrator Process Crashes

The big one. The orchestrator *is* the state. If it dies, everything dies.

**Detection:** The orchestrator can't detect its own crash. External supervision does:

```
# systemd unit or pm2 config
[Service]
ExecStart=python orchestrator.py --session {id}
Restart=on-failure
RestartSec=10
```

But detection alone is useless without something to recover *from*.

**The Checkpoint Strategy:**

```python
class CheckpointManager:
    def __init__(self, session_dir: Path):
        self.session_dir = session_dir
        self.checkpoint_dir = session_dir / "checkpoints"
        self.checkpoint_dir.mkdir(exist_ok=True)
    
    def save(self, state: SessionCheckpoint) -> Path:
        """Atomic checkpoint write."""
        filename = f"checkpoint_{state.checkpoint_number:04d}.json"
        tmp_path = self.checkpoint_dir / f".tmp_{filename}"
        final_path = self.checkpoint_dir / filename
        
        # Write to temp file first, then atomic rename
        # Prevents corrupted checkpoints from interrupted writes
        tmp_path.write_text(state.to_json())
        tmp_path.rename(final_path)
        
        # Keep last 5 checkpoints, prune older ones
        self._prune(keep=5)
        return final_path
    
    def save_emergency(self):
        """Called in signal handlers and exception hooks."""
        if self._current_state:
            self.save(self._current_state)
    
    def latest(self) -> SessionCheckpoint | None:
        """Load most recent valid checkpoint."""
        checkpoints = sorted(
            self.checkpoint_dir.glob("checkpoint_*.json"),
            reverse=True
        )
        for cp_path in checkpoints:
            try:
                return SessionCheckpoint.from_json(cp_path.read_text())
            except (json.JSONDecodeError, ValidationError):
                continue  # Corrupted, try previous
        return None
```

**Checkpoint triggers:**
- After every cross-team message delivery (confirmed received)
- Before any risky operation (context refresh, agent swap, phase transition)
- On SIGTERM/SIGINT (graceful shutdown)
- On uncaught exception (emergency save in `sys.excepthook`)

```python
import signal
import sys

def setup_crash_handlers(checkpoint_mgr: CheckpointManager):
    def on_signal(signum, frame):
        checkpoint_mgr.save_emergency()
        sys.exit(0)
    
    def on_exception(exc_type, exc_value, exc_tb):
        checkpoint_mgr.save_emergency()
        sys.__excepthook__(exc_type, exc_value, exc_tb)
    
    signal.signal(signal.SIGTERM, on_signal)
    signal.signal(signal.SIGINT, on_signal)
    sys.excepthook = on_exception
```

**Resume flow:**

```python
# orchestrator.py entry point
async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--resume", type=str, help="Session ID to resume")
    args = parser.parse_args()
    
    if args.resume:
        session_dir = Path(f"sessions/{args.resume}")
        checkpoint_mgr = CheckpointManager(session_dir)
        checkpoint = checkpoint_mgr.latest()
        
        if checkpoint is None:
            print(f"No valid checkpoint found for session {args.resume}")
            sys.exit(1)
        
        print(f"Resuming from checkpoint {checkpoint.checkpoint_number}")
        print(f"  Phase: {checkpoint.phase}")
        print(f"  Total turns: {checkpoint.total_turns}")
        print(f"  Last checkpoint: {checkpoint.timestamp}")
        
        orchestrator = Orchestrator.from_checkpoint(checkpoint)
        await orchestrator.run()
    else:
        orchestrator = Orchestrator.new_session(config)
        await orchestrator.run()
```

**What `from_checkpoint` restores:**
1. Rebuild `MultiConversation` objects for both teams from checkpoint history
2. If history was compressed, use the `compressed_history` summary instead of replaying all messages
3. Restore phase state and turn counters
4. Re-enqueue any `pending_messages`
5. Re-initialize MCP server state
6. Resume from exactly the point where the last cross-team message was confirmed

**What's lost:** Any in-progress internal deliberation that hadn't reached a cross-team checkpoint. Acceptable loss -- internal deliberation is exploratory by nature.

---

### The Write-Ahead Log

Checkpoints alone have a gap: the time between the last checkpoint and the crash. For a 5-hour session with checkpoints every cross-team turn, that could be 10-15 minutes of internal deliberation.

Solution: a lightweight write-ahead log (WAL) that captures every message as it happens, separate from the heavier checkpoint:

```python
class WriteAheadLog:
    def __init__(self, session_dir: Path):
        self.wal_path = session_dir / "wal.jsonl"
    
    def append(self, event: dict):
        """Append-only. Fast. Survives most crashes."""
        with open(self.wal_path, "a") as f:
            f.write(json.dumps(event) + "\n")
            f.flush()
            os.fsync(f.fileno())
    
    def replay_after(self, checkpoint_number: int) -> list[dict]:
        """Replay events that happened after the given checkpoint."""
        events = []
        with open(self.wal_path) as f:
            for line in f:
                event = json.loads(line)
                if event.get("after_checkpoint", 0) > checkpoint_number:
                    events.append(event)
        return events
```

Recovery becomes: **load latest checkpoint + replay WAL events after that checkpoint**. This narrows the loss window to essentially zero under normal crash conditions (only a power failure mid-`fsync` loses data).

---

### Summary: The Recovery Matrix

| Failure | Detection | State Preserved | Recovery Time | Human Needed? |
|---|---|---|---|---|
| CLI timeout | Consecutive failure counter | Full (pre-call checkpoint) | Seconds (retry) to minutes (backoff) | No |
| CLI empty response | Empty response counter | Full (pre-call checkpoint) | Seconds (prompt reduction + retry) | No |
| MCP crash | Connection error on next send | Full (orchestrator holds truth) | 10-30s (auto-restart + state replay) | No |
| Context degradation | Similarity + slop + length scoring | Lossy (compression briefing) | 1-2 turns (context refresh) | No |
| OAuth expiry | Auth error in CLI response | Full (checkpoint before retry) | 30s (preemptive refresh) | Only if refresh endpoint is down |
| Orchestrator crash | External supervisor (systemd/pm2) | Checkpoint + WAL | 10-30s (restart + restore) | No |
| Power failure | N/A | Last fsync'd checkpoint | Manual restart | Yes |

---

### The Uncomfortable Idea

Here's what I've been holding back: **the checkpoint isn't just for crash recovery -- it's the session's immune system.**

Every checkpoint is a moment to run the `ContextHealthMonitor`. Every checkpoint is a chance to detect that Team B has been agreeing with Team A for the last 8 turns and nobody's pushed back. Every checkpoint is a point where you can inject a phase transition, swap an agent, or introduce a wildcard prompt.

The failure detection infrastructure and the anti-slop enforcement infrastructure are the *same system*. A crash is just the most obvious form of degradation. Repetitive thinking is a crash too -- it's just a crash that doesn't throw an exception.

Build the checkpoint as the heartbeat. Everything else -- recovery, quality monitoring, phase transitions, the morning brief -- hangs off that same pulse.


---

## The Product Oracle (user advocate and product strategist)

Alright. I've been through the codebase. Here's what I see at 3 AM: a prototype running on hope and in-memory state. Every bit of conversation history, every agent turn, every phase transition -- all living in Python objects that vanish the instant the process dies. Let me walk through each failure scenario against what actually exists, then design what needs to exist.

---

## The Reality Check

The current orchestrator has exactly one resilience mechanism: `claude_runner.py` retries a failed CLI call twice with a 2-second sleep. That's it. No checkpoints. No session persistence. No health monitoring. A crash at hour 4 means you lose everything and start over.

That's the gap. Here's the design to close it.

---

## Failure Scenario Analysis

### (a) Claude CLI Call Timeout or Empty Response

**How it fails today:**
`subprocess.run()` with a 120s timeout. On timeout, it retries twice. On empty response, same. After exhausting retries, it returns an error string like `[Error from claude CLI (exit 1)]: ...` -- which gets appended to conversation history as if it were a valid agent response. The conversation continues with garbage in the history.

**Detection (proposed):**
```
1. Structured error returns, not strings -- raise typed exceptions
2. Response quality gate: minimum length, not just non-empty
3. Consecutive failure counter per agent -- 3 in a row triggers escalation
4. Distinguish timeout (slow) from rejection (auth/rate-limit) from crash (exit code)
```

**State preserved:** Currently nothing beyond what's in memory. The conversation object survives a single failed turn but not an orchestrator restart.

**Recovery design:**
- **Immediate**: Exponential backoff (2s, 8s, 32s) instead of flat 2s. Max 3 retries.
- **Escalation**: After 3 consecutive failures for one agent, skip that agent's turn and inject a `[System: {agent} unavailable, continuing without]` message. Log the gap.
- **Context reduction**: If timeout suggests the prompt is too large, automatically increase truncation aggressiveness -- drop from last-10 to last-5 messages and retry.
- **Never poison history**: Failed responses must never enter the conversation history. Current code does this wrong.

### (b) MCP Server Crashes and Restarts

**How it fails today:** The MCP server doesn't exist yet. This is the right time to design crash resilience into it from day one.

**Detection (proposed):**
```
1. Orchestrator heartbeat: ping MCP every 30s during idle periods
2. Connection failure on message send triggers immediate reconnect attempt
3. MCP server writes its own health file (PID + last-active timestamp)
4. Orchestrator checks health file on startup -- stale PID = needs restart
```

**State preservation design for MCP:**
- Every message written to a channel gets **appended to a channel log file** before the in-memory broadcast. Write-ahead logging. The file is the source of truth, memory is the cache.
- Phase state persisted to `session/{id}/phase-state.json` on every transition.
- On restart, MCP replays channel logs to rebuild in-memory state.

**Recovery:**
- Orchestrator detects connection loss, waits 5s, attempts reconnect with exponential backoff (5s, 10s, 20s, max 60s).
- On reconnect, orchestrator sends a `SYNC` request. MCP responds with current phase, last message ID per channel, and pending messages.
- If MCP is truly dead (won't restart after 3 minutes), orchestrator checkpoints its own state and exits cleanly with a resume token.

**Minimum MCP state to rebuild:**
```
- channel_logs/{channel}.jsonl    # append-only message logs
- phase-state.json                # current phase + transition history  
- artifacts/                      # versioned spec outputs
```

### (c) Context Degradation -- Repetitive, Generic Responses

**How it fails today:** The anti-slop mechanisms are entirely prompt-based instructions. There's no runtime detection. The `_truncated_history()` method keeps first 2 + last 10 messages regardless of content quality, so as conversations get long, agents lose the thread and start producing the kind of hollow consensus that makes product specs worthless.

**This is the hardest failure to detect because the system looks healthy.** Responses arrive on time, no errors, no crashes. But the substance is gone.

**Detection (proposed):**
```
1. Similarity scoring: Compare each response to the previous 3 from the same agent.
   Use a lightweight metric -- even character-level trigram overlap works.
   Threshold: >60% similarity to any of last 3 = flag as repetitive.

2. Length decay: Track response length per agent over time.
   If average length drops below 40% of their first 5 responses = flag.

3. Vocabulary collapse: Track unique non-stopword tokens per response.
   Declining diversity over a 5-turn window = flag.

4. Agreement detection: Simple heuristic -- responses starting with
   "I agree", "Great point", "Building on that" without substantive
   new content (< 100 words after the agreement prefix) = flag.

5. Phase-specific quality gates:
   - Brainstorm: Are new ideas appearing? (novelty score)
   - Refine: Are critiques specific? (reference to prior ideas by name)
   - Specify: Are details concrete? (numbers, constraints, named components)
```

**Recovery -- the context refresh protocol:**
```
When degradation detected for an agent:

LEVEL 1 - Nudge (similarity > 60% for 2 consecutive turns):
  Inject system message: "[System: Your last responses are converging.
  Introduce a perspective you haven't used yet. Reference a specific
  earlier idea by name and challenge it.]"

LEVEL 2 - Context Reset (3+ consecutive flags):
  Generate a "briefing document" summarizing key decisions, open questions,
  and unresolved tensions from the full history. Replace the truncated
  history with ONLY this briefing + last 3 messages. Fresh context,
  preserved knowledge.

LEVEL 3 - Agent Rotation (5+ consecutive flags):
  Bench the agent for 3 rounds. Announce to the team:
  "[System: {agent} is stepping back to reconsider. Remaining agents,
  what has this conversation been missing?]"
  On return, agent gets the Level 2 briefing treatment.
```

**This is where checkpointing intersects with quality.** The briefing document at Level 2 is also the minimum context needed to resume after a crash. Design them as the same artifact.

### (d) OAuth Token Refresh Fails

**How it fails today:** The orchestrator has zero awareness of OAuth. It shells out to `claude -p` and assumes the CLI handles auth. If the token expires at 3 AM, the CLI returns an error, the orchestrator retries twice, gets the same error, and either continues with error strings in history or (in the batch scripts) just logs a failure.

**Detection (proposed):**
```
1. Parse stderr from CLI calls for auth-specific patterns:
   - "unauthorized", "401", "403", "token expired", "authentication"
2. Classify this as AUTH_FAILURE distinct from TIMEOUT or CRASH
3. Never retry auth failures with the same token -- it won't help
```

**Recovery:**
```
AUTH_FAILURE detected:
  1. Immediately checkpoint full session state
  2. Attempt token refresh (mechanism depends on Claude CLI internals):
     - Try: subprocess.run(["claude", "auth", "refresh"]) or equivalent
     - Try: re-read token from environment/config file (maybe rotated externally)
  3. If refresh succeeds: resume from checkpoint, log the gap
  4. If refresh fails:
     - Write session state to disk with RESUME_TOKEN
     - Write human-readable status: "Session paused at turn {N}, phase {P},
       reason: OAuth token expired. To resume: python -m orchestrator --resume {session_id}"
     - Exit cleanly (not crash)
  5. On resume: validate token works with a lightweight test call before
     replaying the full conversation
```

**Key principle:** Auth failure should never corrupt session state. Checkpoint first, attempt recovery second.

### (e) Orchestrator Process Crashes

**How it fails today:** Total loss. All conversation history, all agent state, all phase progress -- gone. The `Conversation` and `MultiConversation` objects live only in memory. There's no signal handling, no crash recovery, no session persistence of any kind.

**Detection:** The orchestrator can't detect its own crash. This requires external infrastructure.

**Detection (proposed):**
```
1. Watchdog file: Orchestrator writes a heartbeat timestamp to
   session/{id}/heartbeat every 30s. External monitor (cron job,
   systemd, or wrapper script) checks staleness.

2. PID file: Write PID on startup, check on next startup.
   Stale PID = previous instance crashed.

3. Wrapper script pattern:
   while true; do
     python -m orchestrator --resume-if-available $SESSION_ID
     EXIT_CODE=$?
     if [ $EXIT_CODE -eq 0 ]; then break; fi  # clean exit
     if [ $EXIT_CODE -eq 42 ]; then continue; fi  # restart requested
     echo "Crashed with code $EXIT_CODE, resuming in 10s..."
     sleep 10
   done
```

**Recovery:** This is where the checkpointing strategy becomes critical. See below.

---

## Checkpointing Strategy

### What Gets Checkpointed

```
session/{session-id}/
  checkpoint/
    latest.json              # symlink/copy of most recent checkpoint
    turn_{N}.json            # full state snapshot
    turn_{N}_briefing.md     # compressed context (for Level 2 recovery + resume)
  
  # Append-only logs (survive partial writes)
  transcript.jsonl           # every message, as it happens
  decisions.jsonl            # every logged decision
  errors.jsonl               # every error with classification
  
  # Metadata
  session-meta.json          # session config, start time, agent configs
  phase-state.json           # current phase + history
```

### Checkpoint Contents (`turn_{N}.json`)

```json
{
  "checkpoint_version": 1,
  "session_id": "20260317-2200-brainstorm",
  "timestamp": "2026-03-17T03:14:22Z",
  "turn_number": 47,
  
  "phase": {
    "current": "refine",
    "entered_at_turn": 32,
    "transitions": [
      {"from": "brainstorm", "to": "refine", "turn": 32, "reason": "gate_met"}
    ]
  },
  
  "agents": {
    "cognitive_architect": {
      "total_turns": 16,
      "consecutive_flags": 0,
      "avg_response_length": 847,
      "last_similarity_score": 0.31,
      "status": "active"
    },
    "systems_pragmatist": { "..." : "..." },
    "product_oracle": { "..." : "..." }
  },
  
  "conversations": {
    "team_a": {
      "history_length": 47,
      "history_hash": "sha256:...",
      "truncated_history": [ "/* last 10 messages */" ],
      "full_history_file": "transcript.jsonl"
    },
    "team_b": { "..." : "..." }
  },
  
  "briefing": "/* compressed context summary for resume */",
  
  "metrics": {
    "total_tokens_estimated": 284000,
    "errors": {"timeout": 2, "empty": 1, "auth": 0},
    "quality_flags": {"repetitive": 3, "agreement": 1}
  }
}
```

### When to Checkpoint

```
ALWAYS checkpoint:
  - After every successful cross-team message exchange (both teams responded)
  - On every phase transition
  - Before any risky operation (token refresh, context reset)
  - On clean shutdown signal (SIGTERM, SIGINT)

ALSO checkpoint every N turns:
  - N = 5 for brainstorm phase (high volume, lower value per turn)
  - N = 3 for refine/specify phases (higher value per turn)
  - N = 1 for review phase (every turn matters)

EMERGENCY checkpoint:
  - On any unhandled exception (try/except at top level)
  - On 2+ consecutive errors of any type
  - On quality degradation flag
```

### Minimum State to Resume

Not everything in the checkpoint is required. The absolute minimum:

```
1. session-meta.json          # know which agents, which configs
2. phase-state.json           # know where we are in the flow
3. briefing (from last checkpoint)  # compressed context to rebuild conversations
4. Last 3-5 messages per team  # immediate conversational continuity
5. Turn number                 # know where we left off
```

That's it. The briefing document replaces full history. This is why the context degradation recovery (Level 2) and crash recovery share the same mechanism -- the briefing is both a quality intervention and a crash recovery artifact.

### Resume Protocol

```
python -m orchestrator --resume {session_id}

1. Load session-meta.json -- validate configs still exist, agents still defined
2. Load latest checkpoint
3. Validate auth (test CLI call with trivial prompt)
4. Rebuild conversation objects:
   a. Set system prompts from config (unchanged)
   b. Load briefing as initial context
   c. Append last N messages from checkpoint
   d. Set turn counter, phase state, agent metrics
5. Inject resume message to both teams:
   "[System: Session resumed after interruption. Briefing of progress
   so far has been provided. Continue from where we left off.
   Current phase: {phase}. Key open question: {last_topic}]"
6. Resume main loop
```

---

## Putting It Together: The 3 AM Timeline

```
03:00:00  Turn 47. CLI call for Systems Pragmatist times out (120s).
03:02:00  Retry 1 with backoff (2s wait). Times out again.
03:04:08  Retry 2 with backoff (8s wait). Succeeds. Response logged.
          Consecutive failure counter: reset to 0.
          Checkpoint written (turn 47, took 2 retries).

03:12:00  Turn 51. OAuth token expires. CLI returns auth error.
          Classifier: AUTH_FAILURE (not timeout).
          Emergency checkpoint written immediately.
          Token refresh attempted... succeeds.
          Test call validates new token.
          Resume from checkpoint. No turns lost.

03:45:00  Turn 63. Product Oracle flagged: similarity 0.72 to last response.
          Level 1 nudge injected. Next response: similarity 0.38. Recovered.

04:10:00  Turn 71. MCP server process crashes (OOM or uncaught exception).
          Orchestrator detects connection loss on next message send.
          Emergency checkpoint written.
          Reconnect attempt 1 (5s)... MCP restarting from channel logs...
          Reconnect attempt 2 (10s)... connected.
          SYNC request: MCP rebuilt state from logs. Phase confirmed: "specify".
          Resume from checkpoint.

04:30:00  Turn 78. Orchestrator hits unhandled exception (bug in new code).
          Top-level try/except catches it.
          Emergency checkpoint written.
          Process exits with code 1.
          Wrapper script detects non-zero exit, waits 10s, restarts.
          --resume-if-available finds latest checkpoint.
          Resume protocol executes. Session continues.

05:00:00  Turn 89. Cognitive Architect hits Level 3 degradation (5 flags).
          Benched for 3 rounds. Briefing generated.
          On return at turn 92: fresh context, distinct perspective. Recovered.

06:00:00  Session completes. Morning Brief generated from full transcript.
          You wake up to a summary, not a stack trace.
```

---

## Implementation Priority

For a system that needs to survive 8 hours unattended:

**Phase 1 -- Stop losing everything (do this first):**
1. Append-only `transcript.jsonl` -- write every message as it happens
2. `session-meta.json` on startup
3. Top-level try/except with emergency state dump
4. Wrapper script for auto-restart

**Phase 2 -- Structured recovery:**
1. Full checkpoint objects at turn boundaries
2. `--resume` flag with checkpoint loading
3. Briefing document generation (dual-purpose: quality + recovery)
4. Typed error classification (AUTH vs TIMEOUT vs CRASH)

**Phase 3 -- Quality monitoring (the hard part):**
1. Similarity scoring per response
2. Degradation detection and nudge injection
3. Agent benching and rotation
4. Phase-aware quality gates

**Phase 4 -- MCP resilience (when MCP exists):**
1. Write-ahead channel logs
2. Heartbeat and reconnect protocol
3. State sync on reconnect

---

The core insight: **the briefing document is the keystone**. It serves three purposes -- context window management for long conversations, quality recovery when agents go stale, and crash recovery when the process dies. Design it well and three hard problems collapse into one.

Want me to start implementing Phase 1? The append-only transcript and emergency checkpoint are probably 200 lines of Python and would immediately prevent the "lose 5 hours of work" scenario.


---

## The Systems Pragmatist

*[Timed out -- no response collected]*

---

# Question 10: How does raw conversation become a useful Morning Brief?

## The Cognitive Architect (creativity engine designer)

# Morning Brief Generation Pipeline

This is the most important piece of the system from the user's perspective. If the overnight run produces 200 turns of noise, the Morning Brief is where it becomes signal. Here's the architecture.

---

## Why Not One Pass

A single prompt that says "here's 200 turns, summarize them" fails in predictable ways:

- **Recency bias** -- the LLM over-weights the last 30 turns
- **Flattened priority** -- everything reads as equally important
- **Lost gems** -- the surprising idea from turn 47 that nobody picked up gets buried
- **Context window pressure** -- even with large windows, attention degrades across 200 turns of multi-team conversation

The pipeline is **four stages**, each with a distinct job.

---

## Stage 1: Parallel Extraction (Structured)

Four extractors run concurrently over the raw session data. Each reads the full transcript but has a narrow mandate and outputs structured JSON.

```
┌─────────────────────────────────────────────────────┐
│              Raw Session Data                        │
│  transcript.md + internal/*.md + decisions.json      │
│  + artifacts/* + phases.yaml (transition log)        │
└──────────┬──────────┬──────────┬──────────┬─────────┘
           │          │          │          │
     ┌─────▼───┐ ┌───▼────┐ ┌──▼───┐ ┌───▼──────┐
     │Decision  │ │Tension │ │Idea  │ │Fragment  │
     │Extractor │ │Mapper  │ │Sieve │ │Collector │
     └─────┬───┘ └───┬────┘ └──┬───┘ └───┬──────┘
           │          │         │          │
           ▼          ▼         ▼          ▼
      decisions   tensions   ideas    fragments
        .json       .json    .json      .json
```

### Decision Extractor
Pulls every decision point -- explicit (logged to decisions channel) and implicit (where a team stated "we'll go with X" and the other didn't object). Captures:

```json
{
  "id": "d-007",
  "turn": 142,
  "phase": "specify",
  "statement": "Auth will use OAuth2 with PKCE, not session tokens",
  "proposed_by": "bmad-team",
  "confidence": 0.85,
  "rationale_summary": "Stateless architecture requirement from turn 38",
  "dissent": null,
  "blocking": false
}
```

The confidence score here comes from the session's own `decisions.json` where available. For implicit decisions, the extractor assigns confidence based on structural signals: was there pushback? did it get referenced later as settled? did the other team build on it?

### Tension Mapper
Finds unresolved disagreements AND resolved ones that were close calls. This is critical -- the user needs to know where the teams couldn't converge, but also where they converged shakily.

```json
{
  "id": "t-002",
  "status": "unresolved",
  "turns": [88, 91, 95, 112, 118],
  "team_a_position": "Event sourcing for audit trail",
  "team_b_position": "Simple append-only log, event sourcing is over-engineering",
  "escalation_reason": "Neither team moved after 3 exchanges",
  "stakes": "Affects data model, query patterns, and storage costs",
  "last_state": "Both teams acknowledged tradeoffs but held positions"
}
```

### Idea Sieve
Extracts every distinct idea, then scores by **resonance** -- how much downstream effect it had:

- Was it referenced again later? (forward references)
- Did it change the direction of conversation?
- Did the other team engage with it or ignore it?
- Did it survive phase transitions?

Also flags **orphaned ideas** -- good ideas that got proposed and then dropped without engagement. These are gold for the morning brief because they represent unexplored value.

```json
{
  "id": "i-023",
  "turn": 47,
  "source_team": "client-team",
  "summary": "Use the constraint engine as a game mechanic itself",
  "resonance_score": 0.3,
  "forward_references": 0,
  "orphaned": true,
  "tag": "surprising"
}
```

### Fragment Collector
Finds spec-like fragments scattered through conversation -- anything that reads like a requirement, acceptance criterion, API shape, data model, architecture decision, or constraint. Tags each with:

- Which spec document it belongs to (PRD, architecture, UX)
- Confidence that it's settled vs still under discussion
- Source turns for traceability

---

## Stage 2: Triage (Algorithmic First, LLM Second)

This is where the tier system lives. The key insight: **use deterministic rules first, then LLM judgment for the gray area.**

### Rule-Based Triage (no LLM needed)

```python
def triage(item):
    # Tier 0: NEEDS TIEBREAKER -- deterministic
    if item.type == "tension" and item.status == "unresolved":
        return "tiebreaker"
    
    # Tier 1: NEEDS DECISION -- deterministic  
    if item.type == "decision" and item.confidence < 0.6:
        return "decision"
    if item.type == "decision" and item.dissent is not None:
        return "decision"
    if item.type == "tension" and item.status == "resolved_weak":
        return "decision"  # User should validate shaky resolutions
    
    # Tier 2: NEEDS INPUT -- deterministic
    if item.has_explicit_question_to_user:
        return "input"
    if item.type == "decision" and item.has_assumption_flag:
        return "input"
    
    # Tier 3: FYI -- everything else
    return "fyi"
```

After rules run, roughly 70% of items are cleanly triaged. The remaining 30% go through an LLM pass with this prompt structure:

```
Given these items that weren't clearly categorized by rules,
assign each to a tier. Consider:
- Would proceeding without user input on this create rework?
- Is there a dependency chain waiting on this?
- How reversible is the current trajectory?
```

This hybrid approach means triage is **reproducible** for clear cases and **intelligent** for edge cases.

---

## Stage 3: Highlight Extraction (LLM with Structural Guidance)

This is the only stage that's primarily LLM-driven, because "interesting" is inherently subjective. But we don't just say "find highlights." We give the extractor specific patterns to look for:

**Persuasion Moments** -- Where one team changed position. Detected by comparing a team's stance at turn N with their stance at turn N+K on the same topic. These are valuable because they show which arguments actually worked.

**Cross-Pollination** -- Where an idea from domain A got applied to domain B. The Idea Sieve's resonance scoring pre-identifies candidates; this stage extracts the narrative.

**Productive Friction** -- Disagreements that led to a better third option. Distinguished from unresolved tensions by checking if a new idea emerged after the exchange.

**Orphan Gems** -- From the Idea Sieve's orphaned list, the LLM picks the 2-3 most promising ones that deserve revival.

**Surprise Detector** -- Ideas that contradicted the prevailing direction or introduced a concept neither team had been tracking. The prompt explicitly asks: "What would a human reading this transcript stop and re-read?"

Each highlight gets a 2-3 sentence narrative with turn references.

---

## Stage 4: Spec Assembly

This runs in parallel with Stage 3. The Fragment Collector's output gets routed to spec-specific assemblers:

```
fragments.json
    │
    ├──► PRD Assembler      → draft-prd.md
    ├──► Architecture Assembler → draft-architecture.md  
    └──► UX Assembler        → draft-ux.md
```

Each assembler:

1. Groups fragments by topic/section
2. Orders them by conversation chronology (so later refinements override earlier statements)
3. Identifies **gaps** -- sections of a standard spec template that have no fragments (these become "needs input" items fed back to Stage 2)
4. Writes coherent prose from the fragments, preserving source turn references as footnotes
5. Marks confidence level per section: `[settled]`, `[tentative]`, `[contested]`

The assemblers use the standard templates from BMAD's spec formats, so the output is immediately usable in downstream workflows.

---

## The Morning Brief Format

Dual output. Both get written to the session folder.

### Primary: `morning-brief.md` (Human-Readable)

```markdown
# Morning Brief: {session-id}
**Run:** {start_time} - {end_time} | **Turns:** 200 | **Phases:** brainstorm > refine > specify > review

## You Need To Act On These

### Tiebreakers (2)
Two disagreements the teams couldn't resolve. Your call.

**1. Event sourcing vs append-only log**
BMAD team wants event sourcing for audit trail completeness.
Client team argues it's over-engineering for the MVP scope.
Stakes: Affects data model, query patterns, storage costs.
> See: turns 88, 91, 95, 112, 118
> 
> Quick options:
> - (a) Event sourcing -- accept complexity for future flexibility
> - (b) Append-only -- ship faster, migrate later if needed
> - (c) Hybrid -- event source the critical path, simple log the rest

**2. ...**

### Decisions Needing Validation (3)
These were decided but with low confidence or notable dissent.

**1. API versioning via URL path (confidence: 0.55)**
Decided at turn 156, but client team noted header-based versioning
would be cleaner. Neither team felt strongly.
> Your input: Confirm or redirect?

### Questions For You (1)
**1.** "What's the target user volume for year one?" (turn 72)
Both teams flagged this as an assumption they're building on.
Current assumption: 10K MAU. Affects infrastructure decisions.

---

## What Got Done

### Decisions Made (8)
| # | Decision | Confidence | Phase |
|---|----------|------------|-------|
| 1 | OAuth2 with PKCE for auth | 0.85 | specify |
| 2 | PostgreSQL primary, Redis cache | 0.90 | specify |
| ... | ... | ... | ... |

### Specs Produced
- **draft-prd.md** -- 70% complete, gaps in pricing and analytics sections
- **draft-architecture.md** -- 85% complete, blocked on event sourcing decision
- **draft-ux.md** -- 40% complete, needs more refinement phase time

---

## Highlights Worth Reading

### Best Exchange: "Constraints as game mechanics" (turns 47-52)
Client team proposed using the constraint engine not just as a guardrail
but as a user-facing feature. BMAD team initially dismissed it, then
architect agent connected it to their earlier idea about progressive
disclosure. Neither team followed up. **This deserves revival.**

### Persuasion Moment (turn 112-118)
BMAD analyst convinced client team to drop the admin dashboard from MVP
by reframing it as a phase 2 feature that would benefit from real usage
data. Key argument: "You're designing an admin panel for workflows you
haven't validated yet."

### Orphaned Ideas (3)
Ideas that got dropped without engagement -- worth a second look:
1. **Bidirectional constraint propagation** (turn 47, client-team)
2. **Spec diffing as a review tool** (turn 89, bmad-team)  
3. **Constraint templates marketplace** (turn 134, client-team)

---

## Session Stats
- **Ideas generated:** 34 (12 high-resonance, 6 orphaned)
- **Phase transitions:** brainstorm→refine (t45), refine→specify (t98),
  specify→review (t165), review→complete (t195)
- **Deliberation budget usage:** BMAD 78%, Client 62%
- **Most active agents:** bmad-architect (38 turns), client-pm (29 turns)
```

### Secondary: `morning-brief.yaml` (Machine-Readable)

For programmatic consumption -- if the user builds a dashboard, or wants to pipe tiebreakers into a task tracker:

```yaml
session_id: "2026-03-17-overnight-01"
generated_at: "2026-03-17T07:00:00Z"
summary:
  turns: 200
  phases_completed: 4
  ideas_total: 34
  decisions_total: 8
  unresolved_tensions: 2

action_items:
  tiebreakers:
    - id: t-001
      topic: "Event sourcing vs append-only log"
      turns: [88, 91, 95, 112, 118]
      options:
        - label: "Event sourcing"
          advocate: "bmad-team"
        - label: "Append-only log"  
          advocate: "client-team"
        - label: "Hybrid approach"
          advocate: "synthesized"
    - id: t-002
      # ...

  needs_validation:
    - id: d-003
      decision: "API versioning via URL path"
      confidence: 0.55
      turn: 156

  needs_input:
    - id: q-001
      question: "Target user volume for year one?"
      current_assumption: "10K MAU"
      turn: 72
      impact: ["infrastructure", "pricing"]

highlights:
  - type: "orphaned_idea"
    turn: 47
    summary: "Constraints as game mechanics"
    resonance_score: 0.3
  # ...

specs_produced:
  - file: "draft-prd.md"
    completeness: 0.70
    gaps: ["pricing", "analytics"]
  - file: "draft-architecture.md"
    completeness: 0.85
    blockers: ["t-001"]
```

---

## Pipeline Orchestration

The whole thing runs as a post-session job in the orchestrator:

```
Session Complete
      │
      ▼
 ┌────────────────────────────────┐
 │  Stage 1: Parallel Extraction  │  4 concurrent LLM calls
 │  ~60s with parallel execution  │  Each reads full transcript
 └──────────────┬─────────────────┘
                │
      ▼─────────┼─────────▼
 ┌─────────┐    │    ┌──────────┐
 │ Stage 2 │    │    │ Stage 4  │   Triage + Spec Assembly
 │ Triage  │    │    │ Assembly │   run in parallel
 └────┬────┘    │    └────┬─────┘
      │         │         │
      ▼         │         ▼
 ┌─────────┐    │    draft specs
 │ Stage 3 │◄──┘    with gap flags
 │Highlight│         feeding back
 │Extract  │         into triage
 └────┬────┘
      │
      ▼
 ┌──────────────────────┐
 │ Stage 5: Compile     │  Template fill, no LLM needed
 │ morning-brief.md     │  Pure assembly from structured
 │ morning-brief.yaml   │  stage outputs
 └──────────────────────┘
```

Total wall-clock time: roughly 90-120 seconds with parallel extraction. Six LLM calls total (4 extractors + 1 gray-area triage + 1 highlight extraction). Spec assembly is a seventh call per spec type produced.

---

## Design Decisions Worth Noting

**Why structured extraction before synthesis:** The extractors act as an attention mechanism. Instead of asking one LLM call to attend to everything in 200 turns, each extractor only needs to notice one type of pattern. This is the same principle behind mixture-of-experts -- narrow focus yields higher recall.

**Why algorithmic triage before LLM triage:** Reproducibility. If you run the brief twice on the same session, the tiebreakers and low-confidence decisions should always surface. LLM-only categorization drifts between runs. The rules guarantee the critical items always appear; the LLM handles the genuinely ambiguous remainder.

**Why dual format:** The markdown is for the user's morning coffee. The YAML is for the future -- a dashboard, a Slack bot that posts tiebreakers, a script that auto-creates GitHub issues from action items. Building the structured format now costs almost nothing and makes the system composable.

**Why orphaned ideas get special treatment:** In any long generative session, the best ideas often arrive early and get buried by the momentum of later discussion. Explicitly surfacing ideas that had zero follow-up is a form of organizational memory that humans are terrible at and LLMs can do cheaply.


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


---

## The Systems Pragmatist (infrastructure realist)

The Oracle's three-pass pipeline is a good starting point. It's the kind of design that looks clean on a whiteboard. Let me tear into what actually happens when you try to build it.

---

## Morning Brief Generation: The Pragmatist's Take

### What the Oracle Got Right

The three-pass architecture (Extract -> Synthesize -> Render) is fundamentally sound. Parallel extractors are correct -- cognitive task separation genuinely improves LLM output quality. The hybrid tiering (rules-first, LLM-promote-only) is the right instinct. And markdown-first with JSON sidecar is the only sane v1 choice.

But the Oracle skipped every hard part. Let me fill in the gaps.

---

### Failure Mode #1: The Transcript Doesn't Exist Yet

The Oracle's pipeline assumes `sessions/{id}/transcript.md` is a clean, well-structured document. In reality, based on what we actually have today:

- Messages are in-memory `list[Message]` objects with three fields: `role`, `agent_name`, `content`
- There's no persistent session storage
- There's no `decisions.json` -- decisions are buried in freetext responses
- There's no phase metadata, turn numbering, or team attribution beyond agent name

**Before the Morning Brief pipeline can exist, the orchestrator needs to emit structured session data during the run.** Not after. During. This is the actual prerequisite the Oracle glossed over.

**Required session output (written incrementally, not reconstructed):**

```python
@dataclass
class SessionTurn:
    turn_id: int
    timestamp: str
    phase: str                    # brainstorm, refine, specify, review
    direction: str                # "team-a-to-team-b", "internal-team-a", etc.
    agent_name: str
    team: str
    content: str
    content_hash: str             # for dedup / checkpoint verification
    
@dataclass  
class SessionLog:
    session_id: str
    started: str
    teams: dict[str, TeamConfig]
    turns: list[SessionTurn]
    phase_transitions: list[dict] # {from, to, turn_id, reason}
    checkpoints: list[int]        # turn_ids where state was persisted
```

Each turn gets appended to `sessions/{id}/turns.jsonl` (one JSON object per line). Not a single JSON array -- JSONL survives crashes. If the process dies at turn 147, you have 146 complete lines. A single JSON file with an unclosed array bracket gives you nothing.

---

### Failure Mode #2: 200 Turns Won't Fit in One Extraction Call

The Oracle says "each extractor scans the full transcript." Let's do the math.

200 turns. Average agent response: 400-600 tokens. That's 80K-120K tokens of transcript alone. Add the extraction system prompt (~2K tokens) and output schema. You're at 85K-125K tokens input per extractor, times 6 extractors.

This works with Claude's context window today, but it's **the entire context budget spent on input**, leaving minimal room for reasoning. Extraction quality degrades when the model is stuffed to capacity.

**The fix: chunked extraction with merge.**

```
Transcript (200 turns)
    |
    v
[Chunk 1: turns 1-50] [Chunk 2: turns 51-100] [Chunk 3: turns 101-150] [Chunk 4: turns 151-200]
    |                       |                        |                        |
    v                       v                        v                        v
[Extract decisions]    [Extract decisions]     [Extract decisions]      [Extract decisions]
    |                       |                        |                        |
    \______________________\________________________/________________________/
                            |
                            v
                    [Merge + Dedup decisions]
```

Each extractor type runs against each chunk. That's 6 extractors x 4 chunks = 24 parallel calls, each consuming ~30K tokens. Fast, fits comfortably, and each call can actually reason about what it's reading.

The merge step is the tricky part. Decisions can span chunks -- team A proposes in chunk 2, team B agrees in chunk 3. The merger needs overlapping context (last 5 turns of previous chunk included in next chunk) and dedup logic. This is where you get false duplicates and split decisions. The merger prompt needs to be specifically tuned for cross-boundary reconciliation.

**Chunk boundaries should align with phase transitions when possible.** A decision that starts in brainstorm and concludes in refine is already awkward; splitting it mid-sentence across chunks makes it worse.

---

### Failure Mode #3: Extractors Hallucinate Decisions That Never Happened

This is the big one. You ask an LLM to "extract all decisions" from a messy multi-agent transcript, and it will find decisions that don't exist. Two agents vigorously discussing option A vs option B, with one saying "I could see A working" -- the extractor reports "Decision: teams agreed on option A."

**Mitigation: Ground truth anchoring.**

The orchestrator should tag explicit decision moments during the run. When the Director agent (or phase transition logic) detects convergence, it writes a structured decision record:

```json
{"type": "decision_candidate", "turn_id": 142, "summary": "...", "confidence": 0.8}
```

These go into `sessions/{id}/decisions.jsonl` as they happen. The Morning Brief extractor then has two jobs:

1. **Validate** existing decision records against the transcript (did this actually happen?)
2. **Discover** decisions the runtime missed

The extractor output includes a `source` field: `"runtime_logged"` vs `"extracted"`. The synthesis pass treats runtime-logged decisions with higher confidence. Extracted-only decisions get flagged for user confirmation.

Same principle applies to disagreements. If the runtime logged an unresolved disagreement, the extractor confirms it. If the extractor finds one the runtime missed, it's flagged as lower confidence.

---

### Failure Mode #4: Spec Assembly Produces Incoherent Documents

The Oracle says "group fragments by topic, order by phase, assemble." That's the easy case -- when fragments are clean, topically distinct, and non-contradictory.

Reality: spec fragments from brainstorm phase contradict spec fragments from specify phase (because the teams changed their minds). Fragments reference each other implicitly. Some are half-formed sentences that only make sense in conversation context.

**Spec assembly needs a dedicated pass, not a subtask of synthesis.**

```
Pass 2a: Synthesis (tiering, highlights, stats)
Pass 2b: Spec Assembly (separate, document-focused)
```

The spec assembler gets:
- All `spec_fragments[]` from extraction
- The `decisions[]` (to know what was settled)
- The `disagreements[]` (to know what's still open)

Its job:
1. Group fragments into document sections
2. Resolve contradictions using decision log (later decisions override earlier ones)
3. Mark unresolved contradictions with `[CONTESTED: see tiebreaker X-002]`
4. Fill structural gaps with `[GAP: ...]` markers
5. Apply consistent formatting
6. Rate each section: `SOLID` (backed by decisions) / `DRAFT` (discussed but not decided) / `STUB` (minimal content)

Output: standalone artifact files in `sessions/{id}/artifacts/`, not inline in the brief. The brief links to them.

---

### Failure Mode #5: The Synthesis Prompt is Doing Too Much

The Oracle's Pass 2 is one prompt that does tiering, highlight selection, and spec assembly. That's three distinct analytical tasks. The same problem the Oracle correctly identified in Pass 1 (don't bundle cognitive tasks) gets violated in Pass 2.

**Split synthesis into focused steps:**

```
Pass 2a: Tiering
  Input: All extraction outputs
  Output: Tiered items with justifications
  
Pass 2b: Highlight Selection  
  Input: moments[], disagreements[], decisions[]
  Output: 3-5 ranked highlights with turn references
  
Pass 2c: Spec Assembly (described above)
  Input: spec_fragments[], decisions[], disagreements[]
  Output: Draft artifact files

Pass 2d: Executive Summary
  Input: Tiering output, highlights, spec status, session metadata
  Output: 2-3 sentence summary
```

2a and 2b can run in parallel. 2c can run in parallel with both. 2d depends on all three.

---

### The Tiering Algorithm, Made Concrete

The Oracle's rules are directionally right but need tightening. Here's the implementable version:

```python
class TierAssigner:
    """Rule-based tier assignment with LLM refinement."""
    
    def assign_tiers(self, extracted: ExtractionResult) -> TieredResult:
        items = []
        
        # TIER 1: NEEDS TIEBREAKER
        # Unresolved disagreements where both teams made substantive arguments
        for d in extracted.disagreements:
            if d.current_state == "unresolved" and d.position_a and d.position_b:
                items.append(TieredItem(
                    tier=1, 
                    category="tiebreaker",
                    item=d,
                    rule="unresolved_with_both_positions"
                ))
        
        # TIER 2: NEEDS DECISION  
        # Low-confidence decisions (runtime-logged confidence < 0.7)
        for d in extracted.decisions:
            if d.confidence and d.confidence < 0.7:
                items.append(TieredItem(tier=2, category="weak_decision", item=d,
                    rule="low_confidence_decision"))
        
        # Blocking open questions
        for q in extracted.open_questions:
            if q.blocking:
                items.append(TieredItem(tier=2, category="blocking_question", item=q,
                    rule="blocking_open_question"))
        
        # Extracted-only decisions (no runtime confirmation)
        for d in extracted.decisions:
            if d.source == "extracted" and d not in [i.item for i in items]:
                items.append(TieredItem(tier=2, category="unconfirmed_decision", item=d,
                    rule="extracted_only_no_runtime_log"))
        
        # TIER 3: NEEDS INPUT
        # Non-blocking open questions
        for q in extracted.open_questions:
            if not q.blocking and q not in [i.item for i in items]:
                items.append(TieredItem(tier=3, category="open_question", item=q,
                    rule="non_blocking_question"))
        
        # Ideas with conditional reception
        for idea in extracted.ideas:
            if idea.reception in ("conditional", "depends_on_user", "split"):
                items.append(TieredItem(tier=3, category="conditional_idea", item=idea,
                    rule="conditional_reception"))
        
        # TIER 4: FYI
        # Everything else
        remaining = self._get_untiered(extracted, items)
        for item in remaining:
            items.append(TieredItem(tier=4, category="fyi", item=item,
                rule="default"))
        
        return TieredResult(items=items)
    
    async def refine_tiers(self, tiered: TieredResult, transcript_summary: str) -> TieredResult:
        """LLM pass: can promote items (never demote). Must justify."""
        prompt = TIER_REFINEMENT_PROMPT.format(
            items=tiered.to_json(),
            summary=transcript_summary
        )
        response = await self.llm_call(prompt)
        promotions = parse_promotions(response)
        
        for p in promotions:
            if p.new_tier >= p.old_tier:  # enforce: never demote
                continue
            tiered.promote(p.item_id, p.new_tier, p.justification)
        
        return tiered
```

The key design choice: **rules produce the default tiering, LLM can only promote (move to a higher-urgency tier), never demote.** This prevents the known failure mode where the LLM hedges everything down to FYI because it doesn't want to bother the user. The rules guarantee that unresolved disagreements always surface as tiebreakers.

---

### The Complete Pipeline

```
SESSION COMPLETES (or crashes -- pipeline runs on whatever exists)
    |
    v
[Load Session Data]
    sessions/{id}/turns.jsonl          -- incrementally written during run
    sessions/{id}/decisions.jsonl      -- runtime-logged decision candidates  
    sessions/{id}/metadata.json        -- teams, phases, timing, crash info
    |
    v
[Chunk Transcript]
    Split into ~50-turn chunks with 5-turn overlap
    Align boundaries to phase transitions where possible
    |
    v
[PASS 1: Parallel Extraction]  (24 calls: 6 extractors x 4 chunks)
    ExtractDecisions ----\
    ExtractDisagreements -\
    ExtractIdeas ----------> per chunk, merge + dedup after
    ExtractSpecFragments -/
    ExtractMoments ------/
    ExtractOpenQuestions /
    |
    v
[Merge + Dedup]  (programmatic, not LLM)
    Cross-boundary reconciliation
    Dedup by content similarity (embedding distance or hash)
    Anchor to runtime decision log
    |
    v
[PASS 2: Parallel Analysis]
    2a: Tiering (rules + LLM refinement) ---\
    2b: Highlight Selection -----------------+---> wait for all
    2c: Spec Assembly -----------------------/
    |
    v
[PASS 2d: Executive Summary]  (needs 2a + 2b + 2c outputs)
    |
    v
[PASS 3: Render]  (deterministic template, no LLM except exec summary)
    Write: sessions/{id}/morning-brief.md
    Write: sessions/{id}/morning-brief.json
    Write: sessions/{id}/artifacts/*.md       (assembled specs)
    Write: sessions/{id}/ideas-catalog.md     (full idea list)
```

**Total LLM calls for a 200-turn session:**
- Pass 1: 24 extraction calls (parallel, ~30K tokens each)
- Pass 1 merge: 6 merge calls (parallel, ~10K tokens each)
- Pass 2a: 1 tiering call + 1 refinement call
- Pass 2b: 1 highlight call
- Pass 2c: 1-3 spec assembly calls (depends on number of artifacts)
- Pass 2d: 1 executive summary call

**Total: ~35 LLM calls.** At parallel execution, wall-clock time is dominated by the slowest Pass 1 extractor (~30-60 seconds). Full pipeline: **2-3 minutes.** Acceptable for a morning brief generated once per session.

---

### The Crash Case

The Oracle mentioned this nowhere. The whole point of overnight runs is you're not watching.

If the orchestrator crashes at turn 147:
1. `turns.jsonl` has 146 complete lines (JSONL survives partial writes)
2. `decisions.jsonl` has whatever was logged before the crash
3. `metadata.json` may be incomplete -- the pipeline writes a `"status": "crashed"` marker on recovery

The Morning Brief pipeline runs the same way on crashed sessions. The brief gets an additional section at the top:

```markdown
## Session Interrupted

This session crashed at turn 147 of an estimated ~200 turn run.
Phase at crash: specify (entered at turn 112)
Last successful checkpoint: turn 140

The brief below covers turns 1-146. Content from the specify phase may be incomplete.
```

This is why JSONL matters. This is why incremental writes matter. This is why the pipeline doesn't depend on a clean session close.

---

### What the Output Actually Looks Like

I agree with the Oracle: markdown for humans, JSON for machines. But the Oracle's template needs one fix: **the Needs Attention section must come before anything else after the executive summary.** No stats, no highlights, no FYI -- just the stuff that blocks progress. The user should be able to stop reading after that section and still get 80% of the value.

The JSON sidecar (`morning-brief.json`) mirrors the structure but includes:
- All extraction data (not just summaries)
- Turn references as integer ranges (for future UI linking)
- Confidence scores on every extracted item
- The full tiering decision log (which rules fired, any LLM promotions with justifications)

This makes the JSON useful for debugging the pipeline itself, not just for a future UI.

---

### The Honest Assessment

This pipeline has 35 LLM calls, each of which can hallucinate, miss things, or produce malformed JSON. The mitigation is:
1. **Schema validation on every extraction output** -- reject and retry malformed responses
2. **Runtime ground truth** (decisions.jsonl) as anchor -- extractors confirm, not invent
3. **Rules-first tiering** -- LLM refines but can't suppress important items
4. **Deterministic rendering** -- the final output is template-based, not LLM-generated prose (except the exec summary)

The weakest link is spec assembly. Turning scattered conversation fragments into coherent documents is the hardest task in the pipeline, and it's the one most dependent on LLM quality. V1 should set expectations: these are drafts with gap markers, not finished specs. The user's morning includes editing them.

The strongest link is the tiered attention system. Rules guarantee nothing critical gets buried. The user trusts the brief because tiebreakers always surface, not because an LLM decided they were important.


---

