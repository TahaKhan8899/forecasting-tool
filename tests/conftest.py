import pytest
from typing import Generator
from fastapi.testclient import TestClient

from app.main import app  # Import the FastAPI app instance

@pytest.fixture(scope="session")
def client() -> Generator[TestClient, None, None]:
    """
    Fixture that creates a test client for testing FastAPI endpoints.
    This provides a reusable client instance for all tests.
    """
    with TestClient(app) as test_client:
        yield test_client
