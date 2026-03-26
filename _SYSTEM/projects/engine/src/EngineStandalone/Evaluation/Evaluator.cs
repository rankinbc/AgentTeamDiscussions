// Evaluator.cs — Post-session quality scoring.
// Evaluates design docs and transcripts using LLM calls via ClaudeRunner.
// Produces per-question scores and an experiment-wide summary.
// Invoked via the --eval flag or the `eval` subcommand.

using System.Text;
using System.Text.Json;
using System.Text.RegularExpressions;
using EngineStandalone.Abstractions;
using EngineStandalone.Config;
using EngineStandalone.Runner;

namespace EngineStandalone.Evaluation;

/// <summary>
/// Result of evaluating a design doc/transcript pair.
/// </summary>
public class EvaluationResult
{
    public string Name { get; set; } = "";
    public Dictionary<string, ScoreEntry>? DocScores { get; set; }
    public Dictionary<string, ScoreEntry>? TranscriptScores { get; set; }
    public Dictionary<string, Dictionary<string, ScoreEntry>>? AgentScores { get; set; }
}

/// <summary>
/// A single score entry with score and optional evidence.
/// </summary>
public class ScoreEntry
{
    public double Score { get; set; }
    public string? Evidence { get; set; }
}

/// <summary>
/// Summary of evaluation results.
/// </summary>
public class EvaluationSummary
{
    public Dictionary<string, double> DocAverages { get; set; } = new();
    public Dictionary<string, double> TranscriptAverages { get; set; } = new();
    public Dictionary<string, Dictionary<string, double>> AgentAverages { get; set; } = new();
    public double Overall { get; set; }
}

/// <summary>
/// LLM-based evaluator for agent discussion experiments.
/// </summary>
public class Evaluator
{
    private readonly IClaudeRunner _claudeRunner;
    private readonly IConfigLoader _configLoader;
    private readonly string _evalSystemPrompt;
    private readonly string _designDocEvalPrompt;
    private readonly string _transcriptEvalPrompt;
    private readonly string _agentEvalPrompt;

    public Evaluator(IClaudeRunner claudeRunner, IConfigLoader configLoader)
    {
        _claudeRunner = claudeRunner;
        _configLoader = configLoader;

        // Load evaluation prompts
        _evalSystemPrompt = configLoader.TemplateExists("evaluation/eval_system.md.j2")
            ? configLoader.LoadPromptRaw("evaluation/eval_system.md.j2")
            : GetDefaultEvalSystemPrompt();

        _designDocEvalPrompt = configLoader.TemplateExists("evaluation/design_doc_eval.md.j2")
            ? configLoader.LoadPromptRaw("evaluation/design_doc_eval.md.j2")
            : GetDefaultDesignDocEvalPrompt();

        _transcriptEvalPrompt = configLoader.TemplateExists("evaluation/transcript_eval.md.j2")
            ? configLoader.LoadPromptRaw("evaluation/transcript_eval.md.j2")
            : GetDefaultTranscriptEvalPrompt();

        _agentEvalPrompt = configLoader.TemplateExists("evaluation/agent_eval.md.j2")
            ? configLoader.LoadPromptRaw("evaluation/agent_eval.md.j2")
            : GetDefaultAgentEvalPrompt();
    }

    /// <summary>
    /// Find paired design docs and transcripts in a directory.
    /// </summary>
    public List<(string Name, string DocPath, string? TranscriptPath)> FindExperimentFiles(string expDir)
    {
        var pairs = new List<(string, string, string?)>();

        foreach (var docPath in Directory.GetFiles(expDir, "*.md").OrderBy(f => f))
        {
            var name = Path.GetFileNameWithoutExtension(docPath);
            if (name == "index" || name.EndsWith("-transcript"))
                continue;

            var transcriptPath = Path.Combine(expDir, $"{name}-transcript.md");
            pairs.Add((name, docPath, File.Exists(transcriptPath) ? transcriptPath : null));
        }

        return pairs;
    }

    /// <summary>
    /// Evaluate a design document.
    /// </summary>
    public async Task<Dictionary<string, ScoreEntry>?> EvaluateDesignDocAsync(string docText, int timeout)
    {
        var defaults = _configLoader.Defaults();
        var truncated = docText.Length > defaults.Truncation.DocEvalInput
            ? docText.Substring(0, defaults.Truncation.DocEvalInput)
            : docText;

        var payload = $"## Design Document to Evaluate\n\n{truncated}";
        var response = await _claudeRunner.RunAsync(_evalSystemPrompt + "\n\n" + _designDocEvalPrompt, payload, timeout);
        return ParseScores(response);
    }

