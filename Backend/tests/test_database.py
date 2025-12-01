"""Test cases for database operations."""
import pytest
from datetime import datetime
from ..database.models import UserData, Milestone, AgentOutput
from ..database.repository import UserRepository, MilestoneRepository, AgentOutputRepository

# Mock database for testing
class MockCollection:
    def __init__(self):
        self.data = {}
        self.counter = 0
    
    async def insert_one(self, doc):
        self.counter += 1
        doc_id = f"mock_id_{self.counter}"
        self.data[doc_id] = doc
        return MockResult(doc_id)
    
    async def find_one(self, query):
        for doc_id, doc in self.data.items():
            if all(doc.get(k) == v for k, v in query.items()):
                doc["_id"] = doc_id
                return doc
        return None
    
    def find(self, query):
        return MockCursor([
            {**doc, "_id": doc_id} 
            for doc_id, doc in self.data.items()
            if all(doc.get(k) == v for k, v in query.items())
        ])

class MockResult:
    def __init__(self, inserted_id):
        self.inserted_id = inserted_id

class MockCursor:
    def __init__(self, data):
        self.data = data
    
    def sort(self, field, direction):
        return self
    
    def limit(self, count):
        return self
    
    async def __aiter__(self):
        for item in self.data:
            yield item

@pytest.mark.asyncio
async def test_user_data_model():
    """Test UserData model validation."""
    user_data = UserData(
        user_id="test_user",
        name="Test User",
        skills=["Python", "FastAPI"],
        experience_years=3
    )
    
    assert user_data.user_id == "test_user"
    assert user_data.name == "Test User"
    assert len(user_data.skills) == 2
    assert user_data.experience_years == 3

@pytest.mark.asyncio
async def test_milestone_model():
    """Test Milestone model validation."""
    milestone = Milestone(
        user_id="test_user",
        title="Learn Python",
        description="Complete Python course",
        category="learning",
        priority=3
    )
    
    assert milestone.user_id == "test_user"
    assert milestone.title == "Learn Python"
    assert milestone.category == "learning"
    assert milestone.status == "active"
    assert milestone.progress == 0.0

@pytest.mark.asyncio
async def test_agent_output_model():
    """Test AgentOutput model validation."""
    output = AgentOutput(
        user_id="test_user",
        agent_type="career",
        task_type="job_search",
        input_data={"skills": ["Python"]},
        output_data={"jobs": []},
        status="success",
        execution_time=1.5
    )
    
    assert output.user_id == "test_user"
    assert output.agent_type == "career"
    assert output.status == "success"
    assert output.execution_time == 1.5