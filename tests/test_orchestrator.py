"""End-to-end multi-agent research workflow tests."""

import pytest
from src.research_system.llm.provider import MockProvider
from src.research_system.models.enums import ResearchDepth, TaskStatus
from src.research_system.orchestrator.workflow import MultiAgentResearchWorkflow


@pytest.mark.asyncio
async def test_full_workflow_execution():
    """Verify complete end-to-end workflow from topic to peer-reviewed whitepaper."""
    llm = MockProvider()
    workflow = MultiAgentResearchWorkflow(llm_client=llm)

    thoughts = []
    def record_thought(t):
        thoughts.append(t)

    response = await workflow.run_research(
        topic="Scalable Vector Symbolic Architectures for Autonomous AI",
        depth=ResearchDepth.QUICK,
        max_iterations=1,
        on_thought_callback=record_thought,
    )

    assert response.status == TaskStatus.COMPLETED
    assert response.research_id != ""
    assert len(response.markdown_report) > 200
    assert len(response.sources) > 0
    assert response.review_result is not None
    assert len(thoughts) >= 5
    assert response.execution_time_seconds >= 0.0
