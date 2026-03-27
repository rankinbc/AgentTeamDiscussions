// ContextModels.cs — Data models for context telemetry and budget enforcement.
// ContextSection captures one named section of a payload. ContextSnapshot captures
// the full measurement for one agent turn. ContextDiagnosis reports budget health.

namespace EngineStandalone.Telemetry;

/// <summary>
/// One named section of the user payload with its size measurements.
/// </summary>
public class ContextSection
{
    public string Name { get; set; } = "";
    public string Content { get; set; } = "";
    public int CharCount => Content.Length;
    public int EstimatedTokens => EstimateTokens(Content);
    public bool IsProtected { get; set; }

    /// <summary>
    /// Approximate token count using word-count heuristic.
    /// Good enough for relative comparisons and budget enforcement.
    /// </summary>
    public static int EstimateTokens(string text)
    {
        if (string.IsNullOrEmpty(text)) return 0;
        var words = text.Split(default(char[]), StringSplitOptions.RemoveEmptyEntries).Length;
        return (int)(words * 1.3);
    }
}

/// <summary>
/// Full measurement snapshot for one agent turn. Recorded by ContextTelemetry,
/// emitted as an SSE event, and written to context_stats.json at session end.
/// </summary>
public class ContextSnapshot
{
    public string AgentKey { get; set; } = "";
    public string Round { get; set; } = "";
    public int QuestionNumber { get; set; }
    public DateTime Timestamp { get; set; } = DateTime.UtcNow;

    public List<ContextSection> Sections { get; set; } = new();

    public int TotalChars => Sections.Sum(s => s.CharCount);
    public int TotalEstimatedTokens => Sections.Sum(s => s.EstimatedTokens);

    public int SystemPromptChars { get; set; }
    public int SystemPromptEstimatedTokens { get; set; }

    public int BudgetTokens { get; set; }
    public bool WasRescued { get; set; }
    public List<string> RescueActions { get; set; } = new();
}

/// <summary>
/// Diagnostic result from budget evaluation. Reports whether the payload is
/// healthy, over budget, under budget, or imbalanced (one section dominating).
/// </summary>
public record ContextDiagnosis(
    string Status,             // "ok", "over_budget", "under_budget", "imbalanced"
    int TotalTokens,
    int OverByTokens,
    string? DominantSection,   // section name if imbalanced
    double DominantPct         // percentage of total the dominant section occupies
);

/// <summary>
/// Per-section stats for JSON serialization in context_stats.json.
/// </summary>
public class SectionStats
{
    public int Chars { get; set; }
    public int Tokens { get; set; }
    public bool Protected { get; set; }
    public bool Trimmed { get; set; }
    public int? OriginalChars { get; set; }
}

/// <summary>
/// Summary statistics across all turns in a session.
/// </summary>
public class SessionContextSummary
{
    public int TotalTurns { get; set; }
    public double AvgPayloadTokens { get; set; }
    public int MaxPayloadTokens { get; set; }
    public int MinPayloadTokens { get; set; }
    public int RescueCount { get; set; }
    public int ImbalancedCount { get; set; }
    public int OverBudgetCount { get; set; }
    public Dictionary<string, double> AvgSectionTokens { get; set; } = new();
}
