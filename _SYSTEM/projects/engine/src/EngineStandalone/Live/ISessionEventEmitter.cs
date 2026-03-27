// SSE live streaming protocol: interface + strongly-typed event records.
// Each event type mirrors the React UI's TypeScript types (ui/src/types/events.ts).
// The emitter is optional -- when null, the engine runs in CLI-only mode.
using System.Text.Json.Serialization;

namespace EngineStandalone.Live;

/// <summary>
/// Contract for emitting session events to live consumers (SSE, console, etc.).
/// </summary>
public interface ISessionEventEmitter
{
    void Emit(SessionEvent evt);
    string? PopModerator();
    void QueueModerator(string message);
}

/// <summary>
/// Base class for all session events. Serialized as JSON for SSE.
/// </summary>
[JsonDerivedType(typeof(SessionStartEvent))]
[JsonDerivedType(typeof(AgentProfileEvent))]
[JsonDerivedType(typeof(QuestionStartEvent))]
[JsonDerivedType(typeof(QuestionDoneEvent))]
[JsonDerivedType(typeof(QuestionFailedEvent))]
[JsonDerivedType(typeof(RoundStartEvent))]
[JsonDerivedType(typeof(AgentThinkingEvent))]
[JsonDerivedType(typeof(AgentContextEvent))]
[JsonDerivedType(typeof(AgentContextStatsEvent))]
[JsonDerivedType(typeof(AgentResponseEvent))]
[JsonDerivedType(typeof(SynthesisStartEvent))]
[JsonDerivedType(typeof(SynthesisDoneEvent))]
[JsonDerivedType(typeof(LedgerExtractedEvent))]
[JsonDerivedType(typeof(SessionDoneEvent))]
[JsonDerivedType(typeof(BriefStartEvent))]
[JsonDerivedType(typeof(BriefDoneEvent))]
[JsonDerivedType(typeof(ModeratorMessageEvent))]
[JsonDerivedType(typeof(SessionStoppedEvent))]
public abstract record SessionEvent
{
    [JsonPropertyName("type")]
    public abstract string Type { get; }

    [JsonPropertyName("time")]
    public string Time { get; init; } = DateTime.UtcNow.ToString("o");
}

public record SessionStartEvent : SessionEvent
{
    public override string Type => "session_start";

    [JsonPropertyName("brief")]
    public string Brief { get; init; } = "";

    [JsonPropertyName("mode")]
    public string Mode { get; init; } = "";

    [JsonPropertyName("question_count")]
    public int QuestionCount { get; init; }

    [JsonPropertyName("agents")]
    public List<string> Agents { get; init; } = new();

    [JsonPropertyName("display_names")]
    public Dictionary<string, string> DisplayNames { get; init; } = new();

    [JsonPropertyName("timeout")]
    public int? Timeout { get; init; }
}

public record AgentProfileEvent : SessionEvent
{
    public override string Type => "agent_profile";

    [JsonPropertyName("key")]
    public string Key { get; init; } = "";

    [JsonPropertyName("name")]
    public string Name { get; init; } = "";

    [JsonPropertyName("role")]
    public string Role { get; init; } = "";

    [JsonPropertyName("traits")]
    public Dictionary<string, double> Traits { get; init; } = new();

    [JsonPropertyName("cognitive_style")]
    public string? CognitiveStyle { get; init; }

    [JsonPropertyName("emotional_baseline")]
    public string? EmotionalBaseline { get; init; }

    [JsonPropertyName("drives")]
    public List<string> Drives { get; init; } = new();

    [JsonPropertyName("pushback_on")]
    public List<string> PushbackOn { get; init; } = new();

    [JsonPropertyName("anti_slop")]
    public Dictionary<string, object> AntiSlop { get; init; } = new();

    [JsonPropertyName("voice_tone")]
    public string? VoiceTone { get; init; }

    [JsonPropertyName("intensity")]
    public double? Intensity { get; init; }
}

public record QuestionStartEvent : SessionEvent
{
    public override string Type => "question_start";

    [JsonPropertyName("number")]
    public int Number { get; init; }

    [JsonPropertyName("total")]
    public int Total { get; init; }

    [JsonPropertyName("title")]
    public string Title { get; init; } = "";
}

public record QuestionDoneEvent : SessionEvent
{
    public override string Type => "question_done";

    [JsonPropertyName("number")]
    public int Number { get; init; }

    [JsonPropertyName("elapsed")]
    public double Elapsed { get; init; }
}

public record QuestionFailedEvent : SessionEvent
{
    public override string Type => "question_failed";

    [JsonPropertyName("number")]
    public int Number { get; init; }

    [JsonPropertyName("reason")]
    public string Reason { get; init; } = "";
}

public record RoundStartEvent : SessionEvent
{
    public override string Type => "round_start";

    [JsonPropertyName("round")]
    public string Round { get; init; } = "";

