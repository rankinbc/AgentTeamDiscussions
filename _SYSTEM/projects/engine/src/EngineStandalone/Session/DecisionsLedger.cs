// Append-only decisions ledger. Never edited, never summarized.
// Accumulates across ALL questions and chains forward as context for subsequent questions.
// Format: ### Q{N}: {topic} followed by - DECIDED: / - OPEN: entries.

using System.Text.RegularExpressions;

namespace EngineStandalone.Session;

/// <summary>
/// Manages the append-only decisions ledger.
/// </summary>
public static class DecisionsLedger
{
    /// <summary>
    /// Get the path to the decisions ledger file.
    /// </summary>
    public static string GetLedgerPath(string sessionDir)
    {
        return Path.Combine(sessionDir, "decisions_ledger.md");
    }

    /// <summary>
    /// Read the current ledger contents.
    /// </summary>
    public static string ReadLedger(string sessionDir)
    {
        var path = GetLedgerPath(sessionDir);
        if (!File.Exists(path))
            return "";

        return SessionPersistence.ReadWithoutMarker(path);
    }

    /// <summary>
    /// Extract the ## Ledger section from a design doc.
    /// Falls back to parsing ## Decisions sub-headings if ## Ledger is absent.
    /// </summary>
    public static string? ExtractLedgerSection(string designDoc)
    {
        // Primary: explicit ## Ledger section with - DECIDED: entries
        var match = Regex.Match(designDoc, @"## Ledger\s*\n(.*?)(?=\n## |\Z)", RegexOptions.Singleline);
        if (match.Success)
            return match.Value.Trim();

        // Fallback: parse ### sub-headings under ## Decisions into ledger entries
        var decisionsMatch = Regex.Match(designDoc, @"## Decisions\s*\n(.*?)(?=\n## |\Z)", RegexOptions.Singleline);
        if (!decisionsMatch.Success)
            return null;

        var body = decisionsMatch.Groups[1].Value;
        var subHeadings = Regex.Matches(body, @"^### (.+)$", RegexOptions.Multiline);
        if (subHeadings.Count == 0)
            return null;

        var entries = subHeadings
            .Cast<Match>()
            .Select(m => $"- DECIDED: {m.Groups[1].Value.Trim()}")
            .ToList();

        return string.Join("\n", entries);
    }

    /// <summary>
    /// Check if the ledger extraction is consistent with the design doc.
    /// Validates that the ledger decision count is 0.2-4.0x the design doc's decision count.
    /// Extreme ratios indicate hallucinated extraction by the LLM.
    /// </summary>
    public static bool HallucinationCheck(string designDoc, string ledgerSection, double ratioMax = 4.0, double ratioMin = 0.2)
    {
        // Count decisions in design doc (various patterns)
        var docDecisions = Regex.Matches(designDoc, @"(?:^### D\d|^### [A-Z]|\d+\.\s+\*\*)", RegexOptions.Multiline).Count;
        if (docDecisions == 0)
        {
            docDecisions = Regex.Matches(designDoc, @"^### ", RegexOptions.Multiline).Count;
        }

        // Count ledger decisions
        var ledgerDecisions = Regex.Matches(ledgerSection, @"- (DECIDED|CONTESTED):").Count;

        if (docDecisions == 0)
            return true;

        var ratio = (double)ledgerDecisions / docDecisions;
        return !(ratio > ratioMax || ratio < ratioMin);
    }

    /// <summary>
    /// Append a section to the ledger (skip if question already exists).
    /// Idempotent: won't duplicate if ### Q{n}: already present.
    /// </summary>
    public static void AppendToLedger(string sessionDir, string ledgerSection, int questionNumber, string? questionTitle = null)
    {
        var path = GetLedgerPath(sessionDir);
        var existing = File.Exists(path)
            ? SessionPersistence.ReadWithoutMarker(path)
            : "";

        // Idempotency guard: skip if this question's header already exists
        if (existing.Contains($"### Q{questionNumber}:"))
            return;

        // Prepend question header if the section doesn't already have one
        if (!ledgerSection.Contains($"### Q{questionNumber}:"))
        {
            var title = questionTitle ?? $"Question {questionNumber}";
            var truncatedTitle = title.Length > 60 ? title[..60] : title;
            ledgerSection = $"### Q{questionNumber}: {truncatedTitle}\n{ledgerSection}";
        }

        var newContent = existing.TrimEnd() + "\n\n" + ledgerSection + "\n";
        SessionPersistence.WriteWithMarker(path, newContent);
    }

    /// <summary>
    /// Create a fallback ledger entry when extraction fails.
    /// </summary>
    public static string CreateFallbackEntry(int questionNumber, string questionTitle)
    {
        var truncatedTitle = questionTitle.Length > 40 ? questionTitle.Substring(0, 40) : questionTitle;
        return $"### Q{questionNumber}: {truncatedTitle}\n- DECIDED: See design doc for details\n";
    }
}
