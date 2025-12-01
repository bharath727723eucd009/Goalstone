"""Learning-focused agent for educational recommendations and skill development."""
from typing import Dict, Any, List
from ..base_agent import BaseAgent
from ...tools.external_apis import LearningAPIClient
from ...database.repository import AgentOutputRepository
from ...database.models import AgentOutput
from ...observability.logger import get_logger
from ...observability.metrics import metrics_collector
import time

logger = get_logger(__name__)

class LearningAgent(BaseAgent):
    """Agent specialized in educational content and skill development."""
    
    def __init__(self):
        super().__init__("learning_agent", "Learning Agent")
        self.learning_client = LearningAPIClient()
        self.output_repo = AgentOutputRepository()
    
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process learning-related tasks."""
        start_time = time.time()
        user_id = task.get("user_id", "unknown")
        task_type = task.get("type")
        
        logger.info("Processing learning task", task_type=task_type, user_id=user_id)
        
        try:
            if task_type == "course_recommendation":
                result = await self._handle_course_recommendation(task)
            elif task_type == "skill_gap_analysis":
                result = await self._handle_skill_gap_analysis(task)
            elif task_type == "learning_path":
                result = await self._handle_learning_path(task)
            elif task_type == "certification_guidance":
                result = await self._handle_certification_guidance(task)
            else:
                raise ValueError(f"Unknown task type: {task_type}")
            
            execution_time = time.time() - start_time
            
            # Save to database if user_id provided
            if user_id != "unknown":
                agent_output = AgentOutput(
                    user_id=user_id,
                    agent_type="learning",
                    task_type=task_type,
                    input_data=task,
                    output_data=result,
                    status="success",
                    execution_time=execution_time
                )
                await self.output_repo.save_agent_output(agent_output)
            
            self.update_metrics("tasks_completed")
            metrics_collector.record_agent_run("learning", task_type, "success", execution_time, user_id)
            
            return result
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.update_metrics("errors")
            metrics_collector.record_agent_run("learning", task_type, "error", execution_time, user_id)
            logger.error("Learning task processing failed", error=str(e), user_id=user_id)
            raise
    
    async def get_recommendations(self, user_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate learning recommendations."""
        interests = user_data.get("interests", [])
        skill_level = user_data.get("skill_level", "beginner")
        learning_goals = user_data.get("learning_goals", [])
        
        courses = await self.learning_client.recommend_courses(interests, skill_level, learning_goals)
        
        return [
            {
                "type": "learning",
                "title": course["title"],
                "description": course["description"],
                "priority": course.get("relevance_score", 0.5)
            }
            for course in courses
        ]
    
    async def _handle_course_recommendation(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Recommend courses based on user criteria."""
        criteria = task.get("criteria", {})
        courses = await self.learning_client.search_courses(criteria)
        return {"courses": courses}
    
    async def _handle_skill_gap_analysis(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze skill gaps and recommend learning paths."""
        current_skills = task.get("current_skills", [])
        target_skills = task.get("target_skills", [])
        analysis = await self.learning_client.analyze_skill_gaps(current_skills, target_skills)
        return {"analysis": analysis}
    
    async def _handle_learning_path(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Create personalized learning path."""
        user_data = task.get("user_data", {})
        goal = task.get("learning_goal", "")
        
        path = await self._generate_learning_path(
            user_data.get("current_skills", []),
            goal,
            user_data.get("time_commitment", "5_hours_week"),
            user_data.get("learning_style", "mixed")
        )
        return {"learning_path": path}
    
    async def _handle_certification_guidance(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Provide certification guidance."""
        field = task.get("field", "")
        experience_level = task.get("experience_level", "beginner")
        
        certifications = await self._recommend_certifications(field, experience_level)
        return {"certifications": certifications}
    
    async def _generate_learning_path(self, current_skills: List[str], goal: str, 
                                    time_commitment: str, learning_style: str) -> Dict[str, Any]:
        """Generate structured learning path."""
        # Mock implementation - replace with actual logic
        phases = [
            {
                "phase": 1,
                "title": "Foundation",
                "duration": "4 weeks",
                "topics": ["Basics", "Core Concepts"]
            },
            {
                "phase": 2,
                "title": "Intermediate",
                "duration": "6 weeks",
                "topics": ["Advanced Topics", "Practical Applications"]
            },
            {
                "phase": 3,
                "title": "Advanced",
                "duration": "4 weeks",
                "topics": ["Expert Level", "Real Projects"]
            }
        ]
        
        return {
            "goal": goal,
            "total_duration": "14 weeks",
            "phases": phases,
            "learning_style": learning_style
        }
    
    async def _recommend_certifications(self, field: str, experience_level: str) -> List[Dict[str, Any]]:
        """Recommend relevant certifications."""
        # Mock implementation
        cert_map = {
            "data_science": [
                {"name": "Google Data Analytics", "level": "beginner", "duration": "6 months"},
                {"name": "AWS Machine Learning", "level": "intermediate", "duration": "3 months"}
            ],
            "software_development": [
                {"name": "AWS Developer Associate", "level": "intermediate", "duration": "4 months"},
                {"name": "Google Cloud Professional", "level": "advanced", "duration": "6 months"}
            ]
        }
        
        return cert_map.get(field, [])