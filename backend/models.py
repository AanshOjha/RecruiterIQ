# Pydantic models for API requests and responses

from pydantic import BaseModel

class LoginRequest(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class RegisterRequest(BaseModel):
    email: str
    password: str
    role: str  # "admin", "recruiter", or "hiring_manager"

class UserResponse(BaseModel):
    id: str
    email: str
    role: str
    created_at: str
    message: str