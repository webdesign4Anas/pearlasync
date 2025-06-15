from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories import users_repository

async def list_user_purchases(db: AsyncSession, user_id: int):
    return await users_repository.get_user_purchases(db, user_id)
