# conftest.py

import pytest
import pytest_asyncio
from typing import AsyncGenerator

from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.config import settings
from app.database import Base, get_db
from app.main import app

# Create the engine once for the entire test session
@pytest.fixture(scope="session")
def engine():
    db_url = f"postgresql+asyncpg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"
    return create_async_engine(db_url)

# Create the session maker, also once for the session
@pytest.fixture(scope="session")
def TestingSessionLocal(engine):
    return async_sessionmaker(autocommit=False, autoflush=False, bind=engine)

# This is the critical fixture. It runs for each test function.
@pytest_asyncio.fixture(scope="function")
async def session(engine, TestingSessionLocal) -> AsyncGenerator[AsyncSession, None]:
    # --- Setup ---
    # Create a new connection for the setup phase
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # --- Test Execution ---
    # Create a session to be used by the test
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        # --- Teardown ---
        await db.close()

# Client fixture remains the same
@pytest_asyncio.fixture(scope="function")
async def client(session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_db():
        yield session

    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    del app.dependency_overrides[get_db]

# User creation fixtures remain the same
@pytest_asyncio.fixture
async def test_user(client: AsyncClient):
    payload = {"email": "testuser@example.com", "password": "password123"}
    response = await client.post("/register/user", json=payload)
    assert response.status_code == 201, f"Failed to create user. Response: {response.text}" # Add a helpful message
    
    new_user = response.json()
    new_user["password"] = payload["password"]
    new_user["email"] = payload["email"]
    return new_user

@pytest_asyncio.fixture
async def test_business_owner(client: AsyncClient):
    payload = {
        "email": "testbusiness@example.com",
        "password": "password123",
        "business_type": "MAKEUP_ARTIST",
        "business_name": "Glamour Inc.",
        "description": "The best makeup services."
    }
    response = await client.post("/register/business", json=payload)
    assert response.status_code == 201, f"Failed to create business owner. Response: {response.text}" # Add helpful message
    
    new_user = response.json()
    new_user["password"] = payload["password"]
    new_user["email"] = payload["email"]
    return new_user