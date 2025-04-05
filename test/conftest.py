import pytest

from app.main import app
from app.persistence.entities import Base
from fastapi.testclient import TestClient


@pytest.fixture(scope="function", autouse=True)
def init_db(monkeypatch):
    monkeypatch.setenv("SQLALCHEMY_DATABASE_URL", "sqlite:///:memory:")
    from app.persistence.session import engine

    with engine.begin() as conn:
        Base.metadata.create_all(conn)
    yield
    with engine.begin() as conn:
        Base.metadata.drop_all(conn)


@pytest.fixture()
def client():
    # app.dependency_overrides[get_session] = override_get_session
    with TestClient(app=app, base_url="http://test") as test_client:
        yield test_client
