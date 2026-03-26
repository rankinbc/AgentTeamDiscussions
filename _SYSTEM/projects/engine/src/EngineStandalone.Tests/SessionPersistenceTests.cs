using EngineStandalone.Session;
using Xunit;

namespace EngineStandalone.Tests;

public class SessionPersistenceTests : IDisposable
{
    private readonly string _tempDir;

    public SessionPersistenceTests()
    {
        _tempDir = Path.Combine(Path.GetTempPath(), $"engine-test-{Guid.NewGuid():N}");
        Directory.CreateDirectory(_tempDir);
    }

    public void Dispose()
    {
        if (Directory.Exists(_tempDir))
            Directory.Delete(_tempDir, recursive: true);
    }

    // --- T01: WriteWithMarker writes content + completion marker ---

    [Fact]
    public void WriteWithMarker_WritesContentAndMarker()
    {
        var path = Path.Combine(_tempDir, "test.md");

        SessionPersistence.WriteWithMarker(path, "Hello world");

        var raw = File.ReadAllText(path);
        Assert.Contains("Hello world", raw);
        Assert.Contains("<!-- complete -->", raw);
    }

    // --- T02: IsComplete returns true only when marker present ---

    [Fact]
    public void IsComplete_TrueWhenMarkerPresent()
    {
        var path = Path.Combine(_tempDir, "complete.md");
        SessionPersistence.WriteWithMarker(path, "some content");

        Assert.True(SessionPersistence.IsComplete(path));
    }

    // --- T03: IsComplete returns false for missing/truncated file ---

    [Fact]
    public void IsComplete_FalseForMissingFile()
    {
        var path = Path.Combine(_tempDir, "nonexistent.md");

        Assert.False(SessionPersistence.IsComplete(path));
    }

    [Fact]
    public void IsComplete_FalseForFileWithoutMarker()
    {
        var path = Path.Combine(_tempDir, "incomplete.md");
        File.WriteAllText(path, "partial content without marker");

        Assert.False(SessionPersistence.IsComplete(path));
    }

    // --- T04: ReadWithoutMarker strips marker, preserves content ---

    [Fact]
    public void ReadWithoutMarker_StripsMarkerPreservesContent()
    {
        var path = Path.Combine(_tempDir, "doc.md");
        SessionPersistence.WriteWithMarker(path, "# Design Doc\n\nContent here.");

        var content = SessionPersistence.ReadWithoutMarker(path);

        Assert.Contains("# Design Doc", content);
        Assert.Contains("Content here.", content);
        Assert.DoesNotContain("<!-- complete -->", content);
    }

    // --- T05: HashQuestionList is deterministic ---

    [Fact]
    public void HashQuestionList_SameInputSameHash()
    {
        var questions = new[] { (1, "Feature Ranking"), (2, "Architecture") };

        var hash1 = SessionPersistence.HashQuestionList(questions);
        var hash2 = SessionPersistence.HashQuestionList(questions);

        Assert.Equal(hash1, hash2);
    }

    // --- T06: HashQuestionList changes when questions reordered ---

    [Fact]
    public void HashQuestionList_DifferentOrderDifferentHash()
    {
        var questionsA = new[] { (1, "Feature Ranking"), (2, "Architecture") };
        var questionsB = new[] { (1, "Architecture"), (2, "Feature Ranking") };

        var hashA = SessionPersistence.HashQuestionList(questionsA);
        var hashB = SessionPersistence.HashQuestionList(questionsB);

        Assert.NotEqual(hashA, hashB);
    }

    // --- T07: CountCompletedQuestions counts only marker-complete design docs ---

    [Fact]
    public void CountCompletedQuestions_CountsOnlyCompleteFiles()
    {
        var sessionDir = Path.Combine(_tempDir, "session");
        var questionsDir = Path.Combine(sessionDir, "questions");
        Directory.CreateDirectory(questionsDir);

        // Two complete design docs
        SessionPersistence.WriteWithMarker(
            Path.Combine(questionsDir, "01-feature-ranking.md"), "doc 1");
        SessionPersistence.WriteWithMarker(
            Path.Combine(questionsDir, "02-architecture.md"), "doc 2");

        // One incomplete file (no marker)
        File.WriteAllText(
            Path.Combine(questionsDir, "03-auth-flow.md"), "incomplete");

        Assert.Equal(2, SessionPersistence.CountCompletedQuestions(sessionDir));
    }

