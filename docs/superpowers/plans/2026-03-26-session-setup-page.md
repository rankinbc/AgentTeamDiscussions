# Session Setup Page + Stop Control Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a setup page to the React UI where users compose topics, select agents, and launch discussions. Add a stop button to the live dashboard header.

**Architecture:** Add `react-router-dom` for two routes (`/` setup, `/session` dashboard). Backend gets 4 new API endpoints in `LiveServer.cs` for listing briefs, listing agents, starting sessions, and stopping sessions. The engine manages session lifecycle via a shared `SessionManager` class that holds the running task and CancellationTokenSource.

**Tech Stack:** React 19, react-router-dom, TypeScript, CSS (index.css), C# ASP.NET Minimal API, YamlDotNet

---

### Task 1: Install react-router-dom

**Files:**
- Modify: `_SYSTEM/projects/engine/ui/package.json`

- [ ] **Step 1: Install the dependency**

```bash
cd _SYSTEM/projects/engine/ui
npm install react-router-dom
```

- [ ] **Step 2: Verify it installed**

```bash
cd _SYSTEM/projects/engine/ui
node -e "require('react-router-dom'); console.log('ok')"
```

Expected: `ok`

- [ ] **Step 3: Commit**

```bash
git add _SYSTEM/projects/engine/ui/package.json _SYSTEM/projects/engine/ui/package-lock.json
git commit -m "feat(ui): add react-router-dom dependency"
```

---

### Task 2: Add Vite proxy for /api routes

**Files:**
- Modify: `_SYSTEM/projects/engine/ui/vite.config.ts`

- [ ] **Step 1: Add /api proxy rule**

In `vite.config.ts`, add `'/api'` to the proxy map:

```typescript
proxy: {
  '/events': 'http://localhost:8899',
  '/ledger': 'http://localhost:8899',
  '/moderator': 'http://localhost:8899',
  '/questions': 'http://localhost:8899',
  '/api': 'http://localhost:8899',
},
```

- [ ] **Step 2: Commit**

```bash
git add _SYSTEM/projects/engine/ui/vite.config.ts
git commit -m "feat(ui): add /api proxy route for session management endpoints"
```

---

### Task 3: Create SessionManager on the backend

**Files:**
- Create: `_SYSTEM/projects/engine/src/EngineStandalone/Live/SessionManager.cs`

This class holds a reference to the running session task and its CancellationTokenSource, allowing the API to start and stop sessions.

- [ ] **Step 1: Create SessionManager.cs**

```csharp
using EngineStandalone.Abstractions;
using EngineStandalone.Agents;
using EngineStandalone.Config;
using EngineStandalone.Discussion;
using EngineStandalone.Runner;
using EngineStandalone.Session;
using EngineStandalone.Synthesis;

namespace EngineStandalone.Live;

/// <summary>
/// Manages the lifecycle of a running discussion session.
/// Allows the API to start new sessions and stop running ones.
/// </summary>
public class SessionManager
{
    private readonly string _baseDir;
    private readonly IServiceProvider _provider;
    private Task? _runningTask;
    private CancellationTokenSource? _cts;
    private SseSessionEmitter? _emitter;

    public bool IsRunning => _runningTask is { IsCompleted: false };
    public SseSessionEmitter? Emitter => _emitter;

    public SessionManager(string baseDir, IServiceProvider provider)
    {
        _baseDir = baseDir;
        _provider = provider;
    }

    /// <summary>
    /// Start a new session from a SessionConfig. Returns false if a session is already running.
    /// </summary>
    public bool Start(SessionConfig config, SseSessionEmitter emitter)
    {
        if (IsRunning) return false;

        _emitter = emitter;
        _cts = new CancellationTokenSource();
        var ct = _cts.Token;

        var runner = new SessionRunner(
            _baseDir,
            _provider.GetRequiredService<IConfigLoader>(),
            _provider.GetRequiredService<IAgentLoader>(),
            _provider.GetRequiredService<IPromptBuilder>(),
            _provider.GetRequiredService<IClaudeRunner>(),
            _provider.GetRequiredService<IDiscussionEngine>(),
            _provider.GetRequiredService<IMorningBriefGenerator>(),
            emitter);

        _runningTask = Task.Run(async () =>
        {
            try
            {
                await runner.RunFromConfigAsync(config);
            }
            catch (OperationCanceledException)
            {
                Console.WriteLine("Session cancelled by user.");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Session error: {ex.Message}");
            }
        }, ct);

        return true;
    }

    /// <summary>
    /// Stop the currently running session.
    /// </summary>
    public bool Stop()
    {
        if (!IsRunning) return false;

        _cts?.Cancel();
        _emitter?.Emit(new SessionEvent { Type = "session_stopped" });
        return true;
    }
}
```

