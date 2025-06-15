from fastapi import status,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories import notifications_repository
from app import models


async def get_business_owner_notification(owner:models.BusinessOwners,db):
    return await notifications_repository.get_notifications_by_owner(owner,db)



async def get_business_owner_specefi_notification(id,owner,db:AsyncSession):
    
    notification:models.Notification=notifications_repository.get_notifications_by_owner_and_id(id,owner,db)

    if not notification:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Notification not found")
    
    if notification.is_read:
        return{"status":"Already_read"}
    
    notification.is_read=True
    await db.commit()
    return {"status":"marked_as_read"}