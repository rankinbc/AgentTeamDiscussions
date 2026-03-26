// Parses a markdown discussion brief (the user's input) into structured data.
// Brief format: product description + "What's Already Decided" (constraints every agent sees)
// + numbered "Open Questions" (e.g. `1. **Feature Ranking**`).
// Slugify converts question titles to filesystem-safe names for output files.

using System.Text.RegularExpressions;

namespace EngineStandalone.Brief;

/// <summary>
/// Represents a parsed question from a discussion brief.
/// </summary>
public class Question
{
    public int Number { get; set; }
    public string Title { get; set; } = "";
    public string Body { get; set; } = "";
}

/// <summary>
/// Represents a structured discussion brief.
/// </summary>
public class ParsedBrief
{
    public string ProductDescription { get; set; } = "";
    public List<string> Constraints { get; set; } = new();
    public List<Question> Questions { get; set; } = new();
}

/// <summary>
/// Exception thrown when brief parsing fails.
/// </summary>
public class BriefParseException : Exception
{
    public BriefParseException(string message) : base(message) { }
}

/// <summary>
/// Parses discussion brief markdown files.
/// </summary>
public class BriefParser
{
    /// <summary>
    /// Parse a discussion brief. Returns (decisions_text, questions_list).
    /// </summary>
    public (string Decisions, List<Question> Questions) ParseBrief(string path)
    {
        var text = File.ReadAllText(path);

        // "What's Already Decided" becomes the decisions context that every agent sees.
        var decisionsMatch = Regex.Match(text, @"## What's Already Decided\s*\n(.*?)(?=\n## |\Z)", RegexOptions.Singleline);
        var decisions = decisionsMatch.Success ? decisionsMatch.Groups[1].Value.Trim() : "";

        // Extract "Open Questions" section
        var questionsMatch = Regex.Match(text, @"## Open Questions[^\n]*\n(.*?)(?=\n## |\Z)", RegexOptions.Singleline);
        if (!questionsMatch.Success)
        {
            throw new BriefParseException("No 'Open Questions' section found in brief.");
        }

        var questionsText = questionsMatch.Groups[1].Value.Trim();

        // Parse numbered questions: expects `N. **Title** body...` format.
        var pattern = new Regex(@"^(\d+)\.\s+\*\*(.+?)\*\*\s*(.*?)(?=^\d+\.\s+\*\*|\Z)", RegexOptions.Multiline | RegexOptions.Singleline);
        var matches = pattern.Matches(questionsText);

        var questions = matches.Select(m => new Question
        {
            Number = int.Parse(m.Groups[1].Value),
            Title = m.Groups[2].Value.Trim(),
            Body = m.Groups[3].Value.Trim()
        }).ToList();

        if (questions.Count == 0)
        {
            throw new BriefParseException("No questions parsed from brief.");
        }

        return (decisions, questions);
    }

    /// <summary>
    /// Parse a discussion brief into a structured Brief object.
    /// </summary>
    public ParsedBrief ParseBriefStructured(string path)
    {
        var text = File.ReadAllText(path);
        var brief = new ParsedBrief();

        // Product description: H1 title + any text before the first ## heading
        var preSectionMatch = Regex.Split(text, @"^##\s+", RegexOptions.Multiline);
        var preSection = preSectionMatch[0];
        brief.ProductDescription = Regex.Replace(preSection, @"^#\s+", "", RegexOptions.Multiline).Trim();

        // Constraints: bullet items from "What's Already Decided"
        var decidedMatch = Regex.Match(text, @"## What's Already Decided\s*\n(.*?)(?=\n## |\Z)", RegexOptions.Singleline);
        if (decidedMatch.Success)
        {
            foreach (var line in decidedMatch.Groups[1].Value.Split('\n'))
            {
                var stripped = line.Trim();
                if (stripped.StartsWith("- ") || stripped.StartsWith("* "))
                {
                    brief.Constraints.Add(stripped.Substring(2).Trim());
                }
                else if (stripped.StartsWith("-") && stripped.Length > 1)
                {
                    brief.Constraints.Add(stripped.Substring(1).Trim());
                }
            }
        }

        // Questions: numbered items from "Open Questions"
        var questionsMatch = Regex.Match(text, @"## Open Questions[^\n]*\n(.*?)(?=\n## |\Z)", RegexOptions.Singleline);
        if (!questionsMatch.Success)
        {
            throw new BriefParseException("No 'Open Questions' section found in brief.");
        }

        var questionsText = questionsMatch.Groups[1].Value.Trim();
        var pattern = new Regex(@"^(\d+)\.\s+\*\*(.+?)\*\*\s*(.*?)(?=^\d+\.\s+\*\*|\Z)", RegexOptions.Multiline | RegexOptions.Singleline);
        var matches = pattern.Matches(questionsText);

        brief.Questions = matches.Select(m => new Question
        {
            Number = int.Parse(m.Groups[1].Value),
            Title = m.Groups[2].Value.Trim(),
            Body = m.Groups[3].Value.Trim()
        }).ToList();

        if (brief.Questions.Count == 0)
        {
            throw new BriefParseException("No questions parsed from brief.");
        }

        return brief;
    }

    /// <summary>
    /// Convert a title to a URL/filename-safe slug (lowercase, alphanumeric + hyphens).
    /// </summary>
    public static string Slugify(string title, int maxLength = 60)
    {
        var slug = Regex.Replace(title.ToLower(), @"[^a-z0-9]+", "-").Trim('-');
        if (slug.Length > maxLength)
        {
            slug = slug.Substring(0, maxLength).TrimEnd('-');
        }
        return string.IsNullOrEmpty(slug) ? "untitled" : slug;
    }
}
