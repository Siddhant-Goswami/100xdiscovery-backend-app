# 100xEngineers Discovery Platform API Specification

Base URL: `https://overwhelming-georgetta-100xengineers-391a6937.koyeb.app/api`

## Authentication
The API uses Supabase email authentication. All endpoints (except authentication endpoints) require a valid JWT token.

### Authentication Headers
Include the JWT token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

## Authentication Endpoints

### 1. Sign Up
Create a new user account.

**Endpoint:** `POST /auth/signup`

**Request Body:**
```json
{
    "email": "user@example.com",
    "password": "your_password"
}
```

**Success Response (200 OK):**
```json
{
    "message": "Signup successful. Please check your email for verification.",
    "user": {
        "id": "user_id",
        "email": "user@example.com",
        // other user details
    }
}
```

### 2. Login
Authenticate and get access token.

**Endpoint:** `POST /auth/login`

**Request Body:**
```json
{
    "email": "user@example.com",
    "password": "your_password"
}
```

**Success Response (200 OK):**
```json
{
    "message": "Login successful",
    "user": {
        "id": "user_id",
        "email": "user@example.com",
        // other user details
    },
    "access_token": "your_jwt_token"
}
```

## Protected Endpoints

All the following endpoints require authentication. Include the JWT token in the Authorization header.

### 1. Create User Profile
Create a new user profile in the platform.

**Endpoint:** `POST /profiles`

**Request Body:**
```json
{
    "name": "string",
    "skills": ["string"],
    "bio": "string",
    "projects": ["string"],
    "collaboration_interests": ["string"],
    "portfolio_url": "string (valid URL)"
}
```

**Example Request:**
```json
{
    "name": "John Doe",
    "skills": ["Python", "FastAPI", "React", "Node.js"],
    "bio": "Full-stack developer with 5 years of experience",
    "projects": ["E-commerce Platform", "AI Chat Application"],
    "collaboration_interests": ["Open Source", "AI/ML Projects"],
    "portfolio_url": "https://johndoe.dev"
}
```

**Success Response (200 OK):**
```json
{
    "id": "uuid-string",
    "email": "user@example.com",
    "name": "John Doe",
    "skills": ["Python", "FastAPI", "React", "Node.js"],
    "bio": "Full-stack developer with 5 years of experience",
    "projects": ["E-commerce Platform", "AI Chat Application"],
    "collaboration_interests": ["Open Source", "AI/ML Projects"],
    "portfolio_url": "https://johndoe.dev"
}
```

**Error Responses:**
- `401 Unauthorized`: Invalid or missing authentication token
- `400 Bad Request`: Invalid data format or validation error
- `500 Internal Server Error`: Server-side error

### 2. Get All Profiles
Retrieve all user profiles.

**Endpoint:** `GET /profiles`

**Success Response (200 OK):**
```json
[
    {
        "id": "uuid-string",
        "name": "string",
        "skills": ["string"],
        "bio": "string",
        "projects": ["string"],
        "collaboration_interests": ["string"],
        "portfolio_url": "string"
    }
]
```

**Error Response:**
- `500 Internal Server Error`: Server-side error

### 3. Get Profile by ID
Retrieve a specific user profile by ID.

**Endpoint:** `GET /profiles/{profile_id}`

**Parameters:**
- `profile_id`: UUID string

**Success Response (200 OK):**
```json
{
    "id": "uuid-string",
    "name": "string",
    "skills": ["string"],
    "bio": "string",
    "projects": ["string"],
    "collaboration_interests": ["string"],
    "portfolio_url": "string"
}
```

**Error Responses:**
- `404 Not Found`: Profile not found
- `500 Internal Server Error`: Server-side error

### 4. Search Profiles
Search for profiles using natural language queries.

**Endpoint:** `POST /search`

**Request Body:**
```json
{
    "query": "string"
}
```

**Example Queries:**
- "Find developers with machine learning experience"
- "Show me full-stack developers with React experience"
- "Find people interested in blockchain projects"

**Success Response (200 OK):**
```json
[
    {
        "id": "uuid-string",
        "reason": "string explaining why this profile matches"
    }
]
```

**Example Response:**
```json
[
    {
        "id": "e873b4d1-f5c3-4e0b-900f-9290c290f50a",
        "reason": "This profile has machine learning listed as a skill, and the bio mentions AI/ML engineering."
    }
]
```

**Error Response:**
- `400 Bad Request`: Invalid query format
- `500 Internal Server Error`: Server-side error

## Data Validation Rules

1. **Name**: Required string
2. **Skills**: Non-empty array of strings
3. **Bio**: Required string
4. **Projects**: Array of strings
5. **Collaboration Interests**: Array of strings
6. **Portfolio URL**: Valid HTTPS URL

## Rate Limiting
Currently, no rate limiting is implemented.

## Error Response Format
All error responses follow this format:
```json
{
    "detail": "Error message describing what went wrong"
}
```

## Notes for Frontend Integration

1. **URL Handling**: Ensure portfolio URLs are valid HTTPS URLs
2. **Search Functionality**: 
   - The search is powered by Groq LLM and supports natural language queries
   - Results include matching profiles with explanations
3. **Error Handling**: 
   - Implement proper error handling for all status codes
   - Display appropriate user feedback for validation errors

## Example Frontend Implementation

```typescript
// Example TypeScript interface for Profile and Auth
interface Profile {
    id?: string;
    email?: string;
    name: string;
    skills: string[];
    bio: string;
    projects: string[];
    collaboration_interests: string[];
    portfolio_url: string;
}

interface AuthRequest {
    email: string;
    password: string;
}

interface AuthResponse {
    message: string;
    user: any;
    access_token?: string;
}

// Example API calls using fetch
const api = {
    async signup(data: AuthRequest): Promise<AuthResponse> {
        const response = await fetch('/api/auth/signup', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        if (!response.ok) throw new Error('Signup failed');
        return response.json();
    },

    async login(data: AuthRequest): Promise<AuthResponse> {
        const response = await fetch('/api/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        if (!response.ok) throw new Error('Login failed');
        return response.json();
    },

    async createProfile(profile: Profile, token: string): Promise<Profile> {
        const response = await fetch('/api/profiles', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(profile)
        });
        if (!response.ok) throw new Error('Failed to create profile');
        return response.json();
    },

    async getAllProfiles(token: string): Promise<Profile[]> {
        const response = await fetch('/api/profiles', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        if (!response.ok) throw new Error('Failed to fetch profiles');
        return response.json();
    },

    async searchProfiles(query: string, token: string): Promise<Array<{id: string, reason: string}>> {
        const response = await fetch('/api/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ query })
        });
        if (!response.ok) throw new Error('Search failed');
        return response.json();
    }
};
``` 