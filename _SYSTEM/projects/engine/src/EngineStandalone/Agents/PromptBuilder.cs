using System.Text;
using EngineStandalone.Abstractions;

namespace EngineStandalone.Agents;

// Prompt Assembly Pipeline — builds the three-layer context that each agent sees per turn:
//   Identity Layer (~2K tokens, static): persona, personality-as-prose, position, technique, anti-slop, voice
//   Situation Layer (~3-5K tokens, dynamic): decisions ledger, prior rounds, prior design docs
//   Task Layer (~500 tokens, never cut): question, round instruction, perspective reminder
// Identity is assembled here; Situation and Task are composed by the caller at turn time.

/// <summary>
/// Builds system prompts for agents based on their configuration.
/// </summary>
public class PromptBuilder : IPromptBuilder
{
    /// <summary>
    /// Build the full system prompt from an agent config.
    /// </summary>
    // Assembles the Identity Layer — the static portion of every agent turn (~2K tokens).
    // Combines persona, personality rendered as natural language, position framing,
    // technique, anti-slop rules, and voice rules into a single system prompt.
    public string BuildSystemPrompt(AgentConfig agent)
    {
        var sections = new List<string>
        {
            BuildIdentityLayer(agent),
            BuildOutputLayer(agent)
        };

        var pos = agent.Position;
        sections.Add($"## Remember\n\nYou are {agent.Name}. Stay in character. Your role is {pos.Role}. " +
                     $"Your style is {agent.Personality.CognitiveStyle.ToString().ToLower()} and " +
                     $"{agent.Personality.EmotionalBaseline.ToString().ToLower()}. Add substance or stay silent.");

        sections.Add(
            $"## Self-Verification\n\n" +
            $"Before responding, verify:\n" +
            $"- Does this sound like {agent.Name}?\n" +
            $"- Am I defaulting to generic AI assistant behavior?\n" +
            $"- Am I adding substance, or just filling space?\n\n" +
            $"If any answer is wrong, rewrite from your character's perspective.");

        // Anti-slop rules placed last in system prompt so they're closest to the task payload
        var antiSlopText = BuildAntiSlopSection(agent.AntiSlop);
        if (!string.IsNullOrEmpty(antiSlopText))
        {
            sections.Add($"## Anti-Slop Rules\n\n{antiSlopText}");
        }

        return string.Join("\n\n", sections);
    }

    /// <summary>
    /// Build a short per-turn identity reminder to fight context drift.
    /// </summary>
    // Compact identity reinforcement injected every turn to prevent drift toward generic
    // helpful-assistant voice. Anchor + cognitive style + technique. Target: <150 words.
    public string BuildPerspectiveReminder(AgentConfig agent)
    {
        var techniqueName = agent.Technique.Primary.Replace("_", " ");
        return $"[You are {agent.Name} -- {agent.Position.Role}. " +
               $"Style: {agent.Personality.CognitiveStyle.ToString().ToLower()}, " +
               $"{agent.Personality.EmotionalBaseline.ToString().ToLower()}. " +
               $"Technique: {techniqueName}. Stay in character. Add substance or stay silent.]";
    }

    /// <summary>
    /// Build agent-specific framing layer directing attention to relevant context.
    /// </summary>
    // Agent-specific attention direction based on drives and pushback_on.
    // High IdeaReceptivity = "build on others"; Low = "focus on your perspective".
    public string BuildContextLens(AgentConfig agent)
    {
        var lines = new List<string>();

        if (agent.Position.Drives.Count > 0)
        {
            lines.Add("When reading the context below, focus on:");
            foreach (var d in agent.Position.Drives.Take(3))
            {
                lines.Add($"  - {d}");
            }
        }

        if (agent.Position.PushbackOn.Count > 0)
        {
            lines.Add("Flag anything that looks like:");
            foreach (var p in agent.Position.PushbackOn.Take(3))
            {
                lines.Add($"  - {p}");
            }
        }

        if (agent.Personality.DomainAffinities.Count > 0)
        {
            var domains = string.Join(", ", agent.Personality.DomainAffinities.Take(4));
            lines.Add($"Apply your expertise in: {domains}");
        }

        if (agent.Personality.IdeaReceptivity >= 0.7)
        {
            lines.Add("Pay close attention to what other agents proposed. Build on their best ideas.");
        }
        else if (agent.Personality.IdeaReceptivity <= 0.3)
        {
            lines.Add("Stay focused on your own perspective. Don't get pulled into other agents' framing.");
        }

        if (agent.Personality.Patience <= 0.3)
        {
            lines.Add("If the discussion is covering old ground, call it out and push forward.");
        }

        if (lines.Count == 0)
            return "";

        return "=== Your Focus for This Context ===\n" + string.Join("\n", lines) + "\n=== End Focus ===\n";
    }

