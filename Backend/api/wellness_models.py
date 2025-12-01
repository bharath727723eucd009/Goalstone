"""Pydantic models for Wellness Agent endpoints."""
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class WellnessRequest(BaseModel):
    """Request model for wellness agent."""
    user_data: Dict[str, Any]
    task_type: str = Field(..., description="Type of wellness task")
    preferences: Dict[str, Any] = {}
    dietary_restrictions: List[str] = []
    nutrition_goals: List[str] = []

class FitnessAssessment(BaseModel):
    """Fitness assessment response model."""
    bmi: float
    activity_score: int
    fitness_level: str
    recommendations: List[str]

class WorkoutPlan(BaseModel):
    """Workout plan response model."""
    name: str
    duration: int
    intensity: str
    exercises: List[Dict[str, Any]] = []

class NutritionAdvice(BaseModel):
    """Nutrition advice response model."""
    meal_suggestions: List[str]
    macros: Dict[str, int]
    restrictions_considered: List[str]

class WellnessResponse(BaseModel):
    """Standard wellness response model."""
    status: str
    data: Dict[str, Any]
    assessment: Optional[FitnessAssessment] = None
    workout_plan: Optional[WorkoutPlan] = None
    nutrition_advice: Optional[NutritionAdvice] = None