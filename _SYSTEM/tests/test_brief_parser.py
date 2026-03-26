"""Tests for agentteam.brief.parser."""
import pytest
from pathlib import Path

from agentteam.brief.parser import Brief, BriefParseError, parse_brief, parse_brief_structured, slugify

VALID_BRIEF = """\
## What's Already Decided

- Use Python 3.11+
- Sessions stored as markdown

## Open Questions

1. **How does a round begin?** After a reset, the orchestrator sets context.

2. **What is the error handling strategy?** Handle timeout, network, invalid.
"""

NO_QUESTIONS_SECTION = """\
## What's Already Decided

- Something decided

## Notes

No questions section here.
"""


# ---------------------------------------------------------------------------
# parse_brief
# ---------------------------------------------------------------------------

class TestParseBrief:
    def test_returns_tuple_of_decisions_and_questions(self, tmp_path):
        p = tmp_path / "brief.md"
        p.write_text(VALID_BRIEF, encoding="utf-8")
        result = parse_brief(p)
        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_decisions_text_includes_expected_content(self, tmp_path):
        p = tmp_path / "brief.md"
        p.write_text(VALID_BRIEF, encoding="utf-8")
        decisions, _ = parse_brief(p)
        assert "Python 3.11+" in decisions

    def test_question_count(self, sample_brief):
        _, questions = parse_brief(sample_brief)
        assert len(questions) == 2

    def test_question_fields_present(self, sample_brief):
        _, questions = parse_brief(sample_brief)
        q = questions[0]
        assert "number" in q
        assert "title" in q
        assert "body" in q

    def test_question_number_is_int(self, sample_brief):
        _, questions = parse_brief(sample_brief)
        assert questions[0]["number"] == 1
        assert questions[1]["number"] == 2

    def test_question_title_stripped(self, sample_brief):
        _, questions = parse_brief(sample_brief)
        assert questions[0]["title"] == "How does a round begin?"

    def test_question_body_contains_context(self, sample_brief):
        _, questions = parse_brief(sample_brief)
        assert "orchestrator" in questions[0]["body"]

    def test_missing_questions_section_raises_brief_parse_error(self, tmp_path):
        p = tmp_path / "brief.md"
        p.write_text(NO_QUESTIONS_SECTION, encoding="utf-8")
        with pytest.raises(BriefParseError, match="No 'Open Questions'"):
            parse_brief(p)

    def test_empty_questions_list_raises_brief_parse_error(self, tmp_path):
        p = tmp_path / "brief.md"
        p.write_text("## Open Questions\n\nNo numbered items here.\n", encoding="utf-8")
        with pytest.raises(BriefParseError, match="No questions parsed"):
            parse_brief(p)

    def test_brief_parse_error_is_a_value_error(self, tmp_path):
        """BriefParseError must be a ValueError so callers can catch ValueError."""
        p = tmp_path / "brief.md"
        p.write_text("nothing useful", encoding="utf-8")
        with pytest.raises(ValueError):
            parse_brief(p)

    def test_no_decisions_section_returns_empty_string(self, tmp_path):
        brief = "## Open Questions\n\n1. **Q1** Some body text.\n"
        p = tmp_path / "brief.md"
        p.write_text(brief, encoding="utf-8")
        decisions, _ = parse_brief(p)
        assert decisions == ""

    def test_single_question_parsed(self, tmp_path):
        brief = "## Open Questions\n\n1. **One Question** The only question.\n"
        p = tmp_path / "brief.md"
        p.write_text(brief, encoding="utf-8")
        _, questions = parse_brief(p)
        assert len(questions) == 1
        assert questions[0]["title"] == "One Question"


# ---------------------------------------------------------------------------
# slugify
# ---------------------------------------------------------------------------

class TestSlugify:
    @pytest.mark.parametrize("title,expected", [
        ("How does a round begin?", "how-does-a-round-begin"),
        ("What is Error Handling?", "what-is-error-handling"),
        ("Simple", "simple"),
        ("multi  space  title", "multi-space-title"),
    ])
    def test_basic_slugification(self, title, expected):
        assert slugify(title) == expected

    def test_default_max_length_is_60(self):
        long_title = "a " * 100
        assert len(slugify(long_title)) <= 60

    def test_custom_max_length_respected(self):
        assert len(slugify("hello world something long", max_length=5)) <= 5

    def test_strips_leading_and_trailing_hyphens(self):
        slug = slugify("!!! Question ???")
        assert not slug.startswith("-")
        assert not slug.endswith("-")

    def test_output_is_lowercase(self):
        assert slugify("UPPER CASE TITLE") == slugify("upper case title")

    def test_special_chars_become_hyphens(self):
        slug = slugify("one/two:three")
        assert "/" not in slug
        assert ":" not in slug


# ---------------------------------------------------------------------------
# Brief dataclass
# ---------------------------------------------------------------------------

FULL_BRIEF = """\
# My Product

A tool for doing things efficiently.

## What's Already Decided

- Use Python 3.11+
- Sessions are stored as markdown

## Open Questions

1. **How does a round begin?** After a reset, the orchestrator sets context.

2. **What is the error handling strategy?** Handle timeout and network errors.
"""

BRIEF_NO_H1 = """\
Some description without a heading.

## What's Already Decided

- Constraint one
- Constraint two

## Open Questions

1. **Only question** The body here.
"""

