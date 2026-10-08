"""Command line: generate -> judge -> report, plus a blind packet for your own ratings."""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path

from .brief import load_engine_session, load_round_counts
from .conditions import BASELINES, run_condition
from .judge import DEFAULT_PAIRS, judge_pair
from .normalize import load_display_names, normalize_doc
from .prompts import situation
from .report import build_report, make_blind_packet

# The engine hardcodes this model in Runner/ClaudeRunner.cs; baselines must match it to be fair.
DEFAULT_MODEL = os.environ.get("ATD_BENCH_MODEL", "claude-sonnet-4-6")
HERE = Path(__file__).resolve().parent.parent


def make_llm(model: str, max_tokens: int):
    from langchain_anthropic import ChatAnthropic

    return ChatAnthropic(model=model, max_tokens=max_tokens, max_retries=6, default_request_timeout=600)


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


async def cmd_generate(args, llm_factory=make_llm) -> Path:
    from langchain_core.callbacks import UsageMetadataCallbackHandler

    session = load_engine_session(Path(args.engine_session), Path(args.brief) if args.brief else None)
    engine_root = session.path.parents[2]
    names = load_display_names(engine_root)
    rounds = load_round_counts(engine_root, session.brief.team, session.brief.mode)
    run_dir = Path(args.out) if args.out else HERE / "runs" / session.path.name
    run_json = run_dir / "run.json"
    run = json.loads(run_json.read_text(encoding="utf-8")) if run_json.exists() else {"conditions": {}}

    questions = [q for q in session.brief.questions if q.number in session.docs]
    missing = [q.number for q in session.brief.questions if q.number not in session.docs]
    if missing:
        print(f"Skipping questions with no engine design doc: {missing}", file=sys.stderr)
    session.brief.questions = questions

    for q in questions:
        _write(run_dir / "docs" / "engine" / f"{q.number:02d}.md", normalize_doc(session.docs[q.number].text, names))
    secs = [session.docs[q.number].seconds for q in questions]
    run["conditions"]["engine"] = {
        "calls": (sum(rounds.values()) + 1) * len(questions),
        "seconds": sum(s for s in secs if s) or None,
    }
    run.update({
        "brief_title": session.brief.title,
        "engine_session": session.path.name,
        "model": args.model,
        "questions": len(questions),
        "question_list": [{"number": q.number, "title": q.title, "body": q.body} for q in questions],
        "situations": {str(q.number): situation(session.brief, q, "") for q in questions},
        "round_counts": rounds,
    })

    async def one(cond: str) -> None:
        done = all((run_dir / "docs" / cond / f"{q.number:02d}.md").exists() for q in questions)
        if done and not args.force:
            print(f"[{cond}] already generated; use --force to redo")
            return
        usage = UsageMetadataCallbackHandler()
        llm = llm_factory(args.model, args.max_tokens)

        def save(r):
            _write(run_dir / "docs" / cond / f"{r.number:02d}.md", normalize_doc(r.doc, names))
            print(f"[{cond}] Q{r.number} done in {r.seconds}s")

        results = await run_condition(cond, llm, session.brief, engine_root, rounds, {"callbacks": [usage]}, save)
        totals = list(usage.usage_metadata.values())
        run["conditions"][cond] = {
            "calls": sum(r.calls for r in results),
            "seconds": round(sum(r.seconds for r in results), 1),
            "input_tokens": sum(t.get("input_tokens", 0) for t in totals),
            "output_tokens": sum(t.get("output_tokens", 0) for t in totals),
        }
        _write(run_json, json.dumps(run, indent=2))  # save each condition's stats as it finishes

    if args.force and (run_dir / "judgments.jsonl").exists():
        print("Note: judgments.jsonl was made from the old docs; delete it before judging again.", file=sys.stderr)
    # One condition failing (say, a rate limit) should not throw away the others' work.
    outcomes = await asyncio.gather(*(one(c) for c in args.conditions), return_exceptions=True)
    _write(run_json, json.dumps(run, indent=2))
    failed = [(c, o) for c, o in zip(args.conditions, outcomes) if isinstance(o, BaseException)]
    for cond, err in failed:
        print(f"[{cond}] failed: {err!r}. Run generate again to retry it.", file=sys.stderr)
    print(f"Run written to {run_dir}")
    if failed:
        raise SystemExit(1)
    return run_dir


