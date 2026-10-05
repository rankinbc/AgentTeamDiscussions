// DiscussionEngine.cs — The Conversation Engine: orchestrates round structure and synthesis.
// Controls the propose->critique->evaluate pipeline for each question, then invokes the
// Moderator (synthesis) step to merge all responses into a single design doc.

using System.Text;
using System.Text.RegularExpressions;
using EngineStandalone.Abstractions;
using EngineStandalone.Agents;
using EngineStandalone.Brief;
using EngineStandalone.Config;
using EngineStandalone.Runner;

namespace EngineStandalone.Discussion;

/// <summary>
/// Result of running a question through the discussion engine.
/// </summary>
public class QuestionResult
{
    public string DesignDoc { get; set; } = "";
    public string Transcript { get; set; } = "";
    public Dictionary<string, Dictionary<string, string>> RoundResponses { get; set; } = new();
}

/// <summary>
/// Main discussion engine that orchestrates multi-round agent discussions.
/// </summary>
public class DiscussionEngine : IDiscussionEngine
{
    private readonly IClaudeRunner _claudeRunner;
    private readonly IPromptBuilder _promptBuilder;
    private readonly IConfigLoader _configLoader;
    private readonly IRoundRunner _roundRunner;
    private readonly string _synthesisTemplate;

    public DiscussionEngine(IClaudeRunner claudeRunner, IPromptBuilder promptBuilder, IConfigLoader configLoader, IRoundRunner roundRunner)
    {
        _claudeRunner = claudeRunner;
        _promptBuilder = promptBuilder;
        _configLoader = configLoader;
        _roundRunner = roundRunner;
        _synthesisTemplate = configLoader.LoadPromptRaw("prompts/synthesis.md.j2");
    }

    /// <summary>
    /// Fills the synthesis template's placeholders ({{ question_number }}, {{ topic_tag }},
    /// {{ max_ledger_words | default(50) }}). The template is loaded raw, so without this the
    /// model saw the Jinja syntax literally and never produced a usable ## Ledger section.
    /// The topic tag is the title cut to 60 chars, matching DecisionsLedger's ### Q{n}: header.
    /// </summary>
    public static string FillSynthesisTemplate(string template, int questionNumber, string questionTitle, int maxLedgerWords)
    {
        var topicTag = questionTitle.Length > 60 ? questionTitle[..60] : questionTitle;
        var filled = Regex.Replace(template, @"\{\{\s*question_number\s*\}\}", questionNumber.ToString());
        filled = Regex.Replace(filled, @"\{\{\s*topic_tag\s*\}\}", topicTag.Replace("$", "$$"));
        filled = Regex.Replace(filled, @"\{\{\s*max_ledger_words(\s*\|\s*default\(\s*\d+\s*\))?\s*\}\}", maxLedgerWords.ToString());
        return filled;
    }

    /// <summary>
    /// Compute speaking order for agents.
    /// </summary>
    public List<string> ComputeSpeakingOrder(List<string> agents, TeamConfig team)
    {
        return _roundRunner.ComputeSpeakingOrder(agents, team);
    }

    /// <summary>
    /// Run a round of discussion.
    /// </summary>
    public Task<Dictionary<string, string>> RunRoundAsync(
        List<string> agents,
        Dictionary<string, string> systemPrompts,
        TeamConfig team,
        Question question,
        string decisions,
        string priorRounds,
        string priorSpecs,
        string openQuestions,
        int timeout,
        string roundInstruction = "",
        Dictionary<string, string>? agentRoles = null,
        bool sequential = true,
        RoundCallbacks? callbacks = null,
        string roundName = "",
        int questionNumber = 0,
        string context = "")
    {
        return _roundRunner.RunRoundAsync(
            agents, systemPrompts, team, question, decisions, priorRounds,
            priorSpecs, openQuestions, timeout, roundInstruction, agentRoles,
            sequential, callbacks, roundName, questionNumber, context);
    }

