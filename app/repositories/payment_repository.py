from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app import models


async def get_business_owner_by_id(owner_id:int,db:AsyncSession):
    business_owner=await db.scalar(select(models.BusinessOwners.id==owner_id))
    return business_owner




async def create_payment(payment:models.Payments,db:AsyncSession):
    db.add(payment)
    await db.flush()
    return payment