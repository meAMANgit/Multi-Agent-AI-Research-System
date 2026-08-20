"""Unit tests for research tools: crawler, search, extractor, citation scoring."""

import pytest
from src.research_system.tools.citation_tools import CitationTools
from src.research_system.tools.crawler import html_to_markdown
from src.research_system.tools.data_extractor import DataExtractor
from src.research_system.tools.search_tools import SearchTools


def test_html_to_markdown_cleaning():
    """Verify HTML cleaning and text extraction."""
    raw_html = """
    <html>
        <head><title>Test Page</title></head>
        <body>
            <script>alert('malicious')</script>
            <nav><a href="#">Nav item</a></nav>
            <article>
                <h1>Solid State Battery Breakthrough</h1>
                <p>New ceramic electrolytes exhibit 12 mS/cm ionic conductivity at room temperature.</p>
            </article>
            <footer>Copyright 2026</footer>
        </body>
    </html>
    """
    md = html_to_markdown(raw_html)
    assert "Solid State Battery Breakthrough" in md
    assert "12 mS/cm" in md
    assert "alert" not in md
    assert "Nav item" not in md


def test_data_extractor_metrics():
    """Test regex extraction of quantitative benchmarks."""
    sample_text = (
        "The market is projected to reach $58.7 billion by 2030, showing a 31.4% CAGR. "
        "Latency was measured at 28 ms under peak load, offering a 3.4x speedup."
    )
    points = DataExtractor.extract_metrics(sample_text)
    assert len(points) >= 3
    
    values = [p.value for p in points]
    assert any("31.4%" in v for v in values)
    assert any("$58.7 billion" in v for v in values)
    assert any("28 ms" in v for v in values)


def test_citation_tools_scoring():
    """Test domain authority calculation and bibliography generation."""
    edu_score = CitationTools.calculate_domain_authority("https://cs.stanford.edu/paper.pdf")
    assert edu_score >= 90.0

    arxiv_score = CitationTools.calculate_domain_authority("https://arxiv.org/abs/2401.1234")
    assert arxiv_score >= 95.0


@pytest.mark.asyncio
async def test_search_tools_fallback():
    """Test search tool fallback mechanics."""
    search_tool = SearchTools()
    hits = await search_tool.execute_search("Edge AI Inference Optimization", max_results=3)
    assert len(hits) > 0
    assert hits[0].url != ""
    assert hits[0].title != ""
