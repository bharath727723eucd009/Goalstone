"""Simplified Career Agent implementation."""
from typing import Dict, Any, List
from ..base_agent import BaseAgent

class CareerAgent(BaseAgent):
    """Agent specialized in career guidance and job market analysis."""
    
    def __init__(self):
        super().__init__("career_agent", "Career Agent")
    
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process career-related tasks."""
        self.logger.info("Processing career task", task_type=task.get("type"))
        
        try:
            user_data = task.get("user_data", {})
            user_goals = task.get("user_goals", [])
            
            # Generate career recommendations based on user data
            current_skills = user_data.get("skills", [])
            if isinstance(current_skills, str):
                current_skills = [current_skills]
            
            experience_years = self._safe_int(user_data.get("experience_years", 0))
            current_role = user_data.get("current_role", "")
            
            # Generate target roles based on experience and skills
            target_roles = self._generate_target_roles(current_skills, experience_years, current_role)
            
            # Create 30/60/90 day roadmap
            roadmap = self._create_career_roadmap(current_skills, target_roles, user_goals)
            
            return {
                "current_skills": current_skills,
                "target_roles": target_roles,
                "tasks": roadmap["tasks"],
                "roadmap_30_days": roadmap["30_days"],
                "roadmap_60_days": roadmap["60_days"], 
                "roadmap_90_days": roadmap["90_days"],
                "recommendation": roadmap["summary"]
            }
            
        except Exception as e:
            self.update_metrics("errors")
            self.logger.error("Task processing failed", error=str(e))
            raise
    
    async def get_recommendations(self, user_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate career recommendations."""
        skills = user_data.get("skills", [])
        experience = self._safe_int(user_data.get("experience_years", 0))
        
        return [
            {
                "type": "career",
                "title": f"Senior {skills[0] if skills else 'Developer'} Role",
                "description": f"Position requiring {experience}+ years experience",
                "priority": 0.8
            }
        ]
    
    def _safe_int(self, value, default=0):
        """Safely convert value to int."""
        try:
            return int(float(value)) if value else default
        except (ValueError, TypeError):
            return default
    
    def _generate_target_roles(self, skills: List[str], experience: int, current_role: str) -> List[Dict[str, Any]]:
        """Generate target roles based on skills and experience."""
        roles = []
        
        if experience < 2:
            roles.append({
                "title": f"Junior {skills[0] if skills else 'Developer'}",
                "match_score": 0.9,
                "requirements": ["Basic programming", "Problem solving"]
            })
        elif experience < 5:
            roles.append({
                "title": f"Mid-level {skills[0] if skills else 'Developer'}",
                "match_score": 0.8,
                "requirements": ["Advanced programming", "Team collaboration"]
            })
        else:
            roles.append({
                "title": f"Senior {skills[0] if skills else 'Developer'}",
                "match_score": 0.9,
                "requirements": ["Leadership", "Architecture design"]
            })
            roles.append({
                "title": f"Lead {skills[0] if skills else 'Engineer'}",
                "match_score": 0.7,
                "requirements": ["Team management", "Strategic planning"]
            })
        
        return roles
    
    def _create_career_roadmap(self, skills: List[str], target_roles: List[Dict], goals: List[str]) -> Dict[str, Any]:
        """Create a 30/60/90 day career roadmap."""
        
        # 30-day tasks
        tasks_30 = [
            {"task": "Update resume with current skills", "priority": "high", "completed": False},
            {"task": "Complete online course in primary skill", "priority": "medium", "completed": False},
            {"task": "Network with 5 industry professionals", "priority": "medium", "completed": False}
        ]
        
        # 60-day tasks  
        tasks_60 = [
            {"task": "Apply to 10 relevant positions", "priority": "high", "completed": False},
            {"task": "Prepare for technical interviews", "priority": "high", "completed": False},
            {"task": "Build portfolio project", "priority": "medium", "completed": False}
        ]
        
        # 90-day tasks
        tasks_90 = [
            {"task": "Negotiate job offers", "priority": "high", "completed": False},
            {"task": "Plan transition to new role", "priority": "medium", "completed": False},
            {"task": "Set goals for first 100 days", "priority": "low", "completed": False}
        ]
        
        all_tasks = tasks_30 + tasks_60 + tasks_90
        
        summary = f"Career roadmap focusing on {skills[0] if skills else 'skill development'} with {len(target_roles)} target roles identified."
        
        return {
            "tasks": all_tasks,
            "30_days": tasks_30,
            "60_days": tasks_60,
            "90_days": tasks_90,
            "summary": summary
        }