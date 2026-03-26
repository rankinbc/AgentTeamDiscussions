# Agent Actions

## What It Is

Agent Actions are discrete capabilities that agents can perform during their turn beyond their standard discussion response. An action might be a structured thinking exercise ("List 5 ways this could fail in production"), a creativity prompt ("Reframe this problem from the user's perspective"), or — in V2 — an external tool call (web search, API lookup, document retrieval).

Actions are the system's mechanism for making agents *do* specific things at specific moments, rather than just respond to whatever's in their context.

## Why It Exists

Without actions, every agent turn is the same shape: receive context + directive → produce a discussion response. This works for general debate, but some of the most valuable contributions come from specific, directed cognitive tasks:

- A proposer told to "steal a mechanism from a completely different industry" produces more novel output than one told to "propose a solution"
- A critic told to "write the post-mortem for when this fails" finds different problems than one told to "find problems"
- An evaluator told to "list the top 5 assumptions this design makes" produces more actionable output than one told to "evaluate this"

Actions are how the system gets this specificity without hard-coding it into the round structure. They're configurable, assignable, and composable — the building blocks of more sophisticated discussion patterns.

## How It Fits the System

Actions sit between the Conversation Engine (which decides *when* to fire them) and Discussion Agents (which *execute* them):

- **Defined in configuration**: Actions are declared as named, reusable definitions — either globally or per-agent
- **Triggered by Conversation Engine**: The engine decides when to inject an action based on rules (round assignment, schedule, convergence detection)
- **Executed by Discussion Agents**: An action modifies the agent's task directive for that turn. The agent doesn't "choose" to use an action — it receives one
- **Configurable in Agent Workshop**: Actions can be assigned to agents, rounds, or trigger conditions via the UI
- **Results captured by Session Platform**: Action outputs are persisted like any other agent response

## Two Types of Actions

### Type 1: Prompt-Based Actions (V1)

A prompt-based action is a structured directive injected into the agent's task layer. It shapes *how* the agent thinks on that turn without any external calls.

**Examples:**

| Action Name | Directive | Best For |
|---|---|---|
| `failure_postmortem` | "Write the post-mortem report for when this design fails in production. What went wrong? What did we miss?" | Critique rounds |
| `steal_mechanism` | "Identify a mechanism from a completely different industry (hospitality, aviation, gaming, medicine) that could solve this problem. Explain the analogy concretely." | Propose rounds |
| `assumption_audit` | "List every assumption this design makes. For each, rate how likely it is to be wrong and what breaks if it is." | Evaluate rounds |
| `user_reframe` | "Forget the technical discussion. You are the end user. Walk through trying to use this. Where do you get confused, frustrated, or stuck?" | Any round |
| `edge_case_hunt` | "Identify 5 edge cases nobody has mentioned. For each, describe the scenario and what the system should do." | Specify phase |
| `minimum_viable` | "Strip this design to the absolute minimum that would test the core hypothesis. What can be cut without losing the learning?" | Refine phase |
| `competitive_scan` | "Based on your knowledge, how do existing products solve this same problem? What can we learn from their approach — and where should we deliberately differ?" | Brainstorm phase |
| `dependency_map` | "List every external dependency this design has (APIs, services, libraries, data sources). For each, what's the fallback if it's unavailable?" | Specify phase |
| `new_feature_ideation` | "Think of a new feature that would make this product easier to use. Describe the user need it addresses and why it matters." | Brainstorm phase |

These are just prompt engineering — the agent receives an extra directive alongside its normal task. No new infrastructure required.

### Type 2: Tool-Based Actions (V2)

A tool-based action makes an external call and feeds results back into the agent's context. These require a multi-step turn: agent turn → tool execution → result injection → (optional) agent follow-up turn.

**Examples:**

| Action Name | Execution | Result |
|---|---|---|
| `web_search` | Search the web for a query derived from the discussion | Search results summary injected into next turn's context |
| `api_check` | Verify that a specific API/library supports a claimed capability | Factual confirmation or denial |
| `doc_lookup` | Retrieve relevant documentation for a technology mentioned in discussion | Extracted documentation snippet |
| `prior_session` | Pull relevant decisions from a previous session on a related topic | Historical context injection |

