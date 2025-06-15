from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app import models

async def get_user_purchases(db: AsyncSession, user_id: int):

    result=await db.scalars(select(models.Purchase).where(models.Purchase.user_id==user_id))
    
    return result
