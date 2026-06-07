from fastapi import APIRouter, Depends, HTTPException
from app.api.dependencies import get_current_user
from app.services.profile_service import profile_service
from app.schemas.models import UserPreferencesRequest, FavoriteMovieRequest

router = APIRouter(prefix="/profile", tags=["Profile"])

@router.get("/")
async def get_profile(
    user = Depends(get_current_user)):
    profile = profile_service.get_profile(user["id"])
    if not profile:
        raise HTTPException(
            status_code=404, 
            detail="Profile not found")
    return profile

@router.post("/favorites")
async def add_favorite(
    request: FavoriteMovieRequest,
    user = Depends(get_current_user)
): 
    success = profile_service.add_favorite_movie(user["id"], request.tmdb_id)
    
    if not success: 
        raise HTTPException(
            status_code=400,
            detail="Could not add favorite movie"
        )
    return {"success": True,
            "message": "Movie added to favorites"}

@router.put("/preferences")
async def update_preferences(
    request: UserPreferencesRequest,
    user = Depends(get_current_user)
):
    success = profile_service.update_preferences(user["id"], request.model_dump())

    if not success: 
        raise HTTPException(
            status_code=400,
            detail="Could not update preferences")
            
    return {"success": True,
            "message": "Preferences updated"}