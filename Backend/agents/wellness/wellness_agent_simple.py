"""Simplified Wellness Agent implementation."""
from typing import Dict, Any, List
from ..base_agent import BaseAgent

class WellnessAgent(BaseAgent):
    """Agent specialized in health, fitness, and wellness guidance."""
    
    def __init__(self):
        super().__init__("wellness_agent", "Wellness Agent")
    
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process wellness-related tasks."""
        self.logger.info("Processing wellness task", task_type=task.get("type"))
        
        try:
            user_data = task.get("user_data", {})
            user_goals = task.get("user_goals", [])
            
            # Safely extract user data
            age = self._safe_float(user_data.get("age", 25))
            activity_level = user_data.get("activity_level", "moderate")
            
            # Generate wellness recommendations
            recommendations = self._generate_wellness_recommendations(age, activity_level, user_goals)
            weekly_plan = self._create_weekly_plan(activity_level)
            health_tips = self._get_health_tips(age, activity_level)
            
            return {
                "recommendation": recommendations,
                "weekly_plan": weekly_plan,
                "health_tips": health_tips,
                "activity_level": activity_level
            }
            
        except Exception as e:
            self.update_metrics("errors")
            self.logger.error("Task processing failed", error=str(e))
            raise
    
    async def get_recommendations(self, user_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate wellness recommendations."""
        activity_level = user_data.get("activity_level", "moderate")
        
        return [
            {
                "type": "wellness",
                "title": "Daily Exercise",
                "description": f"Aim for 30 minutes of {activity_level} activity daily",
                "priority": 0.8
            },
            {
                "type": "wellness", 
                "title": "Hydration",
                "description": "Drink 8 glasses of water daily",
                "priority": 0.6
            }
        ]
    
    def _safe_float(self, value, default=0.0):
        """Safely convert value to float."""
        try:
            return float(value) if value else default
        except (ValueError, TypeError):
            return default
    
    def _safe_int(self, value, default=0):
        """Safely convert value to int."""
        try:
            return int(float(value)) if value else default
        except (ValueError, TypeError):
            return default
    
    def _generate_wellness_recommendations(self, age: float, activity_level: str, goals: List[str]) -> str:
        """Generate personalized wellness recommendations."""
        recommendations = []
        
        # Age-based recommendations
        if age > 40:
            recommendations.append("• Consider regular health checkups and preventive screenings")
            recommendations.append("• Focus on joint-friendly exercises like swimming or yoga")
        elif age < 25:
            recommendations.append("• Build healthy habits early with consistent exercise routine")
            recommendations.append("• Focus on strength training and cardiovascular fitness")
        else:
            recommendations.append("• Maintain balanced approach to fitness and nutrition")
            recommendations.append("• Include both cardio and strength training in routine")
        
        # Activity level recommendations
        if activity_level == "low":
            recommendations.append("• Start with 15-20 minutes of light exercise daily")
            recommendations.append("• Take stairs instead of elevators when possible")
            recommendations.append("• Try walking meetings or standing desk")
        elif activity_level == "high":
            recommendations.append("• Ensure adequate rest and recovery between workouts")
            recommendations.append("• Focus on injury prevention and proper form")
            recommendations.append("• Consider working with a trainer for advanced techniques")
        else:
            recommendations.append("• Aim for 150 minutes of moderate exercise per week")
            recommendations.append("• Include 2-3 strength training sessions weekly")
        
        # Goal-based recommendations
        for goal in goals:
            if "weight" in goal.lower():
                recommendations.append("• Create sustainable caloric deficit through diet and exercise")
                recommendations.append("• Track food intake and focus on whole foods")
            elif "muscle" in goal.lower() or "strength" in goal.lower():
                recommendations.append("• Prioritize protein intake (0.8-1g per lb body weight)")
                recommendations.append("• Progressive overload in strength training")
            elif "energy" in goal.lower():
                recommendations.append("• Ensure 7-9 hours of quality sleep nightly")
                recommendations.append("• Consider stress management techniques")
        
        return "\n".join(recommendations)
    
    def _create_weekly_plan(self, activity_level: str) -> List[Dict[str, Any]]:
        """Create a weekly fitness plan."""
        if activity_level == "low":
            return [
                {"day": "Monday", "activity": "20-minute walk", "duration": 20},
                {"day": "Wednesday", "activity": "Basic stretching", "duration": 15},
                {"day": "Friday", "activity": "Light bodyweight exercises", "duration": 15},
                {"day": "Sunday", "activity": "Gentle yoga", "duration": 20}
            ]
        elif activity_level == "high":
            return [
                {"day": "Monday", "activity": "Strength training (upper body)", "duration": 60},
                {"day": "Tuesday", "activity": "HIIT cardio", "duration": 45},
                {"day": "Wednesday", "activity": "Strength training (lower body)", "duration": 60},
                {"day": "Thursday", "activity": "Active recovery (yoga/stretching)", "duration": 30},
                {"day": "Friday", "activity": "Full body strength", "duration": 60},
                {"day": "Saturday", "activity": "Cardio (running/cycling)", "duration": 45},
                {"day": "Sunday", "activity": "Rest or light activity", "duration": 30}
            ]
        else:  # moderate
            return [
                {"day": "Monday", "activity": "Strength training", "duration": 45},
                {"day": "Tuesday", "activity": "Cardio workout", "duration": 30},
                {"day": "Wednesday", "activity": "Rest or light stretching", "duration": 15},
                {"day": "Thursday", "activity": "Strength training", "duration": 45},
                {"day": "Friday", "activity": "Cardio workout", "duration": 30},
                {"day": "Saturday", "activity": "Active recovery", "duration": 30},
                {"day": "Sunday", "activity": "Rest day", "duration": 0}
            ]
    
    def _get_health_tips(self, age: float, activity_level: str) -> List[str]:
        """Get general health tips."""
        tips = [
            "Stay hydrated throughout the day",
            "Eat a balanced diet with plenty of vegetables",
            "Get 7-9 hours of quality sleep",
            "Manage stress through relaxation techniques"
        ]
        
        if age > 35:
            tips.append("Consider regular health screenings")
            tips.append("Focus on bone health with weight-bearing exercises")
        
        if activity_level == "low":
            tips.append("Start slowly and gradually increase activity")
            tips.append("Find activities you enjoy to stay motivated")
        
        return tips