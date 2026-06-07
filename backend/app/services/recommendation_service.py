'''This module handles the recommendation workflow. 
It is responsible for collecting the user taste profile, process mood and energy context, user intent, call the recommendation pipeline, and return the ranked movie recommendations. '''
from typing import List, Optional
from app.schemas.models import RecommendationRequest, MovieRecommendation
from app.services.profile_service import profile_service

'''This class generates movie recommendations. 
The request contains the mood, energy, intent, and optional preferences'''
class RecommendationService:
    def get_recommendations(
            self, 
            request: RecommendationRequest,
            user_id: Optional[str] = None,
            session_id:  Optional[str] = None 
    ) -> List[MovieRecommendation]:
        
        if user_id: 
            taste_profile = (
                profile_service.get_user_taste_profile(user_id)
            )
        else: 
            taste_profile = {
                "favorite_movies": [],
                "preferences": {},
                "disliked_movie_ids": []
            }
        mood = request.mood
        energy = request.energy
        intent = request.intent

        print("User Profile:", taste_profile)
        print("Context:", {
            "mood": mood,
            "energy": energy, 
            "intent": intent
        })
        return []
    
'''This is going to be replaced with the machine learning pipeline later.'''
recommendation_service = RecommendationService()