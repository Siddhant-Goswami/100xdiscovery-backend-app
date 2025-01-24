import os
import logging
from supabase import create_client, Client
from dotenv import load_dotenv
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Missing Supabase credentials in environment variables")

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    logger.info("Successfully connected to Supabase")
except Exception as e:
    logger.error(f"Failed to connect to Supabase: {str(e)}")
    raise

async def get_all_profiles():
    try:
        response = supabase.table("profiles").select("*").execute()
        return response.data
    except Exception as e:
        logger.error(f"Error fetching profiles: {str(e)}")
        raise

async def get_profile(profile_id: str) -> Optional[dict]:
    """
    Get a profile by ID.
    Returns None if no profile is found.
    """
    try:
        response = supabase.table("profiles").select("*").eq("id", profile_id).single().execute()
        return response.data
    except postgrest.exceptions.APIError as e:
        if "PGRST116" in str(e):  # No rows found
            return None
        logger.error(f"API Error fetching profile {profile_id}: {str(e)}")
        raise e
    except Exception as e:
        logger.error(f"Error fetching profile {profile_id}: {str(e)}")
        raise e

async def get_profile_by_email(email: str):
    try:
        response = supabase.table("profiles").select("*").eq("email", email).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        logger.error(f"Error fetching profile by email {email}: {str(e)}")
        raise

async def create_profile(profile_data: dict):
    try:
        # Check if user already has a profile
        if "email" in profile_data:
            existing_profile = await get_profile_by_email(profile_data["email"])
            if existing_profile:
                raise ValueError("User already has a profile")
        
        response = supabase.table("profiles").insert(profile_data).execute()
        return response.data[0]
    except Exception as e:
        logger.error(f"Error creating profile: {str(e)}")
        raise

async def update_profile(profile_id: str, profile_data: dict):
    try:
        # Get existing profile to check if it has email
        existing_profile = await get_profile(profile_id)
        if not existing_profile:
            raise ValueError("Profile not found")
        
        # Only update allowed fields
        allowed_fields = ["name", "skills", "bio", "projects", "collaboration_interests", "portfolio_url"]
        update_data = {k: v for k, v in profile_data.items() if k in allowed_fields}
        
        response = supabase.table("profiles").update(update_data).eq("id", profile_id).execute()
        return response.data[0]
    except Exception as e:
        logger.error(f"Error updating profile: {str(e)}")
        raise

async def delete_profile(profile_id: str):
    try:
        response = supabase.table("profiles").delete().eq("id", profile_id).execute()
        return response.data[0]
    except Exception as e:
        logger.error(f"Error deleting profile: {str(e)}")
        raise

async def search_profiles(query: str):
    try:
        response = supabase.table("profiles").select("*").execute()
        return response.data
    except Exception as e:
        logger.error(f"Error searching profiles: {str(e)}")
        raise 