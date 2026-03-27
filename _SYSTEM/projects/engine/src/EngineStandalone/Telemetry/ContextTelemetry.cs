// ContextTelemetry.cs — Records per-turn context snapshots, logs to console,
// and writes context_stats.json at session end.
// ConcurrentBag ensures parallel-mode agent turns don't race on accumulation.
// WriteSessionStatsAsync clears the bag after writing to prevent cross-session accumulation.

using System.Collections.Concurrent;
using System.Text.Json;
using EngineStandalone.Abstractions;

namespace EngineStandalone.Telemetry;

/// <summary>
/// Thread-safe telemetry service. Console output is immediate per-turn;
/// JSON is written once at session end.
/// </summary>
public class ContextTelemetry : IContextTelemetry
{
    private readonly ConcurrentBag<ContextSnapshot> _snapshots = new();

    public void Record(ContextSnapshot snapshot)
    {
        _snapshots.Add(snapshot);
    }

    /// <summary>
    /// Prints the per-turn context breakdown table to console.
    /// </summary>
    public void LogToConsole(ContextSnapshot snapshot)
    {
        var budgetPct = snapshot.BudgetPercent * 100;
        var budgetStr = snapshot.BudgetTokens > 0
            ? $" ({budgetPct:F0}% of {snapshot.BudgetTokens} budget)"
            : "";

        var header = $"    [context] {snapshot.AgentKey} | Q{snapshot.QuestionNumber}";
        if (!string.IsNullOrEmpty(snapshot.RoundName))
            header += $" {snapshot.RoundName}";
        header += $" | {snapshot.TotalTokens} tokens{budgetStr}";

        Console.WriteLine(header);

        if (snapshot.RescueActions.Count > 0)
        {
            Console.WriteLine($"      [rescued] {string.Join(", ", snapshot.RescueActions)}");
        }

        var activeSections = snapshot.Sections.Where(s => s.Chars > 0).ToList();
        if (activeSections.Count == 0) return;

        // Column widths for alignment
        var maxNameLen = activeSections.Max(s => s.Name.Length);
        var maxChars = activeSections.Max(s => s.Chars);
        var maxTokens = activeSections.Max(s => s.Tokens);
        var charsWidth = Math.Max(maxChars.ToString().Length, 5);
        var tokensWidth = Math.Max(maxTokens.ToString().Length, 5);

        foreach (var section in activeSections)
        {
            var pct = snapshot.TotalTokens > 0
                ? (int)Math.Round((double)section.Tokens / snapshot.TotalTokens * 100)
                : 0;
            var protectedTag = section.IsProtected ? " [protected]" : "";
            var name = section.Name.PadRight(maxNameLen);
            var chars = section.Chars.ToString().PadLeft(charsWidth);
            var tokens = section.Tokens.ToString().PadLeft(tokensWidth);
            Console.WriteLine($"      {name}  {chars} chars / {tokens} tokens ({pct,2}%){protectedTag}");
        }
    }

    /// <summary>
    /// Serializes all accumulated snapshots to context_stats.json in the session directory,
    /// then clears the bag so the next session starts fresh.
    /// </summary>
    public async Task WriteSessionStatsAsync(string sessionDir)
    {
        var snapshots = _snapshots.ToList();
        if (snapshots.Count == 0) return;

        var path = Path.Combine(sessionDir, "context_stats.json");
        var data = snapshots.Select(s => new
        {
            agent = s.AgentKey,
            round = s.RoundName,
            question = s.QuestionNumber,
            total_tokens = s.TotalTokens,
            total_chars = s.TotalChars,
            budget_tokens = s.BudgetTokens,
            budget_pct = Math.Round(s.BudgetPercent * 100, 1),
            rescue_actions = s.RescueActions,
            sections = s.Sections.Where(sec => sec.Chars > 0).Select(sec => new
            {
                name = sec.Name,
                chars = sec.Chars,
                tokens = sec.Tokens,
                is_protected = sec.IsProtected
            }).ToList()
        }).ToList();

        var json = JsonSerializer.Serialize(data, new JsonSerializerOptions { WriteIndented = true });
        await File.WriteAllTextAsync(path, json);

        // Clear bag — service is singleton, sessions run sequentially
        while (_snapshots.TryTake(out _)) { }
    }
}
