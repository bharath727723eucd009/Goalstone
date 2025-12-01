"""Test cases for agent route endpoints."""
import pytest
from fastapi.testclient import TestClient
from ..main import app

client = TestClient(app)

def test_career_agent_endpoint():
    """Test career agent endpoint."""
    payload = {
        "user_data": {
            "skills": ["Python", "Machine Learning"],
            "experience_years": 3
        },
        "task_type": "job_search",
        "parameters": {"remote_ok": True}
    }
    
    response = client.post("/api/v1/agents/career", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "data" in data

def test_finance_agent_endpoint():
    """Test finance agent endpoint."""
    payload = {
        "user_data": {
            "income": 75000,
            "expenses": 50000,
            "age": 30
        },
        "task_type": "budget_analysis",
        "parameters": {"time_horizon": "5_years"}
    }
    
    response = client.post("/api/v1/agents/finance", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"

def test_wellness_agent_endpoint():
    """Test wellness agent endpoint."""
    payload = {
        "user_data": {
            "age": 28,
            "activity_level": "moderate",
            "health_goals": ["weight_loss"]
        },
        "task_type": "fitness_plan",
        "parameters": {"workout_days": 4}
    }
    
    response = client.post("/api/v1/agents/wellness", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"

def test_learning_agent_endpoint():
    """Test learning agent endpoint."""
    payload = {
        "user_data": {
            "current_skills": ["Python"],
            "interests": ["Machine Learning"],
            "learning_style": "hands_on"
        },
        "task_type": "course_recommendation",
        "parameters": {"budget": 500}
    }
    
    response = client.post("/api/v1/agents/learning", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"

def test_agent_health_endpoints():
    """Test agent health check endpoints."""
    agents = ["career", "finance", "wellness", "learning"]
    
    for agent in agents:
        response = client.get(f"/api/v1/agents/{agent}/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "agent_id" in data

def test_invalid_task_type():
    """Test handling of invalid task types."""
    payload = {
        "user_data": {"test": "data"},
        "task_type": "invalid_task",
        "parameters": {}
    }
    
    response = client.post("/api/v1/agents/career", json=payload)
    assert response.status_code == 500