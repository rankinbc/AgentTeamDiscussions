"""Step planner — decides what happens next in a session, from disk state alone.

`next_step` walks the questions/rounds/agents in order and returns the first
thing that is not finished, writing that step's prompt file. `save_step`
consumes the response the subagent wrote. Both are idempotent, so a crash at
any point resumes by calling `next_step` again. Cascade rules follow
SessionRunner.RunQuestionWithCascadeAsync.
"""

import json
import random
from datetime import datetime
from pathlib import Path

from . import data, persist, prompts
from .brief import Question, slugify

ERROR_MARKERS = ("[Claude CLI timed out", "[Error", "[Empty response")
PLUGIN_NAME = "agent-discuss"


class StepError(Exception):
    pass


# --- helpers -------------------------------------------------------------------

def _questions(config: dict) -> list:
    return [Question(q["number"], q["title"], q["body"]) for q in config["questions"]]


def _filename(q: Question) -> str:
    return f"{q.number:02d}-{slugify(q.title)}"


def resolve_mode(config: dict):
    team = data.load_team(config["team"])
    active = set(team.agents)
    if config.get("agents"):
        active = {a for a in config["agents"] if a in team.agents}
        if not active:
            raise StepError("None of the selected agents exist in this team.")
    mode = team.modes.get(config["mode"])
    if mode is None:
        raise StepError(f"Unknown mode '{config['mode']}' for team '{config['team']}'. "
                        f"Available: {', '.join(team.modes)}")
    mode = data.filter_mode(mode, active)
    if not mode.groups:
        raise StepError("No rounds have agents after filtering. Select more agents or a different mode.")
    return team, mode


def speaking_order(agent_keys: list, team) -> list:
    """RoundRunner.ComputeSpeakingOrder: assertiveness*0.5 + intensity*0.3 + stubbornness*0.2 ± 0.1."""
    scored = []
    for key in agent_keys:
        agent = team.agents.get(key)
        if agent is None:
            score = 0.5
        else:
            p = agent.personality
            score = p.assertiveness * 0.5 + agent.position.intensity * 0.3 + p.stubbornness * 0.2
        scored.append((key, score + random.random() * 0.2 - 0.1))
    return [k for k, _ in sorted(scored, key=lambda x: x[1], reverse=True)]


def subagent_names() -> dict:
    manifest = data.PLUGIN_ROOT / "agents" / "manifest.json"
    if manifest.exists():
        with open(manifest, encoding="utf-8") as f:
            return json.load(f)
    return {}


def subagent_for(key: str) -> str:
    return f"{PLUGIN_NAME}:{subagent_names().get(key, key.replace('_', '-'))}"


def healthy(text: str, min_len: int = 20) -> bool:
    return bool(text) and len(text.strip()) >= min_len and not any(m in text for m in ERROR_MARKERS)


def _work(session_dir: Path, q: Question, round_name: str, key: str, kind: str) -> Path:
    return session_dir / "work" / f"q{q.number:02d}-{round_name}-{key}.{kind}.md"


def _decisions_text(config: dict, session_dir: Path) -> str:
    decided = "\n".join(f"- {d}" for d in config.get("decided") or [])
    ledger = persist.read_ledger(session_dir)
    if decided and ledger:
        return decided + "\n\n" + ledger
    return decided or ledger


def _prior_context(config: dict, session_dir: Path, upto: Question) -> tuple:
    """Prior-doc headings from the most recent complete doc, open questions from all of them."""
    prior_specs = ""
    open_qs = []
    for q in _questions(config):
        if q.number >= upto.number:
            break
        doc_path = session_dir / "questions" / f"{_filename(q)}.md"
        if not persist.is_complete(doc_path):
            continue
        doc = persist.read_without_marker(doc_path)
        prior_specs = prompts.compress_doc_to_decisions(doc)
        open_qs += [f"- [from Q{q.number}] {t}" for t in prompts.extract_open_questions(doc)]
    limit = int((data.defaults().get("truncation") or {}).get("prior_specs", 6000))
    if len(prior_specs) > limit:
        prior_specs = prior_specs[-limit:]
    return prior_specs, "\n".join(open_qs)


def _transcript(q: Question, rounds: list) -> str:
    out = [f"# Transcript: {q.title}", "", f"*Generated: {persist.now_stamp()}*", ""]
    for round_name, responses in rounds:
        out += [f"## Round: {prompts.round_label(round_name)}", ""]
        for key, resp in responses:
            out += [f"### {data.display_name(key)}", "", resp, ""]
    return "\n".join(out) + "\n"


