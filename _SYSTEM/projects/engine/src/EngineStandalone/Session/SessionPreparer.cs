// Interactive session preparation — builds a SessionConfig through CLI prompts.
// The user provides what to discuss, picks a team, and picks a mode.
// The result is a session.json that the runner consumes.

using EngineStandalone.Abstractions;
using EngineStandalone.Agents;
using EngineStandalone.Config;

namespace EngineStandalone.Session;

/// <summary>
/// Builds a SessionConfig interactively via CLI prompts.
/// </summary>
public class SessionPreparer
{
    private readonly IAgentLoader _agentLoader;
    private readonly IConfigLoader _configLoader;

    public SessionPreparer(IAgentLoader agentLoader, IConfigLoader configLoader)
    {
        _agentLoader = agentLoader;
        _configLoader = configLoader;
    }

    /// <summary>
    /// Run the full interactive preparation flow. Returns a ready SessionConfig.
    /// </summary>
    public SessionConfig Prepare()
    {
        var config = new SessionConfig { Source = "interactive" };

        Console.WriteLine();
        Console.WriteLine("═══════════════════════════════════════════════");
        Console.WriteLine("  New Session");
        Console.WriteLine("═══════════════════════════════════════════════");
        Console.WriteLine();

        // Step 1: What to discuss
        config.Questions = AskQuestions();
        config.Title = config.Questions.Count == 1
            ? config.Questions[0].Title
            : $"{config.Questions.Count}-question session";

        // Step 2: What's already decided
        config.Decided = AskDecisions();

        // Step 3: Pick a team
        config.Team = AskTeam();

        // Step 4: Load team, select agents
        var team = _agentLoader.LoadTeamByName(config.Team);
        config.Agents = AskAgents(team);

        // Step 5: Pick a mode (from the chosen team's available modes)
        config.Mode = AskMode(team);

        // Step 6: Timeout (optional)
        config.Timeout = AskTimeout();

        // Hash for resume integrity
        config.QuestionHash = SessionPersistence.HashQuestionList(
            config.Questions.Select(q => (q.Number, q.Title)));

        var agentSummary = config.Agents != null
            ? $"{config.Agents.Count}/{team.Agents.Count} agents"
            : $"all {team.Agents.Count} agents";

        Console.WriteLine();
        Console.WriteLine("───────────────────────────────────────────────");
        Console.WriteLine($"  Topic:     {config.Title}");
        Console.WriteLine($"  Questions: {config.Questions.Count}");
        Console.WriteLine($"  Team:      {config.Team} ({agentSummary})");
        Console.WriteLine($"  Mode:      {config.Mode}");
        Console.WriteLine($"  Timeout:   {config.Timeout}s");
        Console.WriteLine("───────────────────────────────────────────────");
        Console.WriteLine();

        return config;
    }

    /// <summary>
    /// Build a SessionConfig from CLI arguments (non-interactive).
    /// Topic is split into questions if it contains numbered items.
    /// </summary>
    public SessionConfig PrepareFromArgs(
        string topic,
        string? team = null,
        string? mode = null,
        int timeout = 120,
        List<string>? agents = null)
    {
        var teamName = team ?? "beta-agents";

        // A pasted/selected brief (has "## Open Questions") keeps its decisions and context;
        // anything else is treated as a free-form topic.
        if (Brief.BriefParser.LooksLikeBrief(topic))
        {
            var briefConfig = BuildFromBriefText(topic, "api", teamName,
                mode ?? _agentLoader.LoadTeamByName(teamName).DefaultMode, timeout);
            briefConfig.Agents = agents;
            return briefConfig;
        }

        var questions = ParseTopicIntoQuestions(topic);

        // If no mode specified, use team's default
        if (mode == null)
        {
            var loadedTeam = _agentLoader.LoadTeamByName(teamName);
            mode = loadedTeam.DefaultMode;
        }

        var config = new SessionConfig
        {
            Source = "cli-args",
            Title = questions.Count == 1
                ? questions[0].Title
                : $"{questions.Count}-question session",
            Questions = questions,
            Team = teamName,
            Agents = agents,
            Mode = mode,
            Timeout = timeout,
        };

        config.QuestionHash = SessionPersistence.HashQuestionList(
            config.Questions.Select(q => (q.Number, q.Title)));

        return config;
    }

    /// <summary>
    /// Build a SessionConfig from a legacy markdown brief file.
    /// </summary>
    public SessionConfig PrepareFromBrief(string briefPath, string? team = null, string? mode = null, int timeout = 120)
    {
        // An explicit team uses its own default mode; otherwise keep the historical compete default
        var resolvedMode = mode ?? (team != null ? _agentLoader.LoadTeamByName(team).DefaultMode : "compete");
        var config = BuildFromBriefText(File.ReadAllText(briefPath), briefPath, team ?? "beta-agents", resolvedMode, timeout);
        config.Title = Path.GetFileNameWithoutExtension(briefPath);
        return config;
    }

