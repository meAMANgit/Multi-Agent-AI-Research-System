"""Enums used throughout ResearchCore AI."""

from enum import Enum


class AgentRole(str, Enum):
    """Specialized roles within the research team."""
    DIRECTOR = "Lead Research Director"
    QUERY_PLANNER = "Search Query Planner"
    RETRIEVER = "Web & Academic Retriever"
    FACT_CHECKER = "Fact & Credibility Auditor"
    DATA_ANALYST = "Quantitative Data Analyst"
    REPORT_WRITER = "Research Synthesis Author"
    PEER_REVIEWER = "Peer Reviewer & QA"


class ResearchDepth(str, Enum):
    """Research depth tier affecting search vector count and iterations."""
    QUICK = "quick"              # Fast summary (1-2 queries, 1 iteration)
    STANDARD = "standard"        # Standard report (3-5 queries, up to 2 iterations)
    DEEP = "deep"                # Comprehensive report (6-10 queries, up to 3 iterations)
    EXHAUSTIVE = "exhaustive"    # Whitepaper grade (10+ queries, multi-source academic)


class LLMProvider(str, Enum):
    """Supported LLM backend providers."""
    GOOGLE = "google"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GROQ = "groq"
    OLLAMA = "ollama"
    MOCK = "mock"


class TaskStatus(str, Enum):
    """Workflow execution states."""
    PENDING = "pending"
    PLANNING = "planning"
    SEARCHING = "searching"
    VERIFYING = "verifying"
    ANALYZING = "analyzing"
    WRITING = "writing"
    REVIEWING = "reviewing"
    REVISING = "revising"
    COMPLETED = "completed"
    FAILED = "failed"


class ReviewStatus(str, Enum):
    """Peer review evaluation status."""
    APPROVED = "APPROVED"
    REVISION_NEEDED = "REVISION_NEEDED"
    REJECTED = "REJECTED"
