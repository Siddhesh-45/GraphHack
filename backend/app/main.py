from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.config import settings
from app.core.logging import setup_logging, get_logger
from app.api.router import api_router

setup_logging()
logger = get_logger("company_brain")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Starting Company Brain API in [{settings.APP_ENV}] mode (FalkorDB host: {settings.FALKORDB_HOST}:{settings.FALKORDB_PORT})")
    yield
    logger.info("Shutting down Company Brain API")

app = FastAPI(
    title="Company Brain API",
    description="Graph-Native Organizational Intelligence Platform for FalkorDB Graph Hacks 2026",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API Router
app.include_router(api_router, prefix="/api")

@app.get("/")
async def root():
    return {
        "project": "Company Brain",
        "hackathon": "FalkorDB Graph Hacks 2026",
        "track": "Track 03 — Company Brain",
        "status": "operational",
        "docs_url": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.BACKEND_HOST, port=settings.BACKEND_PORT, reload=True)
