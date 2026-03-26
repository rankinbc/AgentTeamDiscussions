"""Unit tests for agentteam/utils/io.py."""

import pytest
from pathlib import Path

from agentteam.utils.io import write_atomic


class TestWriteAtomic:
    def test_writes_content(self, tmp_path):
        path = tmp_path / "output.md"
        write_atomic(path, "hello world")
        assert path.read_text(encoding="utf-8") == "hello world"

    def test_tmp_file_cleaned_up(self, tmp_path):
        path = tmp_path / "output.md"
        write_atomic(path, "content")
        tmp = path.with_suffix(path.suffix + ".tmp")
        assert not tmp.exists()

    def test_overwrites_existing_file(self, tmp_path):
        path = tmp_path / "output.md"
        write_atomic(path, "first")
        write_atomic(path, "second")
        assert path.read_text(encoding="utf-8") == "second"

    def test_encoding_utf8(self, tmp_path):
        path = tmp_path / "output.md"
        content = "Ångström — résumé — 日本語"
        write_atomic(path, content)
        assert path.read_text(encoding="utf-8") == content

    def test_parent_must_exist(self, tmp_path):
        path = tmp_path / "nonexistent_dir" / "file.md"
        with pytest.raises((FileNotFoundError, OSError)):
            write_atomic(path, "content")

    def test_accepts_string_path(self, tmp_path):
        path = str(tmp_path / "output.md")
        write_atomic(path, "string path works")
        assert Path(path).read_text(encoding="utf-8") == "string path works"

    def test_empty_content(self, tmp_path):
        path = tmp_path / "empty.md"
        write_atomic(path, "")
        assert path.exists()
        assert path.read_text(encoding="utf-8") == ""
