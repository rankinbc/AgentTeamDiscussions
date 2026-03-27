using EngineStandalone.Telemetry;

namespace EngineStandalone.Abstractions;

/// <summary>
/// Diagnoses over-budget or imbalanced context snapshots and enforces budget by
/// progressively trimming sections in priority order.
/// </summary>
public interface IContextBudgetEnforcer
{
    ContextDiagnosis Diagnose(ContextSnapshot snapshot);
    (List<ContextSection> Sections, List<string> RescueActions) Enforce(List<ContextSection> sections, ContextDiagnosis diagnosis);
}
