"""Agent evaluation and performance metrics."""
import asyncio
from typing import Dict, Any, List
from datetime import datetime, timedelta
import structlog

logger = structlog.get_logger(__name__)

class AgentEvaluator:
    """Evaluates agent performance and effectiveness."""
    
    def __init__(self):
        self.evaluation_history = []
    
    async def evaluate_agent_response(self, agent_id: str, task: Dict[str, Any], 
                                    response: Dict[str, Any], user_feedback: Dict[str, Any] = None) -> Dict[str, Any]:
        """Evaluate a single agent response."""
        evaluation = {
            "agent_id": agent_id,
            "task_id": task.get("id"),
            "timestamp": datetime.now(),
            "metrics": {}
        }
        
        # Response time evaluation
        if "start_time" in task and "end_time" in response:
            response_time = response["end_time"] - task["start_time"]
            evaluation["metrics"]["response_time"] = response_time
            evaluation["metrics"]["response_time_score"] = self._score_response_time(response_time)
        
        # Quality evaluation based on response structure
        evaluation["metrics"]["completeness_score"] = self._evaluate_completeness(response)
        evaluation["metrics"]["relevance_score"] = self._evaluate_relevance(task, response)
        
        # User feedback integration
        if user_feedback:
            evaluation["metrics"]["user_satisfaction"] = user_feedback.get("rating", 0)
            evaluation["metrics"]["user_feedback"] = user_feedback.get("comments", "")
        
        # Overall score
        evaluation["metrics"]["overall_score"] = self._calculate_overall_score(evaluation["metrics"])
        
        self.evaluation_history.append(evaluation)
        logger.info("Agent response evaluated", agent_id=agent_id, score=evaluation["metrics"]["overall_score"])
        
        return evaluation
    
    async def get_agent_performance_report(self, agent_id: str, days: int = 7) -> Dict[str, Any]:
        """Generate performance report for an agent."""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        relevant_evaluations = [
            eval for eval in self.evaluation_history
            if eval["agent_id"] == agent_id and eval["timestamp"] >= cutoff_date
        ]
        
        if not relevant_evaluations:
            return {"agent_id": agent_id, "message": "No evaluations found"}
        
        # Calculate aggregate metrics
        metrics = {}
        for metric_name in ["response_time_score", "completeness_score", "relevance_score", "overall_score"]:
            values = [eval["metrics"].get(metric_name, 0) for eval in relevant_evaluations]
            metrics[f"avg_{metric_name}"] = sum(values) / len(values) if values else 0
            metrics[f"min_{metric_name}"] = min(values) if values else 0
            metrics[f"max_{metric_name}"] = max(values) if values else 0
        
        # User satisfaction
        satisfaction_scores = [
            eval["metrics"].get("user_satisfaction", 0) 
            for eval in relevant_evaluations 
            if eval["metrics"].get("user_satisfaction", 0) > 0
        ]
        metrics["avg_user_satisfaction"] = sum(satisfaction_scores) / len(satisfaction_scores) if satisfaction_scores else 0
        
        return {
            "agent_id": agent_id,
            "evaluation_period_days": days,
            "total_evaluations": len(relevant_evaluations),
            "metrics": metrics,
            "recommendations": self._generate_recommendations(metrics)
        }
    
    def _score_response_time(self, response_time: float) -> float:
        """Score response time (0-1, higher is better)."""
        if response_time < 1.0:
            return 1.0
        elif response_time < 5.0:
            return 0.8
        elif response_time < 10.0:
            return 0.6
        else:
            return 0.3
    
    def _evaluate_completeness(self, response: Dict[str, Any]) -> float:
        """Evaluate response completeness (0-1)."""
        required_fields = ["status", "data"]
        present_fields = sum(1 for field in required_fields if field in response)
        return present_fields / len(required_fields)
    
    def _evaluate_relevance(self, task: Dict[str, Any], response: Dict[str, Any]) -> float:
        """Evaluate response relevance to task (0-1)."""
        # Simple heuristic: check if response addresses task type
        task_type = task.get("type", "")
        response_data = str(response.get("data", "")).lower()
        
        if task_type.lower() in response_data:
            return 0.8
        else:
            return 0.5  # Default moderate relevance
    
    def _calculate_overall_score(self, metrics: Dict[str, Any]) -> float:
        """Calculate overall performance score."""
        weights = {
            "response_time_score": 0.2,
            "completeness_score": 0.3,
            "relevance_score": 0.3,
            "user_satisfaction": 0.2
        }
        
        weighted_sum = 0
        total_weight = 0
        
        for metric, weight in weights.items():
            if metric in metrics and metrics[metric] > 0:
                weighted_sum += metrics[metric] * weight
                total_weight += weight
        
        return weighted_sum / total_weight if total_weight > 0 else 0.5
    
    def _generate_recommendations(self, metrics: Dict[str, Any]) -> List[str]:
        """Generate improvement recommendations based on metrics."""
        recommendations = []
        
        if metrics.get("avg_response_time_score", 0) < 0.7:
            recommendations.append("Optimize response time - consider caching or async processing")
        
        if metrics.get("avg_completeness_score", 0) < 0.8:
            recommendations.append("Improve response completeness - ensure all required fields are included")
        
        if metrics.get("avg_relevance_score", 0) < 0.7:
            recommendations.append("Enhance response relevance - better task understanding needed")
        
        if metrics.get("avg_user_satisfaction", 0) < 3.5:
            recommendations.append("Focus on user experience improvements")
        
        return recommendations if recommendations else ["Performance is satisfactory"]