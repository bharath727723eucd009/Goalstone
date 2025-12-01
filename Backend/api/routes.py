"""FastAPI routes for the multi-agent system."""
import time
from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException, Depends, Request
from ..auth.middleware import get_current_user, get_current_session
from .models import *
from ..agents.coordinator.coordinator_agent import CoordinatorAgent
from ..sessions.session_manager import SessionManager, InMemorySessionManager
from ..sessions.memory_store import MemoryStore
from ..observability.metrics import metrics_collector
import structlog

logger = structlog.get_logger(__name__)

# Initialize components
coordinator = CoordinatorAgent()
session_manager = InMemorySessionManager()  # Fallback to in-memory
memory_store = MemoryStore()

router = APIRouter()

@router.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    await session_manager.initialize()
    await memory_store.initialize()
    logger.info("API services initialized")

# Goal Management Endpoints
@router.post("/goals", response_model=GoalResponse)
async def create_goal(goal: GoalCreate, request: Request, user_id: str = Depends(get_current_user)):
    """Create a new user goal."""
    start_time = time.time()
    try:
        goal_data = goal.dict()
        goal_id = await memory_store.store_goal(user_id, goal_data)
        
        # Store interaction
        await memory_store.store_interaction(user_id, {
            "action": "goal_created",
            "goal_id": goal_id,
            "goal_data": goal_data
        })
        
        # Get stored goal for response
        goals = await memory_store.get_user_goals(user_id)
        created_goal = next((g for g in goals if g["_id"] == goal_id), None)
        
        if not created_goal:
            raise HTTPException(status_code=500, detail="Failed to retrieve created goal")
        
        metrics_collector.record_request("POST", "/goals", 200, time.time() - start_time)
        return GoalResponse(
            id=created_goal["_id"],
            title=created_goal["title"],
            description=created_goal["description"],
            category=created_goal["category"],
            status=created_goal["status"],
            progress=created_goal.get("progress", 0.0),
            created_at=created_goal["created_at"],
            updated_at=created_goal["updated_at"]
        )
    except Exception as e:
        metrics_collector.record_request("POST", "/goals", 500, time.time() - start_time)
        logger.error("Goal creation failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/goals", response_model=List[GoalResponse])
