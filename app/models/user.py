"""
User model module.

This module defines the SQLAlchemy model for the User entity.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func

from app.db.session import Base


class User(Base):
    """
    User model for storing user information.
    
    Attributes:
        id: Unique identifier for the user
        email: User's email address (unique)
        hashed_password: Hashed password
        first_name: User's first name
        last_name: User's last name
        phone: User's phone number (optional)
        is_active: Whether the user is active
        created_at: When the user was created
        updated_at: When the user was last updated
    """
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        """
        String representation of the User model.
        
        Returns:
            str: String representation
        """
        return f"<User {self.email}>"
