# API Reference & WebSocket Specification

The **ResearchCore AI** backend provides a RESTful and WebSocket API built with **FastAPI**.

Interactive Swagger/OpenAPI documentation is available at `/docs` or `/redoc` when the API server is active.

---

## Base URL
```
http://localhost:8000/api
```

---

## Endpoints

### 1. Healthcheck
- **Endpoint**: `GET /api/health`
- **Response**:
```json
{
  "status": "healthy",
  "service": "ResearchCore AI",
  "version": "2.0.0"
}
```

---

### 2. Available Providers
- **Endpoint**: `GET /api/providers`
- **Description**: Returns all configured and supported LLM providers.
- **Response**:
```json
{
  "active_default": "google",
  "providers": [
    { "id": "google", "name": "Google Gemini", "configured": true },
    { "id": "openai", "name": "OpenAI GPT-4o", "configured": false },
    { "id": "groq", "name": "Groq LLaMA-3.3", "configured": false },
    { "id": "ollama", "name": "Ollama (Local Offline)", "configured": true },
    { "id": "mock", "name": "Deterministic Mock Engine", "configured": true }
  ]
}
```

---

### 3. Run Autonomous Research
- **Endpoint**: `POST /api/research/run`
- **Request Body**:
```json
{
  "topic": "Next-Generation Solid State Batteries",
  "depth": "standard",
  "provider": "google",
  "max_iterations": 2
}
```
- **Response**: Returns a full `ResearchResponse` containing session ID, status, verified facts, quantitative metrics, QA scores, and full Markdown report.

---

### 4. Query Research Session
- **Endpoint**: `GET /api/research/{research_id}`
- **Response**: Full `ResearchResponse` JSON payload.

---

### 5. Export Report
- **Endpoint**: `GET /api/research/{research_id}/export?format={markdown|html|json}`
- **Formats**:
  - `markdown`: Raw markdown with YAML frontmatter.
  - `html`: Standalone interactive HTML dashboard.
  - `json`: Machine-readable Knowledge Graph nodes and edges.

---

## WebSocket Thought Streaming

- **Endpoint**: `ws://localhost:8000/api/ws/{session_id}`
- **Message Format**:
```json
{
  "event": "agent_thought",
  "session_id": "global",
  "data": {
    "timestamp": "2026-08-20T12:00:00Z",
    "agent_name": "Lead Research Director",
    "step": "Strategic Decomposition",
    "thought": "Decomposing research topic into multi-dimensional hypotheses..."
  }
}
```
