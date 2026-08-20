"""Citation verification, domain authority scoring, and bibliography formatting."""

import re
from typing import Dict, List
from urllib.parse import urlparse
from src.research_system.models.schemas import ExtractedFact, SearchResult


class CitationTools:
    """Manages citation scoring, authority analysis, and IEEE/APA formatting."""

    DOMAIN_AUTHORITY_WEIGHTS: Dict[str, float] = {
        "arxiv.org": 98.0,
        "nature.com": 97.0,
        "ieee.org": 97.0,
        "acm.org": 96.0,
        "wikipedia.org": 90.0,
        "github.com": 86.0,
        "bloomberg.com": 89.0,
        "reuters.com": 92.0,
        "techcrunch.com": 82.0,
    }

    @classmethod
    def calculate_domain_authority(cls, url: str) -> float:
        """Estimate domain credibility score based on domain name and TLD."""
        if not url:
            return 70.0
        try:
            parsed = urlparse(url)
            hostname = (parsed.hostname or "").lower()
            
            # Check specific authoritative domains first
            for domain, score in cls.DOMAIN_AUTHORITY_WEIGHTS.items():
                if domain in hostname:
                    return score
            
            # Generic TLD fallback
            if hostname.endswith(".gov"):
                return 98.0
            if hostname.endswith(".edu"):
                return 96.0
            if hostname.endswith(".org"):
                return 88.0
        except Exception:
            pass
        return 78.0

    @classmethod
    def format_ieee_citations(cls, sources: List[SearchResult]) -> str:
        """Format sources into a structured IEEE-style numbered bibliography."""
        if not sources:
            return "_No external sources cited._"

        lines = []
        for idx, src in enumerate(sources, 1):
            domain = urlparse(src.url).netloc if src.url else "Web Source"
            title = src.title or "Online Research Document"
            score = round(src.credibility_score, 1)
            lines.append(f"[{idx}] {title}. *{domain}*. Available at: <{src.url}> (Reliability Index: {score}/100)")
        
        return "\n".join(lines)