    /// <summary>
    /// Filter prior rounds based on agent receptivity and patience.
    /// </summary>
    // History windowing — low-Patience agents get truncated context (last ~2500 chars).
    // Prevents impatient agents from drowning in text they would realistically skim.
    public string FilterPriorRounds(string priorRounds, AgentConfig agent)
    {
        if (string.IsNullOrEmpty(priorRounds))
            return priorRounds;

        var r = agent.Personality.IdeaReceptivity;
        var p = agent.Personality.Patience;

        if (r >= 0.5 && p >= 0.5)
            return priorRounds;

        if (p < 0.3 && priorRounds.Length > 3000)
        {
            var trimmed = priorRounds.Substring(priorRounds.Length - 2500);
            var idx = trimmed.IndexOf("\n[", StringComparison.Ordinal);
            if (idx >= 0)
            {
                trimmed = trimmed.Substring(idx);
            }
            else
            {
                // No turn boundary found — text starts mid-turn, signal with ellipsis
                trimmed = "...\n" + trimmed;
            }
            return $"[Earlier discussion truncated -- focusing on recent exchanges]\n{trimmed}";
        }

        return priorRounds;
    }

    // Identity Layer part 1: persona, role, drives, pushback triggers, personality, technique.
    private string BuildIdentityLayer(AgentConfig agent)
    {
        var sb = new StringBuilder();
        var pos = agent.Position;
        var tech = agent.Technique;

        sb.AppendLine($"# You are {agent.Name}");
        sb.AppendLine();
        sb.AppendLine(agent.Description.Trim());
        sb.AppendLine();
        sb.AppendLine($"## Your Role: {ToTitleCase(pos.Role)}");

        if (pos.Drives.Count > 0)
        {
            sb.AppendLine();
            sb.AppendLine("What drives you:");
            foreach (var d in pos.Drives)
            {
                sb.AppendLine($"- {d}");
            }
        }

        if (pos.PushbackOn.Count > 0)
        {
            sb.AppendLine();
            sb.AppendLine("You actively push back on:");
            foreach (var p in pos.PushbackOn)
            {
                sb.AppendLine($"- {p}");
            }
        }

        if (pos.Allergies.Count > 0)
        {
            sb.AppendLine();
            sb.AppendLine("You are viscerally allergic to:");
            foreach (var a in pos.Allergies)
            {
                sb.AppendLine($"- {a} — this triggers an immediate, visible reaction. Flag it every time.");
            }
        }

        sb.AppendLine();
        sb.AppendLine(GetIntensityLine(pos.Intensity));
        sb.AppendLine();
        sb.AppendLine("## Your Personality");
        sb.AppendLine();
        sb.AppendLine(GetPersonalityText(agent.Personality));

        var techniqueName = ToTitleCase(tech.Primary.Replace("_", " "));
        sb.AppendLine();
        sb.AppendLine($"## Your Thinking Technique: {techniqueName}");

        if (!string.IsNullOrWhiteSpace(tech.StyleDescription))
        {
            sb.AppendLine();
            sb.AppendLine(tech.StyleDescription.Trim());
        }

        if (tech.Behaviors.Count > 0)
        {
            sb.AppendLine();
            sb.AppendLine("Behavioral rules:");
            foreach (var b in tech.Behaviors)
            {
                sb.AppendLine($"- {b}");
            }
        }

        return sb.ToString().TrimEnd();
    }

