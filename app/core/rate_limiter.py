"""
Rate limiting utilities for the application.

This module provides decorators and functions for implementing rate limiting on API endpoints.
"""

from functools import wraps
from typing import Callable

from fastapi import Request
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.core.config import settings

# Initialize rate limiter
# This instance should be used throughout the application
limiter = Limiter(key_func=get_remote_address)


def rate_limit(limit_value: str) -> Callable:
    """
    Decorator for applying rate limiting to API endpoints.
    
    Args:
        limit_value: The rate limit value (e.g., "3/minute")
        
    Returns:
        Callable: Decorator function
    """
    def decorator(func: Callable) -> Callable:
        # Skip rate limiting if in testing mode
        if settings.TESTING:
            @wraps(func)
            async def wrapper(*args, **kwargs):
                return await func(*args, **kwargs)
            return wrapper
        else:
            @limiter.limit(limit_value)
            @wraps(func)
            async def wrapper(*args, **kwargs):
                return await func(*args, **kwargs)
            return wrapper
    return decorator


# Specific rate limit for registration endpoint
def register_rate_limit() -> Callable:
    """
    Decorator for applying rate limiting to the registration endpoint.
    Limits to 3 requests per minute.
    
    Returns:
        Callable: Decorator function
    """
    return rate_limit("3/minute")
