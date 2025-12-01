"""Test cases for API endpoints."""
import pytest
from fastapi.testclient import TestClient
from ..main import app

client = TestClient(app)

def test_root_endpoint():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_system_status():
    """Test system status endpoint."""
    response = client.get("/api/v1/status")
    assert response.status_code == 200
    data = response.json()
    assert "system" in data
    assert "agents" in data

def test_create_session():
    """Test session creation."""
    session_data = {
        "user_id": "test_user",
        "initial_data": {"test": "data"}
    }
    
    response = client.post("/api/v1/sessions", json=session_data)
    assert response.status_code == 200
    assert "session_id" in response.json()

def test_user_profile_update():
    """Test user profile update."""
    profile_data = {
        "user_id": "test_user",
        "name": "Test User",
        "skills": ["Python", "FastAPI"],
        "experience_years": 3
    }
    
    response = client.post("/api/v1/users/test_user/profile", json=profile_data)
    assert response.status_code == 200