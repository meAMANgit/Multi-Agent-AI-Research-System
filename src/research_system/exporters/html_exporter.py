"""Interactive, standalone HTML intelligence dashboard exporter with dark/light styling."""

import html
import json
import os
from src.research_system.models.schemas import ResearchResponse


class HTMLExporter:
    """Exports research response to an interactive standalone HTML whitepaper."""

    @classmethod
    def export_to_string(cls, response: ResearchResponse) -> str:
        """Render self-contained HTML page with embedded CSS, charts, and facts ledger."""
        topic_escaped = html.escape(response.topic)
        score = response.review_result.total_score if response.review_result else 0.0
        
        # Format facts
        facts_html = ""
        for f in response.verified_facts:
            facts_html += f"""
            <div class="fact-card">
                <div class="fact-header">
                    <span class="fact-badge">{html.escape(f.category)}</span>
                    <span class="fact-confidence">Confidence: {f.confidence_score}%</span>
                </div>
                <p class="fact-statement">{html.escape(f.statement)}</p>
                <div class="fact-source">Source: <a href="{html.escape(f.source_url)}" target="_blank">{html.escape(f.source_title)}</a></div>
            </div>
            """

        # Format quantitative metrics
        metrics_html = ""
        for m in response.quantitative_data:
            metrics_html += f"""
            <div class="metric-card">
                <div class="metric-value">{html.escape(m.value)}</div>
                <div class="metric-name">{html.escape(m.metric_name)}</div>
                <div class="metric-context">{html.escape(m.context)}</div>
            </div>
            """

        # Simple markdown to HTML line-by-line conversion for the report body
        report_lines = response.markdown_report.splitlines()
        rendered_body = []
        in_code = False
        for line in report_lines:
            if line.startswith("```"):
                if in_code:
                    rendered_body.append("</pre>")
                    in_code = False
                else:
                    rendered_body.append("<pre><code>")
                    in_code = True
            elif in_code:
                rendered_body.append(html.escape(line))
            elif line.startswith("# "):
                rendered_body.append(f"<h1>{html.escape(line[2:])}</h1>")
            elif line.startswith("## "):
                rendered_body.append(f"<h2>{html.escape(line[3:])}</h2>")
            elif line.startswith("### "):
                rendered_body.append(f"<h3>{html.escape(line[4:])}</h3>")
            elif line.startswith("- "):
                rendered_body.append(f"<li>{html.escape(line[2:])}</li>")
            elif line.strip() == "---":
                rendered_body.append("<hr/>")
            elif line.strip():
                rendered_body.append(f"<p>{html.escape(line)}</p>")

        body_html = "\n".join(rendered_body)

        return f"""<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ResearchCore AI Report: {topic_escaped}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-primary: #0a0e17;
            --bg-secondary: #111827;
            --bg-card: rgba(31, 41, 55, 0.65);
            --border-color: rgba(75, 85, 99, 0.4);
            --text-primary: #f3f4f6;
            --text-secondary: #9ca3af;
            --accent-cyan: #00f2fe;
            --accent-blue: #4facfe;
            --accent-green: #10b981;
            --accent-purple: #8b5cf6;
        }}
        [data-theme="light"] {{
            --bg-primary: #f8fafc;
            --bg-secondary: #ffffff;
            --bg-card: #ffffff;
            --border-color: #e2e8f0;
            --text-primary: #0f172a;
            --text-secondary: #64748b;
            --accent-cyan: #0284c7;
            --accent-blue: #2563eb;
            --accent-green: #059669;
            --accent-purple: #7c3aed;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: 'Inter', -apple-system, sans-serif;
            background-color: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.65;
            padding: 2rem 1rem;
        }}
        .container {{
            max-width: 1100px;
            margin: 0 auto;
        }}
        header {{
            background: linear-gradient(135deg, rgba(79, 172, 254, 0.15), rgba(0, 242, 254, 0.15));
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 2.5rem;
            margin-bottom: 2rem;
            backdrop-filter: blur(12px);
        }}
        .badge-row {{
            display: flex;
            gap: 0.75rem;
            flex-wrap: wrap;
            margin-bottom: 1rem;
        }}
        .badge {{
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.8rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        .badge-score {{ background: rgba(16, 185, 129, 0.2); color: var(--accent-green); border: 1px solid var(--accent-green); }}
        .badge-id {{ background: rgba(139, 92, 246, 0.2); color: var(--accent-purple); }}
        .title {{ font-size: 2.2rem; font-weight: 800; margin-bottom: 0.5rem; background: linear-gradient(to right, #4facfe, #00f2fe); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
        .meta-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-top: 1.5rem; }}
        .meta-item {{ background: var(--bg-card); padding: 1rem; border-radius: 8px; border: 1px solid var(--border-color); }}
        .meta-label {{ font-size: 0.75rem; color: var(--text-secondary); text-transform: uppercase; }}
        .meta-value {{ font-size: 1.1rem; font-weight: 700; color: var(--text-primary); }}
        
        .metrics-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1rem; margin: 2rem 0; }}
        .metric-card {{ background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 12px; padding: 1.5rem; text-align: center; }}
        .metric-value {{ font-size: 2rem; font-weight: 800; color: var(--accent-cyan); font-family: 'JetBrains Mono', monospace; }}
        .metric-name {{ font-size: 0.9rem; font-weight: 600; margin: 0.25rem 0; }}
        .metric-context {{ font-size: 0.8rem; color: var(--text-secondary); }}

        .report-content {{
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 3rem;
            margin-bottom: 2rem;
        }}
        .report-content h1 {{ font-size: 1.8rem; margin: 1.5rem 0 1rem; color: var(--accent-blue); }}
        .report-content h2 {{ font-size: 1.4rem; margin: 1.25rem 0 0.75rem; border-bottom: 1px solid var(--border-color); padding-bottom: 0.4rem; }}
        .report-content h3 {{ font-size: 1.15rem; margin: 1rem 0 0.5rem; }}
        .report-content p {{ margin-bottom: 1rem; color: var(--text-primary); }}
        .report-content li {{ margin-left: 1.5rem; margin-bottom: 0.5rem; }}
        pre {{ background: #000; padding: 1rem; border-radius: 8px; overflow-x: auto; margin: 1rem 0; font-family: 'JetBrains Mono', monospace; font-size: 0.88rem; }}

        .facts-section {{ margin-top: 2rem; }}
        .fact-card {{ background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 10px; padding: 1.25rem; margin-bottom: 0.75rem; }}
        .fact-header {{ display: flex; justify-content: space-between; margin-bottom: 0.5rem; }}
        .fact-badge {{ font-size: 0.75rem; background: rgba(79, 172, 254, 0.2); color: var(--accent-cyan); padding: 0.2rem 0.5rem; border-radius: 4px; font-weight: 600; }}
        .fact-confidence {{ font-size: 0.75rem; color: var(--accent-green); font-weight: 600; }}
        .fact-statement {{ font-size: 0.95rem; margin-bottom: 0.5rem; }}
        .fact-source {{ font-size: 0.8rem; color: var(--text-secondary); }}
        .fact-source a {{ color: var(--accent-cyan); text-decoration: none; }}
        .fact-source a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="badge-row">
                <span class="badge badge-score">QA Score: {score}/100</span>
                <span class="badge badge-id">ID: {response.research_id}</span>
                <span class="badge" style="background: rgba(255,255,255,0.1);">{response.iterations_completed} Iterations</span>
            </div>
            <h1 class="title">{topic_escaped}</h1>
            <p style="color: var(--text-secondary);">Synthesized by ResearchCore AI Autonomous Multi-Agent Deep Research System</p>
            
            <div class="meta-grid">
                <div class="meta-item">
                    <div class="meta-label">Sources Indexed</div>
                    <div class="meta-value">{len(response.sources)}</div>
                </div>
                <div class="meta-item">
                    <div class="meta-label">Verified Facts</div>
                    <div class="meta-value">{len(response.verified_facts)}</div>
                </div>
                <div class="meta-item">
                    <div class="meta-label">Execution Time</div>
                    <div class="meta-value">{round(response.execution_time_seconds, 2)}s</div>
                </div>
                <div class="meta-item">
                    <div class="meta-label">Total Tokens</div>
                    <div class="meta-value">{response.total_tokens:,}</div>
                </div>
            </div>
        </header>

        {f'<div class="metrics-grid">{metrics_html}</div>' if metrics_html else ''}

        <main class="report-content">
            {body_html}
        </main>

        {f'<section class="facts-section"><h2>Verified Evidence Ledger ({len(response.verified_facts)})</h2>{facts_html}</section>' if facts_html else ''}
    </div>
</body>
</html>"""

    @classmethod
    def export_to_file(cls, response: ResearchResponse, output_path: str) -> str:
        """Save HTML report to disk."""
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        content = cls.export_to_string(response)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        return output_path
