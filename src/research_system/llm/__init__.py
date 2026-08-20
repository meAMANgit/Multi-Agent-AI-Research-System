"""LLM module init."""

try:
    from src.research_system.llm.cost_tracker import CostTracker, LLMMetrics
    from src.research_system.llm.provider import (
        BaseLLMClient,
        GoogleProvider,
        OpenAICompatibleProvider,
        MockProvider,
        get_llm_client,
        clean_json_string,
    )
except (ImportError, ModuleNotFoundError):
    from .cost_tracker import CostTracker, LLMMetrics
    from .provider import (
        BaseLLMClient,
        GoogleProvider,
        OpenAICompatibleProvider,
        MockProvider,
        get_llm_client,
        clean_json_string,
    )

__all__ = [
    "CostTracker",
    "LLMMetrics",
    "BaseLLMClient",
    "GoogleProvider",
    "OpenAICompatibleProvider",
    "MockProvider",
    "get_llm_client",
    "clean_json_string",
]
