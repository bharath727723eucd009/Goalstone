"""Finance-focused agent for financial planning and analysis."""
from typing import Dict, Any, List
from ..base_agent import BaseAgent
from ...tools.external_apis import FinanceAPIClient

class FinanceAgent(BaseAgent):
    """Agent specialized in financial planning and investment advice."""
    
    def __init__(self):
        super().__init__("finance_agent", "Finance Agent")
        self.finance_client = FinanceAPIClient()
    
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process finance-related tasks."""
        self.logger.info("Processing finance task", task_type=task.get("type"))
        
        try:
            task_type = task.get("type")
            if task_type == "budget_analysis":
                return await self._handle_budget_analysis(task)
            elif task_type == "investment_advice":
                return await self._handle_investment_advice(task)
            else:
                raise ValueError(f"Unknown task type: {task_type}")
        except Exception as e:
            self.update_metrics("errors")
            self.logger.error("Task processing failed", error=str(e))
            raise
    
    async def get_recommendations(self, user_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate financial recommendations."""
        income = user_data.get("income", 0)
        expenses = user_data.get("expenses", 0)
        goals = user_data.get("financial_goals", [])
        
        advice = await self.finance_client.get_financial_advice(income, expenses, goals)
        self.update_metrics("tasks_completed")
        
        return [
            {
                "type": "finance",
                "title": item["title"],
                "description": item["advice"],
                "priority": item.get("importance", 0.5)
            }
            for item in advice
        ]
    
    async def _handle_budget_analysis(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze user budget and spending patterns."""
        budget_data = task.get("budget_data", {})
        analysis = await self.finance_client.analyze_budget(budget_data)
        return {"analysis": analysis}
    
    async def _handle_investment_advice(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Provide investment recommendations."""
        profile = task.get("risk_profile", "moderate")
        amount = task.get("investment_amount", 0)
        advice = await self.finance_client.get_investment_advice(profile, amount)
        return {"advice": advice}