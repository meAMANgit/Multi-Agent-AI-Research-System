"""Research Report Writer & Synthesis Agent: Compiling executive whitepapers."""

from typing import Optional
from src.research_system.agents.base import BaseAgent
from src.research_system.models.enums import AgentRole, TaskStatus
from src.research_system.models.state import ResearchState
from src.research_system.tools.citation_tools import CitationTools


class ReportWriterAgent(BaseAgent):
    """Synthesizes verified facts, quantitative benchmarks, and architectures into a comprehensive whitepaper."""

    def __init__(self, llm_client, settings=None):
        super().__init__(AgentRole.REPORT_WRITER, llm_client, settings)

    async def execute(self, state: ResearchState) -> ResearchState:
        state.status = TaskStatus.WRITING
        
        self.log_thought(
            state,
            step="Deep Synthesis & Whitepaper Authoring",
            thought="Compiling verified facts, quantitative benchmarks, architectural breakdowns, SWOT trade-offs, and citations into an executive report.",
        )

        # 1. Format verified facts
        facts_text = "\n".join([f"- [{f.category}] {f.statement} (Source: {f.source_title}, Confidence: {f.confidence_score}%)" for f in state.verified_facts])
        
        # 2. Format quantitative benchmarks
        metrics_text = "\n".join([f"- **{m.metric_name}**: {m.value} ({m.context}) [{m.year_or_period or 'N/A'}]" for m in state.quantitative_data])
        
        # 3. Format bibliography
        citations_block = CitationTools.format_ieee_citations(state.raw_search_results)

        prompt = f"""Topic: {state.topic}
Research Objective: {state.plan.primary_objective if state.plan else state.topic}

Verified Empirical Evidence & Facts:
{facts_text if facts_text else "General industry research principles apply."}

Quantitative Benchmarks & Metrics:
{metrics_text if metrics_text else "High scalability and CAGR growth metrics apply."}

External Sources for Citations:
{citations_block}

Task: Write an exhaustive, authoritative, deeply technical, and structured research report.

Required Sections:
# Executive Intelligence Report: {state.topic}
## Executive Summary (Strategic highlights, core discoveries, key figures)
## 1. Technological Foundations & Architecture (Detailed technical mechanisms, components, state of the art)
## 2. Quantitative Benchmarks & Market Metrics (Include a comprehensive Markdown comparison table with metrics)
## 3. Comparative SWOT & Trade-Off Matrix (Detailed strengths, weaknesses, opportunities, threats)
## 4. Operational Roadblocks, Risks & Compliance (Scalability, security, ethical, regulatory challenges)
## 5. Strategic Roadmap & 5-Year Outlook (Actionable guidance for 1-yr, 3-yr, 5-yr horizons)
## References & Verified Citation Ledger (Include numbered citations referencing the sources above)

Ensure maximum technical depth, concrete figures, and scholarly rigor."""

        report_md = await self.llm.generate_text(
            prompt=prompt,
            system_instruction=self.system_prompt,
            temperature=0.3,
            max_tokens=6000,
        )

        # Ensure citations are properly included at bottom if truncated
        if "## References" not in report_md and "## Citations" not in report_md:
            report_md += f"\n\n---\n\n## References & Verified Citation Ledger\n\n{citations_block}\n"

        state.draft_report = report_md
        state.final_report = report_md

        self.log_thought(
            state,
            step="Draft Completed",
            thought=f"Authored executive whitepaper ({len(report_md.split())} words, {len(state.verified_facts)} verified citations). Forwarding to Peer Review QA...",
        )

        return state
