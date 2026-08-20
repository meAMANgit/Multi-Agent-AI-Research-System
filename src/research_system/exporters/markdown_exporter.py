"""Markdown export formatter for research reports."""

import os
from src.research_system.models.schemas import ResearchResponse


class MarkdownExporter:
    """Exports research response to a formatted Markdown file."""

    @classmethod
    def export_to_string(cls, response: ResearchResponse) -> str:
        """Format complete research package as a Markdown document."""
        header = f"""---
title: "Research Report: {response.topic}"
research_id: "{response.research_id}"
status: "{response.status.value}"
quality_score: {response.review_result.total_score if response.review_result else 0.0}/100
iterations: {response.iterations_completed}
execution_time_seconds: {round(response.execution_time_seconds, 2)}s
generated_at: "{response.created_at.isoformat()}"
---

"""
        return header + response.markdown_report

    @classmethod
    def export_to_file(cls, response: ResearchResponse, output_path: str) -> str:
        """Save research markdown to disk."""
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        content = cls.export_to_string(response)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        return output_path
