"""
Security utilities for the application.

This module provides functions for password hashing, JWT token generation and validation.
"""

from datetime import datetime, timedelta
from typing import Any, Optional, Union

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against a hash.
    
    Args:
        plain_password: The plain-text password
        hashed_password: The hashed password
        
    Returns:
        bool: True if the password matches the hash
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash a password.
    
    Args:
        password: The password to hash
        
    Returns:
        str: The hashed password
    """
    return pwd_context.hash(password)


def create_access_token(
    subject: Union[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create a JWT access token.
    
    Args:
        subject: The subject of the token (typically user_id)
        expires_delta: Optional expiration time delta
        
    Returns:
        str: The encoded JWT token
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm="HS256"
    )
    return encoded_jwt


def create_user_token(user_id: int, email: str, last_name: str) -> str:
    """
    Create a JWT token with user information.
    
    Args:
        user_id: The user's ID
        email: The user's email
        last_name: The user's last name
        
    Returns:
        str: The encoded JWT token
    """
    expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.utcnow() + expires_delta
    
    to_encode = {
        "exp": expire,
        "sub": str(user_id),
        "email": email,
        "last_name": last_name
    }
    
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm="HS256"
    )
    return encoded_jwt
