# Benchmark: does the engine beat simpler ways of asking Claude?

The engine's claim is that structured personas and anti-convergence rules produce better
design decisions than asking one model directly. This harness tests that claim on the same
questions the engine already answered, and isolates what each part of the engine contributes.

## The conditions

| Condition | What it is | Calls per question |
|---|---|---|
| `engine` | The design docs from an engine session, read from `engine/output/sessions/<id>` | 6 agents + moderator |
| `single` | One Claude call | 1 |
| `self_critique` | One Claude call that must propose two approaches, attack both and pick one before writing | 1 |
| `plain_panel` | The engine's round structure, round instructions and real moderator prompt (`synthesis.md.j2`), but with generic panelists instead of personas. Built with LangGraph | same as engine |

Every condition gets the same project description, decided constraints, `## Context` and
question, answers the questions in order, and carries its own earlier decisions forward, as
the engine does with its ledger. Baselines are asked for the same sections as the engine's
moderator (Decisions, Contested, Deferred, Open Questions).

## The comparisons

| Pair | Question it answers |
|---|---|
| engine vs single | Is the engine better than just asking? |
| engine vs self_critique | Is it better than one well-written prompt? |
| engine vs plain_panel | Do the **personas** add anything beyond the round structure? |
| plain_panel vs single | Does the **multi-call structure** add anything on its own? |

## How judging stays fair

- **Blind:** the engine's title, `*Generated*` line and `## Ledger` appendix are removed, and
  agent names and persona titles ("Priya", "The Adversarial Critic", "the Architect") are
  replaced with "a reviewer" in every document.
- **Pairwise, both orders:** each pair is judged twice with positions swapped. A side wins only
  if it wins in both orders; otherwise it is a tie. The report shows how often the orders agreed.
- **Substance over length:** the judge is told that length and item count earn nothing and that
  invented problems count against a document. The report still prints median word counts and
  warns when the engine's docs are much longer.
- **Significance:** win counts come with an exact sign-test p-value, and the report warns when
  there are fewer than 20 decisive comparisons.
- **Your own eyes:** `blind` builds an A/B packet with the labels hidden so you can rate pairs
  yourself. Your ratings appear in the report next to the judge's.

## Running it

Needs Python 3.11+ and an Anthropic API key (the baselines call the API through
`langchain-anthropic`; the engine itself still uses the `claude` CLI).

```bash
cd _SYSTEM/projects/benchmark
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
export ANTHROPIC_API_KEY=...                         # Windows: $env:ANTHROPIC_API_KEY="..."
```

**1. Pick an engine session.** The engine hardcodes `claude-sonnet-4-6` in
`Runner/ClaudeRunner.cs`, and the baselines default to the same model, so the existing sessions
in `engine/output/sessions/` are directly comparable. Four of them are complete
(`2026-03-26_1114_5-question-session`, both `10-question-session`s and
`2026-03-26_1839_knowledge-builder-review`), which gives 32 questions to start with. The three
question sessions were created from the dashboard with no brief, so the baselines receive the
same thing the engine did: just the questions. To test more briefs, run the engine on them
first (`dotnet run --project src/EngineStandalone -- input/<brief>.md`). If you change the
engine's model, set `ATD_BENCH_MODEL` to match.

**2. Generate, judge, report:**

```bash
python -m atd_bench generate ../engine/output/sessions/<session-id>
python -m atd_bench judge runs/<session-id>
python -m atd_bench report runs/<session-id>
```

**3. (Optional) rate them yourself:**

```bash
python -m atd_bench blind runs/<session-id>
# read runs/<session-id>/blind/review.md, fill in blind/ratings.csv (A, B or tie)
python -m atd_bench report runs/<session-id>
```

**4. Pool several briefs** for a sample large enough to mean something (aim for 20+ decisive
comparisons per pair):

```bash
python -m atd_bench report runs/* --out results.md
```

Useful flags: `generate --conditions single self_critique` to skip the panel,
`judge --judge-model <id>` (or `ATD_BENCH_JUDGE_MODEL`) to use a different judge model,
`judge --pairs engine:single`. Both `generate` and `judge` skip work that is already on disk,
so an interrupted run can simply be started again.

## Rough cost

For a 7-question brief: `single` and `self_critique` make 7 calls each, `plain_panel` 49, and
judging makes 2 calls per pair per question (56 with the default four pairs). The report lists
the token counts each baseline actually used.

## Limits

- One model judges docs written by the same model family. Self-preference applies equally to
  every condition, but a second judge model (`--judge-model`) is a useful check.
- Anonymizing removes names, not style. The engine and the plain panel may still read like
  "a group decided this". Your blind ratings are the check on that.
- The engine passes its full ledger and prior design docs forward; the baselines pass forward
  only their earlier Decisions sections.

## Files

```
atd_bench/
  brief.py       load an engine session and its brief (port of BriefParser.cs rules)
  normalize.py   strip headers and ledger, anonymize agent names
  prompts.py     baseline prompts, engine round instructions, judge prompt
  conditions.py  single and self_critique (LCEL chains), plain_panel (LangGraph)
  judge.py       blind pairwise judge with structured output
  report.py      results.md, sign test, blind packet
  cli.py         generate / judge / report / blind
tests/           offline tests with fake chat models (pytest)
```
