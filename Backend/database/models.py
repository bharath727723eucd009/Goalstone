"""Pydantic models for MongoDB documents."""
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
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

class UserData(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: str
    name: Optional[str] = None
    email: Optional[str] = None
    skills: List[str] = []
    interests: List[str] = []
    experience_years: int = 0
    income: Optional[float] = None
    health_goals: List[str] = []
    learning_goals: List[str] = []
    financial_goals: List[str] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class Milestone(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: str
    title: str
    description: str
    category: str  # career, finance, wellness, learning
    target_date: Optional[datetime] = None
    status: str = "active"  # active, completed, paused, cancelled
    progress: float = 0.0  # 0.0 to 1.0
    priority: int = 1  # 1-5 scale
    agent_source: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class AgentOutput(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: str
    agent_type: str  # career, finance, wellness, learning
    task_type: str
    input_data: Dict[str, Any]
    output_data: Dict[str, Any]
    status: str  # success, error
    execution_time: float
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class UserProgress(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: str
    category: str
    total_milestones: int = 0
    completed_milestones: int = 0
    active_milestones: int = 0
    completion_rate: float = 0.0
    last_activity: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}