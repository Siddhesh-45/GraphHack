from app.graph.connection import FalkorDBConnectionService, get_graph_connection

# Alias for backward compatibility
FalkorDBService = FalkorDBConnectionService
get_falkor_service = get_graph_connection

__all__ = ["FalkorDBService", "get_falkor_service", "FalkorDBConnectionService", "get_graph_connection"]
