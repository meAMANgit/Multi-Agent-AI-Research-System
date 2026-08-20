"""Execution state container passed between agents in the graph."""

from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional
from pydantic import BaseModel, Field, PrivateAttr
from src.research_system.models.enums import TaskStatus
from src.research_system.models.schemas import (
    AgentThought,
    ExtractedFact,
    PeerReviewResult,
    QuantitativeDataPoint,
    ResearchPlan,
    SearchResult,
    utc_now,
)


class ResearchState(BaseModel):
    """Encapsulates the dynamic state of a research session."""

    research_id: str
    topic: str
    depth: str = "standard"
    status: TaskStatus = TaskStatus.PENDING
    iteration: int = 0
    max_iterations: int = 2

    # Structured artifacts generated across stages
    plan: Optional[ResearchPlan] = None
    generated_queries: List[str] = Field(default_factory=list)
    raw_search_results: List[SearchResult] = Field(default_factory=list)
    crawled_documents: Dict[str, str] = Field(default_factory=dict)
    verified_facts: List[ExtractedFact] = Field(default_factory=list)
    quantitative_data: List[QuantitativeDataPoint] = Field(default_factory=list)
    draft_report: Optional[str] = None
    final_report: Optional[str] = None
    review_result: Optional[PeerReviewResult] = None

    # Telemetry and event feed
    thoughts: List[AgentThought] = Field(default_factory=list)
    total_tokens: int = 0
    estimated_cost_usd: float = 0.0
    start_time: datetime = Field(default_factory=utc_now)
    end_time: Optional[datetime] = None
    error: Optional[str] = None

    # Private callback handlers
    _thought_callbacks: List[Callable[[AgentThought], None]] = PrivateAttr(default_factory=list)

    def register_callback(self, callback: Callable[[AgentThought], None]):
        """Register a callback invoked whenever an agent emits a thought."""
        self._thought_callbacks.append(callback)

    def add_thought(self, agent_name: str, step: str, thought: str, data_preview: Optional[Dict[str, Any]] = None):
        """Append an agent reasoning thought to the stream and notify listeners."""
        thought_obj = AgentThought(
            agent_name=agent_name,
            step=step,
            thought=thought,
            data_preview=data_preview,
        )
        self.thoughts.append(thought_obj)
        for cb in self._thought_callbacks:
            try:
                cb(thought_obj)
            except Exception:
                pass

    @property
    def elapsed_seconds(self) -> float:
        """Calculate elapsed seconds since research began."""
        end = self.end_time or utc_now()
        return (end - self.start_time).total_seconds()
