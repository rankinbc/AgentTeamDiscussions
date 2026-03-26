"""Crash-safe file I/O with completion markers."""
import hashlib, json
from datetime import datetime
from pathlib import Path

COMPLETION_MARKER = "\n<!-- complete -->\n"

def write_with_marker(path: Path, content: str):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content); f.flush(); f.write(COMPLETION_MARKER); f.flush()

def is_complete(path: Path) -> bool:
    if not path.exists(): return False
    try: return "<!-- complete -->" in path.read_text(encoding="utf-8")
    except Exception: return False

def read_without_marker(path: Path) -> str:
    return path.read_text(encoding="utf-8").replace(COMPLETION_MARKER, "").replace("<!-- complete -->", "").strip()

def create_session_dir(sessions_root: Path, brief_name: str) -> Path:
    name = f"{datetime.now().strftime('%Y-%m-%d_%H%M')}_{brief_name}"
    session_dir = sessions_root / name
    session_dir.mkdir(parents=True, exist_ok=True)
    (session_dir / "questions").mkdir(exist_ok=True)
    return session_dir

def hash_question_list(questions: list[dict]) -> str:
    content = json.dumps([{"n": q["number"], "t": q["title"]} for q in questions], sort_keys=True)
    return hashlib.sha256(content.encode()).hexdigest()[:16]

def count_completed_questions(session_dir: Path) -> int:
    questions_dir = session_dir / "questions"
    if not questions_dir.exists(): return 0
    return sum(1 for f in sorted(questions_dir.glob("*.md")) if not f.name.endswith("-transcript.md") and is_complete(f))

def write_session_status(session_dir: Path, status: dict):
    path = session_dir / "session_status.json"
    with open(path, "w", encoding="utf-8") as f: json.dump(status, f, indent=2); f.flush()

def load_session_status(session_dir: Path) -> dict:
    path = session_dir / "session_status.json"
    if path.exists():
        try: return json.loads(path.read_text(encoding="utf-8"))
        except Exception: pass
    return {"questions": {}}
