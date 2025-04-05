def test_register_user(client, monkeypatch):
    monkeypatch.setenv("ALLOW_REGISTER", "True")
    payload = {"email": "user@local.host", "password": "userpw"}
    response = client.post("/api/v1/auth/register", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data


def test_login_user(client):
    payload = {"email": "user@local.host", "password": "userpw"}
    client.post("/api/v1/auth/register", json=payload)

    payload = {"username": "user@local.host", "password": "userpw"}
    response = client.post("/api/v1/auth/login", data=payload)

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
