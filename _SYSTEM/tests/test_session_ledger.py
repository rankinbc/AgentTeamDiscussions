"""Tests for agentteam.session.ledger."""
import pytest
from pathlib import Path

from agentteam.session.ledger import (
    append_to_ledger,
    extract_ledger_section,
    get_ledger_path,
    hallucination_check,
    read_ledger,
)
from agentteam.session.persistence import write_with_marker

LEDGER_SECTION_Q1 = """\
### Q1: How does a round begin?

- DECIDED: The orchestrator calls begin_round after a reset.
- DECIDED: Agents receive context via the situation layer.
"""

LEDGER_SECTION_Q2 = """\
### Q2: What is the error handling strategy?

- DECIDED: Use retries with exponential backoff.
"""

DESIGN_DOC_WITH_LEDGER = """\
# Design Document

## Section

### D1 First Decision
Body text.

### D2 Second Decision
Body text.

## Ledger

### Q1: How does a round begin?

- DECIDED: Orchestrator calls begin_round.
- DECIDED: Agents receive context.
"""


# ---------------------------------------------------------------------------
# get_ledger_path
# ---------------------------------------------------------------------------

class TestGetLedgerPath:
    def test_returns_correct_filename(self, tmp_path):
        assert get_ledger_path(tmp_path) == tmp_path / "decisions_ledger.md"


# ---------------------------------------------------------------------------
# read_ledger
# ---------------------------------------------------------------------------

class TestReadLedger:
    def test_returns_empty_string_when_file_missing(self, tmp_path):
        assert read_ledger(tmp_path) == ""

    def test_returns_content_without_marker(self, tmp_path):
        write_with_marker(get_ledger_path(tmp_path), "ledger content")
        assert read_ledger(tmp_path) == "ledger content"


# ---------------------------------------------------------------------------
# extract_ledger_section
# ---------------------------------------------------------------------------

class TestExtractLedgerSection:
    def test_extracts_section_from_design_doc(self):
        result = extract_ledger_section(DESIGN_DOC_WITH_LEDGER)
        assert result is not None
        assert "DECIDED:" in result

    def test_returns_none_when_no_ledger_header(self):
        assert extract_ledger_section("# No ledger section here\n\nSome content.") is None

    def test_extracted_section_starts_with_ledger_header(self):
        result = extract_ledger_section(DESIGN_DOC_WITH_LEDGER)
        assert result.startswith("## Ledger")


# ---------------------------------------------------------------------------
# hallucination_check
# ---------------------------------------------------------------------------

class TestHallucinationCheck:
    def test_balanced_ratio_returns_true(self):
        # 2 doc sections, 2 ledger decisions -> ratio 1.0 (within 0.2–4.0)
        doc = "### D1 One\n\n### D2 Two\n"
        ledger = "- DECIDED: A\n- DECIDED: B\n"
        assert hallucination_check(doc, ledger) is True

    def test_too_many_ledger_decisions_returns_false(self):
        # 1 doc section, 5 ledger decisions -> ratio 5.0 > 4.0
        doc = "### D1 Only\n"
        ledger = "- DECIDED: A\n- DECIDED: B\n- DECIDED: C\n- DECIDED: D\n- DECIDED: E\n"
        assert hallucination_check(doc, ledger) is False

    def test_too_few_ledger_decisions_returns_false(self):
        # 10 doc sections, 0 ledger decisions -> ratio 0 < 0.2
        doc = "\n".join(f"### D{i} Section\n" for i in range(10))
        ledger = ""  # no DECIDED entries
        assert hallucination_check(doc, ledger) is False

    def test_no_doc_decisions_returns_true(self):
        """Empty doc should not be flagged (edge case guard)."""
        assert hallucination_check("", "- DECIDED: A\n") is True

    def test_custom_ratio_bounds_respected(self):
        # 1 doc section, 2 ledger decisions -> ratio 2.0
        # With ratio_max=1.5, this should fail
        doc = "### D1 Only\n"
        ledger = "- DECIDED: A\n- DECIDED: B\n"
        assert hallucination_check(doc, ledger, ratio_max=1.5) is False


# ---------------------------------------------------------------------------
# append_to_ledger
# ---------------------------------------------------------------------------

class TestAppendToLedger:
    def test_creates_ledger_file_on_first_append(self, tmp_path):
        append_to_ledger(tmp_path, LEDGER_SECTION_Q1, q_num=1)
        assert get_ledger_path(tmp_path).exists()

    def test_appended_content_readable(self, tmp_path):
        append_to_ledger(tmp_path, LEDGER_SECTION_Q1, q_num=1)
        content = read_ledger(tmp_path)
        assert "### Q1:" in content
        assert "DECIDED:" in content

    def test_duplicate_question_not_appended_twice(self, tmp_path):
        append_to_ledger(tmp_path, LEDGER_SECTION_Q1, q_num=1)
        append_to_ledger(tmp_path, LEDGER_SECTION_Q1, q_num=1)
        assert read_ledger(tmp_path).count("### Q1:") == 1

    def test_multiple_questions_all_present(self, tmp_path):
        append_to_ledger(tmp_path, LEDGER_SECTION_Q1, q_num=1)
        append_to_ledger(tmp_path, LEDGER_SECTION_Q2, q_num=2)
        content = read_ledger(tmp_path)
        assert "### Q1:" in content
        assert "### Q2:" in content

    def test_file_marked_complete_after_append(self, tmp_path):
        from agentteam.session.persistence import is_complete
        append_to_ledger(tmp_path, LEDGER_SECTION_Q1, q_num=1)
        assert is_complete(get_ledger_path(tmp_path))
