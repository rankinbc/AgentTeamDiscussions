# Session Setup Page + Stop Control

**Date:** 2026-03-26
**Status:** Approved

---

## Overview

Add a setup page to the React dashboard where users can compose a discussion topic, select agents, and launch a session. Add a stop button to the live dashboard header to terminate running sessions. Introduces client-side routing to the previously single-page app.

---

## Routing

Add `react-router-dom`. Two routes:

| Path | Component | Purpose |
|------|-----------|---------|
| `/` | SetupPage | Configure and launch a new discussion |
| `/session` | Dashboard | Live session view (current App.tsx content) |

---

## Setup Page (`/`)

### Layout (top to bottom)

**1. Topic Input**
- Large textarea: "What should the agents discuss?"
- Placeholder text guiding the user

**2. Brief Picker**
- Horizontal scrollable row of brief cards
- Each card shows brief filename (cleaned: dashes to spaces, no extension)
- Selecting a brief populates the topic textarea with the file's content
- User can pick a brief OR type freeform -- selecting a brief replaces freeform text; editing the textarea deselects the brief
- Fetched from `GET /api/briefs`

**3. Agent Selection**
- Card grid of all available agents
- Each card displays:
  - Agent name and role tagline
  - Personality trait bars (reuse TraitBar component from Roster)
  - Checkbox/toggle overlay to include or exclude
  - Visually dimmed when deselected
- All agents selected by default
- Fetched from `GET /api/agents`

**4. Footer Actions**
- "Create New Agent" link -- placeholder, not functional yet
- "Start Discussion" button -- disabled until topic is non-empty and at least 2 agents selected
- On click: POST to `/api/session/start`, then navigate to `/session`

### Styling
- Same dark theme, CSS variables, and styling approach as existing dashboard
- Cards use `--surface` / `--surface2` backgrounds with `--border`
- Selected agents get accent border (`--blue`), deselected get dimmed opacity
- All new styles added to `index.css`

---

## Stop Button (Dashboard Header)

- Red stop icon/button in the Header component on `/session`
- Visible only when session is running (`connectionStatus === 'live'`)
- On click: POST to `/api/session/stop`
- On success: navigate to `/` (setup page)
- Confirmation not required (session output is already persisted to disk)

---

## New Backend API Endpoints

All added to `LiveServer.cs`.

### GET /api/briefs
- Scans the configured `input/` directory for `.md` files
- Returns JSON array: `[{ name: string, filename: string, content: string }]`
- `name` is the filename with dashes replaced by spaces, extension stripped

### GET /api/agents
- Reads all agent YAML files from `data/agents/` (or wherever the engine loads them)
- Returns JSON array matching the `AgentProfile` shape the UI already uses:
  ```json
  [{
    "key": "cognitive_architect",
    "name": "The Cognitive Architect",
    "tagline": "creativity engine designer",
    "personality": { "assertiveness": 0.7, "curiosity": 0.9, ... },
    "drives": ["..."],
    "antiSlop": ["..."]
  }]
  ```

### POST /api/session/start
- Body: `{ topic: string, agentKeys: string[] }`
- Creates a temporary brief file from the topic text
- Spawns a new session using `SessionRunner` with the specified agents
- Returns `{ sessionId: string }` on success
- Returns 409 if a session is already running

### POST /api/session/stop
- Signals cancellation on the running SessionRunner via CancellationTokenSource
- Returns 200 on success, 404 if no session is running
- Session output up to the stop point is preserved on disk

---

## Vite Proxy Updates

Add to `vite.config.ts`:
```
'/api': 'http://localhost:8899'
```

---

## State Management

- Setup page uses local component state (no need for global context)
- Dashboard continues using existing DashboardContext
- On session start, dashboard connects via SSE as it does today (no changes to useSSE)

---

## Component Hierarchy

```
<BrowserRouter>
  <Routes>
    <Route path="/" element={<SetupPage />} />
    <Route path="/session" element={<Dashboard />} />
  </Routes>
</BrowserRouter>
```

SetupPage is a new top-level component. Dashboard is the current App.tsx content extracted into its own component.

---

## Out of Scope

- Agent editor (placeholder link only)
- Multiple concurrent sessions
- Session history / listing past sessions
- Resume session from UI
- Editing agents from the setup page
