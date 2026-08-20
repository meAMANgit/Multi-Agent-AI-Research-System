"""Unit tests for Pydantic schemas and ResearchState."""

import pytest
from src.research_system.models.enums import AgentRole, LLMProvider, ResearchDepth, ReviewStatus, TaskStatus
from src.research_system.models.schemas import (
    DimensionScores,
    ExtractedFact,
    PeerReviewResult,
    QuantitativeDataPoint,
    ResearchPlan,
    ResearchRequest,
    ResearchResponse,
    SearchResult,
)
from src.research_system.models.state import ResearchState


def test_research_state_thought_logging():
    """Verify thoughts are logged and timestamped correctly."""
    state = ResearchState(
        research_id="test1234",
        topic="Solid State Battery Commercialization",
        depth="standard",
    )
    
    assert state.status == TaskStatus.PENDING
    assert len(state.thoughts) == 0

    state.add_thought("Lead Research Director", "Formulate Hypotheses", "Formulating initial hypotheses.")
    assert len(state.thoughts) == 1
    assert state.thoughts[0].agent_name == "Lead Research Director"
    assert state.thoughts[0].step == "Formulate Hypotheses"


def test_schemas_validation():
    """Verify validation constraints and serialization."""
    fact = ExtractedFact(
        statement="Silicon-anode batteries provide up to 40% energy density increase.",
        source_url="https://nature.com/articles/sample",
        source_title="Nature Energy",
        confidence_score=94.5,
        category="Technical",
    )
    assert fact.confidence_score == 94.5
    assert fact.verified is True

    scores = DimensionScores(
        technical_depth=19.0,
        factual_accuracy=18.5,
        structural_flow=18.0,
        citation_validity=19.0,
        objectivity=17.5,
    )
    review = PeerReviewResult(
        total_score=92.0,
        dimension_scores=scores,
        status=ReviewStatus.APPROVED,
        strengths=["Rigorous citations"],
    )
    assert review.total_score == 92.0
    assert review.status == ReviewStatus.APPROVED


def test_research_request_and_response():
    """Test full response schema construction."""
    req = ResearchRequest(topic="Quantum Machine Learning", depth=ResearchDepth.QUICK)
    assert req.topic == "Quantum Machine Learning"
    assert req.depth == ResearchDepth.QUICK

    res = ResearchResponse(
        research_id="resp001",
        topic="Quantum Machine Learning",
        status=TaskStatus.COMPLETED,
        markdown_report="# Quantum ML Report",
        sources=[SearchResult(title="ArXiv QML", url="https://arxiv.org/abs/123", snippet="QML survey")],
        verified_facts=[],
        quantitative_data=[],
    )
    assert res.research_id == "resp001"
    assert len(res.sources) == 1
