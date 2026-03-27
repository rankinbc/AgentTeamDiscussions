// ContextBudgetEnforcer.cs — Diagnoses over-budget/imbalanced context snapshots
// and rescues them by progressively trimming sections in priority order.
//
// Cut priority (first = cut first):
//   prior_rounds, prior_specs, decisions, open_questions,
//   this_round_so_far, context_lens, role_overlay
//
// Rescue passes: trim to 50% → 25% → remove entirely.
// Trimming truncates from the front at a \n boundary to preserve recency.
// Protected sections (IsProtected=true) are never touched.

using EngineStandalone.Abstractions;

namespace EngineStandalone.Telemetry;

/// <summary>
/// Detects over-budget and imbalanced prompts, then trims in priority order
/// until under the token ceiling.
/// </summary>
public class ContextBudgetEnforcer : IContextBudgetEnforcer
{
    private readonly int _maxPayloadTokens;
    private readonly double _imbalanceThreshold;

    private static readonly string[] CutPriority =
    [
        "prior_rounds",
        "prior_specs",
        "decisions",
        "open_questions",
        "this_round_so_far",
        "context_lens",
        "role_overlay"
    ];

    public ContextBudgetEnforcer(int maxPayloadTokens, double imbalanceThreshold = 0.60)
    {
        _maxPayloadTokens = maxPayloadTokens;
        _imbalanceThreshold = imbalanceThreshold;
    }

    public ContextDiagnosis Diagnose(ContextSnapshot snapshot)
    {
        var isOverBudget = snapshot.TotalTokens > _maxPayloadTokens;
        var excessTokens = Math.Max(0, snapshot.TotalTokens - _maxPayloadTokens);

        var cuttableSections = snapshot.Sections
            .Where(s => !s.IsProtected && s.Chars > 0)
            .ToList();

        var cuttableTotal = cuttableSections.Sum(s => s.Tokens);
        string? offendingSection = null;
        var isImbalanced = false;

        if (cuttableTotal > 0)
        {
            var largest = cuttableSections
                .OrderByDescending(s => s.Tokens)
                .First();

            if ((double)largest.Tokens / cuttableTotal > _imbalanceThreshold)
            {
                isImbalanced = true;
                offendingSection = largest.Name;
            }
        }

        return new ContextDiagnosis
        {
            IsOverBudget = isOverBudget,
            IsImbalanced = isImbalanced,
            OffendingSection = offendingSection,
            ExcessTokens = excessTokens
        };
    }

    public (List<ContextSection> Sections, List<string> RescueActions) Enforce(
        List<ContextSection> sections, ContextDiagnosis diagnosis)
    {
        var working = sections.Select(s => s).ToList();
        var actions = new List<string>();

        // Three passes: trim to 50%, then 25%, then remove
        double[] targets = [0.50, 0.25, 0.0];

        foreach (var target in targets)
        {
            if (TotalTokens(working) <= _maxPayloadTokens)
                break;

            foreach (var name in CutPriority)
            {
                if (TotalTokens(working) <= _maxPayloadTokens)
                    break;

                var idx = working.FindIndex(s => s.Name == name && !s.IsProtected);
                if (idx < 0) continue;

                var section = working[idx];
                if (section.Chars == 0) continue;

                if (target == 0.0)
                {
                    actions.Add($"{name}: removed ({section.Tokens} tokens)");
                    working[idx] = section with { Content = "" };
                }
                else
                {
                    var targetChars = (int)(section.Chars * target);
                    if (targetChars >= section.Chars) continue;

                    var trimmed = TrimFromFront(section.Content, targetChars);
                    if (trimmed.Length >= section.Chars) continue;

                    var newSection = section with { Content = trimmed };
                    actions.Add($"{name}: trimmed to {(int)(target * 100)}% ({section.Tokens}→{newSection.Tokens} tokens)");
                    working[idx] = newSection;
                }
            }
        }

        return (working, actions);
    }

    /// <summary>
    /// Trims content to at most targetChars, cutting from the front at a newline boundary
    /// to preserve the most recent content.
    /// </summary>
    private static string TrimFromFront(string content, int targetChars)
    {
        if (content.Length <= targetChars)
            return content;

        var tail = content.Substring(content.Length - targetChars);

        // Snap to next newline boundary so we don't cut mid-line
        var nlIdx = tail.IndexOf('\n');
        if (nlIdx > 0 && nlIdx < targetChars / 2)
            tail = tail.Substring(nlIdx + 1);

        return tail;
    }

    private static int TotalTokens(List<ContextSection> sections) =>
        sections.Sum(s => s.Tokens);
}
