"""Long-term memory storage for user data and history."""
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING, DESCENDING
from ..config import settings

class MemoryStore:
    """MongoDB-based long-term memory storage."""
    
    def __init__(self):
        self.client = None
        self.db = None
        self.users_collection = None
        self.interactions_collection = None
        self.goals_collection = None
    
    async def initialize(self):
        """Initialize MongoDB connection."""
        self.client = AsyncIOMotorClient(settings.mongodb_url)
        self.db = self.client.ai_life_goals
        self.users_collection = self.db.users
        self.interactions_collection = self.db.interactions
        self.goals_collection = self.db.goals
        
        # Create indexes
        await self.users_collection.create_index("user_id", unique=True)
        await self.interactions_collection.create_index([("user_id", ASCENDING), ("timestamp", DESCENDING)])
        await self.goals_collection.create_index([("user_id", ASCENDING), ("created_at", DESCENDING)])
    
    async def store_user_profile(self, user_id: str, profile_data: Dict[str, Any]) -> bool:
        """Store or update user profile."""
        profile_data.update({
            "user_id": user_id,
            "updated_at": datetime.now()
        })
        
        result = await self.users_collection.replace_one(
            {"user_id": user_id},
            profile_data,
            upsert=True
        )
        return result.acknowledged
    
    async def get_user_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve user profile."""
        return await self.users_collection.find_one({"user_id": user_id})
    
    async def store_interaction(self, user_id: str, interaction_data: Dict[str, Any]) -> bool:
        """Store user interaction history."""
        interaction_data.update({
            "user_id": user_id,
            "timestamp": datetime.now()
        })
        
        result = await self.interactions_collection.insert_one(interaction_data)
        return result.acknowledged
    
    async def get_interaction_history(self, user_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get user interaction history."""
        cursor = self.interactions_collection.find(
            {"user_id": user_id}
        ).sort("timestamp", DESCENDING).limit(limit)
        
        return await cursor.to_list(length=limit)
    
    async def store_goal(self, user_id: str, goal_data: Dict[str, Any]) -> str:
        """Store a user goal."""
        goal_data.update({
            "user_id": user_id,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "status": "active"
        })
        
        result = await self.goals_collection.insert_one(goal_data)
        return str(result.inserted_id)
    
    async def update_goal(self, goal_id: str, updates: Dict[str, Any]) -> bool:
        """Update a goal."""
        from bson import ObjectId
        updates["updated_at"] = datetime.now()
        
        result = await self.goals_collection.update_one(
            {"_id": ObjectId(goal_id)},
            {"$set": updates}
        )
        return result.modified_count > 0
    
    async def get_user_goals(self, user_id: str, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get user goals."""
        query = {"user_id": user_id}
        if status:
            query["status"] = status
        
        cursor = self.goals_collection.find(query).sort("created_at", DESCENDING)
        goals = await cursor.to_list(length=None)
        
        # Convert ObjectId to string
        for goal in goals:
            goal["_id"] = str(goal["_id"])
        
        return goals
    
    async def get_user_analytics(self, user_id: str) -> Dict[str, Any]:
        """Get user analytics and insights."""
        profile = await self.get_user_profile(user_id)
        interactions = await self.get_interaction_history(user_id, limit=100)
        goals = await self.get_user_goals(user_id)
        
        return {
            "total_interactions": len(interactions),
            "active_goals": len([g for g in goals if g["status"] == "active"]),
            "completed_goals": len([g for g in goals if g["status"] == "completed"]),
            "last_activity": interactions[0]["timestamp"] if interactions else None,
            "profile_completeness": len(profile.keys()) if profile else 0
        }