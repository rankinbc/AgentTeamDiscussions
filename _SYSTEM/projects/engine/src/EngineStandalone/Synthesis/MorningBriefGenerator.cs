// Morning Brief generator. Produces a <300-word executive summary designed for a 90-second read.
// Generated via LLM synthesis from the accumulated decisions ledger + any session gaps
// (failed/skipped questions). Unlike the v1 spec (zero-LLM assembly), this uses an LLM call.

using System.Text;
using EngineStandalone.Abstractions;
using EngineStandalone.Config;
using EngineStandalone.Runner;
using EngineStandalone.Session;

namespace EngineStandalone.Synthesis;

/// <summary>
/// Generates the Morning Brief summary from the decisions ledger.
/// </summary>
public class MorningBriefGenerator : IMorningBriefGenerator
{
    private readonly IClaudeRunner _claudeRunner;
    private readonly IConfigLoader _configLoader;
    private readonly string _systemPrompt;
    private readonly string _userPrompt;

    public MorningBriefGenerator(IClaudeRunner claudeRunner, IConfigLoader configLoader)
    {
        _claudeRunner = claudeRunner;
        _configLoader = configLoader;

        // Load prompts
        _systemPrompt = configLoader.LoadPromptRaw("prompts/morning_brief_system.md.j2");
        _userPrompt = configLoader.LoadPromptRaw("prompts/morning_brief_user.md.j2");
    }

    /// <summary>
    /// Generate the Morning Brief from the ledger and session status.
    /// </summary>
    public async Task<string> GenerateAsync(string ledgerText, SessionStatus status, int timeout)
    {
        var gaps = new List<string>();

        // Collect session gaps so the brief can flag incomplete areas to the reader.
        foreach (var (qKey, qStatus) in status.Questions.OrderBy(kv => kv.Key))
        {
            if (qStatus.Status is "skipped" or "partial" or "failed")
            {
                var reason = qStatus.Reason ?? "unknown";
                gaps.Add($"- {qKey} ({qStatus.Title ?? "?"}): {qStatus.Status} -- {reason}");
            }
        }

        var gapSection = "";
        if (gaps.Count > 0)
        {
            gapSection = "\n\nSESSION GAPS (include these in your output):\n" + string.Join("\n", gaps);
        }

        var payload = $"## Decisions Ledger\n\n{ledgerText}\n{gapSection}";

        var response = await _claudeRunner.RunAsync(
            _systemPrompt + "\n\n" + _userPrompt,
            payload,
            timeout);

        return response;
    }
}
