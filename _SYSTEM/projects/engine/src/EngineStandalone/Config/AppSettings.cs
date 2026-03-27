// AppSettings.cs — Tunable knobs loaded from defaults.yaml.
// All values here are defaults; YAML config overrides them at startup via ConfigLoader.

namespace EngineStandalone.Config;

/// <summary>
/// Per-call LLM timeouts in seconds. Discussion=420s, Evaluation=300s.
/// </summary>
public class TimeoutSettings
{
    public int Default { get; set; } = 120;
    public int Discussion { get; set; } = 420;
    public int Evaluation { get; set; } = 300;
    public int BatchQuestion { get; set; } = 600;
    public int LiveTurn { get; set; } = 60;
    public int SynthesisRolling { get; set; } = 30;
    public int Panel { get; set; } = 360;
    public int Brainstorm { get; set; } = 420;
}

/// <summary>
/// Token budget management (char limits). PriorSpecs=6000, DesignDocChain=3000.
/// Prevents context explosion as questions accumulate across rounds.
/// </summary>
public class TruncationSettings
{
    public int PriorSpecs { get; set; } = 6000;
    public int DesignDocChain { get; set; } = 3000;
    public int BrainstormInput { get; set; } = 8000;
    public int AgentEvalInput { get; set; } = 8000;
    public int DocEvalInput { get; set; } = 12000;
    public int RoundAnalysis { get; set; } = 1500;
    public int SpecGenContext { get; set; } = 2000;
    public int LowPatienceContext { get; set; } = 2500;
    public int LiveContext { get; set; } = 5000;
}

/// <summary>
/// Conversation settings loaded from defaults.yaml.
/// </summary>
public class ConversationSettings
{
    public int HistoryKeepFirst { get; set; } = 2;
    public int HistoryKeepLast { get; set; } = 10;
    public int HistoryTruncationThreshold { get; set; } = 14;
    public int MultiHistoryKeepFirst { get; set; } = 3;
    public int MultiHistoryKeepLast { get; set; } = 15;
    public int MultiHistoryTruncationThreshold { get; set; } = 20;
    public int MaxWordCount { get; set; } = 250;
    public string LiveSentenceLimit { get; set; } = "2-4";
}

/// <summary>
/// Safety rails. MinResponseLength=20 chars, MinSynthesisLength=50 chars.
/// CircuitBreakerThreshold=3 consecutive failures before stopping the session.
/// </summary>
public class HealthCheckSettings
{
    public int MinResponseLength { get; set; } = 20;
    public int MinSynthesisLength { get; set; } = 50;
    public double HallucinationRatioMax { get; set; } = 4.0;
    public double HallucinationRatioMin { get; set; } = 0.2;
    public int CircuitBreakerThreshold { get; set; } = 3;
}

/// <summary>
/// Rolling synthesis config for conversation mode (how often to summarize, ledger word cap).
/// </summary>
public class SynthesisSettings
{
    public int IntervalTurns { get; set; } = 10;
    public int MaxLedgerWords { get; set; } = 50;
}

/// <summary>
/// Display settings loaded from defaults.yaml.
/// </summary>
public class DisplaySettings
{
    public int SeparatorWidth { get; set; } = 60;
    public int SlugMaxLength { get; set; } = 60;
}

/// <summary>
/// Path defaults for session and output directories.
/// </summary>
public class PathSettings
{
    public string SessionsDir { get; set; } = "output/sessions";
    public string OutputDir { get; set; } = "output/design-docs";
    public string DefaultTeam { get; set; } = "beta-agents";
}

/// <summary>
/// Session-level defaults.
/// </summary>
public class SessionSettings
{
    public bool RunEval { get; set; }
    public int LivePort { get; set; } = 8899;
}

/// <summary>
/// Context budget settings. MaxPayloadTokens is used for % display in telemetry.
/// Enabled=true activates the budget enforcer to auto-trim over-budget payloads.
/// </summary>
public class ContextBudgetSettings
{
    public bool Enabled { get; set; } = false;
    public int MaxPayloadTokens { get; set; } = 4000;
    public double ImbalanceThreshold { get; set; } = 0.60;
}

/// <summary>
/// Root application settings combining all config sections.
/// </summary>
public class AppSettings
{
    public TimeoutSettings Timeouts { get; set; } = new();
    public TruncationSettings Truncation { get; set; } = new();
    public ConversationSettings Conversation { get; set; } = new();
    public HealthCheckSettings HealthChecks { get; set; } = new();
    public SynthesisSettings Synthesis { get; set; } = new();
    public DisplaySettings Display { get; set; } = new();
    public PathSettings Paths { get; set; } = new();
    public SessionSettings Session { get; set; } = new();
    public ContextBudgetSettings ContextBudget { get; set; } = new();
    public string CompletionMarker { get; set; } = "\n<!-- complete -->\n";
}

/// <summary>
/// Role overlay: modifies agent behavior per-mode (e.g., "competitive" -> "Frame as competing proposal").
/// </summary>
public class RoleOverlay
{
    public string Description { get; set; } = "";
    public string Instruction { get; set; } = "";
}

/// <summary>
/// Agent display configuration.
/// </summary>
public class AgentDisplayConfig
{
    public Dictionary<string, string> DisplayNames { get; set; } = new();
    public Dictionary<string, string> ColorsHex { get; set; } = new();
    public List<string> ColorsAnsiCycle { get; set; } = new();
}
