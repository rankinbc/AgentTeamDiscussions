namespace EngineStandalone.Abstractions;

using EngineStandalone.Session;

/// <summary>
/// Abstraction over crash-safe session file I/O.
/// </summary>
public interface ISessionPersistence
{
    void WriteWithMarker(string path, string content);
    bool IsComplete(string path);
    string ReadWithoutMarker(string path);
    string CreateSessionDir(string sessionsRoot, string briefName);
    string HashQuestionList(IEnumerable<(int Number, string Title)> questions);
    int CountCompletedQuestions(string sessionDir);
    void WriteSessionStatus(string sessionDir, SessionStatus status);
    SessionStatus LoadSessionStatus(string sessionDir);
    void WriteSessionConfig(string sessionDir, SessionConfig config);
    SessionConfig? LoadSessionConfig(string sessionDir);
}
