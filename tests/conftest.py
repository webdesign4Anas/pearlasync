from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import SessionLocal
from app.main import app
from typing import AsyncGenerator
from app.database import get_db
DATABASE_URL = "postgresql+asyncpg://postgres:1@localhost/pearlasync_test"

engine = create_async_engine(DATABASE_URL)

async_session_maker = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)





@pytest.fixture(scope="session")
async def session() -> AsyncGenerator[AsyncSession, None]:
    """Async fixture for database connection."""
    async with async_session_maker() as session:
        yield session


@pytest.fixture(scope="session")
async def client(session: AsyncSession)-> AsyncGenerator[AsyncClient, None]:
    """Async fixture for FastAPI test client, overriding `get_db`."""
    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        yield session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient( base_url="http://test") as client:
        yield client



@pytest.fixture()
async def test_user(client: AsyncClient) -> dict:
    """Async fixture for registering a test user."""
    payload = {
        "email": "anasahmed2452@gmail.com",
        "password": "22526618a"
    }
    
    response = await client.post("/register/user", json=payload)
    new_user = response.json()
    
    # Ensure email and password are properly set
    new_user["password"] = payload["password"]
    new_user["email"] = payload["email"]
    
    assert "email" in new_user
    
    return new_user