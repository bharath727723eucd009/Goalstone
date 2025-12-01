"""Simple working FastAPI application."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Create FastAPI app
app = FastAPI(title="AI Life Goal Management System")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve uploaded files
from fastapi.staticfiles import StaticFiles
import os

# Ensure uploads directory exists
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Include auth routes
from auth.routes import router as auth_router
app.include_router(auth_router, prefix="/api/v1")

# Include tool routes
from api.tool_routes import router as tool_router
app.include_router(tool_router, prefix="/api/v1")





# Include profile routes
from api.profile_routes import router as profile_router
app.include_router(profile_router, prefix="/api/v1")

# Include goalie routes (isolated chatbot feature)
from api.goalie_routes import router as goalie_router
app.include_router(goalie_router, prefix="/goalie", tags=["goalie"])

@app.get("/")
async def root():
    return {"message": "AI Life Goal Management System", "status": "running"}

@app.get("/api/v1/user/stats")
async def get_stats():
    return {
        "total_milestones": 12,
        "completed_milestones": 8,
        "active_goals": 4,
        "completion_rate": 67
    }

# Debug endpoint to check users
@app.get("/api/v1/debug/users")
async def debug_users():
    from database.users import user_db
    users = []
    for email, user_data in user_db.users.items():
        users.append({
            "id": user_data["id"],
            "email": email,
            "name": user_data["name"]
        })
    return {
        "users": users,
        "total_count": len(users)
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)