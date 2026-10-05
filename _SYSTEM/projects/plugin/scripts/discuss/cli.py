"""CLI for the agent-discuss step engine. Every command prints one JSON object.

    python3 -m discuss init BRIEF [--team T] [--mode M] [--agents a,b]
    python3 -m discuss init --topic "free text question" [--team T] [--mode M]
    python3 -m discuss resume SESSION_DIR_OR_NAME
    python3 -m discuss next SESSION_DIR
    python3 -m discuss save SESSION_DIR [--error "reason"]
    python3 -m discuss status SESSION_DIR
    python3 -m discuss list-teams
"""

import argparse
import json
import re
import sys
from pathlib import Path

from . import data, persist, steps
from .brief import Brief, BriefParseError, Question, parse_brief_text, slugify


def _print(obj, code=0):
    print(json.dumps(obj, indent=2, ensure_ascii=False))
    sys.exit(code)


def _fail(message):
    _print({"error": message}, 1)


def _resolve_brief(path_arg: str) -> Path:
    p = Path(path_arg)
    for candidate in (p, Path.cwd() / p, data.INPUT_DIR / p.name):
        if candidate.is_file():
            return candidate.resolve()
    raise FileNotFoundError(f"brief not found: {path_arg}")


def _topic_brief(topic: str) -> Brief:
    """SessionPreparer.PrepareFromArgs: split on `N.`/`N)` items, title = bold text or first sentence."""
    items = [i.strip() for i in re.split(r"^\d+[.)]\s*", topic.strip(), flags=re.M) if i.strip()] or [topic.strip()]
    questions = []
    for n, item in enumerate(items, 1):
        bold = re.match(r"\*\*(.+?)\*\*\s*(.*)", item, re.S)
        if bold:
            title, body = bold.group(1).strip(), bold.group(2).strip()
        else:
            first = re.split(r"(?<=[.?!])\s+", item, maxsplit=1)
            title, body = first[0].strip(), item
        questions.append(Question(n, title, body or title))
    return Brief(title=questions[0].title, decided=[], context="", questions=questions)


def _plan(config, mode) -> list:
    orders = config["plugin"]["orders"]
    return [
        {"question": q["number"], "title": q["title"],
         "rounds": [{"round": r, "agents": orders[f"q{q['number']}"][r]} for r in mode.groups]}
        for q in config["questions"]
    ]


def cmd_init(args):
    if args.topic:
        brief, source = _topic_brief(args.topic), "interactive"
    else:
        if not args.brief:
            _fail("Give a brief path or --topic.")
        path = _resolve_brief(args.brief)
        brief, source = parse_brief_text(path.read_text(encoding="utf-8"), path.stem), str(path)

    team_name = args.team or (data.defaults().get("paths") or {}).get("default_team", "beta-agents")
    team = data.load_team(team_name)
    mode_name = args.mode or team.default_mode
    agents = [a.strip() for a in args.agents.split(",")] if args.agents else None

    config = persist.new_session_config(brief, team=team_name, agents=agents, mode=mode_name, source=source)
    _, mode = steps.resolve_mode(config)  # validates team/mode/agents before touching disk

    sessions_root = Path(args.sessions_dir) if args.sessions_dir else data.SESSIONS_DIR
    sessions_root.mkdir(parents=True, exist_ok=True)
    session_dir = persist.create_session_dir(sessions_root, slugify(brief.title))
    for q in brief.questions:
        config["plugin"]["orders"][f"q{q.number}"] = {r: steps.speaking_order(a, team) for r, a in mode.groups.items()}
    config["state"]["status"] = "running"
    persist.write_session(session_dir, config)
    _print({
        "session_dir": str(session_dir), "title": brief.title, "team": team_name, "mode": mode_name,
        "mode_description": mode.description, "questions": len(brief.questions),
        "agents": sorted({a for g in mode.groups.values() for a in g}),
        "overlays": mode.agent_roles, "plan": _plan(config, mode),
    })


def cmd_resume(args):
    p = Path(args.session)
    session_dir = p if p.is_dir() else data.SESSIONS_DIR / args.session
    if not persist.session_path(session_dir).exists():
        _fail(f"No session.json in {session_dir}")
    config = persist.load_session(session_dir)
    expected = persist.hash_question_list(steps._questions(config))
    if config.get("question_hash") and config["question_hash"] != expected:
        _fail("Question list changed since this session started.")
    _, mode = steps.resolve_mode(config)
    done = [k for k, v in config["state"]["questions"].items() if v.get("status")]
    _print({"session_dir": str(session_dir.resolve()), "title": config["title"], "mode": config["mode"],
            "questions": len(config["questions"]), "finished_questions": len(done),
            "pending": config["plugin"].get("pending"), "plan": _plan(config, mode)})


def cmd_next(args):
    _print(steps.next_step(Path(args.session_dir)))


def cmd_save(args):
    _print(steps.save_step(Path(args.session_dir), error=args.error))


def cmd_status(args):
    config = persist.load_session(Path(args.session_dir))
    states = config["state"]["questions"]
    _print({
        "session_dir": args.session_dir, "title": config["title"], "team": config["team"], "mode": config["mode"],
        "status": config["state"].get("status"), "pending": config["plugin"].get("pending"),
        "questions": [
            {"number": q["number"], "title": q["title"], **states.get(f"q{q['number']}", {"status": "pending"})}
            for q in config["questions"]
        ],
        "warnings": config["plugin"].get("warnings", []),
    })


def cmd_list_teams(args):
    teams = []
    for name in data.list_team_names():
        team = data.load_team(name)
        teams.append({
            "team": name, "default_mode": team.default_mode,
            "agents": [{"key": k, "name": a.name, "role": a.position.role, "subagent": steps.subagent_for(k)}
                       for k, a in team.agents.items()],
            "modes": {m.name: {"description": m.description, "rounds": m.groups, "overlays": m.agent_roles}
                      for m in team.modes.values()},
        })
    _print({"teams": teams})


def main(argv=None):
    parser = argparse.ArgumentParser(prog="discuss", description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("init", help="create a session from a brief or topic")
    p.add_argument("brief", nargs="?")
    p.add_argument("--topic")
    p.add_argument("--team")
    p.add_argument("--mode")
    p.add_argument("--agents", help="comma-separated agent keys")
    p.add_argument("--sessions-dir")
    p.set_defaults(func=cmd_init)

    p = sub.add_parser("resume", help="validate and describe an existing session")
    p.add_argument("session")
    p.set_defaults(func=cmd_resume)

    p = sub.add_parser("next", help="write the next step's prompt file and describe it")
    p.add_argument("session_dir")
    p.set_defaults(func=cmd_next)

    p = sub.add_parser("save", help="consume the pending step's response file")
    p.add_argument("session_dir")
    p.add_argument("--error", help="record the step as failed with this reason")
    p.set_defaults(func=cmd_save)

    p = sub.add_parser("status", help="progress summary")
    p.add_argument("session_dir")
    p.set_defaults(func=cmd_status)

    p = sub.add_parser("list-teams", help="teams, agents and modes")
    p.set_defaults(func=cmd_list_teams)

    args = parser.parse_args(argv)
    try:
        args.func(args)
    except (steps.StepError, BriefParseError, FileNotFoundError) as e:
        _fail(str(e))


if __name__ == "__main__":
    main()
