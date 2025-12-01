"""Test cases for Learning Agent."""
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

class TestLearningAgent:
    def test_course_recommendation_success(self, auth_headers):
        """Test course recommendation."""
        payload = {
            "user_data": {
                "current_skills": ["Python", "SQL"],
                "interests": ["Machine Learning", "Data Science"],
                "learning_style": "hands_on",
                "time_commitment": "10_hours_week"
            },
            "task_type": "course_recommendation",
            "parameters": {
                "budget": 500,
                "certification_required": True
            }
        }
        
        response = client.post("/api/v1/agents/learning", json=payload, headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "data" in data

    def test_skill_gap_analysis_success(self, auth_headers):
        """Test skill gap analysis."""
        payload = {
            "user_data": {
                "current_skills": ["Python", "HTML"],
                "target_role": "Data Scientist"
            },
            "task_type": "skill_gap_analysis",
            "parameters": {
                "current_skills": ["Python", "HTML"],
                "target_skills": ["Python", "Machine Learning", "Statistics", "SQL"]
            }
        }
        
        response = client.post("/api/v1/agents/learning", json=payload, headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"

    def test_learning_path_success(self, auth_headers):
        """Test learning path generation."""
        payload = {
            "user_data": {
                "current_skills": ["Basic Programming"],
                "time_commitment": "5_hours_week",
                "learning_style": "visual"
            },
            "task_type": "learning_path",
            "parameters": {
                "learning_goal": "Become a Full Stack Developer"
            }
        }
        
        response = client.post("/api/v1/agents/learning", json=payload, headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "learning_path" in data["data"]

    def test_certification_guidance_success(self, auth_headers):
        """Test certification guidance."""
        payload = {
            "user_data": {
                "experience_level": "intermediate",
                "field_of_interest": "cloud_computing"
            },
            "task_type": "certification_guidance",
            "parameters": {
                "field": "data_science",
                "experience_level": "beginner"
            }
        }
        
        response = client.post("/api/v1/agents/learning", json=payload, headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"

    def test_learning_no_auth(self):
        """Test learning endpoint without authentication."""
        payload = {
            "user_data": {"current_skills": ["Python"]},
            "task_type": "course_recommendation"
        }
        response = client.post("/api/v1/agents/learning", json=payload)
        assert response.status_code == 401

    def test_learning_invalid_task_type(self, auth_headers):
        """Test learning with invalid task type."""
        payload = {
            "user_data": {"current_skills": ["Python"]},
            "task_type": "invalid_task"
        }
        response = client.post("/api/v1/agents/learning", json=payload, headers=auth_headers)
        assert response.status_code == 500

    def test_learning_missing_user_data(self, auth_headers):
        """Test learning with missing user data."""
        payload = {
            "task_type": "course_recommendation"
        }
        response = client.post("/api/v1/agents/learning", json=payload, headers=auth_headers)
        assert response.status_code == 422

    def test_learning_empty_payload(self, auth_headers):
        """Test learning with empty payload."""
        response = client.post("/api/v1/agents/learning", json={}, headers=auth_headers)
        assert response.status_code == 422

    @patch('Backend.agents.learning.learning_agent.LearningAgent.run')
    async def test_learning_agent_error(self, mock_run, auth_headers):
        """Test learning agent execution error."""
        mock_run.return_value = {"status": "error", "error": "Test error"}
        
        payload = {
            "user_data": {"current_skills": ["Python"]},
            "task_type": "course_recommendation"
        }
        response = client.post("/api/v1/agents/learning", json=payload, headers=auth_headers)
        assert response.status_code == 500

    def test_learning_health_endpoint(self):
        """Test learning agent health check."""
        response = client.get("/api/v1/agents/learning/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["agent_id"] == "learning_agent"

    def test_skill_gap_identification(self, auth_headers):
        """Test skill gap identification logic."""
        payload = {
            "user_data": {
                "current_skills": ["Python", "HTML"]
            },
            "task_type": "skill_gap_analysis",
            "parameters": {
                "current_skills": ["Python", "HTML"],
                "target_skills": ["Python", "Machine Learning", "Statistics", "SQL"]
            }
        }
        
        response = client.post("/api/v1/agents/learning", json=payload, headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        
        # Should identify Machine Learning, Statistics, SQL as gaps
        if "analysis" in data["data"]:
            gaps = data["data"]["analysis"].get("skill_gaps", [])
            expected_gaps = ["Machine Learning", "Statistics", "SQL"]
            assert all(gap in gaps for gap in expected_gaps)

    def test_learning_path_structure(self, auth_headers):
        """Test learning path structure."""
        payload = {
            "user_data": {
                "current_skills": ["Basic Programming"],
                "time_commitment": "10_hours_week"
            },
            "task_type": "learning_path",
            "parameters": {
                "learning_goal": "Web Development"
            }
        }
        
        response = client.post("/api/v1/agents/learning", json=payload, headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        
        if "learning_path" in data["data"]:
            path = data["data"]["learning_path"]
            assert "goal" in path
            assert "total_duration" in path
            assert "phases" in path
            assert isinstance(path["phases"], list)
            assert len(path["phases"]) > 0

    def test_certification_recommendations(self, auth_headers):
        """Test certification recommendations by field."""
        test_cases = [
            ("data_science", ["Google Data Analytics", "AWS Machine Learning"]),
            ("software_development", ["AWS Developer Associate", "Google Cloud Professional"])
        ]
        
        for field, expected_certs in test_cases:
            payload = {
                "user_data": {"experience_level": "beginner"},
                "task_type": "certification_guidance",
                "parameters": {
                    "field": field,
                    "experience_level": "beginner"
                }
            }
            
            response = client.post("/api/v1/agents/learning", json=payload, headers=auth_headers)
            assert response.status_code == 200
            data = response.json()
            
            if "certifications" in data["data"]:
                certs = data["data"]["certifications"]
                cert_names = [cert["name"] for cert in certs]
                assert any(expected_cert in cert_names for expected_cert in expected_certs)

    def test_learning_recommendations_format(self, auth_headers):
        """Test learning recommendations response format."""
        payload = {
            "user_data": {
                "interests": ["Python", "Data Science"],
                "skill_level": "beginner"
            },
            "task_type": "course_recommendation"
        }
        
        response = client.post("/api/v1/agents/learning", json=payload, headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        
        # Should return structured course data
        assert "data" in data
        # The actual structure depends on the agent implementation