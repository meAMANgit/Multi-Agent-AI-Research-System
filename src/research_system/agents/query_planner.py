"""Search Query Planner Agent: Multi-vector query formulation and expansion."""

from typing import List, Optional
from pydantic import BaseModel, Field
from src.research_system.agents.base import BaseAgent
from src.research_system.models.enums import AgentRole, TaskStatus
from src.research_system.models.schemas import SearchQueryItem
from src.research_system.models.state import ResearchState


class QueryExpansionSchema(BaseModel):
    queries: List[SearchQueryItem] = Field(default_factory=list)


class QueryPlannerAgent(BaseAgent):
    """Expands research vectors into specialized academic, market, and counter-argument search queries."""

    def __init__(self, llm_client, settings=None):
        super().__init__(AgentRole.QUERY_PLANNER, llm_client, settings)

    async def execute(self, state: ResearchState) -> ResearchState:
        state.status = TaskStatus.SEARCHING
        
        self.log_thought(
            state,
            step="Query Vector Expansion",
            thought=f"Generating specialized search queries across technical, market, academic, and failure-mode vectors.",
        )

        plan_summary = state.plan.primary_objective if state.plan else state.topic
        prompt = f"""Topic: {state.topic}
Research Objective: {plan_summary}
Existing Queries: {state.generated_queries}

Generate 4 to 6 highly targeted, specialized search queries covering:
1. Technical specifications, state-of-the-art architectures, and whitepapers
2. Market size, CAGR growth rates, industry valuation, and revenue metrics
3. Empirical benchmarks, latency, throughput, energy comparisons
4. Vulnerabilities, failure modes, counter-arguments, and regulatory barriers"""

        try:
            expanded = await self.llm.generate_structured(
                prompt=prompt,
                response_model=QueryExpansionSchema,
                system_instruction=self.system_prompt,
            )
            for item in expanded.queries:
                if item.query not in state.generated_queries:
                    state.generated_queries.append(item.query)
        except Exception as err:
            self.log_thought(state, step="Fallback Expansion", thought=f"Using core queries: {err}")
            # Ensure at least core query vectors exist
            if not state.generated_queries:
                state.generated_queries = [
                    f"{state.topic} architecture technical specifications",
                    f"{state.topic} market size growth CAGR report",
                    f"{state.topic} benchmarks performance comparison",
                ]

        self.log_thought(
            state,
            step="Vector Expansion Complete",
            thought=f"Prepared {len(state.generated_queries)} specialized queries for retrieval execution.",
            data_preview={"active_queries": state.generated_queries},
        )

        return state
