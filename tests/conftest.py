import pytest
from fastapi.testclient import TestClient

from app.main import app

from app.database.connection import engine

from app.database.base import Base


Base.metadata.create_all(
    bind=engine
)

@pytest.fixture
def client():
    return TestClient(app)
