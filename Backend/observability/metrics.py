"""Metrics collection and monitoring."""
import time
from typing import Dict, Any
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from ..observability.logger import get_logger

logger = get_logger(__name__)

# Prometheus metrics
API_REQUESTS = Counter('api_requests_total', 'Total API requests', ['method', 'endpoint', 'status_code', 'user_id'])
API_DURATION = Histogram('api_request_duration_seconds', 'API request duration', ['method', 'endpoint'])
AGENT_RUNS = Counter('agent_runs_total', 'Total agent runs', ['agent_type', 'task_type', 'status', 'user_id'])
AGENT_DURATION = Histogram('agent_execution_duration_seconds', 'Agent execution duration', ['agent_type', 'task_type'])
ERROR_COUNT = Counter('errors_total', 'Total errors', ['error_type', 'component', 'user_id'])
ACTIVE_SESSIONS = Gauge('active_sessions_total', 'Number of active sessions')
DATABASE_OPERATIONS = Counter('database_operations_total', 'Database operations', ['operation', 'collection', 'status'])
TOOL_USAGE = Counter('tool_usage_total', 'Tool usage', ['tool_type', 'user_id', 'status'])
TOOL_DURATION = Histogram('tool_execution_duration_seconds', 'Tool execution duration', ['tool_type'])

class MetricsCollector:
    """Centralized metrics collection."""
    
    def __init__(self):
        self.custom_metrics = {}
    
    def record_api_request(self, method: str, endpoint: str, status_code: int, duration: float, user_id: str = "anonymous"):
        """Record API request metrics."""
        API_REQUESTS.labels(method=method, endpoint=endpoint, status_code=status_code, user_id=user_id).inc()
        API_DURATION.labels(method=method, endpoint=endpoint).observe(duration)
        logger.info("API request recorded", method=method, endpoint=endpoint, status_code=status_code, duration=duration, user_id=user_id)
    
    def record_agent_run(self, agent_type: str, task_type: str, status: str, duration: float, user_id: str):
        """Record agent execution metrics."""
        AGENT_RUNS.labels(agent_type=agent_type, task_type=task_type, status=status, user_id=user_id).inc()
        AGENT_DURATION.labels(agent_type=agent_type, task_type=task_type).observe(duration)
        logger.info("Agent run recorded", agent_type=agent_type, task_type=task_type, status=status, duration=duration, user_id=user_id)
    
    def record_error(self, error_type: str, component: str, user_id: str = "anonymous", error_message: str = ""):
        """Record error metrics."""
        ERROR_COUNT.labels(error_type=error_type, component=component, user_id=user_id).inc()
        logger.error("Error recorded", error_type=error_type, component=component, user_id=user_id, error_message=error_message)
    
    def record_database_operation(self, operation: str, collection: str, status: str):
        """Record database operation metrics."""
        DATABASE_OPERATIONS.labels(operation=operation, collection=collection, status=status).inc()
        logger.debug("Database operation recorded", operation=operation, collection=collection, status=status)
    
    def update_active_sessions(self, count: int):
        """Update active sessions count."""
        ACTIVE_SESSIONS.set(count)
    
    def record_tool_usage(self, tool_type: str, user_id: str, duration: float, status: str):
        """Record tool usage metrics."""
        TOOL_USAGE.labels(tool_type=tool_type, user_id=user_id, status=status).inc()
        TOOL_DURATION.labels(tool_type=tool_type).observe(duration)
        logger.info("Tool usage recorded", tool_type=tool_type, user_id=user_id, duration=duration, status=status)
    
    def record_custom_metric(self, name: str, value: float, labels: Dict[str, str] = None):
        """Record custom metric."""
        self.custom_metrics[name] = {
            "value": value,
            "labels": labels or {},
            "timestamp": time.time()
        }
        logger.info("Custom metric recorded", metric=name, value=value, labels=labels)
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get summary of all metrics."""
        return {
            "custom_metrics": self.custom_metrics,
            "prometheus_metrics": {
                "api_requests_total": sum(API_REQUESTS._value.values()),
                "agent_runs_total": sum(AGENT_RUNS._value.values()),
                "errors_total": sum(ERROR_COUNT._value.values()),
                "active_sessions": ACTIVE_SESSIONS._value.get(),
                "tool_usage_total": sum(TOOL_USAGE._value.values())
            }
        }

# Global metrics collector instance
metrics_collector = MetricsCollector()

def get_prometheus_metrics():
    """Get Prometheus metrics in text format."""
    return generate_latest()