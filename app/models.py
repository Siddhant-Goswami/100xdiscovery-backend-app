from typing import List, Optional, Dict, Any
from pydantic import BaseModel, field_validator, EmailStr, Field
from pydantic.networks import HttpUrl

class AuthRequest(BaseModel):
    """
    Authentication request data for signup and login endpoints.
    """
    email: EmailStr = Field(..., description="User's email address for authentication")
    password: str = Field(..., description="User's password (min 6 characters)")

class AuthResponse(BaseModel):
    """
    Authentication response containing user data and access token.
    """
    message: str = Field(..., description="Response message indicating the result of the authentication request")
    user: Dict[str, Any] = Field(..., description="User details from Supabase including id, email, and metadata")
    access_token: Optional[str] = Field(None, description="JWT access token for authenticated requests (only provided on login)")

    @classmethod
    def from_supabase_response(cls, message: str, user: Any, access_token: Optional[str] = None):
        # Convert Supabase user object to dictionary
        user_dict = {
            "id": str(user.id),
            "email": user.email,
            "email_confirmed": user.email_confirmed_at is not None,
            "last_sign_in": user.last_sign_in_at,
            "created_at": user.created_at,
            "app_metadata": user.app_metadata,
            "user_metadata": user.user_metadata
        }
        return cls(message=message, user=user_dict, access_token=access_token)

class UserProfileCreate(BaseModel):
    """
    Data required to create or update an engineer profile.
    """
    name: str = Field(..., description="Full name of the engineer")
    skills: List[str] = Field(..., description="List of technical skills and competencies")
    bio: str = Field(..., description="Brief professional biography or introduction")
    projects: List[str] = Field(..., description="List of notable projects or achievements")
    collaboration_interests: List[str] = Field(..., description="Areas of interest for collaboration")
    portfolio_url: str = Field(..., description="URL to the engineer's portfolio or professional website")

    @field_validator('portfolio_url')
    def validate_url(cls, v):
        # This will raise an error if the URL is invalid
        HttpUrl(v)
        return v

class UserProfile(UserProfileCreate):
    """
    Complete engineer profile including system-managed fields.
    """
    id: str = Field(..., description="Unique identifier for the profile")
    email: Optional[str] = Field(None, description="Associated email address (optional for existing profiles)")
    user_id: Optional[str] = Field(None, description="Associated user ID (optional for existing profiles)")

    class Config:
        from_attributes = True

class SearchQuery(BaseModel):
    """
    Search query for finding relevant engineer profiles.
    """
    query: str = Field(..., description="Natural language search query to find matching profiles") 