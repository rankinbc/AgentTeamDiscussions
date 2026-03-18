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
import hashlib
import json
import re
import shutil
import sys
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from claude_runner import run_claude_async
from interact import load_team
from prompt_builder import build_system_prompt, build_perspective_reminder
from run_discussion import (
    EXPERIMENT_MODES,
    AGENT_DISPLAY_NAMES,
    SYNTHESIS_SYSTEM_PROMPT,
    parse_brief,
    run_round,
    synthesize,
    format_transcript,
    extract_open_questions,
    slugify,
    TEAM_CONFIG,
    COUNTER_PROPOSE_INSTRUCTION,
    PROPOSE_ROLES,
)

COMPLETION_MARKER = "\n<!-- complete -->\n"

MORNING_BRIEF_SYSTEM = (
    "You are summarizing an overnight design session. You must ONLY use "
    "the information provided in the ledger below. Do NOT reference any other knowledge about "
    "the project. If the ledger contains stub entries like 'See design doc for details', "
    "report that the ledger extraction failed and recommend reading the design docs directly. "
    "Do NOT hallucinate or invent content."
)

MORNING_BRIEF_PROMPT = """INPUT: A decisions ledger containing extracted decisions and open questions
from each discussion round.

OUTPUT: Morning Brief in exactly this format:

## Decisions Made
Numbered list. One line each. Group by question topic.

## Risk Flags
Decisions where critic concerns were acknowledged but not fully resolved.
State the concern, not just the decision.

## Open Questions Requiring Human Input
Unresolved items that block downstream work or require judgment calls.

## Recommended Reading Order
Which design docs to read first if the reader wants to go deeper.
Order by importance to near-term decisions, not by session order.

No prose paragraphs. No executive summary. Every line must be scannable.
If any questions failed or produced partial output, add a Session Gaps section."""

LEDGER_EXTRACTION_SYSTEM = (
    "You are a decision extractor. Your ENTIRE response must be a markdown ledger block "
    "starting with ### and containing ONLY lines starting with '- DECIDED:' or '- OPEN:'. "
    "No other text. No explanation. No headers other than the ### line. No numbered lists. "
    "No markdown sections. Just the ledger block."
)

LEDGER_EXTRACTION_PROMPT = """### Q{N}: {TOPIC}
- DECIDED: [fill in each concrete decision from the document, one per line, max 50 words, stated as a constraint not rationale]
- OPEN: [fill in each unresolved question, one per line]

Read the design document below. Replace the bracketed placeholders above with real entries. Output ONLY the completed ledger block starting with ###. Nothing else."""


# -- File utilities --

def write_with_marker(path: Path, content: str):
    """Write content to file with completion marker. Flush before marker."""
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
        f.flush()
        f.write(COMPLETION_MARKER)
        f.flush()


def is_complete(path: Path) -> bool:
    """Check if a file has the completion marker."""
    if not path.exists():
        return False
    try:
        text = path.read_text(encoding="utf-8")
        return "<!-- complete -->" in text
    except Exception:
        return False


def read_without_marker(path: Path) -> str:
    """Read a file, stripping the completion marker."""
    text = path.read_text(encoding="utf-8")
    return text.replace(COMPLETION_MARKER, "").replace("<!-- complete -->", "").strip()


# -- Session directory utilities --

def create_session_dir(sessions_root: Path, brief_name: str) -> Path:
    """Create a timestamped session directory."""
    ts = datetime.now().strftime("%Y-%m-%d_%H%M")
    name = f"{ts}_{brief_name}"
    session_dir = sessions_root / name
    session_dir.mkdir(parents=True, exist_ok=True)
    (session_dir / "questions").mkdir(exist_ok=True)
    return session_dir


def hash_question_list(questions: list[dict]) -> str:
    """Deterministic hash of the question list for resume integrity."""
    content = json.dumps([{"n": q["number"], "t": q["title"]} for q in questions], sort_keys=True)
    return hashlib.sha256(content.encode()).hexdigest()[:16]


def count_completed_questions(session_dir: Path) -> int:
    """Count completed questions by scanning for complete design docs."""
    questions_dir = session_dir / "questions"
    if not questions_dir.exists():
        return 0
    count = 0
    for f in sorted(questions_dir.glob("*.md")):
        if f.name.endswith("-transcript.md"):
            continue
        if is_complete(f):
            count += 1
    return count


# -- Ledger utilities --

def get_ledger_path(session_dir: Path) -> Path:
    return session_dir / "decisions_ledger.md"


def read_ledger(session_dir: Path) -> str:
    """Read the decisions ledger, or return empty string."""
    path = get_ledger_path(session_dir)
    if path.exists():
        return read_without_marker(path)
    return ""


def extract_ledger_section(design_doc: str) -> str | None:
    """Extract the ## Ledger section from a design doc."""
    match = re.search(r"## Ledger\s*\n(.*?)(?=\n## |\Z)", design_doc, re.DOTALL)
    if match:
        return match.group(0).strip()
    return None


async def extract_ledger_from_doc(design_doc: str, q_num: int, q_title: str, timeout: int) -> str | None:
    """Separate LLM call to extract ledger entries from a design doc."""
    topic = q_title[:30].rstrip()
    prompt = LEDGER_EXTRACTION_PROMPT.replace("{N}", str(q_num)).replace("{TOPIC}", topic)
    payload = f"Design document to extract from:\n\n{design_doc[:10000]}"
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


