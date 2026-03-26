using EngineStandalone.Session;

namespace EngineStandalone.Abstractions;

/// <summary>
/// Abstraction over Morning Brief generation from the decisions ledger.
/// </summary>
public interface IMorningBriefGenerator
{
    Task<string> GenerateAsync(string ledgerText, SessionStatus status, int timeout);
}
