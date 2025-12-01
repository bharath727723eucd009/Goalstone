from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from datetime import datetime, timedelta
import uvicorn
import hashlib
import jwt
import json
import os
import asyncio
from typing import Optional, List, Dict, Any

app = FastAPI(title="AI Life Goal Management System")
security = HTTPBearer()

# JWT Configuration
SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: str
    name: str
    email: str

class AgentRequest(BaseModel):
    user_data: dict
    task_type: str = "general"
    parameters: dict = {}

class CareerTask(BaseModel):
    id: str
    title: str
    description: str
    phase: str
    week_or_deadline: str
    category: str
    status: str = "pending"
    resources: list

class CareerPlanRequest(BaseModel):
    roadmap: dict

class CareerUpdateRequest(BaseModel):
    completed_tasks: list
    feedback: str = ""

class ParallelAgentRequest(BaseModel):
    user_goals: List[str]
    user_data: Dict[str, Any]
    task_types: Dict[str, str] = {"career": "milestone_analysis", "wellness": "milestone_analysis", "learning": "milestone_analysis"}
    parameters: Dict[str, Any] = {}

class ParallelAgentResponse(BaseModel):
    status: str
    results: Dict[str, Dict[str, Any]] = {}
    execution_time: float
    errors: Dict[str, str] = {}

class GoalRequest(BaseModel):
    title: str
    description: str = ""
    category: str = "general"
    due_date: Optional[str] = None

class Goal(BaseModel):
    id: str
    user_id: str
    title: str
    description: str
    status: str = "pending"  # pending, in_progress, completed
    category: str = "general"
    created_at: str
    due_date: Optional[str] = None

class RoadmapProgressRequest(BaseModel):
    task_id: str
    completed: bool

# JWT token functions
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None

# Password hashing
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    return hashlib.sha256(password.encode()).hexdigest() == hashed

# Get current user dependency
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Find user in database
    user = None
    for email, user_data in users_db.items():
        if user_data["id"] == user_id:
            user = user_data
            break
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user_id

# Persistent storage file paths
USERS_DB_FILE = "users_db.json"
CAREER_PLANS_DB_FILE = "career_plans_db.json"
USER_GOALS_DB_FILE = "user_goals_db.json"
USER_AGENT_OUTPUTS_DB_FILE = "user_agent_outputs_db.json"
GOALS_DB_FILE = "goals_db.json"
CAREER_PROGRESS_DB_FILE = "career_progress_db.json"
COURSE_PROGRESS_DB_FILE = "course_progress_db.json"

# Load data from files
def load_db(file_path, default_data):
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except:
            return default_data
    return default_data

# Save data to files
def save_db(file_path, data):
    try:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Error saving {file_path}: {e}")

# Initialize databases with persistent storage
users_db = load_db(USERS_DB_FILE, {
    "demo@example.com": {
        "id": "demo_user",
        "name": "Demo User", 
        "email": "demo@example.com",
        "password_hash": hash_password("demo123"),
        "created_at": datetime.now().isoformat()
    }
})

career_plans_db = load_db(CAREER_PLANS_DB_FILE, {})
user_goals_db = load_db(USER_GOALS_DB_FILE, {})
user_agent_outputs_db = load_db(USER_AGENT_OUTPUTS_DB_FILE, {})
goals_db = load_db(GOALS_DB_FILE, [])
career_progress_db = load_db(CAREER_PROGRESS_DB_FILE, {})
course_progress_db = load_db(COURSE_PROGRESS_DB_FILE, {})

@app.post("/api/v1/auth/register")
async def register(request: RegisterRequest):
    try:
        print(f"Registration attempt: {request.email}")
        
        # Validate input
        if not request.email or not request.password or not request.name:
            raise HTTPException(status_code=400, detail="All fields are required")
        
        # Check if user already exists
        if request.email in users_db:
            print(f"User already exists: {request.email}")
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Create new user
        user_id = hashlib.md5(request.email.encode()).hexdigest()[:12]
        password_hash = hash_password(request.password)
        
        users_db[request.email] = {
            "id": user_id,
            "name": request.name,
            "email": request.email,
            "password_hash": password_hash,
            "created_at": datetime.now().isoformat()
        }
        
        # Save to persistent storage
        save_db(USERS_DB_FILE, users_db)
        
        print(f"User registered successfully: {request.email}")
        print(f"Total users in database: {len(users_db)}")
        
        response_data = {
            "message": "User registered successfully",
            "user": {
                "id": user_id,
                "name": request.name,
                "email": request.email
            }
        }
        print(f"Returning response: {response_data}")
        return response_data
    except HTTPException:
        raise
    except Exception as e:
        print(f"Registration error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error during registration")

@app.post("/api/v1/auth/login")
async def login(request: LoginRequest):
    print(f"Login attempt: {request.email}")
    
    # Find user in database
    user = users_db.get(request.email)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Verify password
    if not verify_password(request.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Create JWT token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["id"], "email": user["email"]}, 
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user["id"],
            "email": user["email"],
            "name": user["name"]
        }
    }

@app.get("/api/v1/auth/me")
async def get_current_user_info(current_user_id: str = Depends(get_current_user)):
    # Find user data
    user = None
    for email, user_data in users_db.items():
        if user_data["id"] == current_user_id:
            user = user_data
            break
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "id": user["id"],
        "email": user["email"],
        "name": user["name"]
    }

@app.get("/api/v1/user/stats")
async def get_stats(current_user_id: str = Depends(get_current_user)):
    # Get user-specific goals
    user_goals = [g for g in goals_db if g.get("user_id") == current_user_id]
    
    total = len(user_goals)
    completed = len([g for g in user_goals if g.get("status") == "completed"])
    in_progress = len([g for g in user_goals if g.get("status") == "in_progress"])
    
    completion_rate = int((completed / total * 100)) if total > 0 else 0
    
    return {
        "total_milestones": total,
        "completed_milestones": completed,
        "active_goals": in_progress,
        "completion_rate": completion_rate
    }

@app.get("/api/v1/user/profile")
async def get_profile(current_user_id: str = Depends(get_current_user)):
    # Find user data
    user = None
    for email, user_data in users_db.items():
        if user_data["id"] == current_user_id:
            user = user_data
            break
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "id": user["id"],
        "email": user["email"],
        "name": user["name"]
    }

# Data endpoints
@app.get("/api/v1/data/milestones")
async def get_milestones(current_user_id: str = Depends(get_current_user)):
    return user_goals_db.get(current_user_id, [])

@app.get("/api/v1/data/progress")
async def get_progress(current_user_id: str = Depends(get_current_user)):
    return {"progress": 75}

@app.get("/api/v1/data/agent-outputs")
async def get_agent_outputs(current_user_id: str = Depends(get_current_user)):
    return user_agent_outputs_db.get(current_user_id, [])

# Agent health endpoints
@app.get("/api/v1/agents/career/health")
async def career_health():
    return {"status": "healthy"}

@app.get("/api/v1/agents/finance/health")
async def finance_health():
    return {"status": "healthy"}

@app.get("/api/v1/agents/wellness/health")
async def wellness_health():
    return {"status": "healthy"}

@app.get("/api/v1/agents/learning/health")
async def learning_health():
    return {"status": "healthy"}

# Agent endpoints
async def generate_enhanced_career_block(user_data, user_goals):
    """Generate enhanced career content for parallel agents"""
    skills_input = user_data.get('skills', '')
    experience = int(user_data.get('experience_years', 0))
    location = user_data.get('location', 'Remote')
    current_role = user_data.get('current_role', 'Professional')
    
    current_skills = [s.strip() for s in skills_input.split(',') if s.strip()] if isinstance(skills_input, str) else skills_input
    
    # Determine focus area and seniority
    focus_area = 'backend'
    if any(s.lower() in ['react', 'vue', 'angular', 'frontend', 'css', 'html'] for s in current_skills):
        focus_area = 'frontend'
    elif any(s.lower() in ['data', 'ml', 'python', 'analytics'] for s in current_skills):
        focus_area = 'data'
    elif any(s.lower() in ['aws', 'cloud', 'docker', 'kubernetes'] for s in current_skills):
        focus_area = 'cloud'
    
    seniority = "Junior" if experience <= 2 else "Senior" if experience <= 5 else "Lead"
    
    # Situation summary
    goal_text = ', '.join(user_goals[:2]) if user_goals else 'advance their career'
    situation_summary = f"With {experience} years of experience as a {current_role} in {location}, you're positioned to {goal_text}. Your {focus_area} expertise in {', '.join(current_skills[:3])} provides a strong foundation for {seniority.lower()}-level opportunities."
    
    # Target roles (limit to 2-3)
    target_roles = [
        {"title": f"{seniority} {focus_area.title()} Engineer", "why_fit": f"Your {experience}+ years with {', '.join(current_skills[:2])} aligns perfectly with {focus_area} engineering roles"},
        {"title": f"{focus_area.title()} Team Lead" if experience > 3 else f"{focus_area.title()} Developer", "why_fit": f"Natural progression from your current {current_role} background with leadership potential" if experience > 3 else f"Direct application of your {focus_area} skills in a development role"}
    ]
    
    if experience > 5:
        target_roles.append({"title": "Engineering Manager", "why_fit": "Leadership role leveraging your technical expertise and team management skills"})
    
    # Strategic roadmap summary (limit to 3-4 items)
    if experience <= 2:
        roadmap_summary = [
            f"Master advanced {focus_area} patterns and best practices",
            f"Build 2-3 portfolio projects showcasing {', '.join(current_skills[:2])}",
            f"Network with {focus_area} professionals in {location}"
        ]
    else:
        roadmap_summary = [
            f"Lead {focus_area} architecture decisions and mentor junior developers",
            f"Contribute to open source projects in {focus_area} ecosystem",
            f"Obtain relevant certifications in {', '.join(current_skills[:2])}",
            f"Build strategic partnerships within {location} tech community"
        ]
    
    # Key skills to strengthen (limit to 4 items)
    if experience <= 2:
        key_skills = [
            f"Advanced {focus_area} frameworks and libraries",
            "Version control and collaborative development",
            "Testing and debugging methodologies",
            "Problem-solving and algorithmic thinking"
        ]
    else:
        key_skills = [
            f"System architecture and {focus_area} design patterns",
            "Technical leadership and mentoring abilities",
            "Performance optimization and scalability",
            "Cross-functional collaboration and communication"
        ]
    
    return {
        "situation_summary": situation_summary,
        "target_roles": target_roles,
        "key_skills": key_skills,
        "roadmap_summary": roadmap_summary
    }

async def generate_enhanced_wellness_block(user_data, user_goals):
    """Generate enhanced wellness content for parallel agents"""
    age = int(user_data.get('age', 30))
    activity_level = user_data.get('activity_level', 'moderate')
    
    # Health assessment
    wellness_goals = [g for g in user_goals if any(term in g.lower() for term in ['weight', 'fitness', 'health', 'exercise'])]
    goal_focus = 'general fitness' if not wellness_goals else wellness_goals[0].lower()
    
    if 'weight loss' in goal_focus or 'lose weight' in goal_focus:
        assessment = f"At {age} years old with {activity_level} activity level, your focus on weight loss requires a balanced approach combining cardio and strength training. Your age group typically responds well to consistent, moderate-intensity workouts with proper nutrition timing."
        target_calories = 1800 if age < 40 else 1700
    elif 'muscle' in goal_focus or 'strength' in goal_focus:
        assessment = f"Your {activity_level} activity level at age {age} positions you well for muscle building. Focus on progressive overload and adequate protein intake to maximize strength gains during this optimal training period."
        target_calories = 2200 if age < 40 else 2000
    else:
        assessment = f"With {activity_level} activity levels at {age}, maintaining overall wellness through balanced exercise and nutrition will support long-term health and energy levels for your professional goals."
        target_calories = 2000 if age < 40 else 1900
    
    # Health metrics (limit to 3 key metrics)
    health_metrics = {
        "status": "Good" if activity_level != 'low' else "Needs Improvement",
        "target_calories": target_calories,
        "bmi_range": "18.5-24.9 (optimal)" if age < 40 else "20-25 (healthy aging)"
    }
    
    # Weekly plan based on goals (limit to 4-5 core activities)
    if 'weight loss' in goal_focus:
        weekly_plan = [
            "HIIT cardio sessions (3x/week) for fat burning",
            "Strength training (2x/week) to preserve muscle",
            "Active recovery with walking or yoga",
            "Meal prep and hydration focus"
        ]
    elif 'muscle' in goal_focus:
        weekly_plan = [
            "Heavy compound lifts (3x/week) - squats, deadlifts, bench",
            "Isolation exercises (2x/week) for targeted growth",
            "Progressive overload tracking",
            "High protein intake and recovery focus"
        ]
    else:
        weekly_plan = [
            "Balanced cardio and strength (4x/week)",
            "Flexibility and mobility work (2x/week)",
            "Outdoor activities for variety",
            "Consistent sleep and nutrition habits"
        ]
    
    return {
        "assessment": assessment,
        "health_metrics": health_metrics,
        "weekly_plan": weekly_plan
    }

