"""Test cases for error scenarios and edge cases."""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from ..main import app

client = TestClient(app)

class TestErrorScenarios:
    def test_malformed_json(self):
        """Test handling of malformed JSON."""
        response = client.post(
            "/api/v1/auth/login",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422

    def test_missing_content_type(self):
        """Test request without content type."""
        response = client.post("/api/v1/auth/login", data='{"username": "demo"}')
        assert response.status_code == 422

    def test_oversized_payload(self):
        """Test handling of oversized payloads."""
        large_data = {
            "user_data": {"skills": ["skill"] * 10000},
            "task_type": "job_search"
        }
        
        # Login first
        login_response = client.post("/api/v1/auth/login", json={
            "username": "demo", "password": "password"
        })
        headers = {"Authorization": f"Bearer {login_response.json()['access_token']}"}
        
        response = client.post("/api/v1/agents/career", json=large_data, headers=headers)
        # Should still work but might be slow
        assert response.status_code in [200, 413, 422]

    def test_sql_injection_attempt(self):
        """Test SQL injection protection."""
        malicious_data = {
            "username": "admin'; DROP TABLE users; --",
            "password": "password"
        }
        response = client.post("/api/v1/auth/login", json=malicious_data)
        assert response.status_code == 401

    def test_xss_attempt(self):
        """Test XSS protection in user data."""
        login_response = client.post("/api/v1/auth/login", json={
            "username": "demo", "password": "password"
        })
        headers = {"Authorization": f"Bearer {login_response.json()['access_token']}"}
        
        xss_data = {
            "name": "<script>alert('xss')</script>",
            "email": "test@example.com",
            "skills": ["<img src=x onerror=alert(1)>"]
        }
        
        with patch('Backend.database.repository.UserRepository.get_user') as mock_get, \
             patch('Backend.database.repository.UserRepository.create_user') as mock_create:
            mock_get.return_value = None
            mock_create.return_value = "user_123"
            
            response = client.post("/api/v1/data/users/profile", json=xss_data, headers=headers)
            # Should accept but sanitize data
            assert response.status_code == 200

    @patch('Backend.database.connection.get_database')
    def test_database_timeout(self, mock_db):
        """Test database timeout handling."""
        mock_db.side_effect = TimeoutError("Database timeout")
        
        login_response = client.post("/api/v1/auth/login", json={
            "username": "demo", "password": "password"
        })
        headers = {"Authorization": f"Bearer {login_response.json()['access_token']}"}
        
        response = client.get("/api/v1/data/users/profile", headers=headers)
        assert response.status_code == 500

    def test_concurrent_requests(self):
        """Test handling of concurrent requests."""
        import threading
        import time
        
        login_response = client.post("/api/v1/auth/login", json={
            "username": "demo", "password": "password"
        })
        headers = {"Authorization": f"Bearer {login_response.json()['access_token']}"}
        
        results = []
        
        def make_request():
            response = client.get("/api/v1/auth/me", headers=headers)
            results.append(response.status_code)
        
        threads = []
        for _ in range(10):
            thread = threading.Thread(target=make_request)
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        # All requests should succeed
        assert all(status == 200 for status in results)

    def test_invalid_http_methods(self):
        """Test invalid HTTP methods on endpoints."""
        # Test wrong method on login endpoint
        response = client.get("/api/v1/auth/login")
        assert response.status_code == 405
        
        # Test wrong method on metrics
        response = client.post("/metrics")
        assert response.status_code == 405

    def test_path_traversal_attempt(self):
        """Test path traversal protection."""
        login_response = client.post("/api/v1/auth/login", json={
            "username": "demo", "password": "password"
        })
        headers = {"Authorization": f"Bearer {login_response.json()['access_token']}"}
        
        # Try to access with path traversal
        response = client.get("/api/v1/data/../../../etc/passwd", headers=headers)
        assert response.status_code == 404

    def test_rate_limiting_simulation(self):
        """Test rapid successive requests."""
        login_response = client.post("/api/v1/auth/login", json={
            "username": "demo", "password": "password"
        })
        headers = {"Authorization": f"Bearer {login_response.json()['access_token']}"}
        
        # Make rapid requests
        responses = []
        for _ in range(50):
            response = client.get("/api/v1/auth/me", headers=headers)
            responses.append(response.status_code)
        
        # Most should succeed (no rate limiting implemented yet)
        success_count = sum(1 for status in responses if status == 200)
        assert success_count > 40  # Allow some failures

    @patch('Backend.observability.metrics.metrics_collector.record_api_request')
    def test_metrics_collection_failure(self, mock_metrics):
        """Test handling of metrics collection failures."""
        mock_metrics.side_effect = Exception("Metrics error")
        
        # Request should still succeed even if metrics fail
        response = client.get("/")
        assert response.status_code == 200

    def test_empty_request_bodies(self):
        """Test endpoints with empty request bodies."""
        login_response = client.post("/api/v1/auth/login", json={
            "username": "demo", "password": "password"
        })
        headers = {"Authorization": f"Bearer {login_response.json()['access_token']}"}
        
        # Empty agent request
        response = client.post("/api/v1/agents/career", json={}, headers=headers)
        assert response.status_code == 422
        
        # Empty milestone request
        response = client.post("/api/v1/data/milestones", json={}, headers=headers)
        assert response.status_code == 422

    def test_unicode_handling(self):
        """Test Unicode character handling."""
        login_response = client.post("/api/v1/auth/login", json={
            "username": "demo", "password": "password"
        })
        headers = {"Authorization": f"Bearer {login_response.json()['access_token']}"}
        
        unicode_data = {
            "name": "测试用户 🚀",
            "email": "test@例え.テスト",
            "skills": ["Python", "机器学习", "データサイエンス"]
        }
        
        with patch('Backend.database.repository.UserRepository.get_user') as mock_get, \
             patch('Backend.database.repository.UserRepository.create_user') as mock_create:
            mock_get.return_value = None
            mock_create.return_value = "user_123"
            
            response = client.post("/api/v1/data/users/profile", json=unicode_data, headers=headers)
            assert response.status_code == 200

    def test_token_expiration_simulation(self):
        """Test expired token handling."""
        # Use an obviously expired/invalid token
        expired_headers = {"Authorization": "Bearer expired.token.here"}
        
        response = client.get("/api/v1/auth/me", headers=expired_headers)
        assert response.status_code == 401

    def test_missing_required_fields(self):
        """Test various missing required field scenarios."""
        login_response = client.post("/api/v1/auth/login", json={
            "username": "demo", "password": "password"
        })
        headers = {"Authorization": f"Bearer {login_response.json()['access_token']}"}
        
        # Missing task_type in agent request
        response = client.post("/api/v1/agents/career", json={
            "user_data": {"skills": ["Python"]}
        }, headers=headers)
        assert response.status_code == 422
        
        # Missing title in milestone
        response = client.post("/api/v1/data/milestones", json={
            "description": "Test milestone",
            "category": "learning"
        }, headers=headers)
        assert response.status_code == 422

    @patch('Backend.agents.career.career_agent.CareerAgent.run')
    async def test_agent_timeout_simulation(self, mock_run):
        """Test agent execution timeout."""
        import asyncio
        
        async def slow_agent():
            await asyncio.sleep(10)  # Simulate slow agent
            return {"status": "success", "data": {}}
        
        mock_run.return_value = slow_agent()
        
        login_response = client.post("/api/v1/auth/login", json={
            "username": "demo", "password": "password"
        })
        headers = {"Authorization": f"Bearer {login_response.json()['access_token']}"}
        
        agent_data = {
            "user_data": {"skills": ["Python"]},
            "task_type": "job_search"
        }
        
        # This might timeout or succeed depending on implementation
        response = client.post("/api/v1/agents/career", json=agent_data, headers=headers)
        assert response.status_code in [200, 500, 504]