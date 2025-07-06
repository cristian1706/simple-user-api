"""
Authentication tests module.

This module contains tests for authentication-related functionality.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.session import Base
from app.main import app
from app.core.config import settings
from app.db.session import get_db

# Set testing flag to True to bypass rate limiting
settings.TESTING = True


# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Override the get_db dependency
def override_get_db():
    """
    Override the get_db dependency for testing.
    
    Yields:
        Session: A SQLAlchemy session for testing
    """
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="module")
def client():
    """
    Create a test client.
    
    Yields:
        TestClient: A FastAPI test client
    """
    # Create the database tables
    Base.metadata.create_all(bind=engine)
    
    # Create a test client
    with TestClient(app) as c:
        yield c
    
    # Drop the database tables
    Base.metadata.drop_all(bind=engine)


def test_register_user(client):
    """
    Test user registration.
    
    Args:
        client: Test client
    """
    # Test data
    user_data = {
        "email": "test@example.com",
        "first_name": "Test",
        "last_name": "User",
        "password": "password123"
    }
    
    # Send registration request
    response = client.post(
        f"{settings.API_V1_STR}/auth/register",
        json=user_data,
    )
    
    # Check response
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_register_existing_user(client):
    """
    Test registering a user with an existing email.
    
    Args:
        client: Test client
    """
    # Test data
    user_data = {
        "email": "test@example.com",
        "first_name": "Test",
        "last_name": "User",
        "password": "password123"
    }
    
    # Send registration request (should fail)
    response = client.post(
        f"{settings.API_V1_STR}/auth/register",
        json=user_data,
    )
    
    # Check response
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "Email already registered" in data["detail"]


def test_login_user(client):
    """
    Test user login.
    
    Args:
        client: Test client
    """
    # Login data
    login_data = {
        "username": "test@example.com",
        "password": "password123"
    }
    
    # Send login request with content-type application/json
    response = client.post(
        f"{settings.API_V1_STR}/auth/login",
        json=login_data,
        headers={"Content-Type": "application/json"}
    )
    
    # Check response
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
