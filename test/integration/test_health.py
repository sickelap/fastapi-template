from app.main import app
from fastapi.testclient import TestClient


def test_ping():
    with TestClient(app=app, base_url="http://test") as client:
        response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"health": "OK"}