- [ ] **Step 2: Verify it compiles**

```bash
cd _SYSTEM/projects/engine
dotnet build src/EngineStandalone/EngineStandalone.csproj
```

Expected: Build succeeded.

- [ ] **Step 3: Commit**

```bash
git add _SYSTEM/projects/engine/src/EngineStandalone/Live/SessionManager.cs
git commit -m "feat(engine): add SessionManager for API-driven session lifecycle"
```

---

### Task 4: Add API endpoints to LiveServer.cs

**Files:**
- Modify: `_SYSTEM/projects/engine/src/EngineStandalone/Live/LiveServer.cs`

Change the `Build` method signature to accept the additional dependencies needed for the new endpoints.

- [ ] **Step 1: Update LiveServer.Build to accept SessionManager, IAgentLoader, and baseDir**

Change the method signature from:
```csharp
public static WebApplication Build(SseSessionEmitter emitter, int port = 8899)
```
to:
```csharp
public static WebApplication Build(SseSessionEmitter emitter, SessionManager sessionManager, IAgentLoader agentLoader, string baseDir, int port = 8899)
```

- [ ] **Step 2: Add GET /api/briefs endpoint**

After the existing `/questions/add` endpoint, add:

```csharp
// List available brief files
app.MapGet("/api/briefs", () =>
{
    var inputDir = Path.Combine(baseDir, "input");
    if (!Directory.Exists(inputDir))
        return Results.Json(Array.Empty<object>());

    var briefs = Directory.GetFiles(inputDir, "*.md")
        .Select(f => new
        {
            filename = Path.GetFileName(f),
            name = Path.GetFileNameWithoutExtension(f).Replace("-", " ").Replace("_", " "),
            content = File.ReadAllText(f),
        })
        .ToArray();

    return Results.Json(briefs);
});
```

- [ ] **Step 3: Add GET /api/agents endpoint**

```csharp
// List all available agents with profile data
app.MapGet("/api/agents", () =>
{
    var agents = agentLoader.ListAgents();
    var result = new List<object>();

    foreach (var (id, name, key, file) in agents)
    {
        try
        {
            var config = agentLoader.LoadAgentByKey(key);
            result.Add(new
            {
                key,
                name = config.Name,
                role = config.Position?.Role ?? "",
                traits = config.Personality != null ? new Dictionary<string, double>
                {
                    ["assertiveness"] = config.Personality.Assertiveness,
                    ["creativity"] = config.Personality.CreativityTemp,
                    ["risk tolerance"] = config.Personality.RiskTolerance,
                    ["stubbornness"] = config.Personality.Stubbornness,
                    ["idea receptivity"] = config.Personality.IdeaReceptivity,
                    ["bluntness"] = config.Personality.Bluntness,
                } : new Dictionary<string, double>(),
                drives = config.Position?.Drives ?? new List<string>(),
            });
        }
        catch
        {
            result.Add(new { key, name, role = "", traits = new Dictionary<string, double>(), drives = new List<string>() });
        }
    }

    return Results.Json(result);
});
```

- [ ] **Step 4: Add POST /api/session/start endpoint**

