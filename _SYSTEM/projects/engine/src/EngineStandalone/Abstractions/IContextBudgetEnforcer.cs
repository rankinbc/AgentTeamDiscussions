using EngineStandalone.Config;
using EngineStandalone.Telemetry;

namespace EngineStandalone.Abstractions;

/// <summary>
/// Evaluates context sections against budget thresholds and applies auto-rescue
/// trimming when payloads exceed the configured token ceiling.
/// </summary>
public interface IContextBudgetEnforcer
{
    ContextDiagnosis Diagnose(List<ContextSection> sections, ContextBudgetSettings budget);
    List<ContextSection> Enforce(List<ContextSection> sections, ContextBudgetSettings budget);
}
