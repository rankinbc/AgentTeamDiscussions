"""Unit tests for the step engine ports. Run with:  python3 -m unittest discover -s tests"""

import json
import sys
import tempfile
import unittest
from pathlib import Path

PLUGIN = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PLUGIN / "scripts"))

from discuss import brief, data, persist, prompts, steps  # noqa: E402

ENGINE = PLUGIN.parent / "engine"
REAL_SESSION = ENGINE / "output" / "sessions" / "2026-03-26_1839_knowledge-builder-review"


class BriefTests(unittest.TestCase):
    def test_parses_test_brief(self):
        b = brief.parse_brief_text((ENGINE / "input" / "test-brief.md").read_text(encoding="utf-8"))
        self.assertEqual(len(b.questions), 1)
        self.assertEqual(b.questions[0].number, 1)
        self.assertTrue(b.questions[0].title.startswith("How should agent responses"))
        self.assertEqual(len(b.decided), 3)
        self.assertEqual(b.context, "")

    def test_context_and_multiple_questions(self):
        text = ("# T\n\n## What's Already Decided\n\n- a\n* b\n\n## Context\n\nSome resume text.\n### sub\nmore\n\n"
                "## Open Questions\n\n1. **First** body one\nmore body\n2. **Second** body two\n")
        b = brief.parse_brief_text(text)
        self.assertEqual(b.title, "T")
        self.assertEqual(b.decided, ["a", "b"])
        self.assertEqual(b.context, "Some resume text.\n### sub\nmore")
        self.assertEqual([q.title for q in b.questions], ["First", "Second"])
        self.assertEqual(b.questions[0].body, "body one\nmore body")

    def test_missing_open_questions_raises(self):
        with self.assertRaises(brief.BriefParseError):
            brief.parse_brief_text("# T\n\n## Decided\n- x\n")

    def test_slugify(self):
        self.assertEqual(brief.slugify("Is the hierarchical folder structure the right format for AI consumption?"),
                         "is-the-hierarchical-folder-structure-the-right-format-for-ai")
        self.assertEqual(brief.slugify("???"), "untitled")


class LedgerTests(unittest.TestCase):
    def test_explicit_ledger_section(self):
        doc = "## Decisions\n\n### A\n\n## Ledger\n\n### Q3: topic\n- DECIDED: x\n- OPEN: y\n"
        self.assertEqual(persist.extract_ledger_section(doc), "## Ledger\n\n### Q3: topic\n- DECIDED: x\n- OPEN: y")

    def test_fallback_to_decision_headings(self):
        doc = "## Decisions\n\n### 1. First\ntext\n### 2. Second\n\n## Rules\n\n### Not a decision\n"
        self.assertEqual(persist.extract_ledger_section(doc), "- DECIDED: 1. First\n- DECIDED: 2. Second")

    def test_no_headings_returns_none(self):
        self.assertIsNone(persist.extract_ledger_section("## Decisions\n\n1. **Bold** item\n"))

    @unittest.skipUnless(REAL_SESSION.exists(), "sample session not present")
    def test_matches_real_engine_session(self):
        q1 = next(p for p in (REAL_SESSION / "questions").glob("01-*.md")
                  if not any(p.name.endswith(s) for s in ("-transcript.md", "-propose.md", "-critique.md", "-evaluate.md")))
        self.assertIsNone(persist.extract_ledger_section(persist.read_without_marker(q1)))
        q2 = next(p for p in (REAL_SESSION / "questions").glob("02-*.md")
                  if not any(p.name.endswith(s) for s in ("-transcript.md", "-propose.md", "-critique.md", "-evaluate.md")))
        section = persist.extract_ledger_section(persist.read_without_marker(q2))
        self.assertIn("- DECIDED: 1. The Organizer Agent Is Eliminated", section)

    def test_append_is_idempotent_and_adds_header(self):
        with tempfile.TemporaryDirectory() as d:
            sd = Path(d)
            persist.append_to_ledger(sd, "- DECIDED: x", 1, "A very long title " * 10)
            persist.append_to_ledger(sd, "- DECIDED: dup", 1, "A")
            text = persist.read_ledger(sd)
            self.assertEqual(text.count("### Q1:"), 1)
            self.assertNotIn("dup", text)
            self.assertLessEqual(len(text.splitlines()[0]), len("### Q1: ") + 60)
            self.assertTrue(persist.is_complete(persist.ledger_path(sd)))


