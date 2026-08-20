"""API package init."""

try:
    from src.research_system.api.server import app, start
    from src.research_system.api.routes import router
    from src.research_system.api.websocket import manager
except (ImportError, ModuleNotFoundError):
    from .server import app, start
    from .routes import router
    from .websocket import manager

__all__ = ["app", "start", "router", "manager"]