BRIEF_NO_DECIDED = """\
# Product Title

## Open Questions

1. **Question one** Body text.
"""


class TestBrief:
    def test_brief_has_product_description_field(self):
        b = Brief(product_description="desc", constraints=[], questions=[])
        assert b.product_description == "desc"

    def test_brief_has_constraints_field(self):
        b = Brief(product_description="", constraints=["one", "two"], questions=[])
        assert b.constraints == ["one", "two"]

    def test_brief_has_questions_field(self):
        q = {"number": 1, "title": "T", "body": "B"}
        b = Brief(product_description="", constraints=[], questions=[q])
        assert b.questions == [q]

    def test_brief_default_constraints_is_empty_list(self):
        b = Brief(product_description="x")
        assert b.constraints == []

    def test_brief_default_questions_is_empty_list(self):
        b = Brief(product_description="x")
        assert b.questions == []


# ---------------------------------------------------------------------------
# parse_brief_structured
# ---------------------------------------------------------------------------


class TestParseBriefStructured:
    def test_returns_brief_instance(self, tmp_path):
        p = tmp_path / "brief.md"
        p.write_text(FULL_BRIEF, encoding="utf-8")
        result = parse_brief_structured(p)
        assert isinstance(result, Brief)

    def test_product_description_includes_h1_title(self, tmp_path):
        p = tmp_path / "brief.md"
        p.write_text(FULL_BRIEF, encoding="utf-8")
        brief = parse_brief_structured(p)
        assert "My Product" in brief.product_description

    def test_product_description_includes_body_text(self, tmp_path):
        p = tmp_path / "brief.md"
        p.write_text(FULL_BRIEF, encoding="utf-8")
        brief = parse_brief_structured(p)
        assert "doing things efficiently" in brief.product_description

    def test_product_description_no_h1(self, tmp_path):
        p = tmp_path / "brief.md"
        p.write_text(BRIEF_NO_H1, encoding="utf-8")
        brief = parse_brief_structured(p)
        assert "Some description without a heading" in brief.product_description

    def test_constraints_parsed_as_list(self, tmp_path):
        p = tmp_path / "brief.md"
        p.write_text(FULL_BRIEF, encoding="utf-8")
        brief = parse_brief_structured(p)
        assert isinstance(brief.constraints, list)
        assert len(brief.constraints) == 2

    def test_constraints_strip_dash_prefix(self, tmp_path):
        p = tmp_path / "brief.md"
        p.write_text(FULL_BRIEF, encoding="utf-8")
        brief = parse_brief_structured(p)
        for c in brief.constraints:
            assert not c.startswith("- ")
            assert not c.startswith("* ")

    def test_constraints_content(self, tmp_path):
        p = tmp_path / "brief.md"
        p.write_text(FULL_BRIEF, encoding="utf-8")
        brief = parse_brief_structured(p)
        assert "Use Python 3.11+" in brief.constraints
        assert "Sessions are stored as markdown" in brief.constraints

    def test_no_decided_section_gives_empty_constraints(self, tmp_path):
        p = tmp_path / "brief.md"
        p.write_text(BRIEF_NO_DECIDED, encoding="utf-8")
        brief = parse_brief_structured(p)
        assert brief.constraints == []

    def test_questions_have_correct_keys(self, tmp_path):
        p = tmp_path / "brief.md"
        p.write_text(FULL_BRIEF, encoding="utf-8")
        brief = parse_brief_structured(p)
        for q in brief.questions:
            assert "number" in q
            assert "title" in q
            assert "body" in q

    def test_question_number_is_int(self, tmp_path):
        p = tmp_path / "brief.md"
        p.write_text(FULL_BRIEF, encoding="utf-8")
        brief = parse_brief_structured(p)
        assert brief.questions[0]["number"] == 1
        assert brief.questions[1]["number"] == 2

    def test_question_count(self, tmp_path):
        p = tmp_path / "brief.md"
        p.write_text(FULL_BRIEF, encoding="utf-8")
        brief = parse_brief_structured(p)
        assert len(brief.questions) == 2

    def test_question_title_stripped(self, tmp_path):
        p = tmp_path / "brief.md"
        p.write_text(FULL_BRIEF, encoding="utf-8")
        brief = parse_brief_structured(p)
        assert brief.questions[0]["title"] == "How does a round begin?"

    def test_missing_open_questions_raises(self, tmp_path):
        p = tmp_path / "brief.md"
        p.write_text("## What's Already Decided\n- X\n", encoding="utf-8")
        with pytest.raises(BriefParseError, match="No 'Open Questions'"):
            parse_brief_structured(p)

    def test_empty_questions_raises(self, tmp_path):
        p = tmp_path / "brief.md"
        p.write_text("## Open Questions\n\nNo numbered items.\n", encoding="utf-8")
        with pytest.raises(BriefParseError, match="No questions parsed"):
            parse_brief_structured(p)

    def test_uses_sample_brief_fixture(self, sample_brief):
        """Ensures parse_brief_structured works with conftest sample_brief (no H1)."""
        brief = parse_brief_structured(sample_brief)
        assert isinstance(brief, Brief)
        assert len(brief.questions) == 2
        assert any("Python 3.11+" in c for c in brief.constraints)
