"""Exporters package init."""

try:
    from src.research_system.exporters.markdown_exporter import MarkdownExporter
    from src.research_system.exporters.html_exporter import HTMLExporter
    from src.research_system.exporters.json_exporter import JSONExporter
except (ImportError, ModuleNotFoundError):
    from .markdown_exporter import MarkdownExporter
    from .html_exporter import HTMLExporter
    from .json_exporter import JSONExporter

__all__ = [
    "MarkdownExporter",
    "HTMLExporter",
    "JSONExporter",
]
