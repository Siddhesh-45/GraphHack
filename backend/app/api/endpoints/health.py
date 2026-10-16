from fastapi import APIRouter, Depends
from datetime import datetime, timezone
from app.models.health import HealthResponse
from app.core.config import settings
from app.services.falkor import FalkorDBService, get_falkor_service

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
async def check_health(falkor: FalkorDBService = Depends(get_falkor_service)):
    is_connected, node_count = await falkor.ping_and_count()
    return HealthResponse(
        status="healthy" if is_connected else "degraded",
        version="1.0.0",
        timestamp=datetime.now(timezone.utc),
        environment=settings.APP_ENV,
        falkordb={
            "connected": is_connected,
            "host": settings.FALKORDB_HOST,
            "port": settings.FALKORDB_PORT,
            "graph_name": settings.FALKORDB_GRAPH,
            "total_nodes": node_count if is_connected else 0
        }
    )