def _round_file_text(responses: list) -> str:
    return "".join(f"### {data.display_name(key)}\n\n{resp}\n\n" for key, resp in responses)


def _elapsed(config: dict, qkey: str) -> int:
    started = (config["plugin"].get("question_started") or {}).get(qkey)
    if not started:
        return 0
    return int((datetime.now() - datetime.fromisoformat(started)).total_seconds())


def _mark_question(config, session_dir, q, status, *, reason=None, rounds=None, file=None):
    qkey = f"q{q.number}"
    entry = {"status": status, "title": q.title, "elapsed_seconds": _elapsed(config, qkey)}
    if reason:
        entry["reason"] = reason
    if file:
        entry["file"] = file
    if rounds:
        entry["rounds"] = rounds
    config["state"]["questions"][qkey] = entry
    config["plugin"]["pending"] = None
    persist.write_session(session_dir, config)


# --- next ------------------------------------------------------------------------

def next_step(session_dir: Path) -> dict:
    config = persist.load_session(session_dir)
    pending = config["plugin"].get("pending")
    if pending:
        return pending

    team, mode = resolve_mode(config)
    threshold = int((data.defaults().get("health_checks") or {}).get("circuit_breaker_threshold", 3))
    questions = _questions(config)
    states = config["state"]["questions"]
    consecutive = 0

    for q in questions:
        qkey = f"q{q.number}"
        st = states.get(qkey)
        if st and st.get("status") in ("complete", "skipped", "partial", "failed"):
            consecutive = 0 if st["status"] == "complete" else consecutive + 1
            continue

        if consecutive >= threshold:
            for rest in questions:
                if rest.number >= q.number and f"q{rest.number}" not in states:
                    states[f"q{rest.number}"] = {"status": "skipped", "title": rest.title, "reason": "circuit breaker"}
            config["plugin"]["circuit_breaker"] = True
            persist.write_session(session_dir, config)
            break

        step = _next_for_question(config, session_dir, team, mode, q)
        if step is not None:
            return step
        # Question just got finalized from disk state; re-plan from scratch.
        return next_step(session_dir)

    return _next_after_questions(config, session_dir)


