import httpx
import pytest
from freezegun import freeze_time


async def register(client, email, password) -> httpx.Response:
    with freeze_time() as freezer:
        freezer.tick(100)
        payload = {"email": email, "password": password}
        return await client.post("/api/v1/auth/register", json=payload)


@pytest.mark.asyncio
async def test_first_registered_user_is_superuser(client):
    tokens = (await register(client, "user@local.host", "userpw")).json()

    headers = {"Authorization": f"Bearer {tokens['access_token']}"}
    data = (await client.get("/api/v1/profile", headers=headers)).json()

    assert data["email"] == "user@local.host"
    assert data["is_active"]
    assert data["is_superuser"]


@pytest.mark.asyncio
async def test_second_registered_user_is_not_superuser(client):
    tokens = (await register(client, "user1@local.host", "userpw")).json()
    tokens = (await register(client, "user2@local.host", "userpw")).json()

    headers = {"Authorization": f"Bearer {tokens['access_token']}"}
    data = (await client.get("/api/v1/profile", headers=headers)).json()

    assert data["email"] == "user2@local.host"
    assert data["is_active"]
    assert not data["is_superuser"]
