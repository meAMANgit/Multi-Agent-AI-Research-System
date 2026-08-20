"""Academic & Web Retrieval Agent: Multi-source web search and deep article scraping."""

import asyncio
from typing import List, Optional
from src.research_system.agents.base import BaseAgent
from src.research_system.models.enums import AgentRole, TaskStatus
from src.research_system.models.schemas import SearchResult
from src.research_system.models.state import ResearchState
from src.research_system.tools.citation_tools import CitationTools
from src.research_system.tools.crawler import AsyncWebCrawler
from src.research_system.tools.search_tools import SearchTools


class RetrieverAgent(BaseAgent):
    """Executes multi-source search vectors and scrapes high-signal markdown articles."""

    def __init__(self, llm_client, settings=None):
        super().__init__(AgentRole.RETRIEVER, llm_client, settings)
        self.search_tools = SearchTools(self.settings)
        self.crawler = AsyncWebCrawler(self.settings)

    async def execute(self, state: ResearchState) -> ResearchState:
        state.status = TaskStatus.SEARCHING
        
        queries_to_run = state.generated_queries[-6:] if state.generated_queries else [state.topic]
        
        self.log_thought(
            state,
            step="Parallel Multi-Source Retrieval",
            thought=f"Executing {len(queries_to_run)} search vectors across DuckDuckGo, Wikipedia, and arXiv academic index.",
            data_preview={"queries": queries_to_run},
        )

        # 1. Search engines query execution
        search_tasks = [
            self.search_tools.execute_search(q, max_results=self.settings.MAX_SEARCH_RESULTS_PER_QUERY)
            for q in queries_to_run
        ]
        search_outputs = await asyncio.gather(*search_tasks, return_exceptions=True)

        new_results: List[SearchResult] = []
        for out in search_outputs:
            if isinstance(out, list):
                for res in out:
                    # Update domain authority score
                    res.domain_authority = CitationTools.calculate_domain_authority(res.url)
                    new_results.append(res)

        # Merge with existing, deduplicating by URL
        seen_urls = {r.url for r in state.raw_search_results}
        for r in new_results:
            if r.url not in seen_urls:
                seen_urls.add(r.url)
                state.raw_search_results.append(r)

        self.log_thought(
            state,
            step="Search Complete",
            thought=f"Retrieved {len(state.raw_search_results)} relevant sources across domains. Initiating deep crawling on top sources...",
        )

        # 2. Deep crawl top URLs for full content
        urls_to_crawl = [
            r.url for r in state.raw_search_results 
            if r.url.startswith("http") and r.url not in state.crawled_documents
        ][:5]

        if urls_to_crawl:
            crawled = await self.crawler.crawl_urls(urls_to_crawl, max_concurrency=3)
            for url, content in crawled.items():
                if content:
                    state.crawled_documents[url] = content
                    # Attach content preview to matching SearchResult
                    for res in state.raw_search_results:
                        if res.url == url:
                            res.full_content = content[:1500]

        self.log_thought(
            state,
            step="Crawling Finished",
            thought=f"Indexed {len(state.crawled_documents)} full-text articles into context memory.",
            data_preview={"indexed_urls": list(state.crawled_documents.keys())},
        )

        return state
