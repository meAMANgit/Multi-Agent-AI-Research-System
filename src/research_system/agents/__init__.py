"""Agents package init."""

try:
    from src.research_system.agents.base import BaseAgent
    from src.research_system.agents.director import DirectorAgent
    from src.research_system.agents.query_planner import QueryPlannerAgent
    from src.research_system.agents.retriever import RetrieverAgent
    from src.research_system.agents.fact_checker import FactCheckerAgent
    from src.research_system.agents.data_analyst import DataAnalystAgent
    from src.research_system.agents.report_writer import ReportWriterAgent
    from src.research_system.agents.peer_reviewer import PeerReviewerAgent
except (ImportError, ModuleNotFoundError):
    from .base import BaseAgent
    from .director import DirectorAgent
    from .query_planner import QueryPlannerAgent
    from .retriever import RetrieverAgent
    from .fact_checker import FactCheckerAgent
    from .data_analyst import DataAnalystAgent
    from .report_writer import ReportWriterAgent
    from .peer_reviewer import PeerReviewerAgent

__all__ = [
    "BaseAgent",
    "DirectorAgent",
    "QueryPlannerAgent",
    "RetrieverAgent",
    "FactCheckerAgent",
    "DataAnalystAgent",
    "ReportWriterAgent",
    "PeerReviewerAgent",
]