async def cmd_judge(args, llm_factory=make_llm) -> None:
    run_dir = Path(args.run)
    run = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
    out = run_dir / "judgments.jsonl"
    seen = set()
    if out.exists():
        for ln in out.read_text(encoding="utf-8").splitlines():
            if ln.strip():
                j = json.loads(ln)
                seen.add((j["question"], j["x"], j["y"]))
    llm = llm_factory(args.judge_model, 2000)
    sem = asyncio.Semaphore(args.concurrency)
    pairs = [tuple(p.split(":")) for p in args.pairs] if args.pairs else list(DEFAULT_PAIRS)

    async def one(qn: int, x: str, y: str):
        fx, fy = run_dir / "docs" / x / f"{qn:02d}.md", run_dir / "docs" / y / f"{qn:02d}.md"
        if (qn, x, y) in seen or not (fx.exists() and fy.exists()):
            return None
        async with sem:
            j = await judge_pair(llm, run["situations"][str(qn)], x, fx.read_text(encoding="utf-8"),
                                 y, fy.read_text(encoding="utf-8"))
        j["question"] = qn
        with out.open("a", encoding="utf-8") as f:  # append as we go so a crash loses nothing
            f.write(json.dumps(j) + "\n")
        print(f"Q{qn} {x} vs {y}: {j['outcome']['overall']}")
        return j

    jobs = [(q["number"], x, y) for q in run["question_list"] for x, y in pairs]
    outcomes = await asyncio.gather(*(one(*job) for job in jobs), return_exceptions=True)
    run["judge_model"] = args.judge_model
    _write(run_dir / "run.json", json.dumps(run, indent=2))
    failed = [(job, o) for job, o in zip(jobs, outcomes) if isinstance(o, BaseException)]
    for (qn, x, y), err in failed:
        print(f"Q{qn} {x} vs {y} failed: {err!r}", file=sys.stderr)
    if failed:
        print(f"{len(failed)} comparisons failed; run judge again to retry only those.", file=sys.stderr)
        raise SystemExit(1)


def cmd_report(args) -> None:
    dirs = [Path(d) for d in args.runs]
    text = build_report(dirs)
    target = Path(args.out) if args.out else dirs[0] / "results.md"
    _write(target, text)
    print(text)
    print(f"Saved to {target}")


def cmd_blind(args) -> None:
    pairs = [tuple(p.split(":")) for p in args.pairs] if args.pairs else list(DEFAULT_PAIRS)
    blind = make_blind_packet(Path(args.run), pairs, args.seed)
    print(f"Blind packet in {blind}. Rate items in ratings.csv, then rerun `report`.")


def main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser(prog="atd_bench", description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)

    g = sub.add_parser("generate", help="run the baselines on the questions an engine session answered")
    g.add_argument("engine_session", help="path to engine/output/sessions/<id>")
    g.add_argument("--brief", help="brief file (default: found from session.json's source in engine/input)")
    g.add_argument("--out", help="run directory (default: benchmark/runs/<session id>)")
    g.add_argument("--model", default=DEFAULT_MODEL, help="defaults to the engine's model, claude-sonnet-4-6")
    g.add_argument("--conditions", nargs="+", default=list(BASELINES), choices=BASELINES)
    g.add_argument("--max-tokens", type=int, default=8000)
    g.add_argument("--force", action="store_true")

    j = sub.add_parser("judge", help="blind pairwise judging, both orders")
    j.add_argument("run")
    j.add_argument("--judge-model", default=os.environ.get("ATD_BENCH_JUDGE_MODEL", DEFAULT_MODEL))
    j.add_argument("--pairs", nargs="+", help="e.g. engine:single plain_panel:single")
    j.add_argument("--concurrency", type=int, default=4)

    r = sub.add_parser("report", help="write results.md from one or more runs")
    r.add_argument("runs", nargs="+")
    r.add_argument("--out")

    b = sub.add_parser("blind", help="make a blind A/B packet for your own ratings")
    b.add_argument("run")
    b.add_argument("--pairs", nargs="+")
    b.add_argument("--seed", type=int, default=0)

    args = p.parse_args(argv)
    if args.cmd == "generate":
        asyncio.run(cmd_generate(args))
    elif args.cmd == "judge":
        asyncio.run(cmd_judge(args))
    elif args.cmd == "report":
        cmd_report(args)
    else:
        cmd_blind(args)
