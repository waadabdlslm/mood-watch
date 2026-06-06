'''This module defines dependencies for the FastAPI application, including authentication and user retrieval. 
It uses HTTPBearer for token-based authentication and interacts with Supabase to validate user credentials and retrieve user information.'''

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.database.supabase_client import supabase_client

security = HTTPBearer()

'''The get_current_user function is a dependency that retrieves the current authenticated user based on the provided token.
It uses the HTTPBearer security scheme to extract the token from the request headers and then interacts with'''

async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict: 
    try:
        token = credentials.credentials
        user = supabase_client.auth.get_user(token)
        
        if not user or not user.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token"
            )

        return {
            "id": str(user.user.id), 
            "email": user.user.email
            }
    
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

