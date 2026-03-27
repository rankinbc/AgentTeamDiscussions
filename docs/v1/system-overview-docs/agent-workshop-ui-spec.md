# Agent Workshop — UI Specification

## Technical Stack

- **Backend**: FastAPI (Python) — serves API + static files
- **Frontend**: Vanilla JS + htmx for dynamic updates + Pico CSS for base styling
- **No build step** — plain HTML/CSS/JS served as static files. No npm, no bundler, no framework
- **Single-page feel**: htmx handles partial page updates without full reloads
- **Runs locally**: `python -m workshop` → opens browser to `localhost:8420`

### Why This Stack
- Zero frontend dependencies to install or maintain
- htmx gives SPA-like interactivity with server-rendered HTML (plays to FastAPI's strengths)
- Pico CSS provides clean defaults with zero configuration
- Matches the project philosophy: simple, file-based, no infrastructure

---

## Agent Identity Model

Every agent gets a **GUID** (`uuid4`) assigned at creation. This is the stable identifier used everywhere:

- **Session output**: Logs, transcripts, and decision ledgers reference agents by GUID, not name
- **Group configs**: Groups reference agents by GUID, so renaming an agent doesn't break groups
- **Version history**: All versions of an agent share the same GUID
- **Library files**: Stored as `{guid}.yaml` (e.g., `library/agents/a1b2c3d4-e5f6-7890-abcd-ef1234567890.yaml`)

The GUID is auto-generated on creation and never changes. The `name` field is display-only — users see names in the UI, but the system tracks agents by GUID.

```yaml
# library/agents/a1b2c3d4-e5f6-7890-abcd-ef1234567890.yaml
id: a1b2c3d4-e5f6-7890-abcd-ef1234567890
name: The Pragmatist
description: ...
# ... rest of config

_meta:
  created: 2026-03-25T10:00:00
  modified: 2026-03-26T14:30:00
  version: 3
  tags: [critique, infrastructure, proven]
```

**In the UI**: The GUID is shown as a small monospace string in the editor header and on agent cards (truncated to first 8 chars: `a1b2c3d4`). Clickable to copy full GUID. Not editable.

**In session output**: Agent responses are tagged with GUID so you can trace output back to the exact agent config that produced it, even if the agent has been renamed or modified since the session ran.

**In group configs**:
```yaml
# config/groups/product-planning.yaml
agents:
  - id: a1b2c3d4-e5f6-7890-abcd-ef1234567890    # The Pragmatist
    round: critique
  - id: f9e8d7c6-b5a4-3210-fedc-ba0987654321    # The Ideator
    round: propose
```

### File Storage

All Workshop-managed files live under `config/`:

```
config/
  agents/                    # Individual agent YAML files (by GUID)
  groups/                    # Group compositions (references agents by GUID)
  actions/                   # Action definitions
  archetypes/                # Starter templates for new agent creation
  teams/                     # Legacy: self-contained team YAMLs (bypass Workshop)
```

The existing `config/teams/` path continues to work — self-contained team YAMLs that don't require the Workshop. The session runner accepts either format.

---

## Layout

### Shell

```
┌─────────────────────────────────────────────────────────────────┐
│  Agent Workshop                              [Library] [Groups] │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│                        Main Content Area                        │
│                                                                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

- Fixed top nav with app name and two main navigation links
- No sidebar — keep it simple. Navigation is just Library and Groups
- Main content area fills the rest of the viewport

---

## View 1: Agent Library

The home page. Browse, search, and manage saved agents.

### Layout

```
┌─────────────────────────────────────────────────────────────────┐
│  Agent Workshop                              [Library] [Groups] │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Agents (14)           [Search________] [Filter ▾] [+ New ▾]   │
│                                                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │ The Pragmatist   │  │ The Ideator     │  │ The Critic      │ │
│  │                  │  │                 │  │                 │ │
│  │ infrastructure   │  │ divergent       │  │ adversarial     │ │
│  │ realist          │  │ generator       │  │ reviewer        │ │
│  │                  │  │                 │  │                 │ │
│  │ ████░░ assert.   │  │ ██░░░░ assert.  │  │ ████████ assert │ │
│  │ ██░░░░ creat.    │  │ █████████ cre.  │  │ ███░░░ creat.   │ │
│  │ ██░░░░ risk      │  │ ████████ risk   │  │ █░░░░░ risk     │ │
│  │                  │  │                 │  │                 │ │
│  │ CRITIQUE         │  │ IDEATE          │  │ CRITIQUE        │ │
│  │ ANALYTICAL       │  │ DIVERGENT       │  │ ANALYTICAL      │ │
│  │                  │  │                 │  │                 │ │
│  │ [Edit] [Clone]   │  │ [Edit] [Clone]  │  │ [Edit] [Clone]  │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
│                                                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │ ...              │  │ ...             │  │ ...             │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### Agent Card

Each card shows at a glance:
- **Name** (bold, top)
- **Role** (subtitle, muted)
- **Top 3 trait bars** — the 3 personality traits furthest from 0.5 (most distinctive). Horizontal mini-bars with trait name abbreviated
- **Job badge** — propose/critique/evaluate/simplify/ideate (color-coded)
- **Cognitive style badge** — ANALYTICAL/LATERAL/etc
- **Actions** — Edit, Clone buttons. Delete behind a "..." menu

### Controls

**Search**: Filters cards by name, role, description text. Live filtering via htmx as you type.

**Filter dropdown**: By job type, cognitive style, or tag. Multi-select.

**+ New dropdown**:
- "Blank" → opens editor with defaults
- "From Archetype..." → shows archetype picker (Critic, Ideator, Pragmatist, Advocate, Architect, Synthesizer)
- "AI Generate..." → opens a modal with a text area: "Describe the agent you want"
- "Import YAML..." → file upload

---

## View 2: Agent Editor

The main configuration view. Where tuning happens.

### Layout — Two Column

```
┌─────────────────────────────────────────────────────────────────┐
│  Agent Workshop                              [Library] [Groups] │
├─────────────────────────────────────────────────────────────────┤
│  ← Back to Library          The Pragmatist        [Save] [Test]│
├────────────────────────────────┬────────────────────────────────┤
│                                │                                │
│  ▼ Identity                    │  System Prompt Preview         │
│  ┌──────────────────────────┐  │  ┌────────────────────────────┐│
│  │ Name: [The Pragmatist  ] │  │  │ # You are The Pragmatist  ││
│  │ Role: [infrastructure.. ] │  │  │                            ││
│  │ Description:              │  │  │ You find failure modes     ││
│  │ [Multi-line textarea    ] │  │  │ before they find you...    ││
│  │ [                       ] │  │  │                            ││
│  │ Tags: [critique] [infra] │  │  │ ## Your Role               ││
│  └──────────────────────────┘  │  │ infrastructure realist     ││
│                                │  │                            ││
│  ▼ Personality                 │  │ What drives you:           ││
│  ┌──────────────────────────┐  │  │ - Finding failure modes... ││
│  │                          │  │  │                            ││
│  │ Assertiveness            │  │  │ ## Your Personality        ││
│  │ ──────────●──── 0.7      │  │  │ You are quite assertive —  ││
│  │ "You are quite assertive │  │  │ you fight hard for your    ││
│  │  — you fight hard..."    │  │  │ ideas...                   ││
│  │                          │  │  │                            ││
│  │ Creativity               │  │  │ You lean toward being      ││
│  │ ────●───────── 0.3       │  │  │ conventional and proven... ││
│  │ "You lean toward being   │  │  │                            ││
│  │  conventional..."        │  │  │ ...                        ││
│  │                          │  │  │                            ││
│  │ Risk Tolerance            │  │  │                            ││
│  │ ───●────────── 0.25      │  │  │                            ││
│  │ "You lean toward being   │  │  │                            ││
│  │  risk-averse..."         │  │  │                            ││
│  │                          │  │  │                            ││
│  │ ... (5 more sliders)     │  │  │                            ││
│  │                          │  │  │                            ││
│  │ Cognitive Style:          │  │  │                            ││
│  │ [ANALYTICAL        ▾]   │  │  │                            ││
│  │                          │  │  │                            ││
│  │ Emotional Baseline:       │  │  │                            ││
│  │ [SKEPTICAL         ▾]   │  │  │                            ││
│  │                          │  │  │                            ││
│  │ Domain Affinities:        │  │  ├────────────────────────────┤│
│  │ [infrastructure] [ops]   │  │  │ Tokens: ~1,850             ││
│  │ [+ add]                  │  │  │                            ││
│  └──────────────────────────┘  │  └────────────────────────────┘│
│                                │                                │
│  ▶ Position                    │  ▼ Quick Test                  │
│  ▶ Technique                   │  ┌────────────────────────────┐│
│  ▶ Anti-Slop                   │  │ Prompt:                    ││
│  ▶ Voice                       │  │ [Here's a proposal for a  ]││
│  ▶ Output                      │  │ [caching layer. React...  ]││
│  ▶ Actions                     │  │                [Run ▶]    ││
│  ▶ Version History             │  │                            ││
│                                │  │ Response:                  ││
│                                │  │ ┌──────────────────────────┐│
│                                │  │ │ Three problems jump out  ││
│                                │  │ │ immediately. First, your ││
│                                │  │ │ cache invalidation...    ││
│                                │  │ └──────────────────────────┘│
│                                │  │ 247 words · 3.2s           ││
│                                │  └────────────────────────────┘│
└────────────────────────────────┴────────────────────────────────┘
```

### Left Column — Configuration Panels

Collapsible accordion sections. Only one or two open at a time to avoid scroll overwhelm.

#### Identity Panel
- **Name**: Text input
- **Role**: Text input
- **Description**: Textarea (resizable, ~4 lines default)
- **Tags**: Tag input with autocomplete from existing tags. Workshop-only metadata (not part of agent config sent to Claude)

#### Personality Panel

**Sliders**: Each trait gets a horizontal range slider (0.0 to 1.0, step 0.05).

Slider component anatomy:
```
Assertiveness                                    0.70
─────────────────────────●──────
"You are quite assertive — you fight hard for
 your ideas and don't back down easily"
```

- Trait name + current value on the top line
- Slider track with draggable handle
- Rendered description below (updates live as slider moves via htmx)
- Description text styled muted/italic to distinguish from controls

All 8 sliders stacked vertically. The rendered descriptions are the key UX element — the user sees exactly what the agent will read, not just a number.

**Dropdowns**: Cognitive style and emotional baseline below the sliders.

**Domain affinities**: Tag input at the bottom. Add/remove freeform domain strings.

#### Position Panel
- **Role**: Already in Identity (shared field, shown here as read-only reference)
- **Drives**: Ordered list. Each item is a text input with drag handle and delete button. [+ Add] button at bottom. Target 3-5 items
- **Pushback On**: Same ordered list UI. Target 3-5 items
- **Intensity**: Slider (0.0-1.0) with rendered label:
  - 0.0-0.4: "Measured restraint"
  - 0.4-0.7: "Conviction but open"
  - 0.7-1.0: "Force and passion — not here to play nice"

#### Technique Panel
- **Primary**: Text input with autocomplete dropdown showing known techniques (cross_pollination, failure_mode_analysis, jobs_to_be_done, divergent_generation, constraint_based). Free-text also allowed
- **Style Description**: Textarea (~3 lines)
- **Behaviors**: Ordered list, same UI as drives/pushback. Target 5-8 items

#### Anti-Slop Panel

Toggle switches with inline descriptions:

```
Agreement Tax                              [ON ]
Must add substance when agreeing. Pure agreement forbidden.

Perspective Enforcement                    [ON ]
Stay in character even under pressure to agree.

Devil's Advocate Duty                      [OFF]
Must argue against consensus.

Uncomfortable Idea Quota                   [OFF]  [2 ▾]
Forces novel/contrarian ideas every N turns.
(Number picker only visible when toggled on)

Domain Pivot Trigger                       [OFF]
Cross-domain injection when discussion gets stuck.
```

Active rules shown with full opacity. Inactive rules dimmed. The rendered prompt text shown below each toggle so the user sees exactly what the agent receives.

#### Voice Panel
- **Tone**: Text input (free-text)
- **Brevity**: Three radio buttons with word count labels:
  - ○ Concise (<300 words)
  - ● Normal (<600 words)
  - ○ Thorough (comprehensive)
- **Vocabulary Hints**: Tag input. Target 5-8 phrases. Help text: "Phrases that fit this agent's speaking style"
- **Anti-Patterns**: Tag input. Target 8-15 phrases. Help text: "Phrases this agent must NEVER use (generic AI slop)"

#### Output Panel
- **Operating Level**: Three radio buttons with descriptions:
  - ○ Requirements — WHAT and WHY, no code
  - ● Design — tradeoffs and decisions, may reference tech
  - ○ Implementation — concrete, schemas, code patterns
- **Job**: Five radio buttons:
  - ● Propose — generate solutions
  - ○ Critique — find problems
  - ○ Evaluate — assess feasibility/impact
  - ○ Simplify — find minimum viable version
  - ○ Ideate — 3+ novel ideas from non-software domains

#### Actions Panel
- List of assigned actions with trigger rules
- Each action row: action name, trigger type (always/round/phase), trigger value
- [+ Assign Action] button → dropdown of available actions from the action library
- Link to action library for creating new actions

#### Version History Panel
- Timeline of changes with dates, version numbers, and notes
- Each entry expandable to show what changed (trait diffs)
- [Revert to this version] button on each entry

### Right Column — Preview & Test

**Sticky positioning** — scrolls with the page but stays visible as the user scrolls through config panels.

#### System Prompt Preview
- Full rendered system prompt as the agent will see it
- Read-only code-style display (monospace, scrollable)
- Section headers match config panels for easy cross-reference
- Token count estimate at the top (updates live)
- Updates via htmx whenever any config value changes — the backend renders the prompt and returns it

#### Quick Test
- Collapsible panel at the bottom of the right column
- **Prompt textarea**: User types or selects a test prompt
- **Saved prompts dropdown**: Quick access to previously saved test prompts and starter prompts (the test prompt library from the actions spec)
- **Run button**: Sends current config + prompt to Claude, displays response
- **Response display**: Markdown-rendered response with word count and timing
- **History**: Last 5 test runs shown as collapsible entries below. Useful for comparing before/after when tuning

### Editor Behavior

**Auto-save**: Changes are saved automatically (debounced, ~2 seconds after last edit). No explicit save required for config changes. Visual indicator: "Saved ✓" or "Saving..." in the header.

**Prompt preview updates**: Every config change triggers an htmx request to `/api/preview/prompt` which returns the re-rendered prompt. The preview panel swaps in the new content. This happens on slider `input` events (live as you drag), dropdown `change`, and textarea `blur`.

**Undo**: Browser-native undo works for text fields. For sliders and toggles, the version history panel serves as undo.

---

## View 3: Group Composer

For assembling agents into discussion groups.

### Layout

```
┌─────────────────────────────────────────────────────────────────┐
│  Agent Workshop                              [Library] [Groups] │
├─────────────────────────────────────────────────────────────────┤
│  ← Back to Groups          Product Planning Team    [Save] [Export]│
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Agents in Group                            [+ Add Agent]       │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ ☰ The Pragmatist     infrastructure realist   [CRITIQUE ▾] ✕│
│  │ ☰ The Ideator        divergent generator      [PROPOSE  ▾] ✕│
│  │ ☰ The Critic         adversarial reviewer     [CRITIQUE ▾] ✕│
│  │ ☰ The Advocate        user outcomes            [EVALUATE ▾] ✕│
│  │ ☰ The Architect       system coherence         [PROPOSE  ▾] ✕│
│  │ ☰ The Synthesizer     integration coherence    [EVALUATE ▾] ✕│
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌─────────────────────────┐  ┌───────────────────────────────┐ │
│  │  Balance Analysis       │  │  Round Preview                │ │
│  │                         │  │                               │ │
│  │  Trait Distribution     │  │  PROPOSE                      │ │
│  │       creativity        │  │  ├─ The Ideator               │ │
│  │         ╱    ╲          │  │  └─ The Architect              │ │
│  │   assert ─────  risk    │  │                               │ │
│  │         ╲    ╱          │  │  CRITIQUE                     │ │
│  │       stubborn          │  │  ├─ The Pragmatist            │ │
│  │                         │  │  └─ The Critic                │ │
│  │  ⚠ Low creativity      │  │                               │ │
│  │    spread (all < 0.4)   │  │  EVALUATE                    │ │
│  │                         │  │  ├─ The Advocate              │ │
│  │  Role Coverage          │  │  └─ The Synthesizer           │ │
│  │  Propose:  ██ 2         │  │                               │ │
│  │  Critique: ██ 2         │  │  SYNTHESIZE                   │ │
│  │  Evaluate: ██ 2         │  │  └─ (neutral moderator)      │ │
│  │  ✓ All rounds covered   │  │                               │ │
│  │                         │  │                               │ │
│  │  Anti-Slop Coverage     │  │                               │ │
│  │  Agreement tax: 6/6     │  │                               │ │
│  │  Perspective:   6/6     │  │                               │ │
│  │  Devil's adv:   1/6     │  │                               │ │
│  │  Domain pivot:  2/6     │  │                               │ │
│  │                         │  │                               │ │
│  │  Cognitive Diversity    │  │                               │ │
│  │  ANALYTICAL: 3          │  │                               │ │
│  │  LATERAL: 1             │  │                               │ │
│  │  DIVERGENT: 1           │  │                               │ │
│  │  SYSTEMATIC: 1          │  │                               │ │
│  │  ✓ Good diversity       │  │                               │ │
│  └─────────────────────────┘  └───────────────────────────────┘ │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  Group Actions (applied to all agents in a round)        │  │
│  │  PROPOSE:  [steal_mechanism]  [+ Add]                    │  │
│  │  CRITIQUE: [failure_postmortem] [assumption_audit] [+ Add]│  │
│  │  EVALUATE: [user_reframe]  [+ Add]                       │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### Agent List
- Sortable rows (drag handle ☰ for reordering)
- Each row: agent name, role, round assignment dropdown, remove button (✕)
- Round assignment dropdown: PROPOSE / CRITIQUE / EVALUATE (determines which round the agent participates in)
- [+ Add Agent] button → dropdown showing library agents with search, or "Create New"

### Balance Analysis Panel
- **Trait Distribution**: Simplified radar/spider chart showing the group's average + spread across key personality dimensions. Warnings for low spread (agents too similar) or gaps
- **Role Coverage**: Bar chart showing how many agents per round. Warnings if any round is empty
- **Anti-Slop Coverage**: How many agents have each mechanism enabled. Warning if agreement_tax coverage is low
- **Cognitive Diversity**: Count of each cognitive style. Warning if all agents share the same style

### Round Preview
- Visual tree showing which agents are in which round
- At-a-glance verification that the group structure makes sense

### Group Actions
- Actions assigned at the round level (all agents in that round receive the action)
- Per-round action list with add/remove

### Export
- [Export YAML] button → downloads a session-ready YAML file
- [Copy YAML] button → copies to clipboard
- The exported YAML is identical to what the session runner expects — no translation needed

---

## View 4: Comparison View

Accessed from the Agent Editor: "Compare with..." button.

### Layout

```
┌─────────────────────────────────────────────────────────────────┐
│  Agent Workshop                              [Library] [Groups] │
├─────────────────────────────────────────────────────────────────┤
│  Comparing: The Pragmatist v3  ↔  The Pragmatist v2            │
│             [Change ▾]            [Change ▾]                    │
├────────────────────────────────┬────────────────────────────────┤
│                                │                                │
│  Trait Differences             │  Trait Differences             │
│  assertiveness:  0.7           │  assertiveness:  0.5  (was)   │
│  stubbornness:   0.7           │  stubbornness:   0.5  (was)   │
│  creativity:     0.3           │  creativity:     0.3  (same)  │
│  ... (unchanged hidden)       │                                │
│                                │                                │
├────────────────────────────────┼────────────────────────────────┤
│                                │                                │
│  Test Prompt:                                                   │
│  [Here's a proposal for a caching layer that...              ]  │
│                                                       [Run ▶]  │
│                                                                 │
├────────────────────────────────┬────────────────────────────────┤
│  Response (v3)                 │  Response (v2)                 │
│  ┌────────────────────────────┐│  ┌────────────────────────────┐│
│  │ Three problems jump out    ││  │ This caching approach has  ││
│  │ immediately. First, your   ││  │ some merit, but I see a    ││
│  │ cache invalidation strategy││  │ few concerns. The          ││
│  │ assumes write-through...   ││  │ invalidation strategy...   ││
│  │                            ││  │                            ││
│  └────────────────────────────┘│  └────────────────────────────┘│
│  247 words · 3.2s              │  312 words · 3.8s             │
│                                │                                │
└────────────────────────────────┴────────────────────────────────┘
```

### How It Works
- Select two agents (or two versions of the same agent) via dropdowns at the top
- Trait differences highlighted — only changed values shown, unchanged collapsed
- Shared test prompt input — same prompt sent to both configurations
- Side-by-side responses for direct comparison
- Word count and timing for each

### Use Cases
- **Tuning iteration**: Compare v2 and v3 of the same agent to see if a trait change improved output
- **Agent comparison**: Compare two different agents on the same prompt to check they're producing genuinely different perspectives
- **A/B testing**: Test whether a critic with high bluntness finds different problems than one with low bluntness

---

## Modals

### AI Generate Agent

```
┌───────────────────────────────────────────┐
│  Generate Agent from Description          │
│                                           │
│  Describe the agent you want:             │
│  ┌───────────────────────────────────────┐│
│  │ A skeptical infrastructure engineer   ││
│  │ who thinks in failure modes and       ││
│  │ always asks "what breaks at 3 AM?"    ││
│  └───────────────────────────────────────┘│
│                                           │
│  [Cancel]                    [Generate ▶] │
└───────────────────────────────────────────┘
```

After generation: opens the Agent Editor with the generated config pre-filled for review and adjustment.

### Import YAML

```
┌───────────────────────────────────────────┐
│  Import Agent Configuration               │
│                                           │
│  Drop YAML file here or [Browse...]       │
│                                           │
│  Or paste YAML:                           │
│  ┌───────────────────────────────────────┐│
│  │                                       ││
│  └───────────────────────────────────────┘│
│                                           │
│  ℹ Team YAML files will import all       │
│    agents as separate library entries     │
│                                           │
│  [Cancel]                     [Import ▶]  │
└───────────────────────────────────────────┘
```

### Archetype Picker

```
┌───────────────────────────────────────────┐
│  Start from Archetype                     │
│                                           │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐    │
│  │ Critic   │ │ Ideator │ │Pragmatist│    │
│  │ Finds    │ │ Novel   │ │ Failure  │    │
│  │ problems │ │ ideas   │ │ modes    │    │
│  └─────────┘ └─────────┘ └─────────┘    │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐    │
│  │ Advocate │ │Architect│ │Synthesizr│    │
│  │ User     │ │ System  │ │ Integra- │    │
│  │ outcomes │ │ design  │ │ tion     │    │
│  └─────────┘ └─────────┘ └─────────┘    │
│                                           │
│  [Cancel]                                 │
└───────────────────────────────────────────┘
```

Clicking an archetype opens the Agent Editor with that archetype's config pre-filled.

---

## Interaction Patterns

### Live Preview Updates
Every config change triggers an htmx request:
```html
<!-- Slider example -->
<input type="range" min="0" max="1" step="0.05" value="0.7"
       name="assertiveness"
       hx-post="/api/preview/prompt"
       hx-trigger="input changed delay:300ms"
       hx-target="#prompt-preview"
       hx-include="[name^='agent_']">
```

The backend re-renders the full system prompt and returns HTML. The preview panel swaps content. Feels instant with 300ms debounce.

### Slider Descriptions
Each slider has a description element that updates based on value:
```html
<input type="range" ...
       hx-get="/api/trait-description/assertiveness"
       hx-trigger="input changed delay:100ms"
       hx-target="#assertiveness-desc"
       hx-vals='{"value": this.value}'>
<div id="assertiveness-desc" class="trait-desc">
  You are quite assertive — you fight hard...
</div>
```

The backend returns the rendered natural language description for the current value. Updates faster than the full prompt preview (100ms debounce vs 300ms).

### Quick Test
```html
<button hx-post="/api/agents/current/test"
        hx-target="#test-response"
        hx-include="#test-prompt"
        hx-indicator="#test-spinner">
  Run ▶
</button>
```

Shows a spinner while the Claude call runs (~3-5 seconds). Response is markdown-rendered in the response panel.

### Auto-Save
```html
<!-- Every config input includes -->
hx-post="/api/agents/{id}"
hx-trigger="change delay:2000ms"
hx-indicator="#save-indicator"
```

The save indicator shows "Saving..." → "Saved ✓" with a fade.

---

## Color Coding

Minimal, functional color use:

| Element | Color | Usage |
|---|---|---|
| Job badges | Blue=propose, Red=critique, Green=evaluate, Purple=ideate, Orange=simplify | Agent cards, round preview |
| Trait bars | Gray fill on gray track | Agent cards (mini trait visualization) |
| Warnings | Amber/yellow | Balance analysis warnings |
| Success | Green | "Saved ✓", "✓ All rounds covered" |
| Changed values | Blue highlight | Comparison view trait diffs |
| Active toggles | Primary color | Anti-slop switches |
| Inactive | Dimmed/gray | Disabled toggles, collapsed sections |

---

## Responsive Behavior

- **Desktop (>1024px)**: Two-column editor layout. Three-column card grid in library
- **Tablet (768-1024px)**: Two-column editor (narrower preview). Two-column card grid
- **Mobile (<768px)**: Not a priority (this is a local development tool), but single-column stacking should work naturally with Pico CSS

---

## File Structure

```
projects/workshop/
  __main__.py              # Entry point: starts FastAPI server
  server.py                # FastAPI app, routes, API endpoints
  prompt_renderer.py       # Renders agent config → system prompt (reuses prompt_builder)
  agent_store.py           # CRUD operations on config/agents/ YAML files
  group_store.py           # CRUD operations on config/groups/ YAML files
  static/
    css/
      pico.min.css         # Base styling
      workshop.css         # Custom overrides
    js/
      htmx.min.js          # htmx library
      workshop.js          # Custom JS (slider handling, drag-drop, modals)
  templates/
    layout.html            # Base template (nav, shell)
    library.html           # Agent library view
    editor.html            # Agent editor view
    groups.html            # Group list view
    composer.html          # Group composer view
    comparison.html        # Comparison view
    partials/
      agent_card.html      # Single agent card (used by library + htmx)
      trait_slider.html    # Slider component
      prompt_preview.html  # Rendered prompt (swapped by htmx)
      test_response.html   # Quick test response
      balance_panel.html   # Balance analysis (swapped by htmx)

config/                      # Shared config directory (Workshop reads/writes here)
  agents/                    # Individual agent YAML files (by GUID)
  groups/                    # Group compositions
  actions/                   # Action definitions
  archetypes/                # Starter templates
  teams/                     # Legacy: self-contained team YAMLs
```
