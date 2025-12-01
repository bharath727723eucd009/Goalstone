"""Pydantic models for Learning Agent endpoints."""
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class LearningRequest(BaseModel):
    """Request model for learning agent."""
    user_data: Dict[str, Any]
    task_type: str = Field(..., description="Type of learning task")
    learning_goal: str = ""
    current_skills: List[str] = []
    target_skills: List[str] = []
    field: str = ""
    experience_level: str = "beginner"

class Course(BaseModel):
    """Course recommendation model."""
    title: str
    description: str
    provider: str
    duration: str
    difficulty: str
    rating: float
    price: Optional[float] = None

class LearningPath(BaseModel):
    """Learning path model."""
    goal: str
    total_duration: str
    phases: List[Dict[str, Any]]
    learning_style: str

class SkillGapAnalysis(BaseModel):
    """Skill gap analysis model."""
    skill_gaps: List[str]
    learning_path: List[str]
    estimated_time: str
    priority_skills: List[str] = []

class Certification(BaseModel):
    """Certification model."""
    name: str
    level: str
    duration: str
    provider: str = ""
    cost: Optional[float] = None

class LearningResponse(BaseModel):
    """Standard learning response model."""
    status: str
    data: Dict[str, Any]
    courses: Optional[List[Course]] = None
    learning_path: Optional[LearningPath] = None
    skill_analysis: Optional[SkillGapAnalysis] = None
    certifications: Optional[List[Certification]] = None