    /// <summary>
    /// The Moderator step: a single LLM call that merges all round responses into one design doc.
    /// Prompt includes full discussion, prior decisions, prior design docs, and open questions.
    /// Output must start with '## Decisions'.
    /// </summary>
    public async Task<string> SynthesizeAsync(
        Question question,
        Dictionary<string, Dictionary<string, string>> roundResponses,
        List<string> roundLabels,
        string decisions,
        string priorSpecs,
        string openQuestions,
        int timeout,
        string context = "")
    {
        var displayNames = _configLoader.DisplayNames();
        var sb = new StringBuilder();

        sb.AppendLine($"# Design Question: {question.Title}");
        sb.AppendLine();
        sb.AppendLine("## The Question");
        sb.AppendLine();
        sb.AppendLine(question.Body);
        sb.AppendLine();

        if (!string.IsNullOrWhiteSpace(context))
        {
            sb.AppendLine("## Context (reference material from brief)");
            sb.AppendLine();
            sb.AppendLine(context);
            sb.AppendLine();
        }

        if (!string.IsNullOrEmpty(decisions))
        {
            sb.AppendLine("## Prior Decisions (from brief)");
            sb.AppendLine();
            sb.AppendLine(decisions);
            sb.AppendLine();
        }

        if (!string.IsNullOrEmpty(priorSpecs))
        {
            sb.AppendLine("## Prior Design Docs");
            sb.AppendLine();
            sb.AppendLine(priorSpecs);
            sb.AppendLine();
        }

        if (!string.IsNullOrEmpty(openQuestions))
        {
            sb.AppendLine("## Unresolved Open Questions from Prior Docs");
            sb.AppendLine();
            sb.AppendLine("Resolve any of these that this discussion addresses:");
            sb.AppendLine();
            sb.AppendLine(openQuestions);
            sb.AppendLine();
        }

        foreach (var roundName in roundLabels)
        {
            if (!roundResponses.TryGetValue(roundName, out var responses))
                continue;

            var label = roundName.ToUpper();
            if (label == "COUNTER")
                label = "COUNTER-PROPOSAL";

            sb.AppendLine($"## Round: {label}");
            sb.AppendLine();

            foreach (var (agentKey, response) in responses)
            {
                var name = displayNames.TryGetValue(agentKey, out var dn) ? dn : agentKey;
                sb.AppendLine($"### {name}");
                sb.AppendLine();
                sb.AppendLine(response);
                sb.AppendLine();
            }
        }

        sb.AppendLine("Synthesize into a single design doc. No code. Focus on behavior and rules.");
        sb.AppendLine();
        sb.AppendLine("IMPORTANT: Output ONLY the design doc. Start with '## Decisions'. " +
                      "Do not request file permissions, describe what you would write, or add any " +
                      "meta-commentary before or after the document.");

        var systemPrompt = FillSynthesisTemplate(
            _synthesisTemplate, question.Number, question.Title,
            _configLoader.Defaults().Synthesis.MaxLedgerWords);

        return await _claudeRunner.RunAsync(systemPrompt, sb.ToString(), timeout);
    }

    /// <summary>
    /// Archives the raw discussion as a readable transcript for debugging and evaluation.
    /// </summary>
    public string FormatTranscript(Question question, Dictionary<string, Dictionary<string, string>> roundResponses)
    {
        var displayNames = _configLoader.DisplayNames();
        var sb = new StringBuilder();

        sb.AppendLine($"# Transcript: {question.Title}");
        sb.AppendLine();
        sb.AppendLine($"*Generated: {DateTime.Now:yyyy-MM-dd HH:mm}*");
        sb.AppendLine();

        foreach (var (roundName, responses) in roundResponses)
        {
            var label = roundName == "counter" ? "COUNTER-PROPOSAL" : roundName.ToUpper();
            sb.AppendLine($"## Round: {label}");
            sb.AppendLine();

            foreach (var (agentKey, response) in responses)
            {
                var name = displayNames.TryGetValue(agentKey, out var dn) ? dn : agentKey;
                sb.AppendLine($"### {name}");
                sb.AppendLine();
                sb.AppendLine(response);
                sb.AppendLine();
            }
        }

        return sb.ToString();
    }

    /// <summary>
    /// Parses the "## Open Questions" section from a design doc. These chain forward:
    /// each subsequent question sees all accumulated open questions from prior docs,
    /// enabling decisions to build on each other across the session.
    /// </summary>
    public List<string> ExtractOpenQuestions(string designDoc)
    {
        var match = Regex.Match(designDoc, @"## Open Questions\s*\n(.*?)(?=\n## |\Z)", RegexOptions.Singleline);
        if (!match.Success)
            return new List<string>();

        var text = match.Groups[1].Value.Trim();
        var items = Regex.Matches(text, @"^[\s]*[-*\d.]+\s+(.+)", RegexOptions.Multiline);
        return items.Select(m => m.Groups[1].Value).ToList();
    }

