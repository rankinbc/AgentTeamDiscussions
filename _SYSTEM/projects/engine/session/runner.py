"""V1 Session Runner -- the orchestrator.

Wraps run_discussion.py's engine with:
- Session folder persistence with completion markers
- Decisions ledger (append-only, chains context across questions)
- Error handling with per-round failure cascade
- Session resume with question list hash integrity check
- Morning Brief generation at session end
- Ledger extraction with hallucination check

Usage:
    # Run a full session
    python session_runner.py brief.md

    # Run with specific mode
    python session_runner.py brief.md --mode compete

    # Run with evaluation
    python session_runner.py brief.md --eval

    # Resume a specific session
    python session_runner.py brief.md --resume 2026-03-18_0553_v1-spec-gaps

    # Specify output location
    python session_runner.py brief.md --sessions-dir ../../sessions
"""

import argparse
import asyncio
import re
import shutil
import sys
import time
from datetime import datetime
from pathlib import Path

# Add _SYSTEM to path for agentteam imports
_system_path = str(Path(__file__).resolve().parent.parent.parent.parent)
if _system_path not in sys.path:
    sys.path.insert(0, _system_path)

from agentteam.session.persistence import (
    COMPLETION_MARKER, write_with_marker, is_complete, read_without_marker,
    create_session_dir, hash_question_list, count_completed_questions,
    write_session_status, load_session_status,
)
from agentteam.session.ledger import (
    get_ledger_path, read_ledger, extract_ledger_section,
    hallucination_check, append_to_ledger,
)
from agentteam.agents.loader import load_team
from agentteam.prompts.builder import build_system_prompt
from agentteam.runner.claude import run_claude_async

# Import engine components from discussion/engine.py in same project
_engine_dir = str(Path(__file__).resolve().parent.parent)
if _engine_dir not in sys.path:
    sys.path.insert(0, _engine_dir)

from config_loader import defaults, load_prompt_raw, display_names as _load_display_names
from discussion.engine import (
    EXPERIMENT_MODES,
    AGENT_DISPLAY_NAMES,
    SYNTHESIS_SYSTEM_PROMPT,
    run_question,
    run_round,
    synthesize,
    format_transcript,
    extract_open_questions,
    TEAM_CONFIG,
    COUNTER_PROPOSE_INSTRUCTION,
    PROPOSE_ROLES,
)
from agentteam.brief.parser import parse_brief, slugify
from live.server import LiveEmitter, start_live_server

MORNING_BRIEF_SYSTEM = load_prompt_raw("prompts/morning_brief_system.md.j2")
MORNING_BRIEF_PROMPT = load_prompt_raw("prompts/morning_brief_user.md.j2")
LEDGER_EXTRACTION_SYSTEM = load_prompt_raw("prompts/ledger_extraction_system.md.j2")
LEDGER_EXTRACTION_PROMPT = load_prompt_raw("prompts/ledger_extraction.md.j2")


async def extract_ledger_from_doc(design_doc: str, q_num: int, q_title: str, timeout: int) -> str | None:
    """Separate LLM call to extract ledger entries from a design doc."""
    topic = q_title[:30].rstrip()
    prompt = LEDGER_EXTRACTION_PROMPT.replace("{N}", str(q_num)).replace("{TOPIC}", topic)
    payload = f"Design document to extract from:\n\n{design_doc[:defaults()['truncation']['doc_eval_input']]}"
    try:
        response = await run_claude_async(
            LEDGER_EXTRACTION_SYSTEM + "\n\n" + prompt,
            payload,
            timeout=timeout,
        )
        if response and ("DECIDED:" in response or "OPEN:" in response):
            lines = []
            for line in response.split("\n"):
                stripped = line.strip()
                if stripped.startswith("### Q") or stripped.startswith("- DECIDED:") or stripped.startswith("- OPEN:"):
                    lines.append(stripped)
            if lines:
                return "\n".join(lines)
    except Exception:
        pass
    return None


# -- Round-level error checking --

def check_round_health(responses: dict[str, str]) -> tuple[bool, list[str]]:
    """Check if a round's responses are usable. Returns (healthy, error_agents)."""
    error_agents = []
    for agent_key, resp in responses.items():
        if not resp or len(resp.strip()) < defaults()["health_checks"]["min_response_length"]:
            error_agents.append(agent_key)
        elif "[Claude CLI timed out" in resp or "[Error" in resp or "[Empty response" in resp:
            error_agents.append(agent_key)
    # Round is healthy if at least one agent produced usable output
    healthy = len(error_agents) < len(responses)
    return healthy, error_agents


