import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.services.falkor import FalkorDBService, get_falkor_service

class MockFalkorDBService(FalkorDBService):
    def __init__(self, connected: bool = True, node_count: int = 15):
        self.connected = connected
        self.node_count = node_count

    async def ping_and_count(self):
        return self.connected, self.node_count

@pytest.mark.asyncio
async def test_health_endpoint_healthy():
    app.dependency_overrides[get_falkor_service] = lambda: MockFalkorDBService(connected=True, node_count=42)
    try:
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/api/health")
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"
            assert data["version"] == "1.0.0"
            assert data["falkordb"]["connected"] is True
            assert data["falkordb"]["total_nodes"] == 42
    finally:
        app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_health_endpoint_degraded():
    app.dependency_overrides[get_falkor_service] = lambda: MockFalkorDBService(connected=False, node_count=0)
    try:
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/api/health")
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "degraded"
            assert data["falkordb"]["connected"] is False
            assert data["falkordb"]["total_nodes"] == 0
    finally:
        app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_root_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["project"] == "Company Brain"
        assert data["status"] == "operational"

@pytest.mark.asyncio
async def test_health_endpoint_live():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] in ("healthy", "degraded")
        assert data["version"] == "1.0.0"
        assert "timestamp" in data
        assert "environment" in data
        assert "falkordb" in data
        assert "connected" in data["falkordb"]
        assert "total_nodes" in data["falkordb"]

