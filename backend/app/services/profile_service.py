'''This module handles all database operations related to user profiles, movie preferences, favorites, and feedback. 
It interacts with the Supabase database to retrieve and update user information, including taste profiles used for personalized movie recommendations.'''

from app.database.supabase_client import supabase_client
from typing import Optional, Dict, Any 

'''The ProfileService class provides methods to get user profiles, retrieve taste profiles, add favorite movies, and update user preferences.'''
class ProfileService: 
    def get_profile(
            self, 
            user_id: str) -> Optional[Dict]:
        
        response = (
            supabase_client
            .table("profiles")
            .select("*")
            .eq("id", user_id)
            .single()
            .execute()
            )
        
        return response.data

    # This method retrieves all user preference signals including favorite movies,
    # genre/director/actor preferences, and disliked movies. The output is later
    # used to feed the personalized recommendation engine.
    def get_user_taste_profile(
            self,
            user_id: str) -> Dict[str, Any]:
        
        favorites = (
            supabase_client
            .table("favorite_movies")
            .select(
                """
                movie_id, 
                movies(tmdb_id, 
                title, 
                genres, 
                keywords
                )
                """
            )
            .eq("user_id", user_id)
            .execute()
        )
    
        preferences = (
            supabase_client
            .table("user_preferences")
            .select("*")
            .eq("user_id", user_id)
            .maybe_single()
            .execute()
        )
    
        dislikes = (
            supabase_client
            .table("movie_feedback")
            .select("movie_id")
            .eq("user_id", user_id)
            .eq("feedback_type", "dislike")
            .execute()
        )
    
        return {
            "user_id": user_id,
            "favorite_movies": favorites.data or [],
            "preferences": preferences.data or {},
            "disliked_movie_ids": [item["movie_id"] for item in (dislikes.data or [])]
        }

    def add_favorite_movie(self, user_id: str, tmdb_id: int) -> bool:
        try: 
            movie = (supabase_client.table("movies").select("id").eq("tmdb_id", tmdb_id).single().execute())
            if not movie.data:
                print("MOVIE NOT FOUND:", tmdb_id)
                return False
            
            supabase_client.table("favorite_movies").insert({
                "user_id": user_id,
                "movie_id": movie.data["id"]
            }).execute()
            return True
        
        except Exception as e:
            print("ADD FAVORTIE MOVIE ERROR:", e)
            return False

    def update_preferences(self, 
                           user_id: str, 
                           preferences: Dict) -> bool:
        try:
            supabase_client.table("user_preferences").upsert({
                "user_id": user_id,
                "favorite_genres": preferences.get("favorite_genres", []),
                "favorite_directors": preferences.get("favorite_directors", []),
                "favorite_actors": preferences.get("favorite_actors", []),
                "disliked_genres": preferences.get("disliked_genres", [])
            }).execute()
            return True
        
        except Exception as e:
            print("UPDATE PREFERENCES ERROR:", e)
            return False
        
profile_service = ProfileService()
