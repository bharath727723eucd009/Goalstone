"""Test cases for logging and metrics."""
import pytest
from fastapi.testclient import TestClient
from ..main import app
from ..observability.metrics import metrics_collector

client = TestClient(app)

def test_metrics_endpoint():
    """Test Prometheus metrics endpoint."""
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "text/plain" in response.headers["content-type"]
    
    # Check for expected metrics
    content = response.text
    assert "api_requests_total" in content
    assert "agent_runs_total" in content
    assert "errors_total" in content

def test_metrics_collection():
    """Test metrics collection functionality."""
    # Record test metrics
    metrics_collector.record_api_request("GET", "/test", 200, 0.5, "test_user")
    metrics_collector.record_agent_run("career", "job_search", "success", 1.2, "test_user")
    metrics_collector.record_error("test_error", "test_component", "test_user")
    
    # Get metrics summary
    summary = metrics_collector.get_metrics_summary()
    assert "prometheus_metrics" in summary
    assert summary["prometheus_metrics"]["api_requests_total"] > 0

def test_logging_middleware():
    """Test that requests are logged through middleware."""
    # Make authenticated request
    login_response = client.post("/api/v1/auth/login", json={
        "username": "demo",
        "password": "password"
    })
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Make request that will be logged
    response = client.get("/api/v1/auth/me", headers=headers)
    assert response.status_code == 200
    
    # Check metrics endpoint shows the requests
    metrics_response = client.get("/metrics")
    assert "api_requests_total" in metrics_response.text