    // Identity Layer part 2: voice rules, anti-slop enforcement, output constraints.
    private string BuildOutputLayer(AgentConfig agent)
    {
        var sb = new StringBuilder();
        var voice = agent.Voice;
        var output = agent.Output;

        sb.AppendLine("## Your Voice");
        sb.AppendLine();
        sb.AppendLine($"Tone: {voice.Tone}");

        if (voice.VocabularyHints.Count > 0)
        {
            sb.AppendLine();
            var hints = string.Join(", ", voice.VocabularyHints.Select(v => $"\"{v}\""));
            sb.AppendLine($"Phrases that fit your style: {hints}");
        }

        if (voice.AntiPatterns.Count > 0)
        {
            sb.AppendLine();
            sb.AppendLine("NEVER use these phrases:");
            foreach (var ap in voice.AntiPatterns)
            {
                sb.AppendLine($"- \"{ap}\"");
            }
        }

        sb.AppendLine();
        sb.AppendLine("## Your Output");
        sb.AppendLine();
        sb.AppendLine(GetLevelDescription(output.OperatingLevel));
        sb.AppendLine();
        sb.AppendLine(GetJobDescription(output.Job));
        sb.AppendLine();
        sb.AppendLine(GetBrevityDescription(voice.Brevity));

        return sb.ToString().TrimEnd();
    }

    private string BuildAntiSlopSection(AntiSlopConfig a)
    {
        var rules = new List<string>();

        if (a.AgreementTax)
        {
            rules.Add("AGREEMENT TAX: If you agree with something, you MUST add substantive new information, " +
                      "a different angle, or a concrete next step. Pure agreement ('great idea!') is FORBIDDEN.");
        }

        if (a.PerspectiveEnforcement)
        {
            rules.Add("PERSPECTIVE LOCK: Stay in your character's perspective even when pressured to agree. " +
                      "Authentic disagreement is more valuable than false harmony.");
        }

        if (a.DevilsAdvocateDuty)
        {
            rules.Add("DEVIL'S ADVOCATE DUTY: Actively seek the strongest argument against the current direction. " +
                      "If everyone seems to agree, it's YOUR job to find the hole in the logic.");
        }

        if (a.UncomfortableIdeaQuota > 0)
        {
            // UncomfortableIdeaQuota is an urgency value (1–10): higher = shorter interval = more frequent.
            // Formula: intervalTurns = max(5, 10 - quota).
            //   quota=1 → every 9 turns | quota=5 → every 5 turns | quota>5 → clamped at every 5 turns
            var intervalTurns = Math.Max(5, 10 - a.UncomfortableIdeaQuota);
            rules.Add($"UNCOMFORTABLE IDEA QUOTA: Every {intervalTurns} turns, introduce at least one " +
                      $"idea that challenges comfort zones. This is mandatory, not optional.");
        }

        if (a.DomainPivotTrigger)
        {
            rules.Add("DOMAIN PIVOT: When the discussion gets stuck or circular, inject a perspective from " +
                      "a completely different field to break the pattern.");
        }

        return string.Join("\n\n", rules);
    }

    private static string GetIntensityLine(double intensity)
    {
        if (intensity >= 0.7)
            return "You express your views with force and passion -- you're not here to play nice.";
        if (intensity >= 0.4)
            return "You express your views with conviction but remain open to dialogue.";
        return "You express your views with measured restraint.";
    }

