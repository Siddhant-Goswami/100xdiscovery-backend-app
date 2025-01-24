from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from . import models, database, search

app = FastAPI(title="100xEngineers Discovery Platform")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/profiles", response_model=models.UserProfile)
async def create_profile(profile: models.UserProfileCreate):
    try:
        profile_dict = profile.model_dump()
        created_profile = await database.create_profile(profile_dict)
        return created_profile
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/profiles", response_model=list[models.UserProfile])
async def get_profiles():
    try:
        profiles = await database.get_all_profiles()
        return profiles
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/profiles/{profile_id}", response_model=models.UserProfile)
async def get_profile(profile_id: str):
    try:
        profile = await database.get_profile(profile_id)
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")
        return profile
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/search")
async def search_profiles(query: models.SearchQuery):
    try:
        # Get all profiles first
        profiles = await database.get_all_profiles()
        
        # Use Groq LLM to search through profiles
        search_results = await search.search_with_llm(query.query, profiles)
        return search_results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 