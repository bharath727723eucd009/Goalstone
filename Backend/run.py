"""Simple startup script for the FastAPI backend."""
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Create FastAPI app
app = FastAPI(
    title="AI Life Goal Management System",
    description="Multi-agent system for personalized life goal management",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "AI Life Goal Management System",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

# Simple auth endpoints for demo
@app.post("/api/v1/auth/login")
async def login(credentials: dict):
    """Demo login endpoint."""
    # Demo credentials
    if credentials.get("email") == "demo@example.com" and credentials.get("password") == "demo123":
        return {
            "access_token": "demo_token_12345",
            "token_type": "bearer",
            "user": {
                "id": "demo_user",
                "email": "demo@example.com",
                "name": "Demo User"
            }
        }
    return {"error": "Invalid credentials"}, 401

@app.post("/api/v1/auth/logout")
async def logout():
    """Demo logout endpoint."""
    return {"message": "Logged out successfully"}

@app.get("/api/v1/user/profile")
async def get_profile():
    """Demo profile endpoint."""
    return {
        "id": "demo_user",
        "email": "demo@example.com", 
        "name": "Demo User",
        "created_at": "2024-01-01T00:00:00Z"
    }

@app.get("/api/v1/user/stats")
async def get_stats():
    """Demo stats endpoint."""
    return {
        "total_milestones": 12,
        "completed_milestones": 8,
        "active_goals": 4,
        "completion_rate": 67
    }

if __name__ == "__main__":
    uvicorn.run(
        "run:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )