"""Database repository for CRUD operations."""
from typing import List, Optional, Dict, Any
from datetime import datetime
from bson import ObjectId
from Backend.database.connection import get_database
from Backend.database.models import UserData, Milestone, AgentOutput, UserProgress
from Backend.observability.logger import get_logger
from Backend.observability.metrics import metrics_collector

logger = get_logger(__name__)

class UserRepository:
    def __init__(self):
        self.db = get_database()
        self.collection = self.db.users

    async def create_user(self, user_data: UserData) -> str:
        """Create new user."""
        try:
            result = await self.collection.insert_one(user_data.dict(by_alias=True, exclude_unset=True))
            metrics_collector.record_database_operation("create", "users", "success")
            logger.info("User created", user_id=user_data.user_id)
            return str(result.inserted_id)
        except Exception as e:
            metrics_collector.record_database_operation("create", "users", "error")
            logger.error("User creation failed", user_id=user_data.user_id, error=str(e))
            raise

    async def get_user(self, user_id: str) -> Optional[UserData]:
        """Get user by ID."""
        user_doc = await self.collection.find_one({"user_id": user_id})
        return UserData(**user_doc) if user_doc else None

    async def update_user(self, user_id: str, updates: Dict[str, Any]) -> bool:
        """Update user data."""
        updates["updated_at"] = datetime.utcnow()
        result = await self.collection.update_one(
            {"user_id": user_id}, 
            {"$set": updates}
        )
        return result.modified_count > 0

class MilestoneRepository:
    def __init__(self):
        self.db = get_database()
        self.collection = self.db.milestones

    async def create_milestone(self, milestone: Milestone) -> str:
        """Create new milestone."""
        result = await self.collection.insert_one(milestone.dict(by_alias=True, exclude_unset=True))
        return str(result.inserted_id)

    async def get_user_milestones(self, user_id: str, status: Optional[str] = None) -> List[Milestone]:
        """Get user milestones."""
        query = {"user_id": user_id}
        if status:
            query["status"] = status
        
        cursor = self.collection.find(query).sort("created_at", -1)
        milestones = []
        async for doc in cursor:
            milestones.append(Milestone(**doc))
        return milestones

    async def update_milestone(self, milestone_id: str, updates: Dict[str, Any]) -> bool:
        """Update milestone."""
        updates["updated_at"] = datetime.utcnow()
        result = await self.collection.update_one(
            {"_id": ObjectId(milestone_id)}, 
            {"$set": updates}
        )
        return result.modified_count > 0

    async def get_milestone(self, milestone_id: str) -> Optional[Milestone]:
        """Get milestone by ID."""
        doc = await self.collection.find_one({"_id": ObjectId(milestone_id)})
        return Milestone(**doc) if doc else None

class AgentOutputRepository:
    def __init__(self):
        self.db = get_database()
        self.collection = self.db.agent_outputs

    async def save_agent_output(self, output: AgentOutput) -> str:
        """Save agent execution output."""
        try:
            result = await self.collection.insert_one(output.dict(by_alias=True, exclude_unset=True))
            metrics_collector.record_database_operation("create", "agent_outputs", "success")
            logger.info("Agent output saved", user_id=output.user_id, agent_type=output.agent_type, task_type=output.task_type)
            return str(result.inserted_id)
        except Exception as e:
            metrics_collector.record_database_operation("create", "agent_outputs", "error")
            logger.error("Agent output save failed", user_id=output.user_id, agent_type=output.agent_type, error=str(e))
            raise

    async def get_user_agent_history(self, user_id: str, agent_type: Optional[str] = None, limit: int = 50) -> List[AgentOutput]:
        """Get user's agent interaction history."""
        query = {"user_id": user_id}
        if agent_type:
            query["agent_type"] = agent_type
        
        cursor = self.collection.find(query).sort("created_at", -1).limit(limit)
        outputs = []
        async for doc in cursor:
            outputs.append(AgentOutput(**doc))
        return outputs

class ProgressRepository:
    def __init__(self):
        self.db = get_database()
        self.collection = self.db.user_progress

    async def update_user_progress(self, user_id: str, category: str) -> UserProgress:
        """Update user progress for a category."""
        milestone_repo = MilestoneRepository()
        milestones = await milestone_repo.get_user_milestones(user_id)
        
        category_milestones = [m for m in milestones if m.category == category]
        total = len(category_milestones)
        completed = len([m for m in category_milestones if m.status == "completed"])
        active = len([m for m in category_milestones if m.status == "active"])
        completion_rate = completed / total if total > 0 else 0.0

        progress_data = {
            "user_id": user_id,
            "category": category,
            "total_milestones": total,
            "completed_milestones": completed,
            "active_milestones": active,
            "completion_rate": completion_rate,
            "last_activity": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }

        await self.collection.update_one(
            {"user_id": user_id, "category": category},
            {"$set": progress_data},
            upsert=True
        )

        return UserProgress(**progress_data)

    async def get_user_progress(self, user_id: str) -> List[UserProgress]:
        """Get all user progress data."""
        cursor = self.collection.find({"user_id": user_id})
        progress_list = []
        async for doc in cursor:
            progress_list.append(UserProgress(**doc))
        return progress_list