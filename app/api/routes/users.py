"""
User routes module.

This module defines the API routes for user operations.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import User as UserSchema, UserUpdate

router = APIRouter()


@router.get("/me", response_model=UserSchema)
async def read_users_me(current_user: User = Depends(get_current_user)) -> UserSchema:
    """
    Get current user information.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        UserSchema: Current user information
    """
    return current_user


@router.put("/me", response_model=UserSchema)
async def update_user_me(
    user_in: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> UserSchema:
    """
    Update current user information.
    
    Args:
        user_in: User update data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        UserSchema: Updated user information
    """
    # Update user fields if provided
    if user_in.first_name is not None:
        current_user.first_name = user_in.first_name
    if user_in.last_name is not None:
        current_user.last_name = user_in.last_name
    if user_in.phone is not None:
        current_user.phone = user_in.phone
    
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    
    return current_user


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_me(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    """
    Delete current user.
    
    Args:
        db: Database session
        current_user: Current authenticated user
    """
    db.delete(current_user)
    db.commit()
