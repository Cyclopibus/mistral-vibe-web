"""Tests for the Cyclopibus Mistral Vibe Web API"""

import pytest
from litestar.testing import TestClient
from app import app


@pytest.fixture
def client():
    """Create a test client for the app"""
    return TestClient(app)


# Hello endpoint tests

def test_hello_endpoint_no_name(client):
    """Test the /hello endpoint without name parameter returns default message"""
    response = client.get("/hello")
    
    # Check status code
    assert response.status_code == 200
    
    # Check response body
    response_data = response.json()
    assert response_data == {"message": "Hello World!"}
    
    # Check content type
    assert "application/json" in response.headers.get("content-type", "")


def test_hello_endpoint_with_name(client):
    """Test the /hello endpoint with name parameter returns personalized message"""
    test_name = "Alice"
    response = client.get("/hello", params={"name": test_name})
    
    # Check status code
    assert response.status_code == 200
    
    # Check response body
    response_data = response.json()
    assert response_data == {"message": f"Hello {test_name}!"}


def test_hello_endpoint_with_different_names(client):
    """Test the /hello endpoint with various names"""
    test_names = ["Bob", "Charlie", "Diana", "Eve"]
    
    for name in test_names:
        response = client.get("/hello", params={"name": name})
        assert response.status_code == 200
        response_data = response.json()
        assert response_data == {"message": f"Hello {name}!"}


def test_hello_endpoint_with_special_characters_name(client):
    """Test the /hello endpoint with special characters in name"""
    test_name = "John Doe!@#"
    response = client.get("/hello", params={"name": test_name})
    
    # Check status code
    assert response.status_code == 200
    
    # Check response body
    response_data = response.json()
    assert response_data == {"message": f"Hello {test_name}!"}


def test_hello_endpoint_with_empty_name(client):
    """Test the /hello endpoint with empty name parameter"""
    response = client.get("/hello", params={"name": ""})
    
    # Check status code
    assert response.status_code == 200
    
    # Check response body - empty name should still use the format
    response_data = response.json()
    assert response_data == {"message": "Hello !"}


def test_hello_endpoint_method_not_allowed(client):
    """Test that POST method is not allowed on /hello"""
    response = client.post("/hello")
    assert response.status_code == 405  # Method Not Allowed


# Echo endpoint tests

def test_echo_endpoint_success(client):
    """Test the /echo endpoint returns the received message"""
    test_message = "Hello, this is a test!"
    response = client.post("/echo", json={"message": test_message})
    
    # Check status code
    assert response.status_code == 200
    
    # Check response body
    response_data = response.json()
    assert response_data == {"echo": test_message}
    
    # Check content type
    assert "application/json" in response.headers.get("content-type", "")


def test_echo_endpoint_empty_message(client):
    """Test the /echo endpoint with empty message"""
    response = client.post("/echo", json={"message": ""})
    
    # Check status code
    assert response.status_code == 200
    
    # Check response body
    response_data = response.json()
    assert response_data == {"echo": ""}


def test_echo_endpoint_special_characters(client):
    """Test the /echo endpoint with special characters"""
    test_message = "Test with special chars: !@#$%^&*()_+-=[]{}|;':\",./<>?"
    response = client.post("/echo", json={"message": test_message})
    
    # Check status code
    assert response.status_code == 200
    
    # Check response body
    response_data = response.json()
    assert response_data == {"echo": test_message}


def test_echo_endpoint_method_not_allowed(client):
    """Test that GET method is not allowed on /echo"""
    response = client.get("/echo")
    assert response.status_code == 405  # Method Not Allowed


def test_echo_endpoint_missing_message(client):
    """Test the /echo endpoint with missing message field"""
    response = client.post("/echo", json={})
    
    # Should return 400 Bad Request for missing required field (Litestar uses 400 for validation errors)
    assert response.status_code == 400


if __name__ == "__main__":
    pytest.main([__file__, "-v"])