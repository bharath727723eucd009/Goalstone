"""Comprehensive test cases for all endpoints."""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from ..main import app

client = TestClient(app)

# Test fixtures
@pytest.fixture
def auth_headers():
    """Get authentication headers."""
    login_response = client.post("/api/v1/auth/login", json={
        "username": "demo",
        "password": "password"
    })
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def agent_request_data():
    """Sample agent request data."""
    return {
        "user_data": {"skills": ["Python"], "experience_years": 3},
        "task_type": "job_search",
        "parameters": {"remote_ok": True}
    }

@pytest.fixture
def user_profile_data():
    """Sample user profile data."""
    return {
        "name": "Test User",
        "email": "test@example.com",
        "skills": ["Python", "FastAPI"],
        "experience_years": 3,
        "income": 75000
    }

@pytest.fixture
def milestone_data():
    """Sample milestone data."""
    return {
        "title": "Learn Machine Learning",
        "description": "Complete ML course",
        "category": "learning",
        "priority": 3
    }

# Auth endpoint tests
class TestAuthEndpoints:
    def test_login_success(self):
        """Test successful login."""
        response = client.post("/api/v1/auth/login", json={
            "username": "demo",
            "password": "password"
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_invalid_credentials(self):
        """Test login with invalid credentials."""
        response = client.post("/api/v1/auth/login", json={
            "username": "invalid",
            "password": "wrong"
        })
        assert response.status_code == 401

    def test_login_missing_fields(self):
        """Test login with missing fields."""
        response = client.post("/api/v1/auth/login", json={
            "username": "demo"
        })
        assert response.status_code == 422

    def test_protected_route_no_token(self):
        """Test protected route without token."""
        response = client.get("/api/v1/auth/me")
        assert response.status_code == 401

    def test_protected_route_invalid_token(self):
        """Test protected route with invalid token."""
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.get("/api/v1/auth/me", headers=headers)
        assert response.status_code == 401

    def test_protected_route_success(self, auth_headers):
        """Test protected route with valid token."""
        response = client.get("/api/v1/auth/me", headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["authenticated"] is True

# Agent endpoint tests
class TestAgentEndpoints:
    def test_career_agent_success(self, auth_headers, agent_request_data):
        """Test career agent success."""
        response = client.post("/api/v1/agents/career", json=agent_request_data, headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"

    def test_finance_agent_success(self, auth_headers):
        """Test finance agent success."""
        payload = {
            "user_data": {"income": 75000, "expenses": 50000},
            "task_type": "budget_analysis"
        }
        response = client.post("/api/v1/agents/finance", json=payload, headers=auth_headers)
        assert response.status_code == 200

    def test_wellness_agent_success(self, auth_headers):
        """Test wellness agent success."""
        payload = {
            "user_data": {"age": 28, "activity_level": "moderate"},
            "task_type": "fitness_plan"
        }
        response = client.post("/api/v1/agents/wellness", json=payload, headers=auth_headers)
        assert response.status_code == 200

    def test_learning_agent_success(self, auth_headers):
        """Test learning agent success."""
        payload = {
            "user_data": {"current_skills": ["Python"], "interests": ["ML"]},
            "task_type": "course_recommendation"
        }
        response = client.post("/api/v1/agents/learning", json=payload, headers=auth_headers)
        assert response.status_code == 200

    def test_agent_no_auth(self, agent_request_data):
        """Test agent endpoint without authentication."""
        response = client.post("/api/v1/agents/career", json=agent_request_data)
        assert response.status_code == 401

    def test_agent_invalid_payload(self, auth_headers):
        """Test agent with invalid payload."""
        response = client.post("/api/v1/agents/career", json={}, headers=auth_headers)
        assert response.status_code == 422

    def test_agent_missing_fields(self, auth_headers):
        """Test agent with missing required fields."""
        payload = {"user_data": {}}
        response = client.post("/api/v1/agents/career", json=payload, headers=auth_headers)
        assert response.status_code == 422

    @patch('Backend.agents.career.career_agent.CareerAgent.run')
    async def test_agent_execution_error(self, mock_run, auth_headers, agent_request_data):
        """Test agent execution error handling."""
        mock_run.return_value = {"status": "error", "error": "Test error"}
        response = client.post("/api/v1/agents/career", json=agent_request_data, headers=auth_headers)
        assert response.status_code == 500

    def test_agent_health_endpoints(self):
        """Test agent health check endpoints."""
        agents = ["career", "finance", "wellness", "learning"]
        for agent in agents:
            response = client.get(f"/api/v1/agents/{agent}/health")
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"

# Data endpoint tests
class TestDataEndpoints:
    @patch('Backend.database.repository.UserRepository.create_user')
    @patch('Backend.database.repository.UserRepository.get_user')
    async def test_create_user_profile(self, mock_get, mock_create, auth_headers, user_profile_data):
        """Test user profile creation."""
        mock_get.return_value = None
        mock_create.return_value = "user_id_123"
        
        response = client.post("/api/v1/data/users/profile", json=user_profile_data, headers=auth_headers)
        assert response.status_code == 200

    @patch('Backend.database.repository.UserRepository.get_user')
    async def test_get_user_profile(self, mock_get, auth_headers):
        """Test get user profile."""
        mock_get.return_value = {"user_id": "test", "name": "Test User"}
        
        response = client.get("/api/v1/data/users/profile", headers=auth_headers)
        assert response.status_code == 200

    @patch('Backend.database.repository.UserRepository.get_user')
    async def test_get_user_profile_not_found(self, mock_get, auth_headers):
        """Test get user profile not found."""
        mock_get.return_value = None
        
        response = client.get("/api/v1/data/users/profile", headers=auth_headers)
        assert response.status_code == 404

    @patch('Backend.database.repository.MilestoneRepository.create_milestone')
    @patch('Backend.database.repository.ProgressRepository.update_user_progress')
    async def test_create_milestone(self, mock_progress, mock_create, auth_headers, milestone_data):
        """Test milestone creation."""
        mock_create.return_value = "milestone_id_123"
        
        response = client.post("/api/v1/data/milestones", json=milestone_data, headers=auth_headers)
        assert response.status_code == 200

    @patch('Backend.database.repository.MilestoneRepository.get_user_milestones')
    async def test_get_milestones(self, mock_get, auth_headers):
        """Test get user milestones."""
        mock_get.return_value = []
        
        response = client.get("/api/v1/data/milestones", headers=auth_headers)
        assert response.status_code == 200

    @patch('Backend.database.repository.MilestoneRepository.get_milestone')
    @patch('Backend.database.repository.MilestoneRepository.update_milestone')
    async def test_update_milestone(self, mock_update, mock_get, auth_headers):
        """Test milestone update."""
        mock_get.return_value = type('obj', (object,), {"user_id": "demo_user", "category": "learning"})
        mock_update.return_value = True
        
        updates = {"status": "completed", "progress": 1.0}
        response = client.put("/api/v1/data/milestones/123", json=updates, headers=auth_headers)
        assert response.status_code == 200

    @patch('Backend.database.repository.MilestoneRepository.get_milestone')
    async def test_update_milestone_not_found(self, mock_get, auth_headers):
        """Test update non-existent milestone."""
        mock_get.return_value = None
        
        updates = {"status": "completed"}
        response = client.put("/api/v1/data/milestones/123", json=updates, headers=auth_headers)
        assert response.status_code == 404

    def test_data_endpoints_no_auth(self, user_profile_data):
        """Test data endpoints without authentication."""
        response = client.post("/api/v1/data/users/profile", json=user_profile_data)
        assert response.status_code == 401

    def test_invalid_milestone_data(self, auth_headers):
        """Test milestone creation with invalid data."""
        invalid_data = {"title": ""}  # Missing required fields
        response = client.post("/api/v1/data/milestones", json=invalid_data, headers=auth_headers)
        assert response.status_code == 422

    @patch('Backend.database.repository.AgentOutputRepository.get_user_agent_history')
    async def test_get_agent_history(self, mock_get, auth_headers):
        """Test get agent execution history."""
        mock_get.return_value = []
        
        response = client.get("/api/v1/data/agent-outputs", headers=auth_headers)
        assert response.status_code == 200

    @patch('Backend.database.repository.ProgressRepository.get_user_progress')
    async def test_get_user_progress(self, mock_get, auth_headers):
        """Test get user progress."""
        mock_get.return_value = []
        
        response = client.get("/api/v1/data/progress", headers=auth_headers)
        assert response.status_code == 200

# Database error tests
class TestDatabaseErrors:
    @patch('Backend.database.repository.UserRepository.create_user')
    async def test_database_connection_error(self, mock_create, auth_headers, user_profile_data):
        """Test database connection error handling."""
        mock_create.side_effect = Exception("Database connection failed")
        
        response = client.post("/api/v1/data/users/profile", json=user_profile_data, headers=auth_headers)
        assert response.status_code == 500

    @patch('Backend.database.repository.MilestoneRepository.create_milestone')
    async def test_milestone_creation_db_error(self, mock_create, auth_headers, milestone_data):
        """Test milestone creation database error."""
        mock_create.side_effect = Exception("Database error")
        
        response = client.post("/api/v1/data/milestones", json=milestone_data, headers=auth_headers)
        assert response.status_code == 500

# Metrics endpoint tests
class TestMetricsEndpoint:
    def test_metrics_endpoint_available(self):
        """Test metrics endpoint is available."""
        response = client.get("/metrics")
        assert response.status_code == 200
        assert "text/plain" in response.headers["content-type"]

    def test_metrics_content(self):
        """Test metrics endpoint returns expected content."""
        response = client.get("/metrics")
        content = response.text
        
        # Check for expected metric names
        expected_metrics = [
            "api_requests_total",
            "agent_runs_total", 
            "errors_total",
            "api_request_duration_seconds",
            "agent_execution_duration_seconds"
        ]
        
        for metric in expected_metrics:
            assert metric in content

    def test_metrics_after_requests(self, auth_headers, agent_request_data):
        """Test metrics are updated after making requests."""
        # Make some requests to generate metrics
        client.post("/api/v1/agents/career", json=agent_request_data, headers=auth_headers)
        client.get("/api/v1/auth/me", headers=auth_headers)
        
        # Check metrics
        response = client.get("/metrics")
        assert response.status_code == 200
        
        content = response.text
        assert "api_requests_total" in content
        assert "agent_runs_total" in content

# Integration tests
class TestIntegration:
    def test_full_user_workflow(self, auth_headers):
        """Test complete user workflow."""
        # 1. Create user profile
        profile_data = {
            "name": "Integration Test User",
            "email": "integration@test.com",
            "skills": ["Python", "Testing"],
            "experience_years": 2
        }
        
        with patch('Backend.database.repository.UserRepository.get_user') as mock_get, \
             patch('Backend.database.repository.UserRepository.create_user') as mock_create:
            mock_get.return_value = None
            mock_create.return_value = "user_123"
            
            profile_response = client.post("/api/v1/data/users/profile", json=profile_data, headers=auth_headers)
            assert profile_response.status_code == 200
        
        # 2. Create milestone
        milestone_data = {
            "title": "Complete Integration Test",
            "description": "Test the full workflow",
            "category": "learning",
            "priority": 1
        }
        
        with patch('Backend.database.repository.MilestoneRepository.create_milestone') as mock_create, \
             patch('Backend.database.repository.ProgressRepository.update_user_progress') as mock_progress:
            mock_create.return_value = "milestone_123"
            
            milestone_response = client.post("/api/v1/data/milestones", json=milestone_data, headers=auth_headers)
            assert milestone_response.status_code == 200
        
        # 3. Run agent
        agent_data = {
            "user_data": {"skills": ["Python"], "interests": ["Testing"]},
            "task_type": "course_recommendation"
        }
        
        agent_response = client.post("/api/v1/agents/learning", json=agent_data, headers=auth_headers)
        assert agent_response.status_code == 200
        
        # 4. Check metrics
        metrics_response = client.get("/metrics")
        assert metrics_response.status_code == 200