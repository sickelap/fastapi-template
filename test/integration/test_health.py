import pytest


@pytest.mark.asyncio
async def test_ping(client):
    response = await client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"health": "OK"}
