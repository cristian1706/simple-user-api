"""
User schemas module.

This module defines Pydantic schemas for user-related operations.
"""

from typing import Optional

from pydantic import BaseModel, EmailStr, Field, validator


class UserBase(BaseModel):
    """
    Base user schema with common attributes.
    
    Attributes:
        email: User's email address
        first_name: User's first name
        last_name: User's last name
    """
    
    email: EmailStr
    first_name: str
    last_name: str


class UserCreate(UserBase):
    """
    Schema for creating a new user.
    
    Attributes:
        password: User's password
    """
    
    password: str = Field(..., min_length=8)
    
    @validator('password')
    def password_strength(cls, v):
        """
        Validate password strength.
        
        Args:
            v: Password value
            
        Returns:
            str: Validated password
            
        Raises:
            ValueError: If password is too weak
        """
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v


class UserUpdate(BaseModel):
    """
    Schema for updating a user.
    
    Attributes:
        first_name: User's first name
        last_name: User's last name
        phone: User's phone number
    """
    
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None


class UserInDBBase(UserBase):
    """
    Base schema for user in database.
    
    Attributes:
        id: User's ID
        is_active: Whether the user is active
    """
    
    id: int
    is_active: bool
    
    class Config:
        """
        Pydantic config class.
        """
        
        orm_mode = True


class User(UserInDBBase):
    """
    Schema for user response.
    
    Attributes:
        phone: User's phone number
    """
    
    phone: Optional[str] = None


class UserInDB(UserInDBBase):
    """
    Schema for user in database with hashed password.
    
    Attributes:
        hashed_password: User's hashed password
    """
    
    hashed_password: str
