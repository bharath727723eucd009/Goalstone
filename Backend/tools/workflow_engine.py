"""Workflow engine for orchestrating complex multi-agent workflows."""
import asyncio
from typing import Dict, Any, List, Optional
from enum import Enum
from datetime import datetime
import structlog

logger = structlog.get_logger(__name__)

class WorkflowStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"

class WorkflowTask:
    """Represents a single task in a workflow."""
    
    def __init__(self, task_id: str, agent_type: str, task_data: Dict[str, Any], 
                 dependencies: List[str] = None):
        self.task_id = task_id
        self.agent_type = agent_type
        self.task_data = task_data
        self.dependencies = dependencies or []
        self.status = TaskStatus.PENDING
        self.result = None
        self.error = None
        self.start_time = None
        self.end_time = None

class Workflow:
    """Represents a workflow with multiple tasks."""
    
    def __init__(self, workflow_id: str, name: str, tasks: List[WorkflowTask]):
        self.workflow_id = workflow_id
        self.name = name
        self.tasks = {task.task_id: task for task in tasks}
        self.status = WorkflowStatus.PENDING
        self.start_time = None
        self.end_time = None
        self.results = {}

class WorkflowEngine:
    """Orchestrates complex workflows across multiple agents."""
    
    def __init__(self, coordinator_agent):
        self.coordinator = coordinator_agent
        self.active_workflows = {}
        self.workflow_history = []
    
    async def execute_workflow(self, workflow: Workflow) -> Dict[str, Any]:
        """Execute a workflow with dependency management."""
        workflow.status = WorkflowStatus.RUNNING
        workflow.start_time = datetime.now()
        self.active_workflows[workflow.workflow_id] = workflow
        
        logger.info("Starting workflow execution", workflow_id=workflow.workflow_id)
        
        try:
            # Execute tasks based on dependencies
            completed_tasks = set()
            
            while len(completed_tasks) < len(workflow.tasks):
                # Find tasks ready to execute
                ready_tasks = []
                for task_id, task in workflow.tasks.items():
                    if (task.status == TaskStatus.PENDING and 
                        all(dep in completed_tasks for dep in task.dependencies)):
                        ready_tasks.append(task)
                
                if not ready_tasks:
                    # Check for circular dependencies or failed dependencies
                    failed_tasks = [t for t in workflow.tasks.values() if t.status == TaskStatus.FAILED]
                    if failed_tasks:
                        workflow.status = WorkflowStatus.FAILED
                        break
                    else:
                        logger.error("Circular dependency detected", workflow_id=workflow.workflow_id)
                        workflow.status = WorkflowStatus.FAILED
                        break
                
                # Execute ready tasks in parallel
                task_coroutines = []
                for task in ready_tasks:
                    task_coroutines.append(self._execute_task(task))
                
                results = await asyncio.gather(*task_coroutines, return_exceptions=True)
                
                # Process results
                for i, result in enumerate(results):
                    task = ready_tasks[i]
                    if isinstance(result, Exception):
                        task.status = TaskStatus.FAILED
                        task.error = str(result)
                        logger.error("Task failed", task_id=task.task_id, error=str(result))
                    else:
                        task.status = TaskStatus.COMPLETED
                        task.result = result
                        workflow.results[task.task_id] = result
                        completed_tasks.add(task.task_id)
                        logger.info("Task completed", task_id=task.task_id)
            
            # Determine final workflow status
            if workflow.status == WorkflowStatus.RUNNING:
                failed_tasks = [t for t in workflow.tasks.values() if t.status == TaskStatus.FAILED]
                if failed_tasks:
                    workflow.status = WorkflowStatus.FAILED
                else:
                    workflow.status = WorkflowStatus.COMPLETED
            
            workflow.end_time = datetime.now()
            
            # Move to history
            self.workflow_history.append(workflow)
            del self.active_workflows[workflow.workflow_id]
            
            logger.info("Workflow execution completed", 
                       workflow_id=workflow.workflow_id, 
                       status=workflow.status.value)
            
            return {
                "workflow_id": workflow.workflow_id,
                "status": workflow.status.value,
                "results": workflow.results,
                "execution_time": (workflow.end_time - workflow.start_time).total_seconds()
            }
            
        except Exception as e:
            workflow.status = WorkflowStatus.FAILED
            workflow.end_time = datetime.now()
            logger.error("Workflow execution failed", workflow_id=workflow.workflow_id, error=str(e))
            raise
    
    async def _execute_task(self, task: WorkflowTask) -> Dict[str, Any]:
        """Execute a single task."""
        task.status = TaskStatus.RUNNING
        task.start_time = datetime.now()
        
        try:
            # Route task to appropriate agent
            if task.agent_type in self.coordinator.agents:
                agent = self.coordinator.agents[task.agent_type]
                result = await agent.process_task(task.task_data)
            else:
                # Use coordinator for unknown agent types
                task_with_agent = task.task_data.copy()
                task_with_agent["agent_type"] = task.agent_type
                result = await self.coordinator.process_task(task_with_agent)
            
            task.end_time = datetime.now()
            return result
            
        except Exception as e:
            task.end_time = datetime.now()
            task.status = TaskStatus.FAILED
            task.error = str(e)
            raise
    
    def create_goal_achievement_workflow(self, goal_data: Dict[str, Any], 
                                       user_data: Dict[str, Any]) -> Workflow:
        """Create a workflow for achieving a specific goal."""
        workflow_id = f"goal_{goal_data.get('id', 'unknown')}_{datetime.now().timestamp()}"
        
        tasks = []
        
        # Analysis phase
        tasks.append(WorkflowTask(
            "analyze_goal",
            "coordinator",
            {
                "type": "goal_analysis",
                "goal_data": goal_data,
                "user_data": user_data
            }
        ))
        
        # Domain-specific planning
        category = goal_data.get("category", "general")
        if category in ["career", "finance", "wellness", "learning"]:
            tasks.append(WorkflowTask(
                f"plan_{category}",
                category,
                {
                    "type": "goal_planning",
                    "goal_data": goal_data,
                    "user_data": user_data
                },
                dependencies=["analyze_goal"]
            ))
        
        # Resource gathering
        tasks.append(WorkflowTask(
            "gather_resources",
            "coordinator",
            {
                "type": "resource_gathering",
                "goal_data": goal_data,
                "user_data": user_data
            },
            dependencies=["analyze_goal"]
        ))
        
        # Action plan creation
        tasks.append(WorkflowTask(
            "create_action_plan",
            "coordinator",
            {
                "type": "action_plan_creation",
                "goal_data": goal_data,
                "user_data": user_data
            },
            dependencies=[f"plan_{category}" if category in ["career", "finance", "wellness", "learning"] else "analyze_goal", "gather_resources"]
        ))
        
        return Workflow(workflow_id, f"Goal Achievement: {goal_data.get('title', 'Unknown')}", tasks)
    
    def get_workflow_status(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Get the status of a workflow."""
        if workflow_id in self.active_workflows:
            workflow = self.active_workflows[workflow_id]
        else:
            workflow = next((w for w in self.workflow_history if w.workflow_id == workflow_id), None)
        
        if not workflow:
            return None
        
        return {
            "workflow_id": workflow.workflow_id,
            "name": workflow.name,
            "status": workflow.status.value,
            "start_time": workflow.start_time.isoformat() if workflow.start_time else None,
            "end_time": workflow.end_time.isoformat() if workflow.end_time else None,
            "tasks": {
                task_id: {
                    "status": task.status.value,
                    "agent_type": task.agent_type,
                    "error": task.error
                }
                for task_id, task in workflow.tasks.items()
            }
        }