```csharp
// Start a new discussion session
app.MapPost("/api/session/start", async (HttpContext ctx) =>
{
    if (sessionManager.IsRunning)
        return Results.Conflict(new { error = "A session is already running" });

    using var reader = new StreamReader(ctx.Request.Body);
    var body = await reader.ReadToEndAsync();

    string topic;
    List<string>? agentKeys = null;
    try
    {
        var json = System.Text.Json.JsonDocument.Parse(body);
        topic = json.RootElement.GetProperty("topic").GetString() ?? "";
        if (json.RootElement.TryGetProperty("agentKeys", out var agentsEl))
        {
            agentKeys = agentsEl.EnumerateArray()
                .Select(a => a.GetString()!)
                .Where(a => a != null)
                .ToList();
        }
    }
    catch
    {
        return Results.BadRequest(new { error = "Invalid request body. Expected: { topic, agentKeys? }" });
    }

    if (string.IsNullOrWhiteSpace(topic))
        return Results.BadRequest(new { error = "Topic is required" });

    var preparer = new SessionPreparer(agentLoader,
        emitter is SseSessionEmitter ? null! :
        throw new InvalidOperationException()); // will fix below

    // Use the correct way to build config
    var configLoader = sessionManager.GetConfigLoader(); // we'll need to expose this

    var config = new SessionPreparer(agentLoader, configLoader)
        .PrepareFromArgs(topic, agents: agentKeys);
    config.Source = "api";

    // Create a fresh emitter for the new session
    var newEmitter = new SseSessionEmitter();
    if (!sessionManager.Start(config, newEmitter))
        return Results.Conflict(new { error = "Failed to start session" });

    return Results.Ok(new { status = "started", title = config.Title });
});
```

Wait -- this approach has a problem. The `LiveServer.Build` creates the app once, but we need to swap the emitter when a new session starts. Let me revise the approach.

**Revised Step 4: Rethink the emitter architecture**

The `SessionManager` will own the emitter and the `/events` SSE endpoint will read from the manager's current emitter. Update the approach:

Replace step 1-4 with a cleaner approach. The `LiveServer.Build` method accepts `SessionManager` which owns the emitter lifecycle. The SSE endpoint subscribes to the manager's current emitter.

Update `SessionManager` to also hold `IConfigLoader`:

```csharp
// In SessionManager, add:
private readonly IConfigLoader _configLoader;

public SessionManager(string baseDir, IServiceProvider provider)
{
    _baseDir = baseDir;
    _provider = provider;
    _configLoader = provider.GetRequiredService<IConfigLoader>();
}

public IConfigLoader ConfigLoader => _configLoader;
public IAgentLoader AgentLoader => _provider.GetRequiredService<IAgentLoader>();
```

- [ ] **Step 4 (revised): Add POST /api/session/start endpoint**

```csharp
app.MapPost("/api/session/start", async (HttpContext ctx) =>
{
    if (sessionManager.IsRunning)
        return Results.Conflict(new { error = "A session is already running" });

    using var reader = new StreamReader(ctx.Request.Body);
    var body = await reader.ReadToEndAsync();

    string topic;
    List<string>? agentKeys = null;
    try
    {
        var json = JsonDocument.Parse(body);
        topic = json.RootElement.GetProperty("topic").GetString() ?? "";
        if (json.RootElement.TryGetProperty("agentKeys", out var agentsEl))
        {
            agentKeys = agentsEl.EnumerateArray()
                .Select(a => a.GetString()!)
                .Where(a => a != null)
                .ToList();
        }
    }
    catch
    {
        return Results.BadRequest(new { error = "Invalid request body" });
    }

    if (string.IsNullOrWhiteSpace(topic))
        return Results.BadRequest(new { error = "Topic is required" });

    var preparer = new SessionPreparer(agentLoader, sessionManager.ConfigLoader);
    var config = preparer.PrepareFromArgs(topic, agents: agentKeys);
    config.Source = "api";

    var newEmitter = new SseSessionEmitter();
    if (!sessionManager.Start(config, newEmitter))
        return Results.Conflict(new { error = "Failed to start session" });

    return Results.Ok(new { status = "started", title = config.Title });
});
```

- [ ] **Step 5: Add POST /api/session/stop endpoint**

```csharp
app.MapPost("/api/session/stop", () =>
{
    if (!sessionManager.IsRunning)
        return Results.NotFound(new { error = "No session is running" });

    sessionManager.Stop();
    return Results.Ok(new { status = "stopped" });
});
```

- [ ] **Step 6: Update the /events endpoint to use SessionManager's current emitter**

Replace the existing `/events` handler to read from `sessionManager.Emitter` instead of the static `emitter` parameter. The endpoint should return "no session" if the emitter is null:

