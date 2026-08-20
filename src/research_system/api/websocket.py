"""WebSocket connection manager for real-time agent thought streaming."""

import asyncio
import json
import logging
from typing import Dict, List, Set
from fastapi import WebSocket

logger = logging.getLogger("research_system.api.websocket")


class ConnectionManager:
    """Manages active WebSocket client connections for real-time streaming."""

    def __init__(self):
        self.active_connections: Set[WebSocket] = set()
        self.session_subscribers: Dict[str, Set[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, session_id: str = "global"):
        await websocket.accept()
        self.active_connections.add(websocket)
        if session_id not in self.session_subscribers:
            self.session_subscribers[session_id] = set()
        self.session_subscribers[session_id].add(websocket)
        logger.info("WebSocket client connected to session: %s", session_id)

    def disconnect(self, websocket: WebSocket, session_id: str = "global"):
        self.active_connections.discard(websocket)
        if session_id in self.session_subscribers:
            self.session_subscribers[session_id].discard(websocket)
        logger.info("WebSocket client disconnected from session: %s", session_id)

    async def broadcast_thought(self, session_id: str, payload: dict):
        """Broadcast an agent thought event to all subscribers."""
        message = json.dumps({"event": "agent_thought", "session_id": session_id, "data": payload}, default=str)
        
        # Broadcast to session subscribers and global listeners
        recipients = list(self.session_subscribers.get(session_id, set())) + list(self.session_subscribers.get("global", set()))
        dead_connections = set()
        
        for ws in set(recipients):
            try:
                await ws.send_text(message)
            except Exception:
                dead_connections.add(ws)

        for dead_ws in dead_connections:
            self.disconnect(dead_ws, session_id)


manager = ConnectionManager()
