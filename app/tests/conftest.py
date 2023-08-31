import pytest
from starlette.testclient import TestClient
from app import app

test_client = TestClient(app)


@pytest.fixture
def client():
    """Create test client"""
    yield test_client  # testing happens here
