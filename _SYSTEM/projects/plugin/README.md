# agent-discuss — AgentTeamDiscussions as a Claude Code plugin

Prototype that runs the engine's discussion loop (propose → critique → evaluate → synthesize →
decisions ledger → Morning Brief) inside Claude Code instead of the C# engine. Every persona is a
subagent; a small Python step engine builds every prompt and persists every artifact in the same
`output/sessions/` layout the engine uses.

## Layout

```
.claude-plugin/plugin.json
agents/                     33 generated persona subagents (+ manifest.json) and two hand-written ones:
  synthesizer.md            the moderator (body = templates/prompts/synthesis.md.j2)
  morning-brief.md          the Morning Brief writer (morning_brief_system + morning_brief_user)
skills/discuss/SKILL.md     /agent-discuss:discuss — the orchestrator loop
skills/list-teams/SKILL.md  /agent-discuss:list-teams
scripts/gen_agents.py       persona YAML -> agents/*.md  (port of PromptBuilder.BuildSystemPrompt)
scripts/discuss/            step engine CLI (init / resume / next / save / status / list-teams)
tests/                      unit tests + end-to-end dry run (no Claude calls)
```

Source of truth is read in place, nothing is copied: personas from `_SYSTEM/data/discussionAgents/`,
modes from `_SYSTEM/projects/engine/data/teams/`, overlays/display names/defaults from
`_SYSTEM/projects/engine/config/`. Requires Python 3 and PyYAML.

## Run

```bash
# from the repo root
claude --plugin-dir _SYSTEM/projects/plugin
```

Inside Claude Code:

```
/agent-discuss:list-teams
/agent-discuss:discuss _SYSTEM/projects/engine/input/test-brief.md --mode compete
/agent-discuss:discuss --topic "How should we handle errors?" --team beta-agents
/agent-discuss:discuss --resume 2026-10-05_0852_test-brief
```

Headless / overnight:

```bash
claude -p "/agent-discuss:discuss _SYSTEM/projects/engine/input/my-brief.md" \
  --plugin-dir _SYSTEM/projects/plugin --permission-mode acceptEdits --max-turns 600
```

Output lands in `_SYSTEM/projects/engine/output/sessions/{date}_{slug}/` with the engine's file names
(`questions/NN-slug.md`, `-transcript.md`, `-propose.md`…, `decisions_ledger.md`, `summary.md`, `session.json`),
so the engine's evaluator works unchanged:

```bash
cd _SYSTEM/projects/engine && dotnet run --project src/EngineStandalone -- eval output/sessions/<folder>/questions
```

## How it works

1. `init` parses the brief, validates team/mode/agents, computes the speaking order for every round once
   (`assertiveness*0.5 + intensity*0.3 + stubbornness*0.2 ± 0.1`) and stores it in `session.json`.
2. The skill loops `next` → subagent → `save`. `next` finds the first unfinished turn from files on disk and
   writes its prompt to `work/qNN-round-agent.prompt.md`; the orchestrator passes only the two file paths to
   the persona subagent, which reads the prompt, writes its answer to the response file and replies `done`.
   `save` stamps the response with the completion marker.
3. When a round completes, `next` writes the round file; when all rounds complete it emits a `synthesize`
   step; after the last question a `brief` step. The design doc, transcript, ledger entry and Morning Brief
   are written exactly as `SessionRunner` writes them.
4. Everything is idempotent, so `--resume` after a crash continues from the last saved turn.

Why the orchestrating model never sees prompt or response content: the engine's `RoundRunner.BuildAgentSections`
controls precisely what each agent sees. Letting the orchestrator paraphrase would leak its opinion into every
turn and make blind proposals / anti-sycophancy measurement meaningless. It also keeps the orchestrator's
context tiny, which is what makes multi-hour unattended runs feasible.

## Regenerate personas

```bash
python3 _SYSTEM/projects/plugin/scripts/gen_agents.py
```

Run after editing any persona YAML. Generated files carry a header comment; do not edit them by hand.

## Tests

```bash
cd _SYSTEM/projects/plugin
python3 -m unittest discover -s tests          # ports: brief, prompts, ledger, persistence, speaking order
python3 tests/dry_run.py                       # full init -> next/save loop -> done with canned responses
```

## Parity with the C# engine, and known gaps

Same: system prompts (section order and trait phrasing), per-turn payload order, Position Summary compression,
low-patience truncation, round instructions, overlays, cascade rules (propose fails → skipped; critique/evaluate
fails → partial; synthesis under 50 chars → partial; 3 consecutive failures → circuit breaker), ledger
extraction (ledger section → decision headings → stub), file layout and completion markers.

The engine bugs found while porting (double ledger, resume over-counting, unfilled synthesis placeholders,
unparsed `allergies`, preparer/runner reading different team files) were fixed in the C# engine on 2026-10-05,
so the two now agree on those points. One remaining difference: the plugin ignores `allergies` because the
shared persona YAMLs don't define any; add them there and re-run `gen_agents.py` to pick them up.

Not ported yet:
- Context-budget enforcer (`Telemetry/ContextBudgetEnforcer.cs`) and `context_stats.json`.
- SSE events for the live dashboard (a `SubagentStop` hook writing an event log would be the natural fit).
- Post-session evaluation (use the engine's `eval` subcommand on the session folder).
- Per-call timeouts: a persona subagent is bounded by `maxTurns: 4` instead.
