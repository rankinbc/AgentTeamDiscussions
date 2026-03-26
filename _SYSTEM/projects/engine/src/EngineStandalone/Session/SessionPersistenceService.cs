// Instance wrapper over the static SessionPersistence class.
// Enables DI and interface-based testing while preserving the existing static API.

using EngineStandalone.Abstractions;

namespace EngineStandalone.Session;

/// <summary>
/// Instance service that delegates to the static SessionPersistence methods.
/// Implements ISessionPersistence for dependency injection.
/// </summary>
public class SessionPersistenceService : ISessionPersistence
{
    public void WriteWithMarker(string path, string content)
        => SessionPersistence.WriteWithMarker(path, content);

    public bool IsComplete(string path)
        => SessionPersistence.IsComplete(path);

    public string ReadWithoutMarker(string path)
        => SessionPersistence.ReadWithoutMarker(path);

    public string CreateSessionDir(string sessionsRoot, string briefName)
        => SessionPersistence.CreateSessionDir(sessionsRoot, briefName);

    public string HashQuestionList(IEnumerable<(int Number, string Title)> questions)
        => SessionPersistence.HashQuestionList(questions);

    public int CountCompletedQuestions(string sessionDir)
        => SessionPersistence.CountCompletedQuestions(sessionDir);

    public void WriteSessionStatus(string sessionDir, SessionStatus status)
        => SessionPersistence.WriteSessionStatus(sessionDir, status);

    public SessionStatus LoadSessionStatus(string sessionDir)
        => SessionPersistence.LoadSessionStatus(sessionDir);

    public void WriteSessionConfig(string sessionDir, SessionConfig config)
        => SessionPersistence.WriteSessionConfig(sessionDir, config);

    public SessionConfig? LoadSessionConfig(string sessionDir)
        => SessionPersistence.LoadSessionConfig(sessionDir);
}
