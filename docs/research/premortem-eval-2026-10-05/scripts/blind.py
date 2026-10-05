import json, random, re
from pathlib import Path
root = Path(__file__).resolve().parent
rng = random.Random(20261005)
key = {}
SCRUB = [(r"One reviewer holds that every turn", "Every turn"), (r"Another reviewer's view is that the real choice", "The real choice, though,"), (r"and that round-count is the only one", "and round-count is the only one")]
JUDGE = """You are judging two pre-mortem reports on the same planning question. You do not know how either was produced.

Context packet the reports were written from (read it; use it to check claims): {packet}
Report X: {x}
Report Y: {y}

The reader is the solo developer who wrote these plans. They will act on at most the top few findings.

Step 1. For EACH report, go through every numbered item under "What breaks" and label it:
 - VALID or INVALID (invalid = factually wrong about the packet, or doesn't follow from it)
 - NON-OBVIOUS or OBVIOUS (obvious = the author almost certainly already knows it, or it is generic software advice)
 - ACTIONABLE or NOT (would it change what the author builds or decides next?)
Step 2. List findings that appear in only one report and are VALID + NON-OBVIOUS (the unique catches).
Step 3. Rate each report's "Undecided" and "Questions for you" sections 1-5 for sharpness (5 = every item is a real decision only this author can make).
Step 4. Verdict: which report would you rather hand the author before they build? X, Y, or TIE, with confidence (low/medium/high) and a 2-3 sentence reason.

Do not reward length, polish, or tone; reward valid, non-obvious, actionable content. Penalize padding and invalid claims.

Write your judgment to {out} and end it with exactly one final line of JSON, no code fence:
{{"x_valid_nonobvious_actionable": <int>, "y_valid_nonobvious_actionable": <int>, "x_invalid": <int>, "y_invalid": <int>, "x_unique": <int>, "y_unique": <int>, "x_questions": <1-5>, "y_questions": <1-5>, "verdict": "X"|"Y"|"TIE", "confidence": "low"|"medium"|"high"}}
"""
for s in sorted(p for p in root.iterdir() if p.is_dir() and p.name.startswith("s")):
    texts = {}
    for arm in ("single", "team"):
        t = (s / f"{arm}.md").read_text()
        for pat, rep in SCRUB:
            t = re.sub(pat, rep, t)
        texts[arm] = t
    key[s.name] = {}
    for judge in ("opus", "sonnet"):
        order = ["single", "team"]; rng.shuffle(order)
        d = s / f"blind-{judge}"; d.mkdir(exist_ok=True)
        (d / "X.md").write_text(texts[order[0]]); (d / "Y.md").write_text(texts[order[1]])
        (d / "judge.prompt.md").write_text(JUDGE.format(packet=s / "packet.md", x=d / "X.md", y=d / "Y.md", out=d / "judgment.md"))
        key[s.name][judge] = {"X": order[0], "Y": order[1]}
(root / "KEY.json").write_text(json.dumps(key, indent=1))
print("blinded; key stored separately (not shown)")
