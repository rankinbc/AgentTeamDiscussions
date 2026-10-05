"""Offline tests: fake chat models, the real engine session checked into output/sessions."""

from __future__ import annotations

import asyncio
import csv
import json
import shutil
from argparse import Namespace
from pathlib import Path
from typing import Any

import pytest
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from langchain_core.runnables import RunnableLambda

from atd_bench import cli, judge, normalize, report
from atd_bench.brief import load_engine_session, load_round_counts, parse_brief_text
from atd_bench.conditions import extract_final_doc, run_condition

ENGINE = Path(__file__).resolve().parents[2] / "engine"
SESSION = ENGINE / "output" / "sessions" / "2026-03-26_1839_knowledge-builder-review"


class FakeChat(BaseChatModel):
    """Returns a design doc (or a panel turn) and records every prompt it was sent."""

    prompts: list[str] = []
    judge_choice: str = "A"

    @property
    def _llm_type(self) -> str:
        return "fake"

    def _generate(self, messages, stop=None, run_manager=None, **kw: Any) -> ChatResult:
        text = "\n".join(str(m.content) for m in messages)
        self.prompts.append(text)
        n = len(self.prompts)
        if "<deliberation>" in text:
            body = f"<deliberation>scratch {n}</deliberation>\n## Decisions\n- Choice {n}\n\n## Open Questions\n- None"
        elif "Your task (" in text:
            body = f"Panel turn {n}. Panelist 2 thinks otherwise."
        else:
            body = f"## Decisions\n- Choice {n} per Panelist 1\n\n## Open Questions\n- None\n\n## Ledger\n- DECIDED: x"
        msg = AIMessage(body, usage_metadata={"input_tokens": 10, "output_tokens": 5, "total_tokens": 15},
                        response_metadata={"model_name": "fake"})
        return ChatResult(generations=[ChatGeneration(message=msg)])

    def with_structured_output(self, schema, **kw):
        def run(_msgs):
            c = self.judge_choice
            return schema(reasoning="fake", risk_discovery=c, decision_quality=c, actionability=c,
                          alternatives=c, signal_to_noise=c, overall=c, confidence="low")
        return RunnableLambda(run)


def test_parse_brief_matches_engine_rules():
    text = "# T\n\nIntro.\n\n## What's Already Decided\n\n- A\n- B\n\n## Context\n\nResume here.\n\n" \
           "## Open Questions\n\n1. **First** body one.\n2. **Second** body two.\n"
    b = parse_brief_text(text)
    assert (b.title, b.description, b.decided, b.context) == ("T", "Intro.", ["A", "B"], "Resume here.")
    assert [(q.number, q.title, q.body) for q in b.questions] == [(1, "First", "body one."), (2, "Second", "body two.")]


def test_load_real_engine_session():
    s = load_engine_session(SESSION)
    assert len(s.brief.questions) == 7 and set(s.docs) == set(range(1, 8))
    assert s.brief.description.startswith("A system for building")
    assert s.docs[2].seconds == 221
    assert load_round_counts(ENGINE, s.brief.team, s.brief.mode) == {"propose": 2, "critique": 2, "evaluate": 2}


def test_normalize_strips_tells():
    names = normalize.load_display_names(ENGINE)
    raw = "﻿# Title\n\n*Generated: 2026-03-26 | Q2 | 221s | Mode: compete*\n\n## Decisions\n" \
          "The Adversarial Critic and Priya agreed; Panelist 4 did not. The Architect's plan lost.\n" \
          "An orchestrator service stays.\n\n## Ledger\n- DECIDED: x\n"
    out = normalize.normalize_doc(raw, names)
    assert out.startswith("## Decisions")
    assert "Ledger" not in out and "Priya" not in out and "Adversarial" not in out and "Panelist" not in out
    assert "Architect" not in out and "a reviewer's plan lost" in out
    assert "An orchestrator service stays." in out  # ordinary lowercase words are untouched


def test_extract_final_doc():
    assert extract_final_doc("<deliberation>x</deliberation>\n## Decisions\n- a") == "## Decisions\n- a"
    assert extract_final_doc("noise\n## Decisions\n- a") == "## Decisions\n- a"


def test_conditions_call_counts_and_chain_prior_decisions():
    s = load_engine_session(SESSION)
    s.brief.questions = s.brief.questions[:2]
    rounds = {"propose": 2, "critique": 2, "evaluate": 2}
    for cond, per_q in (("single", 1), ("self_critique", 1), ("plain_panel", 7)):
        llm = FakeChat(prompts=[])
        results = asyncio.run(run_condition(cond, llm, s.brief, ENGINE, rounds))
        assert len(llm.prompts) == 2 * per_q
        assert [r.calls for r in results] == [per_q, per_q]
        assert results[0].doc.startswith("## Decisions")
        assert "Decisions from earlier questions" in llm.prompts[per_q]  # Q2 sees Q1's decisions
    # The panel's moderator gets the engine's real synthesis prompt and all six turns.
    assert "You are a reporter documenting the outcome" in llm.prompts[6]
    assert llm.prompts[6].count("### Panelist") == 6


def test_combine_requires_both_orders():
    a = {c: "A" for c in judge.CRITERIA}
    b = {c: "B" for c in judge.CRITERIA}
    assert judge.combine(a, b)["overall"] == "x"    # x won as A, then won again as B
    assert judge.combine(a, a)["overall"] == "tie"  # always picked position A: pure position bias


def test_sign_test():
    assert report.sign_test_p(0, 0) == 1.0
    assert report.sign_test_p(5, 5) == 1.0
    assert report.sign_test_p(10, 0) == pytest.approx(2 / 1024)


def test_end_to_end(tmp_path):
    out = tmp_path / "run"
    factory = lambda model, max_tokens: FakeChat(prompts=[])
    args = Namespace(engine_session=str(SESSION), brief=None, out=str(out), model="fake",
                     conditions=["single", "self_critique", "plain_panel"], max_tokens=100, force=False)
    asyncio.run(cli.cmd_generate(args, factory))
    for cond in ("engine", "single", "self_critique", "plain_panel"):
        assert len(list((out / "docs" / cond).glob("*.md"))) == 7
    assert "Ledger" not in (out / "docs" / "engine" / "02.md").read_text(encoding="utf-8")
    meta = json.loads((out / "run.json").read_text())["conditions"]
    assert meta["plain_panel"]["calls"] == 49 and meta["plain_panel"]["input_tokens"] == 490

    asyncio.run(cli.cmd_judge(Namespace(run=str(out), judge_model="fake", pairs=None, concurrency=2), factory))
    rows = [json.loads(ln) for ln in (out / "judgments.jsonl").read_text().splitlines()]
    assert len(rows) == 7 * len(judge.DEFAULT_PAIRS)
    assert all(r["outcome"]["overall"] == "tie" and not r["orders_agree"] for r in rows)

    blind = report.make_blind_packet(out, [("engine", "single")])
    key = json.loads((blind / "key.json").read_text())
    with (blind / "ratings.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["item", "preferred", "notes"])
        for item, k in key.items():  # always prefer the engine's doc
            w.writerow([item, "A" if k["A"] == "engine" else "B", ""])
    text = report.build_report([out])
    assert "| engine vs single | 7 | 0 | 0 | 7 |" in text
    assert "## Your blind ratings" in text and "| engine vs single | 7 | 7 | 0 | 0 | 100% | 0.016 |" in text
