using EngineStandalone.Session;
using EngineStandalone.Types;
using Xunit;

namespace EngineStandalone.Tests;

public class SessionConfigTests : IDisposable
{
    private readonly string _tempDir;

    public SessionConfigTests()
    {
        _tempDir = Path.Combine(Path.GetTempPath(), $"session-config-test-{Guid.NewGuid():N}");
        Directory.CreateDirectory(_tempDir);
    }

    public void Dispose()
    {
        if (Directory.Exists(_tempDir))
            Directory.Delete(_tempDir, true);
    }

    [Fact]
    public void DefaultConfig_HasCorrectDefaults()
    {
        var config = new SessionConfig();

        Assert.Equal(1, config.Version);
        Assert.Equal("beta-agents", config.Team);
        Assert.Equal("compete", config.Mode);
        Assert.Equal(120, config.Timeout);
        Assert.Equal("interactive", config.Source);
        Assert.Equal(SessionRunStatus.Ready, config.State.Status);
        Assert.Empty(config.Questions);
        Assert.Empty(config.Decided);
    }

    [Fact]
    public void WriteAndRead_RoundTrips()
    {
        var config = new SessionConfig
        {
            Title = "Test Session",
            Team = "beta-agents",
            Mode = "compete",
            Timeout = 180,
            Source = "test",
            QuestionHash = "abc123",
            Decided = new List<string> { "Decision 1", "Decision 2" },
            Questions = new List<SessionQuestion>
            {
                new() { Number = 1, Title = "First question", Body = "Body of first question" },
                new() { Number = 2, Title = "Second question", Body = "Body of second question" },
            },
        };

        SessionConfigIO.Write(_tempDir, config);

        Assert.True(File.Exists(Path.Combine(_tempDir, "session.json")));

        var loaded = SessionConfigIO.Read(_tempDir);

        Assert.NotNull(loaded);
        Assert.Equal("Test Session", loaded!.Title);
        Assert.Equal("beta-agents", loaded.Team);
        Assert.Equal("compete", loaded.Mode);
        Assert.Equal(180, loaded.Timeout);
        Assert.Equal("abc123", loaded.QuestionHash);
        Assert.Equal(2, loaded.Decided.Count);
        Assert.Equal("Decision 1", loaded.Decided[0]);
        Assert.Equal(2, loaded.Questions.Count);
        Assert.Equal("First question", loaded.Questions[0].Title);
        Assert.Equal("Body of second question", loaded.Questions[1].Body);
    }

    [Fact]
    public void Read_MissingFile_ReturnsNull()
    {
        var result = SessionConfigIO.Read(_tempDir);
        Assert.Null(result);
    }

    [Fact]
    public void Read_CorruptFile_ReturnsNull()
    {
        File.WriteAllText(Path.Combine(_tempDir, "session.json"), "not json at all {{{");
        var result = SessionConfigIO.Read(_tempDir);
        Assert.Null(result);
    }

    [Fact]
    public void Exists_ReturnsFalse_WhenMissing()
    {
        Assert.False(SessionConfigIO.Exists(_tempDir));
    }

    [Fact]
    public void Exists_ReturnsTrue_WhenPresent()
    {
        SessionConfigIO.Write(_tempDir, new SessionConfig());
        Assert.True(SessionConfigIO.Exists(_tempDir));
    }

    [Fact]
    public void StateUpdates_PersistCorrectly()
    {
        var config = new SessionConfig { Title = "Stateful Test" };
        SessionConfigIO.Write(_tempDir, config);

        SessionPersistence.UpdateSessionState(_tempDir, state =>
        {
            state.Status = SessionRunStatus.Running;
            state.Questions["q1"] = new QuestionState
            {
                Status = QuestionRunStatus.Complete,
                Title = "Test question",
                ElapsedSeconds = 42,
            };
        });

        var loaded = SessionConfigIO.Read(_tempDir);
        Assert.NotNull(loaded);
        Assert.Equal(SessionRunStatus.Running, loaded!.State.Status);
        Assert.Single(loaded.State.Questions);
        Assert.Equal(QuestionRunStatus.Complete, loaded.State.Questions["q1"].Status);
        Assert.Equal(42, loaded.State.Questions["q1"].ElapsedSeconds);
    }

    [Fact]
    public void Json_UsesSnakeCaseNaming()
    {
        var config = new SessionConfig
        {
            Title = "Snake Case Test",
            QuestionHash = "abc123",
        };
        SessionConfigIO.Write(_tempDir, config);

        var json = File.ReadAllText(Path.Combine(_tempDir, "session.json"));

        Assert.Contains("\"question_hash\"", json);
        Assert.Contains("\"session_complete\"", json);
        Assert.DoesNotContain("\"QuestionHash\"", json);
        Assert.DoesNotContain("\"SessionComplete\"", json);
    }

    [Fact]
    public void Enums_SerializeAsSnakeCaseStrings()
    {
        var config = new SessionConfig { Title = "Enum Test" };
        config.State.Status = SessionRunStatus.Running;
        config.State.Questions["q1"] = new QuestionState
        {
            Status = QuestionRunStatus.InProgress,
            Rounds = new Dictionary<string, RoundRunStatus>
            {
                ["propose"] = RoundRunStatus.Complete,
                ["critique"] = RoundRunStatus.Failed,
            }
        };

        SessionConfigIO.Write(_tempDir, config);
        var json = File.ReadAllText(Path.Combine(_tempDir, "session.json"));

        Assert.Contains("\"running\"", json);
        Assert.Contains("\"in_progress\"", json);
        Assert.Contains("\"complete\"", json);
        Assert.Contains("\"failed\"", json);

        // Round-trips correctly
        var loaded = SessionConfigIO.Read(_tempDir);
        Assert.NotNull(loaded);
        Assert.Equal(SessionRunStatus.Running, loaded!.State.Status);
        Assert.Equal(QuestionRunStatus.InProgress, loaded.State.Questions["q1"].Status);
        Assert.Equal(RoundRunStatus.Complete, loaded.State.Questions["q1"].Rounds!["propose"]);
        Assert.Equal(RoundRunStatus.Failed, loaded.State.Questions["q1"].Rounds!["critique"]);
    }
}
