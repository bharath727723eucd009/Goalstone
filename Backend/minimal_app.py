from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Working"}

@app.get("/api/v1/users/me")
async def get_profile():
    return {
        "id": "demo_user",
        "name": "Demo User",
        "email": "demo@gmail.com",
        "location": "San Francisco, CA",
        "role": "professional",
        "tagline": "AI-powered life goals explorer",
        "avatar": None,
        "stats": {"total_goals": 12, "completed_goals": 8, "streak_days": 15},
        "preferences": {"email_notifications": True, "weekly_summary": True, "focus_areas": ["career", "wellness"]}
    }

@app.put("/api/v1/users/me")
async def update_profile():
    return {"message": "Profile updated successfully"}

@app.put("/api/v1/users/me/preferences")
async def update_preferences():
    return {"message": "Preferences updated successfully"}

@app.post("/api/v1/auth/login")
async def login():
    return {"access_token": "demo_token", "user": {"id": "demo_user", "name": "Demo User", "email": "demo@gmail.com"}}

@app.post("/api/v1/auth/register")
async def register():
    return {"message": "User registered successfully"}

@app.post("/api/v1/agents/career")
async def career_agent():
    return {"recommendations": [], "roadmap": []}

@app.post("/api/v1/agents/finance")
async def finance_agent():
    return {"recommendations": []}

@app.post("/api/v1/agents/wellness")
async def wellness_agent():
    return {"recommendations": []}

@app.post("/api/v1/agents/learning")
async def learning_agent():
    return {"recommendations": []}

@app.get("/api/v1/user/stats")
async def get_user_stats():
    return {"total_milestones": 12, "completed_milestones": 8, "active_goals": 4, "completion_rate": 67}