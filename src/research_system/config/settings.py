"""Global settings and environment management using Pydantic."""

from functools import lru_cache
import os
from typing import Optional
from pydantic import Field

try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseModel as BaseSettings


class Settings(BaseSettings):
    """Application configuration loaded from environment and defaults."""

    # Project metadata
    PROJECT_NAME: str = "ResearchCore AI"
    VERSION: str = "2.0.0"
    ENVIRONMENT: str = "production"
    DEBUG: bool = False

    # Provider & Model Settings
    DEFAULT_LLM_PROVIDER: str = "google"
    DEFAULT_MODEL_NAME: str = "gemini-2.5-flash"

    # API Keys
    GEMINI_API_KEY: Optional[str] = Field(default=None)
    OPENAI_API_KEY: Optional[str] = Field(default=None)
    ANTHROPIC_API_KEY: Optional[str] = Field(default=None)
    GROQ_API_KEY: Optional[str] = Field(default=None)
    TAVILY_API_KEY: Optional[str] = Field(default=None)
    SERPAPI_API_KEY: Optional[str] = Field(default=None)

    # Ollama Settings
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3.3:70b"

    # Orchestrator & Multi-Agent Execution Settings
    MAX_RESEARCH_ITERATIONS: int = 3
    QUALITY_SCORE_THRESHOLD: float = 85.0
    MAX_SEARCH_RESULTS_PER_QUERY: int = 5
    REQUEST_TIMEOUT_SECONDS: int = 30
    CRAWLER_USER_AGENT: str = "ResearchCoreAI/2.0 (DeepResearchBot; +https://github.com/meAMANgit/Multi-Agent-AI-Research-System)"

    # Server Settings
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    STREAMLIT_PORT: int = 8501
    LOG_LEVEL: str = "INFO"

    # Output paths
    OUTPUT_DIR: str = os.path.join(os.getcwd(), "outputs")

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }


@lru_cache()
def get_settings() -> Settings:
    """Return a cached singleton instance of system settings."""
    return Settings()
