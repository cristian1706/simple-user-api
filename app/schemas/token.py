"""
Token schemas module.

This module defines Pydantic schemas for token-related operations.
"""

from typing import Optional

from pydantic import BaseModel, Field


class Token(BaseModel):
    """
    Schema for access token.
    
    Attributes:
        access_token: JWT access token
        token_type: Token type (bearer)
    """
    
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    """
    Schema for token payload.
    
    Attributes:
        sub: Subject (user ID)
        email: User's email
        last_name: User's last name
        exp: Expiration time
    """
    
    sub: Optional[str] = None
    email: Optional[str] = None
    last_name: Optional[str] = None
    exp: Optional[int] = None


class LoginRequest(BaseModel):
    """
    Schema for login request.
    
    Attributes:
        username: User's email address
        password: User's password
    """
    
    username: str
    password: str = Field(..., min_length=1)