    // --- T08: CountCompletedQuestions ignores transcripts and incomplete files ---

    [Fact]
    public void CountCompletedQuestions_IgnoresTranscripts()
    {
        var sessionDir = Path.Combine(_tempDir, "session2");
        var questionsDir = Path.Combine(sessionDir, "questions");
        Directory.CreateDirectory(questionsDir);

        // One design doc (complete)
        SessionPersistence.WriteWithMarker(
            Path.Combine(questionsDir, "01-feature-ranking.md"), "doc");

        // Transcript (complete but should be ignored — ends with -transcript.md)
        SessionPersistence.WriteWithMarker(
            Path.Combine(questionsDir, "01-feature-ranking-transcript.md"), "transcript");

        // Note: round files (-propose.md, -critique.md) are NOT filtered by
        // CountCompletedQuestions — only -transcript.md files are excluded.
        // This test verifies the transcript exclusion specifically.
        Assert.Equal(1, SessionPersistence.CountCompletedQuestions(sessionDir));
    }

    [Fact]
    public void CountCompletedQuestions_ZeroForMissingDir()
    {
        var sessionDir = Path.Combine(_tempDir, "no-session");

        Assert.Equal(0, SessionPersistence.CountCompletedQuestions(sessionDir));
    }

    // --- T09: SessionStatus JSON roundtrip ---

    [Fact]
    public void SessionStatus_WriteAndLoadRoundtrip()
    {
        var sessionDir = Path.Combine(_tempDir, "status-test");
        Directory.CreateDirectory(sessionDir);

        var status = new SessionStatus
        {
            QuestionHash = "abc123",
            Mode = "compete",
            Brief = "test.md",
            SessionComplete = false,
            CompletedQuestions = 3,
            FailedQuestions = 1,
            Questions = new Dictionary<string, QuestionStatus>
            {
                ["q1"] = new QuestionStatus { Status = "complete", Title = "Feature Ranking" }
            }
        };

        SessionPersistence.WriteSessionStatus(sessionDir, status);
        var loaded = SessionPersistence.LoadSessionStatus(sessionDir);

        Assert.Equal("abc123", loaded.QuestionHash);
        Assert.Equal("compete", loaded.Mode);
        Assert.Equal(3, loaded.CompletedQuestions);
        Assert.True(loaded.Questions.ContainsKey("q1"));
        Assert.Equal("complete", loaded.Questions["q1"].Status);
    }

    // --- T10: SessionStatus load returns default for missing/corrupt JSON ---

    [Fact]
    public void SessionStatus_LoadMissingFileReturnsDefault()
    {
        var sessionDir = Path.Combine(_tempDir, "empty-session");
        Directory.CreateDirectory(sessionDir);

        var status = SessionPersistence.LoadSessionStatus(sessionDir);

        Assert.NotNull(status);
        Assert.Null(status.QuestionHash);
        Assert.Empty(status.Questions);
    }

    [Fact]
    public void SessionStatus_LoadCorruptJsonReturnsDefault()
    {
        var sessionDir = Path.Combine(_tempDir, "corrupt-session");
        Directory.CreateDirectory(sessionDir);
        File.WriteAllText(Path.Combine(sessionDir, "session_status.json"), "{ invalid json }}}");

        var status = SessionPersistence.LoadSessionStatus(sessionDir);

        Assert.NotNull(status);
        Assert.Empty(status.Questions);
    }

    // --- T28: CreateSessionDir produces timestamped dir with questions/ subdir ---

    [Fact]
    public void CreateSessionDir_CreatesTimestampedDirWithQuestionsSubdir()
    {
        var sessionDir = SessionPersistence.CreateSessionDir(_tempDir, "my-brief");

        Assert.True(Directory.Exists(sessionDir));
        Assert.True(Directory.Exists(Path.Combine(sessionDir, "questions")));
        Assert.Contains("my-brief", Path.GetFileName(sessionDir));
        // Should contain date pattern YYYY-MM-DD
        Assert.Matches(@"\d{4}-\d{2}-\d{2}", Path.GetFileName(sessionDir));
    }

    // --- T35: HashQuestionList returns 16-char hex string ---

    [Fact]
    public void HashQuestionList_Returns16CharHexString()
    {
        var questions = new[] { (1, "Test Question") };

        var hash = SessionPersistence.HashQuestionList(questions);

        Assert.Equal(16, hash.Length);
        Assert.Matches(@"^[0-9a-f]{16}$", hash);
    }
}
