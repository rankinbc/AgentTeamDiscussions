using EngineStandalone.Telemetry;

namespace EngineStandalone.Abstractions;

/// <summary>
/// Collects context snapshots per agent turn, logs them, and writes session stats.
/// </summary>
public interface IContextTelemetry
{
    void Record(ContextSnapshot snapshot);
    void LogToConsole(ContextSnapshot snapshot);
    Task WriteSessionStatsAsync(string sessionDir);
}
