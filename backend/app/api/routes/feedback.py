from fastapi import APIRouter, Depends, HTTPException
from app.api.dependencies import get_current_user
from app.schemas.models import FeedbackRequest
from app.database.supabase_client import supabase_client

router = APIRouter(prefix="/feedback", tags=["Feedback"])

@router.post("/")
async def submit_feedback(
    request: FeedbackRequest, 
    user = Depends(get_current_user)
):
    try: 
        supabase_client.table("movie_feedback").upsert({
        "user_id": user["id"],
        "movie_id": request.movie_id,
        "feedback_type": request.feedback_type.value
    }).execute()

        return {
            "success": True, 
            "message": f"Feedback '{request.feedback_type}' recorded"}
    
    except Exception as e: 
        print("FEEDBACK ERROR:", e)
        raise HTTPException(
            status_code=400, 
            detail="Could not save feedback"
)
