"""Unit tests for agentteam/output/transcripts.py."""

import pytest
from pathlib import Path
from unittest.mock import MagicMock

from agentteam.output.transcripts import format_round_transcript, write_round_transcripts
from agentteam.types import TeamConfig


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_team(agents_spec: dict) -> TeamConfig:
    """Build a minimal TeamConfig from a dict of agent specs."""
    agents_data = {}
    for key, spec in agents_spec.items():
        agents_data[key] = {
            "name": spec.get("name", key),
            "description": spec.get("description", "Test agent."),
            "position": {
                "role": spec.get("role", "participant"),
                "drives": spec.get("drives", ["drive one", "drive two", "drive three"]),
                "pushback_on": spec.get("pushback_on", ["pushback one", "pushback two", "pushback three"]),
            },
            "technique": {
                "behaviors": spec.get(
                    "behaviors",
                    ["behavior one", "behavior two", "behavior three", "behavior four", "behavior five"],
                ),
            },
        }
    return TeamConfig.model_validate({
        "name": "Test Team",
        "agents": agents_data,
    })


SAMPLE_QUESTION = {"number": 1, "title": "How should auth work?", "body": "Describe the auth flow."}

SAMPLE_RESPONSES = {
    "agent_a": "I propose JWT tokens.",
    "agent_b": "I suggest OAuth2.",
}


# ---------------------------------------------------------------------------
# TestFormatRoundTranscript
# ---------------------------------------------------------------------------

class TestFormatRoundTranscript:
    def setup_method(self):
        self.team = make_team({
            "agent_a": {"name": "Alice", "role": "Systems Architect"},
            "agent_b": {"name": "Bob", "role": "Devil's Advocate"},
        })

    def test_header_contains_round_num_and_label(self):
        result = format_round_transcript(SAMPLE_QUESTION, 1, "propose", SAMPLE_RESPONSES, self.team)
        assert "# Round 1: PROPOSE" in result

    def test_header_contains_question_title(self):
        result = format_round_transcript(SAMPLE_QUESTION, 1, "propose", SAMPLE_RESPONSES, self.team)
        assert "How should auth work?" in result

    def test_agent_name_and_role(self):
        result = format_round_transcript(SAMPLE_QUESTION, 1, "propose", SAMPLE_RESPONSES, self.team)
        assert "## Alice (Systems Architect)" in result

    def test_response_text_present(self):
        result = format_round_transcript(SAMPLE_QUESTION, 1, "propose", SAMPLE_RESPONSES, self.team)
        assert "I propose JWT tokens." in result
        assert "I suggest OAuth2." in result

    def test_counter_label_formatted(self):
        result = format_round_transcript(SAMPLE_QUESTION, 2, "counter", SAMPLE_RESPONSES, self.team)
        assert "# Round 2: COUNTER-PROPOSAL" in result

    def test_multiple_agents_present(self):
        result = format_round_transcript(SAMPLE_QUESTION, 1, "propose", SAMPLE_RESPONSES, self.team)
        assert "## Alice" in result
        assert "## Bob" in result

    def test_unknown_agent_key_no_crash(self):
        responses = {"unknown_key": "Some response from unknown agent."}
        result = format_round_transcript(SAMPLE_QUESTION, 1, "propose", responses, self.team)
        assert "unknown_key" in result
        assert "Some response from unknown agent." in result

    def test_empty_responses_no_crash(self):
        result = format_round_transcript(SAMPLE_QUESTION, 1, "propose", {}, self.team)
        assert "# Round 1: PROPOSE" in result


# ---------------------------------------------------------------------------
# TestWriteRoundTranscripts
# ---------------------------------------------------------------------------

class TestWriteRoundTranscripts:
    def setup_method(self):
        self.team = make_team({
            "agent_a": {"name": "Alice", "role": "Systems Architect"},
            "agent_b": {"name": "Bob", "role": "Devil's Advocate"},
        })
        self.round_responses = {
            "propose": SAMPLE_RESPONSES,
            "critique": {"agent_a": "JWT has expiry issues.", "agent_b": "OAuth2 is complex."},
            "evaluate": {"agent_a": "JWT is better for our use case."},
        }
        self.round_labels = ["propose", "critique", "evaluate"]

    def test_creates_round_files(self, tmp_path):
        write_round_transcripts(tmp_path, self.round_responses, self.round_labels, SAMPLE_QUESTION, self.team)
        assert (tmp_path / "round-1-propose.md").exists()
        assert (tmp_path / "round-2-critique.md").exists()
        assert (tmp_path / "round-3-evaluate.md").exists()

    def test_file_names_correct(self, tmp_path):
        paths = write_round_transcripts(tmp_path, self.round_responses, self.round_labels, SAMPLE_QUESTION, self.team)
        names = {p.name for p in paths}
        assert "round-1-propose.md" in names
        assert "round-2-critique.md" in names
        assert "round-3-evaluate.md" in names

    def test_returns_paths(self, tmp_path):
        paths = write_round_transcripts(tmp_path, self.round_responses, self.round_labels, SAMPLE_QUESTION, self.team)
        assert isinstance(paths, list)
        assert all(isinstance(p, Path) for p in paths)
        assert len(paths) == 3

    def test_file_content_readable_markdown(self, tmp_path):
        write_round_transcripts(tmp_path, self.round_responses, self.round_labels, SAMPLE_QUESTION, self.team)
        content = (tmp_path / "round-1-propose.md").read_text(encoding="utf-8")
        assert "# Round 1: PROPOSE" in content
        assert "I propose JWT tokens." in content

    def test_raises_when_dir_missing(self, tmp_path):
        missing = tmp_path / "nonexistent"
        with pytest.raises((FileNotFoundError, OSError, ValueError)):
            write_round_transcripts(missing, self.round_responses, self.round_labels, SAMPLE_QUESTION, self.team)

    def test_utf8_encoding(self, tmp_path):
        responses = {"propose": {"agent_a": "Ångström — résumé"}}
        write_round_transcripts(tmp_path, responses, ["propose"], SAMPLE_QUESTION, self.team)
        content = (tmp_path / "round-1-propose.md").read_text(encoding="utf-8")
        assert "Ångström" in content
