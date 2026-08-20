"""Orchestrator package init."""

try:
    from src.research_system.orchestrator.workflow import MultiAgentResearchWorkflow
except (ImportError, ModuleNotFoundError):
    from .workflow import MultiAgentResearchWorkflow

__all__ = ["MultiAgentResearchWorkflow"]
