"""Mock implementations of external API clients."""
import asyncio
from typing import Dict, Any, List
from ..config import settings

class JobAPIClient:
    """Mock client for job search APIs."""
    
    def __init__(self):
        self.api_key = settings.job_api_key
    
    async def search_jobs(self, skills: List[str], experience: int) -> List[Dict[str, Any]]:
        """Mock job search."""
        await asyncio.sleep(0.1)  # Simulate API call
        return [
            {
                "title": f"Senior {skills[0] if skills else 'Developer'}",
                "description": f"Position requiring {experience}+ years experience",
                "match_score": 0.8,
                "company": "TechCorp"
            },
            {
                "title": f"Lead {skills[0] if skills else 'Engineer'}",
                "description": f"Leadership role for {experience}+ years",
                "match_score": 0.7,
                "company": "InnovateCo"
            }
        ]
    
    async def analyze_skills(self, skills: List[str]) -> Dict[str, Any]:
        """Mock skill analysis."""
        await asyncio.sleep(0.1)
        return {
            "in_demand": skills[:2] if len(skills) > 2 else skills,
            "emerging": ["AI", "Cloud Computing"],
            "recommendations": ["Consider learning Python", "Improve communication skills"]
        }

class FinanceAPIClient:
    """Mock client for financial APIs."""
    
    def __init__(self):
        self.api_key = settings.finance_api_key
    
    async def get_financial_advice(self, income: float, expenses: float, goals: List[str]) -> List[Dict[str, Any]]:
        """Mock financial advice."""
        await asyncio.sleep(0.1)
        savings_rate = (income - expenses) / income if income > 0 else 0
        
        return [
            {
                "title": "Emergency Fund",
                "advice": f"Build emergency fund with {savings_rate:.1%} savings rate",
                "importance": 0.9
            },
            {
                "title": "Investment Strategy",
                "advice": "Consider diversified portfolio based on risk tolerance",
                "importance": 0.7
            }
        ]
    
    async def analyze_budget(self, budget_data: Dict[str, Any]) -> Dict[str, Any]:
        """Mock budget analysis."""
        await asyncio.sleep(0.1)
        return {
            "spending_categories": {"housing": 30, "food": 15, "transport": 10},
            "recommendations": ["Reduce dining out", "Consider refinancing"],
            "savings_potential": 200
        }
    
    async def get_investment_advice(self, risk_profile: str, amount: float) -> Dict[str, Any]:
        """Mock investment advice."""
        await asyncio.sleep(0.1)
        return {
            "recommended_allocation": {"stocks": 60, "bonds": 30, "cash": 10},
            "expected_return": 0.07,
            "risk_level": risk_profile
        }

class WellnessAPIClient:
    """Mock client for wellness APIs."""
    
    def __init__(self):
        self.api_key = settings.wellness_api_key
    
    async def get_wellness_tips(self, goals: List[str], activity_level: str) -> List[Dict[str, Any]]:
        """Mock wellness tips."""
        await asyncio.sleep(0.1)
        return [
            {
                "title": "Daily Exercise",
                "content": f"Aim for 30 minutes of {activity_level} activity daily",
                "urgency": 0.8
            },
            {
                "title": "Hydration",
                "content": "Drink 8 glasses of water daily",
                "urgency": 0.6
            }
        ]
    
    async def create_fitness_plan(self, goals: List[str], preferences: Dict[str, Any]) -> Dict[str, Any]:
        """Mock fitness plan creation."""
        await asyncio.sleep(0.1)
        return {
            "weekly_schedule": {
                "monday": "Cardio 30min",
                "wednesday": "Strength training",
                "friday": "Yoga"
            },
            "duration": "12 weeks"
        }
    
    async def get_nutrition_advice(self, restrictions: List[str], goals: List[str]) -> Dict[str, Any]:
        """Mock nutrition advice."""
        await asyncio.sleep(0.1)
        return {
            "meal_suggestions": ["Grilled chicken salad", "Quinoa bowl"],
            "macros": {"protein": 25, "carbs": 45, "fat": 30},
            "restrictions_considered": restrictions
        }
    
    async def recommend_workouts(self, fitness_level: str, workout_type: str, duration: int) -> List[Dict[str, Any]]:
        """Mock workout recommendations."""
        await asyncio.sleep(0.1)
        workouts = {
            "beginner": [
                {"name": "Basic Cardio", "duration": duration, "intensity": "low"},
                {"name": "Bodyweight Exercises", "duration": duration, "intensity": "low"}
            ],
            "intermediate": [
                {"name": "HIIT Training", "duration": duration, "intensity": "medium"},
                {"name": "Weight Training", "duration": duration, "intensity": "medium"}
            ],
            "advanced": [
                {"name": "CrossFit", "duration": duration, "intensity": "high"},
                {"name": "Olympic Lifting", "duration": duration, "intensity": "high"}
            ]
        }
        return workouts.get(fitness_level, workouts["beginner"])

class LearningAPIClient:
    """Mock client for learning/education APIs."""
    
    def __init__(self):
        self.api_key = settings.learning_api_key
    
    async def recommend_courses(self, interests: List[str], skill_level: str, goals: List[str]) -> List[Dict[str, Any]]:
        """Mock course recommendations."""
        await asyncio.sleep(0.1)
        return [
            {
                "title": f"Advanced {interests[0] if interests else 'Programming'}",
                "description": f"{skill_level.title()} level course",
                "relevance_score": 0.9,
                "duration": "8 weeks"
            },
            {
                "title": "Data Science Fundamentals",
                "description": "Learn data analysis and visualization",
                "relevance_score": 0.7,
                "duration": "12 weeks"
            }
        ]
    
    async def search_courses(self, criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Mock course search."""
        await asyncio.sleep(0.1)
        return [
            {
                "title": "Machine Learning Basics",
                "provider": "TechEdu",
                "rating": 4.5,
                "price": 99
            }
        ]
    
    async def analyze_skill_gaps(self, current_skills: List[str], target_skills: List[str]) -> Dict[str, Any]:
        """Mock skill gap analysis."""
        await asyncio.sleep(0.1)
        gaps = [skill for skill in target_skills if skill not in current_skills]
        return {
            "skill_gaps": gaps,
            "learning_path": [f"Learn {gap}" for gap in gaps[:3]],
            "estimated_time": "6 months"
        }
    
    async def get_learning_resources(self, topic: str, difficulty: str) -> List[Dict[str, Any]]:
        """Mock learning resources."""
        await asyncio.sleep(0.1)
        return [
            {
                "title": f"{topic} Fundamentals",
                "type": "course",
                "provider": "EduPlatform",
                "difficulty": difficulty,
                "duration": "4 weeks",
                "rating": 4.5
            },
            {
                "title": f"Mastering {topic}",
                "type": "book",
                "author": "Expert Author",
                "difficulty": difficulty,
                "pages": 300,
                "rating": 4.7
            }
        ]