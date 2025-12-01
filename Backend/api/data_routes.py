"""FastAPI routes for user data and milestone management."""
from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel
from datetime import datetime
from ..auth.middleware import get_current_user
from ..database.repository import UserRepository, MilestoneRepository, AgentOutputRepository, ProgressRepository
from ..database.models import UserData, Milestone, AgentOutput
import structlog

logger = structlog.get_logger(__name__)
router = APIRouter(prefix="/data", tags=["data"])

# Initialize repositories
user_repo = UserRepository()
milestone_repo = MilestoneRepository()
agent_output_repo = AgentOutputRepository()
progress_repo = ProgressRepository()

class UserDataCreate(BaseModel):
    name: str
    email: str
    skills: List[str] = []
    interests: List[str] = []
    experience_years: int = 0
    income: float = None
    health_goals: List[str] = []
    learning_goals: List[str] = []
    financial_goals: List[str] = []

class MilestoneCreate(BaseModel):
    title: str
    description: str
    category: str
    target_date: datetime = None
    priority: int = 1

class MilestoneUpdate(BaseModel):
    title: str = None
    description: str = None
    status: str = None
    progress: float = None
    priority: int = None

@router.post("/users/profile")
async def create_or_update_user_profile(
    profile_data: UserDataCreate,
    user_id: str = Depends(get_current_user)
):
    """Create or update user profile."""
    try:
        existing_user = await user_repo.get_user(user_id)
        
        if existing_user:
            # Update existing user
            updates = profile_data.dict(exclude_unset=True)
            success = await user_repo.update_user(user_id, updates)
            if not success:
                raise HTTPException(status_code=500, detail="Failed to update profile")
            return {"message": "Profile updated successfully"}
        else:
            # Create new user
            user_data = UserData(user_id=user_id, **profile_data.dict())
            user_doc_id = await user_repo.create_user(user_data)
            return {"message": "Profile created successfully", "id": user_doc_id}
            
    except Exception as e:
        logger.error("Profile operation failed", error=str(e), user_id=user_id)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/users/profile")
async def get_user_profile(user_id: str = Depends(get_current_user)):
    """Get user profile."""
    user = await user_repo.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User profile not found")
    return user

@router.post("/milestones")
async def create_milestone(
    milestone_data: MilestoneCreate,
    user_id: str = Depends(get_current_user)
):
    """Create new milestone."""
    try:
        milestone = Milestone(user_id=user_id, **milestone_data.dict())
        milestone_id = await milestone_repo.create_milestone(milestone)
        
        # Update progress
        await progress_repo.update_user_progress(user_id, milestone_data.category)
        
        return {"message": "Milestone created successfully", "id": milestone_id}
    except Exception as e:
        logger.error("Milestone creation failed", error=str(e), user_id=user_id)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/milestones")
async def get_user_milestones(
    status: str = None,
    user_id: str = Depends(get_current_user)
):
    """Get user milestones."""
    milestones = await milestone_repo.get_user_milestones(user_id, status)
    return milestones

@router.put("/milestones/{milestone_id}")
async def update_milestone(
    milestone_id: str,
    updates: MilestoneUpdate,
    user_id: str = Depends(get_current_user)
):
    """Update milestone."""
    try:
        # Verify milestone belongs to user
        milestone = await milestone_repo.get_milestone(milestone_id)
        if not milestone or milestone.user_id != user_id:
            raise HTTPException(status_code=404, detail="Milestone not found")
        
        update_data = updates.dict(exclude_unset=True)
        success = await milestone_repo.update_milestone(milestone_id, update_data)
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to update milestone")
        
        # Update progress if status changed
        if "status" in update_data:
            await progress_repo.update_user_progress(user_id, milestone.category)
        
        return {"message": "Milestone updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Milestone update failed", error=str(e), user_id=user_id)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/agent-outputs")
async def save_agent_output(
    agent_type: str,
    task_type: str,
    input_data: Dict[str, Any],
    output_data: Dict[str, Any],
    execution_time: float,
    status: str = "success",
    user_id: str = Depends(get_current_user)
):
    """Save agent execution output."""
    try:
        agent_output = AgentOutput(
            user_id=user_id,
            agent_type=agent_type,
            task_type=task_type,
            input_data=input_data,
            output_data=output_data,
            status=status,
            execution_time=execution_time
        )
        
        output_id = await agent_output_repo.save_agent_output(agent_output)
        return {"message": "Agent output saved", "id": output_id}
    except Exception as e:
        logger.error("Agent output save failed", error=str(e), user_id=user_id)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/agent-outputs")
async def get_agent_history(
    agent_type: str = None,
    limit: int = 50,
    user_id: str = Depends(get_current_user)
):
    """Get user's agent interaction history."""
    outputs = await agent_output_repo.get_user_agent_history(user_id, agent_type, limit)
    return outputs

@router.get("/progress")
async def get_user_progress(user_id: str = Depends(get_current_user)):
    """Get user progress across all categories."""
    progress_data = await progress_repo.get_user_progress(user_id)
    return progress_data

@router.get("/progress/{category}")
async def get_category_progress(
    category: str,
    user_id: str = Depends(get_current_user)
):
    """Get user progress for specific category."""
    progress = await progress_repo.update_user_progress(user_id, category)
    return progress