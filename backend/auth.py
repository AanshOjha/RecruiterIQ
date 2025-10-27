# Authentication utilities and dependencies
from fastapi import HTTPException, Depends, Request, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session

from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, ADMIN_EMAIL, ADMIN_PASSWORD
from database import get_db, User, UserRole, hash_password

# Security
security = HTTPBearer()

def create_access_token(data: dict) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_cookie(request: Request, db: Session = Depends(get_db)) -> str:
    """Verify JWT token"""
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=401,
            detail="Authentication required"
        )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        verify_user = db.query(User).filter(User.email == email).first()
        if verify_user is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return verify_user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def create_admin_user(db: Session) -> None:
    # Create admin user if it doesn't exist
    if not ADMIN_EMAIL or not ADMIN_PASSWORD:
        print("Warning: ADMIN_EMAIL or ADMIN_PASSWORD not found in environment variables")
        return
    
    # Check if admin user already exists
    existing_admin = db.query(User).filter(User.email == ADMIN_EMAIL).first()
    if existing_admin:
        print(f"Admin user already exists: {ADMIN_EMAIL}")
        return
    
    # Create new admin user
    hashed_password = hash_password(ADMIN_PASSWORD)
    admin_user = User(
        email=ADMIN_EMAIL,
        hashed_password=hashed_password,
        role=UserRole.admin
    )
    
    db.add(admin_user)
    db.commit()
    print(f"Admin user created successfully: {ADMIN_EMAIL}")