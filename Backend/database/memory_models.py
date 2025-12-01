"""Memory bank models for long-term context storage."""
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
from datetime import datetime
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class MemoryEntry(BaseModel):
    """Individual memory entry."""
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: str
    session_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    agent_type: str
    summary: str
    key_insights: List[str] = []
    user_preferences: Dict[str, Any] = {}
    context_tokens: int = 0
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class CompactedMemory(BaseModel):
    """Compacted memory for context window."""
    user_id: str
    compacted_summary: str
    key_patterns: List[str]
    user_profile: Dict[str, Any]
    recent_context: List[Dict[str, Any]]
    total_sessions: int
    last_updated: datetime = Field(default_factory=datetime.utcnow)

class MemoryRequest(BaseModel):
    """Request to create memory entry."""
    session_data: Dict[str, Any]
    agent_results: Dict[str, Any]
    user_goals: List[str] = []

class MemoryResponse(BaseModel):
    """Memory operation response."""
    status: str
    memory_id: Optional[str] = None
    compacted_context: Optional[str] = None
    context_length: int = 0