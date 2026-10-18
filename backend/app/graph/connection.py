import logging
from typing import Tuple, Optional, Dict, Any, List
from falkordb import FalkorDB
from app.core.config import settings

logger = logging.getLogger(__name__)

# Canonical labels requiring unique constraints on `id`
CANONICAL_NODE_LABELS = [
    "Person",
    "Team",
    "Project",
    "Service",
    "Document",
    "Chunk",
    "Ticket",
    "ChatMessage",
    "Decision",
    "Incident",
    "Skill",
]

# Secondary range indexes for fast property lookups
CANONICAL_INDEXES = [
    ("Person", "name"),
    ("Person", "email"),
    ("Team", "name"),
    ("Service", "name"),
    ("Decision", "status"),
    ("Decision", "decision_date"),
    ("Incident", "severity"),
    ("Incident", "occurred_at"),
    ("Document", "checksum"),
]


class FalkorDBConnectionService:
    """
    Core FalkorDB connection lifecycle manager and query executor.
    Supports connection pooling, query parameterization, and schema constraint setup.
    """
    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[int] = None,
        password: Optional[str] = None,
        graph_name: Optional[str] = None,
        max_connections: Optional[int] = None,
        socket_timeout: float = 3.0,
        socket_connect_timeout: float = 3.0,
    ):
        self.host = host or settings.FALKORDB_HOST
        self.port = port or settings.FALKORDB_PORT
        self.password = password or settings.FALKORDB_PASSWORD
        self.graph_name = graph_name or settings.FALKORDB_GRAPH
        self.max_connections = max_connections or settings.FALKORDB_MAX_CONNECTIONS
        self.socket_timeout = socket_timeout
        self.socket_connect_timeout = socket_connect_timeout
        self._driver: Optional[FalkorDB] = None
        self._client: Optional[FalkorDB] = None

    def get_client(self) -> FalkorDB:
        """Instantiate or return the active FalkorDB client driver."""
        if self._driver is None:
            self._driver = FalkorDB(
                host=self.host,
                port=self.port,
                password=self.password or None,
                max_connections=self.max_connections,
                socket_timeout=self.socket_timeout,
                socket_connect_timeout=self.socket_connect_timeout,
            )
            self._client = self._driver
            logger.info(f"Initialized FalkorDB driver for {self.host}:{self.port} (pool max: {self.max_connections})")
        return self._driver

    def get_graph(self, graph_name: Optional[str] = None):
        """Return the Graph handle for the target graph name."""
        target_graph = graph_name or self.graph_name
        return self.get_client().select_graph(target_graph)

    def query(self, cypher: str, params: Optional[Dict[str, Any]] = None, graph_name: Optional[str] = None):
        """
        Execute a strictly parameterized Cypher query against FalkorDB.
        """
        graph = self.get_graph(graph_name)
        return graph.query(cypher, params or {})

    def init_schema(self, graph_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Idempotently create unique constraints and range indexes on FalkorDB.
        Safe to invoke repeatedly on application boot without throwing.
        """
        target_graph = graph_name or self.graph_name
        graph = self.get_graph(target_graph)
        created_constraints: List[str] = []
        created_indexes: List[str] = []

        # 1. Unique Constraints on `id`
        for label in CANONICAL_NODE_LABELS:
            try:
                graph.create_node_unique_constraint(label, "id")
                created_constraints.append(f"{label}.id")
                logger.info(f"Created unique constraint on {label}(id)")
            except Exception as e:
                # FalkorDB raises exception when constraint already exists
                err_msg = str(e).lower()
                if "already exists" in err_msg or "already indexed" in err_msg:
                    logger.debug(f"Unique constraint on {label}(id) already operational")
                else:
                    logger.warning(f"Could not create unique constraint on {label}(id): {e}")

        # 2. Secondary Range Indexes
        for label, prop in CANONICAL_INDEXES:
            try:
                graph.create_node_range_index(label, prop)
                created_indexes.append(f"{label}.{prop}")
                logger.info(f"Created range index on {label}({prop})")
            except Exception as e:
                err_msg = str(e).lower()
                if "already exists" in err_msg or "already indexed" in err_msg:
                    logger.debug(f"Range index on {label}({prop}) already operational")
                else:
                    logger.warning(f"Could not create index on {label}({prop}): {e}")

        return {
            "graph": target_graph,
            "created_constraints": created_constraints,
            "created_indexes": created_indexes,
            "total_canonical_labels": len(CANONICAL_NODE_LABELS),
        }

    async def ping_and_count(self, graph_name: Optional[str] = None) -> Tuple[bool, int]:
        """
        Pings FalkorDB and counts total nodes in the graph.
        Returns (is_connected, total_nodes).
        """
        try:
            graph = self.get_graph(graph_name)
            res = graph.query("MATCH (n) RETURN count(n) AS c")
            total_nodes = res.result_set[0][0] if (res and res.result_set) else 0
            return True, total_nodes
        except Exception as e:
            logger.warning(f"FalkorDB connection check failed at {self.host}:{self.port} - {str(e)}")
            return False, 0

    def close(self):
        """Close connection pool and release resources."""
        if self._driver is not None:
            try:
                self._driver.connection_pool.disconnect()
            except Exception as e:
                logger.debug(f"Error disconnecting FalkorDB pool: {e}")
            self._driver = None
            self._client = None
            logger.info("FalkorDB connections closed.")


_connection_service_instance: Optional[FalkorDBConnectionService] = None


def get_graph_connection() -> FalkorDBConnectionService:
    global _connection_service_instance
    if _connection_service_instance is None:
        _connection_service_instance = FalkorDBConnectionService()
    return _connection_service_instance
