"""Logging and metrics middleware for FastAPI."""
import time
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from .metrics import metrics_collector
from .logger import get_logger

logger = get_logger(__name__)

class LoggingMetricsMiddleware(BaseHTTPMiddleware):
    """Middleware for logging and metrics collection."""
    
    async def dispatch(self, request: Request, call_next):
        """Process request with logging and metrics."""
        start_time = time.time()
        
        # Extract user info if available
        user_id = getattr(request.state, 'user_id', 'anonymous')
        
        # Log request start
        logger.info(
            "Request started",
            method=request.method,
            url=str(request.url),
            user_id=user_id,
            client_ip=request.client.host if request.client else "unknown"
        )
        
        try:
            # Process request
            response = await call_next(request)
            
            # Calculate duration
            duration = time.time() - start_time
            
            # Record metrics
            endpoint = request.url.path
            metrics_collector.record_api_request(
                method=request.method,
                endpoint=endpoint,
                status_code=response.status_code,
                duration=duration,
                user_id=user_id
            )
            
            # Log successful response
            logger.info(
                "Request completed",
                method=request.method,
                endpoint=endpoint,
                status_code=response.status_code,
                duration=duration,
                user_id=user_id
            )
            
            return response
            
        except Exception as e:
            # Calculate duration for failed requests
            duration = time.time() - start_time
            
            # Record error metrics
            metrics_collector.record_error(
                error_type=type(e).__name__,
                component="api",
                user_id=user_id,
                error_message=str(e)
            )
            
            # Log error
            logger.error(
                "Request failed",
                method=request.method,
                endpoint=request.url.path,
                duration=duration,
                user_id=user_id,
                error=str(e),
                error_type=type(e).__name__
            )
            
            raise