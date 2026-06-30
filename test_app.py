"""Tests for the Cyclopibus Mistral Vibe Web API"""

import pytest
from litestar.testing import TestClient
from app import app


@pytest.fixture
def client():
    """Create a test client for the app"""
    return TestClient(app)


def test_hello_endpoint(client):
    """Test the /hello endpoint returns correct response"""
    response = client.get("/hello")
    
    # Check status code
    assert response.status_code == 200
    
    # Check response body
    response_data = response.json()
    assert response_data == {"message": "Hello World!"}
    
    # Check content type
    assert "application/json" in response.headers.get("content-type", "")


def test_hello_endpoint_method_not_allowed(client):
    """Test that POST method is not allowed on /hello"""
    response = client.post("/hello")
    assert response.status_code == 405  # Method Not Allowed


if __name__ == "__main__":
    pytest.main([__file__, "-v"])