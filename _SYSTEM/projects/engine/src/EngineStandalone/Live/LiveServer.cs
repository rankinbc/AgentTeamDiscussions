// ASP.NET Core Minimal API server started when --live flag is used.
// Exposes endpoints the React UI expects: GET /events (SSE), GET /ledger,
// POST /moderator, POST /questions/add. Adds CORS headers for Vite dev server.
using System.Text.Json;
using EngineStandalone.Abstractions;
using EngineStandalone.Agents;
using EngineStandalone.Session;

namespace EngineStandalone.Live;

/// <summary>
/// Configures and starts the ASP.NET Core Minimal API server for live SSE streaming.
/// Endpoints: GET /events (SSE), GET /ledger, POST /moderator, POST /questions/add,
/// GET /api/briefs, GET /api/agents, GET /api/teams, POST /api/session/start, POST /api/session/stop
/// </summary>
public static class LiveServer
{
    public static WebApplication Build(SseSessionEmitter emitter, SessionManager sessionManager, IAgentLoader agentLoader, string baseDir, int port = 8899)
    {
        var builder = WebApplication.CreateBuilder();
        builder.WebHost.UseUrls($"http://0.0.0.0:{port}");
        builder.Logging.ClearProviders(); // Suppress Kestrel noise

        var app = builder.Build();

        // Shared data directory: _SYSTEM/data (two levels up from engine baseDir which is _SYSTEM/projects/engine/)
        var sharedDataDir = Path.GetFullPath(Path.Combine(baseDir, "..", "..", "data"));
        var sharedAgentLoader = Directory.Exists(Path.Combine(sharedDataDir, "discussionAgents"))
            ? new AgentLoader(sharedDataDir, agentsSubdir: "discussionAgents")
            : null;

        // CORS for Vite dev server
        app.Use(async (context, next) =>
        {
            context.Response.Headers.Append("Access-Control-Allow-Origin", "*");
            context.Response.Headers.Append("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
            context.Response.Headers.Append("Access-Control-Allow-Headers", "Content-Type");

            if (context.Request.Method == "OPTIONS")
            {
                context.Response.StatusCode = 204;
                return;
            }

            await next();
        });

        // SSE endpoint
        app.MapGet("/events", async (HttpContext ctx) =>
        {
            var currentEmitter = sessionManager.Emitter ?? emitter;
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
            catch (OperationCanceledException)
            {
                // Client disconnected
            }
        });

        // Ledger endpoint
        app.MapGet("/ledger", () =>
        {
            var currentEmitter = sessionManager.Emitter ?? emitter;
            var sessionDir = currentEmitter.SessionDir;
            if (sessionDir == null) return Results.Text("# Decisions Ledger\n\nNo session active.\n");

            var ledgerPath = Path.Combine(sessionDir, "decisions_ledger.md");
            if (File.Exists(ledgerPath))
                return Results.Text(File.ReadAllText(ledgerPath));

            return Results.Text("# Decisions Ledger\n\nNo decisions yet.\n");
        });

        // Moderator endpoint
        app.MapPost("/moderator", async (HttpContext ctx) =>
        {
            using var reader = new StreamReader(ctx.Request.Body);
            var body = await reader.ReadToEndAsync();

            string message;
            try
            {
                var json = JsonDocument.Parse(body);
                message = json.RootElement.GetProperty("message").GetString() ?? body;
            }
            catch
            {
                message = body;
            }

            emitter.QueueModerator(message);
            return Results.Ok();
        });

        // Question queue endpoint
        app.MapPost("/questions/add", async (HttpContext ctx) =>
        {
            using var reader = new StreamReader(ctx.Request.Body);
            var body = await reader.ReadToEndAsync();
            // TODO: Implement live question queueing in Phase 2
            Console.WriteLine($"  [Live] Question queued: {body}");
            return Results.Ok();
        });

        // --- API endpoints for session management ---

        // List available brief files (engine input/ + shared data briefs/)
        app.MapGet("/api/briefs", () =>
        {
            var dirs = new List<string>();
            var inputDir = Path.Combine(baseDir, "input");
            if (Directory.Exists(inputDir)) dirs.Add(inputDir);
            var sharedBriefsDir = Path.Combine(sharedDataDir, "briefs");
            if (Directory.Exists(sharedBriefsDir)) dirs.Add(sharedBriefsDir);

            var seen = new HashSet<string>();
            var briefs = dirs
                .SelectMany(d => Directory.GetFiles(d, "*.md"))
                .Where(f => seen.Add(Path.GetFileName(f))) // deduplicate by filename
                .Select(f => new
                {
                    filename = Path.GetFileName(f),
                    name = Path.GetFileNameWithoutExtension(f).Replace("-", " ").Replace("_", " "),
                    content = File.ReadAllText(f),
                })
                .ToArray();

            return Results.Json(briefs);
        });

        // List all agents with profile data (engine + shared data)
        app.MapGet("/api/agents", () =>
        {
            var result = new List<object>();
            var seen = new HashSet<string>();

            void AddAgentsFrom(IAgentLoader loader)
            {
                foreach (var (id, name, key, file) in loader.ListAgents())
                {
                    if (!seen.Add(key)) continue; // skip duplicates
                    try
                    {
                        var config = loader.LoadAgentByKey(key);
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
            }

            // Engine agents first (these are the ones that actually work with the engine)
            AddAgentsFrom(agentLoader);

            // Shared agents (additional agents from _SYSTEM/data)
            if (sharedAgentLoader != null)
                AddAgentsFrom(sharedAgentLoader);

            return Results.Json(result);
        });

        // List all teams (engine + shared data)
        app.MapGet("/api/teams", () =>
        {
            var result = new List<object>();
            var seen = new HashSet<string>();

            void AddTeamsFrom(IAgentLoader loader)
            {
                foreach (var (name, file, count) in loader.ListTeams())
                {
                    var teamName = Path.GetFileNameWithoutExtension(file);
                    if (!seen.Add(teamName)) continue;
                    try
                    {
                        var team = loader.LoadTeamByName(teamName);
                        var agentKeys = team.Agents.Keys.OrderBy(k => k).ToList();
                        result.Add(new
                        {
                            name = teamName,
                            displayName = name,
                            agentCount = count,
                            agents = agentKeys,
                            modes = team.Modes.Keys.OrderBy(k => k).ToList(),
                            defaultMode = team.DefaultMode,
                        });
                    }
                    catch
                    {
                        result.Add(new { name = teamName, displayName = name, agentCount = count, agents = new List<string>(), modes = new List<string>(), defaultMode = "default" });
                    }
                }
            }

            AddTeamsFrom(agentLoader);
            if (sharedAgentLoader != null)
                AddTeamsFrom(sharedAgentLoader);

            return Results.Json(result);
        });

        // Start a new session
        app.MapPost("/api/session/start", async (HttpContext ctx) =>
        {
            if (sessionManager.IsRunning)
                return Results.Conflict(new { error = "A session is already running" });

            using var reader = new StreamReader(ctx.Request.Body);
            var body = await reader.ReadToEndAsync();

            string topic;
            string? team = null;
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
                if (json.RootElement.TryGetProperty("team", out var teamEl))
                    team = teamEl.GetString();
            }
            catch
            {
                return Results.BadRequest(new { error = "Invalid request body" });
            }

            if (string.IsNullOrWhiteSpace(topic))
                return Results.BadRequest(new { error = "Topic is required" });

            var preparer = new SessionPreparer(agentLoader, sessionManager.ConfigLoader);
            var config = preparer.PrepareFromArgs(topic, team: team, agents: agentKeys);
            config.Source = "api";

            var newEmitter = new SseSessionEmitter();
            if (!sessionManager.Start(config, newEmitter))
                return Results.Conflict(new { error = "Failed to start session" });

            return Results.Ok(new { status = "started", title = config.Title });
        });

        // Stop the running session
        app.MapPost("/api/session/stop", () =>
        {
            if (!sessionManager.IsRunning)
                return Results.NotFound(new { error = "No session is running" });

            sessionManager.Stop();
            return Results.Ok(new { status = "stopped" });
        });

        return app;
    }
}
