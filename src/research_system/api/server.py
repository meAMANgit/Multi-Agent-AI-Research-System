"""FastAPI application server entrypoint."""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from src.research_system.api.routes import router
from src.research_system.config.settings import get_settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)
logger = logging.getLogger("research_system.server")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan hook for startup and shutdown procedures."""
    logger.info("Initializing ResearchCore AI Multi-Agent Deep Research System v2.0...")
    yield
    logger.info("Shutting down ResearchCore AI server.")


app = FastAPI(
    title="ResearchCore AI API",
    description="Enterprise Multi-Agent AI Deep Research & Intelligence Engine API",
    version="2.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Enable CORS for external dashboards and Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(router)


def start():
    """CLI launcher for API server."""
    settings = get_settings()
    uvicorn.run(
        "src.research_system.api.server:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
    )


if __name__ == "__main__":
    start()