    /// <summary>
    /// Build a SessionConfig from brief markdown text (decisions, context, questions).
    /// Title comes from the H1 heading when present, else the first question.
    /// </summary>
    private static SessionConfig BuildFromBriefText(string text, string source, string team, string mode, int timeout)
    {
        var parser = new Brief.BriefParser();
        var (decisions, questions) = parser.ParseBriefText(text);
        var h1 = System.Text.RegularExpressions.Regex.Match(text, @"^#\s+(.+)$", System.Text.RegularExpressions.RegexOptions.Multiline);

        var config = new SessionConfig
        {
            Source = source,
            Title = h1.Success ? h1.Groups[1].Value.Trim() : questions[0].Title,
            Context = Brief.BriefParser.ExtractContext(text),
            Decided = decisions.Split('\n', StringSplitOptions.RemoveEmptyEntries)
                .Select(d => d.TrimStart('-', '*', ' ').Trim())
                .Where(d => !string.IsNullOrWhiteSpace(d))
                .ToList(),
            Questions = questions.Select(q => new SessionQuestion
            {
                Number = q.Number,
                Title = q.Title,
                Body = q.Body,
            }).ToList(),
            Team = team,
            Mode = mode,
            Timeout = timeout,
        };

        config.QuestionHash = SessionPersistence.HashQuestionList(
            config.Questions.Select(q => (q.Number, q.Title)));

        return config;
    }

    // --- Interactive steps ---

    private List<SessionQuestion> AskQuestions()
    {
        Console.WriteLine("What should the agents discuss?");
        Console.WriteLine("(Paste your topic or questions. Enter a blank line when done.)");
        Console.WriteLine();

        var lines = new List<string>();
        while (true)
        {
            var line = Console.ReadLine();
            if (line == null || (string.IsNullOrWhiteSpace(line) && lines.Count > 0))
                break;
            lines.Add(line);
        }

        var text = string.Join("\n", lines).Trim();
        if (string.IsNullOrWhiteSpace(text))
        {
            Console.WriteLine("  No input provided. Exiting.");
            Environment.Exit(1);
        }

        return ParseTopicIntoQuestions(text);
    }

    private List<string> AskDecisions()
    {
        Console.WriteLine();
        Console.WriteLine("What's already decided? (one per line, blank line to skip)");
        Console.WriteLine();

        var decisions = new List<string>();
        while (true)
        {
            Console.Write("  > ");
            var line = Console.ReadLine();
            if (string.IsNullOrWhiteSpace(line))
                break;
            decisions.Add(line.TrimStart('-', '*', ' ').Trim());
        }

        return decisions;
    }

    private string AskTeam()
    {
        var teams = _agentLoader.ListTeams();
        if (teams.Count == 0)
        {
            Console.WriteLine("  No teams found. Using default: beta-agents");
            return "beta-agents";
        }

        Console.WriteLine();
        Console.WriteLine("Available teams:");
        for (var i = 0; i < teams.Count; i++)
        {
            var (name, file, count) = teams[i];
            Console.WriteLine($"  {i + 1}. {name} ({count} agents)");
        }
        Console.WriteLine();
        Console.Write($"Pick a team [1]: ");

        var input = Console.ReadLine()?.Trim();
        if (string.IsNullOrWhiteSpace(input) || input == "1")
            return Path.GetFileNameWithoutExtension(teams[0].File);

        if (int.TryParse(input, out var idx) && idx >= 1 && idx <= teams.Count)
            return Path.GetFileNameWithoutExtension(teams[idx - 1].File);

        // Try matching by name
        var match = teams.FirstOrDefault(t =>
            t.Name.Contains(input, StringComparison.OrdinalIgnoreCase));
        if (match != default)
            return Path.GetFileNameWithoutExtension(match.File);

        Console.WriteLine($"  Unknown team '{input}'. Using default: beta-agents");
        return "beta-agents";
    }

    private static List<string>? AskAgents(TeamConfig team)
    {
        var agentKeys = team.Agents.Keys.OrderBy(k => k).ToList();

        if (agentKeys.Count <= 2)
            return null; // Not worth filtering tiny teams

        Console.WriteLine();
        Console.WriteLine($"Team has {agentKeys.Count} agents. Use all or select specific ones?");
        Console.WriteLine();

        for (var i = 0; i < agentKeys.Count; i++)
        {
            var key = agentKeys[i];
            var agent = team.Agents[key];
            var role = agent.Position?.Role ?? "";
            Console.WriteLine($"  {i + 1}. {agent.Name} — {role}");
        }

        Console.WriteLine();
        Console.Write("Enter agent numbers (e.g. 1,3,5) or 'all' [all]: ");

        var input = Console.ReadLine()?.Trim();
        if (string.IsNullOrWhiteSpace(input) || input.Equals("all", StringComparison.OrdinalIgnoreCase))
            return null; // null = use all

        var selected = new List<string>();
        foreach (var part in input.Split(',', ' ', StringSplitOptions.RemoveEmptyEntries))
        {
            var trimmed = part.Trim();

            // Try as number
            if (int.TryParse(trimmed, out var idx) && idx >= 1 && idx <= agentKeys.Count)
            {
                var key = agentKeys[idx - 1];
                if (!selected.Contains(key))
                    selected.Add(key);
                continue;
            }

            // Try as agent key name
            if (team.Agents.ContainsKey(trimmed) && !selected.Contains(trimmed))
            {
                selected.Add(trimmed);
                continue;
            }

            // Try fuzzy match on name
            var match = team.Agents.FirstOrDefault(a =>
                a.Value.Name.Contains(trimmed, StringComparison.OrdinalIgnoreCase));
            if (match.Key != null && !selected.Contains(match.Key))
            {
                selected.Add(match.Key);
            }
        }

        if (selected.Count == 0)
        {
            Console.WriteLine("  No valid agents selected. Using all.");
            return null;
        }

        Console.WriteLine($"  Selected: {string.Join(", ", selected.Select(k => team.Agents[k].Name))}");
        return selected;
    }

