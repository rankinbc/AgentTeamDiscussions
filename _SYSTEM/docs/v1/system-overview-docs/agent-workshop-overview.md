# Agent Workshop

## What It Is

The Agent Workshop is an optional module for creating, tuning, and managing reusable Discussion Agents and agent groups. It provides a simple web UI for visual agent configuration and a library system for saving and reusing agents that have been proven effective through iteration.

It's not required — agent groups can be generated on the fly via Claude from a simple description. The Workshop exists for when you want to go deeper: fine-tune an agent that's almost right, build a curated library of proven agents, or visually compose a balanced group for a specific type of discussion.

## Why It Exists

Generating an agent team is easy. Generating a *good* agent team is an iterative process:

1. You generate a team and run a session
2. You review the output and notice the critic was too aggressive, the ideator too unfocused
3. You tweak traits, adjust voice constraints, tighten the position framing
4. You run again and compare
5. After several cycles, you have agents that consistently produce the kind of thinking you want

Without the Workshop, this iteration happens by hand-editing YAML and mentally tracking what changed. The Workshop makes it visual, trackable, and reusable — turning agent tuning from guesswork into a systematic process.

## How It Fits the System

The Agent Workshop is a companion to the core discussion system, not a dependency:

- **Outputs agent configuration**: Produces the same YAML that the system already consumes. No special format — Workshop-created agents are identical to hand-written ones
- **Connects to Evaluation & Improvement**: The tuning loop depends on being able to see how an agent performed. Workshop should surface evaluation data alongside agent configuration
- **Independent of Conversation Engine**: The Workshop doesn't change how discussions run. It only changes how agents are configured before a session starts
- **Optional by design**: The system works without it. Power users may prefer YAML. New users or visual thinkers may prefer the UI

---

## Agent Configuration Schema

The Workshop exposes the full agent configuration visually. Here's every field the UI needs to handle:

### Identity (required)

| Field | UI Control | Notes |
|---|---|---|
| `id` | Auto-generated | UUID4 GUID. Assigned at creation, never changes. The stable identifier used in session output, group configs, and version history. Display-only in UI (truncated to first 8 chars, clickable to copy full) |
| `name` | Text input | Display name. Required. Can be changed without affecting references — all references use `id` |
| `description` | Textarea | Multi-line narrative: background, expertise, core motivation. Required |

### Personality

**Scalar Traits** — each is a 0.0-1.0 slider with labeled breakpoints:

| Trait | Low (0.0) | Mid (0.5) | High (1.0) |
|---|---|---|---|
| `assertiveness` | Reserved, diplomatic | Balanced | Fights hard, doesn't back down |
| `creativity_temp` | Conventional, proven-path | Balanced | Wildly creative, unexpected ideas |
| `risk_tolerance` | Risk-averse, safety-focused | Balanced | Embraces bold bets, untested approaches |
| `attention_span` | Topic-hopper, jumps freely | Balanced | Deeply focused, drills exhaustively |
| `stubbornness` | Flexible, quick to update | Balanced | Holds ground, requires strong evidence |
| `idea_receptivity` | Agenda driver, redirects to own ideas | Balanced | Builds on others, amplifies their points |
| `bluntness` | Diplomatic, softens criticism | Balanced | Brutally direct, zero sugar-coating |
| `patience` | Cuts tangents, pushes to move on | Balanced | Lets discussions breathe, allows tangents |

The system renders these into natural language at 5 levels:
- 0.0-0.2: "You are strongly [low]"
- 0.2-0.4: "You lean toward [low]"
- 0.4-0.6: "You balance [low] and [high]"
- 0.6-0.8: "You are quite [high]"
- 0.8-1.0: "You are extremely [high]"

**UI requirement**: Show the rendered text next to each slider so the user sees exactly what the agent will read.

**Enumerated Traits:**

| Trait | UI Control | Options |
|---|---|---|
| `cognitive_style` | Dropdown | ANALYTICAL, LATERAL, SYSTEMATIC, INTUITIVE, DIVERGENT |
| `emotional_baseline` | Dropdown | OPTIMISTIC, SKEPTICAL, CURIOUS, CAUTIOUS, NEUTRAL, ENTHUSIASTIC |

**Domain Affinities:**

| Field | UI Control | Notes |
|---|---|---|
| `domain_affinities` | Tag input | Freeform list of domains the agent draws from (e.g., "cognitive science", "game design", "Byzantine history"). Used for cross-domain perspective injection |

### Position

