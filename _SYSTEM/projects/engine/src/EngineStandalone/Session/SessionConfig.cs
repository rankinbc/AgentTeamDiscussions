// Unified session manifest — the single source of truth for a session.
// Created during preparation (interactive CLI or file-based), consumed by SessionRunner,
// updated in-place during execution. Replaces the old session_status.json + brief file + CLI flags split.

using System.Text.Json;
using System.Text.Json.Serialization;
using EngineStandalone.Types;

namespace EngineStandalone.Session;

/// <summary>
/// Complete session specification and runtime state in one object.
/// Written to session.json at session creation, updated during execution.
/// </summary>
public class SessionConfig
{
    /// <summary>Schema version for forward compatibility.</summary>
    public int Version { get; set; } = 1;

    /// <summary>When the session was created (UTC ISO 8601).</summary>
    public string Created { get; set; } = DateTime.UtcNow.ToString("o");

    /// <summary>Human-readable session title (derived from first question or user input).</summary>
    public string Title { get; set; } = "";

    // --- Intent (what to discuss) ---

    /// <summary>Things already decided — context every agent sees.</summary>
    public List<string> Decided { get; set; } = new();

    /// <summary>Questions to discuss.</summary>
    public List<SessionQuestion> Questions { get; set; } = new();

    // --- Configuration (who discusses, how) ---

    /// <summary>Team name (matches a YAML file in data/teams/).</summary>
    public string Team { get; set; } = "beta-agents";

    /// <summary>
    /// Agent keys to include. When set, only these agents participate.
    /// When empty/null, all agents from the team are used.
    /// </summary>
    public List<string>? Agents { get; set; }

    /// <summary>Experiment mode name (from the team's modes).</summary>
    public string Mode { get; set; } = "compete";

    /// <summary>Timeout per LLM call in seconds.</summary>
    public int Timeout { get; set; } = 120;

    // --- Source tracking ---

    /// <summary>Where this session config came from (file path, "interactive", or "api").</summary>
    public string Source { get; set; } = "interactive";

    /// <summary>SHA256 hash of the question list for resume integrity.</summary>
    public string? QuestionHash { get; set; }

    // --- Runtime state (updated during execution) ---

    /// <summary>Runtime execution state.</summary>
    public SessionState State { get; set; } = new();

    /// <summary>Path to team YAML actually used (resolved at runtime).</summary>
    public string? ResolvedTeamPath { get; set; }
}

/// <summary>
/// A question within the session config.
/// </summary>
public class SessionQuestion
{
    public int Number { get; set; }
    public string Title { get; set; } = "";
    public string Body { get; set; } = "";
}

/// <summary>
/// Runtime execution state — the mutable part of session.json.
/// </summary>
public class SessionState
{
    /// <summary>Overall session status.</summary>
    public SessionRunStatus Status { get; set; } = SessionRunStatus.Ready;

    public bool SessionComplete { get; set; }
    public int TotalElapsedSeconds { get; set; }
    public int CompletedQuestions { get; set; }
    public int FailedQuestions { get; set; }

    /// <summary>Per-question execution status.</summary>
    public Dictionary<string, QuestionState> Questions { get; set; } = new();
}

/// <summary>
/// Execution state for a single question.
/// </summary>
public class QuestionState
{
    public QuestionRunStatus Status { get; set; }
    public string? Title { get; set; }
    public string? Reason { get; set; }
    public int ElapsedSeconds { get; set; }
    public string? File { get; set; }
    public Dictionary<string, RoundRunStatus>? Rounds { get; set; }
}

/// <summary>
/// JSON serialization helpers for SessionConfig.
/// </summary>
public static class SessionConfigIO
{
    private static readonly JsonSerializerOptions JsonOptions = new()
    {
        WriteIndented = true,
        PropertyNamingPolicy = JsonNamingPolicy.SnakeCaseLower,
        DefaultIgnoreCondition = JsonIgnoreCondition.WhenWritingNull,
        Converters = { new JsonStringEnumConverter(JsonNamingPolicy.SnakeCaseLower) }
    };

    private static readonly JsonSerializerOptions ReadOptions = new()
    {
        PropertyNamingPolicy = JsonNamingPolicy.SnakeCaseLower,
        Converters = { new JsonStringEnumConverter(JsonNamingPolicy.SnakeCaseLower) }
    };

    /// <summary>Write session.json to a session directory.</summary>
    public static void Write(string sessionDir, SessionConfig config)
    {
        var path = Path.Combine(sessionDir, "session.json");
        var json = JsonSerializer.Serialize(config, JsonOptions);
        File.WriteAllText(path, json);
    }

    /// <summary>Read session.json from a session directory. Returns null if missing or corrupt.</summary>
    public static SessionConfig? Read(string sessionDir)
    {
        var path = Path.Combine(sessionDir, "session.json");
        if (!File.Exists(path))
            return null;

        try
        {
            var json = File.ReadAllText(path);
            return JsonSerializer.Deserialize<SessionConfig>(json, ReadOptions);
        }
        catch
        {
            return null;
        }
    }

    /// <summary>Check if a session directory has a session.json.</summary>
    public static bool Exists(string sessionDir)
        => File.Exists(Path.Combine(sessionDir, "session.json"));
}
