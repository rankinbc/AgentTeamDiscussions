// ContextModels.cs — Data types for context telemetry and budget enforcement.
// ContextSection: one named slice of an agent's assembled prompt.
// ContextSnapshot: full per-turn record of all sections, sizes, and rescue actions.
// ContextDiagnosis: output of budget analysis before enforcement.

namespace EngineStandalone.Telemetry;

/// <summary>
/// One named section of an assembled agent prompt. IsProtected sections
/// are never trimmed by the budget enforcer.
/// </summary>
public record ContextSection(string Name, string Content, bool IsProtected = false)
{
    public int Chars => Content.Length;
    public int Tokens => (int)(Chars / 4.0);
}

/// <summary>
/// Full per-turn snapshot of all context sections, sizes, and any rescue actions taken.
/// BudgetTokens is used for % display only — enforcement is controlled by ContextBudgetSettings.Enabled.
/// </summary>
public class ContextSnapshot
{
    public required string AgentKey { get; init; }
    public required string RoundName { get; init; }
    public required int QuestionNumber { get; init; }
    public required List<ContextSection> Sections { get; init; }
    public required int BudgetTokens { get; init; }
    public List<string> RescueActions { get; init; } = new();

    public int TotalChars => Sections.Sum(s => s.Chars);
    public int TotalTokens => Sections.Sum(s => s.Tokens);
    public double BudgetPercent => BudgetTokens > 0 ? (double)TotalTokens / BudgetTokens : 0;
}

/// <summary>
/// Result of budget analysis for a snapshot. IsImbalanced is true when any single
/// cuttable section exceeds ImbalanceThreshold of total cuttable tokens.
/// </summary>
public class ContextDiagnosis
{
    public bool IsOverBudget { get; init; }
    public bool IsImbalanced { get; init; }
    public string? OffendingSection { get; init; }
    public int ExcessTokens { get; init; }
}
