"""FastAPI route handlers for individual agents."""
from typing import Dict, Any, List
from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel
from Backend.auth.middleware import get_current_user, get_current_session
from Backend.database.repository import AgentOutputRepository
from Backend.database.models import AgentOutput
import time
import asyncio
from Backend.agents.career.career_agent_pro import CareerAgent
from Backend.agents.finance.finance_agent import FinanceAgent
from Backend.agents.wellness.wellness_agent_complete import WellnessAgent
from Backend.agents.learning.learning_agent_complete import LearningAgent
from Backend.observability.logger import get_logger
from Backend.observability.metrics import metrics_collector

logger = get_logger(__name__)

# Initialize agents and repository
career_agent = CareerAgent()
finance_agent = FinanceAgent()
wellness_agent = WellnessAgent()
learning_agent = LearningAgent()
agent_output_repo = AgentOutputRepository()

router = APIRouter(prefix="/agents", tags=["agents"])

class AgentRequest(BaseModel):
    """Base request model for agent interactions."""
    user_data: Dict[str, Any]
    task_type: str
    parameters: Dict[str, Any] = {}

class AgentResponse(BaseModel):
    """Standard response model for agent interactions."""
    status: str
    data: Dict[str, Any] = {}
    error: str = None

class ParallelAgentRequest(BaseModel):
    """Request model for parallel agent execution."""
    user_goals: List[str]
    user_data: Dict[str, Any]
    task_types: Dict[str, str] = {"career": "milestone_analysis", "wellness": "milestone_analysis", "learning": "milestone_analysis"}
    parameters: Dict[str, Any] = {}

class ParallelAgentResponse(BaseModel):
    """Response model for parallel agent execution."""
    status: str
    results: Dict[str, Dict[str, Any]] = {}
    execution_time: float
    errors: Dict[str, str] = {}

@router.post("/career", response_model=AgentResponse)
async def career_agent_endpoint(request_data: AgentRequest, request: Request, user_id: str = Depends(get_current_user)):
    """
    Career Agent endpoint for job search and career guidance.
    
    Example payload:
    {
        "user_data": {
            "skills": ["Python", "Machine Learning"],
            "experience_years": 3,
            "location": "San Francisco"
        },
        "task_type": "job_search",
        "parameters": {
            "salary_range": [80000, 120000],
            "remote_ok": true
        }
    }
    """
    try:
        session_data = get_current_session(request)
        user_input = {
            "type": request_data.task_type,
            "user_data": request_data.user_data,
            "user_id": user_id,
            "session_data": session_data,
            **request_data.parameters
        }
        
        start_time = time.time()
        
        logger.info("Career agent execution started", user_id=user_id, task_type=request_data.task_type)
        
        result = await career_agent.run(user_input)
        execution_time = time.time() - start_time
        
        # Record agent metrics
        metrics_collector.record_agent_run(
            agent_type="career",
            task_type=request_data.task_type,
            status=result["status"],
            duration=execution_time,
            user_id=user_id
        )
        
        # Save agent output to MongoDB
        agent_output = AgentOutput(
            user_id=user_id,
            agent_type="career",
            task_type=request_data.task_type,
            input_data=user_input,
            output_data=result["data"] if result["status"] == "success" else {},
            status=result["status"],
            execution_time=execution_time
        )
        await agent_output_repo.save_agent_output(agent_output)
        
        logger.info("Career agent execution completed", user_id=user_id, status=result["status"], duration=execution_time)
        
        if result["status"] == "error":
            metrics_collector.record_error("agent_execution_error", "career_agent", user_id, result["error"])
            raise HTTPException(status_code=500, detail=result["error"])
        
        return AgentResponse(status=result["status"], data=result["data"])
        
    except Exception as e:
        logger.error("Career agent endpoint failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/finance", response_model=AgentResponse)
