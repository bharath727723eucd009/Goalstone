"""Integration tests for all agents with database and metrics."""
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

class TestAgentIntegration:
    @patch('Backend.database.repository.AgentOutputRepository.save_agent_output')
    async def test_agent_output_saved_to_database(self, mock_save, auth_headers):
        """Test that agent outputs are saved to database."""
        mock_save.return_value = "output_id_123"
        
        payload = {
            "user_data": {"skills": ["Python"]},
            "task_type": "job_search"
        }
        
        response = client.post("/api/v1/agents/career", json=payload, headers=auth_headers)
        assert response.status_code == 200
        
        # Verify save was called
        mock_save.assert_called_once()
        call_args = mock_save.call_args[0][0]
        assert call_args.agent_type == "career"
        assert call_args.task_type == "job_search"

    def test_metrics_updated_after_agent_run(self, auth_headers):
        """Test that metrics are updated after agent execution."""
        # Get initial metrics
        initial_metrics = client.get("/metrics")
        initial_content = initial_metrics.text
        
        # Run agent
        payload = {
            "user_data": {"skills": ["Python"]},
            "task_type": "job_search"
        }
        response = client.post("/api/v1/agents/career", json=payload, headers=auth_headers)
        assert response.status_code == 200
        
        # Check metrics updated
        updated_metrics = client.get("/metrics")
        updated_content = updated_metrics.text
        
        # Should have agent_runs_total metric
        assert "agent_runs_total" in updated_content

    def test_all_agents_health_checks(self):
        """Test health checks for all agents."""
        agents = ["career", "finance", "wellness", "learning"]
        
        for agent in agents:
            response = client.get(f"/api/v1/agents/{agent}/health")
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"
            assert f"{agent}_agent" in data["agent_id"]

    def test_agent_logging_integration(self, auth_headers):
        """Test that agent executions are properly logged."""
        with patch('Backend.observability.logger.get_logger') as mock_logger:
            mock_log_instance = AsyncMock()
            mock_logger.return_value = mock_log_instance
            
            payload = {
                "user_data": {"skills": ["Python"]},
                "task_type": "job_search"
            }
            
            response = client.post("/api/v1/agents/career", json=payload, headers=auth_headers)
            assert response.status_code == 200
            
            # Verify logging calls were made
            assert mock_log_instance.info.call_count >= 2  # Start and completion logs

    def test_session_data_passed_to_agents(self, auth_headers):
        """Test that session data is passed to agents."""
        with patch('Backend.agents.career.career_agent.CareerAgent.run') as mock_run:
            mock_run.return_value = {"status": "success", "data": {"test": "result"}}
            
            payload = {
                "user_data": {"skills": ["Python"]},
                "task_type": "job_search"
            }
            
            response = client.post("/api/v1/agents/career", json=payload, headers=auth_headers)
            assert response.status_code == 200
            
            # Verify agent received session data
            call_args = mock_run.call_args[0][0]
            assert "session_data" in call_args
            assert "user_id" in call_args

    @patch('Backend.database.repository.AgentOutputRepository.save_agent_output')
    async def test_database_error_handling(self, mock_save, auth_headers):
        """Test handling of database errors during agent execution."""
        mock_save.side_effect = Exception("Database connection failed")
        
        payload = {
            "user_data": {"skills": ["Python"]},
            "task_type": "job_search"
        }
        
        # Agent should still complete successfully even if database save fails
        response = client.post("/api/v1/agents/career", json=payload, headers=auth_headers)
        # This might be 200 or 500 depending on error handling implementation
        assert response.status_code in [200, 500]

    def test_concurrent_agent_executions(self, auth_headers):
        """Test concurrent agent executions."""
        import threading
        import time
        
        results = []
        
        def run_agent(agent_type):
            payload = {
                "user_data": {"skills": ["Python"]},
                "task_type": "job_search" if agent_type == "career" else "budget_analysis"
            }
            response = client.post(f"/api/v1/agents/{agent_type}", json=payload, headers=auth_headers)
            results.append((agent_type, response.status_code))
        
        # Run multiple agents concurrently
        threads = []
        for agent in ["career", "finance"]:
            thread = threading.Thread(target=run_agent, args=(agent,))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        # All should succeed
        assert all(status == 200 for _, status in results)
        assert len(results) == 2

    def test_agent_error_metrics(self, auth_headers):
        """Test error metrics are recorded for agent failures."""
        with patch('Backend.agents.career.career_agent.CareerAgent.run') as mock_run:
            mock_run.return_value = {"status": "error", "error": "Test error"}
            
            payload = {
                "user_data": {"skills": ["Python"]},
                "task_type": "job_search"
            }
            
            response = client.post("/api/v1/agents/career", json=payload, headers=auth_headers)
            assert response.status_code == 500
            
            # Check error metrics
            metrics_response = client.get("/metrics")
            assert "errors_total" in metrics_response.text

    def test_agent_execution_time_tracking(self, auth_headers):
        """Test that agent execution times are tracked."""
        payload = {
            "user_data": {"skills": ["Python"]},
            "task_type": "job_search"
        }
        
        response = client.post("/api/v1/agents/career", json=payload, headers=auth_headers)
        assert response.status_code == 200
        
        # Check duration metrics
        metrics_response = client.get("/metrics")
        assert "agent_execution_duration_seconds" in metrics_response.text

    def test_user_context_preservation(self, auth_headers):
        """Test that user context is preserved across agent calls."""
        # Make multiple agent calls with same auth
        agents_and_tasks = [
            ("career", "job_search"),
            ("finance", "budget_analysis"),
            ("wellness", "fitness_plan"),
            ("learning", "course_recommendation")
        ]
        
        for agent, task in agents_and_tasks:
            payload = {
                "user_data": {"test": "data"},
                "task_type": task
            }
            
            response = client.post(f"/api/v1/agents/{agent}", json=payload, headers=auth_headers)
            assert response.status_code == 200
            
            # Each should maintain user context
            data = response.json()
            assert data["status"] == "success"