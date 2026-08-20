"""Models package init."""

try:
    from src.research_system.models.enums import (
        AgentRole,
        ResearchDepth,
        LLMProvider,
        TaskStatus,
        ReviewStatus,
    )
    from src.research_system.models.schemas import (
        SearchQueryItem,
        SearchResult,
        ExtractedFact,
        QuantitativeDataPoint,
        DimensionScores,
        PeerReviewResult,
        ResearchPlan,
        ResearchRequest,
        AgentThought,
        ResearchResponse,
    )
    from src.research_system.models.state import ResearchState
except (ImportError, ModuleNotFoundError):
    from .enums import (
        AgentRole,
        ResearchDepth,
        LLMProvider,
        TaskStatus,
        ReviewStatus,
    )
    from .schemas import (
        SearchQueryItem,
        SearchResult,
        ExtractedFact,
        QuantitativeDataPoint,
        DimensionScores,
        PeerReviewResult,
        ResearchPlan,
        ResearchRequest,
        AgentThought,
        ResearchResponse,
    )
    from .state import ResearchState

__all__ = [
    "AgentRole",
    "ResearchDepth",
    "LLMProvider",
    "TaskStatus",
    "ReviewStatus",
    "SearchQueryItem",
    "SearchResult",
    "ExtractedFact",
    "QuantitativeDataPoint",
    "DimensionScores",
    "PeerReviewResult",
    "ResearchPlan",
    "ResearchRequest",
    "AgentThought",
    "ResearchResponse",
    "ResearchState",
]
