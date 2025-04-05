from app.config import settings


def test_register_user(client):
    payload = {"email": "user@local.host", "password": "userpw"}
    response = client.post("/api/v1/auth/register", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data


def test_register_user_when_registration_disabled(client, monkeypatch):
    monkeypatch.setattr(settings, "ALLOW_REGISTER", False)

    payload = {"email": "user@local.host", "password": "userpw"}
    response = client.post("/api/v1/auth/register", json=payload)

    assert response.status_code == 403


def test_register_user_with_the_same_email(client):
    payload = {"email": "user@local.host", "password": "userpw1"}
    client.post("/api/v1/auth/register", json=payload)
    payload = {"email": "user@local.host", "password": "userpw2"}
    response = client.post("/api/v1/auth/register", json=payload)

    assert response.status_code == 409


def test_login_user(client):
    payload = {"email": "user@local.host", "password": "userpw"}
    client.post("/api/v1/auth/register", json=payload)

    payload = {"username": "user@local.host", "password": "userpw"}
    response = client.post("/api/v1/auth/login", data=payload)

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
