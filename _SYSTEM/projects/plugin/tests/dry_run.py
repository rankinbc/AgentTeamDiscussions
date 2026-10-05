#!/usr/bin/env python3
"""End-to-end dry run of the step engine with canned responses (no Claude calls).

    python3 tests/dry_run.py [--sessions-dir DIR] [--brief PATH] [--mode compete]

Drives init -> (next -> canned response -> save)* -> done, injecting one failed
turn and one simulated crash (re-running `next` before `save`), then checks that
every artifact the C# engine would write exists and carries the completion marker.
"""

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

PLUGIN = Path(__file__).resolve().parents[1]
CLI = [sys.executable, str(PLUGIN / "scripts" / "discuss")]


def run(*args):
    out = subprocess.run(CLI + list(args), capture_output=True, text=True)
    try:
        return json.loads(out.stdout)
    except json.JSONDecodeError:
        raise SystemExit(f"non-JSON output from {args}:\n{out.stdout}\n{out.stderr}")


def canned_turn(step):
    return (
        f"Canned response from {step['display_name']} in round {step['round']} for Q{step['question']}. "
        "I argue for approach A because it is simpler. The other proposal ignores failure modes.\n\n"
        "## Position Summary\n"
        f"I advocate approach A ({step['agent']}). I reject approach B. Simplicity wins."
    )


def canned_doc(step):
    n = step["question"]
    return (
        "## Decisions\n\n### 1. Approach A is adopted\nBecause it is simpler.\n\n### 2. Approach B is rejected\n\n"
        "## Contested\n\nNone.\n\n## Deferred\n\n- Caching.\n\n## Open Questions\n\n- How is approach A monitored?\n\n"
        f"## Ledger\n\n### Q{n}: {step['question_title'][:60]}\n- DECIDED: Approach A is adopted\n"
        "- DECIDED: Approach B is rejected\n- OPEN: How is approach A monitored?\n"
    )


def canned_brief(_step):
    return "## Decisions Made\n1. Approach A adopted (Q1).\n\n## Risk Flags\n- none\n\n## Open Questions Requiring Human Input\n- monitoring\n\n## Recommended Reading Order\n1. Q1\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sessions-dir")
    ap.add_argument("--brief", default=str(PLUGIN.parent / "engine" / "input" / "test-brief.md"))
    ap.add_argument("--mode", default="compete")
    args = ap.parse_args()
    sessions_dir = args.sessions_dir or tempfile.mkdtemp(prefix="agent-discuss-")

    init = run("init", args.brief, "--mode", args.mode, "--sessions-dir", sessions_dir)
    assert "session_dir" in init, init
    sd = init["session_dir"]
    print(f"session: {sd}")
    print("plan:", json.dumps(init["plan"], indent=1)[:400], "...")

    steps_seen, injected_error, injected_crash = [], False, False
    for _ in range(200):
        step = run("next", sd)
        kind = step.get("type")
        if kind == "done":
            print("done:", {k: step[k] for k in ("completed", "failed_or_partial", "total", "warnings")})
            break
        assert kind in ("turn", "synthesize", "brief"), step
        steps_seen.append(kind)
        assert Path(step["prompt_file"]).exists(), "prompt file missing"

        if kind == "turn" and not injected_crash:
            # Simulated crash: `next` again must return the identical pending step.
            again = run("next", sd)
            assert again == step, "next is not idempotent while a step is pending"
            injected_crash = True

        if kind == "turn" and step["round"] == "critique" and not injected_error:
            injected_error = True
            print(run("save", sd, "--error", "simulated subagent failure"))
            continue

        text = {"turn": canned_turn, "synthesize": canned_doc, "brief": canned_brief}[kind](step)
        Path(step["response_file"]).write_text(text, encoding="utf-8")
        saved = run("save", sd)
        assert "error" not in saved, saved
    else:
        raise SystemExit("loop did not finish")

    # --- artifact checks -------------------------------------------------------
    session = json.loads((Path(sd) / "session.json").read_text())
    expected = []
    for q in session["questions"]:
        slug = (Path(sd) / "questions").glob(f"{q['number']:02d}-*.md")
        names = {p.name for p in slug}
        base = next(n for n in names if n.endswith(".md") and "-transcript" not in n and
                    not any(n.endswith(f"-{r}.md") for r in ("propose", "counter", "critique", "evaluate")))
        stem = base[:-3]
        rounds = [r["round"] for r in init["plan"][q["number"] - 1]["rounds"]]
        expected += [f"questions/{stem}.md", f"questions/{stem}-transcript.md"] + \
                    [f"questions/{stem}-{r}.md" for r in rounds]
    expected += ["decisions_ledger.md", "summary.md"]
    missing = [f for f in expected if "<!-- complete -->" not in (Path(sd) / f).read_text(encoding="utf-8")]
    assert not missing, f"missing/incomplete: {missing}"
    assert all(v["status"] == "complete" for v in session["state"]["questions"].values()), session["state"]
    assert session["state"]["session_complete"] is True
    ledger = (Path(sd) / "decisions_ledger.md").read_text()
    assert "### Q1:" in ledger and "- DECIDED: Approach A is adopted" in ledger
    print(f"steps: {len(steps_seen)} ({steps_seen.count('turn')} turns, {steps_seen.count('synthesize')} synth, "
          f"{steps_seen.count('brief')} brief); all {len(expected)} artifacts complete")
    print("OK")


if __name__ == "__main__":
    main()
