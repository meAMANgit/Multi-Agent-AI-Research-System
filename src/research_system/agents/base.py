"""Base agent abstraction with telemetry, logging, and error boundaries."""

import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from src.research_system.config.prompts import PROMPTS
from src.research_system.config.settings import Settings, get_settings
from src.research_system.llm.provider import BaseLLMClient
from src.research_system.models.enums import AgentRole
from src.research_system.models.state import ResearchState

logger = logging.getLogger("research_system.agent")


class BaseAgent(ABC):
    """Abstract base class for all specialist research agents."""

    def __init__(
        self,
        role: AgentRole,
        llm_client: BaseLLMClient,
        settings: Optional[Settings] = None,
    ):
        self.role = role
        self.llm = llm_client
        self.settings = settings or get_settings()
        self.system_prompt = PROMPTS.get(self._get_prompt_key(), {}).get("system", "")

    def _get_prompt_key(self) -> str:
        """Derive prompt dictionary key from agent role."""
        if self.role == AgentRole.DIRECTOR:
            return "director"
        elif self.role == AgentRole.QUERY_PLANNER:
            return "query_planner"
        elif self.role == AgentRole.RETRIEVER:
            return "retriever"
        elif self.role == AgentRole.FACT_CHECKER:
            return "fact_checker"
        elif self.role == AgentRole.DATA_ANALYST:
            return "data_analyst"
        elif self.role == AgentRole.REPORT_WRITER:
            return "report_writer"
        elif self.role == AgentRole.PEER_REVIEWER:
            return "peer_reviewer"
        return "director"

    def log_thought(
        self,
        state: ResearchState,
        step: str,
        thought: str,
        data_preview: Optional[Dict[str, Any]] = None,
    ):
        """Record thought into state feed and console log."""
        logger.info("[%s] %s: %s", self.role.value, step, thought)
        state.add_thought(
            agent_name=self.role.value,
            step=step,
            thought=thought,
            data_preview=data_preview,
        )

    @abstractmethod
    async def execute(self, state: ResearchState) -> ResearchState:
        """Execute the agent's primary task on the research state."""
        pass
