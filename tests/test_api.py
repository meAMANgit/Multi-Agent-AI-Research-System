"""API endpoint tests using FastAPI TestClient / async httpx."""

import pytest
from httpx import ASGITransport, AsyncClient
from src.research_system.api.server import app


@pytest.mark.asyncio
async def test_health_check_endpoint():
    """Verify health endpoint."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/api/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "healthy"
        assert data["service"] == "ResearchCore AI"


@pytest.mark.asyncio
async def test_providers_endpoint():
    """Verify provider listing."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/api/providers")
        assert resp.status_code == 200
        data = resp.json()
        assert "providers" in data
        assert len(data["providers"]) >= 4


@pytest.mark.asyncio
async def test_research_run_endpoint():
    """Verify synchronous research execution via API."""
    payload = {
        "topic": "Microgrid Energy Storage Optimization",
        "depth": "quick",
        "provider": "mock",
        "max_iterations": 1,
    }
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.post("/api/research/run", json=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert "research_id" in data
        assert data["status"] == "completed"
        assert len(data["markdown_report"]) > 100

        # Test export endpoint
        res_id = data["research_id"]
        exp_resp = await client.get(f"/api/research/{res_id}/export?format=markdown")
        assert exp_resp.status_code == 200

        exp_json = await client.get(f"/api/research/{res_id}/export?format=json")
        assert exp_json.status_code == 200
        assert "knowledge_graph" in exp_json.json()
