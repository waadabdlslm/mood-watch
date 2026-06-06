'''This module handles user signup and login using Supabase for authentication.
It validates API requests using Pydantic models defined in app/schemas/models.py and returns authentication responses containing access tokens and user information.'''

from fastapi import APIRouter, HTTPException 
from app.schemas.models import SignUpRequest, LoginRequest, AuthResponse
from app.database.supabase_client import supabase_client

'''The APIRouter is configured with a prefix of "/auth" and tagged as "Authentication" for better organization in API documentation.'''
router = APIRouter(prefix="/auth", tags=["Authentication"])

'''The signup endpoint allows users to register by providing an email, username, and password. 
It validates the input using the SignUpRequest model and interacts with Supabase to create a new user. 
If the signup is successful, it returns an AuthResponse containing the access token and user information. 
If the signup fails (e.g., due to an existing email or invalid password), it raises an HTTPException with an appropriate error message.'''

@router.post("/signup", response_model=AuthResponse)
async def signup(request: SignUpRequest):
    try: 
        response = supabase_client.auth.sign_up({
            "email": request.email,
            "password": request.password,
            "options": {
            "data": {"username": request.username}
            }
        })

        if not response.user:
            raise HTTPException(
                status_code=400, 
                detail="Signup failed")
        
        if not response.session:
            raise HTTPException(
                status_code=201, 
                detail="Account created. Please check your email for confirmation.")
        
        return AuthResponse(
            access_token=response.session.access_token,
            user_id=str(response.user.id),
            username=request.username
        )
    except HTTPException: 
        raise
    except Exception as e:
        print("SUPABASE SIGNUP ERROR:", e)
    
        raise HTTPException(
            status_code=400, 
            detail=str(e))

'''The login endpoint allows users to authenticate by providing their email and password.
It validates the input using the LoginRequest model and interacts with Supabase to verify the credentials.
If the login is successful, it returns an AuthResponse containing the access token and user information.
If the login fails (e.g., due to invalid credentials), it raises an HTTPException with an appropriate error message.'''

@router.post("/login", response_model=AuthResponse)
async def login(request: LoginRequest):
    try:
        response = supabase_client.auth.sign_in_with_password({
            "email": request.email,
            "password": request.password
        })

        if not response.user:
            raise HTTPException(
                status_code=401, 
                detail="Invalid credentials")
        
        profile = (
            supabase_client
            .table("profiles")
            .select("username")
            .eq("id", str(response.user.id))
            .single()
            .execute()
        )
        
        return AuthResponse(
            access_token=response.session.access_token,
            user_id=str(response.user.id),
            username=(profile.data.get("username") if profile.data else None)
        )
    except Exception:
        raise
        
    except Exception as e:
        print("LOGIN ERROR:", e)
        raise HTTPException(
            status_code=401, 
            detail=str(e)
            )