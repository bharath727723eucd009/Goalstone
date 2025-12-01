"""Test cases for session management."""
import pytest
from ..sessions.session_manager import InMemorySessionManager
from ..sessions.memory_store import MemoryStore

@pytest.mark.asyncio
async def test_in_memory_session_manager():
    """Test in-memory session manager."""
    manager = InMemorySessionManager()
    await manager.initialize()
    
    # Create session
    session_id = await manager.create_session("test_user", {"key": "value"})
    assert session_id is not None
    
    # Get session
    session_data = await manager.get_session(session_id)
    assert session_data is not None
    assert session_data["user_id"] == "test_user"
    assert session_data["key"] == "value"
    
    # Update session
    success = await manager.update_session(session_id, {"new_key": "new_value"})
    assert success is True
    
    updated_data = await manager.get_session(session_id)
    assert updated_data["new_key"] == "new_value"
    
    # Delete session
    success = await manager.delete_session(session_id)
    assert success is True
    
    deleted_data = await manager.get_session(session_id)
    assert deleted_data is None

@pytest.mark.asyncio
async def test_memory_store_user_profile():
    """Test memory store user profile operations."""
    store = MemoryStore()
    
    # Mock the MongoDB operations
    store.users_collection = MockCollection()
    
    profile_data = {
        "name": "Test User",
        "skills": ["Python", "FastAPI"],
        "experience_years": 3
    }
    
    # Store profile
    success = await store.store_user_profile("test_user", profile_data)
    assert success is True
    
    # Get profile
    profile = await store.get_user_profile("test_user")
    assert profile is not None
    assert profile["name"] == "Test User"

class MockCollection:
    """Mock MongoDB collection for testing."""
    
    def __init__(self):
        self.data = {}
    
    async def replace_one(self, filter_dict, data, upsert=False):
        user_id = filter_dict["user_id"]
        self.data[user_id] = data
        return MockResult(True)
    
    async def find_one(self, filter_dict):
        user_id = filter_dict["user_id"]
        return self.data.get(user_id)
    
    async def create_index(self, *args, **kwargs):
        pass

class MockResult:
    def __init__(self, acknowledged):
        self.acknowledged = acknowledged