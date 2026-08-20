"""Token usage, cost estimation, and latency telemetry tracker."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class LLMMetrics:
    """Telemetry metrics for an individual LLM call."""
    provider: str
    model: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    latency_ms: float
    cost_usd: float
    timestamp: datetime = field(default_factory=utc_now)


class CostTracker:
    """Calculates and monitors token consumption and cost across LLM providers."""

    # Cost per 1k tokens (input, output) in USD
    PRICING_TABLE = {
        "gemini-2.5-flash": (0.000075, 0.0003),
        "gemini-1.5-pro": (0.00125, 0.005),
        "gpt-4o": (0.0025, 0.010),
        "gpt-4o-mini": (0.00015, 0.0006),
        "claude-3-5-sonnet": (0.003, 0.015),
        "groq-llama-3.3-70b": (0.00059, 0.00079),
        "ollama": (0.0, 0.0),
        "mock": (0.0, 0.0),
    }

    def __init__(self):
        self.call_history: List[LLMMetrics] = []

    def record_usage(
        self,
        provider: str,
        model: str,
        prompt_tokens: int,
        completion_tokens: int,
        latency_ms: float = 0.0,
    ) -> LLMMetrics:
        """Record token usage and compute approximate cost."""
        total_tokens = prompt_tokens + completion_tokens
        
        # Match pricing
        model_key = next((k for k in self.PRICING_TABLE if k in model.lower()), "gemini-2.5-flash")
        input_price_per_k, output_price_per_k = self.PRICING_TABLE.get(model_key, (0.0001, 0.0005))
        
        cost_usd = (prompt_tokens / 1000.0 * input_price_per_k) + (
            completion_tokens / 1000.0 * output_price_per_k
        )

        metric = LLMMetrics(
            provider=provider,
            model=model,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
            latency_ms=latency_ms,
            cost_usd=cost_usd,
        )
        self.call_history.append(metric)
        return metric

    @property
    def total_tokens(self) -> int:
        return sum(m.total_tokens for m in self.call_history)

    @property
    def total_cost_usd(self) -> float:
        return sum(m.cost_usd for m in self.call_history)

    def get_summary(self) -> Dict[str, float]:
        return {
            "total_calls": len(self.call_history),
            "total_tokens": self.total_tokens,
            "total_cost_usd": round(self.total_cost_usd, 6),
            "avg_latency_ms": (
                round(sum(m.latency_ms for m in self.call_history) / len(self.call_history), 2)
                if self.call_history
                else 0.0
            ),
        }