| Field | UI Control | Notes |
|---|---|---|
| `role` | Text input | Stakeholder/functional role. Required. (e.g., "infrastructure realist", "product strategist") |
| `drives` | Multi-line list (3-5 items) | Core motivations this agent pursues |
| `pushback_on` | Multi-line list (3-5 items) | Things this agent actively challenges |
| `intensity` | Slider 0.0-1.0 | 0-0.4: measured restraint. 0.4-0.7: conviction but open. 0.7-1.0: force and passion |

### Technique

| Field | UI Control | Notes |
|---|---|---|
| `primary` | Text input or dropdown with common options | Thinking approach name. Rendered as title case in prompts. Common: cross_pollination, failure_mode_analysis, jobs_to_be_done, divergent_generation, constraint_based |
| `style_description` | Textarea | Prose describing how this technique operates in practice |
| `behaviors` | Multi-line list (5-8 items) | Concrete behavioral rules (e.g., "Name the failure mode before engaging with the happy path") |

### Anti-Slop

| Field | UI Control | Default | Effect |
|---|---|---|---|
| `agreement_tax` | Toggle | ON | Must add substance when agreeing. Pure agreement forbidden |
| `perspective_enforcement` | Toggle | ON | Stay in character even under pressure to agree |
| `devils_advocate_duty` | Toggle | OFF | Must argue against consensus |
| `uncomfortable_idea_quota` | Number (0-5) | 0 | If > 0, must propose uncomfortable idea every N turns (N = max(5, 10-value)) |
| `domain_pivot_trigger` | Toggle | OFF | Cross-domain injection when stuck |

**UI requirement**: Show which rules are active with their rendered text. Inactive rules should be visually dimmed.

### Voice

| Field | UI Control | Notes |
|---|---|---|
| `tone` | Text input | Free-text speaking style (e.g., "blunt and unimpressed", "evocative and nostalgic") |
| `brevity` | Dropdown | concise (<300 words), normal (<600 words), thorough (comprehensive) |
| `vocabulary_hints` | Tag/list input (5-8) | Phrases that fit this agent's style |
| `anti_patterns` | Tag/list input (8-15) | Phrases to NEVER use. Rendered as forbidden slop list |

### Output

| Field | UI Control | Options |
|---|---|---|
| `operating_level` | Radio/dropdown | **requirements** (WHAT/WHY, no code), **design** (tradeoffs, may reference tech), **implementation** (concrete, schemas, code patterns) |
| `job` | Radio/dropdown | **propose** (generate solutions), **critique** (find problems), **evaluate** (assess feasibility/impact), **simplify** (find minimum viable), **ideate** (3+ novel ideas from non-software domains) |

---

## Web UI Design

### Architecture

```
Browser (SPA)
    ↕ REST API (JSON)
FastAPI Server
    ↕ File I/O
YAML Files (agent library + group configs)
```

- **Backend**: FastAPI (Python) — lightweight, async, already in the project's ecosystem
- **Frontend**: Vanilla JS + a minimal CSS framework (e.g., Pico CSS, Simple.css) or htmx for dynamic updates. No React/Vue/Angular — keep the dependency footprint tiny
- **Storage**: YAML files in a `library/` directory structure. No database
- **Runs locally**: `python -m workshop` starts the server on localhost

### Directory Structure

```
config/
  agents/                    # Workshop-managed individual agent configs
    {guid}.yaml              # One file per agent, named by GUID
  groups/                    # Workshop-managed group compositions
    {group-id}.yaml          # Agent references by GUID + role assignments
  actions/                   # Action definitions
    failure_postmortem.yaml
    steal_mechanism.yaml
    ...
  archetypes/                # Starter templates for new agent creation
    critic.yaml
    ideator.yaml
    pragmatist.yaml
    advocate.yaml
    architect.yaml
    synthesizer.yaml
  teams/                     # Legacy: self-contained team YAMLs (bypass Workshop)
    beta-agents.yaml
    ...
```

The existing `config/teams/` path continues to work — self-contained team YAMLs that don't require the Workshop. The `config/agents/` + `config/groups/` path is the decomposed version used by the Workshop. The session runner accepts either format.

### API Endpoints