    /// <summary>
    /// Evaluate a transcript.
    /// </summary>
    public async Task<Dictionary<string, ScoreEntry>?> EvaluateTranscriptAsync(string transcriptText, int timeout)
    {
        var defaults = _configLoader.Defaults();
        var truncated = transcriptText.Length > defaults.Truncation.DocEvalInput
            ? transcriptText.Substring(0, defaults.Truncation.DocEvalInput)
            : transcriptText;

        var payload = $"## Transcript to Evaluate\n\n{truncated}";
        var response = await _claudeRunner.RunAsync(_evalSystemPrompt + "\n\n" + _transcriptEvalPrompt, payload, timeout);
        return ParseScores(response);
    }

    /// <summary>
    /// Evaluate a pair of design doc and transcript.
    /// </summary>
    public async Task<EvaluationResult> EvaluatePairAsync(string name, string docPath, string? transcriptPath, int timeout)
    {
        Console.WriteLine($"  Evaluating {name}...");

        var result = new EvaluationResult { Name = name };

        // Evaluate design doc
        var docText = await File.ReadAllTextAsync(docPath);
        result.DocScores = await EvaluateDesignDocAsync(docText, timeout);

        // Evaluate transcript if available
        if (transcriptPath != null)
        {
            var transcriptText = await File.ReadAllTextAsync(transcriptPath);
            result.TranscriptScores = await EvaluateTranscriptAsync(transcriptText, timeout);
        }

        return result;
    }

    /// <summary>
    /// Evaluate all files in an experiment directory.
    /// </summary>
    public async Task<(List<EvaluationResult> Evaluations, EvaluationSummary Summary)> EvaluateExperimentAsync(string expDir, int timeout)
    {
        var pairs = FindExperimentFiles(expDir);
        if (pairs.Count == 0)
        {
            Console.WriteLine($"  No design docs found in {expDir}");
            return (new List<EvaluationResult>(), new EvaluationSummary());
        }

        var evaluations = new List<EvaluationResult>();

        foreach (var (name, docPath, transcriptPath) in pairs)
        {
            var result = await EvaluatePairAsync(name, docPath, transcriptPath, timeout);
            evaluations.Add(result);
        }

        var summary = ComputeSummary(evaluations);
        return (evaluations, summary);
    }

    /// <summary>
    /// Compute aggregate scores across all evaluated pairs.
    /// </summary>
    public EvaluationSummary ComputeSummary(List<EvaluationResult> evaluations)
    {
        var docTotals = new Dictionary<string, double>();
        var docCounts = new Dictionary<string, int>();
        var transcriptTotals = new Dictionary<string, double>();
        var transcriptCounts = new Dictionary<string, int>();

        foreach (var ev in evaluations)
        {
            if (ev.DocScores != null)
            {
                foreach (var (dim, entry) in ev.DocScores)
                {
                    docTotals[dim] = docTotals.GetValueOrDefault(dim) + entry.Score;
                    docCounts[dim] = docCounts.GetValueOrDefault(dim) + 1;
                }
            }

            if (ev.TranscriptScores != null)
            {
                foreach (var (dim, entry) in ev.TranscriptScores)
                {
                    transcriptTotals[dim] = transcriptTotals.GetValueOrDefault(dim) + entry.Score;
                    transcriptCounts[dim] = transcriptCounts.GetValueOrDefault(dim) + 1;
                }
            }
        }

        var docAvgs = docTotals.ToDictionary(
            kv => kv.Key,
            kv => Math.Round(kv.Value / docCounts[kv.Key], 1));

        var transcriptAvgs = transcriptTotals.ToDictionary(
            kv => kv.Key,
            kv => Math.Round(kv.Value / transcriptCounts[kv.Key], 1));

        var allScores = docAvgs.Values.Concat(transcriptAvgs.Values).ToList();
        var overall = allScores.Count > 0 ? Math.Round(allScores.Average(), 1) : 0;

        return new EvaluationSummary
        {
            DocAverages = docAvgs,
            TranscriptAverages = transcriptAvgs,
            Overall = overall
        };
    }

