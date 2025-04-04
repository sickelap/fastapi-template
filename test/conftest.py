import pytest

from app.main import app
from app.persistence.entities import Base
from app.persistence.session import engine
from fastapi.testclient import TestClient


@pytest.fixture(scope="function", autouse=True)
def init_db():
    with engine.begin() as conn:
        Base.metadata.create_all(conn)
    with engine.begin() as conn:
        Base.metadata.drop_all(conn)


@pytest.fixture()
def client():
    with TestClient(app=app, base_url="http://test") as ac:
        yield ac
