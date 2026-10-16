import logging
from typing import Tuple, Optional
from falkordb import FalkorDB
from app.core.config import settings

logger = logging.getLogger(__name__)

class FalkorDBService:
    def __init__(self, host: str, port: int, password: Optional[str] = None, graph_name: str = "company_brain"):
        self.host = host
        self.port = port
        self.password = password
        self.graph_name = graph_name
        self._client: Optional[FalkorDB] = None

    def get_client(self) -> FalkorDB:
        if self._client is None:
            self._client = FalkorDB(
                host=self.host,
                port=self.port,
                password=self.password or None
            )
        return self._client

    async def ping_and_count(self) -> Tuple[bool, int]:
        """
        Pings FalkorDB and counts total nodes in the graph.
        Returns (is_connected, total_nodes).
        """
        try:
            client = self.get_client()
            graph = client.select_graph(self.graph_name)
            res = graph.query("MATCH (n) RETURN count(n) AS c")
            total_nodes = res.result_set[0][0] if (res and res.result_set) else 0
            return True, total_nodes
        except Exception as e:
            logger.warning(f"FalkorDB connection check failed at {self.host}:{self.port} - {str(e)}")
            return False, 0

    def close(self):
        self._client = None

_falkor_instance: Optional[FalkorDBService] = None

def get_falkor_service() -> FalkorDBService:
    global _falkor_instance
    if _falkor_instance is None:
        _falkor_instance = FalkorDBService(
            host=settings.FALKORDB_HOST,
            port=settings.FALKORDB_PORT,
            password=settings.FALKORDB_PASSWORD,
            graph_name=settings.FALKORDB_GRAPH
        )
    return _falkor_instance
