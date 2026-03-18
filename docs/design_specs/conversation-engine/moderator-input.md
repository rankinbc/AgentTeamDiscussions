# Moderator Input (Live Steering)

*Implementation spec for injecting human direction into live conversations*

## Problem

Once `live_conversation.py` starts, there's no way to influence the discussion. If agents go off-topic, circle endlessly, or miss an important angle, you just watch. The only option is Ctrl+C and restart with a different question.

## Goal

Add a text input to the web UI that lets the user inject messages into the conversation as a "Moderator" -- a participant with special authority. Agents see the moderator's message in their context and respond to it like any other message, but the moderator's input carries weight because the system prompt tells agents to treat moderator messages as priority directives.

## Design

### How It Works

1. User types a message in the input box at the bottom of the UI
2. Browser POSTs the message to `/moderator`
3. Server injects the message into the conversation history as a moderator entry
4. Next agent to speak sees it in their context and responds to it
5. The message appears in the chat UI with a distinct "MODERATOR" style

### Message Injection

The moderator message is added to the `history` list like any agent message, but with a special marker:

```python
history.append({
    "agent": "__moderator__",
    "name": "MODERATOR",
    "text": message,
    "turn": current_turn,
})
```

Agents see it in their context as:
```
[MODERATOR]: Consider the privacy implications of this approach.
```

### System Prompt Addition

Add to `CONVERSATION_SYSTEM`:
```
- If the MODERATOR speaks, treat their message as a priority. Address their point before continuing
  other threads. The moderator is the person who submitted this topic -- they're steering the
  discussion toward what matters to them.
```

### UI Changes

Add an input bar below the turn counter:

```html
<div class="moderator-bar">
    <input type="text" id="mod-input" placeholder="Steer the conversation..." />
    <button onclick="sendModMessage()">Send</button>
</div>
```

Styling: subtle, not dominant. Dark input field matching the existing aesthetic. The input should be clearly available but not visually competing with the conversation.

Moderator messages in the chat use a distinct style:
```css
.msg.moderator {
    border-left-color: var(--amber);
    background: rgba(245, 166, 35, 0.06);
}
.msg.moderator .m-name { color: var(--amber); }
```

### Server Endpoint

```python
def do_POST(self):
    if self.path == "/moderator":
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode()
        data = json.loads(body)
        message = data.get("message", "").strip()
        if message:
            # Add to shared queue that the conversation loop checks
            moderator_queue.append(message)
            emit("system_message", {"message": f"Moderator: {message}"})
            # Also emit as a proper message for the chat
            emit("moderator_message", {"text": message})
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"ok":true}')
```

### Conversation Loop Integration

```python
# Shared state between HTTP server thread and conversation loop
moderator_queue = []

# In run_conversation(), after each agent speaks and before next agent:
while moderator_queue:
    mod_msg = moderator_queue.pop(0)
    history.append({
        "agent": "__moderator__",
        "name": "MODERATOR",
        "text": mod_msg,
        "turn": turn,
    })
```

Threading note: `moderator_queue` is a plain list accessed from two threads. In CPython, list.append and list.pop(0) are effectively atomic due to the GIL. For safety, wrap in the existing `_event_lock` or use `collections.deque` (which has thread-safe append/popleft).

### Context Handling

Moderator messages are treated like any other message in the context window:
- Recent (last 5): shown verbatim
- Older: compressed to first sentence like agent messages

No special treatment in context compression. The moderator's authority comes from the system prompt instruction, not from persistence tricks.

### What This Changes

- `live_conversation.py`:
  - Add `moderator_queue` (thread-safe deque)
  - Add `do_POST` handler to `ConvHandler`
  - Add moderator input bar to HTML
  - Add `moderator_message` SSE event type
  - Add moderator CSS styles
  - Update `CONVERSATION_SYSTEM` with moderator instruction
  - Check queue between agent turns

### What This Doesn't Change

- Agent system prompts (personality, voice)
- Speaking order computation
- Context compression logic (moderator messages compress like any other)
- Convergence detection (moderator messages don't count as agreement signals)
- Transcript saving (moderator messages saved with `MODERATOR` attribution)

## Edge Cases

- **Message while no agents are speaking**: Queued and picked up before the next agent's turn.
- **Multiple messages queued**: All injected in order before the next agent speaks.
- **Empty message**: Ignored (whitespace check).
- **Very long message**: No explicit limit, but it enters the context window like any other message. If it's too long it'll compress to first sentence in older history.
- **Message after conversation ends**: Ignored (conversation loop has exited).

## What the Moderator Should NOT Be

- NOT a way to give agents private instructions (all agents see it)
- NOT a voting mechanism
- NOT a way to force conclusions (agents can disagree with the moderator)
- NOT displayed differently in transcripts (it's part of the conversation record)

## Success Criteria

1. User can type a message and see it appear in the chat immediately
2. The next agent to speak addresses the moderator's point
3. Moderator messages are preserved in the saved transcript
4. The input doesn't interfere with the conversation flow (no pausing, no blocking)
5. Multiple moderator messages can be queued without issues