async def generate_enhanced_learning_block(user_data, user_goals):
    """Generate enhanced learning content for parallel agents"""
    skills_input = user_data.get('skills', '')
    experience = int(user_data.get('experience_years', 0))
    current_role = user_data.get('current_role', 'Developer')
    
    current_skills = [s.strip() for s in skills_input.split(',') if s.strip()] if isinstance(skills_input, str) else skills_input
    
    # Determine target stack from goals and skills
    learning_goals = [g for g in user_goals if any(term in g.lower() for term in ['learn', 'master', 'skill', 'technology'])]
    target_stack = ', '.join(current_skills[:3]) if current_skills else 'full-stack development'
    
    # Profile summary
    if experience <= 1:
        profile_summary = f"As a {current_role} beginning your journey with {target_stack}, you're building foundational skills that will serve as the cornerstone of your technical career. Your learning path should focus on mastering core concepts before advancing to specialized frameworks."
    elif experience <= 3:
        profile_summary = f"With {experience} years as a {current_role} working with {target_stack}, you're ready to deepen your expertise and expand into complementary technologies. This is the ideal time to specialize while maintaining breadth."
    else:
        profile_summary = f"As an experienced {current_role} with {experience} years using {target_stack}, your learning focus should shift toward architecture, leadership, and cutting-edge technologies that will position you for senior technical roles."
    
    # Learning phases based on experience (limit to 2-3 phases)
    if experience <= 1:
        learning_phases = [
            {"name": "Foundation", "duration": "2-3 months", "focus": "Core programming concepts and development environment"},
            {"name": "Application", "duration": "3-4 months", "focus": "Building real projects and understanding workflows"}
        ]
    elif experience <= 3:
        learning_phases = [
            {"name": "Skill Expansion", "duration": "2-3 months", "focus": "Broadening technical skills and learning new frameworks"},
            {"name": "Architecture", "duration": "3-4 months", "focus": "System design and scalable application development"}
        ]
    else:
        learning_phases = [
            {"name": "Innovation", "duration": "2-3 months", "focus": "Exploring emerging technologies and industry trends"},
            {"name": "Strategy", "duration": "3-4 months", "focus": "Technical strategy and organizational impact"},
            {"name": "Leadership", "duration": "Ongoing", "focus": "Industry contribution and knowledge sharing"}
        ]
    
    # Curated courses based on current skills and experience
    focus_area = 'backend'
    if any(s.lower() in ['react', 'vue', 'angular', 'frontend'] for s in current_skills):
        focus_area = 'frontend'
    elif any(s.lower() in ['data', 'ml', 'python'] for s in current_skills):
        focus_area = 'data'
    elif any(s.lower() in ['aws', 'cloud', 'docker'] for s in current_skills):
        focus_area = 'cloud'
    
    # Curated courses (exactly 3 recommendations)
    if focus_area == 'frontend':
        courses = [
            {"title": "React Complete Guide", "platform": "Udemy", "why_relevant": "Comprehensive React skills for modern frontend development"},
            {"title": "JavaScript ES6+ Features", "platform": "freeCodeCamp", "why_relevant": "Essential modern JavaScript concepts and patterns"},
            {"title": "CSS Grid & Flexbox", "platform": "CSS-Tricks", "why_relevant": "Professional layout techniques for responsive design"}
        ]
    elif focus_area == 'data':
        courses = [
            {"title": "Python for Data Science", "platform": "Coursera", "why_relevant": "Core data analysis and visualization skills"},
            {"title": "Machine Learning Fundamentals", "platform": "edX", "why_relevant": "Essential ML concepts for data professionals"},
            {"title": "SQL for Data Analysis", "platform": "DataCamp", "why_relevant": "Advanced database querying and optimization"}
        ]
    elif focus_area == 'cloud':
        courses = [
            {"title": "AWS Solutions Architect", "platform": "A Cloud Guru", "why_relevant": "Comprehensive cloud architecture and services"},
            {"title": "Docker & Kubernetes", "platform": "Udemy", "why_relevant": "Container orchestration for modern deployments"},
            {"title": "Infrastructure as Code", "platform": "HashiCorp Learn", "why_relevant": "Terraform and automated infrastructure management"}
        ]
    else:
        courses = [
            {"title": "System Design Interview", "platform": "Educative", "why_relevant": "Scalable architecture patterns and best practices"},
            {"title": "Full Stack Development", "platform": "Coursera", "why_relevant": "End-to-end application development skills"},
            {"title": "Git & DevOps Fundamentals", "platform": "Pluralsight", "why_relevant": "Essential collaboration and deployment workflows"}
        ]
    
    return {
        "profile_summary": profile_summary,
        "learning_phases": learning_phases,
        "courses": courses
    }

