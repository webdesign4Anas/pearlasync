from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app import models

async def get_user_by_email(email:str,db:AsyncSession):
    existing_email=await db.scalar(select(models.Users).where(models.Users.email==email))
    return existing_email