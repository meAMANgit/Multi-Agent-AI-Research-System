"""Tools package init."""

try:
    from src.research_system.tools.crawler import AsyncWebCrawler, html_to_markdown
    from src.research_system.tools.search_tools import SearchTools
    from src.research_system.tools.data_extractor import DataExtractor
    from src.research_system.tools.citation_tools import CitationTools
except (ImportError, ModuleNotFoundError):
    from .crawler import AsyncWebCrawler, html_to_markdown
    from .search_tools import SearchTools
    from .data_extractor import DataExtractor
    from .citation_tools import CitationTools

__all__ = [
    "AsyncWebCrawler",
    "html_to_markdown",
    "SearchTools",
    "DataExtractor",
    "CitationTools",
]
