"""Prometheus metrics endpoint."""
from fastapi import APIRouter, Response
from prometheus_client import CONTENT_TYPE_LATEST
from ..observability.metrics import get_prometheus_metrics

router = APIRouter(tags=["metrics"])

@router.get("/metrics")
async def prometheus_metrics():
    """Prometheus-compatible metrics endpoint."""
    metrics_data = get_prometheus_metrics()
    return Response(
        content=metrics_data,
        media_type=CONTENT_TYPE_LATEST
    )