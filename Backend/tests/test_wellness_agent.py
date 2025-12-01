"""Test cases for Wellness Agent."""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from ..main import app

client = TestClient(app)

@pytest.fixture
def auth_headers():
    """Get authentication headers."""
    login_response = client.post("/api/v1/auth/login", json={
        "username": "demo",
        "password": "password"
    })
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

class TestWellnessAgent:
    def test_fitness_plan_success(self, auth_headers):
        """Test fitness plan generation."""
        payload = {
            "user_data": {
                "age": 28,
                "weight": 70,
                "height": 175,
                "activity_level": "moderate",
                "health_goals": ["weight_loss", "muscle_gain"]
            },
            "task_type": "fitness_plan",
            "parameters": {
                "workout_days": 4,
                "equipment": ["dumbbells", "resistance_bands"]
            }
        }
        
        response = client.post("/api/v1/agents/wellness", json=payload, headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "data" in data

    def test_nutrition_advice_success(self, auth_headers):
        """Test nutrition advice generation."""
        payload = {
            "user_data": {
                "age": 30,
                "dietary_preferences": ["vegetarian"],
                "health_goals": ["weight_loss"]
            },
            "task_type": "nutrition_advice",
            "parameters": {
                "dietary_restrictions": ["gluten_free"],
                "nutrition_goals": ["high_protein"]
            }
        }
        
        response = client.post("/api/v1/agents/wellness", json=payload, headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"

    def test_health_assessment_success(self, auth_headers):
        """Test health assessment."""
        payload = {
            "user_data": {
                "age": 35,
                "weight": 80,
                "height": 180,
                "activity_level": "low"
            },
            "task_type": "health_assessment"
        }
        
        response = client.post("/api/v1/agents/wellness", json=payload, headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "assessment" in data["data"]

    def test_workout_recommendation_success(self, auth_headers):
        """Test workout recommendations."""
        payload = {
            "user_data": {
                "fitness_level": "beginner",
                "available_time": 30
            },
            "task_type": "workout_recommendation",
            "parameters": {
                "preferences": {
                    "workout_type": "cardio",
                    "duration": 30
                }
            }
        }
        
        response = client.post("/api/v1/agents/wellness", json=payload, headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"

    def test_wellness_no_auth(self):
        """Test wellness endpoint without authentication."""
        payload = {
            "user_data": {"age": 25},
            "task_type": "fitness_plan"
        }
        response = client.post("/api/v1/agents/wellness", json=payload)
        assert response.status_code == 401

    def test_wellness_invalid_task_type(self, auth_headers):
        """Test wellness with invalid task type."""
        payload = {
            "user_data": {"age": 25},
            "task_type": "invalid_task"
        }
        response = client.post("/api/v1/agents/wellness", json=payload, headers=auth_headers)
        assert response.status_code == 500

    def test_wellness_missing_user_data(self, auth_headers):
        """Test wellness with missing user data."""
        payload = {
            "task_type": "fitness_plan"
        }
        response = client.post("/api/v1/agents/wellness", json=payload, headers=auth_headers)
        assert response.status_code == 422

    def test_wellness_empty_payload(self, auth_headers):
        """Test wellness with empty payload."""
        response = client.post("/api/v1/agents/wellness", json={}, headers=auth_headers)
        assert response.status_code == 422

    @patch('Backend.agents.wellness.wellness_agent.WellnessAgent.run')
    async def test_wellness_agent_error(self, mock_run, auth_headers):
        """Test wellness agent execution error."""
        mock_run.return_value = {"status": "error", "error": "Test error"}
        
        payload = {
            "user_data": {"age": 25},
            "task_type": "fitness_plan"
        }
        response = client.post("/api/v1/agents/wellness", json=payload, headers=auth_headers)
        assert response.status_code == 500

    def test_wellness_health_endpoint(self):
        """Test wellness agent health check."""
        response = client.get("/api/v1/agents/wellness/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["agent_id"] == "wellness_agent"

    def test_wellness_bmi_calculation(self, auth_headers):
        """Test BMI calculation in health assessment."""
        payload = {
            "user_data": {
                "weight": 70,
                "height": 175,
                "age": 30
            },
            "task_type": "health_assessment"
        }
        
        response = client.post("/api/v1/agents/wellness", json=payload, headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        
        # BMI should be calculated (70 / (1.75^2) = 22.9)
        if "assessment" in data["data"]:
            bmi = data["data"]["assessment"].get("bmi", 0)
            assert 22 <= bmi <= 23

    def test_wellness_activity_scoring(self, auth_headers):
        """Test activity level scoring."""
        test_cases = [
            ("low", 1),
            ("moderate", 3),
            ("high", 5),
            ("very_high", 7)
        ]
        
        for activity_level, expected_score in test_cases:
            payload = {
                "user_data": {
                    "activity_level": activity_level,
                    "age": 25
                },
                "task_type": "health_assessment"
            }
            
            response = client.post("/api/v1/agents/wellness", json=payload, headers=auth_headers)
            assert response.status_code == 200
            data = response.json()
            
            if "assessment" in data["data"]:
                score = data["data"]["assessment"].get("activity_score", 0)
                assert score == expected_score