@app.post("/api/v1/agents/career")
async def career_agent(request: dict, current_user_id: str = Depends(get_current_user)):
    user_data = request.get('user_data', {})
    task_type = request.get('task_type', 'general')
    
    # Extract dynamic inputs
    skills_input = user_data.get('skills', '')
    experience = int(user_data.get('experience_years', 0))
    location = user_data.get('location', 'Remote')
    career_goal = user_data.get('goal', '')
    
    # Parse skills
    if isinstance(skills_input, str):
        current_skills = [s.strip() for s in skills_input.split(',') if s.strip()]
    else:
        current_skills = skills_input
    
    # Job Search Strategy specific logic
    if task_type == 'job_search':
        return await generate_job_search_strategy(current_skills, experience, location, career_goal)
    
    # Skill Development specific logic
    if task_type == 'skill_development':
        return await generate_skill_development_plan(user_data)
    
    # Continue with general career guidance logic
    
    # Dynamic skill recommendations based on current skills and goals
    all_tech_skills = {
        'frontend': ['React', 'Vue.js', 'Angular', 'TypeScript', 'CSS', 'HTML'],
        'backend': ['Node.js', 'Python', 'Java', 'Go', 'PostgreSQL', 'MongoDB'],
        'cloud': ['AWS', 'Azure', 'Docker', 'Kubernetes', 'Terraform'],
        'data': ['Python', 'SQL', 'Pandas', 'Machine Learning', 'Tableau', 'Spark'],
        'mobile': ['React Native', 'Flutter', 'Swift', 'Kotlin']
    }
    
    # Determine focus area from skills and goal
    focus_area = 'backend'  # default
    frontend_skills = ['react', 'vue', 'angular', 'frontend', 'html', 'css', 'javascript', 'tailwind', 'bootstrap', 'sass', 'scss', 'ui', 'ux']
    data_skills = ['data', 'ml', 'analytics', 'python', 'pandas', 'numpy', 'tensorflow', 'pytorch', 'sklearn', 'tableau', 'powerbi']
    cloud_skills = ['aws', 'cloud', 'docker', 'kubernetes', 'azure', 'gcp', 'devops', 'terraform', 'jenkins']
    
    if any(s.lower() in frontend_skills for s in current_skills):
        focus_area = 'frontend'
    elif any(s.lower() in data_skills for s in current_skills):
        focus_area = 'data'
    elif any(s.lower() in cloud_skills for s in current_skills):
        focus_area = 'cloud'
    elif 'mobile' in career_goal.lower():
        focus_area = 'mobile'
    
    # Priority skills based on focus area, excluding current skills
    available_skills = [s for s in all_tech_skills[focus_area] if s.lower() not in [cs.lower() for cs in current_skills]]
    priority_skills = available_skills[:4]
    
    # Dynamic role recommendations with seniority levels
    seniority = "Junior" if experience <= 2 else "Senior" if experience <= 5 else "Lead"
    
    role_map = {
        'frontend': [
            {"title": f"{seniority} Frontend Developer", "description": f"Build responsive web applications in {location} using React/Vue", "seniority_level": seniority},
            {"title": "UI/UX Engineer", "description": "Bridge design and development with user-centered interfaces", "seniority_level": seniority}
        ],
        'backend': [
            {"title": f"{seniority} Backend Engineer", "description": f"Develop scalable APIs and services for {location} companies", "seniority_level": seniority},
            {"title": "DevOps Engineer", "description": "Automate deployment pipelines and manage cloud infrastructure", "seniority_level": seniority}
        ],
        'data': [
            {"title": f"{seniority} Data Engineer", "description": f"Build data pipelines and analytics for {location} enterprises", "seniority_level": seniority},
            {"title": "ML Engineer", "description": "Deploy machine learning models in production systems", "seniority_level": seniority}
        ],
        'cloud': [
            {"title": f"{seniority} Cloud Engineer", "description": f"Design cloud architecture for {location} organizations", "seniority_level": seniority},
            {"title": "Site Reliability Engineer", "description": "Ensure system reliability and performance at scale", "seniority_level": seniority}
        ],
        'mobile': [
            {"title": f"{seniority} Mobile Developer", "description": f"Create native and cross-platform apps for {location} market", "seniority_level": seniority},
            {"title": "Mobile Product Engineer", "description": "Lead mobile product development and user experience", "seniority_level": seniority}
        ]
    }
    
    recommended_roles = role_map[focus_area]
    if experience > 5:
        recommended_roles.append({"title": "Engineering Manager", "description": "Lead technical teams and drive product development", "seniority_level": "Management"})
    
    # Dynamic roadmap based on all inputs
    foundation_tasks = [
        {
            "id": f"f1_{focus_area}_{experience}_{len(current_skills)}",
            "title": f"Master {priority_skills[0] if priority_skills else 'Core Technologies'}",
            "explanation": f"Deep dive into {priority_skills[0] if priority_skills else 'essential technologies'} through hands-on projects. Focus on {focus_area} fundamentals for {seniority.lower()} level.",
            "timeframe": "Week 1-2" if experience <= 2 else "Week 1"
        },
        {
            "id": f"f2_{focus_area}_{experience}_{len(current_skills)}",
            "title": f"Build {focus_area.title()} Portfolio for {location}",
            "explanation": f"Create {2 if experience <= 2 else 3}-{3 if experience <= 2 else 5} impressive {focus_area} projects targeting {location} market requirements and showcasing {', '.join(priority_skills[:2]) if priority_skills else 'key skills'}.",
            "timeframe": "Week 2-4" if experience <= 2 else "Week 2-3"
        },
        {
            "id": f"f3_{focus_area}_{experience}_{len(current_skills)}",
            "title": f"Professional Network in {location}",
            "explanation": f"Connect with {focus_area} professionals in {location}. {'Join junior developer groups and find mentors' if experience <= 2 else 'Attend senior-level meetups and industry conferences'}.",
            "timeframe": "Week 1-6"
        },
        {
            "id": f"f4_{focus_area}_{experience}_{len(current_skills)}",
            "title": f"{seniority} Skills Assessment",
            "explanation": f"Evaluate current {focus_area} abilities against {seniority.lower()} role requirements. {'Focus on fundamentals' if experience <= 2 else 'Identify leadership and architecture gaps'}.",
            "timeframe": "Week 1"
        }
    ]
    
    advancement_tasks = [
        {
            "id": f"a1_{focus_area}_{experience}_{len(current_skills)}",
            "title": f"Advanced {priority_skills[1] if len(priority_skills) > 1 else 'Architecture'}",
            "explanation": f"Master {priority_skills[1] if len(priority_skills) > 1 else 'system design'} for {focus_area}. {'Learn intermediate patterns' if experience <= 2 else 'Design scalable architectures and mentor others'}.",
            "timeframe": "Month 2-3" if experience <= 2 else "Month 2"
        },
        {
            "id": f"a2_{focus_area}_{experience}_{len(current_skills)}",
            "title": f"{'Team Collaboration' if experience <= 2 else 'Leadership & Mentoring'}",
            "explanation": f"{'Learn to work effectively in teams and communicate technical concepts' if experience <= 2 else 'Lead technical teams, mentor junior developers, and drive architectural decisions'}.",
            "timeframe": "Month 2-4"
        },
        {
            "id": f"a3_{focus_area}_{experience}_{len(current_skills)}",
            "title": f"{focus_area.title()} Certification",
            "explanation": f"Obtain {'foundational' if experience <= 2 else 'advanced'} certification in {focus_area} technologies. Target {location} market requirements.",
            "timeframe": "Month 3-4"
        },
        {
            "id": f"a4_{focus_area}_{experience}_{len(current_skills)}",
            "title": f"{'Learn from' if experience <= 2 else 'Lead'} Open Source",
            "explanation": f"{'Contribute to beginner-friendly {focus_area} projects to learn best practices' if experience <= 2 else 'Lead or maintain {focus_area} open source projects to establish thought leadership'}.",
            "timeframe": "Month 2-5"
        }
    ]
    
    market_ready_tasks = [
        {
            "id": f"m1_{focus_area}_{experience}_{len(current_skills)}",
            "title": f"Strategic Job Search in {location}",
            "explanation": f"Target {'3-5 entry-level' if experience <= 2 else '5-10 senior'} {focus_area} companies per week in {location}. {'Focus on internships and junior roles' if experience <= 2 else 'Target leadership and architect positions'}.",
            "timeframe": "Month 4-6"
        },
        {
            "id": f"m2_{focus_area}_{experience}_{len(current_skills)}",
            "title": f"{seniority} Interview Preparation",
            "explanation": f"Practice {focus_area}-specific {'coding fundamentals and basic system design' if experience <= 2 else 'advanced system design, leadership scenarios, and technical architecture'}.",
            "timeframe": "Month 4-5"
        },
        {
            "id": f"m3_{focus_area}_{experience}_{len(current_skills)}",
            "title": f"Salary Strategy for {location}",
            "explanation": f"Research {location} market rates for {seniority.lower()} {focus_area} roles. {'Understand entry-level compensation' if experience <= 2 else 'Prepare for senior-level negotiation tactics'}.",
            "timeframe": "Month 5-6"
        },
        {
            "id": f"m4_{focus_area}_{experience}_{len(current_skills)}",
            "title": f"{'Build' if experience <= 2 else 'Establish'} Professional Presence",
            "explanation": f"{'Create technical blog posts and contribute to discussions' if experience <= 2 else 'Speak at {focus_area} conferences and establish thought leadership in {location}'}.",
            "timeframe": "Month 5-6"
        }
    ]
    
    # Diverse course recommendations from multiple platforms
    course_database = {
        'frontend': [
            {"title": "React - The Complete Guide", "platform": "Udemy", "url": "https://www.udemy.com/course/react-the-complete-guide-incl-redux/", "why_relevant": "Master React fundamentals and advanced patterns"},
            {"title": "Vue.js Complete Course", "platform": "Pluralsight", "url": "https://www.pluralsight.com/courses/vuejs-fundamentals", "why_relevant": "Learn progressive Vue.js framework for modern UIs"},
            {"title": "Advanced CSS Grid & Flexbox", "platform": "CSS-Tricks", "url": "https://css-tricks.com/snippets/css/complete-guide-grid/", "why_relevant": "Master modern CSS layout techniques"},
            {"title": "JavaScript ES6+ Features", "platform": "freeCodeCamp", "url": "https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures/", "why_relevant": "Learn modern JavaScript features and best practices"},
            {"title": "Frontend System Design", "platform": "Infosys Springboard", "url": "https://infyspringboard.onwingspan.com/web/en/app/toc/lex_auth_012683854313897984166_shared/overview", "why_relevant": "Scalable frontend architecture patterns"},
            {"title": "Angular Complete Guide", "platform": "Coursera", "url": "https://www.coursera.org/learn/angular", "why_relevant": "Enterprise-grade Angular framework development"}
        ],
        'backend': [
            {"title": "Node.js Microservices", "platform": "Udemy", "url": "https://www.udemy.com/course/microservices-with-node-js-and-react/", "why_relevant": "Build scalable microservices architecture"},
            {"title": "Spring Boot Masterclass", "platform": "Infosys Springboard", "url": "https://infyspringboard.onwingspan.com/web/en/app/toc/lex_auth_012683854313897984167_shared/overview", "why_relevant": "Enterprise Java development with Spring"},
            {"title": "Python FastAPI Development", "platform": "TestDriven.io", "url": "https://testdriven.io/courses/tdd-fastapi/", "why_relevant": "Modern Python API development with FastAPI"},
            {"title": "Database Design Patterns", "platform": "Pluralsight", "url": "https://www.pluralsight.com/courses/database-design-patterns", "why_relevant": "Advanced database architecture and optimization"},
            {"title": "Go Programming Language", "platform": "Coursera", "url": "https://www.coursera.org/specializations/google-golang", "why_relevant": "High-performance backend development with Go"},
            {"title": "GraphQL API Design", "platform": "Apollo GraphQL", "url": "https://www.apollographql.com/tutorials/", "why_relevant": "Modern API development with GraphQL"}
        ],
        'data': [
            {"title": "Machine Learning Specialization", "platform": "Coursera", "url": "https://www.coursera.org/specializations/machine-learning-introduction", "why_relevant": "Andrew Ng's updated ML course with Python"},
            {"title": "Data Engineering with Apache Spark", "platform": "Databricks Academy", "url": "https://www.databricks.com/learn/training/lakehouse-fundamentals", "why_relevant": "Big data processing and analytics"},
            {"title": "Deep Learning with TensorFlow", "platform": "edX", "url": "https://www.edx.org/course/introduction-to-tensorflow-for-artificial-intelligence", "why_relevant": "Neural networks and deep learning implementation"},
            {"title": "Data Science with R", "platform": "DataCamp", "url": "https://www.datacamp.com/tracks/data-scientist-with-r", "why_relevant": "Statistical analysis and data visualization"},
            {"title": "MLOps Engineering", "platform": "Infosys Springboard", "url": "https://infyspringboard.onwingspan.com/web/en/app/toc/lex_auth_012683854313897984168_shared/overview", "why_relevant": "Production ML pipeline development"},
            {"title": "Advanced SQL Analytics", "platform": "Mode Analytics", "url": "https://mode.com/sql-tutorial/", "why_relevant": "Complex SQL queries and window functions"}
        ],
        'cloud': [
            {"title": "AWS Solutions Architect", "platform": "A Cloud Guru", "url": "https://acloudguru.com/course/aws-certified-solutions-architect-associate-saa-c03", "why_relevant": "Comprehensive AWS cloud architecture"},
            {"title": "Azure DevOps Engineer", "platform": "Microsoft Learn", "url": "https://docs.microsoft.com/en-us/learn/certifications/devops-engineer/", "why_relevant": "CI/CD pipelines and Azure infrastructure"},
            {"title": "Kubernetes Administration", "platform": "Linux Foundation", "url": "https://training.linuxfoundation.org/training/kubernetes-fundamentals/", "why_relevant": "Container orchestration and management"},
            {"title": "Terraform Infrastructure", "platform": "HashiCorp Learn", "url": "https://learn.hashicorp.com/terraform", "why_relevant": "Infrastructure as Code best practices"},
            {"title": "Google Cloud Architect", "platform": "Google Cloud", "url": "https://cloud.google.com/training/cloud-infrastructure", "why_relevant": "GCP services and cloud-native architecture"},
            {"title": "Cloud Security Fundamentals", "platform": "Infosys Springboard", "url": "https://infyspringboard.onwingspan.com/web/en/app/toc/lex_auth_012683854313897984169_shared/overview", "why_relevant": "Enterprise cloud security practices"}
        ],
        'mobile': [
            {"title": "React Native Advanced", "platform": "Expo", "url": "https://docs.expo.dev/tutorial/introduction/", "why_relevant": "Cross-platform mobile development"},
            {"title": "iOS SwiftUI Development", "platform": "Apple Developer", "url": "https://developer.apple.com/tutorials/swiftui", "why_relevant": "Modern iOS app development with SwiftUI"},
            {"title": "Android Jetpack Compose", "platform": "Android Developers", "url": "https://developer.android.com/courses/jetpack-compose/course", "why_relevant": "Modern Android UI development"},
            {"title": "Flutter Production Apps", "platform": "Flutter", "url": "https://flutter.dev/learn", "why_relevant": "Production-ready Flutter applications"},
            {"title": "Mobile App Security", "platform": "OWASP", "url": "https://owasp.org/www-project-mobile-security/", "why_relevant": "Security best practices for mobile apps"},
            {"title": "Cross-Platform Development", "platform": "Xamarin", "url": "https://dotnet.microsoft.com/en-us/learn/xamarin", "why_relevant": "Microsoft's cross-platform mobile solution"}
        ]
    }
    
    # Dynamic course selection based on inputs
    recommended_courses = []
    
    # Primary courses based on focus area
    base_courses = course_database[focus_area][:3]
    recommended_courses.extend(base_courses)
    
    # Add experience-level and skill-specific courses
    if experience <= 2:  # Junior level
        if focus_area == 'frontend':
            recommended_courses.append({"title": "JavaScript Fundamentals", "platform": "freeCodeCamp", "url": "https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures/", "why_relevant": "Build strong JavaScript foundation for junior frontend roles"})
        elif focus_area == 'backend':
            recommended_courses.append({"title": "REST API Design", "platform": "Coursera", "url": "https://www.coursera.org/learn/rest-api", "why_relevant": "Essential API skills for junior backend developers"})
    else:  # Senior level
        if focus_area == 'frontend':
            recommended_courses.append({"title": "Advanced React Patterns", "platform": "Frontend Masters", "url": "https://frontendmasters.com/courses/advanced-react-patterns/", "why_relevant": "Senior-level React architecture and design patterns"})
        elif focus_area == 'backend':
            recommended_courses.append({"title": "System Design Interview", "platform": "Educative", "url": "https://www.educative.io/courses/grokking-the-system-design-interview", "why_relevant": "Critical for senior backend engineering interviews"})
    
    # Add skill-specific courses based on current skills
    if any('tailwind' in s.lower() for s in current_skills):
        recommended_courses.append({"title": "Tailwind CSS Masterclass", "platform": "Udemy", "url": "https://www.udemy.com/course/tailwind-css-zero-to-hero/", "why_relevant": "Master utility-first CSS framework for modern frontend development"})
    
    if any('typescript' in s.lower() for s in current_skills) or 'TypeScript' in priority_skills:
        recommended_courses.append({"title": "TypeScript Deep Dive", "platform": "Udemy", "url": "https://www.udemy.com/course/typescript-the-complete-developers-guide/", "why_relevant": f"Advanced TypeScript for {focus_area} development"})
    
    if any('css' in s.lower() for s in current_skills) and focus_area == 'frontend':
        recommended_courses.append({"title": "Advanced CSS & Sass", "platform": "Udemy", "url": "https://www.udemy.com/course/advanced-css-and-sass/", "why_relevant": "Modern CSS techniques and preprocessors"})
    
    if 'AWS' in priority_skills or 'cloud' in career_goal.lower():
        recommended_courses.append({"title": "AWS Solutions Architect", "platform": "AWS", "url": "https://aws.amazon.com/certification/certified-solutions-architect-associate/", "why_relevant": "Cloud skills essential for modern development roles"})
    
    # Location-specific additions
    if 'san francisco' in location.lower() or 'silicon valley' in location.lower():
        recommended_courses.append({"title": "Startup Engineering Culture", "platform": "Coursera", "url": "https://www.coursera.org/learn/startup-engineering", "why_relevant": f"Relevant for {location} startup ecosystem"})
    
    # Ensure even number of courses (6, 8, 10, etc.)
    target_count = 6 if len(recommended_courses) < 6 else len(recommended_courses)
    if target_count % 2 != 0:
        target_count += 1
    
    # Pad with additional relevant courses if needed
    while len(recommended_courses) < target_count:
        if focus_area == 'frontend':
            recommended_courses.append({"title": "Advanced JavaScript Concepts", "platform": "Udemy", "url": "https://www.udemy.com/course/advanced-javascript-concepts/", "why_relevant": "Master closures, prototypes, and async programming"})
        elif focus_area == 'backend':
            recommended_courses.append({"title": "GraphQL Complete Guide", "platform": "Udemy", "url": "https://www.udemy.com/course/graphql-bootcamp/", "why_relevant": "Modern API development with GraphQL"})
        elif focus_area == 'data':
            recommended_courses.append({"title": "Deep Learning Specialization", "platform": "Coursera", "url": "https://www.coursera.org/specializations/deep-learning", "why_relevant": "Advanced neural networks and deep learning"})
        elif focus_area == 'cloud':
            recommended_courses.append({"title": "Kubernetes Administration", "platform": "Linux Academy", "url": "https://linuxacademy.com/course/kubernetes-administration/", "why_relevant": "Container orchestration and management"})
        else:
            recommended_courses.append({"title": "System Design Fundamentals", "platform": "Educative", "url": "https://www.educative.io/courses/system-design-fundamentals", "why_relevant": "Essential system architecture concepts"})
    
    recommended_courses = recommended_courses[:target_count]
    
    return {
        "status": "success",
        "data": {
            "current_skills": current_skills,
            "priority_skills": priority_skills,
            "recommended_roles": recommended_roles,
            "roadmap": {
                "foundation": foundation_tasks,
                "advancement": advancement_tasks,
                "market_ready": market_ready_tasks
            },
            "recommended_courses": recommended_courses
        }
    }

