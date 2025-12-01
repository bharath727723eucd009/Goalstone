"""Professional Wellness Agent with advanced health analytics and personalized coaching."""
import asyncio
import json
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from agents.base_agent import BaseAgent
try:
    from observability.logger import get_logger
    from observability.metrics import metrics_collector
    logger = get_logger(__name__)
except:
    import structlog
    logger = structlog.get_logger(__name__)
    class MockMetrics:
        def record_agent_run(self, *args, **kwargs): pass
    metrics_collector = MockMetrics()

class WellnessAgent(BaseAgent):
    """Enterprise-grade Wellness Agent with AI-powered health optimization and personalized coaching."""
    
    def __init__(self):
        super().__init__("wellness_agent", "AI Wellness Intelligence Agent")
        self.health_metrics_db = {
            "bmi_categories": {
                "underweight": {"min": 0, "max": 18.5, "risk": "moderate"},
                "normal": {"min": 18.5, "max": 24.9, "risk": "low"},
                "overweight": {"min": 25, "max": 29.9, "risk": "moderate"},
                "obese": {"min": 30, "max": 50, "risk": "high"}
            },
            "activity_coefficients": {
                "sedentary": 1.2, "lightly_active": 1.375, "moderately_active": 1.55,
                "very_active": 1.725, "extremely_active": 1.9
            },
            "nutrition_targets": {
                "protein": {"min": 0.8, "max": 2.2, "unit": "g/kg"},
                "carbs": {"min": 45, "max": 65, "unit": "% calories"},
                "fat": {"min": 20, "max": 35, "unit": "% calories"},
                "fiber": {"min": 25, "max": 35, "unit": "g/day"}
            }
        }
        
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process advanced wellness analysis with AI-powered health optimization."""
        logger.info("Processing advanced wellness analysis", task_type=task.get("type"))
        
        try:
            user_data = task.get("user_data", {})
            user_goals = task.get("user_goals", [])
            
            # Comprehensive health assessment
            health_assessment = await self._comprehensive_health_analysis(user_data)
            
            # AI-powered fitness planning
            fitness_plan = await self._generate_ai_fitness_plan(user_data, user_goals, health_assessment)
            
            # Personalized nutrition optimization
            nutrition_plan = await self._create_nutrition_optimization(user_data, health_assessment)
            
            # Stress and mental wellness analysis
            mental_wellness = await self._analyze_mental_wellness(user_data, user_goals)
            
            # Sleep optimization recommendations
            sleep_optimization = await self._optimize_sleep_patterns(user_data)
            
            # Long-term wellness trajectory
            wellness_trajectory = await self._predict_wellness_trajectory(health_assessment, fitness_plan)
            
            # Personalized coaching recommendations
            coaching_plan = await self._generate_coaching_recommendations(user_data, health_assessment, user_goals)
            
            return {
                "health_assessment": health_assessment,
                "fitness_plan": fitness_plan,
                "nutrition_plan": nutrition_plan,
                "mental_wellness": mental_wellness,
                "sleep_optimization": sleep_optimization,
                "wellness_trajectory": wellness_trajectory,
                "coaching_plan": coaching_plan,
                "recommendation": coaching_plan["ai_summary"],
                "weekly_plan": fitness_plan["weekly_schedule"],
                "health_score": health_assessment["overall_score"],
                "priority_actions": coaching_plan["priority_actions"]
            }
            
        except Exception as e:
            self.update_metrics("errors")
            logger.error("Advanced wellness analysis failed", error=str(e))
            raise
    
    async def get_recommendations(self, user_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate AI-powered wellness recommendations."""
        activity_level = user_data.get("activity_level", "moderate")
        age = self._safe_float(user_data.get("age", 25))
        
        recommendations = []
        
        # Age-specific recommendations
        if age > 40:
            recommendations.append({
                "type": "wellness",
                "title": "Preventive Health Screening",
                "description": "Comprehensive health checkup with biomarker analysis",
                "priority": 0.9
            })
        
        # Activity-based recommendations
        if activity_level == "low":
            recommendations.append({
                "type": "wellness",
                "title": "Progressive Fitness Program",
                "description": "Structured 12-week program to build sustainable fitness habits",
                "priority": 0.8
            })
        
        return recommendations
    
    async def _comprehensive_health_analysis(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Comprehensive health assessment with biomarker analysis."""
        age = self._safe_float(user_data.get("age", 25))
        weight = self._safe_float(user_data.get("weight", 70))
        height = self._safe_float(user_data.get("height", 170))
        activity_level = user_data.get("activity_level", "moderate")
        
        # Advanced BMI and body composition analysis
        bmi = self._calculate_advanced_bmi(weight, height)
        body_composition = self._analyze_body_composition(weight, height, age, user_data.get("gender", ""))
        
        # Metabolic health assessment
        metabolic_health = await self._assess_metabolic_health(user_data, bmi)
        
        # Cardiovascular risk assessment
        cardio_risk = await self._assess_cardiovascular_risk(age, bmi, activity_level, user_data)
        
        # Fitness level assessment
        fitness_assessment = await self._assess_fitness_level(user_data, age)
        
        # Calculate overall health score
        health_scores = {
            "bmi_score": self._score_bmi(bmi["value"]),
            "activity_score": self._score_activity_level(activity_level),
            "metabolic_score": metabolic_health["score"],
            "cardio_score": cardio_risk["score"],
            "fitness_score": fitness_assessment["score"]
        }
        
        overall_score = sum(health_scores.values()) / len(health_scores)
        
        return {
            "bmi_analysis": bmi,
            "body_composition": body_composition,
            "metabolic_health": metabolic_health,
            "cardiovascular_risk": cardio_risk,
            "fitness_assessment": fitness_assessment,
            "health_scores": health_scores,
            "overall_score": overall_score,
            "health_grade": self._grade_health_score(overall_score),
            "risk_factors": self._identify_health_risks(health_scores, user_data),
            "improvement_potential": self._calculate_improvement_potential(health_scores)
        }
    
    async def _generate_ai_fitness_plan(self, user_data: Dict[str, Any], goals: List[str], assessment: Dict[str, Any]) -> Dict[str, Any]:
        """Generate AI-optimized fitness plan based on comprehensive analysis."""
        activity_level = user_data.get("activity_level", "moderate")
        age = self._safe_float(user_data.get("age", 25))
        fitness_score = assessment.get("fitness_assessment", {}).get("score", 50)
        
        # Analyze fitness goals from user input
        goal_analysis = self._analyze_fitness_goals(goals)
        
        # Generate periodized training plan
        training_phases = await self._create_periodized_plan(fitness_score, goal_analysis, age)
        
        # Create weekly schedule with progressive overload
        weekly_schedule = await self._generate_weekly_schedule(activity_level, goal_analysis, training_phases)
        
        # Exercise prescription with scientific backing
        exercise_prescription = await self._prescribe_exercises(user_data, goal_analysis, assessment)
        
        # Recovery and regeneration protocols
        recovery_protocols = await self._design_recovery_protocols(activity_level, age, training_phases)
        
        return {
            "goal_analysis": goal_analysis,
            "training_phases": training_phases,
            "weekly_schedule": weekly_schedule,
            "exercise_prescription": exercise_prescription,
            "recovery_protocols": recovery_protocols,
            "progression_tracking": self._setup_progression_tracking(goal_analysis),
            "adaptation_timeline": self._calculate_adaptation_timeline(fitness_score, goal_analysis),
            "performance_predictions": self._predict_performance_improvements(fitness_score, training_phases)
        }
    
    async def _create_nutrition_optimization(self, user_data: Dict[str, Any], assessment: Dict[str, Any]) -> Dict[str, Any]:
        """Create personalized nutrition optimization plan."""
        age = self._safe_float(user_data.get("age", 25))
        weight = self._safe_float(user_data.get("weight", 70))
        height = self._safe_float(user_data.get("height", 170))
        activity_level = user_data.get("activity_level", "moderate")
        
        # Calculate metabolic requirements
        bmr = self._calculate_bmr(weight, height, age, user_data.get("gender", ""))
        tdee = self._calculate_tdee(bmr, activity_level)
        
        # Macronutrient optimization
        macro_targets = await self._optimize_macronutrients(tdee, user_data, assessment)
        
        # Micronutrient analysis
        micronutrient_plan = await self._analyze_micronutrient_needs(age, user_data, assessment)
        
        # Meal timing optimization
        meal_timing = await self._optimize_meal_timing(activity_level, user_data)
        
        # Hydration strategy
        hydration_plan = await self._create_hydration_strategy(weight, activity_level)
        
        # Supplement recommendations
        supplement_analysis = await self._analyze_supplement_needs(assessment, macro_targets)
        
        return {
            "metabolic_profile": {"bmr": bmr, "tdee": tdee},
            "macro_targets": macro_targets,
            "micronutrient_plan": micronutrient_plan,
            "meal_timing": meal_timing,
            "hydration_plan": hydration_plan,
            "supplement_analysis": supplement_analysis,
            "nutrition_score": self._calculate_nutrition_score(macro_targets, micronutrient_plan),
            "meal_suggestions": self._generate_meal_suggestions(macro_targets, user_data)
        }
    
    async def _analyze_mental_wellness(self, user_data: Dict[str, Any], goals: List[str]) -> Dict[str, Any]:
        """Analyze mental wellness and stress management needs."""
        age = self._safe_float(user_data.get("age", 25))
        activity_level = user_data.get("activity_level", "moderate")
        
        # Stress level assessment
        stress_indicators = self._assess_stress_indicators(user_data, goals)
        
        # Work-life balance analysis
        work_life_balance = self._analyze_work_life_balance(user_data, goals)
        
        # Mental resilience assessment
        resilience_score = self._assess_mental_resilience(user_data, stress_indicators)
        
        # Mindfulness and meditation recommendations
        mindfulness_plan = await self._create_mindfulness_plan(stress_indicators, user_data)
        
        # Social wellness assessment
        social_wellness = self._assess_social_wellness(user_data)
        
        return {
            "stress_assessment": stress_indicators,
            "work_life_balance": work_life_balance,
            "resilience_score": resilience_score,
            "mindfulness_plan": mindfulness_plan,
            "social_wellness": social_wellness,
            "mental_health_score": (resilience_score + work_life_balance["score"] + social_wellness["score"]) / 3,
            "intervention_recommendations": self._recommend_mental_health_interventions(stress_indicators, resilience_score)
        }
    
    async def _optimize_sleep_patterns(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize sleep patterns for recovery and performance."""
        age = self._safe_float(user_data.get("age", 25))
        activity_level = user_data.get("activity_level", "moderate")
        
        # Sleep needs assessment
        sleep_requirements = self._calculate_sleep_requirements(age, activity_level)
        
        # Circadian rhythm optimization
        circadian_plan = await self._optimize_circadian_rhythm(user_data)
        
        # Sleep environment optimization
        environment_recommendations = self._optimize_sleep_environment()
        
        # Sleep hygiene protocols
        sleep_hygiene = self._create_sleep_hygiene_protocols(user_data)
        
        return {
            "sleep_requirements": sleep_requirements,
            "circadian_optimization": circadian_plan,
            "environment_recommendations": environment_recommendations,
            "sleep_hygiene": sleep_hygiene,
            "sleep_score": self._calculate_sleep_score(sleep_requirements, user_data),
            "recovery_optimization": self._optimize_recovery_through_sleep(activity_level)
        }
    
    async def _predict_wellness_trajectory(self, assessment: Dict[str, Any], fitness_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Predict wellness trajectory and long-term outcomes."""
        current_score = assessment.get("overall_score", 50)
        training_intensity = fitness_plan.get("goal_analysis", {}).get("intensity", "moderate")
        
        # Project improvements over time
        projections = []
        base_score = current_score
        
        for month in range(1, 13):
            # Calculate monthly improvement based on training and lifestyle factors
            improvement_rate = self._calculate_improvement_rate(training_intensity, month)
            projected_score = min(100, base_score + (improvement_rate * month))
            
            projections.append({
                "month": month,
                "wellness_score": projected_score,
                "improvement": projected_score - current_score,
                "milestones": self._identify_wellness_milestones(projected_score, month)
            })
        
        # Long-term health predictions
        long_term_benefits = self._predict_long_term_benefits(projections[-1]["wellness_score"])
        
        return {
            "current_baseline": current_score,
            "monthly_projections": projections,
            "12_month_target": projections[-1]["wellness_score"],
            "total_improvement": projections[-1]["improvement"],
            "long_term_benefits": long_term_benefits,
            "risk_reduction": self._calculate_risk_reduction(current_score, projections[-1]["wellness_score"])
        }
    
    async def _generate_coaching_recommendations(self, user_data: Dict[str, Any], assessment: Dict[str, Any], goals: List[str]) -> Dict[str, Any]:
        """Generate personalized coaching recommendations with AI insights."""
        overall_score = assessment.get("overall_score", 50)
        risk_factors = assessment.get("risk_factors", [])
        
        # Prioritize interventions based on impact and feasibility
        priority_actions = self._prioritize_interventions(assessment, user_data)
        
        # Generate personalized coaching messages
        coaching_messages = self._generate_coaching_messages(assessment, goals, user_data)
        
        # Create habit formation strategy
        habit_strategy = await self._create_habit_formation_strategy(priority_actions, user_data)
        
        # Motivation and accountability systems
        accountability_system = self._design_accountability_system(user_data, goals)
        
        # Progress tracking and feedback loops
        tracking_system = self._setup_progress_tracking(assessment, priority_actions)
        
        # AI-generated summary
        ai_summary = self._generate_wellness_ai_summary(assessment, priority_actions, user_data)
        
        return {
            "priority_actions": priority_actions,
            "coaching_messages": coaching_messages,
            "habit_strategy": habit_strategy,
            "accountability_system": accountability_system,
            "tracking_system": tracking_system,
            "ai_summary": ai_summary,
            "success_probability": self._calculate_success_probability(assessment, priority_actions),
            "personalization_score": self._calculate_personalization_score(user_data, assessment)
        }
    
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
    
    def _calculate_advanced_bmi(self, weight: float, height: float) -> Dict[str, Any]:
        """Calculate BMI with advanced analysis."""
        if weight <= 0 or height <= 0:
            return {"value": 0, "category": "unknown", "risk_level": "unknown"}
        
        bmi_value = round(weight / ((height / 100) ** 2), 1)
        
        # Determine category and risk
        for category, data in self.health_metrics_db["bmi_categories"].items():
            if data["min"] <= bmi_value < data["max"]:
                return {
                    "value": bmi_value,
                    "category": category,
                    "risk_level": data["risk"],
                    "healthy_range": "18.5-24.9",
                    "target_weight": self._calculate_target_weight(height)
                }
        
        return {"value": bmi_value, "category": "obese", "risk_level": "high"}
    
    def _analyze_body_composition(self, weight: float, height: float, age: float, gender: str) -> Dict[str, Any]:
        """Analyze body composition estimates."""
        bmi = weight / ((height / 100) ** 2) if height > 0 else 0
        
        # Estimate body fat percentage (simplified formula)
        if gender.lower() == "female":
            body_fat = (1.20 * bmi) + (0.23 * age) - 5.4
        else:
            body_fat = (1.20 * bmi) + (0.23 * age) - 16.2
        
        body_fat = max(5, min(50, body_fat))  # Reasonable bounds
        
        # Estimate muscle mass
        lean_mass = weight * (1 - body_fat / 100)
        
        return {
            "estimated_body_fat": round(body_fat, 1),
            "estimated_lean_mass": round(lean_mass, 1),
            "body_fat_category": self._categorize_body_fat(body_fat, gender),
            "muscle_mass_rating": self._rate_muscle_mass(lean_mass, height, gender)
        }
    
    async def _assess_metabolic_health(self, user_data: Dict[str, Any], bmi: Dict[str, Any]) -> Dict[str, Any]:
        """Assess metabolic health indicators."""
        age = self._safe_float(user_data.get("age", 25))
        activity_level = user_data.get("activity_level", "moderate")
        
        # Metabolic risk factors
        risk_factors = []
        if bmi["value"] > 25:
            risk_factors.append("Elevated BMI")
        if age > 45:
            risk_factors.append("Age-related metabolic decline")
        if activity_level in ["low", "sedentary"]:
            risk_factors.append("Low physical activity")
        
        # Calculate metabolic score
        base_score = 80
        score_adjustments = {
            "Elevated BMI": -15,
            "Age-related metabolic decline": -10,
            "Low physical activity": -20
        }
        
        metabolic_score = base_score - sum(score_adjustments.get(rf, 0) for rf in risk_factors)
        metabolic_score = max(0, min(100, metabolic_score))
        
        return {
            "score": metabolic_score,
            "risk_factors": risk_factors,
            "metabolic_age": self._estimate_metabolic_age(age, metabolic_score),
            "insulin_sensitivity": self._estimate_insulin_sensitivity(bmi["value"], activity_level),
            "recommendations": self._generate_metabolic_recommendations(risk_factors)
        }
    
    async def _assess_cardiovascular_risk(self, age: float, bmi: Dict[str, Any], activity_level: str, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess cardiovascular risk profile."""
        risk_score = 0
        risk_factors = []
        
        # Age factor
        if age > 45:
            risk_score += 10
            risk_factors.append("Age > 45")
        
        # BMI factor
        if bmi["value"] > 30:
            risk_score += 15
            risk_factors.append("Obesity")
        elif bmi["value"] > 25:
            risk_score += 8
            risk_factors.append("Overweight")
        
        # Activity factor
        if activity_level in ["low", "sedentary"]:
            risk_score += 12
            risk_factors.append("Sedentary lifestyle")
        
        # Calculate overall cardiovascular score
        cardio_score = max(0, 100 - risk_score)
        
        return {
            "score": cardio_score,
            "risk_level": "low" if cardio_score > 80 else "moderate" if cardio_score > 60 else "high",
            "risk_factors": risk_factors,
            "heart_age": self._estimate_heart_age(age, cardio_score),
            "protective_factors": self._identify_protective_factors(activity_level, user_data)
        }
    
    async def _assess_fitness_level(self, user_data: Dict[str, Any], age: float) -> Dict[str, Any]:
        """Assess current fitness level."""
        activity_level = user_data.get("activity_level", "moderate")
        
        # Base fitness score by activity level
        activity_scores = {
            "sedentary": 20, "low": 35, "moderate": 60, "high": 80, "very_high": 95
        }
        
        base_score = activity_scores.get(activity_level, 50)
        
        # Age adjustment
        if age > 50:
            age_factor = 0.9
        elif age > 35:
            age_factor = 0.95
        else:
            age_factor = 1.0
        
        fitness_score = int(base_score * age_factor)
        
        return {
            "score": fitness_score,
            "level": self._categorize_fitness_level(fitness_score),
            "strengths": self._identify_fitness_strengths(activity_level),
            "improvement_areas": self._identify_fitness_improvements(fitness_score),
            "fitness_age": self._estimate_fitness_age(age, fitness_score)
        }
    
    def _analyze_fitness_goals(self, goals: List[str]) -> Dict[str, Any]:
        """Analyze fitness goals from user input."""
        goal_text = " ".join(goals).lower()
        
        goal_categories = {
            "weight_loss": ["lose weight", "weight loss", "fat loss", "slim down"],
            "muscle_gain": ["muscle", "strength", "build", "gain", "bulk"],
            "endurance": ["endurance", "cardio", "running", "stamina"],
            "flexibility": ["flexibility", "yoga", "stretch", "mobility"],
            "general_fitness": ["fitness", "health", "active", "exercise"]
        }
        
        identified_goals = []
        for category, keywords in goal_categories.items():
            if any(keyword in goal_text for keyword in keywords):
                identified_goals.append(category)
        
        if not identified_goals:
            identified_goals = ["general_fitness"]
        
        # Determine primary goal and intensity
        primary_goal = identified_goals[0]
        intensity = "high" if len(identified_goals) > 2 else "moderate"
        
        return {
            "primary_goal": primary_goal,
            "secondary_goals": identified_goals[1:],
            "intensity": intensity,
            "goal_complexity": len(identified_goals),
            "training_focus": self._determine_training_focus(primary_goal)
        }
    
    async def _create_periodized_plan(self, fitness_score: float, goal_analysis: Dict[str, Any], age: float) -> Dict[str, Any]:
        """Create periodized training plan."""
        primary_goal = goal_analysis["primary_goal"]
        
        # Define training phases based on goals
        if primary_goal == "weight_loss":
            phases = [
                {"name": "Foundation", "weeks": 4, "focus": "habit_formation", "intensity": "low"},
                {"name": "Progression", "weeks": 6, "focus": "fat_burning", "intensity": "moderate"},
                {"name": "Intensification", "weeks": 4, "focus": "metabolic_boost", "intensity": "high"},
                {"name": "Maintenance", "weeks": 2, "focus": "sustainability", "intensity": "moderate"}
            ]
        elif primary_goal == "muscle_gain":
            phases = [
                {"name": "Adaptation", "weeks": 3, "focus": "movement_quality", "intensity": "low"},
                {"name": "Hypertrophy", "weeks": 8, "focus": "muscle_building", "intensity": "moderate"},
                {"name": "Strength", "weeks": 4, "focus": "strength_gains", "intensity": "high"},
                {"name": "Deload", "weeks": 1, "focus": "recovery", "intensity": "low"}
            ]
        else:  # general_fitness
            phases = [
                {"name": "Base Building", "weeks": 4, "focus": "conditioning", "intensity": "moderate"},
                {"name": "Development", "weeks": 6, "focus": "skill_building", "intensity": "moderate"},
                {"name": "Peak", "weeks": 3, "focus": "performance", "intensity": "high"},
                {"name": "Recovery", "weeks": 3, "focus": "active_recovery", "intensity": "low"}
            ]
        
        return {
            "phases": phases,
            "total_duration": sum(phase["weeks"] for phase in phases),
            "periodization_type": "linear" if fitness_score < 60 else "undulating",
            "progression_strategy": self._design_progression_strategy(primary_goal, fitness_score)
        }
    
    async def _generate_weekly_schedule(self, activity_level: str, goal_analysis: Dict[str, Any], training_phases: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate optimized weekly training schedule."""
        primary_goal = goal_analysis["primary_goal"]
        
        # Base schedule templates by goal
        if primary_goal == "weight_loss":
            schedule = [
                {"day": "Monday", "type": "Cardio + Strength", "duration": 45, "intensity": "moderate", "focus": "full_body"},
                {"day": "Tuesday", "type": "Active Recovery", "duration": 30, "intensity": "low", "focus": "mobility"},
                {"day": "Wednesday", "type": "HIIT Training", "duration": 30, "intensity": "high", "focus": "metabolic"},
                {"day": "Thursday", "type": "Strength Training", "duration": 40, "intensity": "moderate", "focus": "resistance"},
                {"day": "Friday", "type": "Cardio", "duration": 35, "intensity": "moderate", "focus": "endurance"},
                {"day": "Saturday", "type": "Functional Training", "duration": 45, "intensity": "moderate", "focus": "movement"},
                {"day": "Sunday", "type": "Rest", "duration": 0, "intensity": "rest", "focus": "recovery"}
            ]
        elif primary_goal == "muscle_gain":
            schedule = [
                {"day": "Monday", "type": "Upper Body Strength", "duration": 60, "intensity": "high", "focus": "chest_back"},
                {"day": "Tuesday", "type": "Lower Body Strength", "duration": 60, "intensity": "high", "focus": "legs_glutes"},
                {"day": "Wednesday", "type": "Active Recovery", "duration": 30, "intensity": "low", "focus": "mobility"},
                {"day": "Thursday", "type": "Push/Pull", "duration": 55, "intensity": "moderate", "focus": "arms_shoulders"},
                {"day": "Friday", "type": "Full Body", "duration": 50, "intensity": "moderate", "focus": "compound"},
                {"day": "Saturday", "type": "Cardio (optional)", "duration": 25, "intensity": "low", "focus": "recovery"},
                {"day": "Sunday", "type": "Rest", "duration": 0, "intensity": "rest", "focus": "recovery"}
            ]
        else:  # general_fitness
            schedule = [
                {"day": "Monday", "type": "Full Body Strength", "duration": 45, "intensity": "moderate", "focus": "strength"},
                {"day": "Tuesday", "type": "Cardio", "duration": 30, "intensity": "moderate", "focus": "endurance"},
                {"day": "Wednesday", "type": "Flexibility/Yoga", "duration": 30, "intensity": "low", "focus": "mobility"},
                {"day": "Thursday", "type": "Circuit Training", "duration": 40, "intensity": "moderate", "focus": "conditioning"},
                {"day": "Friday", "type": "Strength Training", "duration": 45, "intensity": "moderate", "focus": "resistance"},
                {"day": "Saturday", "type": "Active Recreation", "duration": 60, "intensity": "moderate", "focus": "enjoyment"},
                {"day": "Sunday", "type": "Rest", "duration": 0, "intensity": "rest", "focus": "recovery"}
            ]
        
        return schedule
    
    def _calculate_bmr(self, weight: float, height: float, age: float, gender: str) -> float:
        """Calculate Basal Metabolic Rate using Mifflin-St Jeor equation."""
        if gender.lower() == "female":
            bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161
        else:
            bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
        return max(1000, bmr)  # Minimum reasonable BMR
    
    def _calculate_tdee(self, bmr: float, activity_level: str) -> float:
        """Calculate Total Daily Energy Expenditure."""
        activity_multipliers = {
            "sedentary": 1.2, "low": 1.375, "moderate": 1.55, "high": 1.725, "very_high": 1.9
        }
        multiplier = activity_multipliers.get(activity_level, 1.55)
        return bmr * multiplier
    
    async def _optimize_macronutrients(self, tdee: float, user_data: Dict[str, Any], assessment: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize macronutrient distribution."""
        weight = self._safe_float(user_data.get("weight", 70))
        
        # Protein: 1.6-2.2g per kg body weight for active individuals
        protein_grams = weight * 1.8
        protein_calories = protein_grams * 4
        
        # Fat: 25-30% of total calories
        fat_calories = tdee * 0.275
        fat_grams = fat_calories / 9
        
        # Carbs: remaining calories
        carb_calories = tdee - protein_calories - fat_calories
        carb_grams = carb_calories / 4
        
        return {
            "calories": int(tdee),
            "protein": {"grams": round(protein_grams, 1), "calories": int(protein_calories), "percentage": round(protein_calories/tdee*100, 1)},
            "carbs": {"grams": round(carb_grams, 1), "calories": int(carb_calories), "percentage": round(carb_calories/tdee*100, 1)},
            "fat": {"grams": round(fat_grams, 1), "calories": int(fat_calories), "percentage": round(fat_calories/tdee*100, 1)},
            "fiber_target": max(25, weight * 0.4),
            "water_target": max(2000, weight * 35)  # ml per day
        }
    
    def _generate_wellness_ai_summary(self, assessment: Dict[str, Any], priority_actions: List[Dict[str, Any]], user_data: Dict[str, Any]) -> str:
        """Generate AI-powered wellness summary."""
        overall_score = assessment.get("overall_score", 50)
        age = self._safe_float(user_data.get("age", 25))
        
        summary_parts = []
        
        # Overall health assessment
        if overall_score >= 80:
            summary_parts.append("Your wellness profile shows excellent health markers with strong foundation for continued optimization.")
        elif overall_score >= 60:
            summary_parts.append("Your wellness profile indicates good health with significant opportunities for improvement.")
        else:
            summary_parts.append("Your wellness assessment reveals important areas requiring immediate attention for optimal health.")
        
        # Priority focus areas
        if priority_actions:
            top_priority = priority_actions[0]["category"]
            summary_parts.append(f"Primary focus should be on {top_priority} optimization for maximum health impact.")
        
        # Age-specific insights
        if age > 40:
            summary_parts.append("Age-specific protocols included for metabolic optimization and longevity enhancement.")
        elif age < 30:
            summary_parts.append("Foundation-building approach emphasized for long-term health trajectory optimization.")
        
        # Confidence and timeline
        summary_parts.append("With consistent implementation, expect measurable improvements within 4-6 weeks and significant transformation within 3-4 months.")
        
        return " ".join(summary_parts)
    
    def _score_bmi(self, bmi: float) -> float:
        """Score BMI on 0-100 scale."""
        if 18.5 <= bmi <= 24.9:
            return 100
        elif 25 <= bmi <= 29.9:
            return 70
        elif bmi < 18.5:
            return 60
        else:
            return max(20, 100 - (bmi - 30) * 5)
    
    def _score_activity_level(self, activity_level: str) -> float:
        """Score activity level on 0-100 scale."""
        scores = {"sedentary": 20, "low": 40, "moderate": 70, "high": 90, "very_high": 100}
        return scores.get(activity_level, 50)
    
    def _grade_health_score(self, score: float) -> str:
        """Convert health score to letter grade."""
        if score >= 90: return "A+"
        elif score >= 85: return "A"
        elif score >= 80: return "A-"
        elif score >= 75: return "B+"
        elif score >= 70: return "B"
        elif score >= 65: return "B-"
        elif score >= 60: return "C+"
        elif score >= 55: return "C"
        else: return "Needs Improvement"
    
    def _prioritize_interventions(self, assessment: Dict[str, Any], user_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Prioritize health interventions by impact and feasibility."""
        health_scores = assessment.get("health_scores", {})
        
        interventions = []
        
        # Analyze each health domain
        for domain, score in health_scores.items():
            if score < 70:  # Needs improvement
                impact = (70 - score) / 70  # Higher impact for lower scores
                feasibility = self._assess_intervention_feasibility(domain, user_data)
                
                interventions.append({
                    "category": domain.replace("_score", "").replace("_", " ").title(),
                    "current_score": score,
                    "target_score": min(100, score + 20),
                    "impact": impact,
                    "feasibility": feasibility,
                    "priority_score": impact * feasibility,
                    "timeline": self._estimate_intervention_timeline(domain, score),
                    "actions": self._get_intervention_actions(domain)
                })
        
        # Sort by priority score
        interventions.sort(key=lambda x: x["priority_score"], reverse=True)
        return interventions[:5]  # Top 5 priorities
    
    def _assess_intervention_feasibility(self, domain: str, user_data: Dict[str, Any]) -> float:
        """Assess feasibility of intervention (0-1 scale)."""
        age = self._safe_float(user_data.get("age", 25))
        
        # Base feasibility by domain
        feasibility_map = {
            "activity": 0.8, "bmi": 0.6, "metabolic": 0.7, "cardio": 0.8, "fitness": 0.9
        }
        
        base_feasibility = feasibility_map.get(domain, 0.7)
        
        # Age adjustment
        if age > 50:
            base_feasibility *= 0.9
        elif age < 30:
            base_feasibility *= 1.1
        
        return min(1.0, base_feasibility)
    
    def _estimate_intervention_timeline(self, domain: str, current_score: float) -> str:
        """Estimate timeline for intervention success."""
        improvement_needed = 70 - current_score
        
        if improvement_needed <= 10:
            return "2-4 weeks"
        elif improvement_needed <= 20:
            return "6-8 weeks"
        elif improvement_needed <= 30:
            return "3-4 months"
        else:
            return "6+ months"
    
    def _get_intervention_actions(self, domain: str) -> List[str]:
        """Get specific actions for each intervention domain."""
        action_map = {
            "activity": [
                "Increase daily step count by 2,000 steps",
                "Add 2 structured workout sessions per week",
                "Implement active breaks every 2 hours"
            ],
            "bmi": [
                "Create 300-500 calorie daily deficit",
                "Increase protein intake to 1.6g per kg body weight",
                "Implement portion control strategies"
            ],
            "metabolic": [
                "Optimize meal timing with intermittent fasting",
                "Increase fiber intake to 35g daily",
                "Add resistance training 3x per week"
            ],
            "cardio": [
                "Implement 150 minutes moderate cardio weekly",
                "Add HIIT sessions 2x per week",
                "Monitor and improve resting heart rate"
            ],
            "fitness": [
                "Follow progressive overload strength program",
                "Improve flexibility with daily stretching",
                "Enhance functional movement patterns"
            ]
        }
        return action_map.get(domain, ["Consult healthcare professional", "Implement gradual lifestyle changes"])
    
    # Additional helper methods for completeness
    def _calculate_target_weight(self, height: float) -> Dict[str, float]:
        """Calculate healthy target weight range."""
        height_m = height / 100
        min_weight = 18.5 * (height_m ** 2)
        max_weight = 24.9 * (height_m ** 2)
        return {"min": round(min_weight, 1), "max": round(max_weight, 1)}
    
    def _categorize_body_fat(self, body_fat: float, gender: str) -> str:
        """Categorize body fat percentage."""
        if gender.lower() == "female":
            if body_fat < 16: return "athletic"
            elif body_fat < 20: return "fitness"
            elif body_fat < 25: return "average"
            else: return "above_average"
        else:
            if body_fat < 10: return "athletic"
            elif body_fat < 15: return "fitness"
            elif body_fat < 20: return "average"
            else: return "above_average"
    
    def _rate_muscle_mass(self, lean_mass: float, height: float, gender: str) -> str:
        """Rate muscle mass relative to height and gender."""
        height_m = height / 100
        muscle_index = lean_mass / (height_m ** 2)
        
        if gender.lower() == "female":
            if muscle_index > 16: return "excellent"
            elif muscle_index > 14: return "good"
            else: return "needs_improvement"
        else:
            if muscle_index > 20: return "excellent"
            elif muscle_index > 18: return "good"
            else: return "needs_improvement"