async def finance_agent_endpoint(request_data: AgentRequest, request: Request, user_id: str = Depends(get_current_user)):
    """
    Finance Agent endpoint for financial planning and analysis.
    
    Example payload:
    {
        "user_data": {
            "income": 75000,
            "expenses": 50000,
            "age": 30,
            "financial_goals": ["retirement", "house_purchase"]
        },
        "task_type": "budget_analysis",
        "parameters": {
            "time_horizon": "5_years",
            "risk_tolerance": "moderate"
        }
    }
    """
    try:
        session_data = get_current_session(request)
        user_input = {
            "type": request_data.task_type,
            "user_data": request_data.user_data,
            "user_id": user_id,
            "session_data": session_data,
            **request_data.parameters
        }
        
        start_time = time.time()
        logger.info("Finance agent execution started", user_id=user_id, task_type=request_data.task_type)
        
        result = await finance_agent.run(user_input)
        execution_time = time.time() - start_time
        
        # Save agent output to MongoDB
        agent_output = AgentOutput(
            user_id=user_id,
            agent_type="finance",
            task_type=request_data.task_type,
            input_data=user_input,
            output_data=result["data"] if result["status"] == "success" else {},
            status=result["status"],
            execution_time=execution_time
        )
        await agent_output_repo.save_agent_output(agent_output)
        
        metrics_collector.record_agent_run("finance", request_data.task_type, result["status"], execution_time, user_id)
        logger.info("Finance agent execution completed", user_id=user_id, status=result["status"], duration=execution_time)
        
        if result["status"] == "error":
            metrics_collector.record_error("agent_execution_error", "finance_agent", user_id, result["error"])
            raise HTTPException(status_code=500, detail=result["error"])
        
        return AgentResponse(status=result["status"], data=result["data"])
        
    except Exception as e:
        logger.error("Finance agent endpoint failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/wellness", response_model=AgentResponse)
async def wellness_agent_endpoint(request_data: AgentRequest, request: Request, user_id: str = Depends(get_current_user)):
    """
    Wellness Agent endpoint for health and fitness guidance.
    
    Example payload:
    {
        "user_data": {
            "age": 28,
            "weight": 70,
            "height": 175,
            "activity_level": "moderate",
            "health_goals": ["weight_loss", "muscle_gain"]
        },
        "task_type": "fitness_plan",
        "parameters": {
            "workout_days": 4,
            "equipment": ["dumbbells", "resistance_bands"]
        }
    }
    """
    try:
        session_data = get_current_session(request)
        user_input = {
            "type": request_data.task_type,
            "user_data": request_data.user_data,
            "user_id": user_id,
            "session_data": session_data,
            **request_data.parameters
        }
        
        start_time = time.time()
        logger.info("Wellness agent execution started", user_id=user_id, task_type=request_data.task_type)
        
        result = await wellness_agent.run(user_input)
        execution_time = time.time() - start_time
        
        # Save agent output to MongoDB
        agent_output = AgentOutput(
            user_id=user_id,
            agent_type="wellness",
            task_type=request_data.task_type,
            input_data=user_input,
            output_data=result["data"] if result["status"] == "success" else {},
            status=result["status"],
            execution_time=execution_time
        )
        await agent_output_repo.save_agent_output(agent_output)
        
        metrics_collector.record_agent_run("wellness", request_data.task_type, result["status"], execution_time, user_id)
        logger.info("Wellness agent execution completed", user_id=user_id, status=result["status"], duration=execution_time)
        
        if result["status"] == "error":
            metrics_collector.record_error("agent_execution_error", "wellness_agent", user_id, result["error"])
            raise HTTPException(status_code=500, detail=result["error"])
        
        return AgentResponse(status=result["status"], data=result["data"])
        
    except Exception as e:
        logger.error("Wellness agent endpoint failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/learning", response_model=AgentResponse)
async def learning_agent_endpoint(request_data: AgentRequest, request: Request, user_id: str = Depends(get_current_user)):
    """
    Learning Agent endpoint for educational recommendations and skill development.
    
    Example payload:
    {
        "user_data": {
            "current_skills": ["Python", "SQL"],
            "interests": ["Machine Learning", "Data Science"],
            "learning_style": "hands_on",
            "time_commitment": "10_hours_week"
        },
        "task_type": "course_recommendation",
        "parameters": {
            "budget": 500,
            "certification_required": true
        }
    }
    """
    try:
        session_data = get_current_session(request)
        user_input = {
            "type": request_data.task_type,
            "user_data": request_data.user_data,
            "user_id": user_id,
            "session_data": session_data,
            **request_data.parameters
        }
        
        start_time = time.time()
        logger.info("Learning agent execution started", user_id=user_id, task_type=request_data.task_type)
        
        result = await learning_agent.run(user_input)
        execution_time = time.time() - start_time
        
        # Save agent output to MongoDB
        agent_output = AgentOutput(
            user_id=user_id,
            agent_type="learning",
            task_type=request_data.task_type,
            input_data=user_input,
            output_data=result["data"] if result["status"] == "success" else {},
            status=result["status"],
            execution_time=execution_time
        )
        await agent_output_repo.save_agent_output(agent_output)
        
        metrics_collector.record_agent_run("learning", request_data.task_type, result["status"], execution_time, user_id)
        logger.info("Learning agent execution completed", user_id=user_id, status=result["status"], duration=execution_time)
        
        if result["status"] == "error":
            metrics_collector.record_error("agent_execution_error", "learning_agent", user_id, result["error"])
            raise HTTPException(status_code=500, detail=result["error"])
        
        return AgentResponse(status=result["status"], data=result["data"])
        
    except Exception as e:
        logger.error("Learning agent endpoint failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/career/health")