async def get_goals(request: Request, user_id: str = Depends(get_current_user), status: Optional[str] = None):
    """Get user goals."""
    start_time = time.time()
    try:
        goals = await memory_store.get_user_goals(user_id, status)
        metrics_collector.record_request("GET", "/goals", 200, time.time() - start_time)
        
        return [
            GoalResponse(
                id=goal["_id"],
                title=goal["title"],
                description=goal["description"],
                category=goal["category"],
                status=goal["status"],
                progress=goal.get("progress", 0.0),
                created_at=goal["created_at"],
                updated_at=goal["updated_at"]
            )
            for goal in goals
        ]
    except Exception as e:
        metrics_collector.record_request("GET", "/goals", 500, time.time() - start_time)
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/goals/{goal_id}")
async def update_goal(goal_id: str, updates: GoalUpdate, request: Request, user_id: str = Depends(get_current_user)):
    """Update a goal."""
    start_time = time.time()
    try:
        update_data = {k: v for k, v in updates.dict().items() if v is not None}
        success = await memory_store.update_goal(goal_id, update_data)
        
        if not success:
            raise HTTPException(status_code=404, detail="Goal not found")
        
        # Store interaction
        await memory_store.store_interaction(user_id, {
            "action": "goal_updated",
            "goal_id": goal_id,
            "updates": update_data
        })
        
        metrics_collector.record_request("PUT", f"/goals/{goal_id}", 200, time.time() - start_time)
        return {"message": "Goal updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        metrics_collector.record_request("PUT", f"/goals/{goal_id}", 500, time.time() - start_time)
        raise HTTPException(status_code=500, detail=str(e))

# Recommendation Endpoints
@router.post("/recommendations", response_model=List[RecommendationResponse])
async def get_recommendations(request: Request, user_id: str = Depends(get_current_user)):
    """Get personalized recommendations."""
    start_time = time.time()
    try:
        # Get user profile
        profile = await memory_store.get_user_profile(user_id)
        if not profile:
            raise HTTPException(status_code=404, detail="User profile not found")
        
        # Get recommendations from coordinator
        recommendations = await coordinator.get_recommendations(profile)
        
        # Store interaction
        await memory_store.store_interaction(user_id, {
            "action": "recommendations_requested",
            "recommendations_count": len(recommendations)
        })
        
        metrics_collector.record_request("POST", "/recommendations", 200, time.time() - start_time)
        
        return [
            RecommendationResponse(
                type=rec["type"],
                title=rec["title"],
                description=rec["description"],
                priority=rec["priority"],
                agent_source=rec["type"]
            )
            for rec in recommendations
        ]
    except HTTPException:
        raise
    except Exception as e:
        metrics_collector.record_request("POST", "/recommendations", 500, time.time() - start_time)
        logger.error("Recommendations failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

# Plan Generation
@router.post("/plans")
async def create_plan(plan_request: PlanRequest, request: Request, user_id: str = Depends(get_current_user)):
    """Create a comprehensive life plan."""
    start_time = time.time()
    try:
        task = {
            "type": "comprehensive_plan",
            "user_data": plan_request.user_data,
            "plan_type": plan_request.plan_type,
            "time_horizon": plan_request.time_horizon
        }
        
        plan = await coordinator.process_task(task)
        
        # Store interaction
        await memory_store.store_interaction(user_id, {
            "action": "plan_created",
            "plan_type": plan_request.plan_type,
            "time_horizon": plan_request.time_horizon
        })
        
        metrics_collector.record_request("POST", "/plans", 200, time.time() - start_time)
        return plan
    except Exception as e:
        metrics_collector.record_request("POST", "/plans", 500, time.time() - start_time)
        logger.error("Plan creation failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

# Session Management
@router.post("/sessions")
async def create_session(session_data: SessionCreate):
    """Create a new user session."""
    start_time = time.time()
    try:
        session_id = await session_manager.create_session(
            session_data.user_id,
            session_data.initial_data
        )
        metrics_collector.record_request("POST", "/sessions", 200, time.time() - start_time)
        return {"session_id": session_id}
    except Exception as e:
        metrics_collector.record_request("POST", "/sessions", 500, time.time() - start_time)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sessions/{session_id}")
async def get_session(session_id: str):
    """Get session data."""
    start_time = time.time()
    try:
        session_data = await session_manager.get_session(session_id)
        if not session_data:
            raise HTTPException(status_code=404, detail="Session not found")
        
        metrics_collector.record_request("GET", f"/sessions/{session_id}", 200, time.time() - start_time)
        return session_data
    except HTTPException:
        raise
    except Exception as e:
        metrics_collector.record_request("GET", f"/sessions/{session_id}", 500, time.time() - start_time)
        raise HTTPException(status_code=500, detail=str(e))

# User Profile Management
@router.post("/users/{user_id}/profile")
async def update_user_profile(user_id: str, profile: UserProfile):
    """Update user profile."""
    start_time = time.time()
    try:
        success = await memory_store.store_user_profile(user_id, profile.dict())
        if not success:
            raise HTTPException(status_code=500, detail="Failed to update profile")
        
        metrics_collector.record_request("POST", f"/users/{user_id}/profile", 200, time.time() - start_time)
        return {"message": "Profile updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        metrics_collector.record_request("POST", f"/users/{user_id}/profile", 500, time.time() - start_time)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/users/{user_id}/analytics")
async def get_user_analytics(user_id: str):
    """Get user analytics and insights."""
    start_time = time.time()
    try:
        analytics = await memory_store.get_user_analytics(user_id)
        metrics_collector.record_request("GET", f"/users/{user_id}/analytics", 200, time.time() - start_time)
        return analytics
    except Exception as e:
        metrics_collector.record_request("GET", f"/users/{user_id}/analytics", 500, time.time() - start_time)
        raise HTTPException(status_code=500, detail=str(e))

# System Status
@router.get("/status", response_model=Dict[str, Any])
async def get_system_status():
    """Get system and agent status."""
    start_time = time.time()
    try:
        agent_status = await coordinator.get_agent_status()
        metrics_summary = metrics_collector.get_metrics_summary()
        
        status = {
            "system": "healthy",
            "agents": agent_status,
            "metrics": metrics_summary
        }
        
        metrics_collector.record_request("GET", "/status", 200, time.time() - start_time)
        return status
    except Exception as e:
        metrics_collector.record_request("GET", "/status", 500, time.time() - start_time)
        raise HTTPException(status_code=500, detail=str(e))