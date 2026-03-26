"""Structured 3-round discussion engine (propose/critique/evaluate/synthesize)."""
from .engine import (
    parse_brief, run_question, run_round, synthesize,
    format_transcript, extract_open_questions, slugify,
    compute_speaking_order, EXPERIMENT_MODES, AGENT_DISPLAY_NAMES,
    SYNTHESIS_SYSTEM_PROMPT, COUNTER_PROPOSE_INSTRUCTION, PROPOSE_ROLES,
    TEAM_CONFIG,
)