def _next_for_question(config, session_dir, team, mode, q: Question):
    qkey = f"q{q.number}"
    plugin = config["plugin"]
    plugin.setdefault("question_started", {}).setdefault(qkey, datetime.now().isoformat())
    if not plugin.get("started"):  # init writes the key as null, so setdefault would keep it
        plugin["started"] = datetime.now().isoformat()
    orders = plugin.setdefault("orders", {}).setdefault(qkey, {})

    decisions = _decisions_text(config, session_dir)
    prior_specs, open_qs = _prior_context(config, session_dir, q)
    collected = []
    round_status = {}

    for round_name, agents in mode.groups.items():
        if round_name not in orders:
            orders[round_name] = speaking_order(agents, team)
        responses = []
        for key in orders[round_name]:
            resp_path = _work(session_dir, q, round_name, key, "response")
            if persist.is_complete(resp_path):
                responses.append((key, persist.read_without_marker(resp_path)))
                continue

            this_round = "".join(f"[{data.display_name(k)}]\n{r}\n\n" for k, r in responses)
            prompt = prompts.build_turn_prompt(
                team.agents[key], q,
                decisions=decisions,
                prior_rounds=prompts.compress_to_summaries(prompts.accumulate_discussion(collected)),
                prior_specs=prior_specs,
                open_questions=open_qs,
                round_name=round_name,
                overlay=data.overlay_instruction(mode.agent_roles[key]) if key in mode.agent_roles else "",
                this_round_so_far=this_round,
                context=config.get("context") or "",
            )
            prompt_path = _work(session_dir, q, round_name, key, "prompt")
            prompt_path.parent.mkdir(exist_ok=True)
            prompt_path.write_text(prompt, encoding="utf-8")
            step = {
                "type": "turn",
                "question": q.number,
                "question_title": q.title,
                "round": round_name,
                "position": len(responses) + 1,
                "of": len(orders[round_name]),
                "agent": key,
                "display_name": data.display_name(key),
                "subagent": subagent_for(key),
                "prompt_file": str(prompt_path),
                "response_file": str(resp_path),
            }
            plugin["pending"] = step
            persist.write_session(session_dir, config)
            return step

        # Round finished: health check + persist round file.
        ok = [r for r in responses if healthy(r[1])]
        if not ok:
            round_status[round_name] = "failed"
            reason = f"{'Propose' if round_name in ('propose', 'counter') else round_name} round failed: All agents failed in {round_name} round"
            if round_name in ("propose", "counter"):
                _mark_question(config, session_dir, q, "skipped", reason=reason, rounds=round_status)
            else:
                persist.write_with_marker(session_dir / "questions" / f"{_filename(q)}-transcript.md",
                                          _transcript(q, collected))
                _mark_question(config, session_dir, q, "partial", reason=reason, rounds=round_status)
            return None
        round_status[round_name] = "complete"
        round_file = session_dir / "questions" / f"{_filename(q)}-{round_name}.md"
        if not persist.is_complete(round_file):
            persist.write_with_marker(round_file, _round_file_text(responses))
        collected.append((round_name, responses))

    doc_path = session_dir / "questions" / f"{_filename(q)}.md"
    if persist.is_complete(doc_path):
        # Crash between doc write and state update: finish bookkeeping from the doc on disk.
        finalize_question(config, session_dir, q, collected, round_status, persist.read_without_marker(doc_path),
                          already_written=True)
        return None

    prompt = prompts.build_synthesis_prompt(
        q, collected, decisions=decisions, prior_specs=prior_specs, open_questions=open_qs,
        context=config.get("context") or "",
        max_ledger_words=int((data.defaults().get("synthesis") or {}).get("max_ledger_words", 50)),
    )
    prompt_path = session_dir / "work" / f"q{q.number:02d}-synthesis.prompt.md"
    prompt_path.write_text(prompt, encoding="utf-8")
    step = {
        "type": "synthesize",
        "question": q.number,
        "question_title": q.title,
        "subagent": f"{PLUGIN_NAME}:synthesizer",
        "prompt_file": str(prompt_path),
        "response_file": str(session_dir / "work" / f"q{q.number:02d}-synthesis.response.md"),
        "round_status": round_status,
    }
    plugin["pending"] = step
    persist.write_session(session_dir, config)
    return step


def _next_after_questions(config, session_dir: Path) -> dict:
    summary = session_dir / "summary.md"
    if persist.is_complete(summary):
        return finalize_session(config, session_dir)

    ledger = persist.read_ledger(session_dir)
    if not ledger.strip():
        persist.write_with_marker(summary, "# Morning Brief\n\nNo decisions were extracted. Review design docs directly.\n")
        return finalize_session(config, session_dir)

    prompt_path = session_dir / "work" / "morning-brief.prompt.md"
    prompt_path.write_text(prompts.build_brief_prompt(ledger, config["state"]["questions"]), encoding="utf-8")
    step = {
        "type": "brief",
        "subagent": f"{PLUGIN_NAME}:morning-brief",
        "prompt_file": str(prompt_path),
        "response_file": str(session_dir / "work" / "morning-brief.response.md"),
    }
    config["plugin"]["pending"] = step
    persist.write_session(session_dir, config)
    return step


# --- save ------------------------------------------------------------------------