# -- Morning Brief --

async def generate_morning_brief(
    session_dir: Path, ledger_text: str, status: dict, timeout: int
) -> str:
    """Generate the Morning Brief from the decisions ledger."""
    gaps = []
    for q_key, q_status in sorted(status.get("questions", {}).items()):
        if q_status.get("status") in ("skipped", "partial", "failed"):
            reason = q_status.get("reason", "unknown")
            gaps.append(f"- {q_key} ({q_status.get('title', '?')}): {q_status['status']} -- {reason}")

    gap_section = ""
    if gaps:
        gap_section = "\n\nSESSION GAPS (include these in your output):\n" + "\n".join(gaps)

    payload = f"## Decisions Ledger\n\n{ledger_text}\n{gap_section}"

    response = await run_claude_async(
        MORNING_BRIEF_SYSTEM + "\n\n" + MORNING_BRIEF_PROMPT,
        payload,
        timeout=timeout,
    )
    return response


# -- Main session loop --

async def run_question_with_cascade(
    question: dict,
    team,
    system_prompts: dict[str, str],
    decisions: str,
    prior_specs: str,
    open_questions: str,
    timeout: int,
    mode: dict,
    session_dir: Path,
    emitter: "LiveEmitter | None" = None,
) -> dict:
    """Run a question with per-round failure cascade.

    Returns a result dict with status, design_doc, transcript, and round details.
    """
    q_num = question["number"]
    groups = mode["groups"]
    round_labels = list(groups.keys())
    agent_roles = mode.get("agent_roles", {})

    round_responses = {}
    accumulated_discussion = ""
    round_status = {}
    questions_dir = session_dir / "questions"
    slug = slugify(question["title"])
    filename = f"{q_num:02d}-{slug}"

    for round_name in round_labels:
        agents = groups[round_name]
        agent_names = ", ".join(AGENT_DISPLAY_NAMES.get(a, a) for a in agents)
        display_name = "counter-propose" if round_name == "counter" else round_name

        role_info = ""
        for a in agents:
            if a in agent_roles:
                role_info += f" [{a}: {agent_roles[a]}]"
        print(f"  [{q_num}] Round {display_name}: {agent_names}{role_info}", flush=True)
        if emitter:
            emitter.emit("round_start", {"round": display_name, "agents": agent_names})

        round_inst = ""
        if round_name == "counter":
            round_inst = COUNTER_PROPOSE_INSTRUCTION

        def _on_start(agent_key):
            if emitter:
                emitter.emit("agent_thinking", {
                    "agent": agent_key,
                    "display_name": AGENT_DISPLAY_NAMES.get(agent_key, agent_key),
                    "round": display_name,
                    "question": q_num,
                })

        def _on_context(agent_key, system_prompt, payload):
            if emitter:
                emitter.emit("agent_context", {
                    "agent": agent_key,
                    "display_name": AGENT_DISPLAY_NAMES.get(agent_key, agent_key),
                    "round": display_name,
                    "question": q_num,
                    "system_prompt": system_prompt,
                    "payload": payload,
                })

        def _on_done(agent_key, response, elapsed):
            if emitter:
                error = bool(
                    not response or
                    "[Claude CLI timed out" in (response or "") or
                    "[Error" in (response or "")
                )
                emitter.emit("agent_response", {
                    "agent": agent_key,
                    "display_name": AGENT_DISPLAY_NAMES.get(agent_key, agent_key),
                    "response": response or "",
                    "elapsed": round(elapsed),
                    "error": error,
                })

        start = time.time()
        try:
            responses = await run_round(
                agents=agents,
                system_prompts=system_prompts,
                team=team,
                question=question,
                decisions=decisions,
                prior_rounds=accumulated_discussion,
                prior_specs=prior_specs,
                open_questions=open_questions,
                timeout=timeout,
                round_instruction=round_inst,
                agent_roles=agent_roles if round_name in ("propose", "counter") else None,
                on_agent_start=_on_start,
                on_agent_done=_on_done,
                on_agent_context=_on_context,
            )
            elapsed = time.time() - start

            healthy, error_agents = check_round_health(responses)
            if error_agents:
                for ea in error_agents:
                    print(f"    WARNING: {ea}: {responses.get(ea, '???')[:80]}", flush=True)

            if not healthy:
                raise RuntimeError(f"All agents failed in {round_name} round")

            round_responses[round_name] = responses
            round_status[round_name] = "complete"

            # Write round output to disk immediately
            round_file = questions_dir / f"{filename}-{round_name}.md"
            round_text = ""
            for key, resp in responses.items():
                name = AGENT_DISPLAY_NAMES.get(key, key)
                round_text += f"### {name}\n\n{resp}\n\n"
            write_with_marker(round_file, round_text)

            # Accumulate discussion for next round's context
            for key, resp in responses.items():
                name = AGENT_DISPLAY_NAMES.get(key, key)
                label = "COUNTER-PROPOSAL" if round_name == "counter" else round_name.upper()
                accumulated_discussion += f"[{label} - {name}]\n{resp}\n\n"

            # Drain moderator queue between rounds — inject as high-priority context
            if emitter:
                mod_msgs = []
                while True:
                    msg = emitter.pop_moderator()
                    if msg is None:
                        break
                    mod_msgs.append(msg)
                if mod_msgs:
                    directive = "\n".join(f"[MODERATOR DIRECTIVE] {m}" for m in mod_msgs)
                    accumulated_discussion += f"\n{directive}\n\n"
                    print(f"    [moderator] {len(mod_msgs)} directive(s) injected into round context", flush=True)

            print(f"    Done in {elapsed:.0f}s", flush=True)

        except Exception as e:
            elapsed = time.time() - start
            print(f"    ROUND FAILED: {round_name} -- {e} ({elapsed:.0f}s)", flush=True)
            round_status[round_name] = "failed"

            # Failure cascade rules:
            # - propose fails = skip entire question
            # - critique fails = save proposal, no evaluate, no synthesis
            # - evaluate fails = save proposal + critique, no synthesis
            if round_name in ("propose", "counter"):
                return {
                    "status": "skipped",
                    "reason": f"Propose round failed: {e}",
                    "round_status": round_status,
                    "design_doc": None,
                    "transcript": None,
                }
            else:
                # Save what we have and stop this question
                transcript = format_transcript(question, round_responses)
                transcript_path = questions_dir / f"{filename}-transcript.md"
                write_with_marker(transcript_path, transcript)
                return {
                    "status": "partial",
                    "reason": f"{round_name} round failed: {e}",
                    "round_status": round_status,
                    "design_doc": None,
                    "transcript": transcript,
                }

    # All rounds succeeded -- synthesize
    print(f"  [{q_num}] Synthesizing design doc...", flush=True)
    if emitter:
        emitter.emit("synthesis_start", {"question": q_num})
    start = time.time()
    try:
        design_doc = await synthesize(
            question, round_responses, round_labels, decisions,
            prior_specs, open_questions, timeout,
        )
        elapsed = time.time() - start

        if not design_doc or len(design_doc.strip()) < defaults()["health_checks"]["min_synthesis_length"]:
            raise RuntimeError(f"Synthesis produced empty/minimal output ({len(design_doc or '')} chars)")

        print(f"    Synthesis done in {elapsed:.0f}s", flush=True)
        round_status["synthesis"] = "complete"
        if emitter:
            emitter.emit("synthesis_done", {
                "elapsed": round(elapsed),
                "lines": len(design_doc.split("\n")),
                "preview": design_doc[:400],
                "question_num": q_num,
                "question_title": question["title"],
                "round_context": accumulated_discussion[-6000:],
                "system_prompt": SYNTHESIS_SYSTEM_PROMPT,
                "full_doc": design_doc,
            })

        transcript = format_transcript(question, round_responses)
        return {
            "status": "complete",
            "reason": None,
            "round_status": round_status,
            "design_doc": design_doc,
            "transcript": transcript,
        }

    except Exception as e:
        elapsed = time.time() - start
        print(f"    SYNTHESIS FAILED: {e} ({elapsed:.0f}s)", flush=True)
        round_status["synthesis"] = "failed"
        transcript = format_transcript(question, round_responses)
        transcript_path = questions_dir / f"{filename}-transcript.md"
        write_with_marker(transcript_path, transcript)
        return {
            "status": "partial",
            "reason": f"Synthesis failed: {e}",
            "round_status": round_status,
            "design_doc": None,
            "transcript": transcript,
        }


