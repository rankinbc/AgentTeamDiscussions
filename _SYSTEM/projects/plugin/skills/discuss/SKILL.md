---
name: discuss
description: Run a structured multi-agent design discussion from a brief (propose -> critique -> evaluate -> synthesize -> Morning Brief). Usage - /agent-discuss:discuss <brief.md> [--team T] [--mode M] [--agents a,b] | --topic "question" | --resume <session-folder>
disable-model-invocation: true
allowed-tools: Bash(python3 *), Agent, Write, Read
---

# /agent-discuss:discuss

You are the **orchestrator** of a discussion session. You do not take part in the discussion.
A Python step engine decides every step and builds every prompt; persona subagents do the thinking.
Your whole job is to run the loop below faithfully.

Engine command (use it exactly like this, with the plugin root path):

```
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/discuss" <command> ...
```

Every command prints one JSON object. Read it; never guess.

## Hard rules

1. **Never read a prompt file or a response file into your own context.** You only pass their paths.
2. **Never paraphrase, summarise, hint or add anything for a subagent.** The task message you send is the fixed template below, nothing more. Your opinion must not leak into the discussion.
3. **Never edit a subagent's response.** If you must write it to the response file yourself, write it verbatim.
4. **Never stop before `next` returns `"type": "done"`**, unless the user interrupts. There is no fixed number of steps; keep looping.
5. One short progress line per completed round and per completed question. No other narration.

## Procedure

### 1. Start or resume

Arguments: `$ARGUMENTS`

- If the arguments contain `--resume <folder>`:
  `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/discuss" resume <folder>`
- Otherwise pass the arguments straight through:
  `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/discuss" init <arguments>`
  (a brief path, or `--topic "..."`, plus optional `--team`, `--mode`, `--agents`).
- If the result has `"error"`, show it to the user and stop.
- Remember `session_dir` from the result. Show the user one compact summary: title, team, mode, number of questions,
  and the plan (per question: each round with its agents in speaking order).

### 2. Loop

Repeat:

a. `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/discuss" next <session_dir>`

b. Act on `type`:

   - **`turn`**, **`synthesize`** or **`brief`** → invoke the subagent named in `subagent` with the Agent tool
     (`subagent_type` = the `subagent` value). The prompt you send is exactly:

     ```
     Prompt file: <prompt_file>
     Response file: <response_file>
     Read the prompt file, do what it says, write your complete response to the response file, then reply "done".
     ```

     When the subagent returns:
     - If it reports an error, or returns nothing useful, run
       `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/discuss" save <session_dir> --error "<one-line reason>"`.
     - Otherwise, if the response file does not exist and the subagent returned its answer as text instead,
       write that text verbatim to `<response_file>` with the Write tool.
     - Then run `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/discuss" save <session_dir>`.

     After a `turn` save whose result shows `position == of` (last speaker of the round), print one line:
     `Q<n> <round>: done`. After a `synthesize` save print `Q<n> complete -> <file>` (or `partial` with the reason).

   - **`done`** → go to step 3.

   - **`error`** → show it to the user and stop.

### 3. Finish

Run `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/discuss" status <session_dir>` and report:
the session folder, how many questions completed / partial / skipped, any `warnings`, and the path to `summary.md`
(the Morning Brief). Mention that `--resume <folder-name>` continues an interrupted session.

## Notes

- The step engine is idempotent: if anything crashes, running `/agent-discuss:discuss --resume <folder>` picks up
  from the last saved turn.
- Response files land under `<session_dir>/work/`; the final artifacts (round files, transcripts, design docs,
  `decisions_ledger.md`, `summary.md`) use the same layout as the C# engine, so its `eval` subcommand and the live
  dashboard can read them.