```csharp
app.MapGet("/events", async (HttpContext ctx) =>
{
    var currentEmitter = sessionManager.Emitter ?? emitter;
    if (currentEmitter == null)
    {
        ctx.Response.StatusCode = 204;
        return;
    }

    ctx.Response.ContentType = "text/event-stream";
    ctx.Response.Headers.Append("Cache-Control", "no-cache");
    ctx.Response.Headers.Append("Connection", "keep-alive");

    var channel = currentEmitter.Subscribe();
    var ct = ctx.RequestAborted;

    try
    {
        await foreach (var evt in channel.Reader.ReadAllAsync(ct))
        {
            var json = SseSessionEmitter.ToJson(evt);
            await ctx.Response.WriteAsync($"data: {json}\n\n", ct);
            await ctx.Response.Body.FlushAsync(ct);
        }
    }
    catch (OperationCanceledException) { }
});
```

- [ ] **Step 7: Update the /ledger endpoint to use SessionManager**

```csharp
app.MapGet("/ledger", () =>
{
    var currentEmitter = sessionManager.Emitter ?? emitter;
    var sessionDir = currentEmitter?.SessionDir;
    if (sessionDir == null) return Results.Text("# Decisions Ledger\n\nNo session active.\n");

    var ledgerPath = Path.Combine(sessionDir, "decisions_ledger.md");
    if (File.Exists(ledgerPath))
        return Results.Text(File.ReadAllText(ledgerPath));

    return Results.Text("# Decisions Ledger\n\nNo decisions yet.\n");
});
```

- [ ] **Step 8: Verify it compiles**

```bash
cd _SYSTEM/projects/engine
dotnet build src/EngineStandalone/EngineStandalone.csproj
```

Expected: Build succeeded.

- [ ] **Step 9: Commit**

```bash
git add _SYSTEM/projects/engine/src/EngineStandalone/Live/LiveServer.cs _SYSTEM/projects/engine/src/EngineStandalone/Live/SessionManager.cs
git commit -m "feat(engine): add API endpoints for briefs, agents, session start/stop"
```

---

### Task 5: Wire SessionManager into Program.cs

**Files:**
- Modify: `_SYSTEM/projects/engine/src/EngineStandalone/Program.cs`

- [ ] **Step 1: Update StartLiveServer to create SessionManager and pass it to LiveServer.Build**

Change the `StartLiveServer` method:

```csharp
private static (SseSessionEmitter? Emitter, WebApplication? App, SessionManager? Manager) StartLiveServer(
    bool live, int port, ServiceProvider provider, string baseDir)
{
    if (!live) return (null, null, null);

    var emitter = new SseSessionEmitter();
    var manager = new SessionManager(baseDir, provider);
    var agentLoader = provider.GetRequiredService<IAgentLoader>();
    var webApp = LiveServer.Build(emitter, manager, agentLoader, baseDir, port);
    _ = webApp.StartAsync();
    Console.WriteLine($"Live SSE dashboard: http://localhost:{port}");
    return (emitter, webApp, manager);
}
```

- [ ] **Step 2: Update all call sites of StartLiveServer**

In the root command handler (line ~62):
```csharp
var (emitter, webApp, _) = StartLiveServer(live, defaults.Session.LivePort, provider, baseDir);
```

In the `new` command handler (line ~119):
```csharp
var (emitter, webApp, _) = StartLiveServer(live, defaults.Session.LivePort, provider, baseDir);
```

- [ ] **Step 3: Verify it compiles**

```bash
cd _SYSTEM/projects/engine
dotnet build src/EngineStandalone/EngineStandalone.csproj
```

Expected: Build succeeded.

- [ ] **Step 4: Commit**

```bash
git add _SYSTEM/projects/engine/src/EngineStandalone/Program.cs
git commit -m "feat(engine): wire SessionManager into CLI startup"
```

---

### Task 6: Add API functions to the UI

**Files:**
- Modify: `_SYSTEM/projects/engine/ui/src/lib/api.ts`

- [ ] **Step 1: Add fetch functions for briefs, agents, session start, session stop**

Append to `api.ts`:

