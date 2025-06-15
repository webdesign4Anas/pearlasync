from fastapi import Depends,status,APIRouter,Query
from sqlalchemy.ext.asyncio import AsyncSession

from  app.database import get_db
from app import schemas,models,oauth2
from typing import Optional,List
from app.services import admin_services



router=APIRouter(prefix="/admin",tags=["Admin"])

#retrieve all users for admin
@router.get("/users",status_code=status.HTTP_200_OK,response_model=list[schemas.UserOut])
async def retireve_all_users(
    db:AsyncSession=Depends(get_db),
    admin:models.Users=Depends(oauth2.require_admin_user),
    role:Optional[str]=Query(None),
    is_active:Optional[bool]=Query(None),
    skip:int=0 ,
    limit:int=20,
    ):
   return await admin_services.get_all_users(db,role,is_active,skip,limit)



#retrieve all payments for admin
@router.get("/payments",status_code=status.HTTP_200_OK,response_model=List[schemas.PaymentOut])
async def get_all_payments(
    db:AsyncSession=Depends(get_db),
    admin:models.Users=Depends(oauth2.require_admin_user),
    status:Optional[str]=Query(None),
    payment_type:Optional[str]=Query(None),
    skip:int=0 ,
    limit:int=20,
):
  return await admin_services.get_all_payments(db,status,payment_type,skip,limit)




#retrieve all business_owner
@router.get("/business_owners",response_model=list[schemas.BusinessOwnersOut],status_code=status.HTTP_200_OK)
async def get_all_business_owners(
    db:AsyncSession=Depends(get_db),
    admin:models.Users=Depends(oauth2.require_admin_user),
    status:Optional[str]=Query(None),
    business_type:Optional[str]=Query(None),
    skip:int=0 ,
    limit:int=20,
):
    return await admin_services.get_all_business_owners(db,status,business_type,skip,limit)




#Blocking User
@router.put("/users/{user_id}/block",status_code=status.HTTP_200_OK)
async def block_user(
    user_id:int,
    db:AsyncSession=Depends(get_db),
    admin:models.Users=Depends(oauth2.require_admin_user),
):
    return await admin_services.block_user(user_id,db)


#Un-Blocking User
@router.put("/users/{user_id}/unblock",status_code=status.HTTP_200_OK)
async def unblock_user(
    user_id:int,
    db:AsyncSession=Depends(get_db),
    admin:models.Users=Depends(oauth2.require_admin_user),
):
   return await admin_services.unblock_user(user_id,db)




#reviewing all revenues
@router.get("/revenues", status_code=status.HTTP_200_OK)
async def get_all_revenues(
    db: AsyncSession = Depends(get_db),
    admin: models.Users = Depends(oauth2.require_admin_user),
):
    return await admin_services.get_revenue_summary(db)