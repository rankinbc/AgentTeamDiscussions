// Agent configuration types — the "Creativity Engine" data model.
//
// Each agent is shaped by 6 independent config layers that combine to produce
// genuinely different perspectives. The key insight from the design docs:
// agents disagree because they hold different VALUES (positions), not because
// they're told to disagree. A Customer advocate and an Infrastructure realist
// will naturally clash on scope without any "be adversarial" instruction.
//
// See: v1/Personalities.md, v1/Positions.md, v1/Anti-Slop.md, v1/Techniques.md

namespace EngineStandalone.Agents;

/// <summary>
/// How the agent reasons. Shapes prompt language about thinking approach.
/// Analytical agents get "break down systematically"; Lateral get "connect unexpected domains".
/// </summary>
public enum CognitiveStyle
{
    Analytical,
    Lateral,
    Systematic,
    Intuitive,
    Divergent
}

/// <summary>
/// The agent's default emotional register. Rendered as natural language in prompts,
/// not as a number — e.g. Skeptical becomes "You approach claims with healthy doubt."
/// </summary>
public enum EmotionalBaseline
{
    Optimistic,
    Skeptical,
    Curious,
    Cautious,
    Neutral,
    Enthusiastic
}

public enum Brevity
{
    Concise,
    Normal,
    Thorough
}

/// <summary>
/// What abstraction level the agent operates at.
/// Affects the Task Layer of context assembly.
/// </summary>
public enum OperatingLevel
{
    Requirements,
    Design,
    Implementation
}

/// <summary>
/// The agent's assigned role in a discussion round.
/// Maps to round names in experiment_modes.yaml (propose/critique/evaluate).
/// </summary>
public enum JobType
{
    Propose,
    Critique,
    Evaluate,
    Simplify,
    Ideate
}

/// <summary>
/// 8 scalar personality dimensions (0.0–1.0) that create emergent agent behavior.
/// These are NOT cosmetic — they directly affect orchestration:
///   - Assertiveness + Intensity → speaking order priority
///   - Patience → context filtering (low patience agents get truncated history)
///   - IdeaReceptivity → whether agent builds on others or stays in own lane
///   - Stubbornness → how much weight in speaking order calculation
/// Rendered as natural language descriptions in the Identity Layer of the prompt.
/// </summary>
public class PersonalityConfig
{
    public double Assertiveness { get; set; } = 0.5;
    public double CreativityTemp { get; set; } = 0.5;
    public double RiskTolerance { get; set; } = 0.5;
    public double AttentionSpan { get; set; } = 0.5;
    public double Stubbornness { get; set; } = 0.5;
    public double IdeaReceptivity { get; set; } = 0.5;
    public double Bluntness { get; set; } = 0.5;
    public double Patience { get; set; } = 0.5;
    public CognitiveStyle CognitiveStyle { get; set; } = CognitiveStyle.Analytical;
    public EmotionalBaseline EmotionalBaseline { get; set; } = EmotionalBaseline.Neutral;
    public List<string> DomainAffinities { get; set; } = new();
}

/// <summary>
/// Positional framing — the agent IS a stakeholder, not just considering one.
/// Creates authentic motivation: a Customer advocate pushes back on scope cuts
/// because they genuinely value user experience, not because they were told to argue.
///   - Drives: what the agent fights for (3-5 items)
///   - PushbackOn: what triggers disagreement (3-5 items)
///   - Intensity: conviction strength, affects speaking order weight
/// </summary>
public class PositionConfig
{
    public string Role { get; set; } = "participant";
    public List<string> Drives { get; set; } = new();
    public List<string> PushbackOn { get; set; } = new();
    public double Intensity { get; set; } = 0.5;
}

/// <summary>
/// Cognitive technique — the thinking pattern an agent applies each turn.
/// Examples: First Principles, Cross-Pollination, Failure-Mode Analysis.
/// Behaviors list contains 5-8 specific actions the agent should take.
/// </summary>
public class TechniqueConfig
{
    public string Primary { get; set; } = "none";
    public string StyleDescription { get; set; } = "";
    public List<string> Behaviors { get; set; } = new();
}