class PromptTests(unittest.TestCase):
    def setUp(self):
        self.team = data.load_team("beta-agents")
        self.q = brief.Question(1, "Title", "Body")

    def test_position_summary_compression(self):
        acc = "[PROPOSE - A]\nlong text\n\n## Position Summary\nI advocate X.\n\n[PROPOSE - B]\nshort, no summary\n\n"
        out = prompts.compress_to_summaries(acc)
        self.assertIn("[PROPOSE - A]\nI advocate X.", out)
        self.assertIn("[PROPOSE - B]\nshort, no summary", out)
        self.assertNotIn("long text", out)

    def test_first_vs_later_speaker(self):
        agent = self.team.agents["cognitive_architect"]
        first = prompts.build_turn_prompt(agent, self.q, decisions="- d", prior_rounds="", prior_specs="",
                                          open_questions="", round_name="propose", overlay="OVERLAY")
        later = prompts.build_turn_prompt(agent, self.q, decisions="- d", prior_rounds="[PROPOSE - X]\nsum\n",
                                          prior_specs="- h", open_questions="- [from Q1] oq",
                                          round_name="critique", this_round_so_far="[X]\nresp\n\n")
        self.assertIn(prompts.FIRST_SPEAKER, first)
        self.assertNotIn("Discussion So Far", first)
        self.assertIn("=== Your Approach ===\nOVERLAY", first)
        self.assertTrue(first.rstrip().endswith("[3 sentences: what you advocate, what you reject, and why.]"))

        self.assertIn(prompts.LATER_SPEAKER, later)
        self.assertIn(prompts.ROUND_INSTRUCTIONS["critique"], later)
        order = [later.index(s) for s in ("[You are", "=== What's Already Decided", "=== Prior Design Docs",
                                          "=== Unresolved Open Questions", "=== Discussion So Far",
                                          "--- This round so far ---", "## Question:", "Your job is to BREAK",
                                          "Other agents have already spoken", "## Position Summary")]
        self.assertEqual(order, sorted(order))

    def test_low_patience_truncation(self):
        critic = self.team.agents["adversarial_critic"]  # patience 0.1
        long = "[A]\n" + "x" * 4000
        out = prompts.filter_prior_rounds(long, critic)
        self.assertTrue(out.startswith("[Earlier discussion truncated"))
        self.assertLess(len(out), 2700)

    def test_synthesis_prompt_fills_template_values(self):
        out = prompts.build_synthesis_prompt(self.q, [("propose", [("cognitive_architect", "resp")])],
                                             decisions="", prior_specs="", open_questions="")
        self.assertTrue(out.startswith("Question number: 1\nTopic tag: Title\n"))
        self.assertIn("## Round: PROPOSE\n\n### The Cognitive Architect (creativity engine designer)\n\nresp", out)
        self.assertIn("Start with '## Decisions'", out)

    def test_speaking_order_prefers_assertive(self):
        order = steps.speaking_order(["context_surgeon", "adversarial_critic"], self.team)
        # critic: 0.9*0.5 + 0.9*0.3 + 0.9*0.2 = 0.9 vs surgeon well below; jitter is ±0.1.
        self.assertEqual(order[0], "adversarial_critic")

    def test_open_questions_and_doc_compression(self):
        doc = "## Decisions\n\n### A\n\n### B\n\n## Open Questions\n\n- one\n2. two\n"
        self.assertEqual(prompts.extract_open_questions(doc), ["one", "two"])
        self.assertEqual(prompts.compress_doc_to_decisions(doc), "- A\n- B")


class PersistTests(unittest.TestCase):
    def test_question_hash_matches_csharp_serialization(self):
        qs = [brief.Question(1, "a", ""), brief.Question(2, "b", "")]
        self.assertEqual(len(persist.hash_question_list(qs)), 16)
        self.assertEqual(persist.hash_question_list(qs), persist.hash_question_list(list(qs)))

    @unittest.skipUnless(REAL_SESSION.exists(), "sample sessions not present")
    def test_hash_matches_real_sessions(self):
        checked = 0
        for session_json in REAL_SESSION.parent.glob("*/session.json"):
            cfg = json.loads(session_json.read_text(encoding="utf-8-sig"))
            if not cfg.get("question_hash"):
                continue
            qs = [brief.Question(q["number"], q["title"], q["body"]) for q in cfg["questions"]]
            self.assertEqual(persist.hash_question_list(qs), cfg["question_hash"], session_json.parent.name)
            checked += 1
        self.assertGreater(checked, 0)

    def test_marker_roundtrip(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "x.md"
            self.assertFalse(persist.is_complete(p))
            persist.write_with_marker(p, "hello")
            self.assertTrue(persist.is_complete(p))
            self.assertEqual(persist.read_without_marker(p), "hello")


if __name__ == "__main__":
    unittest.main()