async def run_session(
    brief_path: Path,
    sessions_root: Path,
    mode_name: str,
    timeout: int,
    run_eval: bool,
    resume_session: str | None = None,
    session_management: bool = True,
    live: bool = False,
    output_dir: str | None = None,
    port: int = 8899,
    team_yaml: Path | None = None,
):
    """Run a discussion session.

    Args:
        team_yaml: Path to a team YAML file. Defaults to data/teams/beta-agents.yaml.
        session_management: If True (default), creates session folder, decision
            ledger, and Morning Brief. If False, writes design docs and transcripts
            to output_dir without session infrastructure.
        live: If True, starts a web dashboard on port 8899 streaming events via SSE.
        output_dir: Custom output directory. Only used when session_management=False.
    """
    decisions_text, all_questions = parse_brief(brief_path)
    mode = EXPERIMENT_MODES[mode_name]
    _team_path = team_yaml if team_yaml else TEAM_CONFIG

    # --- No-session mode: simple doc output without session infrastructure ---
    if not session_management:
        if output_dir:
            out_path = Path(output_dir)
            if not out_path.is_absolute():
                out_path = Path.cwd() / out_path
        else:
            out_path = Path(__file__).resolve().parents[4] / "output" / "design-docs"
        out_path.mkdir(parents=True, exist_ok=True)

        team = load_team(str(_team_path))
        system_prompts = {key: build_system_prompt(agent) for key, agent in team.agents.items()}

        mode_agents = set()
        for agents in mode["groups"].values():
            mode_agents.update(agents)

        print("=" * 60)
        print("Agent Discussion (no session management)")
        print(f"Brief: {brief_path.name}")
        print(f"Mode: {mode_name} -- {mode['description']}")
        print(f"Agents: {', '.join(sorted(mode_agents))}")
        print(f"Output: {out_path}")
        print("=" * 60)

        prior_specs = ""
        accumulated_open_questions = []
        total_start = time.time()

        for question in all_questions:
            q_num = question["number"]
            q_title = question["title"]
            slug = slugify(q_title)
            filename = f"{q_num:02d}-{slug}"

            print(f"\n[{q_num}/{len(all_questions)}] {q_title}", flush=True)
            q_start = time.time()

            oq_text = ""
            if accumulated_open_questions:
                oq_lines = [f"- [from Q{oq['from_q']}] {oq['text']}" for oq in accumulated_open_questions]
                oq_text = "\n".join(oq_lines)

            design_doc, transcript = await run_question(
                question=question, team=team, system_prompts=system_prompts,
                decisions=decisions_text,
                prior_specs=prior_specs[-defaults()["truncation"]["prior_specs"]:] if prior_specs else "",
                open_questions=oq_text, timeout=timeout, mode=mode,
            )
            q_elapsed = time.time() - q_start

            new_oqs = extract_open_questions(design_doc)
            for oq in new_oqs:
                accumulated_open_questions.append({"from_q": q_num, "text": oq})

            header = (
                f"# {q_title}\n\n"
                f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')} | "
                f"Question {q_num} | {q_elapsed:.0f}s | Mode: {mode_name}*\n\n"
            )
            (out_path / f"{filename}.md").write_text(header + design_doc, encoding="utf-8")
            (out_path / f"{filename}-transcript.md").write_text(transcript, encoding="utf-8")

            prior_specs += f"\n\n# {q_title}\n\n{design_doc[:defaults()['truncation']['design_doc_chain']]}"
            print(f"  Wrote {filename}.md ({q_elapsed:.0f}s)", flush=True)

        total_elapsed = time.time() - total_start
        print(f"\nDone. {len(all_questions)} docs in {total_elapsed / 60:.1f} minutes. Output: {out_path}")
        return

    # --- Live dashboard setup ---
    emitter = None
    if live:
        emitter = LiveEmitter()
        start_live_server(emitter, port=port)
        print(f"  Live dashboard: http://localhost:8899/", flush=True)

    # --- Full session mode with ledger, Morning Brief, crash recovery ---
    q_hash = hash_question_list(all_questions)
    print(f"Parsed brief: {len(all_questions)} questions (hash: {q_hash})")

    session_dir = None

    if resume_session:
        # Explicit resume
        candidate = sessions_root / resume_session
        if not candidate.exists():
            print(f"ERROR: Session not found: {candidate}")
            sys.exit(1)
        session_dir = candidate
        # Verify question list hash
        stored_hash = load_session_status(session_dir).get("question_hash")
        if stored_hash and stored_hash != q_hash:
            print(f"ERROR: Question list changed since this session started.")
            print(f"  Session hash: {stored_hash}")
            print(f"  Current hash: {q_hash}")
            print(f"  Cannot resume with a different brief. Start a new session.")
            sys.exit(1)
        completed = count_completed_questions(session_dir)
        print(f"Resuming session: {session_dir.name} ({completed}/{len(all_questions)} completed)")
    else:
        # Auto-detect incomplete sessions
        existing_sessions = sorted(sessions_root.glob(f"*_{brief_path.stem}"))
        if existing_sessions:
            latest = existing_sessions[-1]
            completed = count_completed_questions(latest)
            if completed < len(all_questions):
                # Verify hash before offering resume
                stored_hash = load_session_status(latest).get("question_hash")
                if stored_hash and stored_hash != q_hash:
                    print(f"Found incomplete session but brief has changed. Starting new session.")
                else:
                    print(f"\nFound incomplete session: {latest.name} ({completed}/{len(all_questions)} questions)")
                    if live:
                        answer = "y"
                        print("Auto-resuming (--live mode)")
                    else:
                        answer = input("Resume? [Y/n] ").strip().lower()
                    if answer != "n":
                        session_dir = latest
                        print(f"Resuming from question {completed + 1}")

    if session_dir is None:
        session_dir = create_session_dir(sessions_root, brief_path.stem)

    if emitter:
        emitter.set_session_dir(session_dir)

    # Copy config snapshot
    config_snapshot = session_dir / "config-snapshot.yaml"
    if not config_snapshot.exists():
        shutil.copy2(_team_path, config_snapshot)

    # Load team and build system prompts
    team = load_team(str(_team_path))
    system_prompts = {key: build_system_prompt(agent) for key, agent in team.agents.items()}

    mode_agents = set()
    for agents in mode["groups"].values():
        mode_agents.update(agents)

    questions_dir = session_dir / "questions"
    questions_dir.mkdir(exist_ok=True)

    # Load existing state
    status = load_session_status(session_dir)
    status["question_hash"] = q_hash
    status["mode"] = mode_name
    status["brief"] = brief_path.name
    status["team"] = str(_team_path.resolve())
    write_session_status(session_dir, status)

    ledger_text = read_ledger(session_dir)
    completed = count_completed_questions(session_dir)

    # Build prior context from completed questions
    prior_specs = ""
    accumulated_open_questions = []
    for q in all_questions[:completed]:
        slug = slugify(q["title"])
        filename = f"{q['number']:02d}-{slug}"
        doc_path = questions_dir / f"{filename}.md"
        if is_complete(doc_path):
            doc_text = read_without_marker(doc_path)
            prior_specs += f"\n\n# {q['title']}\n\n{doc_text[:defaults()['truncation']['design_doc_chain']]}"
            new_oqs = extract_open_questions(doc_text)
            for oq in new_oqs:
                accumulated_open_questions.append({"from_q": q["number"], "text": oq})

    questions_to_run = all_questions[completed:]

    print("\n" + "=" * 60)
    print("V1 Session Runner")
    print(f"Brief: {brief_path.name}")
    print(f"Mode: {mode_name} -- {mode['description']}")
    print(f"Agents: {', '.join(sorted(mode_agents))}")
    print(f"Questions: {completed} completed, {len(questions_to_run)} remaining")
    print(f"Timeout: {timeout}s per call")
    print(f"Session: {session_dir.name}")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)

    if emitter:
        emitter.emit("session_start", {
            "brief": brief_path.name,
            "mode": mode_name,
            "question_count": len(all_questions),
            "agents": sorted(mode_agents),
            "display_names": {k: AGENT_DISPLAY_NAMES.get(k, k) for k in mode_agents},
            "timeout": timeout,
        })
        # Emit rich agent profiles after roster is built
        for key, agent in team.agents.items():
            if key not in mode_agents:
                continue
            p = agent.personality
            pos = agent.position
            slop = agent.anti_slop
            emitter.emit("agent_profile", {
                "key": key,
                "name": AGENT_DISPLAY_NAMES.get(key, agent.name),
                "role": pos.role,
                "traits": {
                    "assertiveness": p.assertiveness,
                    "creativity": p.creativity_temp,
                    "risk_tolerance": p.risk_tolerance,
                    "stubbornness": p.stubbornness,
                    "bluntness": p.bluntness,
                },
                "cognitive_style": p.cognitive_style.value if hasattr(p.cognitive_style, "value") else str(p.cognitive_style),
                "emotional_baseline": p.emotional_baseline.value if hasattr(p.emotional_baseline, "value") else str(p.emotional_baseline),
                "drives": pos.drives,
                "pushback_on": pos.pushback_on,
                "intensity": pos.intensity,
                "anti_slop": {
                    "agreement_tax": slop.agreement_tax,
                    "perspective_lock": slop.perspective_enforcement,
                    "devils_advocate": slop.devils_advocate_duty,
                    "uncomfortable_quota": slop.uncomfortable_idea_quota,
                    "domain_pivot": slop.domain_pivot_trigger,
                },
                "context_lens": agent.technique.style_description.strip() if agent.technique.style_description else "",
                "technique": agent.technique.primary,
                "voice_tone": agent.voice.tone,
            })

    total_start = time.time()
    consecutive_failures = 0

    for question in questions_to_run:
        q_num = question["number"]
        q_title = question["title"]
        slug = slugify(q_title)
        filename = f"{q_num:02d}-{slug}"
        q_key = f"q{q_num}"

        # Circuit breaker: 3 consecutive failures
        if consecutive_failures >= defaults()["health_checks"]["circuit_breaker_threshold"]:
            print(f"\n  CIRCUIT BREAKER: {consecutive_failures} consecutive failures. Stopping.")
            for remaining_q in questions_to_run[questions_to_run.index(question):]:
                rk = f"q{remaining_q['number']}"
                status["questions"][rk] = {
                    "status": "skipped",
                    "title": remaining_q["title"],
                    "reason": "circuit breaker",
                }
            write_session_status(session_dir, status)
            break

        print(f"\n[{q_num}/{len(all_questions)}] {q_title}", flush=True)
        if emitter:
            emitter.emit("question_start", {"number": q_num, "total": len(all_questions), "title": q_title})
        q_start = time.time()

        # Drain moderator queue — inject as high-priority context for this question
        moderator_directives = ""
        if emitter:
            mod_msgs = []
            while True:
                msg = emitter.pop_moderator()
                if msg is None:
                    break
                mod_msgs.append(msg)
            if mod_msgs:
                moderator_directives = "\n\nMODERATOR DIRECTIVES (address these before proceeding):\n" + "\n".join(f"- {m}" for m in mod_msgs)
                print(f"  [moderator] {len(mod_msgs)} directive(s) injected", flush=True)

        # Format accumulated open questions
        oq_text = ""
        if accumulated_open_questions:
            oq_lines = [f"- [from Q{oq['from_q']}] {oq['text']}" for oq in accumulated_open_questions]
            oq_text = "\n".join(oq_lines)
        if moderator_directives:
            oq_text = moderator_directives + ("\n\n" + oq_text if oq_text else "")

        # Run with per-round cascade
        result = await run_question_with_cascade(
            question=question,
            team=team,
            system_prompts=system_prompts,
            decisions=decisions_text + "\n\n" + ledger_text if ledger_text else decisions_text,
            prior_specs=prior_specs[-defaults()["truncation"]["prior_specs"]:] if prior_specs else "",
            open_questions=oq_text,
            timeout=timeout,
            mode=mode,
            session_dir=session_dir,
            emitter=emitter,
        )

        q_elapsed = time.time() - q_start

        if result["status"] == "complete":
            design_doc = result["design_doc"]
            transcript = result["transcript"]

            # Extract open questions
            new_oqs = extract_open_questions(design_doc)
            for oq in new_oqs:
                accumulated_open_questions.append({"from_q": q_num, "text": oq})

            # Write design doc
            doc_path = questions_dir / f"{filename}.md"
            header = (
                f"# {q_title}\n\n"
                f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')} | "
                f"Question {q_num} | {q_elapsed:.0f}s | Mode: {mode_name}*\n\n"
            )
            write_with_marker(doc_path, header + design_doc)

            # Write transcript
            transcript_path = questions_dir / f"{filename}-transcript.md"
            write_with_marker(transcript_path, transcript)

            # Ledger extraction with hallucination check
            ledger_section = extract_ledger_section(design_doc)
            if not ledger_section:
                print(f"    No ledger in synthesis, extracting separately...", flush=True)
                ledger_section = await extract_ledger_from_doc(design_doc, q_num, q_title, timeout)

            if ledger_section:
                # Hallucination check
                if not hallucination_check(design_doc, ledger_section):
                    print(f"    WARNING: Ledger extraction looks suspicious (decision count mismatch), using anyway", flush=True)
                append_to_ledger(session_dir, ledger_section, q_num)
                ledger_text = read_ledger(session_dir)
            else:
                fallback_entry = f"### Q{q_num}: {q_title[:40]}\n- DECIDED: See design doc for details\n"
                append_to_ledger(session_dir, fallback_entry, q_num)
                ledger_text = read_ledger(session_dir)
                print(f"    WARNING: Ledger extraction failed, using stub", flush=True)

            prior_specs = design_doc[:defaults()["truncation"]["design_doc_chain"]]

            status["questions"][q_key] = {
                "status": "complete",
                "title": q_title,
                "elapsed_seconds": round(q_elapsed),
                "file": f"{filename}.md",
                "rounds": result["round_status"],
            }
            write_session_status(session_dir, status)

            doc_lines = len(design_doc.split("\n"))
            print(f"  Wrote {filename}.md ({doc_lines} lines) + transcript ({q_elapsed:.0f}s total)", flush=True)

            if emitter:
                ledger_count = ledger_text.count("- DECIDED:") + ledger_text.count("- OPEN:")
                emitter.emit("ledger_extracted", {"count": ledger_count, "question": q_num})
                emitter.emit("question_done", {"number": q_num, "elapsed": round(q_elapsed)})
                # Drain user-submitted questions from the live queue
                while True:
                    queued_text = emitter.pop_question()
                    if queued_text is None:
                        break
                    new_q_num = len(all_questions) + 1
                    new_q = {"number": new_q_num, "title": queued_text, "body": queued_text}
                    all_questions.append(new_q)
                    questions_to_run.append(new_q)
                    emitter.emit("question_queued", {"number": new_q_num, "title": queued_text})
                    print(f"  [queue] Added Q{new_q_num}: {queued_text[:60]}", flush=True)
            consecutive_failures = 0

        else:
            # Partial or skipped
            status["questions"][q_key] = {
                "status": result["status"],
                "title": q_title,
                "reason": result["reason"],
                "elapsed_seconds": round(q_elapsed),
                "rounds": result["round_status"],
            }
            write_session_status(session_dir, status)
            print(f"  Question {result['status']}: {result['reason']} ({q_elapsed:.0f}s)", flush=True)
            if emitter:
                emitter.emit("question_failed", {
                    "number": q_num,
                    "reason": result["reason"] or result["status"],
                })
            consecutive_failures += 1

    # Generate Morning Brief
    print(f"\nGenerating Morning Brief...", flush=True)
    if emitter:
        emitter.emit("brief_start", {})
    ledger_text = read_ledger(session_dir)

    if not ledger_text.strip():
        print("  WARNING: Ledger is empty, writing minimal brief")
        brief_content = "# Morning Brief\n\nNo decisions were extracted. Review design docs directly.\n"
    else:
        try:
            brief_content = await generate_morning_brief(session_dir, ledger_text, status, timeout)
            brief_content = (
                f"# Morning Brief: {session_dir.name}\n\n"
                f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n\n"
                f"{brief_content}"
            )
        except Exception as e:
            print(f"  Morning Brief generation failed: {e}")
            brief_content = (
                f"# Morning Brief (raw ledger -- synthesis call failed)\n\n"
                f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n\n"
                f"{ledger_text}"
            )

    write_with_marker(session_dir / "summary.md", brief_content)
    print(f"  Wrote summary.md", flush=True)
    if emitter:
        emitter.emit("brief_done", {"preview": brief_content[:400]})

    # Final status
    total_elapsed = time.time() - total_start
    completed_count = sum(1 for q in status.get("questions", {}).values() if q.get("status") == "complete")
    failed_count = sum(1 for q in status.get("questions", {}).values() if q.get("status") in ("failed", "skipped", "partial"))

    status["session_complete"] = True
    status["total_elapsed_seconds"] = round(total_elapsed)
    status["completed_questions"] = completed_count
    status["failed_questions"] = failed_count
    write_session_status(session_dir, status)

    print("\n" + "=" * 60)
    print(f"Session complete: {completed_count} succeeded, {failed_count} failed/partial")
    print(f"Total time: {total_elapsed / 60:.1f} minutes")
    print(f"Morning Brief: {session_dir / 'summary.md'}")
    print(f"Session folder: {session_dir}")
    print("=" * 60)

    if emitter:
        emitter.emit("session_done", {
            "elapsed": f"{total_elapsed / 60:.1f}m",
            "completed": completed_count,
            "total": len(all_questions),
        })

    # Optional evaluation
    if run_eval:
        print("\nRunning evaluation...")
        try:
            from evaluation.evaluator import evaluate_experiment
            evaluations, summary = await evaluate_experiment(questions_dir, timeout)
            print(f"  Overall score: {summary.get('overall', '?')}/10")
        except Exception as e:
            print(f"  Evaluation failed: {e}")


