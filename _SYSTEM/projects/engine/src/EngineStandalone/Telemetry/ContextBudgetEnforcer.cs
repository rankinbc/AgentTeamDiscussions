// ContextBudgetEnforcer.cs — Diagnoses and enforces token budgets on agent payloads.
// Runs in three phases: per-section ceiling enforcement, diagnosis, and progressive
// trimming of cuttable sections in priority order. Protected sections are never cut.

using EngineStandalone.Abstractions;
using EngineStandalone.Config;

namespace EngineStandalone.Telemetry;

/// <summary>
/// Evaluates context sections against configured budgets and trims when necessary.
/// </summary>
public class ContextBudgetEnforcer : IContextBudgetEnforcer
{
    // Per-section ceiling map: section name -> config property accessor
    private static readonly Dictionary<string, Func<ContextBudgetSettings, int>> SectionCeilings = new()
    {
        ["prior_rounds"] = b => b.MaxPriorRoundsChars,
        ["prior_specs"] = b => b.MaxPriorSpecsChars,
        ["decisions"] = b => b.MaxDecisionsChars,
        ["this_round_so_far"] = b => b.MaxThisRoundSoFarChars
    };

    public ContextDiagnosis Diagnose(List<ContextSection> sections, ContextBudgetSettings budget)
    {
        var totalTokens = sections.Sum(s => s.EstimatedTokens);

        if (totalTokens > budget.MaxPayloadTokens)
        {
            return new ContextDiagnosis(
                "over_budget", totalTokens, totalTokens - budget.MaxPayloadTokens, null, 0);
        }

        if (totalTokens < budget.MinPayloadTokens)
        {
            return new ContextDiagnosis("under_budget", totalTokens, 0, null, 0);
        }

        // Check for imbalance
        if (totalTokens > 0)
        {
            foreach (var section in sections)
            {
                if (section.IsProtected || section.EstimatedTokens == 0) continue;
                var pct = (double)section.EstimatedTokens / totalTokens;
                if (pct > budget.ImbalanceThreshold)
                {
                    return new ContextDiagnosis(
                        "imbalanced", totalTokens, 0, section.Name, Math.Round(pct, 3));
                }
            }
        }

        return new ContextDiagnosis("ok", totalTokens, 0, null, 0);
    }

    public List<ContextSection> Enforce(List<ContextSection> sections, ContextBudgetSettings budget)
    {
        // Work on a mutable copy
        var result = sections.Select(s => new ContextSection
        {
            Name = s.Name,
            Content = s.Content,
            IsProtected = s.IsProtected
        }).ToList();

        var rescueActions = new List<string>();

        // Phase 1: Apply per-section char ceilings
        foreach (var section in result)
        {
            if (section.IsProtected) continue;
            if (!SectionCeilings.TryGetValue(section.Name, out var getCeiling)) continue;

            var ceiling = getCeiling(budget);
            if (ceiling > 0 && section.CharCount > ceiling)
            {
                var original = section.CharCount;
                section.Content = TruncateFromFront(section.Content, ceiling);
                rescueActions.Add($"ceiling:{section.Name} {original}->{section.CharCount} chars");
            }
        }

        // Phase 2: Check total budget
        var totalTokens = result.Sum(s => s.EstimatedTokens);
        if (totalTokens <= budget.MaxPayloadTokens)
        {
            // Under budget — apply rescue actions if any ceilings were hit
            if (rescueActions.Count > 0)
            {
                ApplyRescueInfo(result, rescueActions);
            }
            return result;
        }

        // Phase 3: Progressive trimming by priority
        foreach (var sectionName in budget.CutPriority)
        {
            var section = result.FirstOrDefault(s => s.Name == sectionName);
            if (section == null || section.IsProtected || section.CharCount == 0) continue;

            // Pass 1: trim to 50%
            totalTokens = result.Sum(s => s.EstimatedTokens);
            if (totalTokens <= budget.MaxPayloadTokens) break;

            var beforeChars = section.CharCount;
            section.Content = TruncateFromFront(section.Content, section.CharCount / 2);
            rescueActions.Add($"trim50:{section.Name} {beforeChars}->{section.CharCount} chars");

            // Pass 2: trim to 25% of original
            totalTokens = result.Sum(s => s.EstimatedTokens);
            if (totalTokens <= budget.MaxPayloadTokens) break;

            beforeChars = section.CharCount;
            section.Content = TruncateFromFront(section.Content, section.CharCount / 2);
            rescueActions.Add($"trim25:{section.Name} {beforeChars}->{section.CharCount} chars");

            // Pass 3: remove entirely
            totalTokens = result.Sum(s => s.EstimatedTokens);
            if (totalTokens <= budget.MaxPayloadTokens) break;

            rescueActions.Add($"removed:{section.Name} ({beforeChars} chars)");
            section.Content = "";
        }

        ApplyRescueInfo(result, rescueActions);
        return result;
    }

    /// <summary>
    /// Truncates text from the front, keeping the tail (most recent content).
    /// Finds the nearest newline boundary to avoid cutting mid-line.
    /// </summary>
    private static string TruncateFromFront(string text, int maxChars)
    {
        if (text.Length <= maxChars) return text;

        var trimmed = text.Substring(text.Length - maxChars);
        var newlineIdx = trimmed.IndexOf('\n');
        if (newlineIdx > 0 && newlineIdx < maxChars / 2)
        {
            trimmed = trimmed.Substring(newlineIdx + 1);
        }

        return $"[...truncated...]\n{trimmed}";
    }

    /// <summary>
    /// Marks sections as rescued by storing rescue info in a convention the snapshot can read.
    /// We use a sentinel section to pass rescue metadata back through the section list.
    /// </summary>
    private static void ApplyRescueInfo(List<ContextSection> sections, List<string> rescueActions)
    {
        if (rescueActions.Count == 0) return;

        // Add a hidden metadata section that ContextSnapshot will detect
        sections.Add(new ContextSection
        {
            Name = "_rescue_metadata",
            Content = string.Join("|", rescueActions),
            IsProtected = true // won't be cut
        });
    }
}