async def career_agent_health():
    """Get Career Agent health status."""
    return await career_agent.health_check()

@router.get("/finance/health")
async def finance_agent_health():
    """Get Finance Agent health status."""
    return await finance_agent.health_check()

@router.get("/wellness/health")
async def wellness_agent_health():
    """Get Wellness Agent health status."""
    return await wellness_agent.health_check()

@router.get("/learning/health")
async def learning_agent_health():
    """Get Learning Agent health status."""
    return await learning_agent.health_check()

@router.post("/parallel", response_model=ParallelAgentResponse)
async def parallel_agents_endpoint(request_data: ParallelAgentRequest, request: Request, user_id: str = Depends(get_current_user)):
    """
    Parallel Agents endpoint - runs Career, Wellness, and Learning agents concurrently.
    """
    try:
        session_data = get_current_session(request)
        start_time = time.time()
        
        logger.info("Parallel agents execution started", user_id=user_id, goals_count=len(request_data.user_goals))
        
        # Prepare input data for each agent
        base_input = {
            "user_data": request_data.user_data,
            "user_id": user_id,
            "session_data": session_data,
            "user_goals": request_data.user_goals,
            **request_data.parameters
        }
        
        # Create agent tasks with specific task types
        async def run_career_agent():
            try:
                career_input = {**base_input, "type": request_data.task_types.get("career", "milestone_analysis")}
                # Add search tool for job market trends
                if "search_tool" not in career_input:
                    from Backend.tools.search_tool import GoogleSearchTool
                    career_input["search_tool"] = GoogleSearchTool()
                result = await career_agent.run(career_input)
                return "career", result
            except Exception as e:
                return "career", {"status": "error", "error": str(e), "data": {}}
        
        async def run_wellness_agent():
            try:
                wellness_input = {**base_input, "type": request_data.task_types.get("wellness", "milestone_analysis")}
                result = await wellness_agent.run(wellness_input)
                return "wellness", result
            except Exception as e:
                return "wellness", {"status": "error", "error": str(e), "data": {}}
        
        async def run_learning_agent():
            try:
                learning_input = {**base_input, "type": request_data.task_types.get("learning", "milestone_analysis")}
                # Add code executor for examples
                if "code_executor" not in learning_input:
                    from Backend.tools.code_executor import CodeExecutor
                    learning_input["code_executor"] = CodeExecutor()
                result = await learning_agent.run(learning_input)
                return "learning", result
            except Exception as e:
                return "learning", {"status": "error", "error": str(e), "data": {}}
        
        # Run all agents concurrently
        agent_results = await asyncio.gather(
            run_career_agent(),
            run_wellness_agent(), 
            run_learning_agent(),
            return_exceptions=True
        )
        
        execution_time = time.time() - start_time
        
        # Process results
        results = {}
        errors = {}
        overall_status = "success"
        
        for agent_name, result in agent_results:
            if isinstance(result, Exception):
                errors[agent_name] = str(result)
                overall_status = "partial_success"
                continue
                
            results[agent_name] = result.get("data", {})
            
            if result.get("status") == "error":
                errors[agent_name] = result.get("error", "Unknown error")
                overall_status = "partial_success"
            
            # Save individual agent outputs to MongoDB
            try:
                agent_output = AgentOutput(
                    user_id=user_id,
                    agent_type=agent_name,
                    task_type=request_data.task_types.get(agent_name, "milestone_analysis"),
                    input_data=base_input,
                    output_data=result.get("data", {}),
                    status=result.get("status", "error"),
                    execution_time=execution_time / 3
                )
                await agent_output_repo.save_agent_output(agent_output)
                
                metrics_collector.record_agent_run(
                    agent_type=agent_name,
                    task_type=request_data.task_types.get(agent_name, "milestone_analysis"),
                    status=result.get("status", "error"),
                    duration=execution_time / 3,
                    user_id=user_id
                )
            except Exception as e:
                logger.error(f"Failed to save {agent_name} agent output", error=str(e))
        
        if len(errors) == 3:
            overall_status = "error"
        
        logger.info("Parallel agents execution completed", 
                   user_id=user_id, 
                   status=overall_status, 
                   duration=execution_time,
                   successful_agents=len(results),
                   failed_agents=len(errors))
        
        return ParallelAgentResponse(
            status=overall_status,
            results=results,
            execution_time=execution_time,
            errors=errors
        )
        
    except Exception as e:
        logger.error("Parallel agents endpoint failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))