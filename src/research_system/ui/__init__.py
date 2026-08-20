"""UI package init."""

try:
    from src.research_system.ui.streamlit_app import run_app
except (ImportError, ModuleNotFoundError):
    from .streamlit_app import run_app

__all__ = ["run_app"]
