"""Test cases for authentication system."""
import pytest
from fastapi.testclient import TestClient
from ..main import app

client = TestClient(app)

def test_login_success():
    """Test successful login."""
    payload = {
        "username": "demo",
        "password": "password"
    }
    
    response = client.post("/api/v1/auth/login", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert "session_id" in data

def test_login_failure():
    """Test failed login with invalid credentials."""
    payload = {
        "username": "invalid",
        "password": "wrong"
    }
    
    response = client.post("/api/v1/auth/login", json=payload)
    assert response.status_code == 401

def test_protected_route_without_token():
    """Test accessing protected route without token."""
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401

def test_protected_route_with_token():
    """Test accessing protected route with valid token."""
    # First login to get token
    login_response = client.post("/api/v1/auth/login", json={
        "username": "demo",
        "password": "password"
    })
    token = login_response.json()["access_token"]
    
    # Use token to access protected route
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/v1/auth/me", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["authenticated"] is True
    assert "user_id" in data

def test_agent_endpoint_with_auth():
    """Test agent endpoint requires authentication."""
    # Without token
    payload = {
        "user_data": {"skills": ["Python"]},
        "task_type": "job_search"
    }
    response = client.post("/api/v1/agents/career", json=payload)
    assert response.status_code == 401
    
    # With token
    login_response = client.post("/api/v1/auth/login", json={
        "username": "demo",
        "password": "password"
    })
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.post("/api/v1/agents/career", json=payload, headers=headers)
    assert response.status_code == 200