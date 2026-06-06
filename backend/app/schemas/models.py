''''This module defines the Pydantic models used in the application. 
It contains request and response models for user authentication, movie recommendations, user preferences, and feedback. 
These models ensure data validation and provide a clear structure for API interactions. 
Furthermore, this layer acts as a contract between the frontend, FastAPI routes, database services, and ML pipeline.'''

'''The models defined in this module include:'''
from pydantic import BaseModel, EmailStr, Field, field_validator       
import re
from typing import Optional, List
from enum import Enum

'''- SignUpRequest: Model for user registration, validating email, username, and password with specific criteria.'''
class SignUpRequest(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, 
                          max_length=30, 
                          pattern=r'^[a-zA-Z0-9_]+$')
    password: str = Field(min_length=8)

    @field_validator("password")
    @classmethod
    def validate_password(cls, value) -> str:
        if not re.search(r'[A-Z]', value):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r'[a-z]', value):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r'[0-9]', value):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r'[!@#$%&*_]', value):
            raise ValueError("Password must contain at least one special character")
        return value

'''- LoginRequest: Model for user login, validating email and password.'''
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

'''- AuthResponse: Model for authentication response, containing access token and user information.'''
class AuthResponse(BaseModel):
    access_token: str
    user_id : str
    username: Optional[str] = None

'''- MoodEnum: Enumeration for user moods, used in recommendation requests.'''
class MoodEnum(str, Enum):
    happy = "happy"
    sad = "sad"
    stressed = "stressed"
    anxious = "anxious"
    excited = "excited"
    nostalgic = "nostalgic"
    calm = "calm"
    whimsical = "whimsical"

'''- EnergyEnum: Enumeration for user energy levels, used in recommendation requests.'''
class EnergyEnum(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

'''- FeedbackType: Enumeration for feedback types, used in feedback requests.'''
class FeedbackType(str, Enum):
    like = "like"
    love = "love"
    ok = "ok"
    dislike = "dislike"
    save = "save"
    watched = "watched"

'''- FavoriteMovieRequest: Model for adding a movie to user's favorites, containing the TMDB movie ID.'''
class FavoriteMovieRequest(BaseModel):
    tmdb_id: int

'''- UserPreferencesRequest: Model for user preferences, containing lists of favorite and disliked genres, directors, and actors.'''
class UserPreferencesRequest(BaseModel):
    favorite_genres: Optional[List[str]] = None
    favorite_directors: Optional[List[str]] = None
    favorite_actors: Optional[List[str]] = None
    disliked_genres: Optional[List[str]] = None

'''- RecommendationRequest: Model for movie recommendation requests, containing mood, energy level, intent, and user preferences.'''
class RecommendationRequest(BaseModel):
    mood: MoodEnum
    energy: EnergyEnum
    intent: Optional[str] = None
    preferences: Optional[UserPreferencesRequest] = None
     
'''- MovieRecommendation: Model for movie recommendations, containing movie details and recommendation explanation.'''
class MovieRecommendation(BaseModel):
    tmdb_id: int
    title: str
    poster_path: Optional[str] = None
    overview: Optional[str] = None
    release_date: Optional[str] = None
    genres: List[str] = Field(default_factory=list)
    explanation: str
    score : float 

'''- RecommendationResponse: Model for recommendation responses, containing a list of recommended movies and a session ID.'''
class RecommendationResponse(BaseModel):
    recommendations: List[MovieRecommendation]
    session_id: Optional[str] 

'''- ProfileResponse: Model for user profile responses, containing user information and preferences.'''
class ProfileResponse(BaseModel):
    id: str
    username: Optional[str]
    favorite_genres: List[str] = Field(default_factory=list)

'''- FeedbackRequest: Model for user feedback on movie recommendations, containing the movie ID and feedback type.'''
class FeedbackRequest(BaseModel):
    movie_id: int = Field(gt=0)
    feedback_type: FeedbackType