    /// <summary>
    /// Orchestrates the full propose->critique->evaluate pipeline for one question.
    /// Each round accumulates discussion that feeds into the next, then synthesis
    /// merges everything into a design doc.
    /// </summary>
    public async Task<QuestionResult> RunQuestionAsync(
        Question question,
        TeamConfig team,
        Dictionary<string, string> systemPrompts,
        string decisions,
        string priorSpecs,
        string openQuestions,
        int timeout,
        TeamMode? mode = null)
    {
        if (mode == null)
        {
            // Fallback: use a simple propose-only structure with all agents
            mode = new TeamMode
            {
                Description = "fallback",
                Groups = new() { ["propose"] = systemPrompts.Keys.ToList() },
            };
        }

        var groups = mode.Groups;
        var roundLabels = groups.Keys.ToList();
        var agentRoles = mode.AgentRoles;

        var roundResponses = new Dictionary<string, Dictionary<string, string>>();
        var accumulatedDiscussion = "";
        var priorRoundSummaries = "";
        var displayNames = _configLoader.DisplayNames();
        var counterProposeInstruction = _configLoader.CounterProposeInstruction();

        foreach (var roundName in roundLabels)
        {
            if (!groups.TryGetValue(roundName, out var agents))
                continue;

            var agentNames = string.Join(", ", agents.Select(a => displayNames.TryGetValue(a, out var n) ? n : a));
            var displayName = roundName == "counter" ? "counter-propose" : roundName;

            // Show role overlays if any
            var roleInfo = "";
            foreach (var a in agents)
            {
                if (agentRoles.TryGetValue(a, out var roleKey))
                    roleInfo += $" [{a}: {roleKey}]";
            }
            Console.WriteLine($"  [{question.Number}] Round {displayName}: {agentNames}{roleInfo}");

            var roundInst = roundName switch
            {
                "counter" => counterProposeInstruction,
                "critique" => "You have read the proposals above. Your job is to BREAK them. " +
                    "Do not fix surface issues -- challenge the core design. What will fail first? " +
                    "What assumption is wrong? If both proposals agree on something, that's the most " +
                    "dangerous assumption -- examine it hardest. Be specific about failure scenarios.",
                "evaluate" => "You have read the proposals and critiques above. Do not merge or compromise. " +
                    "Pick the stronger approach and explain why the other one loses. If the critique " +
                    "destroyed a proposal, say so. If both survived, pick the one with fewer unresolved " +
                    "risks and commit. State your verdict clearly.",
                _ => ""
            };

            var startTime = DateTime.UtcNow;
            var responses = await RunRoundAsync(
                agents: agents,
                systemPrompts: systemPrompts,
                team: team,
                question: question,
                decisions: decisions,
                priorRounds: priorRoundSummaries,
                priorSpecs: priorSpecs,
                openQuestions: openQuestions,
                timeout: timeout,
                roundInstruction: roundInst,
                agentRoles: agentRoles,
                roundName: roundName,
                questionNumber: question.Number);

            var elapsed = (DateTime.UtcNow - startTime).TotalSeconds;

            roundResponses[roundName] = responses;

            // Check for timeouts
            foreach (var (key, resp) in responses)
            {
                if (resp.Contains("[Claude CLI timed out") || resp.Contains("[Error"))
                {
                    Console.WriteLine($"    WARNING: {key}: {resp.Substring(0, Math.Min(80, resp.Length))}");
                }
            }

            // Accumulate full discussion (for synthesis) and compressed summaries (for next round)
            foreach (var (key, resp) in responses)
            {
                var name = displayNames.TryGetValue(key, out var dn) ? dn : key;
                var label = roundName == "counter" ? "COUNTER-PROPOSAL" : roundName.ToUpper();
                accumulatedDiscussion += $"[{label} - {name}]\n{resp}\n\n";
            }
            priorRoundSummaries = DiscussionCompressor.CompressToSummaries(accumulatedDiscussion);

            Console.WriteLine($"    Done in {elapsed:F0}s");
        }

        // Synthesis
        Console.WriteLine($"  [{question.Number}] Synthesizing design doc...");
        var synthStartTime = DateTime.UtcNow;

        var designDoc = await SynthesizeAsync(
            question, roundResponses, roundLabels, decisions,
            priorSpecs, openQuestions, timeout);

        var synthElapsed = (DateTime.UtcNow - synthStartTime).TotalSeconds;
        Console.WriteLine($"    Synthesis done in {synthElapsed:F0}s");

        var transcript = FormatTranscript(question, roundResponses);

        return new QuestionResult
        {
            DesignDoc = designDoc,
            Transcript = transcript,
            RoundResponses = roundResponses
        };
    }
}