    private static string AskMode(TeamConfig team)
    {
        if (team.Modes.Count == 0)
        {
            Console.WriteLine("  No modes defined for this team. Using default.");
            return "default";
        }

        if (team.Modes.Count == 1)
        {
            var only = team.Modes.Keys.First();
            Console.WriteLine($"\n  Mode: {only} (only option for this team)");
            return only;
        }

        var modeNames = team.Modes.Keys.OrderBy(k => k).ToList();

        Console.WriteLine();
        Console.WriteLine("Available modes:");
        for (var i = 0; i < modeNames.Count; i++)
        {
            var name = modeNames[i];
            var desc = team.Modes[name].Description;
            var marker = name == team.DefaultMode ? " (default)" : "";
            Console.WriteLine($"  {i + 1}. {name}{marker} — {desc}");
        }
        Console.WriteLine();
        Console.Write($"Pick a mode [{team.DefaultMode}]: ");

        var input = Console.ReadLine()?.Trim();
        if (string.IsNullOrWhiteSpace(input))
            return team.DefaultMode;

        if (int.TryParse(input, out var idx) && idx >= 1 && idx <= modeNames.Count)
            return modeNames[idx - 1];

        if (team.Modes.ContainsKey(input))
            return input;

        Console.WriteLine($"  Unknown mode '{input}'. Using default: {team.DefaultMode}");
        return team.DefaultMode;
    }

    private int AskTimeout()
    {
        Console.WriteLine();
        Console.Write("Timeout per LLM call in seconds [120]: ");
        var input = Console.ReadLine()?.Trim();

        if (string.IsNullOrWhiteSpace(input))
            return 120;

        if (int.TryParse(input, out var timeout) && timeout > 0)
            return timeout;

        return 120;
    }

    // --- Helpers ---

    /// <summary>
    /// Parse free-form text into questions.
    /// If the text contains numbered items (1. ..., 2. ...), splits into multiple questions.
    /// Otherwise, treats the whole text as a single question.
    /// </summary>
    public static List<SessionQuestion> ParseTopicIntoQuestions(string text)
    {
        // Try to detect numbered list pattern
        var numbered = System.Text.RegularExpressions.Regex.Matches(
            text,
            @"^(\d+)[.)]\s+(.+?)(?=^\d+[.)]\s+|\Z)",
            System.Text.RegularExpressions.RegexOptions.Multiline | System.Text.RegularExpressions.RegexOptions.Singleline);

        if (numbered.Count > 0)
        {
            return numbered.Select(m =>
            {
                var body = m.Groups[2].Value.Trim();
                // Extract title: first sentence or first line
                var title = ExtractTitle(body);
                return new SessionQuestion
                {
                    Number = int.Parse(m.Groups[1].Value),
                    Title = title,
                    Body = body,
                };
            }).ToList();
        }

        // Single question — use first line or first sentence as title
        var title = ExtractTitle(text);
        return new List<SessionQuestion>
        {
            new() { Number = 1, Title = title, Body = text }
        };
    }

    /// <summary>
    /// Extract a short title from a question body.
    /// Uses bold markdown (**title**), first sentence, or first line — whichever is shortest.
    /// </summary>
    public static string ExtractTitle(string body)
    {
        // Check for **bold title** pattern
        var boldMatch = System.Text.RegularExpressions.Regex.Match(body, @"\*\*(.+?)\*\*");
        if (boldMatch.Success)
            return boldMatch.Groups[1].Value.Trim();

        // First line
        var firstLine = body.Split('\n', 2)[0].Trim();

        // First sentence
        var sentenceEnd = firstLine.IndexOfAny(new[] { '.', '?', '!' });
        if (sentenceEnd > 0 && sentenceEnd < 120)
            return firstLine[..(sentenceEnd + 1)].Trim();

        // Truncate first line if too long
        if (firstLine.Length > 80)
            return firstLine[..77] + "...";

        return firstLine;
    }
}
