# test_login.py

import pytest
from httpx import AsyncClient

# The @pytest.mark.asyncio decorator tells pytest to run this as an async test
@pytest.mark.asyncio
async def test_user_login(client: AsyncClient, test_user: dict):
    """Test successful login for a standard user."""
    login_data = {
        "username": test_user["email"],
        "password": test_user["password"]
    }
    
    # API calls with httpx.AsyncClient must be awaited
    response = await client.post("/login", data=login_data)
    
    assert response.status_code == 201
    
    token_data = response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"
    assert token_data["role"] == "USER"
    assert token_data["id"] == test_user["id"]

@pytest.mark.asyncio
async def test_business_owner_login(client: AsyncClient, test_business_owner: dict):
    """Test successful login for a business owner."""
    login_data = {
        "username": test_business_owner["email"],
        "password": test_business_owner["password"]
    }
    
    response = await client.post("/login", data=login_data)
    
    assert response.status_code == 201
    
    token_data = response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"
    assert token_data["role"] == "BUSINESS_OWNER"
    assert token_data["id"] == test_business_owner["id"]

@pytest.mark.asyncio
async def test_login_with_wrong_password(client: AsyncClient, test_user: dict):
    """Test that login fails with an incorrect password."""
    login_data = {
        "username": test_user["email"],
        "password": "wrongpassword" # Incorrect password
    }
    response = await client.post("/login", data=login_data)
    
    # Your login route correctly raises a 403 FORBIDDEN error
    assert response.status_code == 403
    assert response.json()["detail"] == "credentials not matched"

@pytest.mark.asyncio
async def test_login_with_nonexistent_user(client: AsyncClient):
    """Test that login fails for a user that does not exist."""
    login_data = {
        "username": "nonexistent@example.com",
        "password": "password123"
    }
    response = await client.post("/login", data=login_data)
    
    assert response.status_code == 403
    assert response.json()["detail"] == "credentials not matched"