/// <summary>
/// Anti-slop mechanisms — active countermeasures against LLM convergence.
/// Without these, agents drift toward polite agreement within 2-3 rounds.
///   - AgreementTax: must add substance if agreeing; pure "I agree" forbidden
///   - PerspectiveEnforcement: per-turn identity reinforcement prevents drift
///   - DevilsAdvocateDuty: forced contrarian mode (rotating)
///   - UncomfortableIdeaQuota: N contrarian ideas required per discussion
///   - DomainPivotTrigger: switch analytical domain when clustering detected
/// </summary>
public class AntiSlopConfig
{
    public bool AgreementTax { get; set; } = true;
    public bool PerspectiveEnforcement { get; set; } = true;
    public bool DevilsAdvocateDuty { get; set; } = false;
    public int UncomfortableIdeaQuota { get; set; } = 0;
    public bool DomainPivotTrigger { get; set; } = false;
}

/// <summary>
/// Voice constraints — how the agent sounds, not what it says.
/// AntiPatterns is a core feature (8-15 forbidden phrases like "Great point!",
/// "As an AI", "I agree that") that prevent LLM default politeness.
/// </summary>
public class VoiceConfig
{
    public string Tone { get; set; } = "professional";
    public Brevity Brevity { get; set; } = Brevity.Normal;
    public List<string> VocabularyHints { get; set; } = new();
    public List<string> AntiPatterns { get; set; } = new();
}

/// <summary>
/// What the agent produces. Job maps to discussion round assignment.
/// </summary>
public class OutputConfig
{
    public OperatingLevel OperatingLevel { get; set; } = OperatingLevel.Requirements;
    public JobType Job { get; set; } = JobType.Propose;
}

/// <summary>
/// Complete agent definition. Loaded from YAML in data/agents/.
/// Each agent gets a stable GUID at creation — session output references
/// agents by ID so they're stable across renames.
/// The 6 config layers (Personality, Position, Technique, AntiSlop, Voice, Output)
/// combine in PromptBuilder to produce the Identity Layer of each turn's context.
/// </summary>
public class AgentConfig
{
    public string Id { get; set; } = Guid.NewGuid().ToString();
    public string Name { get; set; } = "";
    public string Description { get; set; } = "";
    public PersonalityConfig Personality { get; set; } = new();
    public PositionConfig Position { get; set; } = new();
    public TechniqueConfig Technique { get; set; } = new();
    public AntiSlopConfig AntiSlop { get; set; } = new();
    public VoiceConfig Voice { get; set; } = new();
    public OutputConfig Output { get; set; } = new();
}

/// <summary>
/// A group of agents configured for discussion. The team YAML defines
/// which agents participate and their agent_key identifiers used in
/// experiment_modes.yaml to assign agents to rounds.
/// </summary>
public class TeamConfig
{
    public Dictionary<string, AgentConfig> Agents { get; set; } = new();

    /// <summary>Round structures available for this team. Key = mode name.</summary>
    public Dictionary<string, TeamMode> Modes { get; set; } = new();

    /// <summary>Mode used when none is specified.</summary>
    public string DefaultMode { get; set; } = "default";

    /// <summary>Resolve a mode by name, falling back to DefaultMode.</summary>
    public TeamMode? GetMode(string? modeName = null)
    {
        var name = modeName ?? DefaultMode;
        return Modes.TryGetValue(name, out var mode) ? mode : null;
    }
}

/// <summary>
/// A discussion mode within a team: round groups + optional role overlays.
/// </summary>
public class TeamMode
{
    public string Description { get; set; } = "";
    public Dictionary<string, List<string>> Groups { get; set; } = new();
    public Dictionary<string, string> AgentRoles { get; set; } = new();
}

/// <summary>
/// Pointer to an agent definition in a team YAML file.
/// Agents can be defined inline or referenced by external file.
/// </summary>
public class AgentReference
{
    public string AgentKey { get; set; } = "";
    public string? File { get; set; }
    public string? AgentId { get; set; }
    public string? Name { get; set; }
}