async def main():
    parser = argparse.ArgumentParser(
        description="V1 Session Runner -- run an overnight agent discussion session.",
    )
    _default_brief = Path(__file__).resolve().parents[3] / "data" / "briefs" / "v1-spec-gaps.md"
    parser.add_argument(
        "brief",
        nargs="?",
        default=str(_default_brief),
        help=f"Path to the discussion brief markdown file (default: briefs/v1-spec-gaps.md)",
    )
    parser.add_argument(
        "--sessions-dir",
        default=None,
        help="Sessions output directory (default: output/sessions/ at repo root)",
    )
    parser.add_argument(
        "--mode",
        choices=list(EXPERIMENT_MODES.keys()),
        default="compete",
        help="Agent mode (default: compete)",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=120,
        help="Timeout in seconds per LLM call (default: 120)",
    )
    parser.add_argument(
        "--eval",
        action="store_true",
        help="Run evaluation after session completes",
    )
    parser.add_argument(
        "--resume",
        default=None,
        help="Resume a specific session by folder name",
    )
    parser.add_argument(
        "--no-session",
        action="store_true",
        help="Skip session management (no ledger, no Morning Brief). "
             "Writes design docs directly to --output-dir.",
    )
    parser.add_argument(
        "--live",
        action="store_true",
        help="Enable live web dashboard on port 8899 (streams events via SSE)",
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Output directory for --no-session mode (default: output/design-docs/ at repo root)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8899,
        help="Port for --live web dashboard (default: 8899)",
    )
    parser.add_argument(
        "--team",
        default=None,
        help="Path to team YAML file (default: data/teams/beta-agents.yaml)",
    )

    args = parser.parse_args()

    brief_path = Path(args.brief)
    if not brief_path.is_absolute():
        brief_path = Path.cwd() / brief_path
    if not brief_path.exists():
        print(f"ERROR: Brief not found: {brief_path}")
        sys.exit(1)

    if args.sessions_dir:
        sessions_root = Path(args.sessions_dir)
        if not sessions_root.is_absolute():
            sessions_root = Path.cwd() / sessions_root
    else:
        sessions_root = Path(__file__).resolve().parents[4] / "output" / "sessions"

    sessions_root.mkdir(parents=True, exist_ok=True)

    if args.team:
        team_path = Path(args.team).resolve()
        if not team_path.is_file():
            print(f"ERROR: Team config not found: {team_path}")
            sys.exit(1)
    else:
        team_path = None

    await run_session(
        brief_path=brief_path,
        sessions_root=sessions_root,
        mode_name=args.mode,
        timeout=args.timeout,
        run_eval=args.eval,
        resume_session=args.resume,
        session_management=not args.no_session,
        live=args.live,
        output_dir=args.output_dir,
        port=args.port,
        team_yaml=team_path,
    )


if __name__ == "__main__":
    asyncio.run(main())
