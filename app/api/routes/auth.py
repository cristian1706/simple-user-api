"""
Authentication routes module.

This module defines the API routes for authentication operations.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from app.core.rate_limiter import register_rate_limit
from app.core.security import create_user_token, get_password_hash, verify_password
from app.db.session import get_db
from app.models.user import User
from app.schemas.token import Token, LoginRequest
from app.schemas.user import UserCreate

router = APIRouter()


@router.post("/register", response_model=Token)
@register_rate_limit()
async def register(
    user_in: UserCreate, db: Session = Depends(get_db), request: Request = None
) -> Token:
    """
    Register a new user.
    
    Args:
        user_in: User creation data
        db: Database session
        request: Request object for rate limiting
        
    Returns:
        Token: JWT token for the new user
        
    Raises:
        HTTPException: If email already exists
    """
    # Check if user with this email already exists
    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    
    # Create new user
    db_user = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        first_name=user_in.first_name,
        last_name=user_in.last_name,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Create access token
    access_token = create_user_token(
        user_id=db_user.id, email=db_user.email, last_name=db_user.last_name
    )
    
    return Token(access_token=access_token, token_type="bearer")


@router.post("/login", response_model=Token)
async def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db),
) -> Token:
    """
    Login for access token.
    
    Args:
        login_data: Login request with username and password
        db: Database session
        
    Returns:
        Token: JWT token for the user
        
    Raises:
        HTTPException: If credentials are invalid
    """
    # Find user by email
    user = db.query(User).filter(User.email == login_data.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    
    # Verify password
    if not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    
    # Create access token
    access_token = create_user_token(
        user_id=user.id, email=user.email, last_name=user.last_name
    )
    
    return Token(access_token=access_token, token_type="bearer")
