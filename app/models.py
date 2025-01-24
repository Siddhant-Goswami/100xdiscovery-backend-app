from typing import List
from pydantic import BaseModel, field_validator
from pydantic.networks import HttpUrl

class UserProfileCreate(BaseModel):
    name: str
    skills: List[str]
    bio: str
    projects: List[str]
    collaboration_interests: List[str]
    portfolio_url: str

    @field_validator('portfolio_url')
    def validate_url(cls, v):
        # This will raise an error if the URL is invalid
        HttpUrl(v)
        return v

class UserProfile(UserProfileCreate):
    id: str

    class Config:
        from_attributes = True

class SearchQuery(BaseModel):
    query: str 