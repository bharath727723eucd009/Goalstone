"""Test script for parallel agents functionality."""
import asyncio
import sys
import os

# Add the Backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.career.career_agent_pro import CareerAgent
from agents.wellness.wellness_agent_pro import WellnessAgent  
from agents.learning.learning_agent_pro import LearningAgent

async def test_parallel_agents():
    """Test that all agents work without errors."""
    
    # Sample input data
    test_input = {
        "user_goals": ["Get promoted to senior developer", "Improve work-life balance"],
        "user_data": {
            "skills": ["Python", "JavaScript"],
            "experience_years": "3",
            "current_role": "Software Developer",
            "age": "28",
            "interests": ["Cloud Computing", "AI/ML"],
            "income": "75000",
            "expenses": "3000",
            "activity_level": "moderate",
            "learning_style": "hands_on"
        },
        "type": "milestone_analysis"
    }
    
    # Initialize agents
    career_agent = CareerAgent()
    wellness_agent = WellnessAgent()
    learning_agent = LearningAgent()
    
    print("Testing Career Agent...")
    try:
        career_result = await career_agent.run(test_input)
        print(f"[SUCCESS] Career Agent: {career_result['status']}")
        if career_result['status'] == 'success':
            data = career_result['data']
            print(f"   - Skills: {len(data.get('current_skills', []))}")
            print(f"   - Target Roles: {len(data.get('target_roles', []))}")
            print(f"   - Tasks: {len(data.get('tasks', []))}")
    except Exception as e:
        print(f"[ERROR] Career Agent failed: {e}")
    
    print("\nTesting Wellness Agent...")
    try:
        wellness_result = await wellness_agent.run(test_input)
        print(f"[SUCCESS] Wellness Agent: {wellness_result['status']}")
        if wellness_result['status'] == 'success':
            data = wellness_result['data']
            print(f"   - Weekly Plan: {len(data.get('weekly_plan', []))} activities")
            print(f"   - Health Tips: {len(data.get('health_tips', []))}")
    except Exception as e:
        print(f"[ERROR] Wellness Agent failed: {e}")
    
    print("\nTesting Learning Agent...")
    try:
        learning_result = await learning_agent.run(test_input)
        print(f"[SUCCESS] Learning Agent: {learning_result['status']}")
        if learning_result['status'] == 'success':
            data = learning_result['data']
            print(f"   - Course Suggestions: {len(data.get('course_suggestions', []))}")
            print(f"   - Learning Path Phases: {len(data.get('learning_path', {}).get('phases', []))}")
    except Exception as e:
        print(f"[ERROR] Learning Agent failed: {e}")
    
    print("\nTesting Parallel Execution...")
    try:
        # Run all agents concurrently
        results = await asyncio.gather(
            career_agent.run(test_input),
            wellness_agent.run(test_input),
            learning_agent.run(test_input),
            return_exceptions=True
        )
        
        success_count = sum(1 for r in results if isinstance(r, dict) and r.get('status') == 'success')
        print(f"[SUCCESS] Parallel execution completed: {success_count}/3 agents successful")
        
    except Exception as e:
        print(f"[ERROR] Parallel execution failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_parallel_agents())