"""Wellness-focused agent for health and lifestyle recommendations."""
from typing import Dict, Any, List
from ..base_agent import BaseAgent
from ...tools.external_apis import WellnessAPIClient
from ...database.repository import AgentOutputRepository
from ...database.models import AgentOutput
from ...observability.logger import get_logger
from ...observability.metrics import metrics_collector
import time

logger = get_logger(__name__)

class WellnessAgent(BaseAgent):
    """Agent specialized in health, fitness, and wellness guidance."""
    
    def __init__(self):
        super().__init__("wellness_agent", "Wellness Agent")
        self.wellness_client = WellnessAPIClient()
        self.output_repo = AgentOutputRepository()
    
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process wellness-related tasks."""
        start_time = time.time()
        user_id = task.get("user_id", "unknown")
        task_type = task.get("type")
        
        logger.info("Processing wellness task", task_type=task_type, user_id=user_id)
        
        try:
            if task_type == "fitness_plan":
                result = await self._handle_fitness_plan(task)
            elif task_type == "nutrition_advice":
                result = await self._handle_nutrition_advice(task)
            elif task_type == "health_assessment":
                result = await self._handle_health_assessment(task)
            elif task_type == "workout_recommendation":
                result = await self._handle_workout_recommendation(task)
            else:
                raise ValueError(f"Unknown task type: {task_type}")
            
            execution_time = time.time() - start_time
            
            # Save to database if user_id provided
            if user_id != "unknown":
                agent_output = AgentOutput(
                    user_id=user_id,
                    agent_type="wellness",
                    task_type=task_type,
                    input_data=task,
                    output_data=result,
                    status="success",
                    execution_time=execution_time
                )
                await self.output_repo.save_agent_output(agent_output)
            
            self.update_metrics("tasks_completed")
            metrics_collector.record_agent_run("wellness", task_type, "success", execution_time, user_id)
            
            return result
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.update_metrics("errors")
            metrics_collector.record_agent_run("wellness", task_type, "error", execution_time, user_id)
            logger.error("Wellness task processing failed", error=str(e), user_id=user_id)
            raise
    
    async def get_recommendations(self, user_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate wellness recommendations."""
        health_goals = user_data.get("health_goals", [])
        activity_level = user_data.get("activity_level", "moderate")
        
        tips = await self.wellness_client.get_wellness_tips(health_goals, activity_level)
        self.update_metrics("tasks_completed")
        
        return [
            {
                "type": "wellness",
                "title": tip["title"],
                "description": tip["content"],
                "priority": tip.get("urgency", 0.5)
            }
            for tip in tips
        ]
    
    async def _handle_fitness_plan(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Create personalized fitness plan."""
        goals = task.get("goals", [])
        preferences = task.get("preferences", {})
        plan = await self.wellness_client.create_fitness_plan(goals, preferences)
        return {"plan": plan}
    
    async def _handle_nutrition_advice(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Provide nutrition recommendations."""
        dietary_restrictions = task.get("dietary_restrictions", [])
        goals = task.get("nutrition_goals", [])
        advice = await self.wellness_client.get_nutrition_advice(dietary_restrictions, goals)
        return {"advice": advice}
    
    async def _handle_health_assessment(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Assess user health metrics."""
        user_data = task.get("user_data", {})
        health_metrics = {
            "bmi": self._calculate_bmi(user_data.get("weight"), user_data.get("height")),
            "activity_score": self._assess_activity_level(user_data.get("activity_level", "low")),
            "recommendations": await self._generate_health_recommendations(user_data)
        }
        return {"assessment": health_metrics}
    
    async def _handle_workout_recommendation(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Recommend specific workouts."""
        user_data = task.get("user_data", {})
        preferences = task.get("preferences", {})
        
        workouts = await self.wellness_client.recommend_workouts(
            user_data.get("fitness_level", "beginner"),
            preferences.get("workout_type", "general"),
            preferences.get("duration", 30)
        )
        return {"workouts": workouts}
    
    def _calculate_bmi(self, weight, height) -> float:
        """Calculate BMI from weight and height."""
        try:
            weight_float = float(weight) if weight else 0.0
            height_float = float(height) if height else 0.0
            if weight_float <= 0 or height_float <= 0:
                return 0.0
            return round(weight_float / ((height_float / 100) ** 2), 1)
        except (ValueError, TypeError):
            return 0.0
    
    def _assess_activity_level(self, activity_level: str) -> int:
        """Convert activity level to numeric score."""
        levels = {"low": 1, "moderate": 3, "high": 5, "very_high": 7}
        return levels.get(activity_level.lower(), 1)
    
    async def _generate_health_recommendations(self, user_data: Dict[str, Any]) -> List[str]:
        """Generate personalized health recommendations."""
        recommendations = []
        
        age = user_data.get("age", 25)
        if age > 40:
            recommendations.append("Consider regular health checkups")
        
        activity_level = user_data.get("activity_level", "low")
        if activity_level == "low":
            recommendations.append("Increase daily physical activity")
        
        return recommendations