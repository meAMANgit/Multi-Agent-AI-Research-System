"""FastAPI route handlers for research execution and telemetry."""

import asyncio
from typing import Dict, List, Optional
from fastapi import APIRouter, BackgroundTasks, HTTPException, Query, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, PlainTextResponse

from src.research_system.api.websocket import manager
from src.research_system.config.settings import get_settings
from src.research_system.exporters.html_exporter import HTMLExporter
from src.research_system.exporters.json_exporter import JSONExporter
from src.research_system.exporters.markdown_exporter import MarkdownExporter
from src.research_system.llm.provider import get_llm_client
from src.research_system.models.enums import LLMProvider, ResearchDepth
from src.research_system.models.schemas import AgentThought, ResearchRequest, ResearchResponse
from src.research_system.orchestrator.workflow import MultiAgentResearchWorkflow

router = APIRouter(prefix="/api", tags=["Research"])

# In-memory storage for active and completed research jobs
research_store: Dict[str, ResearchResponse] = {}


@router.get("/health")
async def health_check():
    """Healthcheck endpoint for Kubernetes, Docker, and load balancers."""
    return {"status": "healthy", "service": "ResearchCore AI", "version": "2.0.0"}


@router.get("/providers")
async def list_providers():
    """Return available LLM providers and active environment configuration."""
    settings = get_settings()
    return {
        "active_default": settings.DEFAULT_LLM_PROVIDER,
        "providers": [
            {"id": "google", "name": "Google Gemini", "configured": bool(settings.GEMINI_API_KEY)},
            {"id": "openai", "name": "OpenAI GPT-4o", "configured": bool(settings.OPENAI_API_KEY)},
            {"id": "groq", "name": "Groq LLaMA-3.3", "configured": bool(settings.GROQ_API_KEY)},
            {"id": "ollama", "name": "Ollama (Local Offline)", "configured": True, "url": settings.OLLAMA_BASE_URL},
            {"id": "mock", "name": "Deterministic Mock Engine", "configured": True, "description": "Offline zero-cost testing engine"},
        ]
    }


@router.post("/research/run", response_model=ResearchResponse)
async def run_research_endpoint(request: ResearchRequest):
    """Execute a complete multi-agent research workflow synchronously."""
    workflow = MultiAgentResearchWorkflow(provider=request.provider)
    
    # Callback to stream events to WebSockets
    def _stream_thought(thought: AgentThought):
        asyncio.create_task(manager.broadcast_thought("global", thought.model_dump(mode="json")))

    response = await workflow.run_research(
        topic=request.topic,
        depth=request.depth,
        max_iterations=request.max_iterations,
        on_thought_callback=_stream_thought,
    )
    
    # Cache result
    research_store[response.research_id] = response
    return response


@router.get("/research/{research_id}", response_model=ResearchResponse)
async def get_research_by_id(research_id: str):
    """Retrieve existing completed research session by ID."""
    if research_id not in research_store:
        raise HTTPException(status_code=404, detail=f"Research ID '{research_id}' not found.")
    return research_store[research_id]


@router.get("/research/{research_id}/export")
async def export_research(research_id: str, format: str = Query("markdown", enum=["markdown", "html", "json"])):
    """Export research report in Markdown, Interactive HTML, or JSON Knowledge Graph format."""
    if research_id not in research_store:
        raise HTTPException(status_code=404, detail=f"Research ID '{research_id}' not found.")
    
    resp = research_store[research_id]
    if format == "html":
        return HTMLResponse(content=HTMLExporter.export_to_string(resp))
    elif format == "json":
        return JSONExporter.export_to_dict(resp)
    else:
        return PlainTextResponse(content=MarkdownExporter.export_to_string(resp), media_type="text/markdown")


@router.websocket("/ws/{session_id}")
async def websocket_thought_stream(websocket: WebSocket, session_id: str):
    """WebSocket endpoint for real-time agent thought feeds."""
    await manager.connect(websocket, session_id)
    try:
        while True:
            # Keep-alive loop
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        manager.disconnect(websocket, session_id)