```
# Agents
GET    /api/agents                    # List all agents (summary: id, name, role, key traits)
GET    /api/agents/{id}               # Full agent config
POST   /api/agents                    # Create agent (from JSON body)
PUT    /api/agents/{id}               # Update agent
DELETE /api/agents/{id}               # Delete agent
POST   /api/agents/{id}/clone         # Clone agent with new ID
POST   /api/agents/{id}/test          # Run single-turn test (send prompt, get response)

# Groups
GET    /api/groups                    # List all groups
GET    /api/groups/{id}               # Full group config with resolved agents
POST   /api/groups                    # Create group
PUT    /api/groups/{id}               # Update group
DELETE /api/groups/{id}               # Delete group
POST   /api/groups/{id}/export        # Export as session-ready YAML

# Generation
POST   /api/generate/agent            # AI-generate agent from natural language description
POST   /api/generate/group            # AI-generate full group from description

# Archetypes
GET    /api/archetypes                # List starter templates

# Prompt preview
POST   /api/preview/prompt            # Render system prompt from agent config (no save)

# Import
POST   /api/import/yaml               # Import existing team YAML file into library
```

### Views

#### 1. Agent Library (Home)

The landing page. Shows all saved agents as cards in a grid.

**Each card shows:**
- Agent name and role
- Key trait badges (top 3 distinctive traits — those furthest from 0.5)
- Cognitive style + emotional baseline icons/labels
- Job type badge (propose/critique/evaluate/simplify/ideate)
- Tags (user-assigned)

**Actions:**
- Search/filter by name, role, tag, job type
- Sort by name, last modified, most used
- Create new (blank, from archetype, AI-generate)
- Import from existing YAML
- Click card → Agent Editor

#### 2. Agent Editor

The main configuration view. Two-column layout:

**Left column — Configuration panels** (collapsible sections):

*Identity*
- Name (text)
- Description (textarea with character count)
- Role (text)
- Tags (for library organization — not part of the agent config itself)

*Personality*
- 8 horizontal sliders, each with:
  - Trait name on the left
  - Slider with current value
  - Rendered description on the right (updates live as slider moves)
- Cognitive style dropdown
- Emotional baseline dropdown
- Domain affinities tag input

*Position*
- Drives: ordered list with add/remove/reorder
- Pushback: ordered list with add/remove/reorder
- Intensity slider with rendered label

*Technique*
- Primary technique (text input with autocomplete from known techniques)
- Style description (textarea)
- Behaviors: ordered list with add/remove/reorder

*Anti-Slop*
- Toggle switches for each mechanism
- Uncomfortable idea quota: number spinner (only visible when toggled on)
- Active rules shown with their rendered prompt text
- Inactive rules dimmed

*Voice*
- Tone (text)
- Brevity (dropdown)
- Vocabulary hints: tag input
- Anti-patterns: tag input

*Output*
- Operating level (radio buttons with description)
- Job type (radio buttons with description)

**Right column — Live Preview** (sticky, scrolls with content):

*System Prompt Preview*
- Full rendered prompt as the agent will see it
- Updates live as any config value changes
- Token count estimate at the top
- Sections color-coded to match which config panel produced them
- Collapsible sections for scanning

*Quick Test* (expandable panel at bottom of preview):
- Text input for a test prompt
- "Run" button → sends prompt to Claude with current config → shows response
- Response displayed inline with timing info
- History of test runs (last 5) for quick comparison

#### 3. Group Composer

For assembling agents into a discussion group.

**Top section — Agent Slots:**
- Drop zones for agents (drag from library sidebar or search to add)
- Each slot shows agent card (compact) with role assignment dropdown (propose/critique/evaluate)
- Round assignment: which agents participate in which round
- Remove button per slot
- "Add agent" button → opens library picker or generates new

**Middle section — Balance Analysis:**

*Trait Distribution Chart*
- Radar/spider chart showing the group's spread across personality dimensions
- Overlay individual agent points on the group average
- Highlight dimensions with low spread (agents too similar) or gaps (no coverage)

*Role Coverage*
- Visual indicator: how many proposers, critics, evaluators
- Warning if a round has no agents assigned
- Warning if all agents have the same job type

*Anti-Slop Coverage*
- Which mechanisms are active across the group
- Warning if no agent has devil's advocate duty
- Warning if agreement tax is off for everyone

*Cognitive Diversity*
- Distribution of cognitive styles and emotional baselines
- Flag if all agents share the same style

**Bottom section — Actions:**
- Save as group template
- Export as YAML (session-ready format)
- Load existing team YAML for editing

#### 4. Comparison View

For tuning iteration — see how changes affect output.

**Layout**: Two agents side by side (or before/after versions of the same agent)

**Top — Trait Diff:**
- Side-by-side trait values with differences highlighted
- Changed values shown in color with delta (e.g., assertiveness: 0.6 → 0.8 (+0.2))

**Middle — Prompt Diff:**
- Side-by-side rendered prompts with differences highlighted (like a code diff)

