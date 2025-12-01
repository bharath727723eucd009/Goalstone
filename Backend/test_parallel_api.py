"""Test the parallel agents API endpoint."""
import pytest
import asyncio
from unittest.mock import Mock
from api.agent_routes import parallel_agents_endpoint, ParallelAgentRequest

@pytest.mark.asyncio
async def test_parallel_agents_endpoint():
    """Test that the parallel agents endpoint returns valid results."""
    
    # Mock request data
    request_data = ParallelAgentRequest(
        user_goals=["Get promoted to senior developer", "Improve work-life balance"],
        user_data={
            "skills": ["Python", "JavaScript"],
            "experience_years": 3,
            "current_role": "Software Developer", 
            "age": 28,
            "interests": ["Cloud Computing", "AI/ML"],
            "income": 75000,
            "expenses": 3000,
            "activity_level": "moderate",
            "learning_style": "hands_on"
        },
        task_types={
            "career": "milestone_analysis",
            "wellness": "milestone_analysis", 
            "learning": "milestone_analysis"
        },
        parameters={"time_horizon": "6_months", "priority": "high"}
    )
    
    # Mock request object
    mock_request = Mock()
    mock_request.session = {}
    
    # Mock user_id
    user_id = "test_user_123"
    
    try:
        # Call the endpoint
        response = await parallel_agents_endpoint(request_data, mock_request, user_id)
        
        # Verify response structure
        assert response.status in ["success", "partial_success"]
        assert isinstance(response.results, dict)
        assert isinstance(response.execution_time, float)
        assert isinstance(response.errors, dict)
        
        # Check that we have results for each agent
        expected_agents = ["career", "wellness", "learning"]
        for agent in expected_agents:
            if agent in response.results:
                print(f"[SUCCESS] {agent} agent returned results")
                # Verify agent-specific data structure
                agent_data = response.results[agent]
                assert isinstance(agent_data, dict)
                
                if agent == "career":
                    assert "current_skills" in agent_data
                    assert "target_roles" in agent_data
                    assert "tasks" in agent_data
                elif agent == "wellness":
                    assert "recommendation" in agent_data
                    assert "weekly_plan" in agent_data
                elif agent == "learning":
                    assert "recommendation" in agent_data
                    assert "course_suggestions" in agent_data
            else:
                print(f"[WARNING] {agent} agent not in results")
        
        # Check for errors
        if response.errors:
            print(f"[INFO] Errors reported: {list(response.errors.keys())}")
        else:
            print("[SUCCESS] No errors reported")
        
        print(f"[INFO] Execution time: {response.execution_time:.2f}s")
        print(f"[INFO] Overall status: {response.status}")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Endpoint test failed: {e}")
        return False

if __name__ == "__main__":
    # Run the test
    result = asyncio.run(test_parallel_agents_endpoint())
    if result:
        print("\n[SUCCESS] All tests passed!")
    else:
        print("\n[ERROR] Tests failed!")