def hallucination_check(design_doc: str, ledger_section: str) -> bool:
    """Compare decision count in doc vs ledger. Return True if plausible."""
    # Count decision-like headers in the design doc (### D or ### Decision or numbered items under ## Decisions)
    doc_decisions = len(re.findall(r"(?:^### D\d|^### [A-Z]|\d+\.\s+\*\*)", design_doc, re.MULTILINE))
    if doc_decisions == 0:
        # Fallback: count second-level sections
        doc_decisions = len(re.findall(r"^### ", design_doc, re.MULTILINE))

    ledger_decisions = ledger_section.count("- DECIDED:")

    if doc_decisions == 0:
        return True  # Can't check, assume OK

    ratio = ledger_decisions / doc_decisions
    # Flag if ledger has 4x more decisions than doc sections (hallucination)
    # or less than 20% of doc decisions (missed too many)
    if ratio > 4.0 or ratio < 0.2:
        return False
    return True


def append_to_ledger(session_dir: Path, ledger_section: str, q_num: int):
    """Append a ledger section to the decisions ledger, guarding against dupes."""
    path = get_ledger_path(session_dir)
    existing = ""
    if path.exists():
        existing = path.read_text(encoding="utf-8").replace(COMPLETION_MARKER, "").replace("<!-- complete -->", "")

    if f"### Q{q_num}:" in existing:
        return

    new_content = existing.rstrip() + "\n\n" + ledger_section + "\n"
    write_with_marker(path, new_content)


# -- Status utilities --

def write_session_status(session_dir: Path, status: dict):
    """Write session status JSON."""
    path = session_dir / "session_status.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(status, f, indent=2)
        f.flush()


def load_session_status(session_dir: Path) -> dict:
    """Load session status or return empty."""
    path = session_dir / "session_status.json"
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"questions": {}}


# -- Round-level error checking --

def check_round_health(responses: dict[str, str]) -> tuple[bool, list[str]]:
    """Check if a round's responses are usable. Returns (healthy, error_agents)."""
    error_agents = []
    for agent_key, resp in responses.items():
        if not resp or len(resp.strip()) < 20:
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

        round_inst = ""
        if round_name == "counter":
            round_inst = COUNTER_PROPOSE_INSTRUCTION

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
    start = time.time()
    try:
        design_doc = await synthesize(
            question, round_responses, round_labels, decisions,
            prior_specs, open_questions, timeout,
        )
        elapsed = time.time() - start

        if not design_doc or len(design_doc.strip()) < 50:
            raise RuntimeError(f"Synthesis produced empty/minimal output ({len(design_doc or '')} chars)")

        print(f"    Synthesis done in {elapsed:.0f}s", flush=True)
        round_status["synthesis"] = "complete"

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
):
    """Run a full V1 session."""
    decisions_text, all_questions = parse_brief(brief_path)
    q_hash = hash_question_list(all_questions)
    print(f"Parsed brief: {len(all_questions)} questions (hash: {q_hash})")

    mode = EXPERIMENT_MODES[mode_name]

    # Session resolution: explicit resume, auto-detect, or new
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
                    answer = input("Resume? [Y/n] ").strip().lower()
                    if answer != "n":
                        session_dir = latest
                        print(f"Resuming from question {completed + 1}")

    if session_dir is None:
        session_dir = create_session_dir(sessions_root, brief_path.stem)

    # Copy config snapshot
    config_snapshot = session_dir / "config-snapshot.yaml"
    if not config_snapshot.exists():
        shutil.copy2(TEAM_CONFIG, config_snapshot)

    # Load team and build system prompts
    team = load_team(str(TEAM_CONFIG))
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
            prior_specs = doc_text[:3000]
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

    total_start = time.time()
    consecutive_failures = 0

    for question in questions_to_run:
        q_num = question["number"]
        q_title = question["title"]
        slug = slugify(q_title)
        filename = f"{q_num:02d}-{slug}"
        q_key = f"q{q_num}"

        # Circuit breaker: 3 consecutive failures
        if consecutive_failures >= 3:
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
        q_start = time.time()

        # Format accumulated open questions
        oq_text = ""
        if accumulated_open_questions:
            oq_lines = [f"- [from Q{oq['from_q']}] {oq['text']}" for oq in accumulated_open_questions]
            oq_text = "\n".join(oq_lines)

        # Run with per-round cascade
        result = await run_question_with_cascade(
            question=question,
            team=team,
            system_prompts=system_prompts,
            decisions=decisions_text + "\n\n" + ledger_text if ledger_text else decisions_text,
            prior_specs=prior_specs[-6000:] if prior_specs else "",
            open_questions=oq_text,
            timeout=timeout,
            mode=mode,
            session_dir=session_dir,
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

            prior_specs = design_doc[:3000]

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
            consecutive_failures += 1

    # Generate Morning Brief
    print(f"\nGenerating Morning Brief...", flush=True)
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

    # Optional evaluation
    if run_eval:
        print("\nRunning evaluation...")
        try:
            from evaluate_experiment import evaluate_experiment
            evaluations, summary = await evaluate_experiment(questions_dir, timeout)
            print(f"  Overall score: {summary.get('overall', '?')}/10")
        except Exception as e:
            print(f"  Evaluation failed: {e}")


async def main():
    parser = argparse.ArgumentParser(
        description="V1 Session Runner -- run an overnight agent discussion session.",
    )
    parser.add_argument("brief", help="Path to the discussion brief markdown file")
    parser.add_argument(
        "--sessions-dir",
        default=None,
        help="Sessions output directory (default: ../../sessions relative to script)",
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
        sessions_root = Path(__file__).resolve().parent.parent.parent / "sessions"

    sessions_root.mkdir(parents=True, exist_ok=True)

    await run_session(
        brief_path=brief_path,
        sessions_root=sessions_root,
        mode_name=args.mode,
        timeout=args.timeout,
        run_eval=args.eval,
        resume_session=args.resume,
    )


if __name__ == "__main__":
    asyncio.run(main())
