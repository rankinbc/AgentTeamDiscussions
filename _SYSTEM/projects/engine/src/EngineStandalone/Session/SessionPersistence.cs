// Crash-safe session I/O layer. Every persisted file ends with a <!-- complete --> marker.
// On recovery, files missing the marker are treated as incomplete and re-generated from scratch.
// Progress is derived from artifacts on disk (not a checkpoint file), so the marker is the
// single source of truth for "did this step finish?"

using System.Security.Cryptography;
using System.Text;
using System.Text.Json;

namespace EngineStandalone.Session;

/// <summary>
/// Crash-safe file I/O with completion markers.
/// </summary>
public static class SessionPersistence
{
    public const string CompletionMarker = "\n<!-- complete -->\n";

    /// <summary>
    /// Write content with a completion marker.
    /// </summary>
    public static void WriteWithMarker(string path, string content)
    {
        var dir = Path.GetDirectoryName(path);
        if (!string.IsNullOrEmpty(dir) && !Directory.Exists(dir))
        {
            Directory.CreateDirectory(dir);
        }

        // Two explicit flushes: content first, then marker. If the process crashes
        // between flushes, the marker is absent and recovery treats the file as incomplete.
        using var writer = new StreamWriter(path, false, Encoding.UTF8);
        writer.Write(content);
        writer.Flush();
        writer.Write(CompletionMarker);
        writer.Flush();
    }

    /// <summary>
    /// Check if a file is complete (has the completion marker).
    /// </summary>
    public static bool IsComplete(string path)
    {
        if (!File.Exists(path))
            return false;

        try
        {
            var content = File.ReadAllText(path);
            return content.Contains("<!-- complete -->");
        }
        catch
        {
            return false;
        }
    }

    /// <summary>
    /// Read a file without the completion marker.
    /// </summary>
    public static string ReadWithoutMarker(string path)
    {
        var content = File.ReadAllText(path);
        return content
            .Replace(CompletionMarker, "")
            .Replace("<!-- complete -->", "")
            .Trim();
    }

    /// <summary>
    /// Create a session directory with the standard structure.
    /// Folder name is timestamped: YYYY-MM-DD_HHMM_slug.
    /// </summary>
    public static string CreateSessionDir(string sessionsRoot, string briefName)
    {
        var name = $"{DateTime.Now:yyyy-MM-dd_HHmm}_{briefName}";
        var sessionDir = Path.Combine(sessionsRoot, name);

        Directory.CreateDirectory(sessionDir);
        Directory.CreateDirectory(Path.Combine(sessionDir, "questions"));

        return sessionDir;
    }

    /// <summary>
    /// Hash a question list for session integrity checking.
    /// SHA256 of the serialized question list. Prevents resuming a session
    /// after the brief has been modified (hash mismatch = start fresh).
    /// </summary>
    public static string HashQuestionList(IEnumerable<(int Number, string Title)> questions)
    {
        var content = JsonSerializer.Serialize(
            questions.Select(q => new { n = q.Number, t = q.Title }).ToList(),
            new JsonSerializerOptions { WriteIndented = false });

        using var sha256 = SHA256.Create();
        var hashBytes = sha256.ComputeHash(Encoding.UTF8.GetBytes(content));
        return Convert.ToHexString(hashBytes).Substring(0, 16).ToLower();
    }

    /// <summary>
    /// Count completed questions in a session directory.
    /// </summary>
    public static int CountCompletedQuestions(string sessionDir)
    {
        var questionsDir = Path.Combine(sessionDir, "questions");
        if (!Directory.Exists(questionsDir))
            return 0;

        return Directory.GetFiles(questionsDir, "*.md")
            .Where(f => !f.EndsWith("-transcript.md"))
            .Count(IsComplete);
    }

    /// <summary>
    /// Write session status JSON (legacy format).
    /// </summary>
    public static void WriteSessionStatus(string sessionDir, SessionStatus status)
    {
        var path = Path.Combine(sessionDir, "session_status.json");
        var json = JsonSerializer.Serialize(status, new JsonSerializerOptions
        {
            WriteIndented = true,
            PropertyNamingPolicy = JsonNamingPolicy.SnakeCaseLower
        });
        File.WriteAllText(path, json);
    }

    /// <summary>
    /// Load session status JSON (legacy format).
    /// </summary>
    public static SessionStatus LoadSessionStatus(string sessionDir)
    {
        var path = Path.Combine(sessionDir, "session_status.json");
        if (!File.Exists(path))
            return new SessionStatus();

        try
        {
            var json = File.ReadAllText(path);
            return JsonSerializer.Deserialize<SessionStatus>(json, new JsonSerializerOptions
            {
                PropertyNamingPolicy = JsonNamingPolicy.SnakeCaseLower
            }) ?? new SessionStatus();
        }
        catch
        {
            return new SessionStatus();
        }
    }

    // --- SessionConfig-based persistence (new unified format) ---

    /// <summary>
    /// Write session.json — the unified session manifest.
    /// </summary>
    public static void WriteSessionConfig(string sessionDir, SessionConfig config)
        => SessionConfigIO.Write(sessionDir, config);

    /// <summary>
    /// Load session.json — returns null if missing or corrupt.
    /// </summary>
    public static SessionConfig? LoadSessionConfig(string sessionDir)
        => SessionConfigIO.Read(sessionDir);

    /// <summary>
    /// Update the runtime state portion of session.json without rewriting the entire config.
    /// </summary>
    public static void UpdateSessionState(string sessionDir, Action<SessionState> mutate)
    {
        var config = LoadSessionConfig(sessionDir);
        if (config == null) return;
        mutate(config.State);
        WriteSessionConfig(sessionDir, config);
    }
}

/// <summary>
/// Session status tracking.
/// </summary>
public class SessionStatus
{
    public string? QuestionHash { get; set; }
    public string? Mode { get; set; }
    public string? Brief { get; set; }
    public string? Team { get; set; }
    public bool SessionComplete { get; set; }
    public int TotalElapsedSeconds { get; set; }
    public int CompletedQuestions { get; set; }
    public int FailedQuestions { get; set; }
    public Dictionary<string, QuestionStatus> Questions { get; set; } = new();
}

/// <summary>
/// Status of a single question.
/// </summary>
public class QuestionStatus
{
    public string Status { get; set; } = "";
    public string? Title { get; set; }
    public string? Reason { get; set; }
    public int ElapsedSeconds { get; set; }
    public string? File { get; set; }
    public Dictionary<string, string>? Rounds { get; set; }
}
