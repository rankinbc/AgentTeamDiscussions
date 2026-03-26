// Instance wrapper over the static DecisionsLedger class.
// Enables DI and interface-based testing while preserving the existing static API.

using EngineStandalone.Abstractions;

namespace EngineStandalone.Session;

/// <summary>
/// Instance service that delegates to the static DecisionsLedger methods.
/// Implements IDecisionsLedger for dependency injection.
/// </summary>
public class DecisionsLedgerService : IDecisionsLedger
{
    public string GetLedgerPath(string sessionDir)
        => DecisionsLedger.GetLedgerPath(sessionDir);

    public string ReadLedger(string sessionDir)
        => DecisionsLedger.ReadLedger(sessionDir);

    public string? ExtractLedgerSection(string designDoc)
        => DecisionsLedger.ExtractLedgerSection(designDoc);

    public bool HallucinationCheck(string designDoc, string ledgerSection, double ratioMax = 4.0, double ratioMin = 0.2)
        => DecisionsLedger.HallucinationCheck(designDoc, ledgerSection, ratioMax, ratioMin);

    public void AppendToLedger(string sessionDir, string ledgerSection, int questionNumber, string? questionTitle = null)
        => DecisionsLedger.AppendToLedger(sessionDir, ledgerSection, questionNumber, questionTitle);

    public string CreateFallbackEntry(int questionNumber, string title)
        => DecisionsLedger.CreateFallbackEntry(questionNumber, title);
}
