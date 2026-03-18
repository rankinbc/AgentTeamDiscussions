"""Pydantic models for agent configuration."""

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


class PersonalityConfig(BaseModel):
    assertiveness: float = Field(0.5, ge=0.0, le=1.0)
    creativity_temp: float = Field(0.5, ge=0.0, le=1.0)
    risk_tolerance: float = Field(0.5, ge=0.0, le=1.0)
    cognitive_style: CognitiveStyle = CognitiveStyle.ANALYTICAL
    emotional_baseline: EmotionalBaseline = EmotionalBaseline.NEUTRAL
    attention_span: float = Field(0.5, ge=0.0, le=1.0, description="0=jumps topics, 1=deep focused")
    stubbornness: float = Field(0.5, ge=0.0, le=1.0)
    idea_receptivity: float = Field(0.5, ge=0.0, le=1.0, description="0=drives own agenda, 1=deeply engages with others' ideas")
    bluntness: float = Field(0.5, ge=0.0, le=1.0, description="0=diplomatic, 1=brutally direct/rude")
    patience: float = Field(0.5, ge=0.0, le=1.0, description="0=cuts off tangents aggressively, 1=lets discussions breathe")
    domain_affinities: list[str] = Field(default_factory=list)


class PositionConfig(BaseModel):
    role: str
    drives: list[str] = Field(default_factory=list)
    pushback_on: list[str] = Field(default_factory=list)
    intensity: float = Field(0.5, ge=0.0, le=1.0)


class TechniqueConfig(BaseModel):
    primary: str
    style_description: str = ""
    behaviors: list[str] = Field(default_factory=list)


class AntiSlopConfig(BaseModel):
    agreement_tax: bool = Field(True, description="Must add substance when agreeing")
    perspective_enforcement: bool = Field(True, description="Stay in character even under pressure")
    devils_advocate_duty: bool = Field(False, description="Actively argue the other side")
    uncomfortable_idea_quota: int = Field(0, description="Min uncomfortable ideas per N turns")
    domain_pivot_trigger: bool = Field(False, description="Inject cross-domain perspectives")


class VoiceConfig(BaseModel):
    tone: str = "professional"
    vocabulary_hints: list[str] = Field(default_factory=list)
    anti_patterns: list[str] = Field(default_factory=list, description="Phrases to NEVER use")
    brevity: str = Field("normal", description="concise, normal, or thorough")


class OutputConfig(BaseModel):
    operating_level: str = Field("requirements", description="requirements, design, or implementation")
    job: str = Field("propose", description="What this agent's output IS: propose, critique, evaluate, simplify")


class AgentConfig(BaseModel):
    name: str
    description: str
    personality: PersonalityConfig = Field(default_factory=PersonalityConfig)
    position: PositionConfig = Field(default_factory=lambda: PositionConfig(role="participant"))
    technique: TechniqueConfig = Field(default_factory=lambda: TechniqueConfig(primary="none"))
    anti_slop: AntiSlopConfig = Field(default_factory=AntiSlopConfig)
    voice: VoiceConfig = Field(default_factory=VoiceConfig)
    output: OutputConfig = Field(default_factory=OutputConfig)


class TeamConfig(BaseModel):
    agents: dict[str, AgentConfig]
