import os
import logging
from supabase import create_client, Client
from dotenv import load_dotenv

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

async def get_profile(profile_id: str):
    try:
        response = supabase.table("profiles").select("*").eq("id", profile_id).single().execute()
        return response.data
    except Exception as e:
        logger.error(f"Error fetching profile {profile_id}: {str(e)}")
        raise

async def create_profile(profile_data: dict):
    try:
        response = supabase.table("profiles").insert(profile_data).execute()
        return response.data[0]
    except Exception as e:
        logger.error(f"Error creating profile: {str(e)}")
        raise

async def search_profiles(query: str):
    try:
        response = supabase.table("profiles").select("*").execute()
        return response.data
    except Exception as e:
        logger.error(f"Error searching profiles: {str(e)}")
        raise 