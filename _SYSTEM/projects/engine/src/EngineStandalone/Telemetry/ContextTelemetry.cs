// ContextTelemetry.cs — Records per-turn context snapshots, logs to console,
// and writes context_stats.json at session end. Thread-safe via ConcurrentBag
// for parallel round execution.

using System.Collections.Concurrent;
using System.Text.Json;
using System.Text.Json.Serialization;
using EngineStandalone.Abstractions;

namespace EngineStandalone.Telemetry;

/// <summary>
/// Collects context snapshots and produces telemetry output.
/// </summary>
public class ContextTelemetry : IContextTelemetry
{
    private readonly ConcurrentBag<ContextSnapshot> _snapshots = new();

    private static readonly JsonSerializerOptions JsonOptions = new()
    {
        WriteIndented = true,
        PropertyNamingPolicy = JsonNamingPolicy.SnakeCaseLower,
        DefaultIgnoreCondition = JsonIgnoreCondition.WhenWritingNull
    };

    public void Record(ContextSnapshot snapshot)
    {
        _snapshots.Add(snapshot);
    }

    public void LogToConsole(ContextSnapshot snapshot)
    {
        var totalTokens = snapshot.TotalEstimatedTokens;
        var budgetPct = snapshot.BudgetTokens > 0
            ? (int)(100.0 * totalTokens / snapshot.BudgetTokens)
            : 0;
        var budgetIndicator = totalTokens > snapshot.BudgetTokens ? " OVER" : "";
        var rescueTag = snapshot.WasRescued ? " [RESCUED]" : "";

        Console.WriteLine($"    [context] {snapshot.AgentKey} | Q{snapshot.QuestionNumber} | " +
                          $"{totalTokens} tokens ({budgetPct}% of {snapshot.BudgetTokens} budget){budgetIndicator}{rescueTag}");

        foreach (var section in snapshot.Sections)
        {
            if (section.CharCount == 0) continue;
            var pct = totalTokens > 0 ? (int)(100.0 * section.EstimatedTokens / totalTokens) : 0;
            var protectedTag = section.IsProtected ? " [protected]" : "";
            Console.WriteLine($"      {section.Name,-25} {section.CharCount,6} chars / {section.EstimatedTokens,5} tokens ({pct}%){protectedTag}");
        }
    }

    public async Task WriteSessionStatsAsync(string sessionDir)
    {
        var snapshots = _snapshots.ToArray();
        if (snapshots.Length == 0) return;

        var summary = ComputeSummary(snapshots);
        var turns = snapshots.Select(s => new TurnEntry
        {
            Agent = s.AgentKey,
            Round = s.Round,
            Question = s.QuestionNumber,
            TotalChars = s.TotalChars,
            TotalTokens = s.TotalEstimatedTokens,
            SystemPromptChars = s.SystemPromptChars,
            SystemPromptTokens = s.SystemPromptEstimatedTokens,
            BudgetTokens = s.BudgetTokens,
            Rescued = s.WasRescued,
            RescueActions = s.RescueActions.Count > 0 ? s.RescueActions : null,
            Sections = s.Sections
                .Where(sec => sec.CharCount > 0)
                .ToDictionary(
                    sec => sec.Name,
                    sec => new SectionStats
                    {
                        Chars = sec.CharCount,
                        Tokens = sec.EstimatedTokens,
                        Protected = sec.IsProtected
                    })
        }).ToList();

        var report = new SessionReport
        {
            Generated = DateTime.UtcNow.ToString("o"),
            Summary = summary,
            Turns = turns
        };

        var json = JsonSerializer.Serialize(report, JsonOptions);
        var path = Path.Combine(sessionDir, "context_stats.json");
        await File.WriteAllTextAsync(path, json);
    }

    private static SessionContextSummary ComputeSummary(ContextSnapshot[] snapshots)
    {
        var tokenValues = snapshots.Select(s => s.TotalEstimatedTokens).ToList();
        var summary = new SessionContextSummary
        {
            TotalTurns = snapshots.Length,
            AvgPayloadTokens = tokenValues.Count > 0 ? tokenValues.Average() : 0,
            MaxPayloadTokens = tokenValues.Count > 0 ? tokenValues.Max() : 0,
            MinPayloadTokens = tokenValues.Count > 0 ? tokenValues.Min() : 0,
            RescueCount = snapshots.Count(s => s.WasRescued),
            OverBudgetCount = snapshots.Count(s => s.TotalEstimatedTokens > s.BudgetTokens)
        };

        // Compute average tokens per section name across all turns
        var sectionNames = snapshots
            .SelectMany(s => s.Sections)
            .Where(sec => sec.CharCount > 0)
            .Select(sec => sec.Name)
            .Distinct();

        foreach (var name in sectionNames)
        {
            var sectionTokens = snapshots
                .SelectMany(s => s.Sections)
                .Where(sec => sec.Name == name && sec.CharCount > 0)
                .Select(sec => (double)sec.EstimatedTokens)
                .ToList();
            if (sectionTokens.Count > 0)
            {
                summary.AvgSectionTokens[name] = Math.Round(sectionTokens.Average(), 1);
            }
        }

        return summary;
    }

    // JSON serialization models
    private class SessionReport
    {
        public string Generated { get; set; } = "";
        public SessionContextSummary Summary { get; set; } = new();
        public List<TurnEntry> Turns { get; set; } = new();
    }

    private class TurnEntry
    {
        public string Agent { get; set; } = "";
        public string Round { get; set; } = "";
        public int Question { get; set; }
        public int TotalChars { get; set; }
        public int TotalTokens { get; set; }
        public int SystemPromptChars { get; set; }
        public int SystemPromptTokens { get; set; }
        public int BudgetTokens { get; set; }
        public bool Rescued { get; set; }
        public List<string>? RescueActions { get; set; }
        public Dictionary<string, SectionStats> Sections { get; set; } = new();
    }
}
