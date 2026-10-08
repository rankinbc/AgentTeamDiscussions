"""Turn judgments (and optional human ratings) into results.md, and build the blind packet."""

from __future__ import annotations

import csv
import json
import random
import statistics
from collections import defaultdict
from math import comb
from pathlib import Path

from .judge import CRITERIA
from .normalize import word_count


def sign_test_p(wins: int, losses: int) -> float:
    """Two-sided exact binomial test that decisive outcomes are a coin flip. Ties are dropped."""
    n = wins + losses
    if n == 0:
        return 1.0
    k = min(wins, losses)
    tail = sum(comb(n, i) for i in range(k + 1)) / 2**n
    return min(1.0, 2 * tail)


def load_run(run_dir: Path) -> dict:
    run = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
    path = run_dir / "judgments.jsonl"
    run["judgments"] = [json.loads(ln) for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()] if path.exists() else []
    return run


def _tally(rows: list[tuple[str, str, str]]) -> dict[tuple[str, str], dict[str, int]]:
    """rows of (x, y, winner in {x, y, tie}) -> per pair counts."""
    t: dict[tuple[str, str], dict[str, int]] = defaultdict(lambda: {"x": 0, "y": 0, "tie": 0})
    for x, y, w in rows:
        t[(x, y)][w] += 1
    return t


def _pair_table(tally: dict[tuple[str, str], dict[str, int]]) -> list[str]:
    lines = [
        "| Comparison | n | First wins | Second wins | Ties | First's share of decisive | p (sign test) |",
        "|---|---|---|---|---|---|---|",
    ]
    for (x, y), c in tally.items():
        n = c["x"] + c["y"] + c["tie"]
        decisive = c["x"] + c["y"]
        share = f"{c['x'] / decisive:.0%}" if decisive else "n/a"
        lines.append(f"| {x} vs {y} | {n} | {c['x']} | {c['y']} | {c['tie']} | {share} | {sign_test_p(c['x'], c['y']):.3f} |")
    return lines


def _human_rows(run_dir: Path) -> list[tuple[str, str, str]]:
    key_path, ratings_path = run_dir / "blind" / "key.json", run_dir / "blind" / "ratings.csv"
    if not (key_path.exists() and ratings_path.exists()):
        return []
    key = json.loads(key_path.read_text(encoding="utf-8"))
    rows = []
    with ratings_path.open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            choice = (r.get("preferred") or "").strip().upper()
            item = key.get((r.get("item") or "").strip())
            if not item or choice not in ("A", "B", "TIE"):
                continue
            winner = "tie" if choice == "TIE" else ("x" if item[choice] == item["x"] else "y")
            rows.append((item["x"], item["y"], winner))
    return rows


