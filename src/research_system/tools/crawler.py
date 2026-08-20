"""Async web crawler with HTML-to-markdown parsing, bot-header spoofing, and rate-limiting."""

import asyncio
import logging
import re
from typing import Dict, List, Optional
from bs4 import BeautifulSoup
import httpx

from src.research_system.config.settings import Settings, get_settings

logger = logging.getLogger("research_system.tools.crawler")


def html_to_markdown(html_content: str, max_length: int = 6000) -> str:
    """Convert raw HTML body into clean, high-signal text/markdown."""
    soup = BeautifulSoup(html_content, "html.parser")
    
    # Remove irrelevant tags
    for element in soup(["script", "style", "nav", "footer", "header", "aside", "form", "noscript", "svg"]):
        element.decompose()
        
    # Prefer main article container if present
    main_article = soup.find("article") or soup.find("main") or soup.find("div", class_=re.compile(r"content|post|body", re.I)) or soup.body
    
    if not main_article:
        return ""
        
    # Extract text with line breaks
    text = main_article.get_text(separator="\n", strip=True)
    
    # Clean excessive whitespace and blank lines
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    cleaned_text = "\n\n".join(lines)
    
    # Truncate to avoid context window explosion
    if len(cleaned_text) > max_length:
        cleaned_text = cleaned_text[:max_length] + "\n\n... [Content Truncated for Brevity] ..."
        
    return cleaned_text


class AsyncWebCrawler:
    """Enterprise-grade async web crawler for document retrieval."""

    def __init__(self, settings: Optional[Settings] = None):
        self.settings = settings or get_settings()
        self.headers = {
            "User-Agent": self.settings.CRAWLER_USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        }

    async def fetch_url(self, url: str) -> Optional[str]:
        """Fetch and extract clean markdown content from a single URL."""
        # Avoid non-http URLs or huge binary files
        if not url.startswith("http"):
            return None
            
        try:
            async with httpx.AsyncClient(
                headers=self.headers,
                timeout=self.settings.REQUEST_TIMEOUT_SECONDS,
                follow_redirects=True,
                verify=False,
            ) as client:
                response = await client.get(url)
                if response.status_code == 200 and "text/html" in response.headers.get("content-type", ""):
                    return html_to_markdown(response.text)
                return None
        except Exception as err:
            logger.debug("Failed to fetch %s: %s", url, err)
            return None

    async def crawl_urls(self, urls: List[str], max_concurrency: int = 4) -> Dict[str, str]:
        """Concurrently fetch multiple URLs with bounded concurrency."""
        semaphore = asyncio.Semaphore(max_concurrency)
        results: Dict[str, str] = {}

        async def _bounded_fetch(u: str):
            async with semaphore:
                content = await self.fetch_url(u)
                if content:
                    results[u] = content

        tasks = [_bounded_fetch(u) for u in urls if u]
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
            
        return results
