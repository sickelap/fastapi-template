import uuid
from datetime import timedelta

import httpx
import pytest
from app.application.service.token import (create_access_token,
                                           create_refresh_token)
from app.config import settings
from freezegun import freeze_time

username = "user@local.host"
password = "userpw"


async def register(client, email, password) -> httpx.Response:
    payload = {"email": email, "password": password}
    return await client.post("/api/v1/auth/register", json=payload)


async def login(client, email="", password="") -> httpx.Response:
    payload = {"username": email, "password": password}
    return await client.post("/api/v1/auth/login", data=payload)


async def get_my_details(client, token) -> httpx.Response:
    return await client.get(
        "/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"}
    )


async def refresh_tokens(client, token) -> httpx.Response:
    return await client.post("/api/v1/auth/refresh", json={"refresh_token": token})


@pytest.mark.asyncio
async def test_register_user(client):
    response = await register(client, username, password)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data


@pytest.mark.asyncio
async def test_register_user_when_registration_disabled(client, monkeypatch):
    monkeypatch.setattr(settings, "ALLOW_REGISTER", False)
    response = await register(client, username, password)
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_register_user_with_the_same_email(client):
    await register(client, username, password)
    response = await register(client, username, password)
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_login_user(client):
    await register(client, username, password)
    response = await login(client, username, password)

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data

    me = (await get_my_details(client, data["access_token"])).json()
    assert me["email"] == username


@pytest.mark.asyncio
async def test_token_refresh(client):
    with freeze_time() as freezer:
        tokens = (await register(client, username, password)).json()
        freezer.tick(delta=timedelta(seconds=10))
        new_tokens = (await refresh_tokens(client, tokens["refresh_token"])).json()
        assert (
            tokens["refresh_token"] != new_tokens["refresh_token"]
        ), "refresh token has not been refreshed"
        assert (
            tokens["access_token"] != new_tokens["access_token"]
        ), "access token has not been refreshed"


@pytest.mark.asyncio
async def test_refresh_token_invalidation(client):
    with freeze_time() as freezer:
        await register(client, username, password)
        tokens1 = (await login(client, username, password)).json()
        freezer.tick(delta=timedelta(seconds=10))
        (await refresh_tokens(client, tokens1["refresh_token"])).json()
        """
        try to use the refresh token generated previously
        """
        response = await refresh_tokens(client, tokens1["refresh_token"])
        assert response.status_code == 401


@pytest.mark.asyncio
async def test_use_refresh_token_as_access_token(client):
    tokens = (await register(client, username, password)).json()
    response = await get_my_details(client, tokens["refresh_token"])
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_use_access_token_as_refresh_token(client):
    with freeze_time() as freezer:
        tokens = (await register(client, username, password)).json()
        freezer.tick(delta=timedelta(seconds=10))
        response = await refresh_tokens(client, tokens["access_token"])
        assert response.status_code == 401


@pytest.mark.asyncio
async def test_invalid_refresh_token(client, monkeypatch):
    original_secret_key = settings.SECRET_KEY
    monkeypatch.setattr(settings, "SECRET_KEY", "secret")
    token = create_refresh_token(uuid.uuid4())
    monkeypatch.setattr(settings, "SECRET_KEY", original_secret_key)
    response = await refresh_tokens(client, token)
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_refresh_token_without_token(client):
    response = await refresh_tokens(client, "not-a-token")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_invalid_access_token(client, monkeypatch):
    original_secret_key = settings.SECRET_KEY
    monkeypatch.setattr(settings, "SECRET_KEY", "secret")
    token = create_access_token(uuid.uuid4())
    monkeypatch.setattr(settings, "SECRET_KEY", original_secret_key)
    response = await get_my_details(client, token)
    assert response.status_code == 401
