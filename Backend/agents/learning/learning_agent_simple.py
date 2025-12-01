"""Simplified Learning Agent implementation."""
from typing import Dict, Any, List
from ..base_agent import BaseAgent

class LearningAgent(BaseAgent):
    """Agent specialized in educational content and skill development."""
    
    def __init__(self):
        super().__init__("learning_agent", "Learning Agent")
    
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process learning-related tasks."""
        self.logger.info("Processing learning task", task_type=task.get("type"))
        
        try:
            user_data = task.get("user_data", {})
            user_goals = task.get("user_goals", [])
            
            # Extract user learning preferences
            current_skills = user_data.get("skills", [])
            if isinstance(current_skills, str):
                current_skills = [current_skills]
            
            interests = user_data.get("interests", [])
            if isinstance(interests, str):
                interests = [interests]
            
            learning_style = user_data.get("learning_style", "mixed")
            experience_years = self._safe_int(user_data.get("experience_years", 0))
            
            # Generate learning recommendations
            recommendations = self._generate_learning_recommendations(current_skills, interests, learning_style, user_goals)
            course_suggestions = self._suggest_courses(current_skills, interests, experience_years)
            learning_path = self._create_learning_path(current_skills, interests, learning_style)
            
            return {
                "recommendation": recommendations,
                "course_suggestions": course_suggestions,
                "learning_path": learning_path,
                "current_skills": current_skills,
                "interests": interests
            }
            
        except Exception as e:
            self.update_metrics("errors")
            self.logger.error("Task processing failed", error=str(e))
            raise
    
    async def get_recommendations(self, user_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate learning recommendations."""
        interests = user_data.get("interests", [])
        skill_level = user_data.get("skill_level", "beginner")
        
        return [
            {
                "type": "learning",
                "title": f"Advanced {interests[0] if interests else 'Programming'}",
                "description": f"{skill_level.title()} level course",
                "priority": 0.9
            }
        ]
    
    def _safe_int(self, value, default=0):
        """Safely convert value to int."""
        try:
            return int(float(value)) if value else default
        except (ValueError, TypeError):
            return default
    
    def _generate_learning_recommendations(self, skills: List[str], interests: List[str], 
                                         learning_style: str, goals: List[str]) -> str:
        """Generate personalized learning recommendations."""
        recommendations = []
        
        # Skill-based recommendations
        if not skills:
            recommendations.append("• Start with fundamental programming concepts")
            recommendations.append("• Choose a beginner-friendly language like Python")
        else:
            recommendations.append(f"• Build upon your existing {', '.join(skills[:2])} skills")
            recommendations.append("• Consider advanced topics in your current skill areas")
        
        # Interest-based recommendations
        if interests:
            for interest in interests[:2]:
                if "ai" in interest.lower() or "machine learning" in interest.lower():
                    recommendations.append("• Explore machine learning fundamentals and Python libraries")
                    recommendations.append("• Practice with real datasets and projects")
                elif "web" in interest.lower():
                    recommendations.append("• Learn modern web frameworks and responsive design")
                    recommendations.append("• Build full-stack projects for your portfolio")
                elif "data" in interest.lower():
                    recommendations.append("• Master data analysis tools like SQL and Excel")
                    recommendations.append("• Learn data visualization techniques")
                elif "cloud" in interest.lower():
                    recommendations.append("• Get certified in major cloud platforms (AWS, Azure, GCP)")
                    recommendations.append("• Practice with cloud architecture and deployment")
        
        # Learning style recommendations
        if learning_style == "hands_on":
            recommendations.append("• Focus on project-based learning and practical exercises")
            recommendations.append("• Build a portfolio of real-world projects")
        elif learning_style == "visual":
            recommendations.append("• Use video tutorials and interactive learning platforms")
            recommendations.append("• Create mind maps and visual summaries")
        elif learning_style == "reading":
            recommendations.append("• Supplement with technical books and documentation")
            recommendations.append("• Join online communities and forums for discussions")
        
        # Goal-based recommendations
        for goal in goals:
            if "promotion" in goal.lower() or "senior" in goal.lower():
                recommendations.append("• Develop leadership and communication skills")
                recommendations.append("• Learn system design and architecture patterns")
            elif "career change" in goal.lower() or "switch" in goal.lower():
                recommendations.append("• Build a strong portfolio showcasing new skills")
                recommendations.append("• Network with professionals in your target field")
        
        return "\n".join(recommendations)
    
    def _suggest_courses(self, skills: List[str], interests: List[str], experience: int) -> List[Dict[str, Any]]:
        """Suggest relevant courses based on user profile."""
        courses = []
        
        # Beginner courses
        if experience < 2:
            courses.extend([
                {
                    "title": "Programming Fundamentals",
                    "provider": "CodeAcademy",
                    "duration": "8 weeks",
                    "difficulty": "beginner",
                    "rating": 4.5
                },
                {
                    "title": "Introduction to Web Development",
                    "provider": "freeCodeCamp",
                    "duration": "12 weeks", 
                    "difficulty": "beginner",
                    "rating": 4.7
                }
            ])
        
        # Intermediate courses
        elif experience < 5:
            courses.extend([
                {
                    "title": "Advanced JavaScript Concepts",
                    "provider": "Udemy",
                    "duration": "6 weeks",
                    "difficulty": "intermediate",
                    "rating": 4.6
                },
                {
                    "title": "Database Design and SQL",
                    "provider": "Coursera",
                    "duration": "10 weeks",
                    "difficulty": "intermediate", 
                    "rating": 4.4
                }
            ])
        
        # Advanced courses
        else:
            courses.extend([
                {
                    "title": "System Design and Architecture",
                    "provider": "Pluralsight",
                    "duration": "4 weeks",
                    "difficulty": "advanced",
                    "rating": 4.8
                },
                {
                    "title": "Machine Learning Engineering",
                    "provider": "edX",
                    "duration": "16 weeks",
                    "difficulty": "advanced",
                    "rating": 4.5
                }
            ])
        
        # Interest-specific courses
        for interest in interests:
            if "ai" in interest.lower():
                courses.append({
                    "title": "Deep Learning Specialization",
                    "provider": "Coursera",
                    "duration": "20 weeks",
                    "difficulty": "intermediate",
                    "rating": 4.9
                })
            elif "cloud" in interest.lower():
                courses.append({
                    "title": "AWS Solutions Architect",
                    "provider": "A Cloud Guru",
                    "duration": "12 weeks",
                    "difficulty": "intermediate",
                    "rating": 4.6
                })
        
        return courses[:5]  # Return top 5 recommendations
    
    def _create_learning_path(self, skills: List[str], interests: List[str], learning_style: str) -> Dict[str, Any]:
        """Create a structured learning path."""
        
        phases = []
        
        # Phase 1: Foundation
        phase1_topics = ["Basic concepts", "Core fundamentals"]
        if not skills:
            phase1_topics.extend(["Programming basics", "Problem-solving"])
        else:
            phase1_topics.extend([f"Advanced {skills[0]}", "Best practices"])
        
        phases.append({
            "phase": 1,
            "title": "Foundation Building",
            "duration": "4-6 weeks",
            "topics": phase1_topics,
            "deliverables": ["Complete basic exercises", "Build simple project"]
        })
        
        # Phase 2: Skill Development
        phase2_topics = ["Intermediate concepts", "Practical applications"]
        if interests:
            phase2_topics.extend([f"{interests[0]} fundamentals", "Industry tools"])
        
        phases.append({
            "phase": 2,
            "title": "Skill Development",
            "duration": "6-8 weeks", 
            "topics": phase2_topics,
            "deliverables": ["Complete intermediate project", "Join community"]
        })
        
        # Phase 3: Mastery
        phases.append({
            "phase": 3,
            "title": "Advanced Mastery",
            "duration": "4-6 weeks",
            "topics": ["Advanced techniques", "Real-world projects", "Portfolio development"],
            "deliverables": ["Complete capstone project", "Prepare for interviews"]
        })
        
        return {
            "total_duration": "14-20 weeks",
            "phases": phases,
            "learning_style": learning_style,
            "recommended_time_per_week": "8-12 hours"
        }