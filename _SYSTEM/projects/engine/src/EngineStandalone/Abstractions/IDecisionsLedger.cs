namespace EngineStandalone.Abstractions;

/// <summary>
/// Abstraction over the append-only decisions ledger.
/// </summary>
public interface IDecisionsLedger
{
    string GetLedgerPath(string sessionDir);
    string ReadLedger(string sessionDir);
    string? ExtractLedgerSection(string designDoc);
    bool HallucinationCheck(string designDoc, string ledgerSection, double ratioMax = 4.0, double ratioMin = 0.2);
    void AppendToLedger(string sessionDir, string ledgerSection, int questionNumber, string? questionTitle = null);
    string CreateFallbackEntry(int questionNumber, string title);
}
