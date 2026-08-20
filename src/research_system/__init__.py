"""ResearchCore AI - Enterprise-Grade Multi-Agent AI Deep Research System.

A collaborative multi-agent architecture designed to autonomously research complex
technical, market, scientific, and industry queries, fact-check evidence, synthesize
findings, peer-review reports, and export executive intelligence packages.
"""

__version__ = "2.0.0"
__author__ = "ResearchCore AI Team"

from src.research_system.orchestrator.workflow import MultiAgentResearchWorkflow
from src.research_system.models.schemas import ResearchRequest, ResearchResponse
from src.research_system.models.enums import ResearchDepth, LLMProvider

__all__ = [
    "MultiAgentResearchWorkflow",
    "ResearchRequest",
    "ResearchResponse",
    "ResearchDepth",
    "LLMProvider",
]