async def generate_job_search_strategy(current_skills, experience, location, career_goal):
    # Determine focus area and seniority
    focus_area = 'backend'
    frontend_skills = ['react', 'vue', 'angular', 'frontend', 'html', 'css', 'javascript', 'tailwind', 'bootstrap', 'sass', 'scss', 'ui', 'ux']
    data_skills = ['data', 'ml', 'analytics', 'python', 'pandas', 'numpy', 'tensorflow', 'pytorch', 'sklearn', 'tableau', 'powerbi']
    cloud_skills = ['aws', 'cloud', 'docker', 'kubernetes', 'azure', 'gcp', 'devops', 'terraform', 'jenkins']
    
    if any(s.lower() in frontend_skills for s in current_skills):
        focus_area = 'frontend'
    elif any(s.lower() in data_skills for s in current_skills):
        focus_area = 'data'
    elif any(s.lower() in cloud_skills for s in current_skills):
        focus_area = 'cloud'
    
    seniority = "Junior" if experience <= 2 else "Senior" if experience <= 5 else "Lead"
    
    # Job search roadmap phases
    profile_tasks = [
        {
            "id": f"js_p1_{focus_area}_{experience}",
            "title": f"Optimize {focus_area.title()} Resume",
            "explanation": f"Tailor resume for {seniority.lower()} {focus_area} roles in {location}. Highlight {', '.join(current_skills[:3])} experience.",
            "timeframe": "Week 1"
        },
        {
            "id": f"js_p2_{focus_area}_{experience}",
            "title": "LinkedIn Profile Enhancement",
            "explanation": f"Update headline, summary, and skills for {focus_area} positions. Add {location} location targeting.",
            "timeframe": "Week 1"
        }
    ]
    
    application_tasks = [
        {
            "id": f"js_a1_{focus_area}_{experience}",
            "title": f"Target {location} Companies",
            "explanation": f"Research and list 20-30 {focus_area} companies in {location}. Focus on {'startups' if experience <= 3 else 'established firms'}.",
            "timeframe": "Week 2-3"
        },
        {
            "id": f"js_a2_{focus_area}_{experience}",
            "title": "Daily Applications",
            "explanation": f"Apply to {'3-5' if experience <= 2 else '5-8'} {focus_area} positions daily. Track applications and responses.",
            "timeframe": "Week 2-6"
        }
    ]
    
    interview_tasks = [
        {
            "id": f"js_i1_{focus_area}_{experience}",
            "title": f"{focus_area.title()} Technical Prep",
            "explanation": f"Practice {focus_area}-specific coding problems and {'system design' if experience > 2 else 'basic algorithms'}.",
            "timeframe": "Week 3-6"
        },
        {
            "id": f"js_i2_{focus_area}_{experience}",
            "title": "Mock Interviews",
            "explanation": f"Schedule {'2-3' if experience <= 2 else '3-5'} mock interviews for {seniority.lower()} {focus_area} roles.",
            "timeframe": "Week 4-6"
        }
    ]
    
    # Location-specific job boards and company links
    job_links = []
    
    # Indian cities
    if any(city in location.lower() for city in ['bangalore', 'bengaluru', 'mumbai', 'delhi', 'chennai', 'hyderabad', 'pune']):
        job_links.extend([
            {"type": "job_board", "title": "Naukri.com", "url": "https://www.naukri.com", "why_relevant": f"Leading job portal in India for {focus_area} roles"},
            {"type": "job_board", "title": "LinkedIn Jobs India", "url": "https://www.linkedin.com/jobs/search/?location=India", "why_relevant": f"Professional network with {focus_area} opportunities in {location}"},
            {"type": "job_board", "title": "Indeed India", "url": "https://www.indeed.co.in", "why_relevant": f"Global job search platform with Indian {focus_area} positions"},
            {"type": "company_careers", "title": "Flipkart Careers", "url": "https://www.flipkartcareers.com", "why_relevant": f"Major Indian e-commerce company hiring {focus_area} talent"},
            {"type": "company_careers", "title": "Wipro Careers", "url": "https://careers.wipro.com", "why_relevant": f"Leading IT services company with {focus_area} opportunities"},
            {"type": "linkedin_profile", "title": "LinkedIn Profile Guide", "url": "https://www.linkedin.com/help/linkedin/answer/a507663", "why_relevant": f"Optimize profile for Indian {focus_area} job market"}
        ])
        
        if 'bangalore' in location.lower() or 'bengaluru' in location.lower():
            job_links.extend([
                {"type": "company_careers", "title": "Infosys Careers", "url": "https://www.infosys.com/careers", "why_relevant": "Bangalore-based IT giant with strong tech hiring"},
                {"type": "job_board", "title": "AngelList Bangalore", "url": "https://angel.co/jobs", "why_relevant": "Startup ecosystem jobs in Bangalore"}
            ])
        elif 'mumbai' in location.lower():
            job_links.extend([
                {"type": "company_careers", "title": "Tata Consultancy Services", "url": "https://www.tcs.com/careers", "why_relevant": "Mumbai headquarters with extensive tech opportunities"},
                {"type": "job_board", "title": "TimesJobs Mumbai", "url": "https://www.timesjobs.com", "why_relevant": "Mumbai-focused job opportunities"}
            ])
        else:
            job_links.extend([
                {"type": "company_careers", "title": "HCL Technologies", "url": "https://www.hcltech.com/careers", "why_relevant": f"Global IT services with {focus_area} roles across India"},
                {"type": "job_board", "title": "Shine.com", "url": "https://www.shine.com", "why_relevant": f"Indian job portal specializing in {focus_area} positions"}
            ])
    
    # US cities
    elif any(city in location.lower() for city in ['san francisco', 'seattle', 'new york', 'austin', 'boston']):
        job_links.extend([
            {"type": "job_board", "title": "Indeed", "url": "https://www.indeed.com", "why_relevant": f"Top US job board for {focus_area} positions"},
            {"type": "job_board", "title": "Glassdoor", "url": "https://www.glassdoor.com/Job/jobs.htm", "why_relevant": f"Job search with salary insights for {focus_area} roles"},
            {"type": "job_board", "title": "LinkedIn Jobs US", "url": "https://www.linkedin.com/jobs", "why_relevant": f"Professional networking for US {focus_area} opportunities"},
            {"type": "company_careers", "title": "Google Careers", "url": "https://careers.google.com", "why_relevant": f"Leading tech company hiring {focus_area} engineers"},
            {"type": "company_careers", "title": "Microsoft Careers", "url": "https://careers.microsoft.com", "why_relevant": f"Global tech leader with diverse {focus_area} roles"},
            {"type": "linkedin_profile", "title": "US Tech Resume Guide", "url": "https://www.linkedin.com/help/linkedin/answer/a507663", "why_relevant": f"Optimize resume for US {focus_area} market"}
        ])
        
        if 'san francisco' in location.lower():
            job_links.extend([
                {"type": "company_careers", "title": "Salesforce Careers", "url": "https://www.salesforce.com/company/careers", "why_relevant": "SF-based cloud leader with strong engineering culture"},
                {"type": "job_board", "title": "AngelList SF", "url": "https://angel.co/jobs", "why_relevant": "Silicon Valley startup opportunities"}
            ])
        elif 'seattle' in location.lower():
            job_links.extend([
                {"type": "company_careers", "title": "Amazon Jobs", "url": "https://www.amazon.jobs", "why_relevant": "Seattle headquarters with massive tech hiring"},
                {"type": "job_board", "title": "Dice Seattle", "url": "https://www.dice.com", "why_relevant": "Tech-focused job board for Seattle market"}
            ])
        else:
            job_links.extend([
                {"type": "company_careers", "title": "Meta Careers", "url": "https://www.metacareers.com", "why_relevant": f"Social media giant hiring {focus_area} talent"},
                {"type": "job_board", "title": "Stack Overflow Jobs", "url": "https://stackoverflow.com/jobs", "why_relevant": f"Developer-focused job board for {focus_area} roles"}
            ])
    
    # Default/Remote
    else:
        job_links.extend([
            {"type": "job_board", "title": "AngelList", "url": "https://angel.co/jobs", "why_relevant": f"Startup jobs platform for {focus_area} roles"},
            {"type": "job_board", "title": "Remote.co", "url": "https://remote.co", "why_relevant": f"Remote-first job board for {focus_area} positions"},
            {"type": "job_board", "title": "We Work Remotely", "url": "https://weworkremotely.com", "why_relevant": f"Largest remote work community for {focus_area} jobs"},
            {"type": "job_board", "title": "FlexJobs", "url": "https://www.flexjobs.com", "why_relevant": f"Curated remote and flexible {focus_area} opportunities"},
            {"type": "company_careers", "title": "GitLab Careers", "url": "https://about.gitlab.com/jobs", "why_relevant": f"All-remote company with {focus_area} positions globally"},
            {"type": "linkedin_profile", "title": "Remote Work Profile Guide", "url": "https://www.linkedin.com/help/linkedin/answer/a507663", "why_relevant": "Optimize profile for remote job search"}
        ])
    
    # Ensure even number (6, 8, 10, etc.)
    target_count = 6 if len(job_links) < 6 else len(job_links)
    if target_count % 2 != 0:
        target_count += 1
    
    # Add focus area specific links to reach target
    while len(job_links) < target_count:
        if focus_area == 'data':
            job_links.append({"type": "job_board", "title": "Kaggle Jobs", "url": "https://www.kaggle.com/jobs", "why_relevant": "Data science and ML job opportunities"})
        elif focus_area == 'frontend':
            job_links.append({"type": "job_board", "title": "Dribbble Jobs", "url": "https://dribbble.com/jobs", "why_relevant": "Design-focused frontend opportunities"})
        elif focus_area == 'cloud':
            job_links.append({"type": "job_board", "title": "AWS Jobs", "url": "https://www.amazon.jobs/en/teams/aws", "why_relevant": "Cloud infrastructure and DevOps roles"})
        else:
            job_links.append({"type": "job_board", "title": "Hired", "url": "https://hired.com", "why_relevant": f"Curated {focus_area} job matching platform"})
    
    job_links = job_links[:target_count]
    
    return {
        "status": "success",
        "data": {
            "current_skills": current_skills,
            "priority_skills": ["Interview Skills", "Networking", "Portfolio", "Communication"],
            "recommended_roles": [
                {"title": f"{seniority} {focus_area.title()} Engineer", "description": f"Target role in {location} market"},
                {"title": f"{focus_area.title()} Developer", "description": f"Alternative title for {focus_area} positions"}
            ],
            "roadmap": {
                "foundation": profile_tasks,
                "advancement": application_tasks,
                "market_ready": interview_tasks
            },
            "recommended_links": job_links
        }
    }

