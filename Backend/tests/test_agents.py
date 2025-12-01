"""Test cases for agent functionality."""
import pytest
import asyncio
from ..agents.coordinator.coordinator_agent import CoordinatorAgent
from ..agents.career.career_agent import CareerAgent

@pytest.mark.asyncio
async def test_career_agent_recommendations():
    """Test career agent recommendations."""
    agent = CareerAgent()
    
    user_data = {
        "skills": ["Python", "Machine Learning"],
        "experience_years": 3,
        "interests": ["AI", "Data Science"]
    }
    
    recommendations = await agent.get_recommendations(user_data)
    
    assert isinstance(recommendations, list)
    assert len(recommendations) > 0
    assert all("type" in rec and rec["type"] == "career" for rec in recommendations)

@pytest.mark.asyncio
async def test_coordinator_agent():
    """Test coordinator agent orchestration."""
    coordinator = CoordinatorAgent()
    
    user_data = {
        "skills": ["Python"],
        "experience_years": 2,
        "income": 50000,
        "health_goals": ["fitness"],
        "learning_goals": ["AI"]
    }
    
    recommendations = await coordinator.get_recommendations(user_data)
    
    assert isinstance(recommendations, list)
    assert len(recommendations) > 0
    
    # Should have recommendations from multiple agent types
    types = {rec["type"] for rec in recommendations}
    assert len(types) > 1

@pytest.mark.asyncio
async def test_agent_health_check():
    """Test agent health check functionality."""
    agent = CareerAgent()
    health = await agent.health_check()
    
    assert "agent_id" in health
    assert "status" in health
    assert health["status"] == "healthy"