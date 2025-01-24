from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from . import models, database, search, auth
from typing import Optional

app = FastAPI(
    title="100xEngineers Discovery Platform",
    description="""
    The 100xEngineers Discovery Platform API enables users to create, manage, and discover engineering profiles.
    It supports both authenticated and unauthenticated access, with enhanced features for authenticated users.
    
    Key Features:
    * User Authentication (Signup/Login)
    * Profile Management (CRUD operations)
    * Profile Search with AI-powered matching
    """,
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/auth/signup", response_model=models.AuthResponse, 
    summary="Create a new user account",
    description="Register a new user with email and password. An email verification will be sent to complete the signup process.")
async def signup(auth_data: models.AuthRequest):
    try:
        response = database.supabase.auth.sign_up({
            "email": auth_data.email,
            "password": auth_data.password
        })
        return models.AuthResponse.from_supabase_response(
            message="Signup successful. Please check your email for verification.",
            user=response.user
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/auth/login", response_model=models.AuthResponse,
    summary="Authenticate user and get token",
    description="Login with email and password to receive an access token for authenticated requests.")
async def login(auth_data: models.AuthRequest):
    try:
        response = database.supabase.auth.sign_in_with_password({
            "email": auth_data.email,
            "password": auth_data.password
        })
        return models.AuthResponse.from_supabase_response(
            message="Login successful",
            user=response.user,
            access_token=response.session.access_token
        )
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/api/profiles", response_model=models.UserProfile,
    summary="Create a new profile",
    description="Create a new engineer profile. Requires authentication. The profile will be associated with the authenticated user's email.")
async def create_profile(
    profile: models.UserProfileCreate,
    current_user: str = Depends(auth.get_current_user)
):
    try:
        profile_dict = profile.model_dump()
        profile_dict["email"] = current_user
        created_profile = await database.create_profile(profile_dict)
        return created_profile
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/profiles", response_model=list[models.UserProfile],
    summary="List all profiles",
    description="Retrieve a list of all engineer profiles. Authentication is optional.")
async def get_profiles(current_user: Optional[str] = Depends(auth.get_current_user)):
    try:
        profiles = await database.get_all_profiles()
        return profiles
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/profiles/{profile_id}", response_model=models.UserProfile,
    summary="Get a specific profile",
    description="Retrieve details of a specific profile by ID. Authentication is optional.")
async def get_profile(
    profile_id: str,
    current_user: Optional[str] = Depends(auth.get_current_user)
):
    try:
        profile = await database.get_profile(profile_id)
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")
        return profile
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/profiles/{profile_id}", response_model=models.UserProfile,
    summary="Update a profile",
    description="Update an existing profile. Requires authentication. Users can only update their own profiles.")
async def update_profile(
    profile_id: str,
    profile: models.UserProfileCreate,
    current_user: str = Depends(auth.get_current_user)
):
    try:
        existing_profile = await database.get_profile(profile_id)
        if not existing_profile:
            raise HTTPException(status_code=404, detail="Profile not found")
        
        if existing_profile.get("email"):
            if existing_profile["email"] != current_user:
                raise HTTPException(status_code=403, detail="Not authorized to update this profile")
        
        profile_dict = profile.model_dump()
        updated_profile = await database.update_profile(profile_id, profile_dict)
        return updated_profile
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/profiles/{profile_id}",
    summary="Delete a profile",
    description="Delete an existing profile. Requires authentication. Users can only delete their own profiles.")
async def delete_profile(
    profile_id: str,
    current_user: str = Depends(auth.get_current_user)
):
    try:
        existing_profile = await database.get_profile(profile_id)
        if not existing_profile:
            raise HTTPException(status_code=404, detail="Profile not found")
        
        if existing_profile.get("email"):
            if existing_profile["email"] != current_user:
                raise HTTPException(status_code=403, detail="Not authorized to delete this profile")
        
        deleted_profile = await database.delete_profile(profile_id)
        return {"message": "Profile deleted successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/search",
    summary="Search profiles",
    description="Search for profiles using AI-powered matching. Accepts a search query and returns relevant profiles. Authentication is optional.")
async def search_profiles(
    query: models.SearchQuery,
    current_user: Optional[str] = Depends(auth.get_current_user)
):
    try:
        profiles = await database.get_all_profiles()
        search_results = await search.search_with_llm(query.query, profiles)
        return search_results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 