**Bottom — Output Comparison:**
- Same test prompt sent to both configurations
- Responses displayed side by side
- Word count, stance analysis, key claim extraction for each

---

## Test Run Capability

Critical for the tuning loop. Without it, you'd need to run a full session to test a change.

### How It Works

1. User edits an agent in the Agent Editor
2. User types a test prompt in the Quick Test panel (or selects from saved test prompts)
3. Workshop calls `claude -p` with the current agent's rendered system prompt + the test prompt
4. Response displayed in the preview panel with timing
5. User adjusts traits, runs again, compares

### Test Prompt Library

Pre-built test prompts for common evaluation scenarios:
- "Here's a proposal for X. What's wrong with it?" (tests critique quality)
- "Generate 3 approaches to solve Y." (tests ideation range)
- "Evaluate this design decision: Z." (tests evaluation depth)
- "Someone just proposed [consensus opinion]. Respond." (tests anti-slop effectiveness)
- Custom user-saved prompts

### Implementation

```python
async def test_agent(agent_config: dict, prompt: str) -> dict:
    system_prompt = build_system_prompt(AgentConfig(**agent_config))
    response = await run_claude_async(
        system_prompt=system_prompt,
        message=prompt,
        timeout=60
    )
    return {
        "response": response,
        "token_estimate": len(system_prompt.split()) + len(prompt.split()),
        "timestamp": datetime.now().isoformat()
    }
```

Uses the same `claude_runner` the discussion system uses — no separate integration.

---

## AI-Assisted Generation

### Agent Generation

```
POST /api/generate/agent
Body: { "description": "a skeptical infrastructure engineer who thinks in failure modes" }
```

Calls Claude with a meta-prompt that:
1. Takes the natural language description
2. Generates a complete agent config (all fields)
3. Returns JSON matching the schema
4. Workshop displays it in the editor for review/adjustment

The generation prompt should include the full schema with field descriptions and example values from existing agents, so Claude produces well-calibrated output.

### Group Generation

```
POST /api/generate/group
Body: { "description": "a team for evaluating SaaS product ideas, focus on market fit and technical feasibility" }
```

Generates 5-7 agents with complementary roles and assigns them to rounds. Returns a complete group config.

---

## Version History

Each agent file tracks its own history:

```yaml
# library/agents/a1b2c3d4-e5f6-7890-abcd-ef1234567890.yaml
id: a1b2c3d4-e5f6-7890-abcd-ef1234567890
name: The Pragmatist
description: ...
personality:
  assertiveness: 0.7
  # ...

_meta:
  created: 2026-03-25T10:00:00
  modified: 2026-03-26T14:30:00
  version: 3
  tags: [critique, infrastructure, proven]
  notes: "v3: increased stubbornness from 0.5 to 0.7 — was yielding too easily in critique rounds"
  history:
    - version: 1
      date: 2026-03-25T10:00:00
      note: "Initial generation from archetype"
    - version: 2
      date: 2026-03-25T22:00:00
      note: "Reduced creativity_temp from 0.7 to 0.4 — too many wild suggestions in evaluate round"
    - version: 3
      date: 2026-03-26T14:30:00
      note: "Increased stubbornness — was yielding too easily"
```

The `_meta` section is Workshop-only metadata. It's stripped when exporting to session-ready YAML (the discussion system ignores it, but cleaner to strip).

---

## Key Design Constraints

- **Optional**: The system works identically without the Workshop. It produces standard YAML, nothing more
- **No lock-in**: Agents created in the Workshop are plain YAML files. Edit by hand, generate with Claude, or manage however you want
- **Simple**: Functional UI over polished UI. No accounts, no cloud, no deployment complexity
- **File-based**: Agent library is a directory of YAML files, not a database. Consistent with the rest of the system
- **Same tools**: Uses the same `claude_runner` and `prompt_builder` as the discussion system. No parallel implementations

## Interactions

| Component | Relationship |
|---|---|
| Discussion Agents | Workshop produces the configuration that defines agents |
| Creativity Engine | Workshop exposes Creativity Engine parameters (traits, anti-slop, voice) as visual controls |
| Evaluation & Improvement | Evaluation data informs tuning decisions; Workshop surfaces this alongside agent config |
| Conversation Engine | No direct interaction — Workshop configures agents, engine runs them |
| Session Platform | No direct interaction — but session output informs Workshop tuning decisions |
| Context Management | No direct interaction |

## Current State

Not yet implemented. Agent configuration is currently YAML-only, hand-edited or AI-generated. The Workshop is a V1 module — it makes the existing configuration system more accessible and supports the iteration loop that produces better agents over time.
