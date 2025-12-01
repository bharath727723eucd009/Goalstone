"""Base agent class for all specialized agents."""
import asyncio
from abc import ABC, abstractmethod
from typing import Dict, Any, List
import structlog

logger = structlog.get_logger(__name__)

class BaseAgent(ABC):
    """Abstract base class for all agents in the system."""
    
    def __init__(self, agent_id: str, name: str):
        self.agent_id = agent_id
        self.name = name
        self.logger = logger.bind(agent_id=agent_id, agent_name=name)
        self.metrics = {"tasks_completed": 0, "errors": 0}
    
    @abstractmethod
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process a task and return results."""
        pass
    
    @abstractmethod
    async def get_recommendations(self, user_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate recommendations based on user data."""
        pass
    
    async def run(self, user_input: Dict[str, Any]) -> Dict[str, Any]:
        """Main entry point for agent execution."""
        try:
            self.logger.info("Agent run started", input_keys=list(user_input.keys()))
            result = await self.process_task(user_input)
            self.update_metrics("tasks_completed")
            return {"status": "success", "data": result}
        except Exception as e:
            self.update_metrics("errors")
            self.logger.error("Agent run failed", error=str(e))
            return {"status": "error", "error": str(e)}
    
    async def health_check(self) -> Dict[str, Any]:
        """Return agent health status."""
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "status": "healthy",
            "metrics": self.metrics
        }
    
    def update_metrics(self, metric: str, value: int = 1):
        """Update agent metrics."""
        self.metrics[metric] = self.metrics.get(metric, 0) + value