// ASP.NET Core Minimal API server started when --live flag is used.
// Exposes endpoints the React UI expects: GET /events (SSE), GET /ledger,
// POST /moderator, POST /questions/add. Adds CORS headers for Vite dev server.
using System.Text.Json;
using EngineStandalone.Abstractions;
using EngineStandalone.Session;

namespace EngineStandalone.Live;

/// <summary>
/// Configures and starts the ASP.NET Core Minimal API server for live SSE streaming.
/// Endpoints: GET /events (SSE), GET /ledger, POST /moderator, POST /questions/add,
/// GET /api/briefs, GET /api/agents, POST /api/session/start, POST /api/session/stop
/// </summary>
public static class LiveServer
{
    public static WebApplication Build(SseSessionEmitter emitter, SessionManager sessionManager, IAgentLoader agentLoader, string baseDir, int port = 8899)
    {
        var builder = WebApplication.CreateBuilder();
        builder.WebHost.UseUrls($"http://0.0.0.0:{port}");
        builder.Logging.ClearProviders(); // Suppress Kestrel noise

        var app = builder.Build();

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

        // List all agents with profile data
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

        // Start a new session
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