```typescript
export interface BriefInfo {
  filename: string;
  name: string;
  content: string;
}

export interface AgentInfo {
  key: string;
  name: string;
  role: string;
  traits: Record<string, number>;
  drives: string[];
}

export async function fetchBriefs(): Promise<BriefInfo[]> {
  const res = await fetch('/api/briefs');
  return res.json();
}

export async function fetchAgents(): Promise<AgentInfo[]> {
  const res = await fetch('/api/agents');
  return res.json();
}

export async function startSession(topic: string, agentKeys: string[]): Promise<{ status: string; title: string }> {
  const res = await fetch('/api/session/start', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ topic, agentKeys }),
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.error || 'Failed to start session');
  }
  return res.json();
}

export async function stopSession(): Promise<void> {
  const res = await fetch('/api/session/stop', { method: 'POST' });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.error || 'Failed to stop session');
  }
}
```

- [ ] **Step 2: Commit**

```bash
git add _SYSTEM/projects/engine/ui/src/lib/api.ts
git commit -m "feat(ui): add API client functions for briefs, agents, session lifecycle"
```

---

### Task 7: Create the SetupPage component

**Files:**
- Create: `_SYSTEM/projects/engine/ui/src/pages/SetupPage.tsx`

- [ ] **Step 1: Create SetupPage.tsx**

```tsx
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { fetchBriefs, fetchAgents, startSession } from '../lib/api';
import type { BriefInfo, AgentInfo } from '../lib/api';

export default function SetupPage() {
  const navigate = useNavigate();
  const [topic, setTopic] = useState('');
  const [briefs, setBriefs] = useState<BriefInfo[]>([]);
  const [agents, setAgents] = useState<AgentInfo[]>([]);
  const [selectedBrief, setSelectedBrief] = useState<string | null>(null);
  const [selectedAgents, setSelectedAgents] = useState<Set<string>>(new Set());
  const [launching, setLaunching] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchBriefs().then(setBriefs).catch(() => {});
    fetchAgents().then(a => {
      setAgents(a);
      setSelectedAgents(new Set(a.map(ag => ag.key)));
    }).catch(() => {});
  }, []);

  const selectBrief = (b: BriefInfo) => {
    if (selectedBrief === b.filename) {
      setSelectedBrief(null);
      setTopic('');
    } else {
      setSelectedBrief(b.filename);
      setTopic(b.content);
    }
  };

  const handleTopicChange = (val: string) => {
    setTopic(val);
    setSelectedBrief(null);
  };

  const toggleAgent = (key: string) => {
    setSelectedAgents(prev => {
      const next = new Set(prev);
      if (next.has(key)) next.delete(key);
      else next.add(key);
      return next;
    });
  };

  const canStart = topic.trim().length > 0 && selectedAgents.size >= 2;

  const handleStart = async () => {
    if (!canStart || launching) return;
    setLaunching(true);
    setError('');
    try {
      await startSession(topic, Array.from(selectedAgents));
      navigate('/session');
    } catch (e: any) {
      setError(e.message || 'Failed to start session');
      setLaunching(false);
    }
  };

  return (
    <div className="setup-page">
      <header className="setup-hdr">
        <div className="hdr-logo">ATD <span>// SETUP</span></div>
      </header>

      <div className="setup-content">
        {/* Topic */}
        <section className="setup-section">
          <h2 className="setup-label">What should the agents discuss?</h2>
          <textarea
            className="setup-topic"
            value={topic}
            onChange={e => handleTopicChange(e.target.value)}
            placeholder="Describe the topic, paste questions, or select a brief below..."
            rows={6}
          />
        </section>

        {/* Briefs */}
        {briefs.length > 0 && (
          <section className="setup-section">
            <h2 className="setup-label">Or start from a brief</h2>
            <div className="brief-row">
              {briefs.map(b => (
                <button
                  key={b.filename}
                  className={`brief-card ${selectedBrief === b.filename ? 'selected' : ''}`}
                  onClick={() => selectBrief(b)}
                >
                  {b.name}
                </button>
              ))}
            </div>
          </section>
        )}

        {/* Agents */}
        <section className="setup-section">
          <h2 className="setup-label">Select agents</h2>
          <div className="agent-grid">
            {agents.map(a => {
              const on = selectedAgents.has(a.key);
              return (
                <div
                  key={a.key}
                  className={`setup-agent-card ${on ? 'selected' : 'dimmed'}`}
                  onClick={() => toggleAgent(a.key)}
                >
                  <div className="sac-check">{on ? '\u2713' : ''}</div>
                  <div className="sac-name">{a.name}</div>
                  <div className="sac-role">{a.role}</div>
                  {Object.entries(a.traits).map(([name, val]) => (
                    <div key={name} className="trait-row">
                      <span className="trait-lbl">{name}</span>
                      <div className="trait-bar">
                        <div className="trait-fill" style={{ width: `${val * 100}%`, background: on ? 'var(--blue)' : 'var(--dim)' }} />
                      </div>
                      <span className="trait-val">{val.toFixed(1)}</span>
                    </div>
                  ))}
                  {a.drives.length > 0 && (
                    <div className="sac-drives">
                      {a.drives.slice(0, 2).map((d, i) => (
                        <div key={i} className="sac-drive">{d}</div>
                      ))}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </section>

        {/* Footer */}
        <div className="setup-footer">
          <a className="setup-link dim" href="#">+ Create new agent</a>
          {error && <span className="setup-error">{error}</span>}
          <button
            className={`setup-start ${canStart ? '' : 'disabled'}`}
            onClick={handleStart}
            disabled={!canStart || launching}
          >
            {launching ? 'Starting...' : 'Start Discussion'}
          </button>
        </div>
      </div>
    </div>
  );
}
```

