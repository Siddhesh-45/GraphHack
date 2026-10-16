from fastapi import APIRouter
from app.models.health import HealthResponse
from app.core.config import settings
from datetime import datetime

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
async def get_health():
    # Attempt minimal FalkorDB check if connection service is available
    falkor_connected = False
    node_count = 0
    try:
        from falkordb import FalkorDB
        db = FalkorDB(host=settings.FALKORDB_HOST, port=settings.FALKORDB_PORT, password=settings.FALKORDB_PASSWORD or None)
        graph = db.select_graph(settings.FALKORDB_GRAPH)
        res = graph.query("MATCH (n) RETURN count(n) AS c")
        node_count = res.result_set[0][0] if res.result_set else 0
        falkor_connected = True
    except Exception:
        falkor_connected = False

    return HealthResponse(
        status="healthy" if falkor_connected else "degraded",
        version="1.0.0",
        timestamp=datetime.utcnow(),
        environment=settings.APP_ENV,
        falkordb={
            "connected": falkor_connected,
            "host": settings.FALKORDB_HOST,
            "port": settings.FALKORDB_PORT,
            "graph_name": settings.FALKORDB_GRAPH,
            "total_nodes": node_count
        }
    )