    [JsonPropertyName("agents")]
    public string Agents { get; init; } = "";
}

public record AgentThinkingEvent : SessionEvent
{
    public override string Type => "agent_thinking";

    [JsonPropertyName("agent")]
    public string Agent { get; init; } = "";

    [JsonPropertyName("display_name")]
    public string DisplayName { get; init; } = "";

    [JsonPropertyName("round")]
    public string Round { get; init; } = "";

    [JsonPropertyName("question")]
    public int Question { get; init; }
}

public record AgentContextEvent : SessionEvent
{
    public override string Type => "agent_context";

    [JsonPropertyName("agent")]
    public string Agent { get; init; } = "";

    [JsonPropertyName("display_name")]
    public string DisplayName { get; init; } = "";

    [JsonPropertyName("round")]
    public string Round { get; init; } = "";

    [JsonPropertyName("question")]
    public int Question { get; init; }

    [JsonPropertyName("system_prompt")]
    public string SystemPrompt { get; init; } = "";

    [JsonPropertyName("payload")]
    public string Payload { get; init; } = "";
}

public record AgentContextStatsEvent : SessionEvent
{
    public override string Type => "agent_context_stats";

    [JsonPropertyName("agent")]
    public string Agent { get; init; } = "";

    [JsonPropertyName("round")]
    public string Round { get; init; } = "";

    [JsonPropertyName("question")]
    public int Question { get; init; }

    [JsonPropertyName("total_tokens")]
    public int TotalTokens { get; init; }

    [JsonPropertyName("budget_tokens")]
    public int BudgetTokens { get; init; }

    [JsonPropertyName("budget_pct")]
    public double BudgetPct { get; init; }

    [JsonPropertyName("sections")]
    public List<ContextSectionStat> Sections { get; init; } = new();

    [JsonPropertyName("rescue_actions")]
    public List<string> RescueActions { get; init; } = new();
}

public record ContextSectionStat
{
    [JsonPropertyName("name")]
    public string Name { get; init; } = "";

    [JsonPropertyName("chars")]
    public int Chars { get; init; }

    [JsonPropertyName("tokens")]
    public int Tokens { get; init; }

    [JsonPropertyName("is_protected")]
    public bool IsProtected { get; init; }
}

public record AgentResponseEvent : SessionEvent
{
    public override string Type => "agent_response";

    [JsonPropertyName("agent")]
    public string Agent { get; init; } = "";

    [JsonPropertyName("display_name")]
    public string DisplayName { get; init; } = "";

    [JsonPropertyName("response")]
    public string Response { get; init; } = "";

    [JsonPropertyName("elapsed")]
    public double Elapsed { get; init; }

    [JsonPropertyName("question")]
    public int Question { get; init; }

    [JsonPropertyName("round")]
    public string Round { get; init; } = "";

    [JsonPropertyName("error")]
    public bool? Error { get; init; }
}

public record SynthesisStartEvent : SessionEvent
{
    public override string Type => "synthesis_start";

    [JsonPropertyName("question")]
    public int Question { get; init; }
}

public record SynthesisDoneEvent : SessionEvent
{
    public override string Type => "synthesis_done";

    [JsonPropertyName("question_num")]
    public int QuestionNum { get; init; }

    [JsonPropertyName("question_title")]
    public string QuestionTitle { get; init; } = "";

    [JsonPropertyName("round_context")]
    public string RoundContext { get; init; } = "";

    [JsonPropertyName("system_prompt")]
    public string SystemPrompt { get; init; } = "";

    [JsonPropertyName("full_doc")]
    public string FullDoc { get; init; } = "";

    [JsonPropertyName("preview")]
    public string Preview { get; init; } = "";

    [JsonPropertyName("elapsed")]
    public double Elapsed { get; init; }

    [JsonPropertyName("lines")]
    public int Lines { get; init; }
}

public record LedgerExtractedEvent : SessionEvent
{
    public override string Type => "ledger_extracted";

    [JsonPropertyName("count")]
    public int Count { get; init; }

    [JsonPropertyName("question")]
    public int Question { get; init; }
}

public record SessionDoneEvent : SessionEvent
{
    public override string Type => "session_done";

    [JsonPropertyName("elapsed")]
    public string Elapsed { get; init; } = "";

    [JsonPropertyName("completed")]
    public int Completed { get; init; }

    [JsonPropertyName("total")]
    public int Total { get; init; }
}

public record BriefStartEvent : SessionEvent
{
    public override string Type => "brief_start";
}

public record BriefDoneEvent : SessionEvent
{
    public override string Type => "brief_done";

    [JsonPropertyName("preview")]
    public string Preview { get; init; } = "";
}

public record ModeratorMessageEvent : SessionEvent
{
    public override string Type => "moderator_message";

    [JsonPropertyName("text")]
    public string Text { get; init; } = "";
}

public record SessionStoppedEvent : SessionEvent
{
    public override string Type => "session_stopped";
}
