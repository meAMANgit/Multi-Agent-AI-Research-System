"""Pydantic data schemas for research workflow, requests, and outputs."""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from src.research_system.models.enums import LLMProvider, ResearchDepth, ReviewStatus, TaskStatus


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class SearchQueryItem(BaseModel):
    """Individual query formulated by Query Planner."""
    query: str
    target_dimension: str
    priority: int = Field(default=1, ge=1, le=5)
    source_type: str = "web"


class SearchResult(BaseModel):
    """Structured search hit returned from search engines or crawlers."""
    title: str
    url: str
    snippet: str
    full_content: Optional[str] = None
    source_engine: str = "duckduckgo"
    credibility_score: float = 80.0
    published_date: Optional[str] = None
    domain_authority: float = 75.0


class ExtractedFact(BaseModel):
    """Atomic fact verified by the Fact Checker agent."""
    statement: str
    source_url: str
    source_title: str
    confidence_score: float = Field(ge=0.0, le=100.0)
    category: str = "general"
    verified: bool = True


class QuantitativeDataPoint(BaseModel):
    """Quantitative metric or benchmark extracted by Data Analyst."""
    metric_name: str
    value: str
    unit: Optional[str] = None
    context: str
    source_url: Optional[str] = None
    year_or_period: Optional[str] = None


class DimensionScores(BaseModel):
    """Breakdown of scores across 5 quality dimensions."""
    technical_depth: float = Field(ge=0, le=20)
    factual_accuracy: float = Field(ge=0, le=20)
    structural_flow: float = Field(ge=0, le=20)
    citation_validity: float = Field(ge=0, le=20)
    objectivity: float = Field(ge=0, le=20)


class PeerReviewResult(BaseModel):
    """Result of QA review by Peer Reviewer agent."""
    total_score: float = Field(ge=0, le=100)
    dimension_scores: DimensionScores
    status: ReviewStatus = ReviewStatus.APPROVED
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)
    actionable_feedback: str = ""
    recommended_queries: List[str] = Field(default_factory=list)


class ResearchPlan(BaseModel):
    """Deconstructed research directive by Director agent."""
    topic: str
    primary_objective: str
    hypotheses: List[str] = Field(default_factory=list)
    target_dimensions: List[str] = Field(default_factory=list)
    planned_queries: List[str] = Field(default_factory=list)
    required_depth: ResearchDepth = ResearchDepth.STANDARD
    estimated_subtasks: List[str] = Field(default_factory=list)


class ResearchRequest(BaseModel):
    """API or CLI request payload to initiate research."""
    topic: str = Field(..., min_length=3, description="Research topic or question")
    depth: ResearchDepth = Field(default=ResearchDepth.STANDARD)
    provider: LLMProvider = Field(default=LLMProvider.GOOGLE)
    model: Optional[str] = None
    max_iterations: int = Field(default=2, ge=1, le=5)
    custom_instructions: Optional[str] = None


class AgentThought(BaseModel):
    """Individual real-time reasoning event emitted by agents."""
    timestamp: datetime = Field(default_factory=utc_now)
    agent_name: str
    step: str
    thought: str
    data_preview: Optional[Dict[str, Any]] = None


class ResearchResponse(BaseModel):
    """Complete synthesized research response payload."""
    research_id: str
    topic: str
    status: TaskStatus
    plan: Optional[ResearchPlan] = None
    markdown_report: str
    sources: List[SearchResult] = Field(default_factory=list)
    verified_facts: List[ExtractedFact] = Field(default_factory=list)
    quantitative_data: List[QuantitativeDataPoint] = Field(default_factory=list)
    review_result: Optional[PeerReviewResult] = None
    iterations_completed: int = 1
    total_tokens: int = 0
    estimated_cost_usd: float = 0.0
    execution_time_seconds: float = 0.0
    created_at: datetime = Field(default_factory=utc_now)
