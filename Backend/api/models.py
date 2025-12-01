"""Pydantic models for API requests and responses."""
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from datetime import datetime

class GoalCreate(BaseModel):
    title: str
    description: str
    category: str  # career, finance, wellness, learning
    target_date: Optional[datetime] = None
    priority: int = 1  # 1-5 scale

class GoalUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    progress: Optional[float] = None

class GoalResponse(BaseModel):
    id: str
    title: str
    description: str
    category: str
    status: str
    progress: float
    created_at: datetime
    updated_at: datetime

class UserProfile(BaseModel):
    user_id: str
    name: Optional[str] = None
    skills: List[str] = []
    interests: List[str] = []
    experience_years: int = 0
    income: Optional[float] = None
    health_goals: List[str] = []
    learning_goals: List[str] = []

class TaskRequest(BaseModel):
    type: str
    agent_type: Optional[str] = None
    data: Dict[str, Any] = {}

class RecommendationResponse(BaseModel):
    type: str
    title: str
    description: str
    priority: float
    agent_source: str

class PlanRequest(BaseModel):
    user_data: Dict[str, Any]
    plan_type: str = "comprehensive"  # comprehensive, focused
    time_horizon: str = "3_months"  # 1_month, 3_months, 6_months, 1_year

class SessionCreate(BaseModel):
    user_id: str
    initial_data: Dict[str, Any] = {}

class AgentStatus(BaseModel):
    agent_id: str
    name: str
    status: str
    metrics: Dict[str, Any]