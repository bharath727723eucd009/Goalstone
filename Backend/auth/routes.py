"""Authentication routes."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database.users import user_db

router = APIRouter(prefix="/auth", tags=["authentication"])

class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    email: str
    password: str
    name: str

@router.post("/login")
async def login(credentials: LoginRequest):
    """
    Login endpoint - mock implementation.
    In production, verify credentials against user database.
    """
    # Check if email exists
    existing_user = user_db.get_user(credentials.email)
    if not existing_user:
        raise HTTPException(status_code=401, detail="Email not found")
    
    # Verify password
    user = user_db.verify_user(credentials.email, credentials.password)
    if user:
        return {
            "access_token": f"token_{user['id']}",
            "token_type": "bearer",
            "user": {
                "id": user["id"],
                "email": credentials.email,
                "name": user["name"]
            }
        }
    else:
        raise HTTPException(status_code=401, detail="Incorrect password")

@router.post("/register")
async def register(user_data: RegisterRequest):
    """Register new user."""
    try:
        user_id = user_db.create_user(user_data.email, user_data.password, user_data.name)
        return {
            "message": "Registration successful",
            "user_id": user_id
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/me")
async def get_current_user_info():
    """Get current user information."""
    # For demo, return demo user data
    # In production, extract user from JWT token
    return {
        "id": "demo_user",
        "email": "demo@gmail.com",
        "name": "Demo User"
    }

@router.get("/users")
async def get_all_users():
    """Get all registered users (for admin/debug purposes)."""
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