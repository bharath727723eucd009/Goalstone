"""Memory repository for long-term context management."""
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from .connection import get_database
from .memory_models import MemoryEntry, CompactedMemory
from ..observability.logger import get_logger
import json

logger = get_logger(__name__)

class MemoryRepository:
    """Repository for memory bank operations."""
    
    def __init__(self):
        self.db = None
        self.collection_name = "memory_bank"
        self.max_context_tokens = 4000  # LLM context window limit
    
    async def get_collection(self):
        """Get memory collection."""
        if not self.db:
            self.db = await get_database()
        return self.db[self.collection_name]
    
    async def save_memory(self, memory: MemoryEntry) -> str:
        """Save memory entry."""
        try:
            collection = await self.get_collection()
            memory_dict = memory.dict(by_alias=True)
            result = await collection.insert_one(memory_dict)
            logger.info("Memory saved", user_id=memory.user_id, memory_id=str(result.inserted_id))
            return str(result.inserted_id)
        except Exception as e:
            logger.error("Failed to save memory", error=str(e))
            raise
    
    async def get_user_memories(self, user_id: str, limit: int = 10) -> List[MemoryEntry]:
        """Get user's recent memories."""
        try:
            collection = await self.get_collection()
            cursor = collection.find(
                {"user_id": user_id}
            ).sort("timestamp", -1).limit(limit)
            
            memories = []
            async for doc in cursor:
                memories.append(MemoryEntry(**doc))
            
            return memories
        except Exception as e:
            logger.error("Failed to get user memories", error=str(e))
            return []
    
    async def compact_user_context(self, user_id: str) -> CompactedMemory:
        """Compact user's memory for context window."""
        try:
            memories = await self.get_user_memories(user_id, limit=20)
            
            if not memories:
                return CompactedMemory(
                    user_id=user_id,
                    compacted_summary="No previous interactions",
                    key_patterns=[],
                    user_profile={},
                    recent_context=[],
                    total_sessions=0
                )
            
            # Extract key insights and patterns
            all_insights = []
            user_preferences = {}
            agent_summaries = {"career": [], "wellness": [], "learning": []}
            
            for memory in memories:
                all_insights.extend(memory.key_insights)
                user_preferences.update(memory.user_preferences)
                if memory.agent_type in agent_summaries:
                    agent_summaries[memory.agent_type].append(memory.summary)
            
            # Create compacted summary
            compacted_summary = self._create_compacted_summary(agent_summaries, all_insights)
            
            # Extract key patterns
            key_patterns = list(set(all_insights))[:10]  # Top 10 unique insights
            
            # Recent context (last 3 sessions)
            recent_context = [
                {
                    "timestamp": memory.timestamp.isoformat(),
                    "agent_type": memory.agent_type,
                    "summary": memory.summary[:200]  # Truncate for context
                }
                for memory in memories[:3]
            ]
            
            return CompactedMemory(
                user_id=user_id,
                compacted_summary=compacted_summary,
                key_patterns=key_patterns,
                user_profile=user_preferences,
                recent_context=recent_context,
                total_sessions=len(memories)
            )
            
        except Exception as e:
            logger.error("Failed to compact user context", error=str(e))
            return CompactedMemory(
                user_id=user_id,
                compacted_summary="Error loading context",
                key_patterns=[],
                user_profile={},
                recent_context=[],
                total_sessions=0
            )
    
    def _create_compacted_summary(self, agent_summaries: Dict[str, List[str]], insights: List[str]) -> str:
        """Create compacted summary from agent data."""
        summary_parts = []
        
        # Career summary
        if agent_summaries["career"]:
            career_summary = f"Career: {agent_summaries['career'][0][:150]}..."
            summary_parts.append(career_summary)
        
        # Wellness summary
        if agent_summaries["wellness"]:
            wellness_summary = f"Wellness: {agent_summaries['wellness'][0][:150]}..."
            summary_parts.append(wellness_summary)
        
        # Learning summary
        if agent_summaries["learning"]:
            learning_summary = f"Learning: {agent_summaries['learning'][0][:150]}..."
            summary_parts.append(learning_summary)
        
        # Key insights
        if insights:
            top_insights = insights[:3]  # Top 3 insights
            insights_summary = f"Key Insights: {', '.join(top_insights)}"
            summary_parts.append(insights_summary)
        
        return " | ".join(summary_parts)
    
    async def create_memory_from_session(self, user_id: str, session_data: Dict[str, Any], 
                                       agent_results: Dict[str, Any], user_goals: List[str]) -> MemoryEntry:
        """Create memory entry from agent session."""
        try:
            # Extract key insights from agent results
            key_insights = []
            user_preferences = {}
            
            for agent_type, result in agent_results.items():
                if isinstance(result, dict) and "data" in result:
                    data = result["data"]
                    
                    # Extract insights based on agent type
                    if agent_type == "career":
                        if "current_skills" in data:
                            key_insights.append(f"Skills: {', '.join(data['current_skills'][:3])}")
                        if "target_roles" in data and data["target_roles"]:
                            key_insights.append(f"Target: {data['target_roles'][0].get('title', 'N/A')}")
                    
                    elif agent_type == "wellness":
                        if "recommendation" in data:
                            # Extract health status from recommendation
                            rec = data["recommendation"]
                            if "BMI" in rec:
                                key_insights.append("Health metrics tracked")
                    
                    elif agent_type == "learning":
                        if "recommendation" in data:
                            rec = data["recommendation"]
                            if "BEGINNER" in rec:
                                key_insights.append("Learning: Beginner level")
                            elif "INTERMEDIATE" in rec:
                                key_insights.append("Learning: Intermediate level")
            
            # Extract user preferences from session data
            if "user_data" in session_data:
                user_data = session_data["user_data"]
                user_preferences = {
                    "skills": user_data.get("skills", []),
                    "interests": user_data.get("interests", []),
                    "experience_years": user_data.get("experience_years", 0),
                    "learning_style": user_data.get("learning_style", ""),
                    "activity_level": user_data.get("activity_level", "")
                }
            
            # Create summary
            summary = f"Session with {len(agent_results)} agents. Goals: {', '.join(user_goals[:2])}"
            
            # Calculate context tokens (rough estimate)
            context_tokens = len(json.dumps(agent_results)) // 4  # Rough token estimate
            
            memory = MemoryEntry(
                user_id=user_id,
                session_id=f"session_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
                agent_type="parallel",
                summary=summary,
                key_insights=key_insights,
                user_preferences=user_preferences,
                context_tokens=context_tokens
            )
            
            return memory
            
        except Exception as e:
            logger.error("Failed to create memory from session", error=str(e))
            raise