    /// <summary>
    /// Format a human-readable evaluation report.
    /// </summary>
    public string FormatReport(string expName, List<EvaluationResult> evaluations, EvaluationSummary summary, double elapsed)
    {
        var sb = new StringBuilder();

        sb.AppendLine($"# Evaluation: {expName}");
        sb.AppendLine();
        sb.AppendLine($"*Evaluated: {DateTime.Now:yyyy-MM-dd HH:mm} | {elapsed:F0}s*");
        sb.AppendLine();
        sb.AppendLine($"## Overall Score: {summary.Overall}/10");
        sb.AppendLine();

        if (summary.DocAverages.Count > 0)
        {
            sb.AppendLine("### Design Doc Scores (averaged)");
            sb.AppendLine();
            sb.AppendLine("| Dimension | Avg Score |");
            sb.AppendLine("|-----------|-----------|");
            foreach (var (dim, score) in summary.DocAverages.OrderBy(kv => kv.Key))
            {
                var dimName = dim.Replace("_", " ");
                dimName = char.ToUpper(dimName[0]) + dimName.Substring(1);
                sb.AppendLine($"| {dimName} | {score}/10 |");
            }
            sb.AppendLine();
        }

        if (summary.TranscriptAverages.Count > 0)
        {
            sb.AppendLine("### Transcript Scores (averaged)");
            sb.AppendLine();
            sb.AppendLine("| Dimension | Avg Score |");
            sb.AppendLine("|-----------|-----------|");
            foreach (var (dim, score) in summary.TranscriptAverages.OrderBy(kv => kv.Key))
            {
                var dimName = dim.Replace("_", " ");
                dimName = char.ToUpper(dimName[0]) + dimName.Substring(1);
                sb.AppendLine($"| {dimName} | {score}/10 |");
            }
            sb.AppendLine();
        }

        sb.AppendLine("## Per-Question Detail");
        sb.AppendLine();

        foreach (var ev in evaluations)
        {
            sb.AppendLine($"### {ev.Name}");
            sb.AppendLine();

            if (ev.DocScores != null)
            {
                sb.AppendLine("**Design Doc:**");
                sb.AppendLine();
                foreach (var (dim, entry) in ev.DocScores)
                {
                    var dimName = dim.Replace("_", " ");
                    dimName = char.ToUpper(dimName[0]) + dimName.Substring(1);
                    var evidence = !string.IsNullOrEmpty(entry.Evidence) ? $" -- {entry.Evidence}" : "";
                    sb.AppendLine($"- **{dimName}**: {entry.Score}/10{evidence}");
                }
                sb.AppendLine();
            }

            if (ev.TranscriptScores != null)
            {
                sb.AppendLine("**Transcript:**");
                sb.AppendLine();
                foreach (var (dim, entry) in ev.TranscriptScores)
                {
                    var dimName = dim.Replace("_", " ");
                    dimName = char.ToUpper(dimName[0]) + dimName.Substring(1);
                    var evidence = !string.IsNullOrEmpty(entry.Evidence) ? $" -- {entry.Evidence}" : "";
                    sb.AppendLine($"- **{dimName}**: {entry.Score}/10{evidence}");
                }
                sb.AppendLine();
            }
        }

        return sb.ToString();
    }

    private static Dictionary<string, ScoreEntry>? ParseScores(string response)
    {
        // Strip markdown fences if present
        var cleaned = Regex.Replace(response, @"```json\s*", "");
        cleaned = Regex.Replace(cleaned, @"```\s*", "");
        cleaned = cleaned.Trim();

        try
        {
            var result = JsonSerializer.Deserialize<Dictionary<string, JsonElement>>(cleaned);
            if (result == null)
                return null;

            var scores = new Dictionary<string, ScoreEntry>();
            foreach (var (key, value) in result)
            {
                if (value.ValueKind == JsonValueKind.Object)
                {
                    var score = value.TryGetProperty("score", out var s)
                        ? s.GetDouble()
                        : 0;
                    var evidence = value.TryGetProperty("evidence", out var e)
                        ? e.GetString()
                        : null;
                    scores[key] = new ScoreEntry { Score = score, Evidence = evidence };
                }
                else if (value.ValueKind == JsonValueKind.Number)
                {
                    scores[key] = new ScoreEntry { Score = value.GetDouble() };
                }
            }
            return scores;
        }
        catch
        {
            // Try to find JSON object in the response
            var match = Regex.Match(cleaned, @"\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}", RegexOptions.Singleline);
            if (match.Success)
            {
                try
                {
                    return ParseScores(match.Value);
                }
                catch
                {
                    // Fall through
                }
            }
        }

        return null;
    }

    private static string GetDefaultEvalSystemPrompt() =>
        "You are an expert evaluator scoring the quality of design documents and discussion transcripts. " +
        "Output your scores as JSON with dimension names as keys and either a number (1-10) or " +
        "an object with 'score' and 'evidence' fields as values.";

    private static string GetDefaultDesignDocEvalPrompt() =>
        "Score this design document on these dimensions (1-10):\n" +
        "- clarity: How clear and understandable is the document?\n" +
        "- completeness: Does it cover all necessary aspects?\n" +
        "- actionability: Can someone implement from this spec?\n" +
        "- decision_quality: Are the decisions well-reasoned?\n\n" +
        "Output JSON with dimension names as keys.";

    private static string GetDefaultTranscriptEvalPrompt() =>
        "Score this discussion transcript on these dimensions (1-10):\n" +
        "- engagement: Did agents engage with each other's ideas?\n" +
        "- diversity: Were different perspectives represented?\n" +
        "- depth: Did the discussion go deep on important points?\n" +
        "- progression: Did the discussion build toward decisions?\n\n" +
        "Output JSON with dimension names as keys.";

    private static string GetDefaultAgentEvalPrompt() =>
        "Score this agent's performance on authenticity to their configured personality (1-10):\n" +
        "- voice_consistency: Does the agent maintain their configured tone?\n" +
        "- role_adherence: Does the agent stay in their assigned role?\n" +
        "- personality_traits: Do their responses reflect their personality config?\n\n" +
        "Output JSON with dimension names as keys.";
}
