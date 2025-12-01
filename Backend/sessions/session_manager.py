"""Session management for user interactions."""
import json
import asyncio
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import redis.asyncio as redis
from ..config import settings

class SessionManager:
    """Manages user sessions with Redis backend."""
    
    def __init__(self):
        self.redis_client = None
        self.session_timeout = 3600  # 1 hour
    
    async def initialize(self):
        """Initialize Redis connection."""
        self.redis_client = redis.from_url(settings.redis_url)
    
    async def create_session(self, user_id: str, session_data: Dict[str, Any]) -> str:
        """Create a new user session."""
        session_id = f"session:{user_id}:{datetime.now().timestamp()}"
        session_data.update({
            "user_id": user_id,
            "created_at": datetime.now().isoformat(),
            "last_activity": datetime.now().isoformat()
        })
        
        await self.redis_client.setex(
            session_id,
            self.session_timeout,
            json.dumps(session_data)
        )
        return session_id
    
    async def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve session data."""
        data = await self.redis_client.get(session_id)
        if data:
            session_data = json.loads(data)
            # Update last activity
            session_data["last_activity"] = datetime.now().isoformat()
            await self.redis_client.setex(
                session_id,
                self.session_timeout,
                json.dumps(session_data)
            )
            return session_data
        return None
    
    async def update_session(self, session_id: str, updates: Dict[str, Any]) -> bool:
        """Update session data."""
        session_data = await self.get_session(session_id)
        if session_data:
            session_data.update(updates)
            session_data["last_activity"] = datetime.now().isoformat()
            await self.redis_client.setex(
                session_id,
                self.session_timeout,
                json.dumps(session_data)
            )
            return True
        return False
    
    async def delete_session(self, session_id: str) -> bool:
        """Delete a session."""
        result = await self.redis_client.delete(session_id)
        return result > 0
    
    async def cleanup_expired_sessions(self):
        """Clean up expired sessions (handled by Redis TTL)."""
        pass

class InMemorySessionManager:
    """Fallback in-memory session manager."""
    
    def __init__(self):
        self.sessions = {}
        self.session_timeout = 3600
    
    async def initialize(self):
        """Initialize in-memory storage."""
        pass
    
    async def create_session(self, user_id: str, session_data: Dict[str, Any]) -> str:
        """Create a new user session."""
        session_id = f"session:{user_id}:{datetime.now().timestamp()}"
        session_data.update({
            "user_id": user_id,
            "created_at": datetime.now(),
            "last_activity": datetime.now()
        })
        self.sessions[session_id] = session_data
        return session_id
    
    async def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve session data."""
        session_data = self.sessions.get(session_id)
        if session_data:
            # Check if expired
            if datetime.now() - session_data["last_activity"] > timedelta(seconds=self.session_timeout):
                del self.sessions[session_id]
                return None
            session_data["last_activity"] = datetime.now()
            return session_data
        return None
    
    async def update_session(self, session_id: str, updates: Dict[str, Any]) -> bool:
        """Update session data."""
        if session_id in self.sessions:
            self.sessions[session_id].update(updates)
            self.sessions[session_id]["last_activity"] = datetime.now()
            return True
        return False
    
    async def delete_session(self, session_id: str) -> bool:
        """Delete a session."""
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False