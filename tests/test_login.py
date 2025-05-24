import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_login(client: AsyncClient, test_user: dict):
    """Test async login route."""
    payload = {
        "username": test_user["email"],
        "password": test_user["password"]
    }

    # Use data for form-encoded (OAuth2 style) or json for JSON body
    response = await client.post("/login", data=payload)

    assert response.status_code == 201, f"Login failed: {response.text}"
    json_response = response.json()
    assert "access_token" in json_response
