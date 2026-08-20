"""Streamlit Web Application: Real-time interactive multi-agent research dashboard."""

import asyncio
import os
import sys
import time

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

import streamlit as st
from src.research_system.exporters.html_exporter import HTMLExporter
from src.research_system.exporters.json_exporter import JSONExporter
from src.research_system.exporters.markdown_exporter import MarkdownExporter
from src.research_system.models.enums import LLMProvider, ResearchDepth, ReviewStatus
from src.research_system.models.schemas import AgentThought, ResearchResponse
from src.research_system.orchestrator.workflow import MultiAgentResearchWorkflow

st.set_page_config(
    page_title="ResearchCore AI - Autonomous Multi-Agent Research System",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for dark glassmorphic styling
st.markdown("""
<style>
    .main { background-color: #0d1117; }
    .stApp { background: radial-gradient(circle at top right, #161b22, #0d1117); color: #e6edf3; }
    .agent-card {
        background: rgba(22, 27, 34, 0.85);
        border: 1px solid rgba(48, 54, 61, 0.8);
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 0.75rem;
        border-left: 4px solid #58a6ff;
        backdrop-filter: blur(8px);
    }
    .agent-director { border-left-color: #bc8cff; }
    .agent-planner { border-left-color: #79c0ff; }
    .agent-retriever { border-left-color: #56d364; }
    .agent-checker { border-left-color: #e3b341; }
    .agent-analyst { border-left-color: #f778ba; }
    .agent-writer { border-left-color: #388bfd; }
    .agent-reviewer { border-left-color: #2ea043; }
    .metric-box {
        background: rgba(22, 27, 34, 0.7);
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
    }
    .metric-val { font-size: 1.8rem; font-weight: 700; color: #58a6ff; font-family: monospace; }
    .metric-lbl { font-size: 0.8rem; color: #8b949e; text-transform: uppercase; letter-spacing: 0.05em; }
</style>
""", unsafe_allow_html=True)


def run_app():
    """Main Streamlit execution loop."""
    # Sidebar: Configurations
    with st.sidebar:
        st.markdown("## ⚙️ Research Controls")
        
        provider_choice = st.selectbox(
            "LLM Provider",
            options=[LLMProvider.GOOGLE.value, LLMProvider.OPENAI.value, LLMProvider.GROQ.value, LLMProvider.OLLAMA.value, LLMProvider.MOCK.value],
            index=0,
            help="Select provider. If no API key is in environment, fallback Mock engine executes deterministically at zero cost.",
        )
        
        depth_choice = st.selectbox(
            "Research Depth",
            options=[ResearchDepth.QUICK.value, ResearchDepth.STANDARD.value, ResearchDepth.DEEP.value, ResearchDepth.EXHAUSTIVE.value],
            index=1,
            help="Determines number of search vectors and extraction depth.",
        )
        
        max_iterations = st.slider("Max QA Feedback Iterations", min_value=1, max_value=4, value=2)
        
        st.markdown("---")
        st.markdown("### 🤖 Multi-Agent Team")
        st.markdown("""
        1. 🎯 **Lead Director**
        2. 🧭 **Query Planner**
        3. 🌐 **Academic Retriever**
        4. 🔍 **Fact Checker**
        5. 📊 **Data Analyst**
        6. ✍️ **Report Writer**
        7. ⚖️ **Peer Reviewer (QA)**
        """)

    # Main Area
    st.markdown("# 🔬 ResearchCore AI")
    st.markdown("##### *Autonomous Multi-Agent Deep Research & Executive Intelligence Engine*")
    st.markdown("---")

    # Sample Presets
    st.markdown("💡 **Sample Research Prompts:**")
    col_p1, col_p2, col_p3 = st.columns(3)
    sample_topic = None
    if col_p1.button("🔋 Next-Gen Solid State Batteries"):
        sample_topic = "Next-Generation Solid State Battery Commercialization & Electrolyte Innovations"
    if col_p2.button("🧠 Autonomous Multi-Agent AI"):
        sample_topic = "Autonomous Multi-Agent AI Architectures for Enterprise Decision Automation"
    if col_p3.button("🛡️ Post-Quantum Cryptography"):
        sample_topic = "Post-Quantum Cryptography Migration Roadmaps and NIST Standards"

    default_val = sample_topic if sample_topic else ""
    topic_input = st.text_area(
        "Enter your research inquiry, hypothesis, or technical question:",
        value=default_val,
        placeholder="e.g. Comparative analysis of High-Bandwidth Memory (HBM3e/HBM4) architectures for LLM training clusters...",
        height=100,
    )

    start_button = st.button("🚀 Launch Autonomous Research", type="primary", use_container_width=True)

    if start_button and topic_input.strip():
        # Live Thought Feed Container
        thought_container = st.empty()
        progress_bar = st.progress(0, text="Initializing multi-agent team...")
        
        thoughts_list = []

        def handle_thought(thought: AgentThought):
            thoughts_list.append(thought)
            with thought_container.container():
                st.markdown("### ⚡ Live Multi-Agent Reasoning Stream")
                for t in thoughts_list[-6:]:
                    agent_cls = "agent-card"
                    if "Director" in t.agent_name:
                        agent_cls += " agent-director"
                    elif "Planner" in t.agent_name:
                        agent_cls += " agent-planner"
                    elif "Retriever" in t.agent_name:
                        agent_cls += " agent-retriever"
                    elif "Fact" in t.agent_name:
                        agent_cls += " agent-checker"
                    elif "Analyst" in t.agent_name:
                        agent_cls += " agent-analyst"
                    elif "Writer" in t.agent_name:
                        agent_cls += " agent-writer"
                    elif "Reviewer" in t.agent_name:
                        agent_cls += " agent-reviewer"
                    
                    st.markdown(f"""
                    <div class="{agent_cls}">
                        <strong>[{t.agent_name}]</strong> &nbsp; <code>{t.step}</code><br/>
                        <span style="color: #c9d1d9;">{t.thought}</span>
                    </div>
                    """, unsafe_allow_html=True)

        workflow = MultiAgentResearchWorkflow(provider=LLMProvider(provider_choice))
        
        progress_bar.progress(20, text="Agents formulating hypotheses and search vectors...")
        
        # Run asynchronous workflow
        response: ResearchResponse = asyncio.run(
            workflow.run_research(
                topic=topic_input.strip(),
                depth=ResearchDepth(depth_choice),
                max_iterations=max_iterations,
                on_thought_callback=handle_thought,
            )
        )
        
        progress_bar.progress(100, text="Research Completed Successfully!")
        time.sleep(0.5)
        progress_bar.empty()

        # Save into session state
        st.session_state["latest_research"] = response

    # Display Results if available
    if "latest_research" in st.session_state:
        res: ResearchResponse = st.session_state["latest_research"]
        
        st.markdown("---")
        st.markdown(f"## 📑 Research Dossier: `{res.topic}`")
        
        # Summary Metrics
        m1, m2, m3, m4, m5 = st.columns(5)
        with m1:
            score = res.review_result.total_score if res.review_result else 0.0
            st.markdown(f"""<div class="metric-box"><div class="metric-val">{score}/100</div><div class="metric-lbl">QA Score</div></div>""", unsafe_allow_html=True)
        with m2:
            st.markdown(f"""<div class="metric-box"><div class="metric-val">{len(res.sources)}</div><div class="metric-lbl">Sources Cites</div></div>""", unsafe_allow_html=True)
        with m3:
            st.markdown(f"""<div class="metric-box"><div class="metric-val">{len(res.verified_facts)}</div><div class="metric-lbl">Verified Facts</div></div>""", unsafe_allow_html=True)
        with m4:
            st.markdown(f"""<div class="metric-box"><div class="metric-val">{round(res.execution_time_seconds, 2)}s</div><div class="metric-lbl">Duration</div></div>""", unsafe_allow_html=True)
        with m5:
            st.markdown(f"""<div class="metric-box"><div class="metric-val">{res.iterations_completed}</div><div class="metric-lbl">Iterations</div></div>""", unsafe_allow_html=True)

        st.markdown("<br/>", unsafe_allow_html=True)

        # Tabs for Output
        tab_report, tab_evidence, tab_metrics, tab_qa, tab_export = st.tabs([
            "📖 Comprehensive Report",
            "🔍 Verified Evidence Ledger",
            "📊 Quantitative Benchmarks",
            "⚖️ Peer Review & Rubrics",
            "💾 Export & Graph",
        ])

        with tab_report:
            st.markdown(res.markdown_report)

        with tab_evidence:
            st.markdown(f"### 🛡️ Verified Facts & Evidence Ledger ({len(res.verified_facts)})")
            if res.verified_facts:
                for f in res.verified_facts:
                    with st.container():
                        st.markdown(f"**[{f.category}]** {f.statement}")
                        st.caption(f"Source: [{f.source_title}]({f.source_url}) • Confidence Index: {f.confidence_score}%")
                        st.divider()
            else:
                st.info("No discrete facts were parsed for this topic.")

        with tab_metrics:
            st.markdown("### 📈 Quantitative Benchmarks & Extracted Metrics")
            if res.quantitative_data:
                for m in res.quantitative_data:
                    st.metric(label=f"{m.metric_name} ({m.year_or_period or 'Metric'})", value=m.value, help=m.context)
                    st.caption(f"Context: {m.context}")
            else:
                st.info("No quantitative data points detected.")

        with tab_qa:
            if res.review_result:
                rev = res.review_result
                st.markdown(f"### 🎯 Peer Review QA Audit — Overall Score: `{rev.total_score}/100`")
                st.markdown(f"**Evaluation Status:** `{rev.status.value}`")
                
                dim_col1, dim_col2 = st.columns(2)
                with dim_col1:
                    st.markdown("#### Dimension Breakdown (Max 20 each)")
                    st.write(f"- **Technical Depth:** {rev.dimension_scores.technical_depth}/20")
                    st.write(f"- **Factual Accuracy:** {rev.dimension_scores.factual_accuracy}/20")
                    st.write(f"- **Structural Flow:** {rev.dimension_scores.structural_flow}/20")
                    st.write(f"- **Citation Validity:** {rev.dimension_scores.citation_validity}/20")
                    st.write(f"- **Objectivity:** {rev.dimension_scores.objectivity}/20")
                
                with dim_col2:
                    st.markdown("#### Key Strengths")
                    for s in rev.strengths:
                        st.write(f"✅ {s}")
                    if rev.weaknesses:
                        st.markdown("#### Areas for Refinement")
                        for w in rev.weaknesses:
                            st.write(f"⚠️ {w}")

                st.info(f"**Actionable Auditor Feedback:** {rev.actionable_feedback}")

        with tab_export:
            st.markdown("### 📦 Export Executive Intelligence Dossier")
            exp_c1, exp_c2, exp_c3 = st.columns(3)
            
            md_content = MarkdownExporter.export_to_string(res)
            html_content = HTMLExporter.export_to_string(res)
            json_content = JSONExporter.export_to_string(res)

            exp_c1.download_button(
                label="📄 Download Markdown (.md)",
                data=md_content,
                file_name=f"research_report_{res.research_id}.md",
                mime="text/markdown",
                use_container_width=True,
            )

            exp_c2.download_button(
                label="🌐 Download Interactive HTML (.html)",
                data=html_content,
                file_name=f"research_report_{res.research_id}.html",
                mime="text/html",
                use_container_width=True,
            )

            exp_c3.download_button(
                label="📊 Download Knowledge Graph (.json)",
                data=json_content,
                file_name=f"knowledge_graph_{res.research_id}.json",
                mime="application/json",
                use_container_width=True,
            )


if __name__ == "__main__":
    run_app()
