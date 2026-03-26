// Concrete SSE emitter using System.Threading.Channels for lock-free event distribution.
// Supports snapshot replay (late-joining clients see full state) and a thread-safe
// moderator queue for human-in-the-loop directives injected between rounds.
using System.Collections.Concurrent;
using System.Text.Json;
using System.Threading.Channels;

namespace EngineStandalone.Live;

/// <summary>
/// Thread-safe SSE event emitter using Channel&lt;T&gt; for lock-free distribution.
/// Also handles the moderator message queue.
/// </summary>
public class SseSessionEmitter : ISessionEventEmitter
{
    private readonly List<SessionEvent> _snapshot = new();
    private readonly object _snapshotLock = new();
    private readonly ConcurrentBag<Channel<SessionEvent>> _clients = new();
    private readonly ConcurrentQueue<string> _moderatorQueue = new();

    /// <summary>
    /// Mutable session directory, set by SessionRunner once the session starts.
    /// Used by the /ledger endpoint to find the decisions ledger file.
    /// </summary>
    public string? SessionDir { get; set; }

    private static readonly JsonSerializerOptions JsonOptions = new()
    {
        PropertyNamingPolicy = JsonNamingPolicy.CamelCase,
        DefaultIgnoreCondition = System.Text.Json.Serialization.JsonIgnoreCondition.WhenWritingNull
    };

    public void Emit(SessionEvent evt)
    {
        // Store in snapshot for late-joining clients
        lock (_snapshotLock)
        {
            _snapshot.Add(evt);
        }

        // Distribute to all connected SSE clients
        foreach (var channel in _clients)
        {
            channel.Writer.TryWrite(evt);
        }

        // Also log to console
        Console.WriteLine($"  [SSE] {evt.Type}");
    }

    /// <summary>
    /// Create a new SSE client channel and replay existing events.
    /// </summary>
    public Channel<SessionEvent> Subscribe()
    {
        var channel = Channel.CreateUnbounded<SessionEvent>(new UnboundedChannelOptions
        {
            SingleReader = true,
            SingleWriter = false
        });

        // Replay snapshot
        lock (_snapshotLock)
        {
            foreach (var evt in _snapshot)
            {
                channel.Writer.TryWrite(evt);
            }
        }

        _clients.Add(channel);
        return channel;
    }

    public void QueueModerator(string message)
    {
        _moderatorQueue.Enqueue(message);
        Emit(new ModeratorMessageEvent { Text = message });
    }

    public string? PopModerator()
    {
        return _moderatorQueue.TryDequeue(out var msg) ? msg : null;
    }

    /// <summary>
    /// Serialize a session event to JSON for SSE transmission.
    /// </summary>
    public static string ToJson(SessionEvent evt)
    {
        return JsonSerializer.Serialize(evt, evt.GetType(), JsonOptions);
    }
}
