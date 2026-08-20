"""Configuration module for ResearchCore AI."""

try:
    from src.research_system.config.settings import Settings, get_settings
    from src.research_system.config.prompts import PROMPTS
except (ImportError, ModuleNotFoundError):
    from .settings import Settings, get_settings
    from .prompts import PROMPTS

__all__ = ["Settings", "get_settings", "PROMPTS"]