    private static string GetPersonalityText(PersonalityConfig p)
    {
        var lines = new List<string>
        {
            DescribeTrait(p.Assertiveness, "reserved and diplomatic",
                "assertive -- you fight hard for your ideas and don't back down easily"),
            DescribeTrait(p.CreativityTemp, "conventional and proven-path",
                "wildly creative -- you reach for novel, unexpected ideas"),
            DescribeTrait(p.RiskTolerance, "risk-averse and safety-focused",
                "risk-tolerant -- you embrace bold bets and untested approaches"),
            $"Your cognitive style is {p.CognitiveStyle.ToString().ToLower()} -- this shapes how you approach every problem.",
            $"Your emotional baseline is {p.EmotionalBaseline.ToString().ToLower()} -- this colors your reactions and framing.",
            DescribeTrait(p.AttentionSpan, "a topic-hopper who jumps between ideas freely",
                "deeply focused -- you drill into one thread exhaustively"),
            DescribeTrait(p.Stubbornness, "flexible and quick to update your views",
                "stubborn -- you hold your ground and require strong evidence to change your mind"),
            DescribeTrait(p.IdeaReceptivity, "an agenda driver who stays focused on your own ideas",
                "deeply engaged with others' ideas -- you build on what others say and genuinely absorb their perspective"),
            DescribeTrait(p.Bluntness, "diplomatic and tactful -- you soften hard truths",
                "brutally direct -- you say exactly what you think with zero sugar-coating"),
            DescribeTrait(p.Patience, "impatient -- you cut off tangents and push to move on",
                "patient -- you let discussions breathe and don't rush to conclusions")
        };

        if (p.DomainAffinities.Count > 0)
        {
            lines.Add($"You naturally draw from these domains: {string.Join(", ", p.DomainAffinities)}.");
        }

        return string.Join("\n", lines);
    }

    // Converts scalar 0.0-1.0 trait values into natural language descriptions.
    // Personality traits are rendered as prose, not numbers — the LLM never sees raw floats.
    private static string DescribeTrait(double value, string lowDesc, string highDesc)
    {
        if (value >= 0.8)
            return $"You are extremely {highDesc}.";
        if (value >= 0.6)
            return $"You are quite {highDesc}.";
        if (value >= 0.4)
            return $"You balance {lowDesc} and {highDesc} tendencies.";
        if (value >= 0.2)
            return $"You lean toward being {lowDesc}.";
        return $"You are strongly {lowDesc}.";
    }

    private static string GetLevelDescription(OperatingLevel level) => level switch
    {
        OperatingLevel.Requirements => "Focus on WHAT and WHY, not HOW. Describe behavior, rules, and decisions. Do NOT write code or schemas.",
        OperatingLevel.Design => "Focus on design decisions and tradeoffs. You may reference technical concepts but keep the emphasis on choices and rationale.",
        OperatingLevel.Implementation => "Be concrete and technical. Include schemas, code patterns, and specific implementation guidance.",
        _ => "Focus on WHAT and WHY, not HOW. Describe behavior, rules, and decisions. Do NOT write code or schemas."
    };

    private static string GetJobDescription(JobType job) => job switch
    {
        JobType.Propose => "Your job is to PROPOSE -- put forward designs, ideas, and solutions.",
        JobType.Critique => "Your job is to CRITIQUE -- attack the core approach, not just surface details. " +
            "Explain why the fundamental design is wrong, what it will fail on, and what assumption " +
            "will break first in production. If two proposals agree, that's suspicious -- find what " +
            "they both missed. Do not propose full alternatives.",
        JobType.Evaluate => "Your job is to EVALUATE -- pick a winner and reject the loser. Do not " +
            "split the difference. If one approach is better, say so and say why the other fails. " +
            "If both approaches have merit, say which tradeoff is worse and commit to the other. " +
            "Assess through user value, feasibility, and real-world impact.",
        JobType.Simplify => "Your job is to SIMPLIFY -- find the minimum viable version. Ask what can be cut or deferred.",
        JobType.Ideate => "Your job is to IDEATE -- generate 3+ specific, named, surprising ideas stolen from non-software domains.",
        _ => "Your job is to PROPOSE -- put forward designs, ideas, and solutions."
    };

    private static string GetBrevityDescription(Brevity brevity) => brevity switch
    {
        Brevity.Concise => "Be direct and brief. Under 300 words.",
        Brevity.Normal => "Be thorough but not exhaustive. Under 600 words.",
        Brevity.Thorough => "Be comprehensive when warranted, but don't pad.",
        _ => "Be thorough but not exhaustive. Under 600 words."
    };

    private static string ToTitleCase(string input)
    {
        if (string.IsNullOrEmpty(input))
            return input;

        return string.Join(" ", input.Split(' ').Select(word =>
            word.Length > 0 ? char.ToUpper(word[0]) + word.Substring(1).ToLower() : word));
    }

}
