"""Pytest configuration file for Luthien Code Control tests."""
import pytest
from fastapi.testclient import TestClient

from luthien_code_control.main import app


@pytest.fixture
def client():
    """Return a test client for the FastAPI app."""
    return TestClient(app)