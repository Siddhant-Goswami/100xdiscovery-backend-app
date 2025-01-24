from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from supabase.client import Client
import jwt
from typing import Optional
from .database import supabase

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Optional[str]:
    """
    Validate JWT token and return user email
    """
    try:
        token = credentials.credentials
        # Verify the JWT token using Supabase's JWT secret
        user = supabase.auth.get_user(token)
        return user.user.email
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) 