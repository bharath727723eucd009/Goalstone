"""Test cases for observability components."""
import pytest
from ..observability.metrics import MetricsCollector
from ..observability.evaluation import AgentEvaluator

def test_metrics_collector():
    """Test metrics collection functionality."""
    collector = MetricsCollector()
    
    # Record request metrics
    collector.record_request("GET", "/test", 200, 0.5)
    
    # Record agent task metrics
    collector.record_agent_task("career", "job_search", "success", 1.2)
    
    # Update active sessions
    collector.update_active_sessions(10)
    
    # Record custom metric
    collector.record_custom_metric("test_metric", 42.0, {"label": "test"})
    
    # Get metrics summary
    summary = collector.get_metrics_summary()
    assert "custom_metrics" in summary
    assert "test_metric" in summary["custom_metrics"]
    assert summary["custom_metrics"]["test_metric"]["value"] == 42.0

@pytest.mark.asyncio
async def test_agent_evaluator():
    """Test agent evaluation functionality."""
    evaluator = AgentEvaluator()
    
    task = {
        "id": "test_task",
        "type": "test",
        "start_time": 1000
    }
    
    response = {
        "status": "success",
        "data": {"result": "test"},
        "end_time": 1002
    }
    
    user_feedback = {
        "rating": 4,
        "comments": "Good response"
    }
    
    # Evaluate response
    evaluation = await evaluator.evaluate_agent_response(
        "test_agent", task, response, user_feedback
    )
    
    assert evaluation["agent_id"] == "test_agent"
    assert "metrics" in evaluation
    assert evaluation["metrics"]["user_satisfaction"] == 4
    assert evaluation["metrics"]["overall_score"] > 0
    
    # Get performance report
    report = await evaluator.get_agent_performance_report("test_agent", 7)
    assert report["agent_id"] == "test_agent"
    assert "metrics" in report
    assert "recommendations" in report