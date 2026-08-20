"""Lead Research Director Agent: Task decomposition, planning, and loop steering."""

from typing import Optional
from src.research_system.agents.base import BaseAgent
from src.research_system.models.enums import AgentRole, TaskStatus
from src.research_system.models.schemas import ResearchPlan
from src.research_system.models.state import ResearchState


class DirectorAgent(BaseAgent):
    """Orchestrates research strategy, decomposes topics into hypotheses, and directs sub-agents."""

    def __init__(self, llm_client, settings=None):
        super().__init__(AgentRole.DIRECTOR, llm_client, settings)

    async def execute(self, state: ResearchState) -> ResearchState:
        state.status = TaskStatus.PLANNING
        
        # If this is a revision iteration triggered by QA Reviewer feedback
        if state.iteration > 0 and state.review_result:
            self.log_thought(
                state,
                step="Adaptive Strategy Revision",
                thought=f"Incorporating Peer Review critique (Score: {state.review_result.total_score}/100) to fill knowledge gaps.",
                data_preview={"actionable_feedback": state.review_result.actionable_feedback},
            )
            
            # Incorporate reviewer recommended queries
            if state.review_result.recommended_queries:
                for q in state.review_result.recommended_queries:
                    if q not in state.generated_queries:
                        state.generated_queries.append(q)
            return state

        # Initial research plan formulation
        self.log_thought(
            state,
            step="Strategic Decomposition",
            thought=f"Decomposing user research inquiry '{state.topic}' into multi-dimensional investigation plan.",
        )

        prompt = f"""Analyze this research topic and formulate a comprehensive research plan.
Topic: {state.topic}
Research Depth: {state.depth}
Target Deliverable: Enterprise-grade executive research whitepaper with benchmarks, architecture, SWOT, and citations.

Deconstruct into:
- Primary objective
- 3 key hypotheses
- 5 core target dimensions (Technical, Market, Benchmarks, Risks, Future)
- Initial prioritized search queries
- Estimated subtasks"""

        plan = await self.llm.generate_structured(
            prompt=prompt,
            response_model=ResearchPlan,
            system_instruction=self.system_prompt,
        )

        state.plan = plan
        state.generated_queries = list(plan.planned_queries)
        
        self.log_thought(
            state,
            step="Plan Finalized",
            thought=f"Formulated {len(plan.hypotheses)} hypotheses and {len(plan.planned_queries)} foundational search vectors across {len(plan.target_dimensions)} dimensions.",
            data_preview={"objective": plan.primary_objective, "queries": plan.planned_queries},
        )

        return state
