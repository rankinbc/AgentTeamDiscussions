// Centralized enums replacing magic strings throughout the codebase.

using System.Text.Json;
using System.Text.Json.Serialization;

namespace EngineStandalone.Types;

/// <summary>Overall session lifecycle state.</summary>
[JsonConverter(typeof(JsonStringEnumConverter<SessionRunStatus>))]
public enum SessionRunStatus
{
    Ready,
    Running,
    Complete,
    Aborted
}

/// <summary>Per-question execution outcome.</summary>
[JsonConverter(typeof(JsonStringEnumConverter<QuestionRunStatus>))]
public enum QuestionRunStatus
{
    Complete,
    Partial,
    Skipped,
    Failed,
    InProgress
}

/// <summary>Per-round execution outcome.</summary>
[JsonConverter(typeof(JsonStringEnumConverter<RoundRunStatus>))]
public enum RoundRunStatus
{
    Complete,
    Failed
}

/// <summary>
/// Custom JSON naming policy that converts enum values to snake_case for serialization.
/// E.g., InProgress → "in_progress", Complete → "complete".
/// </summary>
public class SnakeCaseEnumNamingPolicy : JsonNamingPolicy
{
    public override string ConvertName(string name)
    {
        // Insert underscore before each uppercase letter (except the first), then lowercase.
        var result = new System.Text.StringBuilder();
        for (int i = 0; i < name.Length; i++)
        {
            if (i > 0 && char.IsUpper(name[i]))
                result.Append('_');
            result.Append(char.ToLower(name[i]));
        }
        return result.ToString();
    }
}
