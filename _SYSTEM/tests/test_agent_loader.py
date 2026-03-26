"""Tests for agentteam/agents/loader.py — load_agent, load_team, resolve_agent."""

import pytest
import yaml
from pathlib import Path
from pydantic import ValidationError

from agentteam.agents.loader import load_agent, load_team, load_agent_by_key, resolve_agent
from agentteam.types import TeamConfig

_SYSTEM_DIR = Path(__file__).resolve().parent.parent
_AGENTS_DIR = _SYSTEM_DIR / "data" / "discussionAgents"

_MINIMAL_AGENT_YAML = """\
name: Test Agent
description: A test agent for validation purposes.
position:
  role: tester
  drives:
  - drive one
  - drive two
  - drive three
  pushback_on:
  - pushback one
  - pushback two
  - pushback three
technique:
  primary: testing
  behaviors:
  - behavior one
  - behavior two
  - behavior three
  - behavior four
  - behavior five
"""

_INVALID_AGENT_YAML = """\
name: Bad Agent
description: This agent has an invalid assertiveness value.
personality:
  assertiveness: 2.0
position:
  role: tester
  drives:
  - drive one
  - drive two
  - drive three
  pushback_on:
  - pushback one
  - pushback two
  - pushback three
technique:
  primary: testing
  behaviors:
  - behavior one
  - behavior two
  - behavior three
  - behavior four
  - behavior five
"""


def _write_yaml(tmp_path: Path, content: str, filename: str = "agent.yaml") -> Path:
    path = tmp_path / filename
    path.write_text(content, encoding="utf-8")
    return path


def get_agent_yamls():
    return list(_AGENTS_DIR.glob("*.yaml"))


# ---------------------------------------------------------------------------
# TestLoadAgent
# ---------------------------------------------------------------------------

class TestLoadAgent:
    def test_loads_valid_agent_yaml(self, tmp_path):
        path = _write_yaml(tmp_path, _MINIMAL_AGENT_YAML)
        agent = load_agent(str(path))
        assert agent.name == "Test Agent"
        assert agent.description == "A test agent for validation purposes."

    def test_missing_file_raises_file_not_found(self):
        with pytest.raises(FileNotFoundError):
            load_agent("nonexistent_agent.yaml")

    def test_invalid_yaml_raises_validation_error(self, tmp_path):
        path = _write_yaml(tmp_path, _INVALID_AGENT_YAML)
        with pytest.raises(ValidationError):
            load_agent(str(path))

    def test_meta_key_stripped(self, tmp_path):
        content = _MINIMAL_AGENT_YAML + "_meta:\n  created: 2026-01-01\n"
        path = _write_yaml(tmp_path, content)
        agent = load_agent(str(path))
        assert agent.name == "Test Agent"

    def test_loaded_agent_has_correct_position(self, tmp_path):
        path = _write_yaml(tmp_path, _MINIMAL_AGENT_YAML)
        agent = load_agent(str(path))
        assert agent.position.role == "tester"
        assert len(agent.position.drives) == 3
        assert len(agent.position.pushback_on) == 3

    def test_loaded_agent_has_correct_behaviors(self, tmp_path):
        path = _write_yaml(tmp_path, _MINIMAL_AGENT_YAML)
        agent = load_agent(str(path))
        assert len(agent.technique.behaviors) == 5


# ---------------------------------------------------------------------------
# TestLoadAgentRealFiles (parametrized over all 33 real agent files)
# ---------------------------------------------------------------------------

class TestLoadAgentRealFiles:
    @pytest.mark.parametrize("agent_file", get_agent_yamls(), ids=lambda f: f.name)
    def test_all_real_agents_load(self, agent_file):
        agent = load_agent(str(agent_file))
        assert agent.name  # non-empty name
        assert agent.description  # non-empty description


# ---------------------------------------------------------------------------
# TestLoadTeam
# ---------------------------------------------------------------------------

class TestLoadTeam:
    def test_loads_inline_team(self, tmp_path):
        content = """\
name: Test Team
agents:
  agent_a:
    name: Alice
    description: Agent A for testing.
    position:
      role: tester
      drives:
      - drive one
      - drive two
      - drive three
      pushback_on:
      - pushback one
      - pushback two
      - pushback three
    technique:
      primary: testing
      behaviors:
      - behavior one
      - behavior two
      - behavior three
      - behavior four
      - behavior five
"""
        path = _write_yaml(tmp_path, content, "team.yaml")
        team = load_team(str(path))
        assert isinstance(team, TeamConfig)
        assert "agent_a" in team.agents
        assert team.agents["agent_a"].name == "Alice"

    def test_missing_file_raises(self):
        with pytest.raises(FileNotFoundError):
            load_team("nonexistent_team.yaml")

    def test_missing_agents_key_raises(self, tmp_path):
        content = "name: Bad Team\ndescription: no agents key\n"
        path = _write_yaml(tmp_path, content, "bad_team.yaml")
        with pytest.raises(KeyError):
            load_team(str(path))


# ---------------------------------------------------------------------------
# TestResolveAgent
# ---------------------------------------------------------------------------

class TestResolveAgent:
    def _make_team(self, tmp_path):
        content = """\
name: Resolve Test Team
agents:
  alice_key:
    name: Alice
    description: Agent for resolve tests.
    position:
      role: tester
      drives:
      - drive one
      - drive two
      - drive three
      pushback_on:
      - pushback one
      - pushback two
      - pushback three
    technique:
      primary: testing
      behaviors:
      - behavior one
      - behavior two
      - behavior three
      - behavior four
      - behavior five
"""
        path = _write_yaml(tmp_path, content, "resolve_team.yaml")
        return load_team(str(path))

    def test_resolve_by_key(self, tmp_path):
        team = self._make_team(tmp_path)
        key, agent = resolve_agent(team, "alice_key")
        assert key == "alice_key"
        assert agent.name == "Alice"

    def test_resolve_missing_raises_key_error(self, tmp_path):
        team = self._make_team(tmp_path)
        with pytest.raises(KeyError) as exc_info:
            resolve_agent(team, "nonexistent_key")
        assert "alice_key" in str(exc_info.value)
