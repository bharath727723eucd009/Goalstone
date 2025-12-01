"""Performance and load testing."""
import pytest
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor
from fastapi.testclient import TestClient
from ..main import app

client = TestClient(app)

@pytest.mark.slow
class TestPerformance:
    def test_login_performance(self):
        """Test login endpoint performance."""
        start_time = time.time()
        
        for _ in range(10):
            response = client.post("/api/v1/auth/login", json={
                "username": "demo",
                "password": "password"
            })
            assert response.status_code == 200
        
        end_time = time.time()
        avg_time = (end_time - start_time) / 10
        
        # Should complete within reasonable time
        assert avg_time < 1.0  # Less than 1 second per login

    def test_metrics_endpoint_performance(self):
        """Test metrics endpoint performance."""
        start_time = time.time()
        
        for _ in range(20):
            response = client.get("/metrics")
            assert response.status_code == 200
        
        end_time = time.time()
        avg_time = (end_time - start_time) / 20
        
        # Metrics should be fast
        assert avg_time < 0.1  # Less than 100ms per request

    def test_concurrent_agent_requests(self):
        """Test concurrent agent requests."""
        # Login first
        login_response = client.post("/api/v1/auth/login", json={
            "username": "demo", "password": "password"
        })
        headers = {"Authorization": f"Bearer {login_response.json()['access_token']}"}
        
        def make_agent_request():
            return client.post("/api/v1/agents/career", json={
                "user_data": {"skills": ["Python"]},
                "task_type": "job_search"
            }, headers=headers)
        
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(make_agent_request) for _ in range(10)]
            results = [future.result() for future in futures]
        
        end_time = time.time()
        
        # All requests should succeed
        assert all(r.status_code == 200 for r in results)
        
        # Should complete within reasonable time
        assert (end_time - start_time) < 10.0

    def test_memory_usage_stability(self):
        """Test memory usage doesn't grow excessively."""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
        # Make many requests
        login_response = client.post("/api/v1/auth/login", json={
            "username": "demo", "password": "password"
        })
        headers = {"Authorization": f"Bearer {login_response.json()['access_token']}"}
        
        for _ in range(100):
            client.get("/api/v1/auth/me", headers=headers)
            client.get("/metrics")
        
        final_memory = process.memory_info().rss
        memory_growth = final_memory - initial_memory
        
        # Memory growth should be reasonable (less than 50MB)
        assert memory_growth < 50 * 1024 * 1024