Tool-based actions are V2 scope because they change the turn model fundamentally. V1's "one call in, one response out" is simple and crash-resilient. Multi-step turns add state management complexity.

**V1 preparation**: Even though tool-based actions aren't V1, the action system should be designed so tool-based actions can be added later without restructuring. The action definition format should support a `type` field (prompt vs. tool) from the start.

---

## Action Definition Format

Actions are defined as reusable configurations:

```yaml
actions:
  failure_postmortem:
    name: "Failure Post-Mortem"
    type: prompt                          # prompt (V1) or tool (V2)
    description: "Agent writes the post-mortem for when this design fails"
    directive: |
      Write the post-mortem report for when this design fails in production.
      What went wrong? What did we miss? What were the warning signs we ignored?
      Be specific — name the component, the failure mode, and the blast radius.
    tags: [critique, risk, quality]
    recommended_for:
      rounds: [critique, evaluate]        # Suggested round assignments
      phases: [specify, review]           # Suggested phase assignments

  steal_mechanism:
    name: "Cross-Industry Mechanism"
    type: prompt
    description: "Agent borrows a mechanism from a different industry"
    directive: |
      Identify a mechanism from a completely different industry
      (hospitality, aviation, gaming, medicine, logistics, military)
      that could solve the problem being discussed.
      Name the industry, the specific mechanism, and explain the analogy concretely.
      Don't be abstract — show how it would work HERE.
    tags: [creativity, ideation, divergent]
    recommended_for:
      rounds: [propose]
      phases: [brainstorm]

  # V2 example — tool-based
  web_search:
    name: "Web Search"
    type: tool                            # V2
    description: "Search the web to verify a claim or find information"
    tool_config:                          # V2
      handler: web_search
      max_results: 5
      timeout: 30
    tags: [research, verification]
    recommended_for:
      rounds: [evaluate]
      phases: [specify, review]
```

---

## Trigger Model

The Conversation Engine decides when to fire actions. Three trigger mechanisms, all V1-compatible:

### 1. Configuration-Driven (Primary)

Actions are assigned in the agent or group config:

```yaml
# Per-agent assignment
agents:
  the_pragmatist:
    name: "The Pragmatist"
    # ... personality, position, etc.
    actions:
      always: [failure_postmortem]              # Every turn
      rounds:
        critique: [assumption_audit]            # Only in critique rounds
        evaluate: [dependency_map]              # Only in evaluate rounds
      phases:
        brainstorm: [steal_mechanism]           # Only in brainstorm phase
```

```yaml
# Per-round assignment (in group config)
groups:
  product_planning:
    rounds:
      propose:
        actions: [new_feature_ideation]         # All proposers get this
      critique:
        actions: [failure_postmortem, edge_case_hunt]  # All critics get these
```

This is the simplest model — fully declarative, no runtime decisions.

### 2. Engine-Scheduled

The Conversation Engine injects actions based on rules:

```yaml
# In session or engine config
action_schedule:
  - action: steal_mechanism
    every_n_turns: 5                           # Inject every 5th turn
    target: highest_creativity_temp            # Give to the most creative agent

  - action: assumption_audit
    on_convergence: true                       # When agents are agreeing too much
    target: devils_advocate                    # Give to whoever has devil's advocate duty

  - action: user_reframe
    on_phase_transition: true                  # At every phase boundary
    target: all                                # Everyone gets it
```

More dynamic — responds to discussion state. Still deterministic (rule-based, not agent-decided).

### 3. Signal-Requested (Lightweight)

Agents can signal that an action would help, and the engine decides whether to grant it:

The agent's existing `needs` signal metadata already supports this:
```
needs: more-research | counter-argument | evidence | team-input
```

Extended to include action requests:
```
needs: action:failure_postmortem | action:competitive_scan
```

The engine sees the request and decides whether to inject it on the agent's next turn. The agent doesn't execute it directly — it requests, the engine grants or ignores.

