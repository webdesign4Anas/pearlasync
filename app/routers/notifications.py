from fastapi import Depends,HTTPException,status,APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,Result
from app.database import get_db
from app import oauth2,schemas,models
from app.services import notifications_service
router=APIRouter(tags=["Notifications"])
#retrieve all notifications for specefic BO
@router.get("/notifications",status_code=status.HTTP_200_OK,response_model=list[schemas.NotificationsOut])
async def get_notifications(db:AsyncSession=Depends(get_db),owner:models.Users=Depends(oauth2.require_paid_business_owner)):
   return await notifications_service.get_business_owner_notification(owner,db)


#mark specefic notification as read
@router.put("/notifications/{notification_id}/mark-read",status_code=status.HTTP_200_OK)
async def mark_as_read(notification_id:int,db:AsyncSession=Depends(get_db),owner:models.Users=Depends(oauth2.require_paid_business_owner)):
    notification_result:Result=await db.execute(select(models.Notification).where(models.Notification.business_owner_id==owner.id,models.Notification.id==notification_id))
    notification:models.Notification=notification_result.scalar_one_or_none()
    if not notification:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="notification not found")
    notification.is_read=True
    await db.commit()
    return {"status":"marked_as_read"}



  