def build_report(run_dirs: list[Path]) -> str:
    runs = [(d, load_run(d)) for d in run_dirs]
    judgments = [j for _, r in runs for j in r["judgments"]]
    out = ["# Engine vs baselines: results", ""]

    out.append("## Setup")
    for d, r in runs:
        out.append(f"- **{r['brief_title']}** (`{d.name}`): {r['questions']} questions; generator `{r['model']}`, "
                   f"judge `{r.get('judge_model', 'n/a')}`; engine session `{r['engine_session']}`")
    out.append("")

    if judgments:
        out += ["## LLM judge: overall preference", "",
                "Each pair was judged twice with positions swapped. A side wins only if it won in both orders.", ""]
        out += _pair_table(_tally([(j["x"], j["y"], j["outcome"]["overall"]) for j in judgments]))
        agree = sum(j["orders_agree"] for j in judgments) / len(judgments)
        out += ["", f"The two orderings agreed on the overall winner in {agree:.0%} of comparisons. "
                    "Low agreement means the judge is mostly reacting to position, not content.", ""]

        out += ["## LLM judge: by criterion", "", "Wins for the first condition / second condition / ties.", ""]
        pairs = list(dict.fromkeys((j["x"], j["y"]) for j in judgments))
        out.append("| Criterion | " + " | ".join(f"{x} vs {y}" for x, y in pairs) + " |")
        out.append("|---|" + "---|" * len(pairs))
        for c in CRITERIA:
            cells = []
            for x, y in pairs:
                t = _tally([(j["x"], j["y"], j["outcome"][c]) for j in judgments if (j["x"], j["y"]) == (x, y)])[(x, y)]
                cells.append(f"{t['x']} / {t['y']} / {t['tie']}")
            out.append(f"| {c} | " + " | ".join(cells) + " |")
        out.append("")
    else:
        out += ["No judgments yet. Run `python -m atd_bench judge <run>`.", ""]

    human = [row for d, _ in runs for row in _human_rows(d)]
    if human:
        out += ["## Your blind ratings", ""] + _pair_table(_tally(human)) + [""]

    out += ["## Cost and length", "",
            "| Condition | Median words | LLM calls | Input tokens | Output tokens | Seconds |", "|---|---|---|---|---|---|"]
    stats: dict[str, dict] = defaultdict(lambda: {"words": [], "calls": 0, "in": 0, "out": 0, "secs": 0.0})
    for d, r in runs:
        for cond, meta in r["conditions"].items():
            s = stats[cond]
            for f in sorted((d / "docs" / cond).glob("*.md")):
                s["words"].append(word_count(f.read_text(encoding="utf-8")))
            s["calls"] += meta.get("calls", 0)
            s["in"] += meta.get("input_tokens", 0)
            s["out"] += meta.get("output_tokens", 0)
            s["secs"] += meta.get("seconds") or 0
    medians = {}
    for cond, s in stats.items():
        medians[cond] = statistics.median(s["words"]) if s["words"] else 0
        tok_in = f"{s['in']:,}" if s["in"] else "n/a"
        tok_out = f"{s['out']:,}" if s["out"] else "n/a"
        out.append(f"| {cond} | {medians[cond]:.0f} | {s['calls'] or 'n/a'} | {tok_in} | {tok_out} | {s['secs']:.0f} |")
    out.append("")
    out.append("Engine token counts are not available because it calls the `claude` CLI; its call count is "
               "estimated as agents per question plus one moderator call.")

    base = [m for c, m in medians.items() if c != "engine" and m]
    if medians.get("engine") and base and medians["engine"] > 1.5 * statistics.median(base):
        out += ["", "**Length warning:** engine docs are over 1.5x longer than the baselines' median. "
                    "Judges tend to favor longer answers even when told not to, so treat engine wins with caution."]

    decisive = sum(1 for j in judgments if j["outcome"]["overall"] != "tie")
    if judgments and decisive < 20:
        out += ["", f"**Small sample:** only {decisive} decisive comparisons. Add briefs before drawing conclusions."]
    return "\n".join(out) + "\n"


def make_blind_packet(run_dir: Path, pairs: list[tuple[str, str]], seed: int = 0) -> Path:
    """Write blind/review.md (pairs as A/B in random order), blind/key.json and a ratings.csv template."""
    rng = random.Random(seed)
    run = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
    blind = run_dir / "blind"
    blind.mkdir(exist_ok=True)
    items, key, n = [], {}, 0
    for q in run["question_list"]:
        for x, y in pairs:
            fx, fy = run_dir / "docs" / x / f"{q['number']:02d}.md", run_dir / "docs" / y / f"{q['number']:02d}.md"
            if not (fx.exists() and fy.exists()):
                continue
            n += 1
            item = f"item-{n:03d}"
            a, b = (x, y) if rng.random() < 0.5 else (y, x)
            key[item] = {"x": x, "y": y, "A": a, "B": b, "question": q["number"]}
            items.append((item, q, (run_dir / "docs" / a / f"{q['number']:02d}.md").read_text(encoding="utf-8"),
                          (run_dir / "docs" / b / f"{q['number']:02d}.md").read_text(encoding="utf-8")))
    rng.shuffle(items)
    lines = ["# Blind review", "", "For each item, decide which document you would rather act on. "
             "Record A, B or tie in ratings.csv. Do not open key.json until you are done.", ""]
    for item, q, da, db in items:
        lines += [f"---\n\n# {item}: Q{q['number']}. {q['title']}", "", q["body"], "",
                  "## Document A", "", da, "", "## Document B", "", db, ""]
    (blind / "review.md").write_text("\n".join(lines), encoding="utf-8")
    (blind / "key.json").write_text(json.dumps(key, indent=2), encoding="utf-8")
    with (blind / "ratings.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["item", "preferred", "notes"])
        for item, *_ in sorted(items):
            w.writerow([item, "", ""])
    return blind