This is the lightest form of agent-initiated actions without giving agents autonomous tool use.

---

## How Actions Modify a Turn

An action modifies the **task layer** of the agent's context (Layer 3). The standard task directive is augmented, not replaced:

**Without action:**
```
## Your Task
Critique the proposals from the previous round. Find problems, gaps, and
risks. Be specific about what breaks and why.

[Round context: propose round output...]
```

**With `failure_postmortem` action:**
```
## Your Task
Critique the proposals from the previous round. Find problems, gaps, and
risks. Be specific about what breaks and why.

## Action: Failure Post-Mortem
In addition to your critique, write the post-mortem report for when this
design fails in production. What went wrong? What did we miss? What were
the warning signs we ignored? Be specific — name the component, the failure
mode, and the blast radius.

[Round context: propose round output...]
```

The action is additive. The agent still does its normal job (critique) but with an additional structured exercise that shapes its thinking.

**Multiple actions per turn**: An agent can receive multiple actions on a single turn. They're concatenated in the task layer. Keep it to 2-3 max to avoid diluting the agent's focus.

---

## Actions in the Agent Workshop

The Workshop UI should support action management:

### Action Library
- Browse/search available actions
- Create new actions (name, type, directive, tags, recommendations)
- Test actions in isolation (Quick Test with action injected)

### Agent Editor Integration
- "Actions" panel in the agent editor
- Assign actions to the agent with trigger rules (always, per-round, per-phase)
- Preview how the action modifies the rendered prompt

### Group Composer Integration
- Assign actions at the round level
- Visualize which agents get which actions in each round
- Action coverage view: are there rounds with no actions? Overloaded turns with too many?

---

## Starter Action Library

Ship with 10-15 proven prompt-based actions:

**Critique actions:**
- `failure_postmortem` — Write the failure post-mortem
- `assumption_audit` — List and rate every assumption
- `edge_case_hunt` — Find 5 unmentioned edge cases
- `attack_surface` — Identify ways this could be abused or misused

**Propose actions:**
- `steal_mechanism` — Borrow from another industry
- `new_feature_ideation` — Invent a feature for a specific user need
- `constraint_flip` — What if the biggest constraint didn't exist? What would you build?
- `minimum_viable` — Strip to the smallest testable version

**Evaluate actions:**
- `user_reframe` — Experience this as the end user
- `dependency_map` — Map every external dependency and fallback
- `competitive_scan` — How do existing products handle this?
- `build_vs_buy` — For each component, should we build it or use an existing solution?

**General actions:**
- `summarize_progress` — What have we decided? What's still open?
- `blocked_items` — What can't move forward without more information?
- `priority_stack_rank` — Force-rank the open items by importance

---

## Key Design Constraints

- **Additive, not replacement**: Actions augment the normal turn directive. They don't replace the agent's job
- **Engine-controlled**: Agents don't autonomously decide to use actions (V1). The engine or config determines when actions fire
- **Prompt-only in V1**: No external calls, no multi-step turns. Just structured directives
- **Composable**: Actions can be mixed and matched across agents, rounds, and phases
- **Reusable**: Actions are defined once and referenced by name. Same action can be used by different agents in different groups
- **Future-proof**: The definition format supports `type: tool` for V2 tool-based actions without restructuring

## Interactions

| Component | Relationship |
|---|---|
| Conversation Engine | Decides when to inject actions based on config, schedule, or signals |
| Discussion Agents | Execute actions as part of their turn (receive augmented task directive) |
| Context Management | Actions are injected into the task layer (Layer 3) of the context payload |
| Creativity Engine | Some actions reinforce creativity goals (steal_mechanism, constraint_flip) |
| Agent Workshop | UI for creating, assigning, and testing actions |
| Session Platform | Action outputs persisted with the turn — no separate storage |

## Current State

Not yet implemented. The concept builds on the existing task directive system — the Conversation Engine already gives agents per-turn instructions. Actions formalize and extend this into a configurable, reusable system. Prompt-based actions require no new infrastructure beyond the action definition format and injection logic in the Conversation Engine.
