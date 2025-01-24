import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("Missing Groq API key in environment variables")

client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """You are an AI assistant helping to search through user profiles based on natural language queries.
Your task is to analyze the profiles and return relevant matches based on the search criteria."""

FEW_SHOT_EXAMPLES = """
Query: "Find developers interested in AI and machine learning"
Relevant criteria: Look for skills in AI, ML, deep learning, or collaboration interests in AI projects

Query: "Show me full-stack developers with React experience"
Relevant criteria: Look for skills mentioning full-stack, React, web development

Query: "Find people interested in blockchain projects"
Relevant criteria: Look for blockchain skills, crypto projects, or Web3 collaboration interests
"""

async def search_with_llm(query: str, profiles: list) -> list:
    prompt = f"""{SYSTEM_PROMPT}

{FEW_SHOT_EXAMPLES}

Current query: "{query}"

Available profiles:
{profiles}

Return the IDs of the most relevant profiles that match the search criteria, along with a brief explanation of why each profile matches. Format your response as a Python list of dictionaries with 'id' and 'reason' keys."""

    completion = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=1000
    )

    try:
        # Parse the response and return matched profile IDs with reasons
        response = eval(completion.choices[0].message.content)
        return response
    except:
        # Fallback to returning all profiles if parsing fails
        return [{"id": profile["id"], "reason": "Fallback result"} for profile in profiles] 