"""Unit tests for individual specialist agents."""

import pytest
from src.research_system.agents.data_analyst import DataAnalystAgent
from src.research_system.agents.director import DirectorAgent
from src.research_system.agents.fact_checker import FactCheckerAgent
from src.research_system.agents.peer_reviewer import PeerReviewerAgent
from src.research_system.agents.query_planner import QueryPlannerAgent
from src.research_system.agents.report_writer import ReportWriterAgent
from src.research_system.agents.retriever import RetrieverAgent
from src.research_system.llm.provider import MockProvider
from src.research_system.models.schemas import SearchResult
from src.research_system.models.state import ResearchState


@pytest.mark.asyncio
async def test_director_agent():
    llm = MockProvider()
    agent = DirectorAgent(llm)
    state = ResearchState(research_id="test_dir", topic="High Bandwidth Memory HBM4")
    
    updated_state = await agent.execute(state)
    assert updated_state.plan is not None
    assert len(updated_state.plan.hypotheses) > 0
    assert len(updated_state.generated_queries) > 0


@pytest.mark.asyncio
async def test_query_planner_agent():
    llm = MockProvider()
    agent = QueryPlannerAgent(llm)
    state = ResearchState(research_id="test_qp", topic="Post Quantum Cryptography")
    
    updated_state = await agent.execute(state)
    assert len(updated_state.generated_queries) >= 3


@pytest.mark.asyncio
async def test_retriever_agent():
    llm = MockProvider()
    agent = RetrieverAgent(llm)
    state = ResearchState(
        research_id="test_ret",
        topic="Neuromorphic Computing",
        generated_queries=["Neuromorphic Computing architectures benchmarks"],
    )
    
    updated_state = await agent.execute(state)
    assert len(updated_state.raw_search_results) > 0


@pytest.mark.asyncio
async def test_fact_checker_agent():
    llm = MockProvider()
    agent = FactCheckerAgent(llm)
    state = ResearchState(
        research_id="test_fc",
        topic="AI Chips",
        raw_search_results=[
            SearchResult(
                title="AI Chip Latency Report",
                url="https://ieee.org/ai-chips",
                snippet="Throughput increased by 3.2x with specialized systolic arrays.",
            )
        ]
    )
    
    updated_state = await agent.execute(state)
    assert len(updated_state.verified_facts) > 0
    assert updated_state.verified_facts[0].confidence_score >= 70.0


@pytest.mark.asyncio
async def test_peer_reviewer_agent():
    llm = MockProvider()
    agent = PeerReviewerAgent(llm)
    state = ResearchState(
        research_id="test_pr",
        topic="AI Chips",
        draft_report="# AI Chip Scalability\n\nDetailed empirical analysis of systolic array efficiency.",
    )
    
    updated_state = await agent.execute(state)
    assert updated_state.review_result is not None
    assert updated_state.review_result.total_score >= 85.0
