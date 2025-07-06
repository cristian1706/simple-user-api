"""
API dependencies module.

This module provides dependency functions for the API routes.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
from jose.exceptions import JWTError
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.models.user import User
from app.schemas.token import TokenPayload

security = HTTPBearer()


def get_current_user(
    db: Session = Depends(get_db), 
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> User:
    """
    Get the current user from the token.
    
    Args:
        db: Database session
        token: JWT token
        
    Returns:
        User: Current user
        
    Raises:
        HTTPException: If token is invalid or user not found
    """
    try:
        token = credentials.credentials
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=["HS256"]
        )
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    
    user = db.query(User).filter(User.id == token_data.sub).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )
    
    return user
