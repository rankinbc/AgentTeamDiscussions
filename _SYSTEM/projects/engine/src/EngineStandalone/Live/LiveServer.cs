// ASP.NET Core Minimal API server started when --live flag is used.
// Exposes endpoints the React UI expects: GET /events (SSE), GET /ledger,
// POST /moderator, POST /questions/add. Adds CORS headers for Vite dev server.
using System.Text.Json;

namespace EngineStandalone.Live;

/// <summary>
/// Configures and starts the ASP.NET Core Minimal API server for live SSE streaming.
/// Endpoints: GET /events (SSE), GET /ledger, POST /moderator, POST /questions/add
/// </summary>
public static class LiveServer
{
    public static WebApplication Build(SseSessionEmitter emitter, int port = 8899)
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
            ctx.Response.ContentType = "text/event-stream";
            ctx.Response.Headers.Append("Cache-Control", "no-cache");
            ctx.Response.Headers.Append("Connection", "keep-alive");

            var channel = emitter.Subscribe();
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
            var sessionDir = emitter.SessionDir;
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

        return app;
    }
}
