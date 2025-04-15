import pytest
from fastapi.testclient import TestClient

def test_root_endpoint(client: TestClient):
    """
    Test the root endpoint returns status 200 and correct API information.
    """
    response = client.get("/")
    
    # Verify the status code is 200 (OK)
    assert response.status_code == 200
    
    # Verify the response contains the expected API information
    assert response.json()["name"] == "AI-Powered Forecasting Tool API"
    assert response.json()["version"] == "0.1.0"
    assert response.json()["status"] == "active"

def test_health_check(client: TestClient):
    """
    Test that the health check endpoint returns status 200 and the correct response data.
    """
    # Send a GET request to the health endpoint
    response = client.get("/health")
    
    # Verify the response status code is 200 (OK)
    assert response.status_code == 200
    
    # Verify the response data matches what we expect
    assert response.json() == {"status": "healthy"} 