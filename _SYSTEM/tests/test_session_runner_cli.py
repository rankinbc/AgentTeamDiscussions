"""CLI smoke tests for the session runner entry point.

Uses subprocess to invoke session_runner.py directly, avoiding the module-level
config imports (config_loader, discussion.engine) that require engine config files.
Tests only the CLI interface: arg parsing, path validation, error exits.
"""
import subprocess
import sys
from pathlib import Path

import pytest

ENGINE_DIR = Path(__file__).parent.parent / "projects" / "engine"
RUNNER = str(ENGINE_DIR / "session_runner.py")


def run_cli(*args: str) -> subprocess.CompletedProcess:
    """Run session_runner.py as a subprocess and return the result."""
    return subprocess.run(
        [sys.executable, RUNNER, *args],
        capture_output=True,
        text=True,
        cwd=str(ENGINE_DIR),
        timeout=15,
    )


class TestSessionRunnerCLI:
    def test_help_exits_zero(self):
        result = run_cli("--help")
        assert result.returncode == 0

    def test_help_shows_mode_flag(self):
        result = run_cli("--help")
        assert "--mode" in result.stdout

    def test_help_shows_team_flag(self):
        result = run_cli("--help")
        assert "--team" in result.stdout

    def test_help_shows_timeout_flag(self):
        result = run_cli("--help")
        assert "--timeout" in result.stdout

    def test_missing_brief_exits_one(self, tmp_path):
        nonexistent = str(tmp_path / "does_not_exist.md")
        result = run_cli(nonexistent)
        assert result.returncode == 1

    def test_missing_brief_prints_error(self, tmp_path):
        nonexistent = str(tmp_path / "does_not_exist.md")
        result = run_cli(nonexistent)
        output = result.stdout + result.stderr
        assert "ERROR" in output or "not found" in output.lower()

    def test_missing_team_exits_one(self, tmp_path, sample_brief):
        nonexistent_team = str(tmp_path / "no_such_team.yaml")
        result = run_cli(str(sample_brief), "--team", nonexistent_team)
        assert result.returncode == 1

    def test_missing_team_prints_error(self, tmp_path, sample_brief):
        nonexistent_team = str(tmp_path / "no_such_team.yaml")
        result = run_cli(str(sample_brief), "--team", nonexistent_team)
        output = result.stdout + result.stderr
        assert "ERROR" in output
        assert "no_such_team.yaml" in output
