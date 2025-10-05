from fastapi import FastAPI, HTTPException, Depends, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager

# Local imports
from database import get_db, create_tables, User, UserRole, verify_password, hash_password
from auth import create_access_token, verify_token, create_admin_user, verify_admin_token
from models import LoginRequest, Token, RegisterRequest, UserResponse

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    create_tables()
    db = next(get_db())
    try:
        create_admin_user(db)
    finally:
        db.close()
    
    yield
    
    # Shutdown and cleanup (later)

# Initialize FastAPI app
app = FastAPI(title="RecruiterIQ API", lifespan=lifespan)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "http://127.0.0.1:3000", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def home():
    """Health check endpoint"""
    return {
        "message": "Welcome to RecruiterIQ API!",
        "status": "running"
    }

@app.post('/login')
def login(login_data: LoginRequest, response: Response, db: Session = Depends(get_db)):
    # Find user by email
    user = db.query(User).filter(User.email == login_data.email).first()
    
    # Check if user exists and password is correct
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=401, 
            detail="Incorrect email or password"
        )
    
    # Create access token
    access_token = create_access_token(data={"sub": user.email, "role": user.role.value})
    
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,        # ← False for localhost
        samesite="lax",
        max_age=1800
    )

    # Return user info so frontend knows login was successful
    return {
        "message": "Login successful",
        "user": {
            "email": user.email,
            "role": user.role.value
        }
    }

@app.post('/logout')
def logout(response: Response):
    response.delete_cookie(
        key="access_token",
        httponly=False,
        secure=False,
        samesite="lax"
    )
    return {"message": "Logged out successfully"}


@app.post('/register', response_model=UserResponse)
def register(register_data: RegisterRequest, admin_user: User = Depends(verify_admin_token), db: Session = Depends(get_db)):
    """Register new user - Admin only"""
    
    # Validate role
    valid_roles = ["admin", "recruiter", "hiring_manager"]
    if register_data.role not in valid_roles:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid role. Must be one of: {', '.join(valid_roles)}"
        )
    
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == register_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=400, 
            detail="User with this email already exists"
        )
    
    # Create new user
    hashed_password = hash_password(register_data.password)
    new_user = User(
        email=register_data.email,
        hashed_password=hashed_password,
        role=UserRole[register_data.role]  # Convert string to enum
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return UserResponse(
        id=str(new_user.id),
        email=new_user.email,
        role=new_user.role.value,
        created_at=new_user.created_at.isoformat(),
        message="User created successfully"
    )

@app.get('/protected')
def protected_route(current_user_email: str = Depends(verify_token)):
    """Example protected route"""
    return {
        "message": "This is a protected route",
        "user": current_user_email
    }

