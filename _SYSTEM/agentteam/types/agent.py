"""Canonical definition of a Discussion Agent.

This is the AUTHORITATIVE source for what an agent is. All other code
(session runner, prompt builder, Workshop, CLI tools) imports from here.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class CognitiveStyle(str, Enum):
    ANALYTICAL = "analytical"
    LATERAL = "lateral"
    SYSTEMATIC = "systematic"
    INTUITIVE = "intuitive"
    DIVERGENT = "divergent"


class EmotionalBaseline(str, Enum):
    OPTIMISTIC = "optimistic"
    SKEPTICAL = "skeptical"
    CURIOUS = "curious"
    CAUTIOUS = "cautious"
    NEUTRAL = "neutral"
    ENTHUSIASTIC = "enthusiastic"


class Brevity(str, Enum):
    CONCISE = "concise"
    NORMAL = "normal"
    THOROUGH = "thorough"


class OperatingLevel(str, Enum):
    REQUIREMENTS = "requirements"
    DESIGN = "design"
    IMPLEMENTATION = "implementation"


class JobType(str, Enum):
    PROPOSE = "propose"
    CRITIQUE = "critique"
    EVALUATE = "evaluate"
    SIMPLIFY = "simplify"
    IDEATE = "ideate"


class ActionTriggerType(str, Enum):
    ALWAYS = "always"
    ROUND = "round"
    PHASE = "phase"


class PersonalityConfig(BaseModel):
    assertiveness: float = Field(0.5, ge=0.0, le=1.0)
    creativity_temp: float = Field(0.5, ge=0.0, le=1.0)
    risk_tolerance: float = Field(0.5, ge=0.0, le=1.0)
    attention_span: float = Field(0.5, ge=0.0, le=1.0)
    stubbornness: float = Field(0.5, ge=0.0, le=1.0)
    idea_receptivity: float = Field(0.5, ge=0.0, le=1.0)
    bluntness: float = Field(0.5, ge=0.0, le=1.0)
    patience: float = Field(0.5, ge=0.0, le=1.0)
    cognitive_style: CognitiveStyle = Field(CognitiveStyle.ANALYTICAL)
    emotional_baseline: EmotionalBaseline = Field(EmotionalBaseline.NEUTRAL)
    domain_affinities: list[str] = Field(default_factory=list)


class PositionConfig(BaseModel):
    role: str = Field("participant")
    drives: list[str] = Field(default_factory=list, min_length=3, max_length=5)
    pushback_on: list[str] = Field(default_factory=list, min_length=3, max_length=5)
    intensity: float = Field(0.5, ge=0.0, le=1.0)


class TechniqueConfig(BaseModel):
    primary: str = Field("none")
    style_description: str = Field("")
    behaviors: list[str] = Field(default_factory=list, min_length=5, max_length=8)


class AntiSlopConfig(BaseModel):
    agreement_tax: bool = Field(True)
    perspective_enforcement: bool = Field(True)
    devils_advocate_duty: bool = Field(False)
    uncomfortable_idea_quota: int = Field(0, ge=0, le=5)
    domain_pivot_trigger: bool = Field(False)


class VoiceConfig(BaseModel):
    tone: str = Field("professional")
    brevity: Brevity = Field(Brevity.NORMAL)
    vocabulary_hints: list[str] = Field(default_factory=list)
    anti_patterns: list[str] = Field(default_factory=list, min_length=8, max_length=12)


class OutputConfig(BaseModel):
    operating_level: OperatingLevel = Field(OperatingLevel.REQUIREMENTS)
    job: JobType = Field(JobType.PROPOSE)


class ActionAssignment(BaseModel):
    action_id: str = Field(...)
    trigger: ActionTriggerType = Field(ActionTriggerType.ALWAYS)
    trigger_value: Optional[str] = Field(None)


class AgentMeta(BaseModel):
    created: datetime = Field(default_factory=datetime.now)
    modified: datetime = Field(default_factory=datetime.now)
    version: int = Field(1, ge=1)
    tags: list[str] = Field(default_factory=list)
    notes: str = Field("")
    history: list[dict] = Field(default_factory=list)


class AgentConfig(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str = Field(...)
    description: str = Field(...)
    personality: PersonalityConfig = Field(default_factory=PersonalityConfig)
    position: PositionConfig = Field(default_factory=PositionConfig)
    technique: TechniqueConfig = Field(default_factory=TechniqueConfig)
    anti_slop: AntiSlopConfig = Field(default_factory=AntiSlopConfig)
    voice: VoiceConfig = Field(default_factory=VoiceConfig)
    output: OutputConfig = Field(default_factory=OutputConfig)
    actions: list[ActionAssignment] = Field(default_factory=list)
    meta: Optional[AgentMeta] = Field(default=None)


class GroupAgentRef(BaseModel):
    agent_id: str = Field(...)
    round: JobType = Field(JobType.PROPOSE)


class GroupConfig(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str = Field(...)
    description: str = Field("")
    agents: list[GroupAgentRef] = Field(default_factory=list)
    round_actions: dict[str, list[str]] = Field(default_factory=dict)


class TeamConfig(BaseModel):
    """Legacy self-contained team definition with inline agent dicts."""
    agents: dict[str, AgentConfig]
