"""JWT authentication middleware with session injection."""
from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Optional
import structlog
from .jwt_handler import verify_token
from ..sessions.session_manager import SessionManager, InMemorySessionManager

logger = structlog.get_logger(__name__)
security = HTTPBearer()

class AuthMiddleware(BaseHTTPMiddleware):
    """JWT authentication middleware with session retrieval."""
    
    def __init__(self, app, session_manager: Optional[SessionManager] = None):
        super().__init__(app)
        self.session_manager = session_manager or InMemorySessionManager()
        self.public_paths = {"/", "/health", "/docs", "/openapi.json", "/api/v1/auth/login"}
    
    async def dispatch(self, request: Request, call_next):
        """Process request with authentication and session injection."""
        # Skip auth for public paths
        if request.url.path in self.public_paths:
            return await call_next(request)
        
        # Extract token
        authorization = request.headers.get("Authorization")
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing or invalid authorization header"
            )
        
        token = authorization.split(" ")[1]
        payload = verify_token(token)
        
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token"
            )
        
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )
        
        # Retrieve session
        session_id = payload.get("session_id")
        session_data = None
        
        if session_id:
            session_data = await self.session_manager.get_session(session_id)
            if not session_data:
                logger.warning("Session not found", session_id=session_id, user_id=user_id)
        
        # Inject user and session into request state
        request.state.user_id = user_id
        request.state.session_id = session_id
        request.state.session_data = session_data
        request.state.token_payload = payload
        
        logger.info("Request authenticated", user_id=user_id, path=request.url.path)
        
        return await call_next(request)

def get_current_user(request: Request) -> str:
    """Get current user ID from request state."""
    if not hasattr(request.state, "user_id"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated"
        )
    return request.state.user_id

def get_current_session(request: Request) -> Optional[dict]:
    """Get current session data from request state."""
    return getattr(request.state, "session_data", None)