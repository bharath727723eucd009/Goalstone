"""Profile management routes."""
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from pydantic import BaseModel
from typing import Optional
import json
import hashlib
import uuid
import base64
from pathlib import Path

try:
    from Backend.database.users import user_db
except ImportError:
    user_db = None

router = APIRouter(prefix="/users", tags=["profile"])

class ProfileUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    location: Optional[str] = None
    role: Optional[str] = None
    tagline: Optional[str] = None

class PreferencesUpdate(BaseModel):
    email_notifications: Optional[bool] = None
    weekly_summary: Optional[bool] = None
    focus_areas: Optional[list] = None

class PasswordChange(BaseModel):
    current_password: str
    new_password: str

@router.get("/me")
async def get_profile():
    """Get current user profile."""
    # Mock implementation - in production, get from JWT token
    return {
        "id": "demo_user",
        "name": "Demo User",
        "email": "demo@gmail.com",
        "location": "San Francisco, CA",
        "role": "professional",
        "tagline": "AI-powered life goals explorer",
        "avatar": None,  # No avatar by default
        "stats": {
            "total_goals": 12,
            "completed_goals": 8,
            "streak_days": 15
        },
        "preferences": {
            "email_notifications": True,
            "weekly_summary": True,
            "focus_areas": ["career", "wellness"]
        }
    }

@router.put("/me")
async def update_profile(profile: ProfileUpdate):
    """Update user profile."""
    return {"message": "Profile updated successfully"}

@router.put("/me/preferences")
async def update_preferences(preferences: PreferencesUpdate):
    """Update user preferences."""
    return {"message": "Preferences updated successfully"}

@router.post("/me/password")
async def change_password(password_data: PasswordChange):
    """Change user password."""
    if len(password_data.new_password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters")
    return {"message": "Password changed successfully"}

@router.post("/me/avatar")
async def upload_avatar(file: UploadFile = File(...)):
    """Upload user avatar."""
    if not file.content_type or not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    content = await file.read()
    if len(content) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File size must be less than 5MB")
    
    uploads_dir = Path("uploads")
    uploads_dir.mkdir(exist_ok=True)
    
    file_extension = file.filename.split('.')[-1] if file.filename and '.' in file.filename else 'jpg'
    filename = f"avatar_{uuid.uuid4()}.{file_extension}"
    file_path = uploads_dir / filename
    
    with open(file_path, "wb") as buffer:
        buffer.write(content)
    
    return {"message": "Avatar uploaded successfully"}