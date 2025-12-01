"""Coordinator agent that orchestrates multiple specialized agents."""
import asyncio
from typing import Dict, Any, List
from ..base_agent import BaseAgent
from ..career.career_agent import CareerAgent
from ..finance.finance_agent import FinanceAgent
from ..wellness.wellness_agent import WellnessAgent
from ..learning.learning_agent import LearningAgent

class CoordinatorAgent(BaseAgent):
    """Main orchestrator agent that coordinates specialized agents."""
    
    def __init__(self):
        super().__init__("coordinator_agent", "Coordinator Agent")
        self.agents = {
            "career": CareerAgent(),
            "finance": FinanceAgent(),
            "wellness": WellnessAgent(),
            "learning": LearningAgent()
        }
    
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Coordinate task processing across multiple agents."""
        self.logger.info("Coordinating task", task_type=task.get("type"))
        
        try:
            task_type = task.get("type")
            if task_type == "comprehensive_plan":
                return await self._create_comprehensive_plan(task)
            elif task_type == "multi_agent_query":
                return await self._handle_multi_agent_query(task)
            else:
                # Route to specific agent
                agent_type = task.get("agent_type")
                if agent_type in self.agents:
                    return await self.agents[agent_type].process_task(task)
                else:
                    raise ValueError(f"Unknown agent type: {agent_type}")
        except Exception as e:
            self.update_metrics("errors")
            self.logger.error("Task coordination failed", error=str(e))
            raise
    
    async def get_recommendations(self, user_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get recommendations from all agents and prioritize them."""
        tasks = []
        for agent_name, agent in self.agents.items():
            tasks.append(agent.get_recommendations(user_data))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        all_recommendations = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                self.logger.error(f"Agent {list(self.agents.keys())[i]} failed", error=str(result))
                continue
            all_recommendations.extend(result)
        
        # Sort by priority
        all_recommendations.sort(key=lambda x: x.get("priority", 0), reverse=True)
        self.update_metrics("tasks_completed")
        
        return all_recommendations
    
    async def _create_comprehensive_plan(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Create a comprehensive life plan using all agents."""
        user_data = task.get("user_data", {})
        recommendations = await self.get_recommendations(user_data)
        
        plan = {
            "career": [r for r in recommendations if r["type"] == "career"][:3],
            "finance": [r for r in recommendations if r["type"] == "finance"][:3],
            "wellness": [r for r in recommendations if r["type"] == "wellness"][:3],
            "learning": [r for r in recommendations if r["type"] == "learning"][:3]
        }
        
        return {"comprehensive_plan": plan}
    
    async def _handle_multi_agent_query(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle queries that require multiple agents."""
        query = task.get("query", "")
        agent_types = task.get("agent_types", list(self.agents.keys()))
        
        tasks = []
        for agent_type in agent_types:
            if agent_type in self.agents:
                agent_task = {"type": "query", "query": query}
                tasks.append(self.agents[agent_type].process_task(agent_task))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        response = {}
        for i, result in enumerate(results):
            agent_type = agent_types[i]
            if isinstance(result, Exception):
                response[agent_type] = {"error": str(result)}
            else:
                response[agent_type] = result
        
        return {"multi_agent_response": response}
    
    async def get_agent_status(self) -> Dict[str, Any]:
        """Get status of all agents."""
        status = {}
        for agent_name, agent in self.agents.items():
            status[agent_name] = await agent.health_check()
        return status