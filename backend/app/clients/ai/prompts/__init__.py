"""AI prompts package."""

from app.clients.ai.prompts.asset_identification import ASSET_IDENTIFICATION_PROMPT
from app.clients.ai.prompts.threat_analysis import THREAT_ANALYSIS_PROMPT
from app.clients.ai.prompts.architecture_understanding import ARCHITECTURE_UNDERSTANDING_PROMPT
from app.clients.ai.prompts.security_measure import SECURITY_MEASURE_PROMPT

__all__ = [
    "ASSET_IDENTIFICATION_PROMPT",
    "THREAT_ANALYSIS_PROMPT",
    "ARCHITECTURE_UNDERSTANDING_PROMPT",
    "SECURITY_MEASURE_PROMPT",
]
