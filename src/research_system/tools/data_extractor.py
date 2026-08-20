"""Structured quantitative metrics, tables, and numerical data extractor."""

import re
from typing import List
from src.research_system.models.schemas import QuantitativeDataPoint


class DataExtractor:
    """Extracts numerical stats, benchmarks, CAGR, percentages, and financial metrics."""

    METRIC_PATTERNS = [
        # Percentage / Growth
        (r"(\b\d+(?:\.\d+)?%\s*(?:increase|decrease|growth|CAGR|reduction|gain|drop|accuracy|efficiency)?)", "Percentage / Rate"),
        # Dollar amounts
        (r"(\$\s*\d+(?:\.\d+)?\s*(?:billion|million|trillion|B|M|k)?\b)", "Financial Valuation / TAM"),
        # Speed / Latency / Throughput
        (r"(\b\d+(?:\.\d+)?\s*(?:ms|seconds|minutes|Gbps|Mbps|ops/sec|tps|TFLOPs|tokens/sec)\b)", "Performance Benchmark"),
        # Multipliers
        (r"(\b\d+(?:\.\d+)?x\s*(?:faster|speedup|improvement|higher|lower|scaling)?\b)", "Efficiency Multiplier"),
    ]

    @classmethod
    def extract_metrics(cls, text: str, source_url: str = "") -> List[QuantitativeDataPoint]:
        """Parse raw text for quantitative data points and metrics."""
        points: List[QuantitativeDataPoint] = []
        sentences = re.split(r"(?<=[.!?])\s+", text)
        
        seen_metrics = set()
        for sentence in sentences:
            sentence_clean = sentence.strip()
            if len(sentence_clean) < 15 or len(sentence_clean) > 300:
                continue
                
            for pattern, category in cls.METRIC_PATTERNS:
                matches = re.finditer(pattern, sentence_clean, re.IGNORECASE)
                for match in matches:
                    val = match.group(1).strip()
                    if val.lower() not in seen_metrics:
                        seen_metrics.add(val.lower())
                        points.append(
                            QuantitativeDataPoint(
                                metric_name=category,
                                value=val,
                                context=sentence_clean,
                                source_url=source_url,
                            )
                        )
                        if len(points) >= 12:
                            return points
        return points
