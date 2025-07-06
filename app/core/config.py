"""
Application configuration module.

This module defines the settings for the application, including database connection,
JWT configuration, and other application-specific settings.
"""

import os
from datetime import timedelta
from typing import Any, Dict, Optional

from pydantic_settings import BaseSettings
from pydantic import validator


class Settings(BaseSettings):
    """
    Application settings.
    
    Attributes:
        PROJECT_NAME: Name of the project
        API_V1_STR: API version prefix
        SECRET_KEY: Secret key for JWT token generation
        ACCESS_TOKEN_EXPIRE_MINUTES: Expiration time for access tokens
        DATABASE_URL: Database connection URL
        TESTING: Flag to indicate if the application is in testing mode
    """

    PROJECT_NAME: str = "SimpleUser Management API"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "YOUR_SECRET_KEY_HERE"  # In production use another secure key
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15  # 15 minutes
    DATABASE_URL: str = "sqlite:///./app.db"
    
    # CORS settings
    BACKEND_CORS_ORIGINS: list[str] = ["*"]
    
    # Testing flag
    TESTING: bool = False
    
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: str | list[str]) -> list[str] | str:
        """
        Validate CORS origins.
        
        Args:
            v: CORS origins as string or list
            
        Returns:
            List of CORS origins
        """
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    class Config:
        """
        Pydantic config class.
        """
        case_sensitive = True
        env_file = ".env"


# Create settings instance
settings = Settings()
