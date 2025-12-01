"""Career-focused agent for job and professional development recommendations."""
from typing import Dict, Any, List
from ..base_agent import BaseAgent
from ...tools.external_apis import JobAPIClient

class CareerAgent(BaseAgent):
    """Agent specialized in career guidance and job market analysis."""
    
    def __init__(self):
        super().__init__("career_agent", "Career Agent")
        self.job_client = JobAPIClient()
    
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process career-related tasks."""
        self.logger.info("Processing career task", task_type=task.get("type"))
        
        try:
            task_type = task.get("type")
            if task_type == "job_search":
                return await self._handle_job_search(task)
            elif task_type == "skill_analysis":
                return await self._handle_skill_analysis(task)
            else:
                raise ValueError(f"Unknown task type: {task_type}")
        except Exception as e:
            self.update_metrics("errors")
            self.logger.error("Task processing failed", error=str(e))
            raise
    
    async def get_recommendations(self, user_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate career recommendations."""
        skills = user_data.get("skills", [])
        experience = user_data.get("experience_years", 0)
        
        jobs = await self.job_client.search_jobs(skills, experience)
        self.update_metrics("tasks_completed")
        
        return [
            {
                "type": "career",
                "title": job["title"],
                "description": job["description"],
                "priority": job.get("match_score", 0.5)
            }
            for job in jobs
        ]
    
    async def _handle_job_search(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle job search requests."""
        criteria = task.get("criteria", {})
        jobs = await self.job_client.search_jobs(
            criteria.get("skills", []),
            criteria.get("experience", 0)
        )
        return {"jobs": jobs, "count": len(jobs)}
    
    async def _handle_skill_analysis(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze user skills against market demands."""
        skills = task.get("skills", [])
        analysis = await self.job_client.analyze_skills(skills)
        return {"analysis": analysis}