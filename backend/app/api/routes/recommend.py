'''This module handles the recommendation API routes includes the authenticated (logged-in users) and guest recommendations
This rotes delegate recommendation logic to RecommendationService.'''
from fastapi import APIRouter, Depends
import uuid 
from app.api.dependencies import get_current_user
from app.schemas.models import RecommendationRequest, RecommendationResponse 
from app.services.recommendation_service import recommendation_service

router = APIRouter(prefix="/recommend", tags=["Recommendations"])

@router.post("/", response_model=RecommendationResponse)
async def get_recommendations(
    request: RecommendationRequest, 
    user: dict = Depends(get_current_user)
):
    results = recommendation_service.get_recommendations(
        request=request, 
        user_id=user["id"]
    )
    return RecommendationResponse(recommendations=results)

@router.post("/guest", response_model=RecommendationResponse)
async def get_guest_recommendations(request: RecommendationRequest):
    session_id = str(uuid.uuid4())
    results = recommendation_service.get_recommendations(
        request=request,
        session_id=session_id
    )
    return RecommendationResponse(
        recommendations=results,
        session_id=session_id
    )