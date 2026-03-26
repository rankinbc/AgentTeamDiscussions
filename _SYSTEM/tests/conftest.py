"""Shared fixtures for agentteam tests."""
import pytest
from pathlib import Path

import yaml

from agentteam.types import (
    AgentConfig,
    AntiSlopConfig,
    CognitiveStyle,
    PersonalityConfig,
    VoiceConfig,
    Brevity,
)

SAMPLE_BRIEF_TEXT = """\
## What's Already Decided

- We use Python 3.11+
- Sessions are stored as markdown files

## Open Questions

1. **How does a round begin?** After a reset, the orchestrator calls begin_round.
The moderator sets the topic and agents respond in order.

2. **What is the error handling strategy?** We need to handle timeout, network
errors, and invalid responses gracefully without losing session state.
"""


@pytest.fixture
def sample_brief(tmp_path: Path) -> Path:
    """A valid brief file with two numbered questions."""
    p = tmp_path / "brief.md"
    p.write_text(SAMPLE_BRIEF_TEXT, encoding="utf-8")
    return p


@pytest.fixture
def minimal_agent() -> AgentConfig:
    """Minimal valid AgentConfig — only required fields set."""
    return AgentConfig(
        name="Test Agent",
        description="A test agent for unit testing.",
    )


@pytest.fixture
def rich_agent() -> AgentConfig:
    """AgentConfig with non-default personality, voice, and anti-slop settings."""
    return AgentConfig(
        name="Critic",
        description="A sharp analytical critic who finds holes in every plan.",
        personality=PersonalityConfig(
            assertiveness=0.9,
            creativity_temp=0.3,
            cognitive_style=CognitiveStyle.ANALYTICAL,
        ),
        voice=VoiceConfig(
            tone="blunt",
            brevity=Brevity.CONCISE,
            vocabulary_hints=["trade-off", "constraint"],
            anti_patterns=[
                "I think", "perhaps", "perhaps we should consider", "I believe",
                "in my opinion", "we could explore", "it seems to me", "generally speaking",
            ],
        ),
        anti_slop=AntiSlopConfig(
            agreement_tax=True,
            devils_advocate_duty=True,
            uncomfortable_idea_quota=2,
        ),
    )


@pytest.fixture
def minimal_config_dir(tmp_path: Path) -> Path:
    """A minimal config directory with all YAML files ConfigLoader needs."""
    cfg = tmp_path / "config"
    cfg.mkdir()

    (cfg / "defaults.yaml").write_text(yaml.dump({
        "timeouts": {"default": 60, "discussion": 120},
        "truncation": {"short": 2000, "long": 8000},
        "conversation": {
            "history_truncation_threshold": 20,
            "history_keep_first": 2,
            "history_keep_last": 8,
            "multi_history_truncation_threshold": 30,
            "multi_history_keep_first": 3,
            "multi_history_keep_last": 12,
        },
        "display": {"slug_max_length": 60},
    }), encoding="utf-8")

    (cfg / "agent_display.yaml").write_text(yaml.dump({
        "display_names": {"alpha": "Agent Alpha", "beta": "Agent Beta"},
        "colors_hex": {"alpha": "#ff0000", "beta": "#00ff00"},
        "colors_ansi_cycle": ["\033[31m", "\033[32m"],
    }), encoding="utf-8")

    (cfg / "experiment_modes.yaml").write_text(yaml.dump({
        "modes": {"default": {"agents": ["alpha", "beta"]}}
    }), encoding="utf-8")

    (cfg / "role_overlays.yaml").write_text(yaml.dump({
        "counter_propose_instruction": "Counter-propose the previous idea.",
        "overlays": {
            "proposer": {"instruction": "Propose a bold idea."},
        },
    }), encoding="utf-8")

    return cfg


@pytest.fixture
def minimal_template_dir(tmp_path: Path) -> Path:
    """A minimal template directory with one Jinja2 and one HTML file."""
    tmpl = tmp_path / "templates"
    tmpl.mkdir()
    (tmpl / "html").mkdir()
    (tmpl / "html" / "test.html").write_text("<h1>{{ title }}</h1>", encoding="utf-8")
    (tmpl / "test_prompt.md.j2").write_text("Topic: {{ topic }}", encoding="utf-8")
    return tmpl
