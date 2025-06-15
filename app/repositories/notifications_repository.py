from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app import models



# query to get all the notifications for specefic business_owner

async def get_notifications_by_owner(owner:models.BusinessOwners,db:AsyncSession):
    business_owner=await db.scalars(select(models.Notification).where(models.Notification.business_owner_id==owner.id).order_by(models.Notification.created_at.desc()))

    return business_owner



# query to get (SPECEFIC) the notifications for specefic business_owner
async def get_notifications_by_owner_and_id(id:int,owner:models.BusinessOwners,db:AsyncSession):
    specefic_notification=await db.scalar(select(models.Notification).where(models.Notification.business_owner_id==owner.id,models.Notification.id==id))

    return specefic_notification




