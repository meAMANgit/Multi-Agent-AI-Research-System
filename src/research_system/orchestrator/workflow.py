"""Multi-agent execution graph orchestrator with feedback loops and real-time event streaming."""

import asyncio
from datetime import datetime, timezone
import logging
from typing import Callable, List, Optional
import uuid

from src.research_system.agents.data_analyst import DataAnalystAgent
from src.research_system.agents.director import DirectorAgent
from src.research_system.agents.fact_checker import FactCheckerAgent
from src.research_system.agents.peer_reviewer import PeerReviewerAgent
from src.research_system.agents.query_planner import QueryPlannerAgent
from src.research_system.agents.report_writer import ReportWriterAgent
from src.research_system.agents.retriever import RetrieverAgent
from src.research_system.config.settings import Settings, get_settings
from src.research_system.llm.cost_tracker import CostTracker
from src.research_system.llm.provider import BaseLLMClient, get_llm_client
from src.research_system.models.enums import LLMProvider, ResearchDepth, ReviewStatus, TaskStatus
from src.research_system.models.schemas import AgentThought, ResearchRequest, ResearchResponse, utc_now
from src.research_system.models.state import ResearchState

logger = logging.getLogger("research_system.orchestrator")


class MultiAgentResearchWorkflow:
    """Enterprise multi-agent graph orchestrator."""

    def __init__(
        self,
        llm_client: Optional[BaseLLMClient] = None,
        provider: LLMProvider = LLMProvider.GOOGLE,
        settings: Optional[Settings] = None,
    ):
        self.settings = settings or get_settings()
        self.cost_tracker = CostTracker()
        self.llm = llm_client or get_llm_client(provider=provider, settings=self.settings)
        
        # Initialize the 7 specialized research agents
        self.director = DirectorAgent(self.llm, self.settings)
        self.query_planner = QueryPlannerAgent(self.llm, self.settings)
        self.retriever = RetrieverAgent(self.llm, self.settings)
        self.fact_checker = FactCheckerAgent(self.llm, self.settings)
        self.data_analyst = DataAnalystAgent(self.llm, self.settings)
        self.report_writer = ReportWriterAgent(self.llm, self.settings)
        self.peer_reviewer = PeerReviewerAgent(self.llm, self.settings)

    async def run_research(
        self,
        topic: str,
        depth: ResearchDepth = ResearchDepth.STANDARD,
        max_iterations: int = 2,
        on_thought_callback: Optional[Callable[[AgentThought], None]] = None,
    ) -> ResearchResponse:
        """Execute the end-to-end multi-agent research workflow."""
        research_id = str(uuid.uuid4())[:8]
        state = ResearchState(
            research_id=research_id,
            topic=topic,
            depth=depth.value if isinstance(depth, ResearchDepth) else str(depth),
            max_iterations=max_iterations,
            status=TaskStatus.PLANNING,
        )

        if on_thought_callback:
            state.register_callback(on_thought_callback)

        logger.info("Starting ResearchCore AI workflow [ID: %s] for topic: '%s'", research_id, topic)
        state.add_thought("Orchestrator", "Session Initialized", f"Initialized multi-agent research team for topic: '{topic}'")

        try:
            for iteration in range(max_iterations):
                state.iteration = iteration
                
                # 1. Lead Research Director (Strategy & Breakdown)
                state = await self.director.execute(state)
                
                # 2. Search Query Planner (Vector expansion)
                state = await self.query_planner.execute(state)
                
                # 3. Web & Academic Retriever (Search & Scrape)
                state = await self.retriever.execute(state)
                
                # 4 & 5. Concurrently run Fact Checker and Quantitative Data Analyst
                fact_task = self.fact_checker.execute(state)
                analyst_task = self.data_analyst.execute(state)
                await asyncio.gather(fact_task, analyst_task)
                
                # 6. Research Synthesis Author (Report Generation)
                state = await self.report_writer.execute(state)
                
                # 7. Peer Reviewer & QA (Rubric Evaluation)
                state = await self.peer_reviewer.execute(state)
                
                # Check review decision
                if state.review_result and state.review_result.status == ReviewStatus.APPROVED:
                    state.add_thought(
                        "Orchestrator",
                        "Quality Threshold Achieved",
                        f"Report approved on iteration {iteration + 1} with score {state.review_result.total_score}/100.",
                    )
                    break
                elif iteration < max_iterations - 1:
                    state.add_thought(
                        "Orchestrator",
                        "Triggering Revision Loop",
                        f"Iterating (round {iteration + 2}/{max_iterations}) to improve score {state.review_result.total_score if state.review_result else 0}/100.",
                    )

            state.status = TaskStatus.COMPLETED
            state.end_time = utc_now()
            state.total_tokens = self.llm.cost_tracker.total_tokens
            state.estimated_cost_usd = self.llm.cost_tracker.total_cost_usd

        except Exception as err:
            logger.exception("Workflow failed during execution: %s", err)
            state.status = TaskStatus.FAILED
            state.error = str(err)
            state.end_time = utc_now()
            if not state.final_report:
                state.final_report = f"# Research Report Generation Incomplete\n\nAn error occurred during multi-agent execution:\n`{err}`"

        # Construct final validated response
        return ResearchResponse(
            research_id=state.research_id,
            topic=state.topic,
            status=state.status,
            plan=state.plan,
            markdown_report=state.final_report or state.draft_report or "",
            sources=state.raw_search_results,
            verified_facts=state.verified_facts,
            quantitative_data=state.quantitative_data,
            review_result=state.review_result,
            iterations_completed=state.iteration + 1,
            total_tokens=state.total_tokens,
            estimated_cost_usd=state.estimated_cost_usd,
            execution_time_seconds=state.elapsed_seconds,
        )
