from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["profile"])

@router.get("/me")
async def get_profile():
    return {
        "id": "demo_user",
        "name": "Demo User", 
        "email": "demo@gmail.com",
        "avatar": None
    }

@router.put("/me")
async def update_profile():
    return {"message": "Profile updated successfully"}

@router.put("/me/preferences")
async def update_preferences():
    return {"message": "Preferences updated successfully"}