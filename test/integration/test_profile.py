import httpx
import pytest
from freezegun import freeze_time


async def register(client, email, password) -> httpx.Response:
    with freeze_time() as freezer:
        freezer.tick(100)
        payload = {"email": email, "password": password}
        return await client.post("/api/v1/auth/register", json=payload)


async def login(client, email, password) -> httpx.Response:
    payload = {"username": email, "password": password}
    return await client.post("/api/v1/auth/login", data=payload)


async def get_user_id(client, token) -> str:
    data = (
        await client.get(
            "/api/v1/profile", headers={"Authorization": f"Bearer {token}"}
        )
    ).json()
    return data.get("id")


@pytest.mark.asyncio
async def test_first_registered_user_is_superuser(client):
    tokens = (await register(client, "user@local.host", "userpw")).json()
    print("tokens", tokens)
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


@pytest.mark.asyncio
async def test_update_password(client):
    tokens = (await register(client, "user@local.host", "userpw")).json()

    payload = {"old_password": "userpw", "new_password": "pwuser"}
    headers = {"Authorization": f"Bearer {tokens['access_token']}"}
    response = await client.post("/api/v1/profile", json=payload, headers=headers)
    assert response.status_code == 200

    response = await login(client, "user@local.host", "pwuser")
    assert response.status_code == 200, "unable to login with new password"


@pytest.mark.asyncio
async def test_update_password_shoud_fail_when_both_passwords_are_the_same(client):
    tokens = (await register(client, "user@local.host", "userpw")).json()

    payload = {"old_password": "userpw", "new_password": "userpw"}
    headers = {"Authorization": f"Bearer {tokens['access_token']}"}
    response = await client.post("/api/v1/profile", json=payload, headers=headers)
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_update_password_shoud_fail_when_using_short_password(client):
    tokens = (await register(client, "user@local.host", "userpw")).json()

    payload = {"old_password": "userpw", "new_password": "pass"}
    headers = {"Authorization": f"Bearer {tokens['access_token']}"}
    response = await client.post("/api/v1/profile", json=payload, headers=headers)
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_admin_can_disable_user(client):
    admin_tokens = (await register(client, "admin@local.host", "adminpw")).json()
    user_tokens = (await register(client, "user@local.host", "userpw")).json()

    user_id = await get_user_id(client, user_tokens["access_token"])

    response = await client.post(
        "/api/v1/admin/disable_user",
        json={"user_id": user_id},
        headers={"Authorization": f"Bearer {admin_tokens['access_token']}"},
    )
    assert response.status_code == 200

    response = await login(client, "user@local.host", "userpw")
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_regular_user_cannot_disable_another_user(client):
    await register(client, "admin@local.host", "adminpw")
    user1_tokens = (await register(client, "user1@local.host", "userpw")).json()
    user2_tokens = (await register(client, "user2@local.host", "userpw")).json()

    user_id = await get_user_id(client, user1_tokens["access_token"])

    response = await client.post(
        "/api/v1/admin/disable_user",
        json={"user_id": user_id},
        headers={"Authorization": f"Bearer {user2_tokens['access_token']}"},
    )
    assert response.status_code == 403
