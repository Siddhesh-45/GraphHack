import pytest
from app.services.falkor import FalkorDBService, get_falkor_service

@pytest.mark.asyncio
async def test_falkor_service_connection_failure_handling():
    # Attempt connecting to a non-existent port/host
    service = FalkorDBService(host="127.0.0.1", port=59999, graph_name="test_nonexistent")
    is_connected, node_count = await service.ping_and_count()
    assert is_connected is False
    assert node_count == 0

@pytest.mark.asyncio
async def test_falkor_service_singleton():
    s1 = get_falkor_service()
    s2 = get_falkor_service()
    assert s1 is s2

@pytest.mark.asyncio
async def test_falkor_service_close():
    service = FalkorDBService(host="localhost", port=6379)
    service.close()
    assert service._client is None