def save_step(session_dir: Path, error: str = None) -> dict:
    config = persist.load_session(session_dir)
    step = config["plugin"].get("pending")
    if not step:
        raise StepError("No pending step. Run `next` first.")

    resp_path = Path(step["response_file"])
    text = ""
    if resp_path.exists():
        text = resp_path.read_text(encoding="utf-8").replace(persist.MARKER_TEXT, "").strip()
    if error:
        text = f"[Error: {error}]"
    elif not text:
        text = "[Empty response from subagent]"

    if step["type"] == "turn":
        persist.write_with_marker(resp_path, text)
        config["plugin"]["pending"] = None
        persist.write_session(session_dir, config)
        return {"saved": "turn", "agent": step["agent"], "round": step["round"],
                "question": step["question"], "healthy": healthy(text), "chars": len(text)}

    questions = {q.number: q for q in _questions(config)}
    if step["type"] == "synthesize":
        q = questions[step["question"]]
        team, mode = resolve_mode(config)
        collected = _collected_rounds(session_dir, config, mode, q)
        min_len = int((data.defaults().get("health_checks") or {}).get("min_synthesis_length", 50))
        if error or len(text) < min_len:
            round_status = dict(step.get("round_status") or {}, synthesis="failed")
            persist.write_with_marker(session_dir / "questions" / f"{_filename(q)}-transcript.md",
                                      _transcript(q, collected))
            _mark_question(config, session_dir, q, "partial",
                           reason=f"Synthesis failed: {error or f'produced empty/minimal output ({len(text)} chars)'}",
                           rounds=round_status)
            return {"saved": "synthesize", "question": q.number, "status": "partial"}
        round_status = dict(step.get("round_status") or {}, synthesis="complete")
        finalize_question(config, session_dir, q, collected, round_status, text)
        return {"saved": "synthesize", "question": q.number, "status": "complete",
                "file": f"{_filename(q)}.md"}

    if step["type"] == "brief":
        folder = session_dir.name
        if error or not healthy(text):
            content = f"# Morning Brief (raw ledger)\n\n*Generated: {persist.now_stamp()}*\n\n{persist.read_ledger(session_dir)}"
        else:
            content = f"# Morning Brief: {folder}\n\n*Generated: {persist.now_stamp()}*\n\n{text}"
        persist.write_with_marker(session_dir / "summary.md", content)
        config["plugin"]["pending"] = None
        persist.write_session(session_dir, config)
        return finalize_session(config, session_dir)

    raise StepError(f"Unknown pending step type: {step['type']}")


def _collected_rounds(session_dir, config, mode, q: Question) -> list:
    orders = config["plugin"]["orders"].get(f"q{q.number}", {})
    collected = []
    for round_name, agents in mode.groups.items():
        responses = []
        for key in orders.get(round_name, agents):
            p = _work(session_dir, q, round_name, key, "response")
            if persist.is_complete(p):
                responses.append((key, persist.read_without_marker(p)))
        if responses:
            collected.append((round_name, responses))
    return collected


def finalize_question(config, session_dir, q: Question, collected, round_status, design_doc, already_written=False):
    """Design doc + transcript + ledger + state, as SessionRunner does after synthesis."""
    qdir = session_dir / "questions"
    filename = _filename(q)
    if not already_written:
        header = (f"# {q.title}\n\n*Generated: {persist.now_stamp()} | Q{q.number} | "
                  f"{_elapsed(config, f'q{q.number}')}s | Mode: {config['mode']}*\n\n")
        persist.write_with_marker(qdir / f"{filename}.md", header + design_doc)
    if not persist.is_complete(qdir / f"{filename}-transcript.md"):
        persist.write_with_marker(qdir / f"{filename}-transcript.md", _transcript(q, collected))

    section = persist.extract_ledger_section(design_doc) or persist.fallback_ledger_entry(q.number, q.title)
    hc = data.defaults().get("health_checks") or {}
    suspicious = not persist.hallucination_check(
        design_doc, section, hc.get("hallucination_ratio_max", 4.0), hc.get("hallucination_ratio_min", 0.2))
    persist.append_to_ledger(session_dir, section, q.number, q.title)

    rounds = dict(round_status or {})
    rounds.setdefault("synthesis", "complete")
    _mark_question(config, session_dir, q, "complete", rounds=rounds, file=f"{filename}.md")
    if suspicious:
        config["plugin"].setdefault("warnings", []).append(f"q{q.number}: ledger extraction looks suspicious")
        persist.write_session(session_dir, config)


def finalize_session(config, session_dir: Path) -> dict:
    states = config["state"]["questions"]
    completed = sum(1 for s in states.values() if s.get("status") == "complete")
    failed = sum(1 for s in states.values() if s.get("status") in ("failed", "skipped", "partial"))
    started = config["plugin"].get("started")
    total = int((datetime.now() - datetime.fromisoformat(started)).total_seconds()) if started else 0
    config["state"].update({
        "status": "complete", "session_complete": True, "total_elapsed_seconds": total,
        "completed_questions": completed, "failed_questions": failed,
    })
    config["plugin"]["pending"] = None
    persist.write_session(session_dir, config)
    return {
        "type": "done", "session_dir": str(session_dir), "summary": str(session_dir / "summary.md"),
        "completed": completed, "failed_or_partial": failed, "total": len(config["questions"]),
        "elapsed_seconds": total, "circuit_breaker": bool(config["plugin"].get("circuit_breaker")),
        "warnings": config["plugin"].get("warnings", []),
    }
