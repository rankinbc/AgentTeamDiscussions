using EngineStandalone.Telemetry;

namespace EngineStandalone.Abstractions;

/// <summary>
/// Records per-turn context snapshots, logs to console, and writes context_stats.json at session end.
/// </summary>
public interface IContextTelemetry
{
    void Record(ContextSnapshot snapshot);
    void LogToConsole(ContextSnapshot snapshot);
    Task WriteSessionStatsAsync(string sessionDir);
}
