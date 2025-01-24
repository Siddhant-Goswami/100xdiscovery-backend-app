# 100xEngineers Discovery Platform Backend

A FastAPI backend for the 100xEngineers Discovery Platform, featuring user profiles and LLM-powered search functionality.

## Features

- User profile management (CRUD operations)
- Natural language search using Groq LLM
- Supabase integration for data storage

## Tech Stack

- FastAPI
- Supabase
- Groq LLM
- Python 3.8+

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Copy `.env.example` to `.env` and fill in your credentials:
   ```bash
   cp .env.example .env
   ```

5. Run the development server:
   ```bash
   uvicorn app.main:app --reload
   ```

## API Endpoints

- `POST /api/profiles` - Create new profile
- `GET /api/profiles` - List all profiles
- `GET /api/profiles/{id}` - Get specific profile
- `POST /api/search` - Search profiles using natural language

## Environment Variables

- `SUPABASE_URL`: Your Supabase project URL
- `SUPABASE_KEY`: Your Supabase anonymous key
- `GROQ_API_KEY`: Your Groq API key

## Database Setup

Create the following table in your Supabase database:

```sql
create table profiles (
  id uuid default uuid_generate_v4() primary key,
  name text not null,
  skills text[] not null,
  bio text not null,
  projects text[] not null,
  collaboration_interests text[] not null,
  portfolio_url text not null,
  created_at timestamp with time zone default timezone('utc'::text, now()) not null
);
```