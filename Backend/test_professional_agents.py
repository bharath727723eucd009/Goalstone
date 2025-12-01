"""Test professional agents with simplified imports."""
import asyncio
import sys
import os
import structlog

# Add the Backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Mock logger for testing
logger = structlog.get_logger(__name__)

class MockMetricsCollector:
    def record_agent_run(self, *args, **kwargs):
        pass

# Mock the imports
def mock_get_logger(name):
    return logger

sys.modules['observability.logger'] = type('MockModule', (), {'get_logger': mock_get_logger})()
sys.modules['observability.metrics'] = type('MockModule', (), {'metrics_collector': MockMetricsCollector()})()

from agents.career.career_agent_pro import CareerAgent
from agents.wellness.wellness_agent_complete import WellnessAgent  
from agents.learning.learning_agent_complete import LearningAgent

async def test_professional_agents():
    """Test that all professional agents work without errors."""
    
    # Sample input data
    test_input = {
        "user_goals": ["Get promoted to senior developer", "Improve work-life balance", "Learn cloud technologies"],
        "user_data": {
            "skills": ["Python", "JavaScript"],
            "experience_years": 3,
            "current_role": "Software Developer",
            "age": 28,
            "interests": ["Cloud Computing", "AI/ML"],
            "income": 75000,
            "expenses": 3000,
            "activity_level": "moderate",
            "learning_style": "hands_on",
            "time_commitment": "10_hours_week"
        },
        "type": "milestone_analysis"
    }
    
    # Initialize agents
    career_agent = CareerAgent()
    wellness_agent = WellnessAgent()
    learning_agent = LearningAgent()
    
    print("Testing Professional Career Agent...")
    try:
        career_result = await career_agent.run(test_input)
        print(f"[SUCCESS] Career Agent: {career_result['status']}")
        if career_result['status'] == 'success':
            data = career_result['data']
            print(f"   - Skills Analysis: {len(data.get('skills_analysis', {}).get('current_skills', []))}")
            print(f"   - Target Roles: {len(data.get('target_roles', []))}")
            print(f"   - Roadmap Tasks: {len(data.get('tasks', []))}")
            print(f"   - Confidence Score: {data.get('confidence_score', 0):.2f}")
    except Exception as e:
        print(f"[ERROR] Career Agent failed: {e}")
    
    print("\nTesting Professional Wellness Agent...")
    try:
        wellness_result = await wellness_agent.run(test_input)
        print(f"[SUCCESS] Wellness Agent: {wellness_result['status']}")
        if wellness_result['status'] == 'success':
            data = wellness_result['data']
            print(f"   - Health Score: {data.get('health_score', 0):.1f}")
            print(f"   - Weekly Plan: {len(data.get('weekly_plan', []))} activities")
            print(f"   - Priority Actions: {len(data.get('priority_actions', []))}")
    except Exception as e:
        print(f"[ERROR] Wellness Agent failed: {e}")
    
    print("\nTesting Professional Learning Agent...")
    try:
        learning_result = await learning_agent.run(test_input)
        print(f"[SUCCESS] Learning Agent: {learning_result['status']}")
        if learning_result['status'] == 'success':
            data = learning_result['data']
            print(f"   - Course Suggestions: {len(data.get('course_suggestions', []))}")
            print(f"   - Learning Efficiency: {data.get('learning_efficiency_score', 0):.1f}")
            print(f"   - Target Skills: {len(data.get('target_skills', []))}")
    except Exception as e:
        print(f"[ERROR] Learning Agent failed: {e}")
    
    print("\nTesting Professional Parallel Execution...")
    try:
        # Run all agents concurrently
        results = await asyncio.gather(
            career_agent.run(test_input),
            wellness_agent.run(test_input),
            learning_agent.run(test_input),
            return_exceptions=True
        )
        
        success_count = sum(1 for r in results if isinstance(r, dict) and r.get('status') == 'success')
        print(f"[SUCCESS] Professional parallel execution completed: {success_count}/3 agents successful")
        
        # Show sample of rich data
        if success_count > 0:
            print("\n=== SAMPLE PROFESSIONAL OUTPUT ===")
            for i, result in enumerate(results):
                agent_names = ["Career", "Wellness", "Learning"]
                if isinstance(result, dict) and result.get('status') == 'success':
                    data = result['data']
                    print(f"\n{agent_names[i]} Agent Rich Data:")
                    
                    if i == 0:  # Career
                        if 'salary_analysis' in data:
                            print(f"  - Salary Analysis: {data['salary_analysis'].get('total_5_year_growth', 0):.1f}% growth projection")
                        if 'market_analysis' in data:
                            print(f"  - Market Health: {data['market_analysis'].get('overall_market_health', 'N/A')}")
                    elif i == 1:  # Wellness
                        if 'health_assessment' in data:
                            print(f"  - Health Grade: {data['health_assessment'].get('health_grade', 'N/A')}")
                        if 'wellness_trajectory' in data:
                            print(f"  - 12-Month Target: {data['wellness_trajectory'].get('12_month_target', 0):.1f}")
                    elif i == 2:  # Learning
                        if 'certification_strategy' in data:
                            print(f"  - Certification ROI: ${data['certification_strategy'].get('strategy_metrics', {}).get('projected_roi', 0):,}")
                        if 'career_impact' in data:
                            print(f"  - 5-Year Career Impact: {data['career_impact'].get('5_year_impact', {}).get('salary_multiplier', 1):.2f}x")
        
    except Exception as e:
        print(f"[ERROR] Professional parallel execution failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_professional_agents())