- [ ] **Step 2: Commit**

```bash
git add _SYSTEM/projects/engine/ui/src/pages/SetupPage.tsx
git commit -m "feat(ui): create SetupPage component with topic, brief, and agent selection"
```

---

### Task 8: Extract Dashboard from App.tsx and add routing

**Files:**
- Modify: `_SYSTEM/projects/engine/ui/src/App.tsx`
- Modify: `_SYSTEM/projects/engine/ui/src/main.tsx`

- [ ] **Step 1: Update App.tsx to add routing**

Replace the default export in `App.tsx` (lines 386-392). The `Dashboard` function stays in App.tsx (it's already defined there). Just change the export:

```tsx
// At top of App.tsx, add import:
import { useNavigate } from 'react-router-dom';
import { stopSession } from './lib/api';
```

In the Dashboard component, add the stop handler and navigate hook. Add after `const [inspTab, setInspTab] = ...` (line 50):

```tsx
const navigate = useNavigate();
const doStop = async () => {
  try {
    await stopSession();
    navigate('/');
  } catch {}
};
```

Add the stop button in the header, after the Ledger button (inside `.hdr-stats`, after line 196):

```tsx
{conn === 'live' && (
  <button className="hdr-btn danger" onClick={doStop}>Stop</button>
)}
```

Change the default export (lines 386-392) to just export Dashboard:

```tsx
export { Dashboard };
```

Remove the `DashboardProvider` wrapper from App.tsx since it will move to the route.

- [ ] **Step 2: Update main.tsx to add BrowserRouter and routes**

Replace `main.tsx` contents:

```tsx
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import './index.css';
import { DashboardProvider } from './store/DashboardContext';
import { Dashboard } from './App';
import SetupPage from './pages/SetupPage';

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<SetupPage />} />
        <Route path="/session" element={
          <DashboardProvider>
            <Dashboard />
          </DashboardProvider>
        } />
      </Routes>
    </BrowserRouter>
  </StrictMode>,
);
```

- [ ] **Step 3: Verify the UI compiles**

```bash
cd _SYSTEM/projects/engine/ui
npx tsc --noEmit
```

Expected: No errors.

- [ ] **Step 4: Commit**

```bash
git add _SYSTEM/projects/engine/ui/src/App.tsx _SYSTEM/projects/engine/ui/src/main.tsx
git commit -m "feat(ui): add react-router with setup and session routes, stop button in header"
```

---

### Task 9: Add CSS for SetupPage

**Files:**
- Modify: `_SYSTEM/projects/engine/ui/src/index.css`

- [ ] **Step 1: Add setup page styles to the end of index.css**

Append after the `.md hr` rule (line 411):

```css
/* ---- Setup Page ---------------------------------------- */
.setup-page {
  height: 100vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
.setup-hdr {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 0 16px;
  height: 42px;
  background: var(--panel);
  border-bottom: 1px solid var(--border);
}
.setup-content {
  flex: 1;
  overflow-y: auto;
  padding: 24px 32px 80px;
  max-width: 960px;
  margin: 0 auto;
  width: 100%;
}
.setup-content::-webkit-scrollbar { width: 4px; }
.setup-content::-webkit-scrollbar-thumb { background: var(--border-hi); border-radius: 2px; }

.setup-section { margin-bottom: 28px; }
.setup-label {
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 2px;
  color: var(--dim);
  margin-bottom: 10px;
  font-weight: 400;
}

.setup-topic {
  width: 100%;
  background: var(--surface);
  border: 1px solid var(--border);
  color: var(--text);
  font: 12px var(--mono);
  padding: 12px 14px;
  resize: vertical;
  outline: none;
  border-radius: 3px;
  line-height: 1.6;
}
.setup-topic:focus { border-color: var(--blue); }
.setup-topic::placeholder { color: var(--dim); }

/* Brief picker */
.brief-row {
  display: flex;
  gap: 8px;
  overflow-x: auto;
  padding-bottom: 4px;
}
.brief-row::-webkit-scrollbar { height: 3px; }
.brief-row::-webkit-scrollbar-thumb { background: var(--border-hi); }
.brief-card {
  flex-shrink: 0;
  padding: 8px 16px;
  background: var(--surface);
  border: 1px solid var(--border);
  color: var(--text2);
  font: 11px var(--mono);
  cursor: pointer;
  border-radius: 3px;
  white-space: nowrap;
}
.brief-card:hover { background: var(--surface2); color: var(--text); }
.brief-card.selected { border-color: var(--blue); color: var(--blue); }

/* Agent grid */
.agent-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 10px;
}
.setup-agent-card {
  padding: 12px 14px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 4px;
  cursor: pointer;
  transition: opacity .15s, border-color .15s;
  position: relative;
}
.setup-agent-card:hover { background: var(--surface2); }
.setup-agent-card.selected { border-color: var(--blue); }
.setup-agent-card.dimmed { opacity: .4; }
.sac-check {
  position: absolute;
  top: 8px;
  right: 10px;
  font-size: 14px;
  color: var(--blue);
}
.sac-name { font-size: 12px; font-weight: 600; color: var(--text); margin-bottom: 2px; }
.sac-role { font-size: 9px; color: var(--dim); margin-bottom: 8px; }
.sac-drives { margin-top: 8px; }
.sac-drive {
  font-size: 9px;
  color: var(--text2);
  padding: 2px 0 2px 8px;
  border-left: 2px solid var(--green);
  margin: 3px 0;
  line-height: 1.4;
}

/* Footer */
.setup-footer {
  display: flex;
  align-items: center;
  gap: 16px;
  padding-top: 16px;
  border-top: 1px solid var(--border);
}
.setup-link { font-size: 11px; color: var(--blue); text-decoration: none; }
.setup-link.dim { color: var(--dim); }
.setup-link:hover { color: var(--text); }
.setup-error { font-size: 10px; color: var(--red); }
.setup-start {
  margin-left: auto;
  padding: 8px 24px;
  background: var(--blue);
  border: none;
  color: var(--bg);
  font: 12px/1 var(--mono);
  font-weight: 600;
  cursor: pointer;
  border-radius: 3px;
  text-transform: uppercase;
  letter-spacing: 1px;
}
.setup-start:hover { filter: brightness(1.15); }
.setup-start.disabled { opacity: .3; cursor: not-allowed; }
```

- [ ] **Step 2: Commit**

```bash
git add _SYSTEM/projects/engine/ui/src/index.css
git commit -m "feat(ui): add setup page styles"
```

---

### Task 10: Verify end-to-end

**Files:** None (manual testing)

- [ ] **Step 1: Build the backend**

```bash
cd _SYSTEM/projects/engine
dotnet build src/EngineStandalone/EngineStandalone.csproj
```

Expected: Build succeeded.

- [ ] **Step 2: Check TypeScript compiles**

```bash
cd _SYSTEM/projects/engine/ui
npx tsc --noEmit
```

Expected: No errors.

- [ ] **Step 3: Run the dotnet tests**

```bash
cd _SYSTEM/projects/engine
dotnet test
```

Expected: All existing tests pass.

- [ ] **Step 4: Final commit (if any fixes needed)**

Address any compilation issues found during verification.
