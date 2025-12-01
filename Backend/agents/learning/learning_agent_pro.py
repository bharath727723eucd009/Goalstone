"""Professional Learning Agent with advanced AI-powered educational intelligence."""
import asyncio
import json
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from agents.base_agent import BaseAgent
try:
    from observability.logger import get_logger
    from observability.metrics import metrics_collector
    logger = get_logger(__name__)
except:
    import structlog
    logger = structlog.get_logger(__name__)
    class MockMetrics:
        def record_agent_run(self, *args, **kwargs): pass
    metrics_collector = MockMetrics()

class LearningAgent(BaseAgent):
    """Enterprise-grade Learning Agent with AI-powered educational optimization and personalized learning paths."""
    
    def __init__(self):
        super().__init__("learning_agent", "AI Learning Intelligence Agent")
        self.skill_taxonomy = {
            "programming": {
                "python": {"difficulty": 3, "market_demand": 95, "learning_time": 120, "prerequisites": []},
                "javascript": {"difficulty": 4, "market_demand": 90, "learning_time": 100, "prerequisites": []},
                "react": {"difficulty": 5, "market_demand": 85, "learning_time": 80, "prerequisites": ["javascript"]},
                "machine_learning": {"difficulty": 8, "market_demand": 98, "learning_time": 200, "prerequisites": ["python", "statistics"]},
                "cloud_computing": {"difficulty": 6, "market_demand": 92, "learning_time": 150, "prerequisites": ["networking"]},
                "data_science": {"difficulty": 7, "market_demand": 94, "learning_time": 180, "prerequisites": ["python", "statistics"]}
            },
            "business": {
                "project_management": {"difficulty": 4, "market_demand": 80, "learning_time": 60, "prerequisites": []},
                "digital_marketing": {"difficulty": 3, "market_demand": 75, "learning_time": 90, "prerequisites": []},
                "data_analysis": {"difficulty": 5, "market_demand": 88, "learning_time": 120, "prerequisites": ["excel"]},
                "product_management": {"difficulty": 6, "market_demand": 85, "learning_time": 100, "prerequisites": ["business_analysis"]}
            },
            "design": {
                "ui_ux_design": {"difficulty": 5, "market_demand": 82, "learning_time": 140, "prerequisites": []},
                "graphic_design": {"difficulty": 4, "market_demand": 70, "learning_time": 100, "prerequisites": []},
                "web_design": {"difficulty": 4, "market_demand": 75, "learning_time": 90, "prerequisites": ["html_css"]}
            }
        }
        
        self.learning_styles = {
            "visual": {"video_weight": 0.4, "text_weight": 0.2, "interactive_weight": 0.4},
            "auditory": {"video_weight": 0.5, "text_weight": 0.1, "interactive_weight": 0.4},
            "kinesthetic": {"video_weight": 0.2, "text_weight": 0.1, "interactive_weight": 0.7},
            "reading": {"video_weight": 0.2, "text_weight": 0.6, "interactive_weight": 0.2},
            "mixed": {"video_weight": 0.35, "text_weight": 0.3, "interactive_weight": 0.35}
        }
        
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process advanced learning intelligence tasks with AI-powered optimization."""
        logger.info("Processing advanced learning analysis", task_type=task.get("type"))
        
        try:
            user_data = task.get("user_data", {})
            user_goals = task.get("user_goals", [])
            
            # Advanced skill gap analysis with market intelligence
            skill_analysis = await self._analyze_skills_with_market_intelligence(user_data, user_goals)
            
            # AI-powered learning path optimization
            learning_path = await self._generate_ai_learning_path(user_data, skill_analysis, user_goals)
            
            # Personalized course curation with quality scoring
            course_recommendations = await self._curate_premium_courses(skill_analysis, user_data)
            
            # Adaptive learning timeline with milestone tracking
            learning_timeline = await self._create_adaptive_timeline(learning_path, user_data)
            
            # Certification roadmap with ROI analysis
            certification_strategy = await self._design_certification_strategy(skill_analysis, user_data)
            
            # Learning effectiveness optimization
            learning_optimization = await self._optimize_learning_effectiveness(user_data, learning_path)
            
            # Career impact analysis
            career_impact = await self._analyze_learning_career_impact(skill_analysis, certification_strategy)
            
            # AI-powered learning coaching
            coaching_recommendations = await self._generate_learning_coaching(user_data, skill_analysis, learning_path)
            
            return {
                "skill_analysis": skill_analysis,
                "learning_path": learning_path,
                "course_recommendations": course_recommendations,
                "learning_timeline": learning_timeline,
                "certification_strategy": certification_strategy,
                "learning_optimization": learning_optimization,
                "career_impact": career_impact,
                "coaching_recommendations": coaching_recommendations,
                "recommendation": coaching_recommendations["ai_summary"],
                "course_suggestions": course_recommendations["curated_courses"],
                "current_skills": skill_analysis["current_skills"],
                "target_skills": skill_analysis["target_skills"],
                "learning_efficiency_score": learning_optimization["efficiency_score"]
            }
            
        except Exception as e:
            self.update_metrics("errors")
            logger.error("Advanced learning analysis failed", error=str(e))
            raise
    
    async def get_recommendations(self, user_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate AI-powered learning recommendations."""
        interests = user_data.get("interests", [])
        current_skills = user_data.get("skills", [])
        experience = self._safe_int(user_data.get("experience_years", 0))
        
        recommendations = []
        
        for interest in interests[:3]:
            skill_data = self._find_skill_data(interest)
            if skill_data:
                recommendations.append({
                    "type": "learning",
                    "title": f"Advanced {interest.title()} Mastery Program",
                    "description": f"Comprehensive learning path with {skill_data['learning_time']} hours of content",
                    "priority": skill_data["market_demand"] / 100,
                    "difficulty": skill_data["difficulty"],
                    "market_demand": skill_data["market_demand"],
                    "estimated_completion": f"{skill_data['learning_time'] // 20} weeks"
                })
        
        return recommendations
    
    async def _analyze_skills_with_market_intelligence(self, user_data: Dict[str, Any], goals: List[str]) -> Dict[str, Any]:
        """Advanced skill analysis with real-time market intelligence."""
        current_skills = user_data.get("skills", [])
        if isinstance(current_skills, str):
            current_skills = [s.strip() for s in current_skills.split(",")]
        
        interests = user_data.get("interests", [])
        if isinstance(interests, str):
            interests = [i.strip() for i in interests.split(",")]
        
        experience_years = self._safe_int(user_data.get("experience_years", 0))
        learning_style = user_data.get("learning_style", "mixed")
        
        # Analyze current skill proficiency and market value
        skill_proficiency = await self._assess_skill_proficiency(current_skills, experience_years)
        
        # Identify target skills from goals and interests
        target_skills = await self._identify_target_skills(goals, interests, current_skills)
        
        # Market demand analysis for skills
        market_analysis = await self._analyze_skill_market_demand(current_skills + target_skills)
        
        # Skill gap analysis with learning difficulty assessment
        skill_gaps = await self._analyze_comprehensive_skill_gaps(current_skills, target_skills)
        
        # Learning readiness assessment
        learning_readiness = await self._assess_learning_readiness(user_data, skill_gaps)
        
        return {
            "current_skills": current_skills,
            "target_skills": target_skills,
            "skill_proficiency": skill_proficiency,
            "market_analysis": market_analysis,
            "skill_gaps": skill_gaps,
            "learning_readiness": learning_readiness,
            "learning_style": learning_style,
            "experience_level": self._categorize_experience_level(experience_years),
            "skill_portfolio_score": self._calculate_skill_portfolio_score(skill_proficiency, market_analysis)
        }
    
    async def _generate_ai_learning_path(self, user_data: Dict[str, Any], skill_analysis: Dict[str, Any], goals: List[str]) -> Dict[str, Any]:
        """Generate AI-optimized learning path with adaptive sequencing."""
        target_skills = skill_analysis["target_skills"]
        current_skills = skill_analysis["current_skills"]
        learning_style = skill_analysis["learning_style"]
        skill_gaps = skill_analysis["skill_gaps"]
        
        # Create learning dependency graph
        dependency_graph = await self._create_learning_dependency_graph(target_skills)
        
        # Optimize learning sequence using AI algorithms
        optimal_sequence = await self._optimize_learning_sequence(dependency_graph, skill_gaps, user_data)
        
        # Generate learning phases with adaptive milestones
        learning_phases = await self._create_adaptive_learning_phases(optimal_sequence, learning_style)
        
        # Create personalized learning modules
        learning_modules = await self._design_learning_modules(learning_phases, user_data)
        
        # Calculate learning path metrics
        path_metrics = await self._calculate_learning_path_metrics(learning_phases, skill_analysis)
        
        return {
            "dependency_graph": dependency_graph,
            "optimal_sequence": optimal_sequence,
            "learning_phases": learning_phases,
            "learning_modules": learning_modules,
            "path_metrics": path_metrics,
            "total_duration": path_metrics["total_weeks"],
            "difficulty_progression": path_metrics["difficulty_curve"],
            "success_probability": path_metrics["success_probability"]
        }
    
    async def _curate_premium_courses(self, skill_analysis: Dict[str, Any], user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Curate premium courses with quality scoring and personalization."""
        target_skills = skill_analysis["target_skills"]
        learning_style = skill_analysis["learning_style"]
        experience_level = skill_analysis["experience_level"]
        
        curated_courses = []
        
        for skill in target_skills:
            # Find courses for each skill
            skill_courses = await self._find_courses_for_skill(skill, experience_level)
            
            # Score courses based on quality, relevance, and learning style match
            scored_courses = []
            for course in skill_courses:
                quality_score = self._calculate_course_quality_score(course)
                relevance_score = self._calculate_course_relevance(course, skill, user_data)
                style_match = self._calculate_learning_style_match(course, learning_style)
                
                total_score = (quality_score * 0.4) + (relevance_score * 0.4) + (style_match * 0.2)
                
                scored_courses.append({
                    **course,
                    "quality_score": quality_score,
                    "relevance_score": relevance_score,
                    "style_match": style_match,
                    "total_score": total_score,
                    "skill": skill
                })
            
            # Select top courses for this skill
            top_courses = sorted(scored_courses, key=lambda x: x["total_score"], reverse=True)[:3]
            curated_courses.extend(top_courses)
        
        # Diversify course providers and formats
        diversified_courses = self._diversify_course_selection(curated_courses)
        
        return {
            "curated_courses": diversified_courses,
            "total_courses": len(diversified_courses),
            "average_quality": sum(c["quality_score"] for c in diversified_courses) / len(diversified_courses) if diversified_courses else 0,
            "learning_style_alignment": sum(c["style_match"] for c in diversified_courses) / len(diversified_courses) if diversified_courses else 0,
            "course_categories": self._categorize_courses(diversified_courses)
        }
    
    async def _create_adaptive_timeline(self, learning_path: Dict[str, Any], user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create adaptive learning timeline with milestone tracking."""
        learning_phases = learning_path["learning_phases"]
        time_commitment = user_data.get("time_commitment", "10_hours_week")
        
        # Parse time commitment
        weekly_hours = self._parse_time_commitment(time_commitment)
        
        # Calculate timeline for each phase
        timeline_phases = []
        cumulative_weeks = 0
        
        for phase in learning_phases:
            phase_hours = phase["estimated_hours"]
            phase_weeks = max(1, phase_hours / weekly_hours)
            
            # Add buffer time for practice and review
            buffer_multiplier = 1.3 if phase["difficulty"] > 6 else 1.2
            adjusted_weeks = phase_weeks * buffer_multiplier
            
            timeline_phases.append({
                "phase_name": phase["name"],
                "start_week": cumulative_weeks + 1,
                "duration_weeks": int(adjusted_weeks),
                "end_week": cumulative_weeks + int(adjusted_weeks),
                "milestones": self._create_phase_milestones(phase, int(adjusted_weeks)),
                "deliverables": phase.get("deliverables", []),
                "assessment_criteria": self._define_assessment_criteria(phase)
            })
            
            cumulative_weeks += int(adjusted_weeks)
        
        # Create overall timeline metrics
        timeline_metrics = {
            "total_duration_weeks": cumulative_weeks,
            "total_duration_months": round(cumulative_weeks / 4.33, 1),
            "weekly_time_commitment": weekly_hours,
            "total_learning_hours": sum(p["estimated_hours"] for p in learning_phases),
            "milestone_count": sum(len(p["milestones"]) for p in timeline_phases)
        }
        
        return {
            "timeline_phases": timeline_phases,
            "timeline_metrics": timeline_metrics,
            "adaptive_adjustments": self._create_adaptive_adjustments(timeline_phases, user_data),
            "progress_tracking": self._setup_progress_tracking_system(timeline_phases)
        }
    
    async def _design_certification_strategy(self, skill_analysis: Dict[str, Any], user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Design comprehensive certification strategy with ROI analysis."""
        target_skills = skill_analysis["target_skills"]
        experience_level = skill_analysis["experience_level"]
        current_income = self._safe_int(user_data.get("income", 0))
        
        # Identify relevant certifications
        relevant_certifications = []
        
        for skill in target_skills:
            certifications = self._find_certifications_for_skill(skill)
            for cert in certifications:
                # Calculate certification ROI
                roi_analysis = self._calculate_certification_roi(cert, current_income, experience_level)
                
                relevant_certifications.append({
                    **cert,
                    "skill": skill,
                    "roi_analysis": roi_analysis,
                    "priority_score": self._calculate_certification_priority(cert, skill_analysis, roi_analysis)
                })
        
        # Prioritize certifications
        prioritized_certs = sorted(relevant_certifications, key=lambda x: x["priority_score"], reverse=True)
        
        # Create certification roadmap
        certification_roadmap = self._create_certification_roadmap(prioritized_certs[:5])
        
        # Calculate overall strategy metrics
        strategy_metrics = {
            "total_certifications": len(prioritized_certs),
            "recommended_certifications": len(certification_roadmap["phases"]),
            "total_investment": sum(cert["cost"] for cert in prioritized_certs[:5]),
            "projected_roi": sum(cert["roi_analysis"]["annual_increase"] for cert in prioritized_certs[:5]),
            "completion_timeline": certification_roadmap["total_duration"]
        }
        
        return {
            "relevant_certifications": prioritized_certs,
            "certification_roadmap": certification_roadmap,
            "strategy_metrics": strategy_metrics,
            "investment_analysis": self._analyze_certification_investment(prioritized_certs[:5]),
            "career_impact_projection": self._project_certification_career_impact(prioritized_certs[:5])
        }
    
    async def _optimize_learning_effectiveness(self, user_data: Dict[str, Any], learning_path: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize learning effectiveness using cognitive science principles."""
        learning_style = user_data.get("learning_style", "mixed")
        age = self._safe_int(user_data.get("age", 25))
        experience_years = self._safe_int(user_data.get("experience_years", 0))
        
        # Cognitive load optimization
        cognitive_optimization = await self._optimize_cognitive_load(learning_path, age)
        
        # Spaced repetition scheduling
        spaced_repetition = await self._design_spaced_repetition_schedule(learning_path)
        
        # Active learning strategies
        active_learning = await self._design_active_learning_strategies(learning_style, learning_path)
        
        # Metacognitive training
        metacognitive_training = await self._design_metacognitive_training(user_data)
        
        # Learning environment optimization
        environment_optimization = await self._optimize_learning_environment(learning_style)
        
        # Calculate learning efficiency score
        efficiency_factors = {
            "cognitive_load": cognitive_optimization["efficiency_score"],
            "spaced_repetition": spaced_repetition["effectiveness_score"],
            "active_learning": active_learning["engagement_score"],
            "metacognitive": metacognitive_training["awareness_score"],
            "environment": environment_optimization["optimization_score"]
        }
        
        efficiency_score = sum(efficiency_factors.values()) / len(efficiency_factors)
        
        return {
            "cognitive_optimization": cognitive_optimization,
            "spaced_repetition": spaced_repetition,
            "active_learning": active_learning,
            "metacognitive_training": metacognitive_training,
            "environment_optimization": environment_optimization,
            "efficiency_factors": efficiency_factors,
            "efficiency_score": efficiency_score,
            "learning_acceleration": self._calculate_learning_acceleration(efficiency_score),
            "retention_improvement": self._calculate_retention_improvement(efficiency_factors)
        }
    
    async def _analyze_learning_career_impact(self, skill_analysis: Dict[str, Any], certification_strategy: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze career impact of learning investments."""
        target_skills = skill_analysis["target_skills"]
        market_analysis = skill_analysis["market_analysis"]
        certifications = certification_strategy["relevant_certifications"][:5]
        
        # Calculate skill-based career advancement potential
        advancement_potential = {}
        for skill in target_skills:
            market_data = market_analysis.get(skill, {})
            advancement_potential[skill] = {
                "salary_increase_potential": market_data.get("salary_premium", 0.15),
                "job_opportunity_increase": market_data.get("job_growth", 0.20),
                "career_level_advancement": self._calculate_career_level_impact(skill, market_data)
            }
        
        # Project career trajectory changes
        career_projections = []
        base_trajectory = {"level": "current", "salary_multiplier": 1.0, "opportunities": 1.0}
        
        for year in range(1, 6):
            # Calculate cumulative impact
            skill_impact = sum(adv["salary_increase_potential"] for adv in advancement_potential.values()) / len(advancement_potential)
            cert_impact = sum(cert["roi_analysis"]["salary_multiplier"] for cert in certifications) / len(certifications) if certifications else 1.0
            
            projected_salary_multiplier = 1.0 + (skill_impact * year * 0.5) + ((cert_impact - 1.0) * min(year, 2))
            projected_opportunities = 1.0 + (0.1 * year * len(target_skills))
            
            career_projections.append({
                "year": year,
                "salary_multiplier": min(2.0, projected_salary_multiplier),
                "opportunity_multiplier": min(3.0, projected_opportunities),
                "career_level": self._project_career_level(year, skill_impact, cert_impact),
                "market_positioning": self._assess_market_positioning(year, target_skills, certifications)
            })
        
        return {
            "advancement_potential": advancement_potential,
            "career_projections": career_projections,
            "5_year_impact": career_projections[-1],
            "roi_timeline": self._calculate_learning_roi_timeline(career_projections),
            "competitive_advantage": self._assess_competitive_advantage(target_skills, certifications),
            "career_risk_mitigation": self._assess_career_risk_mitigation(target_skills)
        }
    
    async def _generate_learning_coaching(self, user_data: Dict[str, Any], skill_analysis: Dict[str, Any], learning_path: Dict[str, Any]) -> Dict[str, Any]:
        """Generate AI-powered learning coaching recommendations."""
        learning_readiness = skill_analysis["learning_readiness"]
        learning_style = skill_analysis["learning_style"]
        path_metrics = learning_path["path_metrics"]
        
        # Personalized learning strategies
        learning_strategies = await self._generate_personalized_strategies(user_data, skill_analysis)
        
        # Motivation and engagement optimization
        motivation_system = await self._design_motivation_system(user_data, learning_path)
        
        # Learning obstacle identification and mitigation
        obstacle_mitigation = await self._identify_learning_obstacles(user_data, skill_analysis)
        
        # Progress monitoring and feedback systems
        monitoring_system = await self._design_progress_monitoring(learning_path, user_data)
        
        # Adaptive learning recommendations
        adaptive_recommendations = await self._generate_adaptive_recommendations(skill_analysis, learning_path)
        
        # Generate AI coaching summary
        ai_summary = self._generate_learning_ai_summary(user_data, skill_analysis, learning_path, path_metrics)
        
        return {
            "learning_strategies": learning_strategies,
            "motivation_system": motivation_system,
            "obstacle_mitigation": obstacle_mitigation,
            "monitoring_system": monitoring_system,
            "adaptive_recommendations": adaptive_recommendations,
            "ai_summary": ai_summary,
            "coaching_confidence": self._calculate_coaching_confidence(learning_readiness, path_metrics),
            "success_predictors": self._identify_success_predictors(user_data, skill_analysis)
        }
    
    def _safe_int(self, value, default=0):
        """Safely convert value to int."""
        try:
            return int(float(value)) if value else default
        except (ValueError, TypeError):
            return default
    
    def _safe_float(self, value, default=0.0):
        """Safely convert value to float."""
        try:
            return float(value) if value else default
        except (ValueError, TypeError):
            return default
    
    def _find_skill_data(self, skill: str) -> Optional[Dict[str, Any]]:
        """Find skill data in taxonomy."""
        skill_lower = skill.lower().replace(" ", "_")
        for category, skills in self.skill_taxonomy.items():
            if skill_lower in skills:
                return skills[skill_lower]
        return None
    
    async def _assess_skill_proficiency(self, skills: List[str], experience: int) -> Dict[str, Dict[str, Any]]:
        """Assess proficiency level for each skill."""
        proficiency_map = {}
        
        for skill in skills:
            skill_data = self._find_skill_data(skill)
            if skill_data:
                # Estimate proficiency based on experience and skill difficulty
                base_proficiency = min(100, (experience * 15) + 20)  # Base on years
                difficulty_adjustment = max(0.5, 1 - (skill_data["difficulty"] / 10))
                
                estimated_proficiency = int(base_proficiency * difficulty_adjustment)
                
                proficiency_map[skill] = {
                    "proficiency_score": estimated_proficiency,
                    "proficiency_level": self._categorize_proficiency(estimated_proficiency),
                    "market_value": skill_data["market_demand"],
                    "improvement_potential": 100 - estimated_proficiency,
                    "learning_priority": self._calculate_learning_priority(skill_data, estimated_proficiency)
                }
        
        return proficiency_map
    
    async def _identify_target_skills(self, goals: List[str], interests: List[str], current_skills: List[str]) -> List[str]:
        """Identify target skills from goals and interests."""
        target_skills = set()
        
        # Extract skills from goals
        goal_text = " ".join(goals).lower()
        for category, skills in self.skill_taxonomy.items():
            for skill in skills.keys():
                if skill.replace("_", " ") in goal_text or any(word in goal_text for word in skill.split("_")):
                    target_skills.add(skill.replace("_", " ").title())
        
        # Add skills from interests
        for interest in interests:
            interest_lower = interest.lower().replace(" ", "_")
            for category, skills in self.skill_taxonomy.items():
                if interest_lower in skills:
                    target_skills.add(interest)
                # Partial matching
                for skill in skills.keys():
                    if interest_lower in skill or skill in interest_lower:
                        target_skills.add(skill.replace("_", " ").title())
        
        # Remove current skills from targets
        current_skills_lower = [s.lower() for s in current_skills]
        target_skills = [s for s in target_skills if s.lower() not in current_skills_lower]
        
        return list(target_skills)[:8]  # Limit to top 8 targets
    
    async def _analyze_skill_market_demand(self, skills: List[str]) -> Dict[str, Dict[str, Any]]:
        """Analyze market demand for skills."""
        market_analysis = {}
        
        for skill in skills:
            skill_data = self._find_skill_data(skill)
            if skill_data:
                # Simulate market analysis
                market_analysis[skill] = {
                    "demand_score": skill_data["market_demand"],
                    "growth_trend": "high" if skill_data["market_demand"] > 85 else "moderate",
                    "salary_premium": 0.15 + (skill_data["market_demand"] / 1000),
                    "job_growth": 0.10 + (skill_data["market_demand"] / 500),
                    "competition_level": "high" if skill_data["market_demand"] > 90 else "moderate",
                    "future_outlook": "excellent" if skill_data["market_demand"] > 90 else "good"
                }
        
        return market_analysis
    
    async def _analyze_comprehensive_skill_gaps(self, current_skills: List[str], target_skills: List[str]) -> Dict[str, Any]:
        """Analyze comprehensive skill gaps."""
        gaps = []
        
        for target_skill in target_skills:
            if target_skill.lower() not in [s.lower() for s in current_skills]:
                skill_data = self._find_skill_data(target_skill)
                if skill_data:
                    gaps.append({
                        "skill": target_skill,
                        "difficulty": skill_data["difficulty"],
                        "learning_time": skill_data["learning_time"],
                        "prerequisites": skill_data["prerequisites"],
                        "market_demand": skill_data["market_demand"],
                        "priority": self._calculate_gap_priority(skill_data),
                        "learning_path_exists": len(skill_data["prerequisites"]) == 0 or any(prereq in [s.lower() for s in current_skills] for prereq in skill_data["prerequisites"])
                    })
        
        # Sort by priority
        gaps.sort(key=lambda x: x["priority"], reverse=True)
        
        return {
            "total_gaps": len(gaps),
            "critical_gaps": [g for g in gaps if g["priority"] > 80],
            "moderate_gaps": [g for g in gaps if 60 <= g["priority"] <= 80],
            "low_priority_gaps": [g for g in gaps if g["priority"] < 60],
            "all_gaps": gaps,
            "total_learning_time": sum(g["learning_time"] for g in gaps),
            "average_difficulty": sum(g["difficulty"] for g in gaps) / len(gaps) if gaps else 0
        }
    
    async def _assess_learning_readiness(self, user_data: Dict[str, Any], skill_gaps: Dict[str, Any]) -> Dict[str, Any]:
        """Assess learning readiness and capacity."""
        age = self._safe_int(user_data.get("age", 25))
        experience = self._safe_int(user_data.get("experience_years", 0))
        time_commitment = user_data.get("time_commitment", "10_hours_week")
        
        # Calculate readiness factors
        readiness_factors = {
            "cognitive_capacity": self._assess_cognitive_capacity(age),
            "experience_foundation": min(100, experience * 15),
            "time_availability": self._assess_time_availability(time_commitment),
            "learning_complexity": max(0, 100 - (skill_gaps["average_difficulty"] * 10)),
            "motivation_level": self._assess_motivation_level(user_data, skill_gaps)
        }
        
        overall_readiness = sum(readiness_factors.values()) / len(readiness_factors)
        
        return {
            "readiness_factors": readiness_factors,
            "overall_readiness": overall_readiness,
            "readiness_level": self._categorize_readiness(overall_readiness),
            "success_probability": self._calculate_success_probability(readiness_factors),
            "recommended_adjustments": self._recommend_readiness_adjustments(readiness_factors)
        }
    
    def _categorize_experience_level(self, years: int) -> str:
        """Categorize experience level."""
        if years < 1: return "beginner"
        elif years < 3: return "junior"
        elif years < 6: return "intermediate"
        elif years < 10: return "senior"
        else: return "expert"
    
    def _calculate_skill_portfolio_score(self, proficiency: Dict[str, Dict[str, Any]], market: Dict[str, Dict[str, Any]]) -> float:
        """Calculate overall skill portfolio score."""
        if not proficiency:
            return 0
        
        total_score = 0
        for skill, prof_data in proficiency.items():
            market_data = market.get(skill, {})
            skill_score = (prof_data["proficiency_score"] * 0.6) + (market_data.get("demand_score", 50) * 0.4)
            total_score += skill_score
        
        return total_score / len(proficiency)
    
    def _categorize_proficiency(self, score: int) -> str:
        """Categorize proficiency level."""
        if score >= 90: return "expert"
        elif score >= 75: return "advanced"
        elif score >= 60: return "intermediate"
        elif score >= 40: return "beginner"
        else: return "novice"
    
    def _calculate_learning_priority(self, skill_data: Dict[str, Any], proficiency: int) -> float:
        """Calculate learning priority for a skill."""
        market_weight = skill_data["market_demand"] / 100
        difficulty_weight = 1 - (skill_data["difficulty"] / 10)
        proficiency_gap = (100 - proficiency) / 100
        
        return (market_weight * 0.4) + (difficulty_weight * 0.3) + (proficiency_gap * 0.3)
    
    def _calculate_gap_priority(self, skill_data: Dict[str, Any]) -> float:
        """Calculate priority score for skill gap."""
        market_score = skill_data["market_demand"]
        difficulty_penalty = skill_data["difficulty"] * 5
        prerequisite_penalty = len(skill_data["prerequisites"]) * 10
        
        return max(0, market_score - difficulty_penalty - prerequisite_penalty)
    
    def _assess_cognitive_capacity(self, age: int) -> float:
        """Assess cognitive capacity based on age."""
        if age <= 25: return 100
        elif age <= 35: return 95
        elif age <= 45: return 90
        elif age <= 55: return 85
        else: return 80
    
    def _assess_time_availability(self, time_commitment: str) -> float:
        """Assess time availability score."""
        time_scores = {
            "5_hours_week": 40, "10_hours_week": 70, "15_hours_week": 85,
            "20_hours_week": 95, "25_hours_week": 100
        }
        return time_scores.get(time_commitment, 70)
    
    def _assess_motivation_level(self, user_data: Dict[str, Any], skill_gaps: Dict[str, Any]) -> float:
        """Assess motivation level."""
        # Base motivation on goal clarity and market alignment
        goals = user_data.get("user_goals", [])
        goal_clarity = min(100, len(goals) * 25)
        
        # Market alignment motivation
        high_demand_gaps = len(skill_gaps.get("critical_gaps", []))
        market_motivation = min(100, high_demand_gaps * 30)
        
        return (goal_clarity * 0.6) + (market_motivation * 0.4)
    
    def _categorize_readiness(self, score: float) -> str:
        """Categorize learning readiness."""
        if score >= 85: return "highly_ready"
        elif score >= 70: return "ready"
        elif score >= 55: return "moderately_ready"
        else: return "needs_preparation"
    
    def _calculate_success_probability(self, factors: Dict[str, float]) -> float:
        """Calculate learning success probability."""
        weights = {
            "cognitive_capacity": 0.2, "experience_foundation": 0.2,
            "time_availability": 0.3, "learning_complexity": 0.15,
            "motivation_level": 0.15
        }
        
        weighted_score = sum(factors[factor] * weights[factor] for factor in factors)
        return min(100, weighted_score)
    
    def _recommend_readiness_adjustments(self, factors: Dict[str, float]) -> List[str]:
        """Recommend adjustments to improve readiness."""
        recommendations = []
        
        if factors["time_availability"] < 60:
            recommendations.append("Consider increasing weekly time commitment for better learning outcomes")
        
        if factors["learning_complexity"] < 50:
            recommendations.append("Start with foundational skills before tackling advanced topics")
        
        if factors["motivation_level"] < 70:
            recommendations.append("Clarify learning goals and connect them to career objectives")
        
        return recommendations
    
    def _parse_time_commitment(self, commitment: str) -> float:
        """Parse time commitment string to hours per week."""
        time_map = {
            "5_hours_week": 5, "10_hours_week": 10, "15_hours_week": 15,
            "20_hours_week": 20, "25_hours_week": 25
        }
        return time_map.get(commitment, 10)
    
    async def _find_courses_for_skill(self, skill: str, experience_level: str) -> List[Dict[str, Any]]:
        """Find courses for a specific skill."""
        # Mock course database
        courses = [
            {
                "title": f"Complete {skill.title()} Mastery Course",
                "provider": "TechEdu Pro",
                "duration": "12 weeks",
                "format": "video_interactive",
                "difficulty": "intermediate",
                "rating": 4.8,
                "students": 15000,
                "price": 199,
                "certification": True,
                "hands_on_projects": 8,
                "instructor_rating": 4.9
            },
            {
                "title": f"Advanced {skill.title()} Specialization",
                "provider": "University Online",
                "duration": "16 weeks", 
                "format": "academic",
                "difficulty": "advanced",
                "rating": 4.6,
                "students": 8000,
                "price": 299,
                "certification": True,
                "hands_on_projects": 12,
                "instructor_rating": 4.7
            },
            {
                "title": f"{skill.title()} Bootcamp Intensive",
                "provider": "CodeCamp",
                "duration": "8 weeks",
                "format": "intensive",
                "difficulty": "beginner",
                "rating": 4.5,
                "students": 25000,
                "price": 149,
                "certification": False,
                "hands_on_projects": 6,
                "instructor_rating": 4.4
            }
        ]
        
        return courses
    
    def _calculate_course_quality_score(self, course: Dict[str, Any]) -> float:
        """Calculate course quality score."""
        factors = {
            "rating": course.get("rating", 4.0) * 20,  # Convert to 0-100
            "instructor_rating": course.get("instructor_rating", 4.0) * 20,
            "student_count": min(100, course.get("students", 1000) / 100),
            "hands_on_projects": min(100, course.get("hands_on_projects", 0) * 10),
            "certification": 100 if course.get("certification", False) else 70
        }
        
        return sum(factors.values()) / len(factors)
    
    def _calculate_course_relevance(self, course: Dict[str, Any], skill: str, user_data: Dict[str, Any]) -> float:
        """Calculate course relevance score."""
        experience_level = self._categorize_experience_level(self._safe_int(user_data.get("experience_years", 0)))
        
        # Match difficulty to experience
        difficulty_match = {
            "beginner": {"beginner": 100, "intermediate": 70, "advanced": 40},
            "junior": {"beginner": 80, "intermediate": 100, "advanced": 60},
            "intermediate": {"beginner": 60, "intermediate": 90, "advanced": 100},
            "senior": {"beginner": 40, "intermediate": 70, "advanced": 100},
            "expert": {"beginner": 30, "intermediate": 60, "advanced": 100}
        }
        
        course_difficulty = course.get("difficulty", "intermediate")
        difficulty_score = difficulty_match.get(experience_level, {}).get(course_difficulty, 70)
        
        # Skill name matching
        skill_match = 100 if skill.lower() in course["title"].lower() else 80
        
        return (difficulty_score * 0.7) + (skill_match * 0.3)
    
    def _calculate_learning_style_match(self, course: Dict[str, Any], learning_style: str) -> float:
        """Calculate learning style match score."""
        course_format = course.get("format", "mixed")
        
        format_style_match = {
            "video_interactive": {"visual": 90, "auditory": 80, "kinesthetic": 85, "reading": 60, "mixed": 85},
            "academic": {"visual": 70, "auditory": 60, "kinesthetic": 50, "reading": 95, "mixed": 70},
            "intensive": {"visual": 80, "auditory": 85, "kinesthetic": 95, "reading": 70, "mixed": 85},
            "text_based": {"visual": 50, "auditory": 40, "kinesthetic": 30, "reading": 100, "mixed": 60}
        }
        
        return format_style_match.get(course_format, {}).get(learning_style, 70)
    
    def _diversify_course_selection(self, courses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Diversify course selection by provider and format."""
        # Group by provider and format
        providers = {}
        formats = {}
        
        for course in courses:
            provider = course.get("provider", "Unknown")
            format_type = course.get("format", "mixed")
            
            if provider not in providers:
                providers[provider] = []
            providers[provider].append(course)
            
            if format_type not in formats:
                formats[format_type] = []
            formats[format_type].append(course)
        
        # Select diverse courses
        diversified = []
        used_providers = set()
        used_formats = set()
        
        # First pass: select best course from each provider/format
        for course in sorted(courses, key=lambda x: x["total_score"], reverse=True):
            provider = course.get("provider", "Unknown")
            format_type = course.get("format", "mixed")
            
            if len(diversified) < 8 and (provider not in used_providers or format_type not in used_formats):
                diversified.append(course)
                used_providers.add(provider)
                used_formats.add(format_type)
        
        # Second pass: fill remaining slots with highest scoring courses
        for course in sorted(courses, key=lambda x: x["total_score"], reverse=True):
            if len(diversified) < 10 and course not in diversified:
                diversified.append(course)
        
        return diversified
    
    def _categorize_courses(self, courses: List[Dict[str, Any]]) -> Dict[str, int]:
        """Categorize courses by type."""
        categories = {"beginner": 0, "intermediate": 0, "advanced": 0, "certification": 0, "hands_on": 0}
        
        for course in courses:
            difficulty = course.get("difficulty", "intermediate")
            if difficulty in categories:
                categories[difficulty] += 1
            
            if course.get("certification", False):
                categories["certification"] += 1
            
            if course.get("hands_on_projects", 0) > 5:
                categories["hands_on"] += 1
        
        return categories
    
    def _generate_learning_ai_summary(self, user_data: Dict[str, Any], skill_analysis: Dict[str, Any], learning_path: Dict[str, Any], path_metrics: Dict[str, Any]) -> str:
        """Generate AI-powered learning summary."""
        target_skills = skill_analysis["target_skills"]
        learning_readiness = skill_analysis["learning_readiness"]
        success_probability = path_metrics.get("success_probability", 75)
        
        summary_parts = []
        
        # Learning readiness assessment
        readiness_level = learning_readiness["readiness_level"]
        if readiness_level == "highly_ready":
            summary_parts.append("Your learning profile indicates exceptional readiness for advanced skill acquisition.")
        elif readiness_level == "ready":
            summary_parts.append("You demonstrate strong learning readiness with optimal conditions for skill development.")
        else:
            summary_parts.append("Your learning foundation is solid with opportunities for optimization before beginning intensive study.")
        
        # Skill portfolio impact
        if len(target_skills) > 3:
            summary_parts.append(f"The {len(target_skills)} target skills will create a comprehensive, market-aligned skill portfolio.")
        else:
            summary_parts.append(f"Focused development in {len(target_skills)} high-impact skills for maximum career acceleration.")
        
        # Success prediction
        if success_probability > 80:
            summary_parts.append("AI analysis predicts high probability of successful completion with significant career impact.")
        elif success_probability > 65:
            summary_parts.append("Strong success indicators with recommended optimization strategies for maximum effectiveness.")
        else:
            summary_parts.append("Moderate success probability - consider foundational preparation for optimal outcomes.")
        
        # Timeline and commitment
        total_weeks = path_metrics.get("total_weeks", 16)
        summary_parts.append(f"Structured {total_weeks}-week learning journey with adaptive milestones and continuous progress optimization.")
        
        return " ".join(summary_parts)
    
    # Additional helper methods for completeness
    async def _create_learning_dependency_graph(self, skills: List[str]) -> Dict[str, List[str]]:
        """Create learning dependency graph."""
        graph = {}
        for skill in skills:
            skill_data = self._find_skill_data(skill)
            if skill_data:
                graph[skill] = skill_data.get("prerequisites", [])
        return graph
    
    async def _optimize_learning_sequence(self, graph: Dict[str, List[str]], gaps: Dict[str, Any], user_data: Dict[str, Any]) -> List[str]:
        """Optimize learning sequence using topological sort."""
        # Simple topological sort implementation
        in_degree = {skill: 0 for skill in graph}
        for skill in graph:
            for prereq in graph[skill]:
                if prereq in in_degree:
                    in_degree[skill] += 1
        
        queue = [skill for skill, degree in in_degree.items() if degree == 0]
        sequence = []
        
        while queue:
            # Sort by priority within same dependency level
            queue.sort(key=lambda x: gaps.get("all_gaps", [{}])[0].get("priority", 0) if gaps.get("all_gaps") else 0, reverse=True)
            current = queue.pop(0)
            sequence.append(current)
            
            for skill in graph:
                if current in graph[skill]:
                    in_degree[skill] -= 1
                    if in_degree[skill] == 0:
                        queue.append(skill)
        
        return sequence
    
    def _calculate_coaching_confidence(self, readiness: Dict[str, Any], metrics: Dict[str, Any]) -> float:
        """Calculate coaching confidence score."""
        readiness_score = readiness.get("overall_readiness", 70)
        success_prob = metrics.get("success_probability", 70)
        
        return (readiness_score * 0.6) + (success_prob * 0.4)
    
    def _identify_success_predictors(self, user_data: Dict[str, Any], skill_analysis: Dict[str, Any]) -> List[str]:
        """Identify key success predictors."""
        predictors = []
        
        experience = self._safe_int(user_data.get("experience_years", 0))
        if experience >= 3:
            predictors.append("Strong professional experience foundation")
        
        readiness = skill_analysis.get("learning_readiness", {}).get("overall_readiness", 0)
        if readiness > 80:
            predictors.append("High learning readiness and motivation")
        
        skill_count = len(skill_analysis.get("current_skills", []))
        if skill_count >= 3:
            predictors.append("Diverse existing skill portfolio")
        
        return predictors