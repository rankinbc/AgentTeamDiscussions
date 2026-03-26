"""Tests for agentteam.session.persistence."""
import re

import pytest
from pathlib import Path

from agentteam.session.persistence import (
    COMPLETION_MARKER,
    count_completed_questions,
    create_session_dir,
    hash_question_list,
    is_complete,
    load_session_status,
    read_without_marker,
    write_session_status,
    write_with_marker,
)


# ---------------------------------------------------------------------------
# Completion marker I/O
# ---------------------------------------------------------------------------

class TestWriteWithMarker:
    def test_file_contains_completion_marker(self, tmp_path):
        p = tmp_path / "out.md"
        write_with_marker(p, "hello")
        assert "<!-- complete -->" in p.read_text(encoding="utf-8")

    def test_file_contains_content(self, tmp_path):
        p = tmp_path / "out.md"
        write_with_marker(p, "my content")
        assert "my content" in p.read_text(encoding="utf-8")

    def test_overwrites_existing_file(self, tmp_path):
        p = tmp_path / "out.md"
        write_with_marker(p, "first")
        write_with_marker(p, "second")
        assert "first" not in p.read_text(encoding="utf-8")
        assert "second" in p.read_text(encoding="utf-8")


class TestIsComplete:
    def test_true_after_write_with_marker(self, tmp_path):
        p = tmp_path / "f.md"
        write_with_marker(p, "content")
        assert is_complete(p) is True

    def test_false_for_missing_file(self, tmp_path):
        assert is_complete(tmp_path / "nonexistent.md") is False

    def test_false_for_file_without_marker(self, tmp_path):
        p = tmp_path / "partial.md"
        p.write_text("content without marker", encoding="utf-8")
        assert is_complete(p) is False


class TestReadWithoutMarker:
    def test_strips_completion_marker(self, tmp_path):
        p = tmp_path / "f.md"
        write_with_marker(p, "my content")
        result = read_without_marker(p)
        assert result == "my content"
        assert "<!-- complete -->" not in result

    def test_strips_inline_marker_variant(self, tmp_path):
        p = tmp_path / "f.md"
        p.write_text("data<!-- complete -->", encoding="utf-8")
        assert read_without_marker(p) == "data"

    def test_strips_both_marker_variants(self, tmp_path):
        p = tmp_path / "f.md"
        p.write_text("data" + COMPLETION_MARKER, encoding="utf-8")
        assert read_without_marker(p) == "data"


# ---------------------------------------------------------------------------
# Session directory creation
# ---------------------------------------------------------------------------

class TestCreateSessionDir:
    def test_directory_exists_after_creation(self, tmp_path):
        d = create_session_dir(tmp_path, "my-brief")
        assert d.is_dir()

    def test_questions_subdirectory_created(self, tmp_path):
        d = create_session_dir(tmp_path, "my-brief")
        assert (d / "questions").is_dir()

    def test_name_includes_brief_slug(self, tmp_path):
        d = create_session_dir(tmp_path, "my-brief")
        assert "my-brief" in d.name

    def test_name_includes_date_timestamp(self, tmp_path):
        d = create_session_dir(tmp_path, "brief")
        assert re.search(r"\d{4}-\d{2}-\d{2}", d.name), f"No date in: {d.name}"

    def test_idempotent_when_called_twice_at_same_minute(self, tmp_path):
        # exist_ok=True means no error if called again in the same minute
        d1 = create_session_dir(tmp_path, "brief")
        d2 = create_session_dir(tmp_path, "brief")
        assert d1 == d2


# ---------------------------------------------------------------------------
# Question list hashing
# ---------------------------------------------------------------------------

class TestHashQuestionList:
    def test_same_input_same_hash(self):
        questions = [{"number": 1, "title": "Q1", "body": "body"}]
        assert hash_question_list(questions) == hash_question_list(questions)

    def test_different_titles_different_hash(self):
        q1 = [{"number": 1, "title": "Q1", "body": "body"}]
        q2 = [{"number": 1, "title": "Q2", "body": "body"}]
        assert hash_question_list(q1) != hash_question_list(q2)

    def test_returns_16_char_hex_string(self):
        questions = [{"number": 1, "title": "T", "body": ""}]
        h = hash_question_list(questions)
        assert len(h) == 16
        assert re.fullmatch(r"[0-9a-f]+", h)

    def test_body_does_not_affect_hash(self):
        """Hash is keyed only on number+title so body edits don't invalidate it."""
        q1 = [{"number": 1, "title": "T", "body": "version A"}]
        q2 = [{"number": 1, "title": "T", "body": "version B"}]
        assert hash_question_list(q1) == hash_question_list(q2)

    def test_order_matters(self):
        q1 = [{"number": 1, "title": "A"}, {"number": 2, "title": "B"}]
        q2 = [{"number": 2, "title": "B"}, {"number": 1, "title": "A"}]
        assert hash_question_list(q1) != hash_question_list(q2)


# ---------------------------------------------------------------------------
# Counting completed questions
# ---------------------------------------------------------------------------

class TestCountCompletedQuestions:
    def _make_session(self, tmp_path):
        s = tmp_path / "session"
        (s / "questions").mkdir(parents=True)
        return s

    def test_empty_dir_returns_zero(self, tmp_path):
        s = self._make_session(tmp_path)
        assert count_completed_questions(s) == 0

    def test_counts_complete_files(self, tmp_path):
        s = self._make_session(tmp_path)
        write_with_marker(s / "questions" / "q1.md", "done")
        write_with_marker(s / "questions" / "q2.md", "done")
        assert count_completed_questions(s) == 2

    def test_ignores_incomplete_files(self, tmp_path):
        s = self._make_session(tmp_path)
        write_with_marker(s / "questions" / "q1.md", "done")
        (s / "questions" / "q2.md").write_text("partial", encoding="utf-8")
        assert count_completed_questions(s) == 1

    def test_ignores_transcript_files(self, tmp_path):
        s = self._make_session(tmp_path)
        write_with_marker(s / "questions" / "q1-transcript.md", "transcript")
        assert count_completed_questions(s) == 0

    def test_missing_questions_dir_returns_zero(self, tmp_path):
        s = tmp_path / "session"
        s.mkdir()
        assert count_completed_questions(s) == 0


# ---------------------------------------------------------------------------
# Session status JSON
# ---------------------------------------------------------------------------

class TestSessionStatus:
    def test_write_and_load_roundtrip(self, tmp_path):
        s = tmp_path / "session"
        s.mkdir()
        status = {"questions": {"1": "done", "2": "pending"}, "mode": "compete"}
        write_session_status(s, status)
        assert load_session_status(s) == status

    def test_load_missing_file_returns_default(self, tmp_path):
        s = tmp_path / "session"
        s.mkdir()
        assert load_session_status(s) == {"questions": {}}

    def test_load_corrupted_json_returns_default(self, tmp_path):
        s = tmp_path / "session"
        s.mkdir()
        (s / "session_status.json").write_text("not valid json{{{", encoding="utf-8")
        assert load_session_status(s) == {"questions": {}}
