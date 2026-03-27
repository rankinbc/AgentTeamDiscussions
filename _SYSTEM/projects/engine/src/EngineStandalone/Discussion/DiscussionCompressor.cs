using System.Text;
using System.Text.RegularExpressions;

namespace EngineStandalone.Discussion;

/// <summary>
/// Utilities for compressing and extracting structured content from agent discussion transcripts.
/// Separated from PromptBuilder because these operate on discussion output, not prompt assembly.
/// </summary>
public static class DiscussionCompressor
{
    /// <summary>
    /// Extract the ## Position Summary block from an agent response.
    /// Falls back to the last ~300 characters if no summary block is found.
    /// </summary>
    public static string ExtractPositionSummary(string response)
    {
        if (string.IsNullOrEmpty(response))
            return "";

        var match = Regex.Match(response,
            @"##\s*Position Summary\s*\n(.*?)(?=\n## |\Z)",
            RegexOptions.Singleline);
        if (match.Success)
            return match.Groups[1].Value.Trim();

        if (response.Length <= 300)
            return response.Trim();

        var tail = response.Substring(response.Length - 300);
        var sentenceStart = tail.IndexOf(". ", StringComparison.Ordinal);
        if (sentenceStart > 0 && sentenceStart < 200)
            tail = tail.Substring(sentenceStart + 2);

        return tail.Trim();
    }

    /// <summary>
    /// Compress accumulated discussion to position summaries only.
    /// Parses [ROUND - Agent] blocks and extracts each agent's summary.
    /// </summary>
    public static string CompressToSummaries(string accumulatedDiscussion)
    {
        if (string.IsNullOrEmpty(accumulatedDiscussion))
            return "";

        var blocks = Regex.Matches(accumulatedDiscussion,
            @"\[([^\]]+)\]\n(.*?)(?=\n\[|\Z)",
            RegexOptions.Singleline);

        var sb = new StringBuilder();
        foreach (Match block in blocks)
        {
            var header = block.Groups[1].Value;
            var body = block.Groups[2].Value;
            var summary = ExtractPositionSummary(body);
            sb.AppendLine($"[{header}]");
            sb.AppendLine(summary);
            sb.AppendLine();
        }
        return sb.ToString();
    }
}