async def generate_skill_development_plan(user_data):
    skill_level = user_data.get('skill_level', 'Beginner')
    target_area = user_data.get('target_area', 'Programming')
    weekly_hours = user_data.get('weekly_hours', '5-8 hrs')
    time_horizon = user_data.get('time_horizon', '3 months')
    technologies = user_data.get('technologies', '')
    
    # Determine focus area from target_area and technologies
    focus_area = 'backend'
    combined_input = f"{target_area} {technologies}".lower()
    
    if any(term in combined_input for term in ['frontend', 'react', 'vue', 'angular', 'ui', 'css', 'html', 'javascript']):
        focus_area = 'frontend'
    elif any(term in combined_input for term in ['data', 'ml', 'analytics', 'science', 'pandas', 'numpy', 'tableau']):
        focus_area = 'data'
    elif any(term in combined_input for term in ['cloud', 'aws', 'azure', 'gcp', 'devops', 'docker', 'kubernetes', 'terraform']):
        focus_area = 'cloud'
    elif any(term in combined_input for term in ['mobile', 'ios', 'android', 'flutter', 'react native', 'swift', 'kotlin']):
        focus_area = 'mobile'
    
    # Generate summary
    summary = f"As a {skill_level.lower()} learner targeting {target_area}, you're planning to dedicate {weekly_hours} per week over {time_horizon}. This focused approach will help you build practical skills and advance your expertise in {focus_area} development."
    
    # Generate phase-based roadmap
    if time_horizon == '1 month':
        phases = ['Weeks 1-2', 'Weeks 3-4']
    elif time_horizon == '3 months':
        phases = ['Weeks 1-2', 'Weeks 3-4', 'Weeks 5-8', 'Weeks 9-12']
    else:  # 6 months
        phases = ['Weeks 1-4', 'Weeks 5-8', 'Weeks 9-16', 'Weeks 17-24']
    
    # Build roadmap based on skill level and focus area
    roadmap_tasks = []
    
    if skill_level == 'Beginner':
        if focus_area == 'frontend':
            roadmap_tasks = [
                {"id": f"sd_f1_{focus_area}", "title": "HTML & CSS Fundamentals", "explanation": f"Master basic web structure and styling. Build 3-5 static pages to practice layout and responsive design.", "timeframe": phases[0]},
                {"id": f"sd_f2_{focus_area}", "title": "JavaScript Basics", "explanation": f"Learn variables, functions, DOM manipulation. Create interactive elements and simple calculators.", "timeframe": phases[1]},
                {"id": f"sd_f3_{focus_area}", "title": "Framework Introduction", "explanation": f"Start with React basics or chosen framework. Build your first component-based application.", "timeframe": phases[2] if len(phases) > 2 else phases[1]},
                {"id": f"sd_f4_{focus_area}", "title": "Project Portfolio", "explanation": f"Create 2-3 complete projects showcasing your {target_area} skills. Deploy to GitHub Pages.", "timeframe": phases[-1]}
            ]
        elif focus_area == 'backend':
            roadmap_tasks = [
                {"id": f"sd_b1_{focus_area}", "title": "Programming Language Basics", "explanation": f"Master fundamentals of your chosen language. Practice with coding exercises and small programs.", "timeframe": phases[0]},
                {"id": f"sd_b2_{focus_area}", "title": "Database Fundamentals", "explanation": f"Learn SQL basics and database design. Practice with simple CRUD operations.", "timeframe": phases[1]},
                {"id": f"sd_b3_{focus_area}", "title": "API Development", "explanation": f"Build REST APIs with your chosen framework. Implement authentication and data validation.", "timeframe": phases[2] if len(phases) > 2 else phases[1]},
                {"id": f"sd_b4_{focus_area}", "title": "Full Stack Project", "explanation": f"Create a complete backend application with database integration and API endpoints.", "timeframe": phases[-1]}
            ]
    else:  # Intermediate/Advanced
        if focus_area == 'frontend':
            roadmap_tasks = [
                {"id": f"sd_af1_{focus_area}", "title": "Advanced Framework Patterns", "explanation": f"Master state management, routing, and performance optimization in your target framework.", "timeframe": phases[0]},
                {"id": f"sd_af2_{focus_area}", "title": "Testing & Quality", "explanation": f"Implement unit testing, integration testing, and code quality tools. Set up CI/CD pipelines.", "timeframe": phases[1]},
                {"id": f"sd_af3_{focus_area}", "title": "Performance Optimization", "explanation": f"Learn bundle optimization, lazy loading, and performance monitoring techniques.", "timeframe": phases[2] if len(phases) > 2 else phases[1]},
                {"id": f"sd_af4_{focus_area}", "title": "Production Deployment", "explanation": f"Deploy scalable applications with proper monitoring, error tracking, and performance analytics.", "timeframe": phases[-1]}
            ]
        elif focus_area == 'backend':
            roadmap_tasks = [
                {"id": f"sd_ab1_{focus_area}", "title": "Architecture Patterns", "explanation": f"Implement microservices, clean architecture, and design patterns for scalable systems.", "timeframe": phases[0]},
                {"id": f"sd_ab2_{focus_area}", "title": "Database Optimization", "explanation": f"Master query optimization, indexing, caching strategies, and database scaling techniques.", "timeframe": phases[1]},
                {"id": f"sd_ab3_{focus_area}", "title": "Security & Performance", "explanation": f"Implement authentication, authorization, rate limiting, and performance monitoring.", "timeframe": phases[2] if len(phases) > 2 else phases[1]},
                {"id": f"sd_ab4_{focus_area}", "title": "Production Systems", "explanation": f"Deploy with containerization, orchestration, and implement monitoring and logging systems.", "timeframe": phases[-1]}
            ]
    
    # Limit to available phases
    roadmap_tasks = roadmap_tasks[:len(phases)]
    
    # Comprehensive learning resource database
    skill_resources = {
        'frontend_beginner': [
            {"title": "freeCodeCamp Web Development", "platform": "freeCodeCamp", "url": "https://www.freecodecamp.org/learn/responsive-web-design/", "why_relevant": "Free, comprehensive HTML/CSS curriculum with hands-on projects"},
            {"title": "JavaScript Complete Course", "platform": "Udemy", "url": "https://www.udemy.com/course/javascript-the-complete-guide-2020-beginner-advanced/", "why_relevant": "Complete JavaScript from basics to advanced concepts"},
            {"title": "React Fundamentals", "platform": "Pluralsight", "url": "https://www.pluralsight.com/courses/react-fundamentals-update", "why_relevant": "Structured React learning path with practical projects"},
            {"title": "CSS Grid & Flexbox", "platform": "CSS-Tricks", "url": "https://css-tricks.com/snippets/css/complete-guide-grid/", "why_relevant": "Master modern CSS layout techniques"},
            {"title": "Frontend Web Development", "platform": "Coursera", "url": "https://www.coursera.org/specializations/web-design", "why_relevant": "University-backed web development specialization"},
            {"title": "JavaScript Algorithms", "platform": "LeetCode", "url": "https://leetcode.com/explore/learn/", "why_relevant": "Practice coding problems and algorithm thinking"},
            {"title": "Web Development Bootcamp", "platform": "The Odin Project", "url": "https://www.theodinproject.com/", "why_relevant": "Free, comprehensive full-stack curriculum"},
            {"title": "Frontend Mentor Challenges", "platform": "Frontend Mentor", "url": "https://www.frontendmentor.io/", "why_relevant": "Real-world frontend challenges with designs"}
        ],
        'frontend_advanced': [
            {"title": "Advanced React Patterns", "platform": "Frontend Masters", "url": "https://frontendmasters.com/courses/advanced-react-patterns/", "why_relevant": "Master complex React patterns and performance optimization"},
            {"title": "TypeScript Deep Dive", "platform": "Udemy", "url": "https://www.udemy.com/course/typescript-the-complete-developers-guide/", "why_relevant": "Advanced TypeScript for large-scale applications"},
            {"title": "Web Performance Optimization", "platform": "Google Developers", "url": "https://developers.google.com/web/fundamentals/performance", "why_relevant": "Google's guide to web performance best practices"},
            {"title": "Testing JavaScript Applications", "platform": "Kent C. Dodds", "url": "https://testingjavascript.com/", "why_relevant": "Comprehensive testing strategies for JS apps"},
            {"title": "Advanced CSS Architecture", "platform": "Smashing Magazine", "url": "https://www.smashingmagazine.com/printed-books/css/", "why_relevant": "Scalable CSS architecture and methodologies"},
            {"title": "Micro-Frontends Architecture", "platform": "Pluralsight", "url": "https://www.pluralsight.com/courses/microfrontends-architecture", "why_relevant": "Modern frontend architecture patterns"},
            {"title": "GraphQL Complete Guide", "platform": "Apollo GraphQL", "url": "https://www.apollographql.com/tutorials/", "why_relevant": "Modern API development with GraphQL"},
            {"title": "Progressive Web Apps", "platform": "Google Codelabs", "url": "https://codelabs.developers.google.com/pwa", "why_relevant": "Build modern, app-like web experiences"}
        ],
        'backend_beginner': [
            {"title": "Node.js Complete Course", "platform": "Udemy", "url": "https://www.udemy.com/course/the-complete-nodejs-developer-course-2/", "why_relevant": "Comprehensive Node.js from basics to deployment"},
            {"title": "Python for Everybody", "platform": "Coursera", "url": "https://www.coursera.org/specializations/python", "why_relevant": "University of Michigan's Python specialization"},
            {"title": "SQL Fundamentals", "platform": "DataCamp", "url": "https://www.datacamp.com/courses/intro-to-sql-for-data-science", "why_relevant": "Interactive SQL learning with real datasets"},
            {"title": "REST API Development", "platform": "Pluralsight", "url": "https://www.pluralsight.com/courses/rest-fundamentals", "why_relevant": "Build RESTful web services from scratch"},
            {"title": "Database Design Course", "platform": "edX", "url": "https://www.edx.org/course/database-design", "why_relevant": "Learn database modeling and normalization"},
            {"title": "Git Version Control", "platform": "Atlassian", "url": "https://www.atlassian.com/git/tutorials", "why_relevant": "Master Git workflows and collaboration"},
            {"title": "Linux Command Line", "platform": "Linux Academy", "url": "https://linuxacademy.com/course/linux-essentials/", "why_relevant": "Essential Linux skills for backend development"},
            {"title": "API Testing with Postman", "platform": "Postman Academy", "url": "https://academy.postman.com/", "why_relevant": "Learn API testing and documentation"}
        ],
        'backend_advanced': [
            {"title": "System Design Interview", "platform": "Educative", "url": "https://www.educative.io/courses/grokking-the-system-design-interview", "why_relevant": "Master large-scale system architecture"},
            {"title": "Microservices Patterns", "platform": "Manning", "url": "https://www.manning.com/books/microservices-patterns", "why_relevant": "Practical microservices architecture patterns"},
            {"title": "Database Internals", "platform": "O'Reilly", "url": "https://www.oreilly.com/library/view/database-internals/9781492040330/", "why_relevant": "Deep dive into database architecture"},
            {"title": "Distributed Systems", "platform": "MIT OpenCourseWare", "url": "https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/", "why_relevant": "MIT's distributed systems course"},
            {"title": "High Performance Computing", "platform": "Coursera", "url": "https://www.coursera.org/learn/parprog1", "why_relevant": "Parallel programming and optimization"},
            {"title": "Security Engineering", "platform": "OWASP", "url": "https://owasp.org/www-project-web-security-testing-guide/", "why_relevant": "Web application security best practices"},
            {"title": "DevOps Engineering", "platform": "Linux Foundation", "url": "https://training.linuxfoundation.org/training/devops-and-sre-fundamentals/", "why_relevant": "DevOps practices and SRE principles"},
            {"title": "Cloud Architecture", "platform": "AWS Training", "url": "https://aws.amazon.com/training/classroom/architecting-on-aws/", "why_relevant": "Design scalable cloud solutions"}
        ],
        'data_beginner': [
            {"title": "Python for Data Science", "platform": "DataCamp", "url": "https://www.datacamp.com/tracks/data-scientist-with-python", "why_relevant": "Complete Python data science track"},
            {"title": "Statistics Fundamentals", "platform": "Khan Academy", "url": "https://www.khanacademy.org/math/statistics-probability", "why_relevant": "Essential statistics for data analysis"},
            {"title": "SQL for Data Analysis", "platform": "Mode Analytics", "url": "https://mode.com/sql-tutorial/", "why_relevant": "SQL skills for data professionals"},
            {"title": "Data Visualization", "platform": "Tableau", "url": "https://www.tableau.com/learn/training", "why_relevant": "Create compelling data visualizations"},
            {"title": "Excel for Data Analysis", "platform": "Microsoft Learn", "url": "https://docs.microsoft.com/en-us/learn/paths/excel/", "why_relevant": "Advanced Excel techniques for data work"},
            {"title": "R Programming", "platform": "Coursera", "url": "https://www.coursera.org/learn/r-programming", "why_relevant": "Johns Hopkins R programming course"},
            {"title": "Data Analysis with Pandas", "platform": "Real Python", "url": "https://realpython.com/pandas-python-explore-dataset/", "why_relevant": "Practical pandas for data manipulation"},
            {"title": "Machine Learning Basics", "platform": "Coursera", "url": "https://www.coursera.org/learn/machine-learning", "why_relevant": "Andrew Ng's foundational ML course"}
        ],
        'cloud_beginner': [
            {"title": "AWS Cloud Practitioner", "platform": "AWS", "url": "https://aws.amazon.com/training/classroom/aws-cloud-practitioner-essentials/", "why_relevant": "AWS fundamentals and core services"},
            {"title": "Azure Fundamentals AZ-900", "platform": "Microsoft Learn", "url": "https://docs.microsoft.com/en-us/learn/paths/azure-fundamentals/", "why_relevant": "Microsoft Azure basics and services"},
            {"title": "Google Cloud Digital Leader", "platform": "Google Cloud", "url": "https://cloud.google.com/training/cloud-infrastructure", "why_relevant": "GCP services and architecture fundamentals"},
            {"title": "Docker Complete Course", "platform": "Udemy", "url": "https://www.udemy.com/course/docker-mastery/", "why_relevant": "Containerization from basics to production"},
            {"title": "Kubernetes for Beginners", "platform": "KodeKloud", "url": "https://kodekloud.com/courses/kubernetes-for-the-absolute-beginners/", "why_relevant": "Hands-on Kubernetes learning with labs"},
            {"title": "Terraform Associate", "platform": "HashiCorp Learn", "url": "https://learn.hashicorp.com/terraform", "why_relevant": "Infrastructure as Code with Terraform"},
            {"title": "Linux System Administration", "platform": "Linux Academy", "url": "https://linuxacademy.com/course/linux-system-administrator/", "why_relevant": "Essential Linux skills for cloud operations"},
            {"title": "Cloud Computing Concepts", "platform": "Coursera", "url": "https://www.coursera.org/learn/cloud-computing", "why_relevant": "University of Illinois cloud computing fundamentals"}
        ],
        'cloud_advanced': [
            {"title": "AWS Solutions Architect Professional", "platform": "A Cloud Guru", "url": "https://acloudguru.com/course/aws-certified-solutions-architect-professional", "why_relevant": "Advanced AWS architecture and design patterns"},
            {"title": "Azure Solutions Architect Expert", "platform": "Microsoft Learn", "url": "https://docs.microsoft.com/en-us/learn/certifications/azure-solutions-architect/", "why_relevant": "Enterprise Azure architecture and governance"},
            {"title": "Google Cloud Professional Architect", "platform": "Google Cloud", "url": "https://cloud.google.com/certification/cloud-architect", "why_relevant": "GCP enterprise architecture certification"},
            {"title": "Kubernetes Administration (CKA)", "platform": "Linux Foundation", "url": "https://training.linuxfoundation.org/certification/certified-kubernetes-administrator-cka/", "why_relevant": "Production Kubernetes cluster management"},
            {"title": "Advanced Terraform", "platform": "HashiCorp", "url": "https://learn.hashicorp.com/collections/terraform/certification", "why_relevant": "Enterprise infrastructure automation"},
            {"title": "Site Reliability Engineering", "platform": "Coursera", "url": "https://www.coursera.org/learn/site-reliability-engineering-slos", "why_relevant": "Google's SRE practices and principles"},
            {"title": "Multi-Cloud Architecture", "platform": "Pluralsight", "url": "https://www.pluralsight.com/courses/architecting-multi-cloud-applications", "why_relevant": "Design applications across multiple cloud providers"},
            {"title": "Cloud Security Engineering", "platform": "SANS", "url": "https://www.sans.org/cyber-security-courses/cloud-security-fundamentals/", "why_relevant": "Advanced cloud security practices"}
        ]
    }
    
    # Select appropriate resource set
    resource_key = f"{focus_area}_{skill_level.lower()}"
    if resource_key not in skill_resources:
        resource_key = 'backend_beginner'  # fallback
    
    learning_resources = skill_resources[resource_key].copy()
    
    # Prioritize technology-specific resources based on user input
    if technologies:
        tech_list = [t.strip().lower() for t in technologies.split(',')]
        tech_resources = []
        
        for tech in tech_list:
            if 'aws' in tech:
                tech_resources.extend([
                    {"title": "AWS Solutions Architect Associate", "platform": "AWS", "url": "https://aws.amazon.com/certification/certified-solutions-architect-associate/", "why_relevant": "Core AWS services and architecture patterns"},
                    {"title": "AWS Developer Associate", "platform": "A Cloud Guru", "url": "https://acloudguru.com/course/aws-certified-developer-associate", "why_relevant": "AWS development and deployment practices"}
                ])
            elif 'docker' in tech:
                tech_resources.append({"title": "Docker Mastery", "platform": "Udemy", "url": "https://www.udemy.com/course/docker-mastery/", "why_relevant": "Complete Docker containerization course"})
            elif 'kubernetes' in tech:
                tech_resources.append({"title": "Kubernetes Administration", "platform": "KodeKloud", "url": "https://kodekloud.com/courses/certified-kubernetes-administrator-cka/", "why_relevant": "Hands-on Kubernetes administration"})
            elif 'terraform' in tech:
                tech_resources.append({"title": "Terraform Associate Certification", "platform": "HashiCorp", "url": "https://learn.hashicorp.com/collections/terraform/certification", "why_relevant": "Infrastructure as Code with Terraform"})
            elif 'azure' in tech:
                tech_resources.append({"title": "Azure Administrator Associate", "platform": "Microsoft Learn", "url": "https://docs.microsoft.com/en-us/learn/certifications/azure-administrator/", "why_relevant": "Azure cloud administration and management"})
        
        # Replace first few courses with technology-specific ones
        if tech_resources:
            learning_resources = tech_resources + learning_resources[len(tech_resources):]
    
    # Ensure even number of resources (8, 10, 12, etc.)
    target_count = max(8, len(learning_resources))
    if target_count % 2 != 0:
        target_count += 1
    
    # Pad with additional relevant resources if needed
    additional_resources = [
        {"title": "GitHub Learning Lab", "platform": "GitHub", "url": "https://lab.github.com/", "why_relevant": "Hands-on Git and GitHub workflows"},
        {"title": "Stack Overflow", "platform": "Community", "url": "https://stackoverflow.com", "why_relevant": "Community-driven programming Q&A"},
        {"title": "MDN Web Docs", "platform": "Mozilla", "url": "https://developer.mozilla.org/", "why_relevant": "Comprehensive web technology documentation"},
        {"title": "HackerRank Practice", "platform": "HackerRank", "url": "https://www.hackerrank.com/", "why_relevant": "Coding challenges and skill assessment"}
    ]
    
    while len(learning_resources) < target_count:
        for resource in additional_resources:
            if resource not in learning_resources and len(learning_resources) < target_count:
                learning_resources.append(resource)
    
    learning_resources = learning_resources[:target_count]
    
    return {
        "status": "success",
        "data": {
            "summary": summary,
            "current_skills": [t.strip() for t in technologies.split(',')] if technologies else [target_area],
            "priority_skills": ["Practice", "Projects", "Documentation", "Community"],
            "recommended_roles": [
                {"title": f"{skill_level} {focus_area.title()} Engineer", "description": f"Specialized role in {target_area} with focus on {technologies if technologies else 'core technologies'}"},
                {"title": f"{focus_area.title()} Specialist", "description": f"Expert position focusing on {target_area} implementation and best practices"}
            ],
            "roadmap": {
                "foundation": roadmap_tasks[:len(roadmap_tasks)//3 + 1] if roadmap_tasks else [],
                "advancement": roadmap_tasks[len(roadmap_tasks)//3 + 1:2*(len(roadmap_tasks)//3) + 1] if len(roadmap_tasks) > 1 else [],
                "market_ready": roadmap_tasks[2*(len(roadmap_tasks)//3) + 1:] if len(roadmap_tasks) > 2 else []
            },
            "recommended_courses": learning_resources
        }
    }

@app.post("/api/v1/agents/finance")
async def finance_agent(request: dict):
    print(f"Finance agent request: {request}")
    user_data = request.get('user_data', {})
    
    income = user_data.get('income', 50000)
    expenses = user_data.get('expenses', 3000)
    age = user_data.get('age', 30)
    goals = user_data.get('financial_goals', [])
    
    if isinstance(goals, str):
        goals = [g.strip() for g in goals.split(',')]
    
    monthly_income = income / 12
    savings_potential = monthly_income - expenses
    savings_rate = (savings_potential / monthly_income * 100) if monthly_income > 0 else 0
    annual_savings = savings_potential * 12
    
    # Wealth building projections
    years_to_retirement = 65 - age
    compound_growth_7pct = annual_savings * (((1.07 ** years_to_retirement) - 1) / 0.07) if annual_savings > 0 else 0
    
    # Financial health assessment
    if savings_rate >= 20:
        financial_health = "🟢 EXCELLENT - You're on track for financial independence!"
    elif savings_rate >= 15:
        financial_health = "🟡 GOOD - Solid foundation, room for optimization"
    elif savings_rate >= 10:
        financial_health = "🟠 FAIR - Need to boost savings for long-term security"
    else:
        financial_health = "🔴 CRITICAL - Immediate action required for financial stability"
    
    # Age-specific strategies
    if age < 30:
        age_strategy = "🚀 Prime wealth-building years! Focus on aggressive growth (80% stocks, 20% bonds)"
        investment_focus = "Growth stocks, index funds, Roth IRA"
    elif age < 40:
        age_strategy = "⚡ Peak earning potential! Maximize contributions and diversify"
        investment_focus = "Balanced portfolio (70% stocks, 30% bonds), real estate"
    elif age < 50:
        age_strategy = "🎯 Acceleration phase! Catch-up contributions and tax optimization"
        investment_focus = "Conservative growth (60% stocks, 40% bonds), tax-advantaged accounts"
    else:
        age_strategy = "🛡️ Preservation mode! Capital protection with moderate growth"
        investment_focus = "Conservative mix (40% stocks, 60% bonds), dividend stocks"
    
    if savings_potential > 0:
        recommendation = f"💰 **Financial Analysis Report**\n\n**Current Status**: {financial_health}\n\n**Key Metrics**:\n• Monthly Savings: ${savings_potential:,.0f} ({savings_rate:.1f}% of income)\n• Annual Savings: ${annual_savings:,.0f}\n• Projected Retirement Wealth: ${compound_growth_7pct:,.0f} (at 7% growth)\n\n**Age Strategy**: {age_strategy}\n\n**Investment Focus**: {investment_focus}\n\n**Goal Analysis**: {', '.join(goals) if goals else 'No specific goals set - consider defining SMART financial objectives'}"
        
        # Dynamic budget optimization
        if savings_rate >= 20:
            budget = {"Investments": f"{savings_rate:.0f}%", "Necessities": "50%", "Lifestyle": f"{50-savings_rate:.0f}%"}
        else:
            budget = {"Emergency Fund": "10%", "Investments": f"{max(10, savings_rate):.0f}%", "Necessities": "60%", "Lifestyle": "20%"}
    else:
        deficit = abs(savings_potential)
        recommendation = f"🚨 **Financial Emergency Plan**\n\n**Critical Issue**: Monthly deficit of ${deficit:,.0f}\n\n**Immediate Actions Required**:\n• Income boost needed: ${deficit * 12:,.0f} annually\n• Expense reduction: Cut ${deficit:,.0f} monthly spending\n• Emergency fund: Build $1,000 ASAP for stability\n\n**Recovery Timeline**: 3-6 months to achieve positive cash flow\n\n**Priority**: Survival mode - focus on income generation and expense elimination"
        budget = {"Necessities": "80%", "Debt Payment": "15%", "Emergency": "5%"}
    
    return {
        "status": "success", 
        "data": {
            "recommendation": recommendation,
            "budget_breakdown": budget
        }
    }

@app.post("/api/v1/agents/wellness")
async def wellness_agent(request: dict):
    user_data = request.get('user_data', {})
    user_goals = request.get('user_goals', [])
    
    # Extract user profile
    age = int(user_data.get('age', 30))
    activity = user_data.get('activity_level', 'moderate')
    
    # Health calculations (using defaults for demo)
    weight = 70  # kg
    height = 175  # cm
    bmi = weight / ((height/100) ** 2)
    bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
    
    activity_multipliers = {'low': 1.2, 'moderate': 1.55, 'high': 1.9}
    daily_calories = int(bmr * activity_multipliers.get(activity, 1.55))
    
    # Health status assessment
    if bmi < 18.5:
        status = "underweight"
        focus = "healthy weight gain and muscle building"
        calorie_adj = "+300-500"
    elif bmi < 25:
        status = "optimal"
        focus = "maintaining current fitness and building strength"
        calorie_adj = "maintenance"
    elif bmi < 30:
        status = "overweight"
        focus = "gradual weight loss through sustainable habits"
        calorie_adj = "-300-500"
    else:
        status = "needs attention"
        focus = "significant lifestyle changes with professional guidance"
        calorie_adj = "-500-750"
    
    # Generate overview
    overview = f"Based on your {activity} activity level and health goals, your primary focus should be {focus}. At {age} years old, you're in a great position to build sustainable wellness habits that will serve you long-term."
    
    # Metrics section
    metrics = {
        "bmi": round(bmi, 1),
        "target_range": "18.5-24.9",
        "daily_calories": daily_calories,
        "calorie_adjustment": calorie_adj,
        "status": status
    }
    
    # Generate personalized weekly plan
    if any('weight loss' in goal.lower() or 'lose weight' in goal.lower() for goal in user_goals):
        weekly_plan = [
            "**Monday**: HIIT Cardio (30 min) + Core strengthening (15 min) - Focus on high-intensity intervals",
            "**Tuesday**: Upper body strength training (45 min) - Push/pull movements with progressive overload",
            "**Wednesday**: Steady-state cardio (40 min) - Maintain fat-burning heart rate zone",
            "**Thursday**: Lower body strength (45 min) + flexibility work (15 min)",
            "**Friday**: Full-body circuit training (35 min) - Combine cardio and strength",
            "**Saturday**: Active recovery - Long walk, light yoga, or recreational sports (60 min)",
            "**Sunday**: Complete rest day - Focus on meal prep and recovery"
        ]
    elif any('muscle' in goal.lower() or 'strength' in goal.lower() for goal in user_goals):
        weekly_plan = [
            "**Monday**: Chest & Triceps - Bench press, dips, push-ups (60 min)",
            "**Tuesday**: Back & Biceps - Pull-ups, rows, curls with heavy weights (60 min)",
            "**Wednesday**: Legs & Glutes - Squats, deadlifts, lunges for power (60 min)",
            "**Thursday**: Shoulders & Core - Overhead press, lateral raises, planks (45 min)",
            "**Friday**: Full body compound movements - Focus on functional strength (60 min)",
            "**Saturday**: Light cardio (20 min) + deep stretching and mobility work (30 min)",
            "**Sunday**: Complete rest - Prioritize sleep and nutrition for muscle recovery"
        ]
    else:
        weekly_plan = [
            "**Monday**: Balanced workout - 30 min cardio + 30 min strength training",
            "**Tuesday**: Yoga or Pilates - 45 min flow focusing on flexibility and core strength",
            "**Wednesday**: Moderate cardio - 35 min running, cycling, or swimming",
            "**Thursday**: Full-body strength training - 45 min compound movements",
            "**Friday**: Functional fitness - 40 min real-world movement patterns",
            "**Saturday**: Outdoor activity - Hiking, sports, or recreational fitness (60+ min)",
            "**Sunday**: Gentle movement - Light stretching, walking, or restorative yoga"
        ]
    
    # Nutrition guidance
    nutrition_tips = [
        "Eat protein with every meal (0.8-1g per kg body weight daily)",
        "Include colorful vegetables in 2/3 of your meals",
        "Stay hydrated with 8-10 glasses of water daily",
        "Time carbohydrates around your workouts for optimal energy"
    ]
    
    return {
        "status": "success",
        "data": {
            "overview": overview,
            "metrics": metrics,
            "weekly_plan": weekly_plan,
            "nutrition_tips": nutrition_tips,
            "recommendation": f"Your wellness journey focuses on {focus}. With consistent effort and the right approach, you can expect to see meaningful progress within 4-6 weeks."
        }
    }

@app.post("/api/v1/agents/learning")
async def learning_agent(request: dict):
    user_data = request.get('user_data', {})
    user_goals = request.get('user_goals', [])
    
    # Extract learning profile
    current_role = user_data.get('current_role', 'Professional')
    experience = int(user_data.get('experience_years', 0))
    learning_style = user_data.get('learning_style', 'hands_on')
    skills = user_data.get('skills', [])
    
    if isinstance(skills, str):
        skills = [s.strip() for s in skills.split(',')]
    
    # Assess current level
    skill_count = len(skills)
    if skill_count == 0:
        level = "Beginner"
        level_desc = "Starting your learning journey with foundational concepts"
    elif skill_count <= 3:
        level = "Intermediate"
        level_desc = "Building on existing knowledge to develop specialized expertise"
    else:
        level = "Advanced"
        level_desc = "Expanding into leadership and cutting-edge technologies"
    
    # Generate profile summary
    summary = f"As a {level.lower()} learner in {current_role.lower()} with {experience} years of experience, you're {level_desc}. Your {learning_style.replace('_', '-')} learning style will guide our recommended approach to skill development."
    
    # Create learning phases
    if level == "Beginner":
        phases = [
            {
                "name": "Foundation",
                "duration": "2-3 months",
                "focus": "Core programming concepts and development environment setup",
                "skills": ["Programming fundamentals", "Version control (Git)", "Basic web technologies"]
            },
            {
                "name": "Application", 
                "duration": "3-4 months",
                "focus": "Building real projects and understanding software development lifecycle",
                "skills": ["Framework proficiency", "Database basics", "Testing fundamentals"]
            },
            {
                "name": "Specialization",
                "duration": "4-6 months", 
                "focus": "Deep dive into chosen technology stack and industry best practices",
                "skills": ["Advanced frameworks", "System design", "Performance optimization"]
            }
        ]
    elif level == "Intermediate":
        phases = [
            {
                "name": "Skill Expansion",
                "duration": "2-3 months",
                "focus": "Broadening technical skills and learning complementary technologies",
                "skills": ["New programming languages", "Cloud platforms", "DevOps basics"]
            },
            {
                "name": "Architecture",
                "duration": "3-4 months",
                "focus": "Understanding system design and scalable application development",
                "skills": ["Microservices", "API design", "Database optimization"]
            },
            {
                "name": "Leadership",
                "duration": "4-5 months",
                "focus": "Developing technical leadership and mentoring capabilities",
                "skills": ["Team leadership", "Code review", "Technical communication"]
            }
        ]
    else:
        phases = [
            {
                "name": "Innovation",
                "duration": "2-3 months",
                "focus": "Exploring emerging technologies and industry trends",
                "skills": ["AI/ML integration", "Blockchain", "Edge computing"]
            },
            {
                "name": "Strategy",
                "duration": "3-4 months",
                "focus": "Technical strategy and organizational impact",
                "skills": ["Technical vision", "Architecture decisions", "Technology evaluation"]
            },
            {
                "name": "Thought Leadership",
                "duration": "Ongoing",
                "focus": "Industry contribution through content creation and community involvement",
                "skills": ["Public speaking", "Technical writing", "Open source contribution"]
            }
        ]
    
    # Generate course recommendations
    if any('data' in goal.lower() or 'analytics' in goal.lower() for goal in user_goals):
        courses = [
            {
                "title": "Python for Data Science and Machine Learning",
                "provider": "Coursera (IBM)",
                "duration": "6 weeks",
                "url": "https://www.coursera.org/professional-certificates/ibm-data-science",
                "description": "Comprehensive introduction to data analysis, visualization, and machine learning"
            },
            {
                "title": "Advanced SQL for Data Scientists",
                "provider": "DataCamp",
                "duration": "4 weeks",
                "url": "https://www.datacamp.com/courses/advanced-sql",
                "description": "Master complex queries, window functions, and database optimization"
            },
            {
                "title": "Machine Learning Engineering for Production",
                "provider": "Coursera (DeepLearning.AI)",
                "duration": "8 weeks",
                "url": "https://www.coursera.org/specializations/machine-learning-engineering-for-production-mlops",
                "description": "Learn to deploy and maintain ML systems in production environments"
            }
        ]
    elif any('web' in goal.lower() or 'frontend' in goal.lower() or 'fullstack' in goal.lower() for goal in user_goals):
        courses = [
            {
                "title": "Complete React Developer Course",
                "provider": "Udemy",
                "duration": "8 weeks",
                "url": "https://www.udemy.com/course/react-the-complete-guide-incl-redux/",
                "description": "Master React, Redux, and modern frontend development practices"
            },
            {
                "title": "Node.js: The Complete Guide",
                "provider": "Udemy",
                "duration": "6 weeks",
                "url": "https://www.udemy.com/course/nodejs-the-complete-guide/",
                "description": "Build scalable backend applications with Node.js and Express"
            },
            {
                "title": "Full Stack Open",
                "provider": "University of Helsinki",
                "duration": "12 weeks",
                "url": "https://fullstackopen.com/",
                "description": "Free comprehensive course covering modern web development stack"
            }
        ]
    else:
        courses = [
            {
                "title": "CS50: Introduction to Computer Science",
                "provider": "Harvard (edX)",
                "duration": "10 weeks",
                "url": "https://www.edx.org/course/introduction-computer-science-harvardx-cs50x",
                "description": "Foundational computer science concepts and programming principles"
            },
            {
                "title": "System Design Interview Course",
                "provider": "Educative",
                "duration": "6 weeks",
                "url": "https://www.educative.io/courses/grokking-the-system-design-interview",
                "description": "Learn to design scalable systems for technical interviews"
            },
            {
                "title": "AWS Solutions Architect",
                "provider": "A Cloud Guru",
                "duration": "8 weeks",
                "url": "https://acloudguru.com/course/aws-certified-solutions-architect-associate-saa-c03",
                "description": "Master cloud architecture and AWS services for modern applications"
            }
        ]
    
    return {
        "status": "success",
        "data": {
            "summary": summary,
            "current_level": level,
            "learning_phases": phases,
            "course_recommendations": courses,
            "recommendation": f"Based on your {level.lower()} level and {learning_style.replace('_', ' ')} learning preference, focus on {phases[0]['focus'].lower()} over the next {phases[0]['duration']}. This structured approach will build the foundation for your long-term learning goals."
        }
    }

@app.post("/api/v1/career/plan/save")
async def save_career_plan(request: CareerPlanRequest, current_user_id: str = Depends(get_current_user)):
    try:
        career_plans_db[current_user_id] = {
            "roadmap": request.roadmap,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        # Save to persistent storage
        save_db(CAREER_PLANS_DB_FILE, career_plans_db)
        
        # Also save as goals for the user
        if current_user_id not in user_goals_db:
            user_goals_db[current_user_id] = []
        
        # Convert roadmap tasks to goals
        for task in request.roadmap.get("tasks", []):
            goal = {
                "id": task["id"],
                "title": task["title"],
                "description": task["description"],
                "category": task["category"],
                "deadline": task["week_or_deadline"],
                "completed": False,
                "created_at": datetime.now().isoformat()
            }
            user_goals_db[current_user_id].append(goal)
        
        # Save to persistent storage
        save_db(USER_GOALS_DB_FILE, user_goals_db)
        
        return {"status": "success", "message": "Career plan saved as goals successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/career/plan/replan")
async def replan_career(request: CareerUpdateRequest, current_user_id: str = Depends(get_current_user)):
    try:
        # Generate updated tasks (remove completed, add next-level)
        new_tasks = [
            {"id": "adv1", "title": "Advanced React Patterns", "description": "Learn hooks, context, and performance optimization", "phase": "Market Ready", "week_or_deadline": "Week 13", "category": "Skill Building", "status": "pending", "resources": [{'title': 'React Advanced Guide', 'url': 'https://react.dev/learn/thinking-in-react'}]},
            {"id": "adv2", "title": "Microservices Architecture", "description": "Design and implement microservices", "phase": "Market Ready", "week_or_deadline": "Week 14", "category": "Projects", "status": "pending", "resources": [{'title': 'Microservices Guide', 'url': 'https://microservices.io/'}]}
        ]
        
        # Update user goals to mark completed tasks
        if current_user_id in user_goals_db:
            for goal in user_goals_db[current_user_id]:
                if goal["id"] in request.completed_tasks:
                    goal["completed"] = True
            
            # Save to persistent storage
            save_db(USER_GOALS_DB_FILE, user_goals_db)
        
        return {
            "status": "success",
            "data": {
                "tasks": new_tasks,
                "message": f"Plan updated with {len(request.completed_tasks)} completed tasks. Added advanced challenges."
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "total_users": len(users_db)
    }

@app.post("/api/v1/agents/parallel")
async def parallel_agents(request: ParallelAgentRequest, current_user_id: str = Depends(get_current_user)):
    """
    Parallel Agents endpoint - runs Career, Wellness, and Learning agents concurrently.
    """
    try:
        start_time = datetime.now()
        
        # Prepare base input for all agents
        base_input = {
            "user_data": request.user_data,
            "user_goals": request.user_goals,
            **request.parameters
        }
        
        # Load user memory context for agents
        try:
            memory_response = await get_memory_history(5, current_user_id)
            if memory_response["memories"]:
                base_input["user_memory"] = memory_response["context_summary"]
        except Exception as e:
            print(f"Failed to load memory context: {e}")
        
        # Define enhanced agent tasks
        async def run_career_agent():
            try:
                career_data = await generate_enhanced_career_block(request.user_data, request.user_goals)
                return "career", {"status": "success", "data": career_data}
            except Exception as e:
                return "career", {"status": "error", "error": str(e), "data": {}}
        
        async def run_wellness_agent():
            try:
                wellness_data = await generate_enhanced_wellness_block(request.user_data, request.user_goals)
                return "wellness", {"status": "success", "data": wellness_data}
            except Exception as e:
                return "wellness", {"status": "error", "error": str(e), "data": {}}
        
        async def run_learning_agent():
            try:
                learning_data = await generate_enhanced_learning_block(request.user_data, request.user_goals)
                return "learning", {"status": "success", "data": learning_data}
            except Exception as e:
                return "learning", {"status": "error", "error": str(e), "data": {}}
        
        # Run all agents concurrently
        agent_results = await asyncio.gather(
            run_career_agent(),
            run_wellness_agent(),
            run_learning_agent(),
            return_exceptions=True
        )
        
        execution_time = (datetime.now() - start_time).total_seconds()
        
        # Process results
        results = {}
        errors = {}
        overall_status = "success"
        
        for result_item in agent_results:
            if isinstance(result_item, Exception):
                errors["unknown"] = str(result_item)
                overall_status = "partial_success"
                continue
            
            if isinstance(result_item, tuple) and len(result_item) == 2:
                agent_name, result = result_item
                
                if isinstance(result, Exception):
                    errors[agent_name] = str(result)
                    overall_status = "partial_success"
                    continue
                
                if result.get("status") == "success":
                    results[agent_name] = result.get("data", {})
                else:
                    errors[agent_name] = result.get("error", "Unknown error")
                    overall_status = "partial_success"
        
        if len(errors) == 3:
            overall_status = "error"
        elif len(results) == 0:
            overall_status = "error"
        
        # Store combined results
        combined_output = {
            "id": hashlib.md5(f"{current_user_id}_parallel_{datetime.now().isoformat()}".encode()).hexdigest()[:12],
            "user_id": current_user_id,
            "agent_type": "parallel",
            "created_at": datetime.now().isoformat(),
            "input_data": request.dict(),
            "output_data": results,
            "execution_time": execution_time,
            "errors": errors
        }
        
        if current_user_id not in user_agent_outputs_db:
            user_agent_outputs_db[current_user_id] = []
        user_agent_outputs_db[current_user_id].append(combined_output)
        
        # Save to persistent storage
        save_db(USER_AGENT_OUTPUTS_DB_FILE, user_agent_outputs_db)
        
        # Auto-store compacted memory
        try:
            memory_request = {
                "session_data": request.dict(),
                "agent_results": results,
                "user_goals": request.user_goals
            }
            await store_compacted_memory(MemoryRequest(**memory_request), current_user_id)
        except Exception as e:
            print(f"Failed to store memory: {e}")  # Don't fail the main request
        
        return ParallelAgentResponse(
            status=overall_status,
            results=results,
            execution_time=execution_time,
            errors=errors
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Tool endpoints
class SearchRequest(BaseModel):
    query: str
    num_results: int = 5

class ExecuteRequest(BaseModel):
    code: str
    language: str = "python"

@app.post("/api/v1/tools/search")
async def search_tool(request: SearchRequest, current_user_id: str = Depends(get_current_user)):
    """Google Search endpoint."""
    try:
        import time
        start_time = time.time()
        
        # Mock search results
        mock_results = [
            {"title": "Software Engineer Jobs 2024", "link": "https://example.com", "snippet": "High demand for software engineers"},
            {"title": "Python Developer Salary", "link": "https://glassdoor.com", "snippet": "Average salary $95k-140k"},
            {"title": "Remote Tech Jobs", "link": "https://remote.co", "snippet": "500+ remote positions available"}
        ]
        
        execution_time = time.time() - start_time
        
        return {
            "status": "success",
            "query": request.query,
            "results": mock_results[:request.num_results],
            "total_results": len(mock_results),
            "execution_time": execution_time
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/tools/execute")
async def execute_tool(request: ExecuteRequest, current_user_id: str = Depends(get_current_user)):
    """Code execution endpoint."""
    try:
        import time
        if request.language != "python":
            raise HTTPException(status_code=400, detail="Only Python supported")
        
        start_time = time.time()
        
        # Safe code execution simulation
        if "import os" in request.code or "exec(" in request.code:
            return {
                "status": "error",
                "output": "",
                "error": "Unsafe code detected",
                "execution_time": 0
            }
        
        # Mock execution
        output = "Code executed successfully\n"
        if "print" in request.code:
            output += "Hello World\n"
        if "2 + 2" in request.code:
            output += "Result: 4\n"
        
        execution_time = time.time() - start_time
        
        return {
            "status": "success",
            "output": output,
            "error": "",
            "execution_time": execution_time
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Memory endpoints
class MemoryRequest(BaseModel):
    session_data: dict
    agent_results: dict
    user_goals: List[str] = []

@app.post("/api/v1/memory/compacted")
async def store_compacted_memory(request: MemoryRequest, current_user_id: str = Depends(get_current_user)):
    """Store compacted memory from parallel agent session."""
    try:
        # Find user in database
        user_email = None
        for email, user_data in users_db.items():
            if user_data["id"] == current_user_id:
                user_email = email
                break
        
        if not user_email:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Initialize memory_bank if not exists
        if "memory_bank" not in users_db[user_email]:
            users_db[user_email]["memory_bank"] = []
        
        # Create compacted memory entry
        memory_entry = {
            "id": hashlib.md5(f"{current_user_id}_{datetime.now().isoformat()}".encode()).hexdigest()[:12],
            "timestamp": datetime.now().isoformat(),
            "session_summary": f"Session with {len(request.agent_results)} agents",
            "goals": request.user_goals[:3],  # Limit to 3 goals
            "key_insights": [],
            "compacted_results": {}
        }
        
        # Compact agent results (truncate long texts)
        for agent_type, result in request.agent_results.items():
            if isinstance(result, dict) and "data" in result:
                data = result["data"]
                compacted_data = {}
                
                # Extract key info and truncate
                for key, value in data.items():
                    if isinstance(value, str):
                        compacted_data[key] = value[:200] + "..." if len(value) > 200 else value
                    elif isinstance(value, list) and len(value) > 0:
                        if isinstance(value[0], dict):
                            compacted_data[key] = value[:3]  # Limit to 3 items
                        else:
                            compacted_data[key] = value[:5]  # Limit to 5 items
                    else:
                        compacted_data[key] = value
                
                memory_entry["compacted_results"][agent_type] = compacted_data
                
                # Extract key insights
                if agent_type == "career" and "current_skills" in data:
                    memory_entry["key_insights"].append(f"Skills: {', '.join(data['current_skills'][:3])}")
                elif agent_type == "wellness" and "recommendation" in data:
                    if "BMI" in str(data["recommendation"]):
                        memory_entry["key_insights"].append("Health metrics tracked")
                elif agent_type == "learning" and "recommendation" in data:
                    if "BEGINNER" in str(data["recommendation"]):
                        memory_entry["key_insights"].append("Learning: Beginner level")
        
        # Add to memory bank (keep last 20 entries)
        users_db[user_email]["memory_bank"].append(memory_entry)
        if len(users_db[user_email]["memory_bank"]) > 20:
            users_db[user_email]["memory_bank"] = users_db[user_email]["memory_bank"][-20:]
        
        # Save to persistent storage
        save_db(USERS_DB_FILE, users_db)
        
        return {
            "status": "success",
            "memory_id": memory_entry["id"],
            "compacted_context": memory_entry["session_summary"],
            "context_length": len(str(memory_entry))
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/memory/history")
async def get_memory_history(limit: int = 10, current_user_id: str = Depends(get_current_user)):
    """Get user's memory history."""
    try:
        # Find user in database
        user_email = None
        for email, user_data in users_db.items():
            if user_data["id"] == current_user_id:
                user_email = email
                break
        
        if not user_email:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Get memory bank
        memory_bank = users_db[user_email].get("memory_bank", [])
        
        # Return recent memories (limited)
        recent_memories = memory_bank[-limit:] if memory_bank else []
        recent_memories.reverse()  # Most recent first
        
        return {
            "status": "success",
            "memories": recent_memories,
            "total_sessions": len(memory_bank),
            "context_summary": f"User has {len(memory_bank)} previous sessions" if memory_bank else "No previous sessions"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/goals/summary")
async def get_goals_summary(current_user_id: str = Depends(get_current_user)):
    user_goals = [g for g in goals_db if g.get("user_id") == current_user_id]
    
    total = len(user_goals)
    completed = len([g for g in user_goals if g.get("status") == "completed"])
    in_progress = len([g for g in user_goals if g.get("status") == "in_progress"])
    
    # Check overdue goals (simplified - goals without due_date are not overdue)
    from datetime import datetime
    today = datetime.now().isoformat()[:10]
    overdue = len([g for g in user_goals if g.get("due_date") and g.get("due_date") < today and g.get("status") != "completed"])
    
    return {
        "total": total,
        "completed": completed,
        "in_progress": in_progress,
        "overdue": overdue
    }

@app.post("/api/v1/goals")
async def create_goal(goal_request: GoalRequest, current_user_id: str = Depends(get_current_user)):
    goal_id = hashlib.md5(f"{current_user_id}_{datetime.now().isoformat()}".encode()).hexdigest()[:12]
    
    new_goal = {
        "id": goal_id,
        "user_id": current_user_id,
        "title": goal_request.title,
        "description": goal_request.description,
        "status": "pending",
        "category": goal_request.category,
        "created_at": datetime.now().isoformat(),
        "due_date": goal_request.due_date
    }
    
    goals_db.append(new_goal)
    save_db(GOALS_DB_FILE, goals_db)
    
    return {"status": "success", "goal": new_goal}

@app.post("/api/v1/career/roadmap/progress")
async def update_roadmap_progress(request: RoadmapProgressRequest, current_user_id: str = Depends(get_current_user)):
    if current_user_id not in career_progress_db:
        career_progress_db[current_user_id] = {"completed_task_ids": []}
    
    completed_tasks = career_progress_db[current_user_id]["completed_task_ids"]
    
    if request.completed and request.task_id not in completed_tasks:
        completed_tasks.append(request.task_id)
    elif not request.completed and request.task_id in completed_tasks:
        completed_tasks.remove(request.task_id)
    
    career_progress_db[current_user_id]["completed_task_ids"] = completed_tasks
    save_db(CAREER_PROGRESS_DB_FILE, career_progress_db)
    
    return {"status": "success", "completed_task_ids": completed_tasks}

@app.get("/api/v1/career/roadmap/progress")
async def get_roadmap_progress(current_user_id: str = Depends(get_current_user)):
    user_progress = career_progress_db.get(current_user_id, {"completed_task_ids": []})
    return {"status": "success", "completed_task_ids": user_progress["completed_task_ids"]}

class CourseProgressRequest(BaseModel):
    course_title: str
    completed: bool

@app.post("/api/v1/career/course/progress")
async def update_course_progress(request: CourseProgressRequest, current_user_id: str = Depends(get_current_user)):
    if current_user_id not in course_progress_db:
        course_progress_db[current_user_id] = {"completed_course_ids": []}
    
    completed_courses = course_progress_db[current_user_id]["completed_course_ids"]
    
    if request.completed and request.course_title not in completed_courses:
        completed_courses.append(request.course_title)
    elif not request.completed and request.course_title in completed_courses:
        completed_courses.remove(request.course_title)
    
    course_progress_db[current_user_id]["completed_course_ids"] = completed_courses
    save_db(COURSE_PROGRESS_DB_FILE, course_progress_db)
    
    return {"status": "success", "completed_course_ids": completed_courses}

@app.get("/api/v1/career/course/progress")
async def get_course_progress(current_user_id: str = Depends(get_current_user)):
    user_progress = course_progress_db.get(current_user_id, {"completed_course_ids": []})
    return {"status": "success", "completed_course_ids": user_progress["completed_course_ids"]}

@app.get("/api/v1/debug/users")
async def debug_users():
    users_info = []
    for email, user_data in users_db.items():
        users_info.append({
            "id": user_data["id"],
            "name": user_data["name"],
            "email": user_data["email"],
            "created_at": user_data["created_at"],
            "memory_sessions": len(user_data.get("memory_bank", []))
        })
    
    return {
        "total_users": len(users_db),
        "users": users_info
    }

if __name__ == "__main__":
    print("Starting server on http://127.0.0.1:8080")
    print(f"Initial users in database: {len(users_db)}")
    uvicorn.run(app, host="127.0.0.1", port=8080)