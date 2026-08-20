"""Enterprise Rich CLI for ResearchCore AI."""

import argparse
import asyncio
import os
import sys

# Reconfigure stdout/stderr for UTF-8 on Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.markdown import Markdown

from src.research_system.exporters.html_exporter import HTMLExporter
from src.research_system.exporters.json_exporter import JSONExporter
from src.research_system.exporters.markdown_exporter import MarkdownExporter
from src.research_system.models.enums import LLMProvider, ResearchDepth
from src.research_system.models.schemas import AgentThought
from src.research_system.orchestrator.workflow import MultiAgentResearchWorkflow

console = Console(force_terminal=True, legacy_windows=False)


def render_banner():
    """Print clean ASCII banner."""
    banner = """
======================================================================
  RESEARCHCORE AI - MULTI-AGENT DEEP RESEARCH SYSTEM v2.0
  Autonomous Team: Director | Planner | Retriever | FactChecker
                   DataAnalyst | ReportWriter | PeerReviewer
======================================================================
    """
    console.print(Panel(banner.strip(), style="bold cyan", expand=False))


async def run_cli_research(args):
    """Execute research workflow with live terminal feedback."""
    topic = args.topic
    if not topic:
        if args.interactive:
            topic = console.input("[bold yellow]Enter research inquiry / topic: [/bold yellow]").strip()
        else:
            console.print("[bold red]Error: Research topic must be provided via --topic or --interactive mode.[/bold red]")
            sys.exit(1)

    provider = LLMProvider(args.provider)
    depth = ResearchDepth(args.depth)
    max_iterations = args.iterations

    console.print(Panel(
        f"[bold white]Topic:[/bold white] {topic}\n"
        f"[bold white]Provider:[/bold white] {provider.value} | "
        f"[bold white]Depth:[/bold white] {depth.value} | "
        f"[bold white]Max Iterations:[/bold white] {max_iterations}",
        title="[bold green]Configuration[/bold green]",
        border_style="green",
    ))

    def on_thought(thought: AgentThought):
        console.print(f"  [dim cyan]>[/dim cyan] [bold cyan][{thought.agent_name}][/bold cyan] [bold white]{thought.step}:[/bold white] {thought.thought}")

    workflow = MultiAgentResearchWorkflow(provider=provider)

    with Progress(
        SpinnerColumn(spinner_name="dots"),
        TextColumn("[bold cyan]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Multi-Agent Team Collaborating...", total=None)
        response = await workflow.run_research(
            topic=topic,
            depth=depth,
            max_iterations=max_iterations,
            on_thought_callback=on_thought,
        )
        progress.update(task, description="[bold green]Research Finished!")

    # Display summary table
    table = Table(title="Research Execution Summary", border_style="cyan")
    table.add_column("Metric", style="bold white")
    table.add_column("Value", style="bold green")
    
    score = response.review_result.total_score if response.review_result else 0.0
    table.add_row("Session ID", response.research_id)
    table.add_row("Status", response.status.value.upper())
    table.add_row("QA Audit Score", f"{score}/100")
    table.add_row("Sources Indexed", str(len(response.sources)))
    table.add_row("Verified Facts", str(len(response.verified_facts)))
    table.add_row("Execution Duration", f"{round(response.execution_time_seconds, 2)}s")
    table.add_row("Total Tokens", f"{response.total_tokens:,}")
    table.add_row("Estimated Cost", f"${response.estimated_cost_usd:.5f}")

    console.print("\n")
    console.print(table)
    console.print("\n")

    # Output file handling
    if args.output:
        out_path = args.output
        fmt = args.format.lower()
        if fmt == "html":
            HTMLExporter.export_to_file(response, out_path)
        elif fmt == "json":
            JSONExporter.export_to_file(response, out_path)
        else:
            MarkdownExporter.export_to_file(response, out_path)
        console.print(f"[bold green]Successfully exported report to: [/bold green] [underline]{out_path}[/underline]")
    else:
        # Print formatted Markdown preview to console
        console.print(Panel(Markdown(response.markdown_report), title="[bold blue]Final Research Report[/bold blue]", border_style="blue"))


def main():
    parser = argparse.ArgumentParser(description="ResearchCore AI - Enterprise Multi-Agent Deep Research CLI")
    parser.add_argument("-t", "--topic", type=str, help="Research topic or question")
    parser.add_argument("-d", "--depth", type=str, choices=["quick", "standard", "deep", "exhaustive"], default="standard", help="Research depth level")
    parser.add_argument("-p", "--provider", type=str, choices=["google", "openai", "groq", "ollama", "mock"], default="mock", help="LLM backend provider")
    parser.add_argument("-i", "--iterations", type=int, default=2, help="Maximum QA revision iterations")
    parser.add_argument("-o", "--output", type=str, help="Output file path (e.g., ./report.md or ./report.html)")
    parser.add_argument("-f", "--format", type=str, choices=["markdown", "html", "json"], default="markdown", help="Export format")
    parser.add_argument("--interactive", action="store_true", help="Launch interactive prompt mode")

    render_banner()
    args = parser.parse_args()
    
    if len(sys.argv) == 1:
        args.interactive = True

    asyncio.run(run_cli_research(args))


if __name__ == "__main__":
    main()
