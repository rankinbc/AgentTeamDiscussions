"""Tests for assign_rounds_from_job_types and load_team path resolution."""

import pytest
import yaml
from pathlib import Path

from agentteam.agents.loader import assign_rounds_from_job_types, load_team
from agentteam.types import AgentConfig, JobType, OutputConfig, TeamConfig


def make_team_with_jobs(**job_map) -> TeamConfig:
    """Build TeamConfig with agents having specific output.job values.

    Usage: make_team_with_jobs(alice="propose", bob="critique", carol="evaluate")
    """
    agents = {}
    for key, job_str in job_map.items():
        agents[key] = AgentConfig(
            name=key.title(),
            description=f"Test agent with job {job_str}.",
            output=OutputConfig(job=JobType(job_str)),
        )
    return TeamConfig(agents=agents)


# ---------------------------------------------------------------------------
# TestAssignRoundsFromJobTypes
# ---------------------------------------------------------------------------


class TestAssignRoundsFromJobTypes:
    def test_basic_three_round_assignment(self):
        """Agents with propose/critique/evaluate jobs → correct groups."""
        team = make_team_with_jobs(a="propose", b="critique", c="evaluate")
        result = assign_rounds_from_job_types(team)
        assert result["propose"] == ["a"]
        assert result["critique"] == ["b"]
        assert result["evaluate"] == ["c"]

    def test_ideate_maps_to_propose_round(self):
        """ideate agents participate in the propose round."""
        team = make_team_with_jobs(merchant="ideate", critic="critique", evaluator="evaluate")
        result = assign_rounds_from_job_types(team)
        assert "merchant" in result["propose"]
        assert result["critique"] == ["critic"]

    def test_simplify_maps_to_evaluate_round(self):
        """simplify agents participate in the evaluate round."""
        team = make_team_with_jobs(p="propose", s="simplify")
        result = assign_rounds_from_job_types(team)
        assert "s" in result["evaluate"]

    def test_no_proposers_raises_value_error(self):
        """Team with no propose/ideate agents raises ValueError."""
        team = make_team_with_jobs(a="critique", b="evaluate")
        with pytest.raises(ValueError, match="propose"):
            assign_rounds_from_job_types(team)

    def test_all_three_keys_always_present(self):
        """All three round keys are always in the return dict, even if empty."""
        team = make_team_with_jobs(a="propose")
        result = assign_rounds_from_job_types(team)
        assert "propose" in result
        assert "critique" in result
        assert "evaluate" in result
        assert result["critique"] == []
        assert result["evaluate"] == []

    def test_real_beta_agents_team_loads_and_assigns(self):
        """Integration: beta-agents team assigns agents matching experiment_modes.yaml."""
        from agentteam.agents.loader import load_team_by_name
        team = load_team_by_name("beta-agents")
        result = assign_rounds_from_job_types(team)
        # cognitive_architect and flow_orchestrator are proposers
        assert "cognitive_architect" in result["propose"]
        assert "flow_orchestrator" in result["propose"]
        # idea_merchant is an ideate agent — maps to propose round
        assert "idea_merchant" in result["propose"]
        # systems_pragmatist and adversarial_critic are critics
        assert "systems_pragmatist" in result["critique"]
        assert "adversarial_critic" in result["critique"]
        # product_oracle and context_surgeon are evaluators
        assert "product_oracle" in result["evaluate"]
        assert "context_surgeon" in result["evaluate"]


# ---------------------------------------------------------------------------
# TestLoadTeamPathResolution
# ---------------------------------------------------------------------------

_MINIMAL_AGENT_YAML = """\
name: Portable Agent
description: Agent for path-resolution testing.
position:
  role: tester
  drives: [drive one, drive two, drive three]
  pushback_on: [pushback one, pushback two, pushback three]
technique:
  primary: testing
  behaviors: [b one, b two, b three, b four, b five]
output:
  job: propose
  operating_level: requirements
"""


class TestLoadTeamPathResolution:
    def test_agent_file_resolved_relative_to_team_dir(self, tmp_path: Path):
        """Agent files in same dir as team YAML load correctly."""
        agent_file = tmp_path / "my_agent.yaml"
        agent_file.write_text(_MINIMAL_AGENT_YAML, encoding="utf-8")

        team_yaml = tmp_path / "my_team.yaml"
        team_yaml.write_text(yaml.dump({
            "name": "Portable Team",
            "agents": [{"agent_key": "portable", "file": "my_agent.yaml"}],
        }), encoding="utf-8")

        team = load_team(str(team_yaml))
        assert "portable" in team.agents
        assert team.agents["portable"].name == "Portable Agent"

    def test_team_dir_takes_priority_over_agents_dir(self, tmp_path: Path):
        """Co-located agent file wins over same-named file in _AGENTS_DIR."""
        from agentteam.agents.loader import _AGENTS_DIR

        # Create a local override with a different name to distinguish it
        local_yaml = _MINIMAL_AGENT_YAML.replace("Portable Agent", "Local Override Agent")
        agent_file = tmp_path / "local_only.yaml"
        agent_file.write_text(local_yaml, encoding="utf-8")

        # Ensure this filename doesn't exist in _AGENTS_DIR (it shouldn't)
        assert not (_AGENTS_DIR / "local_only.yaml").exists()

        team_yaml = tmp_path / "my_team.yaml"
        team_yaml.write_text(yaml.dump({
            "name": "Override Team",
            "agents": [{"agent_key": "override", "file": "local_only.yaml"}],
        }), encoding="utf-8")

        team = load_team(str(team_yaml))
        assert team.agents["override"].name == "Local Override Agent"

    def test_missing_agent_file_raises_file_not_found(self, tmp_path: Path):
        """FileNotFoundError raised when agent file is absent from both dirs."""
        team_yaml = tmp_path / "my_team.yaml"
        team_yaml.write_text(yaml.dump({
            "name": "Broken Team",
            "agents": [{"agent_key": "ghost", "file": "does_not_exist.yaml"}],
        }), encoding="utf-8")

        with pytest.raises(FileNotFoundError, match="does_not_exist.yaml"):
            load_team(str(team_yaml))

    def test_agent_file_in_agents_dir_still_works(self):
        """Existing teams with files in _AGENTS_DIR continue to load."""
        from agentteam.agents.loader import load_team_by_name
        team = load_team_by_name("beta-agents")
        assert len(team.agents) >= 6
