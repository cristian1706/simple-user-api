"""
User tests module.

This module contains tests for user-related functionality.
"""

import pytest
from fastapi.testclient import TestClient

from app.core.config import settings
from tests.test_auth import client  # Reuse the client fixture from test_auth.py


def get_user_token(client, email_suffix=""):
    """
    Helper function to register a user and get a token.
    
    Args:
        client: Test client
        email_suffix: Suffix to make email unique
        
    Returns:
        str: Bearer token for authentication
    """
    # Test data for user registration
    user_data = {
        "email": f"user_test{email_suffix}@example.com",
        "first_name": "User",
        "last_name": "Test",
        "password": "password123"
    }
    
    # Register user
    response = client.post(
        f"{settings.API_V1_STR}/auth/register",
        json=user_data,
    )
    
    # Check response status
    assert response.status_code == 200, f"Registration failed with status {response.status_code}: {response.text}"
    
    # Get token
    data = response.json()
    assert "access_token" in data, f"access_token not found in response: {data}"
    token = data["access_token"]
    
    return f"Bearer {token}"


def test_read_users_me(client):
    """
    Test getting current user information.
    
    Args:
        client: Test client
    """
    # Get token
    token = get_user_token(client, email_suffix="_read")
    
    # Send request to get user info
    response = client.get(
        f"{settings.API_V1_STR}/users/me",
        headers={"Authorization": token},
    )
    
    # Check response
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "user_test_read@example.com"
    assert data["first_name"] == "User"
    assert data["last_name"] == "Test"
    assert "id" in data
    assert data["is_active"] is True


def test_update_user_me(client):
    """
    Test updating current user information.
    
    Args:
        client: Test client
    """
    # Get token
    token = get_user_token(client, email_suffix="_update")
    
    # Update data
    update_data = {
        "first_name": "Updated",
        "last_name": "Name",
        "phone": "123-456-7890"
    }
    
    # Send request to update user
    response = client.put(
        f"{settings.API_V1_STR}/users/me",
        headers={"Authorization": token},
        json=update_data,
    )
    
    # Check response
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "Updated"
    assert data["last_name"] == "Name"
    assert data["phone"] == "123-456-7890"
    
    # Verify changes by getting user info
    response = client.get(
        f"{settings.API_V1_STR}/users/me",
        headers={"Authorization": token},
    )
    
    # Check response
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "Updated"
    assert data["last_name"] == "Name"
    assert data["phone"] == "123-456-7890"


def test_delete_user_me(client):
    """
    Test deleting current user.
    
    Args:
        client: Test client
    """
    # Get token
    token = get_user_token(client, email_suffix="_delete")
    
    # Send request to delete user
    response = client.delete(
        f"{settings.API_V1_STR}/users/me",
        headers={"Authorization": token},
    )
    
    # Check response
    assert response.status_code == 204
    
    # Verify user is deleted by trying to get user info
    response = client.get(
        f"{settings.API_V1_STR}/users/me",
        headers={"Authorization": token},
    )
    
    # Check response (should be unauthorized or not found)
    assert response.status_code in [401, 403, 404]
