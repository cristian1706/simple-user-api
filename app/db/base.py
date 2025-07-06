"""
Database base module.

This module imports all SQLAlchemy models to ensure they are registered with the Base class.
"""

from app.db.session import Base
from app.models.user import User  # noqa
